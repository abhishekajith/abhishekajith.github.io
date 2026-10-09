"""Static checks for the Jekyll site.

No Ruby available locally, so `jekyll build` cannot run here. These checks
catch the failure modes that would otherwise only surface in CI:
malformed YAML, unbalanced Liquid tags, missing images, dead nav links.

Run from the repo root:  python scripts/validate.py
"""
import os
import re
import sys
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

errors = []
warnings = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


# ── 1. YAML ────────────────────────────────────────────────────────────
try:
    import yaml
except ImportError:
    yaml = None
    warn("PyYAML not installed - skipping YAML parse checks")

if yaml:
    yml_files = ["_config.yml"] + glob.glob("_data/*.yml") + \
        glob.glob(".github/workflows/*.yml")
    for f in yml_files:
        try:
            with open(f, encoding="utf-8") as fh:
                yaml.safe_load(fh)
            print(f"  ok   yaml parses: {f}")
        except Exception as e:
            err(f"yaml FAILED: {f}: {str(e)[:160]}")

    # Nav entries must point at a real page or permalink.
    try:
        nav = yaml.safe_load(open("_data/navigation.yml", encoding="utf-8"))
        pagemap = {}
        for p in glob.glob("_pages/*"):
            txt = open(p, encoding="utf-8").read()
            m = re.search(r"^permalink:\s*(\S+)", txt, re.M)
            if m:
                pagemap[m.group(1)] = p
        for item in nav["main"]:
            url = item["url"]
            if url not in pagemap:
                err(f"nav url {url} (-> {item['title']}) has no page with that permalink")
            else:
                print(f"  ok   nav {item['title']:<14} -> {pagemap[url]}")
    except Exception as e:
        err(f"navigation check failed: {e}")


# ── 2. Liquid tag balance ───────────────────────────────────────────────
PAIRS = {
    "if": "endif", "unless": "endunless", "for": "endfor",
    "comment": "endcomment", "capture": "endcapture",
    "raw": "endraw", "tablerow": "endtablerow",
    "case": "endcase", "highlight": "endhighlight",
}
OPENERS = set(PAIRS)

page_files = glob.glob("_pages/*.md") + glob.glob("_pages/*.html") + \
    glob.glob("_includes/*.html") + glob.glob("_layouts/*.html")

for f in page_files:
    txt = open(f, encoding="utf-8").read()
    stack = []
    for tag in re.findall(r"\{%-?\s*(\w+)", txt):
        if tag in OPENERS:
            stack.append(tag)
        elif tag.startswith("end"):
            want = tag[3:]
            if not stack:
                err(f"{f}: stray {{% {tag} %}} with nothing open")
            elif stack[-1] != want:
                err(f"{f}: {{% {tag} %}} closes {{% {stack[-1]} %}}")
                stack.pop()
            else:
                stack.pop()
    if stack:
        err(f"{f}: unclosed Liquid tag(s): {stack}")
    elif not any(True for _ in re.finditer(r"\{%-?\s*\w", txt)):
        pass
    else:
        print(f"  ok   liquid balanced: {f}")


# ── 3. Front matter ─────────────────────────────────────────────────────
# A layout that does not exist renders the page with NO layout at all: no
# head, no sidebar, no CSS. Silent in the build, obvious on the page.
layouts = {os.path.splitext(f)[0] for f in os.listdir("_layouts")
           if os.path.isfile(os.path.join("_layouts", f))}
print(f"\n  layouts available: {', '.join(sorted(layouts))}")

for p in glob.glob("_pages/*.md") + glob.glob("_pages/*.html"):
    txt = open(p, encoding="utf-8").read()
    if not txt.startswith("---"):
        err(f"{p}: missing YAML front matter")
        continue
    end = txt.find("\n---", 3)
    if end == -1:
        err(f"{p}: front matter never closed")
        continue
    fm = txt[3:end]
    if "layout:" not in fm:
        # Legitimate: _config.yml `defaults` assigns layout: single to pages.
        warn(f"{p}: no explicit layout (falls back to _config defaults)")
    else:
        # A layout that does not exist renders the page with NO layout at all:
        # no head, no sidebar, no CSS. Silent in the build, obvious on the page.
        lay = re.search(r"^layout:\s*(\S+)", fm, re.M)
        if lay and lay.group(1) not in layouts:
            err(f"{p}: layout '{lay.group(1)}' does not exist in _layouts "
                f"(available: {', '.join(sorted(layouts)) or 'none'})")
    if "permalink:" not in fm:
        warn(f"{p}: no permalink (will live at /{os.path.basename(p)}/)")


# ── 3c. Encoding ───────────────────────────────────────────────────────
# Mojibake: UTF-8 bytes decoded as cp1252 then re-encoded. A PowerShell
# round-trip with -Encoding UTF8 will do this silently, and it ships.
ENCODED_FILES = (glob.glob("_pages/*.md") + glob.glob("_pages/*.html")
                 + glob.glob("_data/*.yml") + ["_config.yml"]
                 + ["_bibliography/references.bib"])
for f in ENCODED_FILES:
    raw = open(f, "rb").read()
    if raw.startswith(b"\xef\xbb\xbf"):
        err(f"{f}: has a UTF-8 BOM (breaks YAML front matter parsing)")
    try:
        t = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        err(f"{f}: not valid UTF-8: {e}")
        continue
    moji = t.count("\u00e2\u20ac") + t.count("\ufffd")
    if moji:
        err(f"{f}: {moji} mojibake sequence(s) - smart quotes/dashes were "
            f"double-encoded. Rewrite the file as UTF-8.")

# ── 3d. Bibliography must satisfy jekyll-scholar's parser ─────────────
# jekyll-scholar converts every .bib it finds using BibTeX-Ruby, which:
#   - requires YAML front matter on the file
#   - rejects `%` comments outright (ParseError, build aborts)
#   - chokes on any duplicate .bib elsewhere in the source tree
bib = "_bibliography/references.bib"
if os.path.exists(bib):
    raw = open(bib, encoding="utf-8").read()
    if not raw.startswith("---"):
        err(f"{bib}: missing YAML front matter - jekyll-scholar will not parse it "
            f"and the publications page renders empty")
    pct = [i + 1 for i, ln in enumerate(raw.splitlines()) if ln.lstrip().startswith("%")]
    if pct:
        err(f"{bib}: '%' comments on line(s) {pct[:5]} - BibTeX-Ruby raises "
            f"ParseError on these and the BUILD FAILS")
    entries = re.findall(r"^@\w+\{", raw, re.M)
    if not entries:
        err(f"{bib}: no @entries found")
    else:
        print(f"  ok   bib: {len(entries)} entries, front matter present, no % comments")

# Any other .bib in the source tree will also be parsed by jekyll-scholar.
stray = [p for p in glob.glob("**/*.bib", recursive=True)
         if p.replace("\\", "/") != bib and not p.startswith(("_site", "node_modules", "vendor"))]
if stray:
    err(f"stray .bib file(s) that jekyll-scholar will also try to parse: {stray}")

# ── 4. Images referenced actually exist ─────────────────────────────────
for f in glob.glob("_pages/*.md") + glob.glob("_data/*.yml") + ["_config.yml"]:
    txt = open(f, encoding="utf-8").read()
    for ref in re.findall(r"(?:src=|\]\(|avatar\s*:\s*)[\"']?(/(?:images|files|assets)/[^\"'\s)]+)", txt):
        if ref.startswith("/assets/"):
            continue  # generated at build time
        if not os.path.exists(ref.lstrip("/")):
            err(f"{f}: references missing asset {ref}")


# ── 5. Bibliography sanity ─────────────────────────────────────────────
try:
    bib = open("_bibliography/references.bib", encoding="utf-8").read()
    entries = re.findall(r"^@\w+\{\s*([^,]+),", bib, re.M)
    print(f"  ok   bibliography: {len(entries)} entries -> {', '.join(e.strip() for e in entries)}")
    for e in entries:
        if f"{{{e.strip()}," not in bib and f"{{{e.strip()}" not in bib:
            err(f"bibliography: malformed entry {e}")
    if not entries:
        err("bibliography: no entries parsed")
except FileNotFoundError:
    err("bibliography: _bibliography/references.bib missing")


# ── 6. Gemfile / plugin parity ─────────────────────────────────────────
# Direction matters: gems in the :jekyll_plugins group are auto-loaded by
# Jekyll, so they need no _config.yml entry. But anything _config.yml enables
# MUST be in the Gemfile or the build cannot load it.
gemfile = open("Gemfile", encoding="utf-8").read()
config = open("_config.yml", encoding="utf-8").read()
gems = set(re.findall(r"gem '([a-z0-9_-]+)'", gemfile))

# The `github-pages` meta-gem pulls in every plugin GitHub Pages whitelists,
# so anything it provides is present even without an explicit Gemfile line.
GITHUB_PAGES_PROVIDED = {
    "jekyll-gist", "jekyll-paginate", "jekyll-feed", "jekyll-sitemap",
    "jekyll-redirect-from", "jemoji", "jekyll-default-layout",
    "jekyll-readme-index", "jekyll-titles-from-headings",
    "jekyll-relative-links", "jekyll-optional-front-matter",
    "jekyll-html-compressor", "jekyll-commonmark-ghpages",
}

for plugin in sorted(set(re.findall(r"^\s*-\s*(jekyll-[a-z0-9-]+)\s*$", config, re.M))):
    if plugin in gems:
        source = "Gemfile"
    elif "github-pages" in gems and plugin in GITHUB_PAGES_PROVIDED:
        source = "github-pages gem"
    else:
        err(f"_config.yml enables '{plugin}' but nothing provides it")
        continue
    print(f"  ok   plugin wired: {plugin:<22} (via {source})")

if "jekyll-scholar" in gems and "jekyll-scholar" not in config:
    warn("Gemfile has jekyll-scholar but _config.yml does not list it (still loads via the plugins group)")

# ── report ─────────────────────────────────────────────────────────────
print()
for w in warnings:
    print(f"  warn {w}")
for e in errors:
    print(f"  FAIL {e}")
print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
sys.exit(1 if errors else 0)