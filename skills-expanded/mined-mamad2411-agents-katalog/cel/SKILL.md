---
name: cel
description: >-
  CEL (Common Expression Language) v0.25: write, review and evaluate CEL
  expressions by the cel-spec language definition. Covers syntax and
  precedence, int/uint/double/bool/string/bytes/list/map/null_type, message
  types, type and dyn, timestamps and durations, gradual type checking,
  heterogeneous equality, the has/all/exists/exists_one/map/filter macros,
  standard functions and overloads, string.format, error and unknown
  semantics (commutative && and ||, partial evaluation), and the cost model.
  Current line CEL v0.25 (v0.25.3); CEL spec main is a preview (track); CEL
  v0.24 and v0.6 are legacy, upgraded from. Use when writing a policy,
  validation or filter expression in CEL, embedding a CEL environment,
  reviewing an expression for errors or cost, or upgrading from an older
  cel-spec release. Triggers: CEL, cel-spec, cel-expr, common expression
  language, no_matching_overload, no_such_field, has() macro, exists_one,
  dyn(), google.protobuf.Timestamp, ValidatingAdmissionPolicy expression,
  protovalidate rule.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Common Expression Language (CEL)

CEL is a small, side-effect-free, terminating expression language for embedding in applications, defined by the cel-spec language definition published by the CEL project (`github.com/cel-expr/cel-spec`, formerly `google/cel-spec`). With this skill the agent writes, reviews and reasons about CEL expressions, and checks an embedding against the spec.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. The language definition has no section numbers, so citations name its heading (for example "langdef, Logical Operators"). When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: expression author, reviewer, or implementer of a CEL environment or evaluator.
- Target version: CEL v0.25 (default, pinned at v0.25.3). CEL v0.24 and CEL v0.6 are legacy: read them and upgrade from them, never target them. CEL spec main is a preview (posture: track): do not depend on it. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources) first, check the cel-spec releases page for a newer tag and compare `doc/langdef.md` on master with the pinned tag, and update the pins.
- Environment: the declared variables and their types, the container (protobuf package), enabled macros and extensions, and the host's cost or size limits. These come from the host, not from CEL.
- Type checking: whether the host type-checks expressions before evaluation.

## Invariants

1. **Side-effect-free and terminating.** CEL programs only compute an output from their inputs and cannot loop forever (langdef, Overview). Extension functions must have no observable side effects, because sub-expression order is not guaranteed (langdef, Extension Functions; Evaluation).
2. **No implicit numeric conversion.** `int`, `uint` and `double` overloads take matching types; `1 + 1u` fails to dispatch (langdef, Numeric Values).
3. **Equality is heterogeneous at runtime.** Different types compare unequal rather than erroring, numbers compare across types on one number line, and NaN is unequal to itself; the type checker still requires matching types unless one side is `dyn` (langdef, Equality; Numbers).
4. **`&&` and `||` are commutative over errors.** A deciding operand (`false` for `&&`, `true` for `||`) wins regardless of side, and an error on the other side is ignored; otherwise the error propagates. Use `a ? b : false` for strict left-to-right order (langdef, Logical Operators).
5. **Errors cannot be caught.** There is no in-language error value, raise or catch; only logical operators, `?:` and macros absorb errors (langdef, Runtime Errors).
6. **Unknowns propagate like errors**, keep only critical-path members, beat errors where a value could still decide the result, and lose to errors elsewhere (eval.proto, ExprValue).
7. **`has()` takes a field selection.** On maps it tests the key; on messages it tests presence by proto2 or proto3 rules; on an undeclared message field it raises `no_such_field` (langdef, Field Selection).
8. **Unset fields read as defaults**, unset message fields as empty messages, and unset wrapper fields as `null` (langdef, Protocol Buffer Data Conversion; Dynamic Values).
9. **Overflow and out-of-range conversions are errors**, including timestamp and duration ranges (langdef, Overflow).
10. **Regular expressions are RE2 and match substrings**; anchor with `^` and `$` for full matches (langdef, Regular Expressions).
11. **Macros are the only source of exponential cost.** Implementations can limit or disable them; everything else is polynomial in program and input size (langdef, Performance Limits).
12. **Type checking never changes a result**; it can only reject an expression (langdef, Gradual Type Checking).

## Workflow

1. **Pick the version.** Target CEL v0.25 unless the user names an implementation on an older cel-spec release.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target is recorded, and it is not a legacy or preview line.
2. **Pin down the environment.** List the variables and types, container, enabled macros and extensions, expected result type, and limits from the host.
   -> [`references/errors-and-evaluation.md`](references/errors-and-evaluation.md)
   ✓ Every identifier the expression will use is declared by the host.
3. **Write the expression.** Use the grammar, literals and types, with explicit conversions and parentheses around mixed relations.
   -> [`references/syntax-and-types.md`](references/syntax-and-types.md)
   ✓ It parses, and it stays within the guaranteed nesting limits.
4. **Choose operators, functions and macros.** Check each call against its overloads and call style.
   -> [`references/operators-macros-functions.md`](references/operators-macros-functions.md)
   ✓ Every call has a matching overload for the argument types; no extension is used unless the host enables it.
5. **Make it total.** Guard optional fields, map keys, divisions, indexes, conversions and patterns so every input gives a value, and reason through error and unknown propagation.
   -> [`references/writing-expressions.md`](references/writing-expressions.md), [`references/errors-and-evaluation.md`](references/errors-and-evaluation.md)
   ✓ Allow, deny and malformed inputs each produce the intended `bool` (or declared result type).
6. **Bound the cost.** Check macros and concatenation against input sizes.
   -> [`references/errors-and-evaluation.md`](references/errors-and-evaluation.md)
   ✓ No nested or chained macro iterates over unbounded inputs, and the host's limits are met.
7. **Upgrade** (only when asked). Follow the upgrade section from the source line to CEL v0.25.
   -> [`references/versions.md`](references/versions.md)
   ✓ Expressions give the same results on representative inputs, or each difference is explained by a listed change.

## Verify before done

- [ ] The expression type-checks against the declared environment when the host supports checking (langdef, Gradual Type Checking).
- [ ] No mixed-type arithmetic, and comparisons across numeric types are explicit or `dyn` (langdef, Numeric Values; Equality).
- [ ] Every optional field or key is guarded with `has()` or `in` (langdef, Field Selection).
- [ ] Any reliance on evaluation order uses `?:`, not `&&` or `||` (langdef, Logical Operators).
- [ ] Regular expressions are anchored where an allow-list is meant, and written as raw strings (langdef, Regular Expressions; String and Bytes Values).
- [ ] Macros on maps are read as iterating keys, and `map`/`filter` results as lists (langdef, Macros).
- [ ] Results on sample inputs match the conformance behaviour for the constructs used (`tests/simple/testdata`).
- [ ] Nothing depends on CEL spec main text.

## Reference index

- **`references/versions.md`**: the version lines, what changed in v0.25, v0.7 to v0.24 and v0.6, upgrade steps, and the master-branch preview. Load for steps 1 and 7.
- **`references/syntax-and-types.md`**: grammar, precedence, lexis and reserved words, literals and escapes, values and types, protobuf and JSON mapping, name resolution, gradual typing. Load for step 3.
- **`references/operators-macros-functions.md`**: function and overload rules, equality and ordering, arithmetic, list, map, string and time functions, conversions, macros and `has()`, and `string.format`. Load for step 4.
- **`references/errors-and-evaluation.md`**: evaluation model, environment, runtime errors, commutative logic, macro errors, unknowns and partial evaluation, and the performance model. Load for steps 2, 5 and 6.
- **`references/writing-expressions.md`**: habits for safe guard expressions, a review checklist and common mistakes. Load for step 5.

## Related skills

- `openfga` for relationship-based authorization models: `npx skills add ScaleDockHQ/scaledock-skills --skill openfga`.
- `rego` for Open Policy Agent policies: `npx skills add ScaleDockHQ/scaledock-skills --skill rego`.
- `cedar` for the Cedar authorization policy language: `npx skills add ScaleDockHQ/scaledock-skills --skill cedar`.
- `json-schema` for structural validation of JSON documents: `npx skills add ScaleDockHQ/scaledock-skills --skill json-schema`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [CEL Language Definition (doc/langdef.md)](https://github.com/cel-expr/cel-spec/blob/v0.25.3/doc/langdef.md): Released, v0.25.3, checked 2026-10-05.
- [CEL Introduction (doc/intro.md)](https://github.com/cel-expr/cel-spec/blob/v0.25.3/doc/intro.md): Released, v0.25.3, checked 2026-10-05.
- [CEL Strings extension (doc/extensions/strings.md)](https://github.com/cel-expr/cel-spec/blob/v0.25.3/doc/extensions/strings.md): Released, v0.25.3, checked 2026-10-05.
- [CEL evaluation result protos (proto/cel/expr/eval.proto)](https://github.com/cel-expr/cel-spec/blob/v0.25.3/proto/cel/expr/eval.proto): Released, v0.25.3, checked 2026-10-05.
- [CEL Conformance Tests (tests/README.md)](https://github.com/cel-expr/cel-spec/blob/v0.25.3/tests/README.md): Released, v0.25.3, checked 2026-10-05.
- [CEL simple conformance test data](https://github.com/cel-expr/cel-spec/tree/v0.25.3/tests/simple/testdata): Released, v0.25.3, checked 2026-10-05.
- [cel-spec releases](https://github.com/cel-expr/cel-spec/releases): release notes, v0.0.1 to v0.25.3, checked 2026-10-05.
- [CEL Language Definition, master branch](https://github.com/cel-expr/cel-spec/blob/master/doc/langdef.md): unreleased (development branch), master at 40a3c90 (2026-09-16), checked 2026-10-05.
- [CEL Language Definition v0.24.0](https://github.com/cel-expr/cel-spec/blob/v0.24.0/doc/langdef.md): Released (superseded), v0.24.0, checked 2026-10-05.
- [CEL Language Definition v0.6.0](https://github.com/cel-expr/cel-spec/blob/v0.6.0/doc/langdef.md): Released (superseded), v0.6.0, checked 2026-10-05.
- [cel.dev](https://cel.dev): project website, as published 2026-10-05, checked 2026-10-05.
- [cel.dev CEL overview](https://cel.dev/overview/cel-overview): project website, as published 2026-10-05, checked 2026-10-05.
