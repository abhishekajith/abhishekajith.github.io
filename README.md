# Abhishek Ajith — Portfolio (Astro)

Personal academic website built with [Astro](https://astro.build).
Design: "Living Cells" concept (Concept D) — organic style, teal/green
palette, dark-mode-first, animated cell hero.

## Commands

```bash
npm install     # once, after cloning
npm run dev     # local dev server → http://localhost:4321
npm run build   # static output → dist/
npm run preview # serve dist/ locally to check before deploy
```

## Where things live

| What you want to change            | File                                  |
| ---------------------------------- | ------------------------------------- |
| Site title / lab link / CV path    | `src/data/site.js`                    |
| Research project cards             | `src/data/research.js`                |
| Publications                       | `src/data/publications.js`            |
| News / milestones timeline         | `src/data/news.js`                    |
| Colors (light + dark themes)       | `src/styles/global.css` → ★EDIT-COLORS|
| Fonts                              | `src/layouts/BaseLayout.astro`        |
| Cell animation tuning              | `src/scripts/cells.js` → ★EDIT-CELLS  |
| Portrait photo                     | `public/prof_pic.jpg`                 |
| CV PDF                             | `public/cv/CV_Abhishek_A.pdf`         |

All content data is plain JavaScript arrays with comments — edit values,
save, and the dev server hot-reloads instantly.
