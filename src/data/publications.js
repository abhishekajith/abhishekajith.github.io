// ─────────────────────────────────────────────────────────────
// PUBLICATIONS  ★EDIT
// status: 'review' → teal “Under review” pill
//         'published' → green “Published” pill
//         any other string is shown verbatim (e.g. 'Book chapter')
// The homepage shows the first `FEATURED` entries;
// /publications lists everything, newest year first.
// ─────────────────────────────────────────────────────────────

export const FEATURED = 2;

export const publications = [
  {
    year: 2026,
    title:
      'Early Biomineralizing Radiopaque Phosphorylated Nanocellulose Intercalated Brushite Self-Setting Composites for Periodontal Regeneration',
    authors:
      'Sneha K.R., Ajith A., Muhammed Musthafa C.P., Cheemadan S., Sailaja G.S.',
    venue: 'Ceramics International',
    status: 'review',
    url: '', // add a DOI link when available, e.g. 'https://doi.org/10.xxxx'
  },
  {
    year: 2026,
    title: 'Reclaimed Wastewater in the Semiconductor Industry',
    authors: 'Ambakkattu A.R., Ajith A., Mathew J.',
    venue: 'Handbook of Environmental Chemistry, Springer',
    status: 'Book chapter',
    url: 'https://doi.org/10.1007/698_2026_1270',
  },
];
