'use strict';
// Progressive enhancement only. Every exhibit and source is ordinary static HTML.
const context = document.querySelector('#exhibit-context');
const reference = new URLSearchParams(location.search).get('exhibit');
if (context && reference && /^[a-z][a-z0-9]*(?:-[a-z0-9]+)*@v[1-9][0-9]*$/.test(reference) && reference.length < 100) {
  context.textContent = `Concerning exhibit: ${reference}`;
  context.hidden = false;
}
const search = document.querySelector('#search');
const status = document.querySelector('#status');
if (search && status) {
  const rows = [...document.querySelectorAll('.exhibit-row')];
  const count = document.querySelector('#search-count');
  const empty = document.querySelector('#no-matches');
  const update = () => {
    const term = search.value.toLocaleLowerCase().trim();
    let visible = 0;
    for (const row of rows) {
      row.hidden = !(row.textContent.toLocaleLowerCase().includes(term) && (!status.value || row.dataset.status === status.value));
      if (!row.hidden) visible++;
    }
    count.textContent = `${visible} of ${rows.length} exhibits`;
    empty.hidden = visible !== 0 || rows.length === 0;
  };
  search.addEventListener('input', update);
  status.addEventListener('change', update);
  search.form.addEventListener('reset', () => setTimeout(update, 0));
}
