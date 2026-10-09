---
title: "News"
permalink: /news/
layout: single
author_profile: true
---

Milestones, publications and updates. Edit `_data/news.yml` to add an entry —
this page and the homepage both read from it.

{% assign items = site.data.news %}
{% if items and items.size > 0 %}
  <ol class="news-list">
    {% for item in items %}
      <li class="news-item">
        <span class="news-date">{{ item.date }}</span>
        <div class="news-body">
          <h2 class="news-title">{{ item.title }}</h2>
          <p class="news-desc">{{ item.description }}</p>
        </div>
      </li>
    {% endfor %}
  </ol>
{% else %}
  <p>No updates yet.</p>
{% endif %}

<style>
  .news-list{list-style:none;margin:1.5rem 0 0;padding:0}
  .news-item{display:grid;grid-template-columns:7.5rem 1fr;gap:1rem;padding:1rem 0;border-top:1px solid rgba(0,0,0,.1)}
  .news-date{font-size:.85em;font-weight:700;letter-spacing:.03em;text-transform:uppercase;opacity:.7;padding-top:.2em}
  .news-body p{margin:.25rem 0 0}
  .news-title{font-size:1.1em;margin:0;line-height:1.35}
  @media (max-width:600px){
    .news-item{grid-template-columns:1fr;gap:.25rem}
  }
  @media (prefers-color-scheme: dark){
    .news-item{border-top-color:rgba(255,255,255,.15)}
  }
</style>