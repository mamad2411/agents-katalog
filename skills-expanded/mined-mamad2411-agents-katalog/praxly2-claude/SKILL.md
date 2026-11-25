# Praxly2 — Claude Agent Onboarding

This is the fast-start guide for Claude agents. Read the full project guidelines in [copilot-instructions.md](.github/copilot-instructions.md), the authoritative language definitions in [specs/](specs/), and the detailed architecture docs in [docs/](docs/).

## What this project is

An in-browser multi-language compiler and translator for CS education. Users write code in **Python, Java, JavaScript, CSP pseudocode, Praxis pseudocode, or Blocks** (Blockly, `src/language/blocks/` — its "source text" is workspace JSON). Every language shares one **Universal AST** — no language-specific AST nodes, ever. The AST can be interpreted directly or translated to any other supported language. No backend; everything runs client-side.

## Architecture in 30 seconds

```
Source text
  → Lexer          (src/language/<lang>/lexer.ts)
  → Parser         (src/language/<lang>/parser.ts)
  → Universal AST  (src/language/ast.ts)
  → Interpreter    (src/language/interpreter.ts)    ← executes directly
  → Translator     (src/language/translator.ts)     ← type inference pass
  → Emitter        (src/language/<lang>/emitter.ts) ← generates target code
```

The **Visitor pattern** (`src/language/visitor.ts`) is the spine. Every emitter extends `ASTVisitor` and implements `visitX()` methods. The `Translator.analyze()` pass builds `TranslationContext` (symbol table, inferred types, mutable collections) before dispatching to emitters.

## Critical invariants

1. **One Universal AST** — parsers produce only nodes defined in `ast.ts`. Never add language-specific node types.
2. **All AST nodes require `id: generateId()`** — the debugger and source maps depend on unique IDs.
3. **TypeScript strict mode** — `noUnusedLocals` and `noUnusedParameters` are on. Every new `visit*` method must be listed as `abstract` in `ASTVisitor`.
4. **No global store for editor state** — pages are composition only; behavior lives in hooks under `src/hooks/`, pure transforms in `src/utils/`. Zustand (`src/store/appStore.ts`) covers only chat, AI prefs, BYOK, and the editor bridge.
5. **When adding a new `Statement` node type**: update `ast.ts`, `visitor.ts` (abstract method + dispatch case), all 4+ emitters, `interpreter.ts`, and `translator.ts` (recurse into body in `analyzeBlock`).

## Key files to read first

| File                                      | Why                                                              |
| ----------------------------------------- | ---------------------------------------------------------------- |
| `src/language/ast.ts`                     | All AST node types                                               |
| `src/language/visitor.ts`                 | `ASTVisitor` base, `Precedence` constants, `TargetLanguage` type |
| `src/language/interpreter.ts`             | How AST is executed                                              |
| `src/language/translator.ts`              | Type inference + emitter dispatch                                |
| `src/components/LanguageSelector.tsx`     | `SupportedLang` + `LANG_LABELS` (no component — types only)      |
| `src/hooks/useCodeParsing.ts`             | Where lexers/parsers are wired to the UI                         |
| `src/hooks/useEditorExecution.ts`         | Editor parse/run/debug orchestration                             |
| `src/hooks/useTranslationPanels.ts`       | Which translation panels are open, and their layout              |
| `src/utils/editorUtils.ts`                | CodeMirror language extensions                                   |
| `src/components/editor/AddPanelStrip.tsx` | `PANEL_LANGS` array                                              |
| `src/components/editor/SourcePane.tsx`    | `SOURCE_OPTIONS` array                                           |

## Build & Test

```bash
npm run dev          # Vite dev server → http://localhost:5173/v2/
npm run build        # TypeScript check + production build
npm run test:run     # Vitest unit tests, single run (`npm run test` = watch mode)
npm run test-browser # Selenium csv/ regression suite (needs Chrome; NOT run by test:run)
npx tsc --noEmit     # Type-check only
```

Unit tests live in `tests/` — one file per language (`python.test.ts`, `java.test.ts`, `csp.test.ts`, `praxis.test.ts`, `javascript.test.ts`) plus `round-trip.test.ts` (translate each demo to every target, assert output equivalence) and `examples.test.ts`. The `csv/praxly.test.csv` matrix is the original regression suite, run in a browser via `npm run test-browser` (Selenium) — it is **not** part of `npm run test:run`, so verify against it after parser/interpreter changes. Do **not** edit that CSV.

## Project directories

- **`specs/`** — the **authoritative language definitions** and source of truth for what each
  language supports (syntax, semantics, and deliberate omissions). One file per language
  (`praxis.md`, `csp.md`, `java.md`, `javascript.md`, `python.md`, `blocks.md`) plus `stdlib.md` (the shared
  built-in library mapped across all five languages, with notes on cross-language differences).
  Read the relevant spec before changing a parser/interpreter/emitter, and update it when
  language behavior changes. `praxis.md`/`csp.md`/`java.md` also have an **Extensions for
  Praxly** section for anything beyond the original exam reference.
- **`examples/`** — one runnable demo per language (`demo.praxis`, `demo.csp`, `demo.java`,
  `demo.js`, `demo.py`), each exercising every AST node its parser can produce. `round-trip.test.ts`
  translates each demo to every target and checks output equivalence; see `examples/README.md`
  for the coverage policy. Random/`input()` are intentionally kept out of the auto-run demos
  (non-deterministic / need stdin) and covered by unit tests instead.
- **`docs/`** — deeper architecture references: `COMPILER_PIPELINE.md`, `AST_REFERENCE.md`,
  `COMPONENT_REFERENCE.md`, `ADDING_A_LANGUAGE.md`, `COMMON_ISSUES.md`.

## Common tasks → skills

Invoke these by name; they load on demand rather than sitting in context.

| Skill                                                      | Use it when                                                        |
| ---------------------------------------------------------- | ------------------------------------------------------------------ |
| [`add-language`](.claude/skills/add-language/SKILL.md)     | Adding a source/target language, or it isn't showing in the UI     |
| [`add-tests`](.claude/skills/add-tests/SKILL.md)           | Writing Vitest tests, or picking which test file a case belongs in |
| [`add-ui-feature`](.claude/skills/add-ui-feature/SKILL.md) | Any UI change — deciding which hook or component owns the state    |
| [`verify`](.claude/skills/verify/SKILL.md)                 | Driving the real app in Chrome to confirm a change end to end      |

## Language definitions

`specs/` is the authority for each language's supported syntax, semantics, and standard library
— including what each front-end deliberately rejects. Do **not** duplicate or paraphrase
language rules here (they drift): read the relevant `specs/*.md` file, and update it in the same
change whenever you alter a language's behavior.
