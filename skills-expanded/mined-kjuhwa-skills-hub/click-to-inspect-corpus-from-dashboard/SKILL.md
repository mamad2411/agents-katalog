---
name: click-to-inspect-corpus-from-dashboard
description: Make every corpus item (skill, doc, reference) clickable in a dashboard and open its source .md content in a modal via a server endpoint
category: design
triggers:
  - skill preview modal
  - inspect corpus item
  - dashboard item drilldown
  - clickable reference list
tags:
  - dashboard
  - ux
  - modal
  - sse
version: 1.0.0
---

# Click to Inspect Corpus From Dashboard

A dashboard that lists references from a corpus (skills, knowledge entries, docs, datasets) often ends up read-only — you see names but can't drill into content. The fix is cheap and high-value: add a server endpoint that serves the raw source file by slug, render the list items as clickable, and open a minimal modal with the content.

## Pattern

### 1. Server endpoint — path-safe lookup

```js
if (url.pathname === '/api/hub-item') {
  const kind = url.searchParams.get('kind');   // 'skill' | 'knowledge'
  const name = url.searchParams.get('name');
  if (!/^[a-z0-9-]+$/.test(name)) return res.writeHead(400).end();

  const root = path.join(CORPUS_DIR, kind === 'skill' ? 'skills' : 'knowledge');
  // Auto-walk subcategories — don't require caller to know the category
  for (const cat of fs.readdirSync(root)) {
    const file = kind === 'skill'
      ? path.join(root, cat, name, 'SKILL.md')
      : path.join(root, cat, `${name}.md`);
    if (fs.existsSync(file)) {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ name, kind, path: file, content: fs.readFileSync(file, 'utf8') }));
      return;
    }
  }
  res.writeHead(404).end();
}
```

### 2. Client — make items clickable and fetch on click

```js
// When rendering the list
el.innerHTML = items.map(x => `
  <div class="item" onclick="openItem('${kind}', '${x.name}')">
    <span class="bullet"></span>
    <span class="name">${x.name}</span>
  </div>`).join('');

async function openItem(kind, name) {
  showModal();
  const r = await fetch(`/api/hub-item?kind=${kind}&name=${name}`);
  const data = await r.json();
  document.getElementById('modalPath').textContent = data.path;
  document.getElementById('modalBody').textContent = data.content;
}
```

### 3. Modal — plain `<pre>` is enough

For technical corpora, raw markdown in a monospace `<pre>` is the right call. Markdown rendering adds complexity (dependency or parser code) for little gain — users of a skills/knowledge dashboard are already reading raw .md elsewhere, consistency wins over prettiness.

```html
<div class="modal" id="m" onclick="if(event.target===this)close()">
  <div class="content">
    <header>
      <span class="kind-badge">SKILL</span>
      <span class="title" id="modalTitle"></span>
      <button onclick="close()">×</button>
    </header>
    <div class="path" id="modalPath"></div>
    <pre class="body" id="modalBody"></pre>
  </div>
</div>
```

## Why this matters

Before clickable items: the list is proof that the corpus was scanned, nothing more. Users have to `cat` files or open the repo in a browser to verify a cited item even exists with the right content.

After clickable items: one click confirms the item is real, shows its full content, and builds trust that the system is using what it says it's using. Especially valuable for automated pipelines where users question whether the "300 skills cited" are actually backed by real files.

## Design notes

- **Path safety**: regex-validate `name` before filesystem lookup (`^[a-z0-9-]+$`). Never interpolate directly.
- **Auto-walk categories**: the caller shouldn't have to know which category folder an item lives in — walk them all and stop at first hit. Small corpora make this fast enough.
- **Escape closing**: ESC key + outside-click + explicit × button are all cheap and users expect all three.
- **Cache rule**: don't cache responses — the dashboard is live and the corpus may change during a session.

## Generalization

Applies to any dashboard rendering references to files you own:
- Config editor showing which config files are loaded → click to view source
- Log viewer citing source locations → click to open the file at that line
- Test runner showing which fixtures are used → click to see the fixture content
- API doc listing example payloads → click to see the full example
