---
layout: default
title: Welcome
---

This is the online archive of our family blog, The Paladinos.

Search: <input type="text" id="search-box" placeholder="Search posts...">
<ul id="results-container"></ul>

{% assign posts_by_year = site.posts | group_by_exp: "post", "post.date | date: '%Y'" %}
{% for year in posts_by_year %}
  <h2>{{ year.name }}</h2>
  <ul>
    {% assign sorted_year_posts = year.items | sort: "date" | reverse %}
    {% for post in sorted_year_posts %}
      <li>{{ post.date | date: "%b %e" }}: <a href="/thepaladinos{{ post.url }}">{{ post.title }}</a></li>
    {% endfor %}
  </ul>
{% endfor %}


<script src="https://cdnjs.cloudflare.com/ajax/libs/lunr.js/2.3.9/lunr.min.js"></script>
<script src="/thepaladinos/assets/js/search.js"></script>