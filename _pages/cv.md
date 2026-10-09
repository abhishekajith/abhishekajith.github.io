---
layout: archive
title: "CV"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% include base_path %}

Download: **[PDF version](/files/cv.pdf)**

---

## Education

**PhD - Regenerative Biomaterials and Theranostics**
Cochin University of Science and Technology · 2026 – ongoing
Doctoral research on radiopaque biodegradable biomaterials for orthopaedic
repair and locoregional cancer therapy.

**M.Tech. Polymer Technology** - CGPA 8.52/10.00
Cochin University of Science and Technology · Aug 2020 – Aug 2022
Secured 1st position in the 2020–22 batch.

**M.Sc. Biopolymer Science** - CGPA 8.76/10.00
CIPET: Institute of Petrochemicals Technology · Jul 2017 – Jun 2019

**B.Sc. Chemistry** - CGPA 8.70/10.00
Mahatma Gandhi University · Jul 2014 – May 2017

## Experience

**Junior Research Fellow**
Department of Polymer Science and Rubber Technology, CUSAT · Jul 2023 – Mar 2026
Worked on *"Development of Inherently Radiopaque Biodegradable and Cost Effective
TACE System with Liver Regeneration Potential for The Treatment of
Hepatocellular Carcinoma"* under Prof. G. S. Sailaja. Developed a natural
radiopaque component using nanocellulose extracted from *Agave sisalana* and
prepared drug-eluting chemotherapeutic porous microspheres.

**Project Officer**
Department of Metallurgical and Materials Engineering, IIT Madras · Nov 2022 – Jul 2023
NPOL–DRDO funded project. Prepared specialty interpenetrating polymer network
(IPN) coatings for underwater sound damping. Characterised samples via ATR FT-IR
and dynamic mechanical analysis. Designed and built a custom water-filled
impedance tube for underwater impedance testing.

**Postgraduate Research Assistant**
Department of Polymer Science and Rubber Technology, CUSAT · Dec 2020 – Aug 2022
Worked on moldable osteoinductive bone graft formulations from
bioglass-intercalated quaternised chitosan–sodium alginate polyelectrolyte
complexes. Synthesised and characterised PECs, performed in vitro biological
characterisation (MTT, Actin–DAPI) and bone regeneration marker studies. Also
worked on phosphorylated nanocellulose and intrinsically radiopaque bone
cements.

**Project Trainee**
Department of Biological Sciences and Bioengineering, IIT Kanpur · Dec 2018 – May 2019
Developed photo-polymerising injectable hydrogels for improved cartilage repair.
Methacrylated gelatin, carboxymethyl cellulose and silk fibroin to give Gel-MA,
CMC-MA and Silk-MA. Photo-crosslinked in the presence of LAP under blue light.
Characterised for cell biocompatibility, degradation, compressive strength and
porosity.

## Publications

{% assign entries = site.data.bibliography.entries %}
{% if entries and entries.size > 0 %}
  <ol class="cv-pubs">
    {% for e in entries %}
      <li>
        {% for a in e.author %}{{ a.last }}{% if a.first %}, {{ a.first }}{% endif %}{% unless forloop.last %}; {% endunless %}{% endfor %}.
        <em>{{ e.title }}</em>.
        {% if e.venue %}{{ e.venue }}{% if e.pages %}, {{ e.pages }}{% endif %}{% endif %}{% if e.year %} ({{ e.year }}){% endif %}{% if e.doi %}.
        <a href="https://doi.org/{{ e.doi }}">doi:{{ e.doi }}</a>{% endif %}.
      </li>
    {% endfor %}
  </ol>
{% endif %}

## Technical skills

**Material synthesis** - polymer synthesis and modification; biopolymers from
agro-waste; nanocellulose extraction and phosphorylation; bioglass, hydroxyapatite,
brushite; self-setting bone cements; quantum dots and radiopaque fillers;
interpenetrating polymer networks; photo-crosslinkable hydrogels (Gel-MA, CMC-MA,
Silk-MA).

**Characterisation** - ATR FT-IR; thermogravimetric analysis; dynamic mechanical
analysis; FE-SEM; universal testing machine; in vitro biomimetic mineralisation;
swelling and degradation studies; UV/Vis spectrophotometry.

**Biology & computation** - L929 fibroblast cell culture; MTT cytotoxicity assay;
Actin–DAPI staining; bone regeneration marker studies; underwater impedance
testing; Python, OriginPro, image analysis.

**Languages** - English (professional), Malayalam (native), Hindi (communicative).

<style>
  .cv-pubs{padding-left:1.2em}
  .cv-pubs li{margin-bottom:.5em}
</style>