let idx = null;
let documents = [];

fetch('/thepaladinos/search.json')
  .then(response => response.json())
  .then(data => {
    documents = data;
    idx = lunr(function () {
      this.ref('url');
      this.field('title');
      this.field('content');

      documents.forEach(doc => this.add(doc));
    });
  });

document.getElementById('search-box').addEventListener('input', function () {
  const query = this.value.trim();
  const resultsContainer = document.getElementById('results-container');
  resultsContainer.innerHTML = '';

  if (!query || !idx) return;

  const results = idx.search(query);
  results.forEach(result => {
    const match = documents.find(d => d.url === result.ref);
    const li = document.createElement('li');
    li.innerHTML = `<a href="/thepaladinos/${match.url}">${match.title}</a>`;
    resultsContainer.appendChild(li);
  });
});
