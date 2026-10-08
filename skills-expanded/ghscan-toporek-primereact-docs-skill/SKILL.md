# PrimeReact v11 Docs Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Claude Code plugin that mirrors the PrimeReact **v11** docs (from the GitHub `v11` branch) into local, grep-friendly Markdown, plus a hand-authored router + v10→v11 version guardrail, so Claude answers from real v11 docs instead of guessing.

**Architecture:** Vendored-and-regenerated plugin (mirrors `zero-docs-skill`): a `sync.mjs` shallow-clones `primefaces/primereact@v11`, transforms each `apps/showcase/docs/**/*.mdx` to clean Markdown (inlining the referenced `apps/showcase/demo/**/*.tsx` examples, deferring API tables with a TODO note, rewriting internal links), and commits the result under `skills/primereact-docs/references/**`. A pluggable source adapter lets us later swap to v11's official `.md`/`llms-full.txt` endpoints. A daily GitHub Action re-syncs and opens a rolling PR.

**Tech Stack:** Node ≥20 (CI on Node 24), ES modules, `node --test` + `node:assert/strict`, **zero runtime/dev dependencies**. Transform is line/regex-based (no remark/unified).

## Global Constraints

- **No runtime or dev dependencies.** Only Node built-ins (`node:fs`, `node:path`, `node:child_process`, `node:test`, `node:assert`). Transform is line/regex-based (Approach A) — no `remark`/`unified`/MDX parser.
- **`.claude-plugin/plugin.json` MUST NOT contain a `version` field** (every commit is an update).
- **No raw JSX/JSON artifacts may leak into generated Markdown** — enforced at build time by `assertNoJsx`, which throws on any surviving JSX component tag outside code fences.
- **`references/` path layout:** `references/<variant>/<component>/<page>.md`; the upstream `components/` path infix is dropped; `general/` keeps its sub-structure. Variants mirrored: `general, styled, primitive, headless, tailwind`.
- **`<DocTable>` (API/props tables) is deferred to v2** — replaced by a visible blockquote TODO note, never silently dropped.
- **GitHub Actions versions (exact):** `actions/checkout@v6`, `actions/setup-node@v6` (Node 24), `peter-evans/create-pull-request@v8`. Sync cron is **daily**: `0 6 * * *`.
- **Licensing/attribution:** repo tooling MIT; `references/` content © PrimeFaces/PrimeReact mirrored under MIT with mechanical modifications; README carries a non-affiliation disclaimer.
- **Upstream:** repo `https://github.com/primefaces/primereact`, branch `v11`. Docs root `apps/showcase/docs`, demo root `apps/showcase/demo`.

---

### Task 1: Project scaffold (package.json + dirs)

**Files:**
- Create: `package.json`
- Create: `scripts/lib/.gitkeep`
- Modify: `.gitignore` (already contains `.vendor/` and `node_modules/` — verify)

**Interfaces:**
- Produces: npm scripts `sync`, `sync:check`, `test`; ES-module project so `*.mjs` and `import` work.

- [ ] **Step 1: Create `package.json`**

```json
{
  "name": "primereact-docs-skill",
  "private": true,
  "type": "module",
  "description": "Searchable PrimeReact v11 documentation as a Claude Code skill.",
  "engines": { "node": ">=20" },
  "scripts": {
    "sync": "node scripts/sync.mjs",
    "sync:check": "node scripts/sync.mjs --check",
    "test": "node --test"
  }
}
```

- [ ] **Step 2: Create the lib dir placeholder**

```bash
mkdir -p scripts/lib && touch scripts/lib/.gitkeep
```

- [ ] **Step 3: Verify the test runner works (no tests yet)**

Run: `npm test`
Expected: exits 0; output includes `tests 0` (no failures).

- [ ] **Step 4: Verify `.gitignore`**

Run: `cat .gitignore`
Expected: contains `.vendor/` and `node_modules/`. If not, add them.

- [ ] **Step 5: Commit**

```bash
git add package.json scripts/lib/.gitkeep .gitignore
git commit -m "chore: scaffold primereact-docs-skill project"
```

---

### Task 2: transform — `parseFrontmatter` + `parseAttrs`

**Files:**
- Create: `scripts/lib/transform.mjs`
- Test: `scripts/lib/transform.test.mjs`

**Interfaces:**
- Produces:
  - `parseFrontmatter(raw: string): { data: Record<string,string>, body: string }` — reads simple `key: value` frontmatter (incl. `title`, `description`, `component`), strips surrounding quotes.
  - `parseAttrs(attrString: string): Record<string,string>` — extracts quoted string attributes from a JSX tag's attribute text (ignores `key={...}` expression attrs).
  - `const FENCE: RegExp` — matches a code-fence line.

- [ ] **Step 1: Write the failing test**

```js
// scripts/lib/transform.test.mjs
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { parseFrontmatter, parseAttrs } from './transform.mjs';

test('parseFrontmatter extracts title, description, component', () => {
  const raw = '---\ntitle: Accordion\ndescription: An accordion.\ncomponent: accordion\n---\nBody\n';
  const { data, body } = parseFrontmatter(raw);
  assert.equal(data.title, 'Accordion');
  assert.equal(data.description, 'An accordion.');
  assert.equal(data.component, 'accordion');
  assert.equal(body, 'Body\n');
});

test('parseFrontmatter strips surrounding quotes', () => {
  assert.equal(parseFrontmatter('---\ntitle: "Setup"\n---\nx').data.title, 'Setup');
});

test('parseFrontmatter returns empty data when absent', () => {
  const { data, body } = parseFrontmatter('# Hi\n');
  assert.deepEqual(data, {});
  assert.equal(body, '# Hi\n');
});

test('parseAttrs reads double- and single-quoted attrs, ignores expressions', () => {
  const a = parseAttrs(` name="accordion:basic-demo" mode='hidden' components={['X']}`);
  assert.equal(a.name, 'accordion:basic-demo');
  assert.equal(a.mode, 'hidden');
  assert.equal(a.components, undefined);
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test scripts/lib/transform.test.mjs`
Expected: FAIL — cannot find module `./transform.mjs` / exports undefined.

- [ ] **Step 3: Write minimal implementation**

```js
// scripts/lib/transform.mjs

export const FENCE = /^\s*(```|~~~)/;

/** Parse a leading YAML-ish frontmatter block (--- ... ---). Simple key: value only. */
export function parseFrontmatter(raw) {
  const match = /^---\r?\n([\s\S]*?)\r?\n---\r?\n?/.exec(raw);
  if (!match) return { data: {}, body: raw };
  const data = {};
  for (const line of match[1].split(/\r?\n/)) {
    const m = /^([\w-]+):\s*(.*)$/.exec(line);
    if (!m) continue;
    let value = m[2].trim();
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }
    data[m[1]] = value;
  }
  return { data, body: raw.slice(match[0].length) };
}

/** Extract quoted string attributes from a JSX tag's attribute text. */
export function parseAttrs(s) {
  const attrs = {};
  const re = /([\w-]+)\s*=\s*(?:"([^"]*)"|'([^']*)')/g;
  let m;
  while ((m = re.exec(s))) attrs[m[1]] = m[2] !== undefined ? m[2] : m[3];
  return attrs;
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `node --test scripts/lib/transform.test.mjs`
Expected: PASS (4 tests).

- [ ] **Step 5: Commit**

```bash
git add scripts/lib/transform.mjs scripts/lib/transform.test.mjs
git commit -m "feat(transform): parseFrontmatter and parseAttrs"
```

---

### Task 3: transform — `finalizeDoc`

**Files:**
- Modify: `scripts/lib/transform.mjs`
- Test: `scripts/lib/transform.test.mjs`

**Interfaces:**
- Produces: `finalizeDoc(body: string, title: string): string` — CRLF→LF, drops whole-line `{/* ... */}` MDX comments outside fences, collapses 3+ blank lines, trims, ensures a leading H1 (prepends `# title` if missing), ends with one newline.

- [ ] **Step 1: Write the failing test (append to transform.test.mjs)**

```js
import { finalizeDoc } from './transform.mjs';

test('finalizeDoc normalizes CRLF, collapses blanks, trailing newline', () => {
  assert.equal(finalizeDoc('# Hi\r\n\r\n\r\nBody\r\n\n\n', 'Hi'), '# Hi\n\nBody\n');
});

test('finalizeDoc prepends an H1 when missing', () => {
  assert.equal(finalizeDoc('Just prose.', 'My Title'), '# My Title\n\nJust prose.\n');
});

test('finalizeDoc keeps an existing H1', () => {
  assert.equal(finalizeDoc('# Here\n\nBody', 'Other'), '# Here\n\nBody\n');
});

test('finalizeDoc strips whole-line MDX comments outside fences', () => {
  assert.equal(finalizeDoc('# T\n\n{/* prettier-ignore */}\n\n```tsx\ncode\n```', 'T'),
    '# T\n\n```tsx\ncode\n```\n');
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test scripts/lib/transform.test.mjs`
Expected: FAIL — `finalizeDoc` is not exported.

- [ ] **Step 3: Write minimal implementation (append to transform.mjs)**

```js
/** Normalize a transformed body: drop MDX comments outside fences, collapse blanks, ensure H1 + trailing newline. */
export function finalizeDoc(body, title) {
  let inFence = false;
  let out = body
    .replace(/\r\n/g, '\n')
    .split('\n')
    .filter((line) => {
      if (FENCE.test(line)) { inFence = !inFence; return true; }
      return inFence || !/^\s*\{\/\*.*\*\/\}\s*$/.test(line);
    })
    .join('\n')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
  if (!/^#\s/.test(out)) out = '# ' + title + '\n\n' + out;
  return out + '\n';
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `node --test scripts/lib/transform.test.mjs`
Expected: PASS (all transform tests).

- [ ] **Step 5: Commit**

```bash
git add scripts/lib/transform.mjs scripts/lib/transform.test.mjs
git commit -m "feat(transform): finalizeDoc normalizer"
```

---

### Task 4: transform — `transformComponents` (the custom-component handlers)

**Files:**
- Modify: `scripts/lib/transform.mjs`
- Test: `scripts/lib/transform.test.mjs`

**Interfaces:**
- Consumes: `parseAttrs`, `FENCE` (Task 2).
- Produces: `transformComponents(body: string, opts: { lookupDemo: (component: string, demo: string) => string|null, component: string }): string`.
  - Fence-aware, line-oriented. Outside fences it: drops `import`/`export` lines and whole-line MDX comments; inlines `<DocDemoViewer name="c:d" mode/>` as a ```tsx block via `lookupDemo` (skips `mode="hidden"`, drops if `null`); inlines `<DocPTViewer name="x"/>` via `lookupDemo(component, x)`; converts `<DocTable name category/>` to a TODO blockquote; emits `<DocPrimitiveIntro description/>` text; converts single-line `<Button ... href>text</Button>` to a link; drops other own-line capitalized JSX tags.

- [ ] **Step 1: Write the failing test (append to transform.test.mjs)**

```js
import { transformComponents } from './transform.mjs';

const demoMap = { 'accordion:basic-demo': 'export default () => <Accordion.Root/>;', 'accordion:accordion-pt': 'export const pt = {};' };
const lookupDemo = (comp, demo) => demoMap[`${comp}:${demo}`] ?? null;
const opts = { lookupDemo, component: 'accordion' };

test('transformComponents inlines DocDemoViewer as a tsx block', () => {
  const out = transformComponents('<DocDemoViewer name="accordion:basic-demo" mode="collapsible"/>', opts);
  assert.equal(out, '```tsx\nexport default () => <Accordion.Root/>;\n```');
});

test('transformComponents skips hidden demos and missing demos', () => {
  assert.equal(transformComponents('<DocDemoViewer name="accordion:basic-demo" mode="hidden"/>', opts), '');
  assert.equal(transformComponents('<DocDemoViewer name="accordion:nope"/>', opts), '');
});

test('transformComponents converts DocTable to a TODO note (no raw JSX)', () => {
  const out = transformComponents('<DocTable name="AccordionRoot" category="api" />', opts);
  assert.match(out, /API\/props table for `AccordionRoot` \(`api`\)/);
  assert.match(out, /TODO: mirror in v2/);
  assert.ok(!out.includes('<DocTable'));
});

test('transformComponents emits DocPrimitiveIntro description text', () => {
  assert.equal(transformComponents('<DocPrimitiveIntro description="Build custom sections." />', opts), 'Build custom sections.');
});

test('transformComponents inlines DocPTViewer via doc component', () => {
  const out = transformComponents('<DocPTViewer name="accordion-pt" components={["AccordionRoot"]} />', opts);
  assert.match(out, /```tsx\nexport const pt = \{\};\n```/);
});

test('transformComponents converts Button to a markdown link', () => {
  assert.equal(transformComponents('<Button as="a" href="/llms.txt" target="_blank">Open llms.txt</Button>', opts), '[Open llms.txt](/llms.txt)');
});

test('transformComponents drops other own-line components and import/export', () => {
  const input = "import x from 'y';\n<DocPrimitiveLinks name=\"Accordion\" />\nReal prose.";
  assert.equal(transformComponents(input, opts), 'Real prose.');
});

test('transformComponents leaves fenced content untouched', () => {
  const input = '```tsx\nimport {Accordion} from "primereact/accordion";\n<DocTable/>\n```';
  assert.equal(transformComponents(input, opts), input);
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test scripts/lib/transform.test.mjs`
Expected: FAIL — `transformComponents` not exported.

- [ ] **Step 3: Write minimal implementation (append to transform.mjs)**

```js
/** Fence-aware, line-oriented MDX custom-component → Markdown transform. */
export function transformComponents(body, { lookupDemo, component }) {
  const lines = body.split('\n');
  const out = [];
  let inFence = false;

  const fence = (src) => ['```tsx', String(src).replace(/\s+$/, ''), '```'];

  for (const line of lines) {
    if (FENCE.test(line)) { inFence = !inFence; out.push(line); continue; }
    if (inFence) { out.push(line); continue; }

    const t = line.trim();

    if (t === '') { out.push(line); continue; }
    if (/^(import|export)\s/.test(t)) continue;
    if (/^\{\/\*.*\*\/\}$/.test(t)) continue;

    let m = t.match(/^<DocDemoViewer\b([^>]*)\/>$/);
    if (m) {
      const { name = '', mode } = parseAttrs(m[1]);
      if (mode === 'hidden' || !name.includes(':')) continue;
      const [comp, demo] = name.split(':');
      const src = lookupDemo(comp, demo);
      if (src) out.push(...fence(src));
      continue;
    }

    m = t.match(/^<DocPTViewer\b([^>]*)\/>$/);
    if (m) {
      const { name = '' } = parseAttrs(m[1]);
      const src = name ? lookupDemo(component, name) : null;
      if (src) out.push('**Pass Through example:**', '', ...fence(src));
      continue;
    }

    m = t.match(/^<DocTable\b([^>]*)\/>$/);
    if (m) {
      const { name = 'this component', category = 'api' } = parseAttrs(m[1]);
      out.push(
        '> **API/props table for `' + name + '` (`' + category + '`) is generated from upstream ' +
          'TypeScript types and is not yet mirrored — see the installed package types or the ' +
          'upstream docs. (TODO: mirror in v2.)',
      );
      continue;
    }

    m = t.match(/^<DocPrimitiveIntro\b([^>]*)\/>$/);
    if (m) {
      const { description = '' } = parseAttrs(m[1]);
      if (description) out.push(description);
      continue;
    }

    m = t.match(/^<Button\b([^>]*)>(.*?)<\/Button>$/);
    if (m) {
      const { href } = parseAttrs(m[1]);
      const text = m[2].trim();
      out.push(href ? '[' + text + '](' + href + ')' : text);
      continue;
    }

    // Drop any own-line capitalized JSX tag (self-closing, open, or close) with no inline code.
    if (/^<\/?[A-Z][A-Za-z0-9.]*\b[^>]*>$/.test(t) && !t.includes('`')) continue;

    out.push(line);
  }

  return out.join('\n');
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `node --test scripts/lib/transform.test.mjs`
Expected: PASS (all transform tests, including the 8 new ones).

- [ ] **Step 5: Commit**

```bash
git add scripts/lib/transform.mjs scripts/lib/transform.test.mjs
git commit -m "feat(transform): custom-component handlers (demos, DocTable TODO, Button, strip)"
```

---

### Task 5: transform — `rewriteDocLinks`

**Files:**
- Modify: `scripts/lib/transform.mjs`
- Test: `scripts/lib/transform.test.mjs`

**Interfaces:**
- Consumes: `FENCE`.
- Produces: `rewriteDocLinks(body: string, selfOutPath: string, slugMap: Map<string,string>): string`.
  - Rewrites `](/docs/<slug>…)` and `](https://(v11.)primereact.org/docs/<slug>…)` links. If `slug` is in `slugMap` (urlSlug → outPath), rewrite to a path relative to `selfOutPath`; preserve `#anchor`, drop query strings. If unknown, normalize a root-relative `/docs/...` link to an absolute `https://v11.primereact.org/docs/...` URL (so it is not broken); leave already-absolute links unchanged. Lines inside fences untouched.

- [ ] **Step 1: Write the failing test (append to transform.test.mjs)**

```js
import { rewriteDocLinks } from './transform.mjs';

const slugMap = new Map([
  ['primitive/accordion', 'primitive/accordion/features.md'],
  ['primitive/motion', 'primitive/motion/features.md'],
  ['styled/theming/styled', 'styled/theming/styled.md'],
]);

test('rewriteDocLinks rewrites known root-relative links to relative paths', () => {
  assert.equal(
    rewriteDocLinks('See [Motion](/docs/primitive/motion#phases).', 'primitive/accordion/features.md', slugMap),
    'See [Motion](../motion/features.md#phases).',
  );
});

test('rewriteDocLinks rewrites known absolute primereact.org links', () => {
  assert.equal(
    rewriteDocLinks('[t](https://v11.primereact.org/docs/styled/theming/styled)', 'primitive/accordion/features.md', slugMap),
    '[t](../../styled/theming/styled.md)',
  );
});

test('rewriteDocLinks normalizes unknown root-relative /docs links to absolute', () => {
  assert.equal(
    rewriteDocLinks('[x](/docs/primitive/unknown)', 'primitive/accordion/features.md', slugMap),
    '[x](https://v11.primereact.org/docs/primitive/unknown)',
  );
});

test('rewriteDocLinks leaves non-doc links and fenced lines untouched', () => {
  const s = 'pre [a](/docs/primitive/motion)\n```\n[b](/docs/primitive/motion)\n```\n[ext](https://example.com)';
  assert.equal(
    rewriteDocLinks(s, 'primitive/accordion/features.md', slugMap),
    'pre [a](../motion/features.md)\n```\n[b](/docs/primitive/motion)\n```\n[ext](https://example.com)',
  );
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test scripts/lib/transform.test.mjs`
Expected: FAIL — `rewriteDocLinks` not exported.

- [ ] **Step 3: Write minimal implementation (append to transform.mjs)**

```js
/** Rewrite internal /docs/<slug> links to local relative paths (known) or absolute upstream URLs (unknown). */
export function rewriteDocLinks(body, selfOutPath, slugMap) {
  const fromDir = selfOutPath.includes('/') ? selfOutPath.slice(0, selfOutPath.lastIndexOf('/')).split('/') : [];
  const relativeTo = (target) => {
    const to = target.split('/');
    let i = 0;
    while (i < fromDir.length && i < to.length - 1 && fromDir[i] === to[i]) i++;
    return [...Array(fromDir.length - i).fill('..'), ...to.slice(i)].join('/');
  };
  const linkRe = /\]\((?:https?:\/\/(?:v11\.)?primereact\.org)?\/docs\/([A-Za-z0-9_/-]+?)(?:\.md)?(?:\?[^)#]*)?(#[^)]*)?\)/g;
  let inFence = false;
  return body
    .split('\n')
    .map((line) => {
      if (FENCE.test(line)) { inFence = !inFence; return line; }
      if (inFence) return line;
      return line.replace(linkRe, (full, slug, anchor) => {
        const target = slugMap.get(slug);
        if (target) return '](' + relativeTo(target) + (anchor || '') + ')';
        if (full.startsWith('](/docs/')) return '](https://v11.primereact.org/docs/' + slug + (anchor || '') + ')';
        return full;
      });
    })
    .join('\n');
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `node --test scripts/lib/transform.test.mjs`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/lib/transform.mjs scripts/lib/transform.test.mjs
git commit -m "feat(transform): rewriteDocLinks"
```

---

### Task 6: transform — `assertNoJsx` + `mdxToMarkdown` composer

**Files:**
- Modify: `scripts/lib/transform.mjs`
- Test: `scripts/lib/transform.test.mjs`

**Interfaces:**
- Consumes: all prior transform functions.
- Produces:
  - `assertNoJsx(text: string, label?: string): void` — throws if any JSX component tag (`<Doc…` or `<Capitalized…`) survives outside code fences and inline-code spans.
  - `mdxToMarkdown(raw: string, opts: { lookupDemo, selfOutPath: string, slugMap: Map<string,string> }): string` — full pipeline: parse frontmatter → header (`# title` + description lead) + `transformComponents` → `rewriteDocLinks` → `finalizeDoc` → `assertNoJsx` → return.

- [ ] **Step 1: Write the failing test (append to transform.test.mjs)**

```js
import { assertNoJsx, mdxToMarkdown } from './transform.mjs';

test('assertNoJsx throws on surviving JSX, ignores fences and inline code', () => {
  assert.throws(() => assertNoJsx('# T\n\n<DocTable name="X"/>\n'), /Raw JSX/);
  assert.doesNotThrow(() => assertNoJsx('# T\n\nUse `<Accordion.Root>` here.\n'));
  assert.doesNotThrow(() => assertNoJsx('# T\n\n```tsx\n<Accordion.Root/>\n```\n'));
});

test('mdxToMarkdown runs the full pipeline', () => {
  const raw = [
    '---', 'title: Accordion', 'description: An accordion.', 'component: accordion', '---',
    '<DocPrimitiveIntro description="Custom sections." />',
    '',
    '<DocDemoViewer name="accordion:basic-demo" mode="collapsible"/>',
    '',
    '## API',
    '<DocTable name="AccordionRoot" category="api" />',
    '',
    'See [Motion](/docs/primitive/motion).',
    '',
  ].join('\n');
  const out = mdxToMarkdown(raw, {
    lookupDemo: (c, d) => (c === 'accordion' && d === 'basic-demo' ? 'const X = 1;' : null),
    selfOutPath: 'primitive/accordion/features.md',
    slugMap: new Map([['primitive/motion', 'primitive/motion/features.md']]),
  });
  assert.match(out, /^# Accordion\n\nAn accordion\./);
  assert.match(out, /Custom sections\./);
  assert.match(out, /```tsx\nconst X = 1;\n```/);
  assert.match(out, /TODO: mirror in v2/);
  assert.match(out, /\[Motion\]\(\.\.\/motion\/features\.md\)/);
  assert.ok(!out.includes('<Doc'));
  assert.ok(out.endsWith('\n'));
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test scripts/lib/transform.test.mjs`
Expected: FAIL — `assertNoJsx`/`mdxToMarkdown` not exported.

- [ ] **Step 3: Write minimal implementation (append to transform.mjs)**

```js
/** Fail the build if any JSX component tag survives outside code fences / inline code. */
export function assertNoJsx(text, label = 'doc') {
  let inFence = false;
  for (const line of text.split('\n')) {
    if (FENCE.test(line)) { inFence = !inFence; continue; }
    if (inFence) continue;
    const stripped = line.replace(/`[^`]*`/g, '');
    if (/<Doc[A-Za-z]/.test(stripped) || /<\/?[A-Z][A-Za-z0-9]*[\s/>]/.test(stripped)) {
      throw new Error('Raw JSX artifact left in ' + label + ': ' + line.trim());
    }
  }
}

/** Full MDX → Markdown pipeline for one doc. */
export function mdxToMarkdown(raw, { lookupDemo, selfOutPath, slugMap }) {
  const { data, body } = parseFrontmatter(raw);
  const title = data.title || 'Untitled';
  const lead = data.description ? data.description + '\n\n' : '';
  let out = transformComponents(body, { lookupDemo, component: data.component || '' });
  out = rewriteDocLinks(out, selfOutPath, slugMap);
  out = finalizeDoc('# ' + title + '\n\n' + lead + out, title);
  assertNoJsx(out, selfOutPath);
  return out;
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `node --test scripts/lib/transform.test.mjs`
Expected: PASS (all transform tests).

- [ ] **Step 5: Commit**

```bash
git add scripts/lib/transform.mjs scripts/lib/transform.test.mjs
git commit -m "feat(transform): assertNoJsx guard and mdxToMarkdown composer"
```

---

### Task 7: demos — `createDemoLookup`

**Files:**
- Create: `scripts/lib/demos.mjs`
- Test: `scripts/lib/demos.test.mjs`
- Create (test fixtures): `scripts/lib/__fixtures__/demo/primitive/accordion/basic-demo.tsx`

**Interfaces:**
- Produces: `createDemoLookup({ demoRoot: string, variant: string }): (component: string, demo: string) => string|null` — reads `<demoRoot>/<variant>/<component>/<demo>.tsx`, applies the `@/components/ui/utils` → `@/lib/utils` rewrite, returns content or `null` if absent.

- [ ] **Step 1: Create the fixture demo file**

```tsx
// scripts/lib/__fixtures__/demo/primitive/accordion/basic-demo.tsx
import { cn } from '@/components/ui/utils';
export default function Demo() { return <div className={cn('x')} />; }
```

- [ ] **Step 2: Write the failing test**

```js
// scripts/lib/demos.test.mjs
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createDemoLookup } from './demos.mjs';

const here = dirname(fileURLToPath(import.meta.url));
const demoRoot = join(here, '__fixtures__', 'demo');

test('createDemoLookup reads a demo and rewrites the utils import', () => {
  const lookup = createDemoLookup({ demoRoot, variant: 'primitive' });
  const src = lookup('accordion', 'basic-demo');
  assert.match(src, /@\/lib\/utils/);
  assert.ok(!src.includes('@/components/ui/utils'));
});

test('createDemoLookup returns null for a missing demo', () => {
  const lookup = createDemoLookup({ demoRoot, variant: 'primitive' });
  assert.equal(lookup('accordion', 'nope'), null);
});
```

- [ ] **Step 3: Run test to verify it fails**

Run: `node --test scripts/lib/demos.test.mjs`
Expected: FAIL — module not found.

- [ ] **Step 4: Write minimal implementation**

```js
// scripts/lib/demos.mjs
import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';

/** Build a demo resolver bound to a demo root + variant. */
export function createDemoLookup({ demoRoot, variant }) {
  return (component, demo) => {
    const file = join(demoRoot, variant, component, demo + '.tsx');
    if (!existsSync(file)) return null;
    return readFileSync(file, 'utf8').replace('@/components/ui/utils', '@/lib/utils');
  };
}
```

- [ ] **Step 5: Run test to verify it passes**

Run: `node --test scripts/lib/demos.test.mjs`
Expected: PASS (2 tests).

- [ ] **Step 6: Commit**

```bash
git add scripts/lib/demos.mjs scripts/lib/demos.test.mjs scripts/lib/__fixtures__/demo
git commit -m "feat(demos): createDemoLookup resolver"
```

---

### Task 8: collect — enumerate + normalize paths

**Files:**
- Create: `scripts/lib/collect.mjs`
- Test: `scripts/lib/collect.test.mjs`
- Create (fixtures): `scripts/lib/__fixtures__/docs/primitive/accordion/features.mdx`, `scripts/lib/__fixtures__/docs/styled/components/button/features.mdx`, `scripts/lib/__fixtures__/docs/general/gettingstarted/setup.mdx`

**Interfaces:**
- Consumes: `parseFrontmatter` (Task 2).
- Produces:
  - `findMdx(dir: string): string[]` — recursive, sorted absolute `*.mdx` paths.
  - `toOutPath(srcRel: string): string` — POSIX-relative, `.mdx`→`.md`, drops the `/components/` infix.
  - `toUrlSlug(outPath: string): string` — strips trailing `/features.md` (→ dir slug) else strips `.md`.
  - `variantOf(srcRel: string): string` — first path segment.
  - `collectDocs(docsRoot: string): Array<{ srcAbs, variant, outPath, urlSlug, title, description }>`.

- [ ] **Step 1: Create fixtures**

```mdx
<!-- scripts/lib/__fixtures__/docs/primitive/accordion/features.mdx -->
---
title: Accordion
description: An unstyled accordion.
component: accordion
---
Body.
```

```mdx
<!-- scripts/lib/__fixtures__/docs/styled/components/button/features.mdx -->
---
title: Button
description: A button.
component: button
---
Body.
```

```mdx
<!-- scripts/lib/__fixtures__/docs/general/gettingstarted/setup.mdx -->
---
title: Setup
description: Install guide.
---
Body.
```

- [ ] **Step 2: Write the failing test**

```js
// scripts/lib/collect.test.mjs
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { toOutPath, toUrlSlug, variantOf, collectDocs } from './collect.mjs';

const here = dirname(fileURLToPath(import.meta.url));
const docsRoot = join(here, '__fixtures__', 'docs');

test('toOutPath drops components/ infix and rewrites extension', () => {
  assert.equal(toOutPath('styled/components/button/features.mdx'), 'styled/button/features.md');
  assert.equal(toOutPath('primitive/accordion/features.mdx'), 'primitive/accordion/features.md');
  assert.equal(toOutPath('general/gettingstarted/setup.mdx'), 'general/gettingstarted/setup.md');
});

test('toUrlSlug strips /features.md or .md', () => {
  assert.equal(toUrlSlug('primitive/accordion/features.md'), 'primitive/accordion');
  assert.equal(toUrlSlug('general/gettingstarted/setup.md'), 'general/gettingstarted/setup');
});

test('variantOf returns the first segment', () => {
  assert.equal(variantOf('styled/components/button/features.mdx'), 'styled');
});

test('collectDocs returns normalized entries with frontmatter', () => {
  const entries = collectDocs(docsRoot);
  const byOut = Object.fromEntries(entries.map((e) => [e.outPath, e]));
  assert.equal(entries.length, 3);
  assert.equal(byOut['styled/button/features.md'].title, 'Button');
  assert.equal(byOut['styled/button/features.md'].variant, 'styled');
  assert.equal(byOut['primitive/accordion/features.md'].urlSlug, 'primitive/accordion');
  assert.equal(byOut['general/gettingstarted/setup.md'].description, 'Install guide.');
});
```

- [ ] **Step 3: Run test to verify it fails**

Run: `node --test scripts/lib/collect.test.mjs`
Expected: FAIL — module not found.

- [ ] **Step 4: Write minimal implementation**

```js
// scripts/lib/collect.mjs
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join, relative, sep } from 'node:path';
import { parseFrontmatter } from './transform.mjs';

/** Recursively collect sorted absolute paths of *.mdx under dir. */
export function findMdx(dir) {
  const out = [];
  for (const name of readdirSync(dir)) {
    const full = join(dir, name);
    if (statSync(full).isDirectory()) out.push(...findMdx(full));
    else if (name.endsWith('.mdx')) out.push(full);
  }
  return out.sort();
}

export function toOutPath(srcRel) {
  return srcRel.split(sep).join('/').replace(/\.mdx$/, '.md').replace('/components/', '/');
}

export function toUrlSlug(outPath) {
  return outPath.endsWith('/features.md') ? outPath.slice(0, -'/features.md'.length) : outPath.replace(/\.md$/, '');
}

export function variantOf(srcRel) {
  return srcRel.split(sep)[0];
}

export function collectDocs(docsRoot) {
  const entries = [];
  for (const srcAbs of findMdx(docsRoot)) {
    const srcRel = relative(docsRoot, srcAbs);
    const outPath = toOutPath(srcRel);
    const { data } = parseFrontmatter(readFileSync(srcAbs, 'utf8'));
    entries.push({
      srcAbs,
      variant: variantOf(srcRel),
      outPath,
      urlSlug: toUrlSlug(outPath),
      title: data.title || 'Untitled',
      description: data.description || '',
    });
  }
  return entries;
}
```

- [ ] **Step 5: Run test to verify it passes**

Run: `node --test scripts/lib/collect.test.mjs`
Expected: PASS (4 tests).

- [ ] **Step 6: Commit**

```bash
git add scripts/lib/collect.mjs scripts/lib/collect.test.mjs scripts/lib/__fixtures__/docs
git commit -m "feat(collect): enumerate docs and normalize out-paths/slugs"
```

---

### Task 9: index-gen — `buildIndex`

**Files:**
- Create: `scripts/lib/index-gen.mjs`
- Test: `scripts/lib/index-gen.test.mjs`

**Interfaces:**
- Produces: `buildIndex(entries: Array<{ variant, outPath, title, description }>): string` — Markdown grouped by variant (order: general, styled, primitive, headless, tailwind), each `- [Title](references/<outPath>) — <description>`, sorted by `outPath` within group, ending in one newline.

- [ ] **Step 1: Write the failing test**

```js
// scripts/lib/index-gen.test.mjs
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { buildIndex } from './index-gen.mjs';

test('buildIndex groups by variant in order and lists every entry', () => {
  const out = buildIndex([
    { variant: 'styled', outPath: 'styled/button/features.md', title: 'Button', description: 'A button.' },
    { variant: 'general', outPath: 'general/gettingstarted/setup.md', title: 'Setup', description: '' },
    { variant: 'primitive', outPath: 'primitive/accordion/features.md', title: 'Accordion', description: 'An accordion.' },
  ]);
  assert.match(out, /# PrimeReact v11 Docs Index/);
  assert.ok(out.indexOf('## General') < out.indexOf('## Styled'));
  assert.ok(out.indexOf('## Styled') < out.indexOf('## Primitive'));
  assert.match(out, /- \[Button\]\(references\/styled\/button\/features\.md\) — A button\./);
  assert.match(out, /- \[Setup\]\(references\/general\/gettingstarted\/setup\.md\)\n/);
  assert.ok(out.endsWith('\n'));
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test scripts/lib/index-gen.test.mjs`
Expected: FAIL — module not found.

- [ ] **Step 3: Write minimal implementation**

```js
// scripts/lib/index-gen.mjs
const GROUP_LABELS = { general: 'General', styled: 'Styled', primitive: 'Primitive', headless: 'Headless', tailwind: 'Tailwind' };
const GROUP_ORDER = ['general', 'styled', 'primitive', 'headless', 'tailwind'];

export function buildIndex(entries) {
  const groups = new Map();
  for (const e of entries) {
    if (!groups.has(e.variant)) groups.set(e.variant, []);
    groups.get(e.variant).push(e);
  }
  const rank = (g) => { const i = GROUP_ORDER.indexOf(g); return i === -1 ? GROUP_ORDER.length + 1 : i; };
  const keys = [...groups.keys()].sort((a, b) => rank(a) - rank(b) || a.localeCompare(b));

  const lines = ['# PrimeReact v11 Docs Index', ''];
  for (const key of keys) {
    lines.push('## ' + (GROUP_LABELS[key] || key), '');
    for (const e of groups.get(key).sort((a, b) => a.outPath.localeCompare(b.outPath))) {
      lines.push('- [' + e.title + '](references/' + e.outPath + ')' + (e.description ? ' — ' + e.description : ''));
    }
    lines.push('');
  }
  return lines.join('\n').trim() + '\n';
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `node --test scripts/lib/index-gen.test.mjs`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/lib/index-gen.mjs scripts/lib/index-gen.test.mjs
git commit -m "feat(index-gen): buildIndex grouped by variant"
```

---

### Task 10: source — pluggable adapter

**Files:**
- Create: `scripts/lib/source.mjs`
- Test: `scripts/lib/source.test.mjs`

**Interfaces:**
- Produces:
  - `REPO: string` (`https://github.com/primefaces/primereact`), `BRANCH: string` (`v11`).
  - `cloneV11(vendorDir: string): string` — shallow-clones the branch into `vendorDir`, returns HEAD SHA. (Not unit-tested — network/git.)
  - `githubBranchSource(vendorDir: string): { mode: 'github', docsRoot: string, demoRoot: string }`.
  - `renderedMdSource(): never` — throws (v2 stub).
  - `selectSource(vendorDir: string, mode?: string): { mode, docsRoot?, demoRoot? }` — `mode` from arg or `PRIMEREACT_DOCS_SOURCE` env (default `github`); `rendered` throws.

- [ ] **Step 1: Write the failing test**

```js
// scripts/lib/source.test.mjs
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { join } from 'node:path';
import { githubBranchSource, renderedMdSource, selectSource, REPO, BRANCH } from './source.mjs';

test('githubBranchSource returns docs and demo roots under the vendor dir', () => {
  const s = githubBranchSource('/tmp/vendor');
  assert.equal(s.mode, 'github');
  assert.equal(s.docsRoot, join('/tmp/vendor', 'apps', 'showcase', 'docs'));
  assert.equal(s.demoRoot, join('/tmp/vendor', 'apps', 'showcase', 'demo'));
});

test('renderedMdSource throws a clear not-implemented error', () => {
  assert.throws(() => renderedMdSource(), /not implemented/i);
});

test('selectSource defaults to github and rejects rendered', () => {
  assert.equal(selectSource('/tmp/vendor', 'github').mode, 'github');
  assert.throws(() => selectSource('/tmp/vendor', 'rendered'), /not implemented/i);
});

test('upstream constants point at the v11 branch', () => {
  assert.equal(REPO, 'https://github.com/primefaces/primereact');
  assert.equal(BRANCH, 'v11');
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test scripts/lib/source.test.mjs`
Expected: FAIL — module not found.

- [ ] **Step 3: Write minimal implementation**

```js
// scripts/lib/source.mjs
import { execFileSync } from 'node:child_process';
import { rmSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';

export const REPO = 'https://github.com/primefaces/primereact';
export const BRANCH = 'v11';

/** Shallow-clone the v11 branch into vendorDir; return the resolved HEAD SHA. */
export function cloneV11(vendorDir) {
  rmSync(vendorDir, { recursive: true, force: true });
  mkdirSync(dirname(vendorDir), { recursive: true });
  execFileSync('git', ['clone', '--depth', '1', '--branch', BRANCH, REPO, vendorDir], { stdio: 'inherit' });
  return execFileSync('git', ['-C', vendorDir, 'rev-parse', 'HEAD'], { encoding: 'utf8' }).trim();
}

/** Source adapter reading MDX + demos from a vendored v11 clone. */
export function githubBranchSource(vendorDir) {
  return {
    mode: 'github',
    docsRoot: join(vendorDir, 'apps', 'showcase', 'docs'),
    demoRoot: join(vendorDir, 'apps', 'showcase', 'demo'),
  };
}

/** v2 stub: official .md / llms-full.txt endpoints are not live yet (see SOURCE.md / spec). */
export function renderedMdSource() {
  throw new Error('renderedMdSource: not implemented — v11 official .md/llms endpoints are not live yet (TODO v2).');
}

export function selectSource(vendorDir, mode = process.env.PRIMEREACT_DOCS_SOURCE || 'github') {
  if (mode === 'rendered') return renderedMdSource();
  return githubBranchSource(vendorDir);
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `node --test scripts/lib/source.test.mjs`
Expected: PASS (4 tests).

- [ ] **Step 5: Commit**

```bash
git add scripts/lib/source.mjs scripts/lib/source.test.mjs
git commit -m "feat(source): pluggable adapter (github clone + rendered stub)"
```

---

### Task 11: sync core — `buildSlugMap` + `buildFiles` (hermetic integration)

**Files:**
- Create: `scripts/lib/build.mjs`
- Test: `scripts/lib/build.test.mjs`
- Create (fixtures): `scripts/lib/__fixtures__/demo/primitive/accordion/basic-demo.tsx` (exists from Task 7); reuse the Task 8 docs fixtures.

**Interfaces:**
- Consumes: `collectDocs` (Task 8), `mdxToMarkdown` (Task 6), `createDemoLookup` (Task 7), `buildIndex` (Task 9).
- Produces:
  - `buildSlugMap(entries): Map<string,string>` — `urlSlug` → `outPath`.
  - `buildFiles({ docsRoot, demoRoot }): { files: Map<string,string>, index: string, entries }` — reads every doc, transforms (inlining demos, rewriting links), returns the `outPath`→content map plus the generated `INDEX.md` string and entries.

*(This is the integration seam tested hermetically against the fixture tree; `sync.mjs` (Task 12) wraps it with clone + fs writes.)*

- [ ] **Step 1: Write the failing test**

```js
// scripts/lib/build.test.mjs
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSlugMap, buildFiles } from './build.mjs';
import { collectDocs } from './collect.mjs';

const here = dirname(fileURLToPath(import.meta.url));
const docsRoot = join(here, '__fixtures__', 'docs');
const demoRoot = join(here, '__fixtures__', 'demo');

test('buildSlugMap maps urlSlug to outPath', () => {
  const map = buildSlugMap(collectDocs(docsRoot));
  assert.equal(map.get('primitive/accordion'), 'primitive/accordion/features.md');
});

test('buildFiles transforms every doc and builds an index', () => {
  const { files, index, entries } = buildFiles({ docsRoot, demoRoot });
  assert.equal(files.size, entries.length);
  const acc = files.get('primitive/accordion/features.md');
  assert.match(acc, /^# Accordion\n/);
  assert.ok(!acc.includes('<Doc'));
  assert.match(index, /references\/primitive\/accordion\/features\.md/);
});
```

*(Append a `<DocDemoViewer name="accordion:basic-demo"/>` line to the accordion fixture so the demo-inlining path is exercised.)*

- [ ] **Step 2: Update the accordion fixture to reference its demo**

```mdx
<!-- scripts/lib/__fixtures__/docs/primitive/accordion/features.mdx -->
---
title: Accordion
description: An unstyled accordion.
component: accordion
---
<DocDemoViewer name="accordion:basic-demo" mode="collapsible"/>

Body.
```

- [ ] **Step 3: Run test to verify it fails**

Run: `node --test scripts/lib/build.test.mjs`
Expected: FAIL — module not found.

- [ ] **Step 4: Write minimal implementation**

```js
// scripts/lib/build.mjs
import { readFileSync } from 'node:fs';
import { collectDocs } from './collect.mjs';
import { createDemoLookup } from './demos.mjs';
import { mdxToMarkdown } from './transform.mjs';
import { buildIndex } from './index-gen.mjs';

export function buildSlugMap(entries) {
  return new Map(entries.map((e) => [e.urlSlug, e.outPath]));
}

/** Read + transform every doc under docsRoot, inlining demos from demoRoot. */
export function buildFiles({ docsRoot, demoRoot }) {
  const entries = collectDocs(docsRoot);
  const slugMap = buildSlugMap(entries);
  const files = new Map();
  for (const e of entries) {
    const raw = readFileSync(e.srcAbs, 'utf8');
    const lookupDemo = createDemoLookup({ demoRoot, variant: e.variant });
    files.set(e.outPath, mdxToMarkdown(raw, { lookupDemo, selfOutPath: e.outPath, slugMap }));
  }
  return { files, index: buildIndex(entries), entries };
}
```

- [ ] **Step 5: Run test to verify it passes**

Run: `node --test scripts/lib/build.test.mjs`
Expected: PASS (2 tests).

- [ ] **Step 6: Run the full unit suite**

Run: `npm test`
Expected: PASS — all transform/demos/collect/index-gen/source/build tests green.

- [ ] **Step 7: Commit**

```bash
git add scripts/lib/build.mjs scripts/lib/build.test.mjs scripts/lib/__fixtures__/docs/primitive/accordion/features.mdx
git commit -m "feat(build): buildSlugMap and buildFiles integration core"
```

---

### Task 12: sync.mjs orchestrator + `--check`

**Files:**
- Create: `scripts/sync.mjs`

**Interfaces:**
- Consumes: `cloneV11`, `selectSource` (Task 10); `buildFiles` (Task 11).
- Produces: the `npm run sync` / `npm run sync:check` entry point. Writes `skills/primereact-docs/references/**`, `skills/primereact-docs/INDEX.md`, and `SOURCE.md`. `--check` diffs generated output vs committed and exits non-zero on drift.

*(No new unit test — exercised by the real run in Task 18. Keep logic thin; all testable logic lives in `build.mjs`.)*

- [ ] **Step 1: Write `scripts/sync.mjs`**

```js
// scripts/sync.mjs
import { rmSync, mkdirSync, writeFileSync, readFileSync, existsSync, readdirSync, statSync } from 'node:fs';
import { join, dirname, relative, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { cloneV11, selectSource, REPO, BRANCH } from './lib/source.mjs';
import { buildFiles } from './lib/build.mjs';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const VENDOR = join(ROOT, '.vendor', 'primereact');
const SKILL = join(ROOT, 'skills', 'primereact-docs');
const REFS = join(SKILL, 'references');
const INDEX = join(SKILL, 'INDEX.md');
const SOURCE = join(ROOT, 'SOURCE.md');
const checkMode = process.argv.includes('--check');

function readExistingRefs() {
  const out = new Map();
  if (!existsSync(REFS)) return out;
  const walk = (dir) => {
    for (const name of readdirSync(dir)) {
      const full = join(dir, name);
      if (statSync(full).isDirectory()) walk(full);
      else out.set(relative(REFS, full).split(sep).join('/'), readFileSync(full, 'utf8'));
    }
  };
  walk(REFS);
  return out;
}

function sourceStamp(sha) {
  const today = new Date().toISOString().slice(0, 10);
  return (
    '# Source\n\n' +
    'Docs mirrored from ' + REPO + ' (branch `' + BRANCH + '`).\n' +
    'Upstream commit: ' + sha + '\n' +
    'Synced: ' + today + '\n' +
    'Source mode: github-branch (MDX under apps/showcase/docs + demos under apps/showcase/demo).\n\n' +
    'When v11 ships official `/llms-full.txt` + per-page `.md` endpoints, switch the\n' +
    'rendered-md source adapter (see scripts/lib/source.mjs).\n'
  );
}

async function main() {
  const sha = cloneV11(VENDOR);
  const { docsRoot, demoRoot } = selectSource(VENDOR);
  const { files, index } = buildFiles({ docsRoot, demoRoot });

  if (checkMode) {
    const existing = readExistingRefs();
    const drift = [];
    for (const [p, c] of files) if (existing.get(p) !== c) drift.push(p);
    for (const p of existing.keys()) if (!files.has(p)) drift.push('(removed) ' + p);
    if (!existsSync(INDEX) || readFileSync(INDEX, 'utf8') !== index) drift.push('INDEX.md');
    if (drift.length) {
      console.error('Drift vs upstream ' + sha + ':\n' + drift.map((d) => '  ' + d).join('\n'));
      process.exit(1);
    }
    console.log('Up to date with upstream ' + sha);
    return;
  }

  rmSync(REFS, { recursive: true, force: true });
  for (const [p, content] of files) {
    const dest = join(REFS, p);
    mkdirSync(dirname(dest), { recursive: true });
    writeFileSync(dest, content);
  }
  writeFileSync(INDEX, index);
  writeFileSync(SOURCE, sourceStamp(sha));
  console.log('Synced ' + files.size + ' docs from ' + sha);
}

await main();
```

- [ ] **Step 2: Smoke-check the script parses (no clone yet)**

Run: `node --check scripts/sync.mjs`
Expected: no output, exit 0 (syntax OK).

- [ ] **Step 3: Commit**

```bash
git add scripts/sync.mjs
git commit -m "feat(sync): orchestrator with --check drift mode"
```

---

### Task 13: SKILL.md router (auto-trigger)

**Files:**
- Create: `skills/primereact-docs/SKILL.md`
- Test: `scripts/lib/skill-files.test.mjs`

**Interfaces:**
- Produces: the skill router with YAML frontmatter (`name: primereact-docs`, a trigger-tuned `description`). Structural test asserts frontmatter validity.

- [ ] **Step 1: Write the failing test**

```js
// scripts/lib/skill-files.test.mjs
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseFrontmatter } from './transform.mjs';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..', '..');
const SKILL = join(ROOT, 'skills', 'primereact-docs');

test('SKILL.md has name and a non-trivial description', () => {
  const { data } = parseFrontmatter(readFileSync(join(SKILL, 'SKILL.md'), 'utf8'));
  assert.equal(data.name, 'primereact-docs');
  assert.ok(data.description && data.description.length > 60);
});

test('SKILL.md references the version guardrail and INDEX', () => {
  const body = readFileSync(join(SKILL, 'SKILL.md'), 'utf8');
  assert.match(body, /migration\.md/);
  assert.match(body, /INDEX\.md/);
  assert.match(body, /package\.json/);
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test scripts/lib/skill-files.test.mjs`
Expected: FAIL — SKILL.md missing.

- [ ] **Step 3: Write `skills/primereact-docs/SKILL.md`**

```markdown
---
name: primereact-docs
description: Use when writing, configuring, or debugging PrimeReact v11 UI code — components and their props, theming and design tokens (@primeuix/themes), unstyled/PassThrough styling, Tailwind mode, forms, overlays, menus, data components, or headless hooks. Also use for PrimeReact version questions (v10 vs v11 APIs, migration, renamed/removed components). Provides the real v11 docs locally so answers come from the docs, not guesses (Claude mostly knows v10).
---

# PrimeReact v11 Docs

Local, version-pinned mirror of the **PrimeReact v11** documentation (from the
`v11` branch of `primefaces/primereact`), plus a v10→v11 version guardrail.
Ground every PrimeReact answer in these files instead of recalling APIs from
memory — v11 is a ground-up rewrite and Claude's training mostly reflects v10.

## Always start here

1. **Read `overview.md`** — the v11 mental models (four usage modes, design-token
   theming, compound components, headless hooks, PassThrough) and gotchas.
2. **Check the installed version** — `primereact` in the project's `package.json`.
   - `11.x` (or `11.0.0-*`) → use the mirrored v11 docs in `references/`.
   - `10.x` or lower → the API differs substantially; see `migration.md` and rely
     on your v10 knowledge for names/imports the v11 docs would get wrong.

## Version guardrail — STOP before writing a renamed/removed API

If the project is on **v11** and you are about to write any of these v10 names,
you are using training-memory APIs that were renamed/removed — open `migration.md`:

- `Calendar` → `DatePicker`, `Dropdown` → `Select`, `InputSwitch` → `Switch`,
  `OverlayPanel` → `Popover`, `Sidebar` → `Drawer`, `InputTextarea` → `Textarea`,
  `Chips` → `InputTags`, `TabView`/`TabPanel` → `Tabs`, `Steps` → `Stepper`.
- `import 'primereact/resources/themes/*.css'` (gone — theming is now
  `@primeuix/themes` design tokens via `PrimeReactProvider`).

Some heavy v10 components are **not yet ported to v11** (DataTable, Chart, Editor,
Select-as-data-grid, AutoComplete, TreeTable, PickList, OrderList…). For those,
say so and use v10 guidance — do not invent a v11 API.

## Task → which docs to read

Default to the **styled** variant (batteries-included) unless the project uses
unstyled/primitive, headless hooks, or Tailwind.

| Task | Read |
|---|---|
| **Getting started / install** | `references/general/gettingstarted/*`, `references/styled/installation/*` |
| **Theming / design tokens / presets / dark mode** | `references/styled/theming/*`, a component's `references/styled/<comp>/theming.md` |
| **Unstyled / PassThrough** | `references/general/passthrough.md`, `references/styled/theming/unstyled.md` |
| **Tailwind mode** | `references/general/tailwind.md`, `references/tailwind/**` |
| **A specific styled component** | `references/styled/<component>/features.md` (+ `theming.md`) |
| **Unstyled compound primitives** | `references/primitive/<component>/features.md` |
| **Headless hooks** | `references/headless/<component>/features.md`, `references/general/hooks/*` |
| **Icons** | `references/general/icons/*` |
| **Accessibility / RTL** | `references/general/guides/*` |
| **v10 → v11 migration / version mismatch** | `migration.md` |

## Anything else

Open `INDEX.md` for the full topic list, or grep for a symbol:
`grep -rni "definePreset" skills/primereact-docs/references/`.

## Provenance

`SOURCE.md` records the upstream commit + sync date. Because v11 is in active
development, the mirror can lag the branch by up to a day; for bleeding-edge
questions, confirm against the upstream repo.
```

- [ ] **Step 4: Run test to verify it passes**

Run: `node --test scripts/lib/skill-files.test.mjs`
Expected: PASS (2 tests).

- [ ] **Step 5: Commit**

```bash
git add skills/primereact-docs/SKILL.md scripts/lib/skill-files.test.mjs
git commit -m "feat(skill): SKILL.md router with auto-trigger and guardrail summary"
```

---

### Task 14: migration.md — the v10→v11 version guardrail (core value)

**Files:**
- Create: `skills/primereact-docs/migration.md`
- Modify: `scripts/lib/skill-files.test.mjs`

**Interfaces:**
- Produces: the hand-authored guardrail. Structural test asserts the rename table + theming section + "not yet in v11" list are present.

- [ ] **Step 1: Add the failing test (append to skill-files.test.mjs)**

```js
test('migration.md contains the rename map, theming change, and not-yet list', () => {
  const body = readFileSync(join(SKILL, 'migration.md'), 'utf8');
  assert.match(body, /Calendar.*DatePicker/);
  assert.match(body, /Dropdown.*Select/);
  assert.match(body, /@primeuix\/themes/);
  assert.match(body, /resources\/themes/);
  assert.match(body, /DataTable/);
  assert.match(body, /package\.json/);
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test scripts/lib/skill-files.test.mjs`
Expected: FAIL — migration.md missing.

- [ ] **Step 3: Write `skills/primereact-docs/migration.md`**

```markdown
# PrimeReact Migration & Version Guardrail (v10 → v11)

PrimeReact v11 is a **ground-up rewrite**. The mirrored docs in `references/`
describe **v11**. Before writing code, check the installed version and use this
file to bridge what your training memory (mostly v10) and the v11 docs each say.

## Step 0 — check the installed version FIRST

Read `primereact` in the project's `package.json`:

- **`11.x` / `11.0.0-*`** → use v11: new component names, `@primeuix/themes`
  theming, compound components, headless hooks. Trust `references/`.
- **`10.x` or lower** → use v10: the old names below, CSS-file themes. The v11
  docs will mislead you on names/imports; rely on v10 knowledge.
- **Not installed yet** → ask which major version, or default to v11 (latest) and
  say so.

## Renamed components — STOP if you are about to write the v10 name (on v11)

| v10 (training memory) | v11 | v11 import |
|---|---|---|
| `Calendar` | `DatePicker` | `primereact/datepicker` |
| `Dropdown` | `Select` | `primereact/select` |
| `InputSwitch` | `Switch` (ToggleSwitch) | `primereact/switch` |
| `OverlayPanel` | `Popover` | `primereact/popover` |
| `Sidebar` | `Drawer` | `primereact/drawer` |
| `InputTextarea` | `Textarea` | `primereact/textarea` |
| `Chips` | `InputTags` | `primereact/inputtags` |
| `TabView` / `TabPanel` | `Tabs` (compound: `Tabs`, `Tabs.List`, `Tabs.Tab`, `Tabs.Panel`) | `primereact/tabs` |
| `Steps` | `Stepper` | `primereact/stepper` |
| `Galleria` | `Gallery` | `primereact/gallery` |
| `ScrollPanel` | `ScrollArea` | `primereact/scrollarea` |
| `ScrollTop` | `useScrollTop` hook | `@primereact/hooks` |
| `KeyFilter` | `useKeyFilter` hook | `@primereact/hooks` |
| `InputMask` | `useMask` hook | `@primereact/hooks` |

## Theming — the biggest breaking change

**v10:** static CSS themes —
`import 'primereact/resources/themes/lara-light-cyan/theme.css';` plus
`PrimeReactContext` flags (`ripple`, `inputStyle`). **All of this is gone in v11.**

**v11:** a design-token engine from `@primeuix/themes`:

```tsx
// npm install primereact @primeuix/themes
import { PrimeReactProvider } from 'primereact';
import Aura from '@primeuix/themes/aura';

<PrimeReactProvider value={{ theme: { preset: Aura } }}>{children}</PrimeReactProvider>
```

- Built-in presets: **Aura, Material, Lara, Nora**.
- Tokens in three tiers: primitive → semantic → component; customize with
  `definePreset(...)`; dark mode via `darkModeSelector`.
- **Unstyled mode** (no built-in classes) and **Tailwind** (`tailwindcss-primeui`)
  are first-class. See `references/styled/theming/*` and `references/general/tailwind.md`.

## Not yet ported to v11 (as of the mirrored snapshot)

`DataTable`, `Chart`, `Editor`, `AutoComplete`, the data-grid `Select`/dropdown
filters, `TreeTable`, `TreeSelect`, `PickList`, `OrderList`, `CascadeSelect`,
`MultiStateCheckbox`, `TriStateCheckbox`, and several menu variants
(`MegaMenu`, `SlideMenu`, `TabMenu`, `PanelMenu`, `TieredMenu`).

For these on a v11 project: say the component is not yet in v11, and either use
the v10 component (if the project still has v10 installed) or wait for the port —
**do not invent a v11 API.** Check `INDEX.md`/`references/` to confirm presence.

## Peer dependencies & packages (v11)

- **React 19** is the target.
- Monorepo packages: `@primereact/core`, `@primereact/headless`,
  `@primereact/hooks`, `@primereact/styles`, `@primereact/types`, `@primereact/ui`.
- `@primeuix/themes` is effectively **required** for theming.
- `@primereact/types` may need explicit install for TypeScript.
- Icons via `@primereact/icons` / `@primeicons/react`.

## Direction summary

- Project on **v10** → keep v10 names + CSS-file themes; ignore v11-only APIs.
- Project on **v11** → new names + `@primeuix/themes` tokens; never reach for the
  removed v10 names or `primereact/resources/themes/*.css`.
```

- [ ] **Step 4: Run test to verify it passes**

Run: `node --test scripts/lib/skill-files.test.mjs`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add skills/primereact-docs/migration.md scripts/lib/skill-files.test.mjs
git commit -m "feat(skill): migration.md v10->v11 version guardrail"
```

---

### Task 15: overview.md — read-first mental models

**Files:**
- Create: `skills/primereact-docs/overview.md`
- Modify: `scripts/lib/skill-files.test.mjs`

**Interfaces:**
- Produces: the hand-authored read-first briefing. Structural test asserts it covers the four modes + theming + the incompleteness caveat.

- [ ] **Step 1: Add the failing test (append to skill-files.test.mjs)**

```js
test('overview.md covers the four modes and the v11-in-progress caveat', () => {
  const body = readFileSync(join(SKILL, 'overview.md'), 'utf8');
  assert.match(body, /styled/i);
  assert.match(body, /primitive/i);
  assert.match(body, /headless/i);
  assert.match(body, /tailwind/i);
  assert.match(body, /token/i);
  assert.match(body, /in (active )?development|in progress|not yet/i);
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test scripts/lib/skill-files.test.mjs`
Expected: FAIL — overview.md missing.

- [ ] **Step 3: Write `skills/primereact-docs/overview.md`**

```markdown
# PrimeReact v11 — Mental Models & Gotchas

Read this before answering any PrimeReact v11 question. v11 is a rewrite; these
are the load-bearing concepts that differ from v10.

## Four ways to use v11

A given component can be consumed in up to four modes — pick the one the project uses:

1. **Styled** (`references/styled/**`) — batteries-included components with the
   `@primeuix/themes` design-token theming. The default and most common; closest
   to the v10 mental model. Each component has `features.md` (+ often `theming.md`).
2. **Primitive** (`references/primitive/**`) — unstyled, accessible **compound**
   components (e.g. `Accordion.Root` / `Accordion.Panel` / `Accordion.Trigger`)
   with full control over markup via the polymorphic `as` prop.
3. **Headless** (`references/headless/**`, `references/general/hooks/**`) —
   behavior-only `use*` hooks; you render everything.
4. **Tailwind** (`references/tailwind/**`, `references/general/tailwind.md`) —
   the styled components wired for Tailwind via `tailwindcss-primeui`.

## Theming = design tokens, not CSS files

There is no `primereact/resources/themes/*.css` in v11. Theming is a token engine:
configure a **preset** (Aura/Material/Lara/Nora) on `PrimeReactProvider`, override
with `definePreset`, control dark mode with `darkModeSelector`. Tokens are layered
primitive → semantic → component. See `migration.md` for the import shape.

## Compound components & polymorphism

v11 favors compound APIs (sub-components like `X.Root`, `X.Item`) over the v10
monolithic single-component-with-many-props style. Most sub-components accept an
`as` prop to change the rendered element or supply a custom component, and many
`Content`-style parts accept a render-function child exposing instance state.

## PassThrough (pt)

`pt` lets you inject props/classes into internal elements; `unstyled` drops
built-in styles. See `references/general/passthrough.md`.

## Gotchas

- **v11 is in active development and incomplete.** Several v10 components are not
  yet ported (DataTable, Chart, Editor, AutoComplete, TreeTable, PickList…). If a
  component isn't under `references/`, treat it as not-yet-in-v11 — see `migration.md`.
- **Don't mix v10 names into v11 code** (Calendar/Dropdown/Sidebar/etc.) — the
  guardrail in `migration.md` lists the renames.
- **API/props tables are not mirrored yet (v2).** Where a doc shows a
  "API/props table … not yet mirrored" note, fall back to the installed
  `@primereact/types` or the upstream docs for exhaustive prop lists; the prose,
  usage snippets, and demos in each `features.md` still cover the common cases.
```

- [ ] **Step 4: Run test to verify it passes**

Run: `node --test scripts/lib/skill-files.test.mjs`
Expected: PASS.

- [ ] **Step 5: Run the full suite**

Run: `npm test`
Expected: PASS (all tests).

- [ ] **Step 6: Commit**

```bash
git add skills/primereact-docs/overview.md scripts/lib/skill-files.test.mjs
git commit -m "feat(skill): overview.md mental models"
```

---

### Task 16: Plugin packaging (plugin.json + marketplace.json)

**Files:**
- Create: `.claude-plugin/plugin.json`
- Create: `.claude-plugin/marketplace.json`
- Test: `scripts/lib/plugin-meta.test.mjs`

**Interfaces:**
- Produces: the plugin manifest (no `version`) + marketplace manifest. Test asserts JSON validity, no `version`, and matching names.

- [ ] **Step 1: Write the failing test**

```js
// scripts/lib/plugin-meta.test.mjs
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..', '..');
const read = (p) => JSON.parse(readFileSync(join(ROOT, p), 'utf8'));

test('plugin.json is valid, named, and has NO version field', () => {
  const p = read('.claude-plugin/plugin.json');
  assert.equal(p.name, 'primereact-docs');
  assert.equal(p.version, undefined);
  assert.equal(p.license, 'MIT');
});

test('marketplace.json lists the plugin from ./', () => {
  const m = read('.claude-plugin/marketplace.json');
  assert.equal(m.name, 'primereact-docs');
  assert.equal(m.plugins[0].name, 'primereact-docs');
  assert.equal(m.plugins[0].source, './');
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test scripts/lib/plugin-meta.test.mjs`
Expected: FAIL — files missing.

- [ ] **Step 3: Create `.claude-plugin/plugin.json`**

```json
{
  "name": "primereact-docs",
  "description": "Local, daily-synced mirror of the PrimeReact v11 docs (components, theming/design tokens, PassThrough, hooks) plus a v10->v11 version guardrail, so Claude answers from real v11 docs instead of guessing.",
  "author": { "name": "Pawel Topor", "url": "https://github.com/toporek" },
  "homepage": "https://github.com/toporek/primereact-docs-skill",
  "repository": "https://github.com/toporek/primereact-docs-skill",
  "license": "MIT",
  "keywords": ["primereact", "primereact-v11", "primefaces", "react", "ui-components", "theming", "documentation"]
}
```

- [ ] **Step 4: Create `.claude-plugin/marketplace.json`**

```json
{
  "name": "primereact-docs",
  "owner": { "name": "Pawel Topor", "url": "https://github.com/toporek" },
  "plugins": [
    {
      "name": "primereact-docs",
      "source": "./",
      "description": "Local, daily-synced mirror of the PrimeReact v11 docs plus a v10->v11 version guardrail."
    }
  ]
}
```

- [ ] **Step 5: Run test to verify it passes**

Run: `node --test scripts/lib/plugin-meta.test.mjs`
Expected: PASS (2 tests).

- [ ] **Step 6: Commit**

```bash
git add .claude-plugin/plugin.json .claude-plugin/marketplace.json scripts/lib/plugin-meta.test.mjs
git commit -m "feat(plugin): plugin.json and marketplace.json manifests"
```

---

### Task 17: LICENSE, README, and GitHub workflows

**Files:**
- Create: `LICENSE`
- Create: `README.md`
- Create: `.github/workflows/ci.yml`
- Create: `.github/workflows/sync.yml`

**Interfaces:**
- Produces: MIT license for tooling; README with install + attribution + non-affiliation disclaimer; CI (tests) and daily sync (PR) workflows.

- [ ] **Step 1: Create `LICENSE` (MIT)**

```
MIT License

Copyright (c) 2026 Pawel Topor

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 2: Create `README.md`**

````markdown
# primereact-docs-skill

A Claude Code plugin that mirrors the **PrimeReact v11** documentation into local,
grep-friendly Markdown so Claude Code answers PrimeReact questions (components,
theming/design tokens, PassThrough, hooks) from the real v11 docs instead of
guessing — Claude's training mostly reflects v10, and v11 is a ground-up rewrite.

Because v11 is still in active development and its docs site is often unavailable,
this gives you an **offline, grep-able, version-pinned** snapshot plus a daily
auto-sync and a v10→v11 version guardrail.

## Install

In Claude Code:

```
/plugin marketplace add toporek/primereact-docs-skill
/plugin install primereact-docs@primereact-docs
```

The skill activates automatically when you work on PrimeReact code. New commits
(including the daily docs sync) reach installed users as plugin updates.

## How it works

- `skills/primereact-docs/` — the installable skill: `SKILL.md` router,
  hand-authored `overview.md` + `migration.md` guardrail, generated `INDEX.md`,
  and `references/` (one Markdown file per upstream doc, across the `general`,
  `styled`, `primitive`, `headless`, and `tailwind` variants).
- `scripts/sync.mjs` — shallow-clones the `v11` branch of
  [primefaces/primereact](https://github.com/primefaces/primereact), transforms
  each `apps/showcase/docs/**/*.mdx` to Markdown (inlining the referenced demo
  `.tsx` examples, rewriting internal links), and regenerates `references/` +
  `INDEX.md`. The doc-body source is pluggable (`scripts/lib/source.mjs`) so it
  can switch to v11's official `.md`/`llms-full.txt` endpoints once they ship.

## Updating

```bash
npm run sync        # re-pull upstream and regenerate (commit the result)
npm run sync:check  # non-zero exit if committed output drifts from upstream
npm test            # unit tests for the transform/collect/index/source modules
```

`SOURCE.md` records the upstream commit the current mirror was generated from. A
**daily** GitHub Action opens/updates a single rolling PR when upstream changes.

> **Note (maintainers/forks):** the sync workflow opens PRs via
> `peter-evans/create-pull-request`, which requires **Settings → Actions →
> General → "Allow GitHub Actions to create and approve pull requests"**.

## Known limitations

- **API/props tables are not mirrored yet (v2).** v11 renders them from an 86 MB
  TypeDoc JSON; v1 mirrors prose, usage, and runnable demos, and shows a TODO note
  where a table would be. Use `@primereact/types` or upstream for exhaustive props.
- **v11 is incomplete.** Components not yet ported (DataTable, Chart, Editor,
  AutoComplete, …) have no `references/` entry; see `migration.md`.

## License & attribution

Documentation under `skills/primereact-docs/references/` is © PrimeFaces and the
PrimeReact contributors, mirrored from
[primefaces/primereact](https://github.com/primefaces/primereact) under the
[MIT License](LICENSE) with mechanical modifications (MDX → Markdown; demo files
inlined; internal links rewritten; API-table components replaced with TODO notes).
The sync tooling in this repo is also MIT.

This is an unofficial community project, **not affiliated with or endorsed by
PrimeFaces/PrimeTek**. "PrimeReact" and "PrimeFaces" are names of their respective owners.
````

- [ ] **Step 3: Create `.github/workflows/ci.yml`**

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request: {}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v6
        with:
          node-version: '24'
      - run: npm test
```

- [ ] **Step 4: Create `.github/workflows/sync.yml`**

```yaml
name: Sync PrimeReact v11 docs

on:
  schedule:
    - cron: '0 6 * * *' # daily 06:00 UTC
  workflow_dispatch: {}

permissions:
  contents: write
  pull-requests: write

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v6
        with:
          node-version: '24'
      - name: Run tests
        run: npm test
      - name: Regenerate from upstream
        run: npm run sync
      - name: Open PR on changes
        uses: peter-evans/create-pull-request@v8
        with:
          commit-message: 'chore: sync PrimeReact v11 docs from upstream'
          title: 'chore: sync PrimeReact v11 docs from upstream'
          body: |
            Automated regeneration of `references/` and `INDEX.md` from the
            `v11` branch of primefaces/primereact. See `SOURCE.md` for the new commit.
          branch: auto/sync-primereact-docs
          delete-branch: true
```

- [ ] **Step 5: Verify YAML/JSON parse and tests still pass**

Run: `npm test`
Expected: PASS (no test depends on these files, but confirm nothing broke).

- [ ] **Step 6: Commit**

```bash
git add LICENSE README.md .github/workflows/ci.yml .github/workflows/sync.yml
git commit -m "docs+ci: LICENSE, README, CI + daily sync workflows"
```

---

### Task 18: Generate references via a real sync + verify acceptance

**Files:**
- Create (generated): `skills/primereact-docs/references/**`, `skills/primereact-docs/INDEX.md`, `SOURCE.md`

**Interfaces:**
- Consumes: the whole pipeline. Produces the committed generated mirror.

- [ ] **Step 1: Run the real sync (network + git required)**

Run: `npm run sync`
Expected: clones the `v11` branch, prints `Synced <N> docs from <sha>` with N in the hundreds.

- [ ] **Step 2: Assert no raw JSX/JSON artifacts leaked**

Run: `grep -rnE '<Doc[A-Za-z]|<DocTable|</?[A-Z][A-Za-z0-9]+[ />]' skills/primereact-docs/references/ | grep -v '```' | head`
Expected: no JSX component tags outside code fences. (The build's `assertNoJsx` already fails hard on leaks; this is a belt-and-suspenders check. Investigate any hit.)

- [ ] **Step 3: Assert INDEX lists every generated doc**

Run: `node -e "const {readFileSync}=require('fs');const cp=require('child_process');const files=cp.execSync('find skills/primereact-docs/references -name \"*.md\"').toString().trim().split('\n').map(p=>p.replace('skills/primereact-docs/',''));const idx=readFileSync('skills/primereact-docs/INDEX.md','utf8');const missing=files.filter(f=>!idx.includes(f));console.log(missing.length?('MISSING:\n'+missing.join('\n')):'INDEX lists all '+files.length+' docs');process.exit(missing.length?1:0)"`
Expected: `INDEX lists all <N> docs`.

- [ ] **Step 4: Assert sync is idempotent**

Run: `npm run sync:check`
Expected: `Up to date with upstream <sha>` (exit 0).

- [ ] **Step 5: Spot-check a known component for fidelity**

Run: `sed -n '1,40p' skills/primereact-docs/references/styled/button/features.md`
Expected: an `# Button` H1, the description lead, prose, and at least one inlined ```tsx demo block; no `<Doc…` tags.

- [ ] **Step 6: Commit the generated mirror**

```bash
git add skills/primereact-docs/references skills/primereact-docs/INDEX.md SOURCE.md
git commit -m "chore: generate PrimeReact v11 references mirror"
```

---

### Task 19: Verify auto-trigger + guardrail (RED/GREEN) and validate the plugin

**Files:** none (verification only).

**Interfaces:** validates acceptance criteria end-to-end.

- [ ] **Step 1: Validate the plugin packaging**

Run: `claude plugin validate .`
Expected: passes (no manifest errors). If `claude` CLI is unavailable in this environment, note it and rely on the `plugin-meta` test instead.

- [ ] **Step 2: GREEN — dispatch a subagent simulating a v11 project**

Dispatch a general-purpose subagent with a prompt like: *"A project's package.json pins `primereact@11.0.0-beta.8`. The user wants to add a dropdown select and apply a dark theme. Using only the files under `skills/primereact-docs/`, what component, import, and theming setup should I use?"*
Expected: the agent reads `SKILL.md` → `migration.md`/`references/`, recommends **`Select`** (not `Dropdown`) from `primereact/select`, and `@primeuix/themes` preset + `darkModeSelector` (not a `resources/themes/*.css` import).

- [ ] **Step 2b: RED check within the same scenario**

Expected: the agent does **not** recommend `Dropdown`, `Calendar`, or `import 'primereact/resources/themes/...css'` for the v11 project.

- [ ] **Step 3: Dispatch a subagent simulating a v10 + DataTable request**

Dispatch: *"A project pins `primereact@10.9.8`. The user adds a DataTable. Using `skills/primereact-docs/`, advise."*
Expected: the agent flags that **DataTable is not yet in v11**, that the project is on v10 so v10 DataTable APIs apply, and points to `migration.md`.

- [ ] **Step 4: Record results**

If any scenario fails, refine `SKILL.md`/`migration.md` wording (these are the trigger/guardrail surfaces), re-run, and commit the wording fix:

```bash
git add skills/primereact-docs/SKILL.md skills/primereact-docs/migration.md
git commit -m "fix(skill): sharpen guardrail wording from RED/GREEN retrieval test"
```

- [ ] **Step 5: Final full-suite run**

Run: `npm test && npm run sync:check`
Expected: all unit tests pass; `sync:check` reports up-to-date.

---

## Self-Review (completed by plan author)

**Spec coverage:** sync pipeline (Tasks 2–12), pluggable source (Task 10), all-variants mirror (Tasks 8/11/18), DocTable deferral with TODO note (Task 4), demo inlining (Tasks 4/7), link rewriting (Task 5), no-JSX guard (Task 6/18), INDEX (Tasks 9/18), SOURCE stamp (Task 12), SKILL router + auto-trigger (Task 13), migration guardrail (Task 14), overview (Task 15), plugin packaging no-version (Task 16), LICENSE/README/attribution (Task 17), daily CI+sync workflows with pinned action versions (Task 17), `--check` idempotence (Tasks 12/18), RED/GREEN + `claude plugin validate` (Task 19). All spec sections map to a task.

**Placeholder scan:** the only "TODO" strings are the deliberate, in-scope DocTable deferral note and v2 markers — no plan-level placeholders.

**Type consistency:** function names/signatures are consistent across tasks — `parseFrontmatter`/`parseAttrs`/`finalizeDoc`/`transformComponents`/`rewriteDocLinks`/`assertNoJsx`/`mdxToMarkdown` (transform.mjs); `createDemoLookup` (demos.mjs); `findMdx`/`toOutPath`/`toUrlSlug`/`variantOf`/`collectDocs` (collect.mjs); `buildIndex` (index-gen.mjs); `cloneV11`/`githubBranchSource`/`renderedMdSource`/`selectSource` (source.mjs); `buildSlugMap`/`buildFiles` (build.mjs). `buildFiles` consumes `{docsRoot, demoRoot}` exactly as `selectSource` returns them.
