# abhishekajith.github.io

Personal academic website, built on the
[Academic Pages](https://github.com/academicpages/academicpages.github.io)
theme (Jekyll).

**Live site:** https://abhishekajith.github.io

## Pages

| Path | Source | Notes |
|---|---|---|
| `/about/` | `_pages/about.md` | Bio, background table, current work |
| `/research/` | `_pages/research.md` | Three research areas with figures, current projects |
| `/publications/` | `_pages/publications.html` | jekyll-scholar, filter by year + topic + free text |
| `/news/` | `_pages/news.md` | Renders `_data/news.yml` |
| `/cv/` | `_pages/cv.md` | Full CV, links to `/files/cv.pdf` |
| `/contact/` | `_pages/contact.md` | Links and collaboration interests |

Navigation order is set in `_data/navigation.yml`. Sidebar identity and social
links are in the `author:` block of `_config.yml`.

## Adding a publication

Append to **`_bibliography/references.bib`** — that is the only file you need to
touch. jekyll-scholar reads it and the `/publications` page re-renders on the
next build.

```bibtex
@article{yourkey2026,
  title     = {Title of the paper},
  author    = {Ajith, Abhishek and Doe, Jane},
  journal   = {Journal Name},
  year      = {2026},
  volume    = {00},
  pages     = {00--00},
  doi       = {10.0000/xxxxx},
  keywords  = {nanocellulose, brushite},
  annote    = {published}
}
```

- `keywords` — comma-separated; these populate the topic filter.
- `annote` — `published` (default), `under-review`, `in-press`, or `preprint`.
  Anything other than `published` shows a coloured badge.
- `note` — free text, shown under the authors (e.g. a manuscript ID).

Author names must match a key in `_data/authors.yml` for the sidebar profile
links to resolve.

A copy of the `.bib` is published at `/assets/bibliography.bib` for download. The
build workflow copies it there — do not commit a second copy.

## Adding news

Append to `_data/news.yml`, newest first. Both `/news/` and the homepage read it.

## Build and deploy

Pushes to `main` trigger `.github/workflows/deploy.yml`, which builds with Jekyll
and deploys to GitHub Pages. **You do not need Ruby installed locally to deploy.**

The workflow also copies `_bibliography/references.bib` to
`assets/bibliography.bib` before building, so the two never drift.

To preview locally you would need Ruby 3.3 + Bundler:

```bash
bundle install
bundle exec jekyll serve      # http://localhost:4000
```

## Validation

`jekyll build` cannot run in every environment, so the repo carries static
checks for the failures that would otherwise only show up in CI:

```bash
python scripts/validate.py
```

It verifies that

- every YAML file parses (`_config.yml`, `_data/*.yml`, workflows)
- Liquid block tags balance across pages, includes and layouts
- every nav URL resolves to a real page permalink
- referenced images and files exist on disk
- the bibliography parses and has entries
- every plugin enabled in `_config.yml` is actually provided by the Gemfile
  (directly, or via the `github-pages` meta-gem)

It exits non-zero on any error. Run it before every push.

## Replacing the placeholder figures

`images/research/*.svg` are **placeholder schematics**, labelled as such in the
image itself. Replace them with real FE-SEM, micro-CT or radiograph exports
using the same filenames — nothing else needs to change. 16:10 crops work best.

`images/profile.jpg` is the sidebar portrait.

## CV PDF

`files/cv.pdf` is a generated artefact. Regenerate it whenever you change the CV
page content, and keep it in sync manually — Jekyll does not build it.

## Notes

- **Why `jekyll-scholar` is in the Gemfile but plugins differ.** The
  `github-pages` meta-gem supplies the standard whitelisted plugins
  (`jekyll-gist`, `jekyll-paginate`, …) transitively, so they need no explicit
  Gemfile line. `jekyll-scholar` is *not* part of that set, hence the explicit
  entry.
- **Publications are a collection no more.** The theme's `_publications/*.md`
  sample files were removed in favour of the BibTeX pipeline.
- If the build fails on `jekyll-scholar`, it is a version conflict with
  `github-pages`. Check the Actions log — the fix is to pin compatible versions
  or drop the `github-pages` gem and list plugins individually.