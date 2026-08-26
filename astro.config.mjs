import { defineConfig } from 'astro/config';

// ─────────────────────────────────────────────────────────────
// Astro configuration
//
// `site` tells Astro your final URL so it can generate correct
// canonical links, sitemaps, and Open Graph URLs.
// Because abhishekajith.github.io is a USER site (repo name ==
// username.github.io), the site lives at the domain root — so no
// `base` value is needed. If you ever move to a PROJECT site
// (repo like `portfolio`), add:  base: '/portfolio'
// ─────────────────────────────────────────────────────────────
export default defineConfig({
  site: 'https://abhishekajith.github.io',
});
