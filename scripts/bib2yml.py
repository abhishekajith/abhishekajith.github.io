"""Convert _bibliography/references.bib into _data/publications.yml.

Why this exists: jekyll-scholar is not supported by GitHub Pages (per its
own README) and its bibtex-ruby dependency crashes on Ruby 3.x with
"tried to create Proc object without a block". So the .bib stays the single
source of truth, and this script renders it into something plain Liquid can
iterate - no gem required.

Usage:  python scripts/bib2yml.py
Run before `jekyll build`. The output is generated, so it is gitignored.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, '_bibliography', 'references.bib')
DST = os.path.join(ROOT, '_data', 'publications.yml')

MONTHS = {'jan', 'feb', 'mar', 'apr', 'may', 'jun',
          'jul', 'aug', 'sep', 'oct', 'nov', 'dec'}

# BibTeX-Ruby is not available here, so parse the subset of BibTeX that a
# hand-maintained academic bibliography actually uses.
ENTRY_RE = re.compile(r'@(\w+)\s*\{\s*([^,]+),', re.M)


def strip_comments(text):
    """Remove `%` comments. BibTeX-Ruby rejects them outright."""
    out, depth, i = [], 0, 0
    while i < len(text):
        ch = text[i]
        if ch == '\\':
            out.append(ch)
            if i + 1 < len(text):
                i += 1
                out.append(text[i])
        elif ch == '{':
            depth += 1
            out.append(ch)
        elif ch == '}':
            depth = max(0, depth - 1)
            out.append(ch)
        elif ch == '%':
            while i < len(text) and text[i] != '\n':
                i += 1
            out.append('\n')
        else:
            out.append(ch)
        i += 1
    return ''.join(out)


def read_value(src, start):
    """Read a braced / quoted / bare value plus any # concatenation."""
    val, k = '', start
    while k < len(src):
        while k < len(src) and src[k] in ' \t\r\n,':
            k += 1
        if k >= len(src):
            break
        if src[k] == '{':
            d, m = 1, k + 1
            while m < len(src) and d:
                d += (src[m] == '{') - (src[m] == '}')
                m += 1
            val += src[k + 1:m - 1]
            k = m
        elif src[k] == '"':
            m = k + 1
            while m < len(src) and src[m] != '"':
                m += 2 if src[m] == '\\' else 1
            val += src[k + 1:m]
            k = m + 1
        else:
            m = k
            while m < len(src) and src[m] not in ' \t\r\n,#':
                m += 1
            val += src[k:m]
            k = m
        p = k
        while p < len(src) and src[p] in ' \t\r\n':
            p += 1
        if p < len(src) and src[p] == '#':
            k = p + 1
            continue
        break
    return val, k


def parse_fields(body):
    fields, j = {}, 0
    while True:
        eq = body.find('=', j)
        if eq == -1:
            break
        name = body[j:eq].strip().lower()
        value, k = read_value(body, eq + 1)
        if name:
            fields[name] = value
        j = k
        while j < len(body) and body[j] != ',':
            j += 1
        j += 1
    return fields


def clean(s):
    return re.sub(r'\s+', ' ', s.replace('{', '').replace('}', '')).strip()


def split_authors(raw):
    """'Last, First and Last, First' -> [{last, first}, ...]"""
    out = []
    for a in re.split(r'\s+and\s+', raw, flags=re.I):
        a = clean(a)
        if not a:
            continue
        if ',' in a:
            last, first = a.split(',', 1)
            out.append({'last': last.strip(), 'first': first.strip()})
        else:
            parts = a.split()
            out.append({'last': parts[-1], 'first': ' '.join(parts[:-1])})
    return out


def yaml_quote(s):
    s = str(s).replace('\\', '\\\\').replace('"', '\\"')
    s = s.replace('\n', ' ').replace('\r', ' ')
    return f'"{s}"'


def main():
    if not os.path.exists(SRC):
        print(f"error: {SRC} not found")
        return 1

    raw = strip_comments(open(SRC, encoding='utf-8').read())

    # Drop the YAML front matter if present.
    if raw.startswith('---'):
        end = raw.find('\n---', 3)
        if end != -1:
            raw = raw[end + 4:]

    entries = []
    for m in ENTRY_RE.finditer(raw):
        kind, key = m.group(1).lower(), m.group(2).strip()
        # Field body runs to the matching closing brace of this entry.
        i, d = m.end(), 1
        while i < len(raw) and d:
            d += (raw[i] == '{') - (raw[i] == '}')
            i += 1
        body = raw[m.end():i - 1]
        f = parse_fields(body)

        title = clean(f.get('title', ''))
        if not title:
            continue

        venue = clean(f.get('journal') or f.get('booktitle') or f.get('publisher') or '')
        year_m = re.search(r'\d{4}', f.get('year', ''))

        entries.append({
            'key': key,
            'type': kind,
            'title': title,
            'authors': split_authors(f.get('author', '')),
            'venue': venue,
            'year': int(year_m.group()) if year_m else None,
            'volume': clean(f.get('volume', '')),
            'number': clean(f.get('number', '')),
            'pages': clean(f.get('pages', '')),
            'doi': clean(f.get('doi', '')),
            'url': clean(f.get('url', '')) or (
                f"https://doi.org/{clean(f.get('doi', ''))}" if f.get('doi') else ''),
            'keywords': [k.strip().lower()
                         for k in clean(f.get('keywords', '')).split(',') if k.strip()],
            'note': clean(f.get('note', '')),
            'annote': clean(f.get('annote', '')).lower() or 'published',
        })

    entries.sort(key=lambda e: (-(e['year'] or 0), e['title'].lower()))

    lines = [
        '# GENERATED FILE - do not edit.',
        '# Produced by scripts/bib2yml.py from _bibliography/references.bib.',
        '# Edit the .bib, then re-run the script (or let CI do it).',
        '',
    ]
    for e in entries:
        lines.append('- key: ' + yaml_quote(e['key']))
        lines.append('  title: ' + yaml_quote(e['title']))
        lines.append('  venue: ' + yaml_quote(e['venue']))
        lines.append('  year: ' + (str(e['year']) if e['year'] else '""'))
        lines.append('  volume: ' + yaml_quote(e['volume']))
        lines.append('  pages: ' + yaml_quote(e['pages']))
        lines.append('  doi: ' + yaml_quote(e['doi']))
        lines.append('  url: ' + yaml_quote(e['url']))
        lines.append('  note: ' + yaml_quote(e['note']))
        lines.append('  annote: ' + yaml_quote(e['annote']))
        if e['authors']:
            lines.append('  authors:')
            for a in e['authors']:
                lines.append('    - last: ' + yaml_quote(a['last']))
                lines.append('      first: ' + yaml_quote(a['first']))
        else:
            lines.append('  authors: []')
        lines.append('  keywords:')
        for k in e['keywords']:
            lines.append('    - ' + yaml_quote(k))
        if not e['keywords']:
            lines[-1] = '  keywords: []'
        lines.append('')

    with open(DST, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(lines))

    print(f'wrote {DST} with {len(entries)} entries')
    for e in entries:
        print(f"  - {e['year']}  {e['title'][:64]}")
    return 0


if __name__ == '__main__':
    sys.exit(main())