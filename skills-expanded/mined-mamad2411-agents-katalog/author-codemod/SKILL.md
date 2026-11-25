---
name: author-codemod
description: Writes, fixture-tests, and runs codebase-wide automated transforms (codemods) that parse source to an AST and rewrite nodes via grammar-aware tools (jscodeshift/ts-morph, ast-grep, Comby, libcst/Bowler, OpenRewrite), dry-running before applying one mechanical change across many files. Use when a structural edit must hit many call sites reliably and find-replace would mangle strings, comments, or shadowed names.
when_to_use: One mechanical change must land across many files — rename/move an exported API across all call sites, swap a deprecated call, rewrite an import path or signature, migrate an idiom (callbacks→async, class→hooks). Distinct from refactor-cleanup (judgment-driven edits in a few files), dependency-upgrade (bumping versions), and regex-build (a single pattern, not a tree transform).
---

## When to Use

Reach for this skill when the **same structural edit must hit many files** and correctness depends on understanding the code's grammar, not its text:

- "Rename `getUser` → `fetchUser` everywhere, including imports/exports/JSX, but not the string `"getUser"` in logs"
- "Replace every `moment(x)` with `dayjs(x)` across the repo"
- "Change the import path `@old/pkg` → `@new/pkg` and rewrite the now-renamed named exports"
- "Migrate all `React.Component` classes to function components / hooks"
- "Add `await` to every call site of a function that became async"
- "Swap deprecated `assert.equal` → `assert.strictEqual` repo-wide"

NOT this skill:
- A judgment-heavy cleanup in 1–3 files where each edit is a decision, not a rule → refactor-cleanup
- Bumping a package version and fixing the fallout it causes → dependency-upgrade (a codemod may be a *step* inside it)
- One search/replace pattern over text where a tree isn't needed → regex-build
- Reviewing the resulting diff for bugs → code-review
- Schema/data changes in a running DB → db-migration-safety

## Steps

1. **Pick the tool by language and edit shape — don't reach for `sed`.** A grammar-aware tool refuses to touch strings, comments, and shadowed bindings; text tools can't tell them apart.

   | Language / scope | Tool | Reach for it when |
   |---|---|---|
   | JS/TS, complex semantic rewrite | **jscodeshift** (Babel/recast AST) | rename across imports/exports/JSX, signature changes; preserves formatting via recast |
   | TS, type-aware, follow references | **ts-morph** | needs the type checker — find *all* references to a symbol, not name matches |
   | JS/TS/Go/Python/Rust, pattern→pattern | **ast-grep** (`sg`) | declarative `pattern:`/`rewrite:` in YAML, polyglot, fast, no JS to write |
   | Any language, structural find/replace | **Comby** | lightweight `:[hole]` matchers when you don't want a full AST pass |
   | Python | **libcst** (or **Bowler** for simple cases) | preserves comments + formatting; libcst for graph-aware, Bowler for fluent one-liners |
   | Java/Kotlin | **OpenRewrite** (recipes) | type-aware recipes, dependency + API migrations at scale |

   Default: **ast-grep** for a clean pattern→pattern swap in any language; **jscodeshift** when the JS/TS rewrite needs real logic; **ts-morph** when you must follow type references, not text.

2. **Characterize on 2–3 representative files first, then enumerate edge cases.** Open real call sites and write down what must and must NOT change. Hostile cases that break naive transforms:
   - **Shadowing** — a local `const getUser = ...` that is *not* the imported symbol.
   - **Re-exports / aliases** — `export { getUser as gu }`, `import { getUser as g }`.
   - **Dynamic access** — `obj["getUser"]`, computed members, reflection — usually out of AST reach; list them as manual tail.
   - **Strings & comments** — must be left alone unless explicitly targeted.
   - **Formatting** — preserve it (recast/libcst/ts-morph do; a naive print does not).
   - **Partial matches** — `getUserById` must not be caught by a `getUser` rule.

3. **Write the transform as code and test it on fixtures before touching the tree.** The codemod is software — assert before/after so a bad rule can't run silently. jscodeshift skeleton:

   ```js
   // rename-getUser.js — jscodeshift transform
   module.exports = function (file, api) {
     const j = api.jscodeshift;
     const root = j(file.source);
     // only rename the IMPORTED binding, follow its local name (handles aliases)
     root.find(j.ImportSpecifier, { imported: { name: 'getUser' } })
       .forEach((p) => {
         const local = p.node.local.name;            // respects `as` alias
         root.find(j.Identifier, { name: local })
           .filter((id) => id.parent.node.type !== 'ImportSpecifier')
           .forEach((id) => { id.node.name = 'fetchUser'; });
         p.node.imported.name = 'fetchUser';
       });
     return root.toSource({ quote: 'single' });
   };
   ```
   ```js
   // rename-getUser.test.js — the codemod itself is under test
   const { applyTransform } = require('jscodeshift/dist/testUtils');
   const t = require('./rename-getUser');
   test('renames imported symbol, not the shadow or the string', () => {
     expect(applyTransform(t, {}, { source:
       `import { getUser } from './api';\nconst x = getUser(1);\nlog("getUser");` }))
     .toBe(
       `import { fetchUser } from './api';\nconst x = fetchUser(1);\nlog("getUser");`);
   });
   ```
   ast-grep equivalent needs no test harness but still gets a fixture diff: `sg run -p 'getUser($A)' -r 'fetchUser($A)' --lang ts fixtures/ --dry-run`.

4. **Dry-run across the whole tree; review stats and sampled hunks; tune to zero false hits.** Never let the first run write. jscodeshift `--dry --print` (or `-d -p`), ast-grep `--dry-run`, Comby without `-i`, libcst via a `--no-write` flag. Inspect the **count** of changed files and read a random sample of hunks — if any touch a string, comment, or shadow, fix the rule and re-dry-run. Iterate until the only diff is the intended one.

5. **Apply, then immediately run the toolchain — the codemod's output is unverified until the build agrees.** Run formatter → linter → typecheck → tests in that order: `prettier --write` / `gofmt`, then `eslint --fix`, then `tsc --noEmit`, then the suite. A green typecheck is the strongest signal a JS/TS rename hit every real reference; a red one points straight at a missed or over-eager site.

6. **Handle the long tail manually and document it.** Dynamic access, generated code, vendored files, and cross-package boundaries the AST can't follow stay broken — `grep` the old name to find survivors, fix them by hand, and note in the commit what the codemod could not reach and why.

7. **Commit the transform script alongside its diff.** Check in the codemod file + its fixture test in the same commit as the generated changes, with the exact command in the message. The change becomes reproducible, reviewable as a rule (not N edits), and re-runnable when stragglers appear.

## Common Errors

- **`sed`/find-replace across a grammar.** Rewrites the symbol inside strings, comments, and shadowed locals. Use an AST tool that distinguishes node kinds.
- **Matching the name, not the binding.** A bare `Identifier` rename also hits an unrelated local `getUser`. Anchor to the import/declaration and follow its references (ts-morph `findReferences`, or trace the local name as in step 3).
- **Ignoring `as` aliases and re-exports.** `import { getUser as g }` renames nothing if you only look for `getUser` identifiers. Read `local` vs `imported`; rewrite both the export and its consumers.
- **Substring false positives.** A `getUser` text rule mangles `getUserById`/`getUsers`. AST identifier matching is exact; text rules need word boundaries and review.
- **Printing instead of patching the AST** (`root.toSource()` from a fresh print) reflows the whole file — huge noise diff. Use recast (jscodeshift default), libcst, or ts-morph to preserve untouched formatting.
- **No fixture test on the codemod.** A subtle rule bug silently corrupts hundreds of files. Assert before/after on representative inputs *before* the tree run.
- **Skipping the dry-run.** First run writes; you discover the over-match after it's everywhere. Always dry-run, read sampled hunks, then apply.
- **Trusting "0 errors" without a typecheck.** A rename can compile-pass yet miss dynamic call sites. Run `tsc`/tests after; `grep` the old name for survivors.
- **Letting the formatter mask a bad transform.** Running `prettier` first can hide a structural mistake behind reformatting. Diff the raw codemod output, *then* format.
- **One mega-transform doing five things.** Unreviewable and unrevertable. One codemod = one rule; chain separate scripts.

## Verify

1. **Fixture tests pass:** the codemod's own before/after assertions are green, including a shadow case, an alias/re-export case, and a string-that-must-not-change case.
2. **Dry-run is clean:** the dry-run diff contains only intended hunks — zero edits inside strings, comments, or shadowed locals (confirm by reading a random sample, not just the count).
3. **No stragglers:** `grep -rn '\bgetUser\b'` (old name, word-bounded) over the tree returns only the documented manual tail — nothing the codemod should have caught.
4. **Toolchain agrees:** formatter clean, linter clean, `tsc --noEmit` (or language equivalent) exits 0, full test suite passes on the transformed tree.
5. **Diff is minimal:** changed lines are the transform's effect only — no incidental reformatting of untouched code.
6. **Reproducible:** the codemod script + fixture test are committed with the diff and the exact run command; re-running the codemod on the result is a no-op.

Done = fixture tests + dry-run are clean, the post-apply toolchain (format/lint/typecheck/tests) is fully green, no undocumented stragglers remain, and the transform script ships in the same commit so the change re-runs deterministically.
