---
name: sideroom-guidelines
description: "Follow the mandatory coding workflow before any write or edit, including bug fixes, features, refactors, tests, configuration, and documentation edits. Load the complete skill and exact language guide through sideroom_guidelines or full read calls for Java, PHP/Laravel, JavaScript/JSX, TypeScript/TSX, Python, Go, or Rust targets. Discussion or read-only investigation alone does not require loading it."
license: MIT
metadata:
  author: RMRdeveloper
  version: "1.0"
---

# Sideroom guidelines

## Activation Contract

Before `write` or `edit`, call `sideroom_guidelines` with the target file's `path`. On first load it returns this whole skill and the matching complete language guide, or only this skill for unsupported languages. Later calls return only missing complete documents; an already loaded target receives a short acknowledgement. Reuse loaded guides during the same agent run; load any additional target language before editing it. Reload after compaction or a new run.

Alternatively, load this whole skill with `read`, without `offset` or `limit`, using the absolute packaged path shown in Available Skills. For each supported target language, also fully load its exact guide from `references/languages/`. Both routes satisfy the same gate only on successful, complete delivery.

## Hard Rules

- Apply the loaded guide to changed code in the context of the full user requirements and established project contracts. Architectural rules require demonstrated evidence; KISS, DRY, and YAGNI never justify omitting requested behavior, required error handling, compatibility, or meaningful tests.
- Do not write or edit until the required packaged documents are fully loaded through `sideroom_guidelines` or exact full-file `read` calls; failed or partial loads and same-named files do not count.
- Do not bypass the gate with Bash, a subprocess, or another mutation tool.
- Do not load language guides unrelated to files being changed.
- Fail fast, keep control flow flat, and validate once at the boundary.

## Decision Gates

| Path | Read |
| ------ | ------ |
| `.java` | `references/languages/java.md` |
| `.js` `.jsx` `.mjs` `.cjs` | `references/languages/javascript.md` |
| `.php` | `references/languages/php-laravel.md` |
| `.ts` `.tsx` | `references/languages/typescript.md` |
| `.py` | `references/languages/python.md` |
| `.go` | `references/languages/go.md` |
| `.rs` | `references/languages/rust.md` |
| other | shared table only |

## Execution Steps

1. Load this complete skill through `sideroom_guidelines` with the target path, or a full `read` of its packaged path, before any mutation.
2. Ensure the matching complete language guide is loaded for supported extensions. The tool includes it automatically; with `read`, load it separately.
3. Implement a focused change that satisfies all current requirements and preserves required existing behavior.
4. Review the changes introduced by this run against the loaded guide; fix demonstrated violations caused by the change without refactoring unrelated code.
5. Run the relevant formatter, linter, type checks, and tests before finishing.

## Do / Don't

| Do | Don't |
| --- | --- |
| Braces around every `if` body (Python: a full indented suite) | Unbraced or one-line conditional bodies |
| Early return on bad input | Pyramid `if/else` nesting |
| Explicit error, fail now | Fallbacks that hide the real failure |
| One responsibility per unit | Validate + transform + persist + notify together |
| Extract for real duplication, a present responsibility, or testability | Abstract only for hypothetical future reuse |
| Decomposition by intent (rule 20): name a coherent operation so its caller reads the flow without implementation details, even with one caller | Split only to shorten functions, or separate coupled steps into shared mutable state, excessive parameters, or functions that must be read together |
| Simplest design that satisfies the full requirements | Omit necessary structure to minimize code |
| Implement current requirements and established contracts completely | Add capabilities only for hypothetical future cases |
| Compose small focused units | Deep inheritance for unrelated behavior |
| Talk only to immediate collaborators | Reach through another object's internals |
| A function either does or returns, not both | Side effects inside a getter |
| Validate once at the edge | Re-check the same invariant inward |
| One validator per input | Two validators for the same body/query |
| Let errors surface with context | Empty `catch` or catch-and-continue |
| Return new values instead of mutating input | Mutate parameters |
| One meaning per null/undefined | Overload null for several business states |
| Inject dependencies | Hardcode infra that blocks tests |
| Inner layers depend on nothing outward | Domain imports of DB/HTTP/framework types |
| Names that reveal role or domain meaning | `data`, `info`, `temp`, `result`, `obj` |
| Named const/enum/contract for domain literals | Magic strings |
| Depend on ports where variation is real | Couple a use case to a concrete implementation |
| Comments only for non-obvious intent | Narration, noise, or stale TODOs |

For JavaScript and TypeScript, a function with 3 or more parameters uses one object destructured in the parameter list, unless an external or public compatibility contract fixes the signature. See the language guide for examples.

## Output Contract

Changed code follows every applicable rule in the loaded complete guide. The final response names the validation run and any check that could not run. No extra files, layers, comments, or bypass mutations unless the requirement needs them.

## References

- `references/languages/java.md`
- `references/languages/javascript.md`
- `references/languages/php-laravel.md`
- `references/languages/typescript.md`
- `references/languages/python.md`
- `references/languages/go.md`
- `references/languages/rust.md`
