---
layout: default
title: Home Page
---

Search: <input type="text" id="search-box" placeholder="Search posts...">
<ul id="results-container"></ul>

{% assign posts_by_year = site.posts | group_by_exp: "post", "post.date | date: '%Y'" %}
{% for year in posts_by_year %}
  <h2>{{ year.name }}</h2>
  <ul>
    {% assign sorted_year_posts = year.items | sort: "date" | reverse %}
    {% for post in sorted_year_posts %}
      <li>{{ post.date | date: "%b %e" }}: <a href="{{ post.url }}">{{ post.title }}</a></li>
    {% endfor %}
  </ul>
{% endfor %}


<script src="https://cdnjs.cloudflare.com/ajax/libs/lunr.js/2.3.9/lunr.min.js"></script>
<script src="/assets/js/search.js"></script>