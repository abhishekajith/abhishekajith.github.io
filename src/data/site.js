// ─────────────────────────────────────────────────────────────
// SITE-WIDE SETTINGS  ★EDIT HERE FIRST
// Values below flow into the nav, hero, and footer automatically.
// ─────────────────────────────────────────────────────────────

export const site = {
  // Browser tab title + SEO description
  title: 'Abhishek Ajith - Regenerative Biomaterials',
  description:
    'PhD researcher designing inherently radiopaque, biodegradable biomaterials for orthopaedic repair and locoregional cancer therapy.',

  // Your name as shown in the top-left logo. The <i> part gets the teal dot.
  logoHtml: 'Abhishek<i>.</i>Ajith',

  // Home lab badge in the hero (links out to the lab website)
  lab: {
    label: 'Regenerative Biomaterials · CUSAT',
    url: 'https://www.gssailaja.org/',
    title: 'Regenerative Biomaterials and Theranostics Laboratory',
  },

  // Hero headline. Use \n where you want a line break, and wrap the
  // gradient-highlighted words in *asterisks* (rendered italic + teal→green).
  headlineBefore: 'Living materials that',
  headlineAccent: 'heal',
  headlineAfter: ', see & disappear.',
  intro:
    'PhD researcher at the Regenerative Biomaterials and Theranostics Laboratory - designing inherently radiopaque, biodegradable implants for orthopaedic repair and locoregional cancer therapy.',

  // CV download path (prof_pic.jpg stays in /public as the favicon)
  cvUrl: '/cv/CV_Abhishek_A.pdf',
};
