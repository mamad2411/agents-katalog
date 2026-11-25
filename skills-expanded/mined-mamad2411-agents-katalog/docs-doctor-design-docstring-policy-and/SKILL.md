# Docstring policy and review skill

Status: the separate skill and local Ruff fixtures are implemented. The proposed
OpenGHG policy and first Ruff ratchet are under review in
[OpenGHG PR 1738](https://github.com/openghg/openghg/pull/1738).

## Decision

Treat Python docstrings as a distinct documentation layer and give them a small,
separate review skill. Keep that skill connected to the broader documentation workflow
through shared maintenance triggers and escalation rules.

The separation is justified by a genuinely different unit of work:

| Concern | Assessment and authoring skills | Python docstring-review skill |
| --- | --- | --- |
| Trigger | A user need, page, feature, audit, or documentation-impact decision | Changed Python modules, public objects, signatures, or caller-visible behaviour |
| Primary evidence | User tasks, docs navigation, interfaces, examples, design records, support evidence | Source, annotations, exports, tests, generated API output, and repository docstring policy |
| Typical output | A plan, page or patch, audit findings, or impact decision | Findings or a minimal patch for changed docstrings |
| Main failure | The material does not help the intended reader or is false | The callable contract is missing, stale, misleading, or rendered incorrectly |
| Natural validation | Build, links, examples, preview, user or domain review | Diff scope, Ruff, signature agreement, focused tests, and generated API build |

This is not a claim that docstrings are independent documentation. They feed generated
API reference and may point to authored pages. The split exists to make frequent code
review quick and predictable, while the general skill retains responsibility for
tutorials, how-to guides, explanations, navigation, and cross-page coherence.

Current OpenAI guidance recommends keeping each skill focused on one job and using a
discriminating description to control activation. The bounded trigger and output above
meet that test better than loading the whole documentation workflow for every changed
function. See [Build skills](https://learn.chatgpt.com/docs/build-skills).

## What PR 1730 establishes

OpenGHG [PR 1730](https://github.com/openghg/openghg/pull/1730), “Add shared AI coding
guidance”, already provides a useful starting policy in `AGENTS.md`:

- Google-style docstrings for every public function, method, and class and for
  complicated private objects;
- at least one meaningful sentence for simple private helpers and tests;
- caller-visible contracts, including scientific units, dimensions, coordinates,
  accepted values, mutation, lazy or eager behaviour, and relevant exceptions; and
- no repetition of types already expressed by annotations.

The PR also makes public exports explicit through `__all__`, `_EXPORTS`, and sibling
stubs. Those declarations are better evidence of public status than filename or a
leading underscore alone.

The proposed policy is not yet a complete enforceable contract:

- it does not say when modules and packages require docstrings;
- it does not define where constructor arguments are documented or how inherited and
  overridden methods are handled;
- it does not distinguish a useful one-line private or test docstring from a sentence
  that merely restates the name;
- it does not define which exceptions are relevant enough to document;
- it does not state how generated API pages expose these docstrings; and
- OpenGHG's Ruff configuration currently selects `E`, `F`, and `W`, not the `D`
  docstring rules, so the written policy and automated enforcement differ.

These are appropriate decisions for a short repository document, not for expanding a
root agent-instruction file.

## Canonical OpenGHG document

Use `doc/source/development/docstrings.rst`, matching OpenGHG's existing Sphinx and
reStructuredText structure. Link it from `doc/source/development/index_devel.rst` and
from the docstring summary in `python_devel.rst`. Keep only the high-frequency rule and
the link in `AGENTS.md`.

This creates one source of truth:

```text
doc/source/development/docstrings.rst   normative human-readable policy
                 ↑
AGENTS.md and python_devel.rst           short summary and link
                 ↑
python-docstring-review skill            discovers and applies the policy
                 ↑
Ruff, Sphinx, and later Vale rules        enforce selected mechanical parts
```

The page should remain brief: object-specific rules, two or three representative
examples, maintenance triggers, validation commands, and links to the adopted Google
format and relevant tool documentation. It should not reproduce the Google guide.

## Proposed policy choices

The following choices make the PR 1730 wording precise enough for consistent human,
agent, and tool review.

### Scope and authority

- The policy applies to production Python, test functions where the project explicitly
  requires descriptions, and docstrings rendered into the API reference.
- The implementation, signature, annotations, public-export declarations, and tests
  are evidence for behaviour. A stale docstring does not override them.
- Google style is the presentation dialect. OpenGHG's local choices below override
  generic examples in an external style guide.
- Annotations are authoritative for Python types. Docstrings add meaning that the type
  cannot express.

### Object matrix

| Object | Required content |
| --- | --- |
| Public package or module | A meaningful summary of its responsibility. Add important scope, import-time effects, or relationships only when callers or maintainers need them. |
| Private implementation module | A summary when purpose, invariants, registration, side effects, or relation to the public facade is not evident. Do not require a filename restatement. |
| Public function | Behavioural summary; parameter meaning and constraints; result meaning; caller-visible side effects; relevant exceptions; and scientific contract where applicable. |
| Public method | The same contract as a public function, plus state read or changed and any lifecycle preconditions. Do not repeat an inherited contract unless the override changes it. |
| Class | Responsibility, important invariants, lifecycle or state, constructor parameter meaning, and public attributes where useful. Choose the class docstring as the single canonical home for constructor documentation. |
| Property | Meaning of the exposed value, including units, shape, mutability, caching, or cost where relevant. |
| Complicated private callable or class | The contract, invariant, algorithmic reason, or failure condition needed for safe maintenance. |
| Simple private helper or test | Follow the explicit OpenGHG choice in PR 1730: one meaningful sentence describing behaviour or scenario. Revisit this rule if review shows repeated name-restatement noise. |

For scientific and data APIs, “contract” can include units, dimensions, coordinates,
alignment, missing-data behaviour, metadata effects, eager or lazy computation,
mutation, ordering, randomness, tolerance, validation envelope, and limitations. Include
only the dimensions that affect the object being documented.

Document exceptions that form an intentional caller-visible outcome or important
recovery branch. Do not attempt to enumerate incidental exceptions from every internal
operation.

### Avoided duplication

- Do not repeat annotated types in `Args` or `Returns` entries.
- Do not duplicate constructor arguments between a class and `__init__`.
- Do not restate an inherited method contract when inheritance is accurate and visible.
- Do not turn tutorials, long algorithms, model theory, architecture history, or
  multi-step workflows into docstrings. Link to the appropriate authored page.
- Do not use a docstring where a source comment is needed to explain an implementation
  reason or workaround.

### Maintenance triggers

Review a docstring in the same change when any of these change:

- public name, signature, default, accepted value, return or yield behaviour;
- state mutation, side effect, performance or lazy/eager behaviour;
- exception or warning that callers are expected to handle;
- units, shapes, dimensions, coordinates, metadata, missing-data treatment, numerical
  assumption, or limitation;
- class lifecycle, invariant, public attribute, inheritance, or deprecation; or
- public export status or generated-reference placement.

A changed implementation with none of these effects may record `no docstring impact`
with a short reason. This is the docstring-specific form of the general maintenance
contract.

## Enforcement model

Use three layers and keep their claims separate.

### 1. Deterministic checks

Ruff already exists in OpenGHG. Its stable `D100`–`D104` rules can check missing public
module, class, method, function, and package docstrings, and its pydocstyle settings can
select the Google convention. Ruff's `DOC` rules can compare some parameters, returns,
yields, and exceptions with code, but they are currently preview rules. See the
[Ruff rules](https://docs.astral.sh/ruff/rules/) and
[pydocstyle settings](https://docs.astral.sh/ruff/settings/#lintpydocstyle).

Do not enable every docstring rule as a repository-wide blocking check in one step.
First decide the exact policy, measure the existing baseline, resolve mutually
exclusive style rules, and trial checks on changed files. Start with stable rules that
directly encode adopted decisions. Treat preview rules as a non-blocking experiment
until their behaviour is acceptable and their version is pinned.

Sphinx should remain the rendering check. It can reveal malformed sections,
cross-reference failures, import problems, and differences between a syntactically
valid docstring and the generated page.

Vale is not the primary docstring-structure checker. It may later check adopted
terminology or a few prose patterns inside docstrings, using the same exclusions and
severity policy as other documentation. It cannot determine public status, signature
agreement, or scientific truth.

### 2. Lightweight agent review

The skill checks semantics that deterministic tools cannot establish: whether a
description matches behaviour, whether the important scientific contract is present,
whether a “meaningful sentence” adds information, and whether a long explanation
belongs elsewhere.

### 3. Human or domain review

Require a maintainer or domain reviewer when a docstring states or changes scientific
meaning, uncertainty, validation limits, security behaviour, destructive effects, or
an intentionally breaking public contract.

## `python-docstring-review` skill contract

Provisional description:

> Review or minimally revise Python docstrings affected by a code change, using the
> repository's docstring policy, public API declarations, implementation, annotations,
> and tests. Use for an explicit docstring review or when an adopter's pull-request
> policy requires one; not for general documentation audits, tutorials, or broad prose
> polishing.

The first version should be instructions only. It needs no custom script while `git
diff`, source search, Ruff, and the Sphinx build are sufficient.

### Inputs

- assessment-only or edit-authorised intent;
- diff, base reference, or explicit file/object scope;
- repository policy path, discovered if not supplied; and
- relevant validation command from local project guidance.

### Workflow

1. Read the repository docstring policy and tool configuration.
2. Identify changed Python objects and whether they are public using repository export
   declarations, not naming alone.
3. Determine whether each change affects the caller-visible or maintainer contract.
4. Compare relevant docstrings with signatures, annotations, implementation, tests,
   generated-reference exposure, and adjacent docs.
5. Run configured, changed-scope checks. Do not introduce or reconfigure a linter during
   a review unless requested.
6. In assessment mode, report only actionable findings. In edit mode, make the smallest
   policy-conforming changes and rerun the focused checks.
7. Escalate tutorials, explanations, cross-page restructuring, or disputed scientific
   meaning to the broader documentation workflow or a human reviewer.

### Finding format

Each finding should contain:

`object and location · policy clause · evidence · caller/maintainer consequence · minimal action`

Do not report a preference without a policy clause or concrete reader consequence.
Absence of findings means that the reviewed scope conforms to the checked policy; it is
not a claim that every docstring in the repository is correct.

### Activation boundary

Positive triggers include an explicit request to write or review Python docstrings, a
public API change whose local policy requires docstring impact review, or a targeted
docstring-maintenance task. Negative triggers include ordinary coding with no adopted
impact policy, general prose editing, a Sphinx page audit, and a request to classify
documentation with Diátaxis.

Keep implicit activation conservative during the first pilot. The skill may be invoked
automatically for pull-request review only after OpenGHG's repository policy explicitly
requires that route and trigger evaluation shows acceptable precision.

## Evaluation cases

Before relying on the skill, test at least these cases:

1. a new exported function has no docstring and has units and dimensions visible only
   in tests;
2. a signature rename leaves a stale `Args` entry while annotations remain correct;
3. an internal refactor changes no contract and should produce `no impact`;
4. an overridden method accurately inherits its contract and should not be duplicated;
5. a trivial private helper has a sentence that only restates its name;
6. a class duplicates constructor documentation in the class and `__init__`;
7. a scientific docstring proposes changing a qualification the agent cannot verify and
   must request domain review; and
8. a long model explanation should be moved or linked to authored documentation rather
   than expanded in the docstring.

Evaluate correct non-activation as well as correct findings. Compare the skill with
Ruff-only review so its added semantic value is visible.

## OpenGHG baseline and rollout

Ruff 0.16.2 on OpenGHG `devel` at `4223b11` found no missing docstrings for
production public classes, methods, or functions (`D101`–`D103`). The same rules found
346 existing omissions in tests. Broader candidates are not zero-debt: production has
one `D100`, 30 `D104`, 98 `D417`, and six `D419` findings.

PR 1738 therefore selects only `D101`, `D102`, and `D103`, uses Ruff's Google
convention, and exempts tests from those mechanical presence checks. The human policy
still requires meaningful descriptions for new and materially changed tests. Module,
package, empty-docstring, and parameter-completeness rules remain review concerns until
their baselines are resolved. This is a ratchet, not a claim that existing docstrings
are semantically complete.

The full strict Sphinx build reads the new policy page but fails on the pre-existing
documentation baseline, including malformed existing docstrings, missing and duplicate
references, inconsistent headings, and notebook execution restrictions. Standalone
strict docutils validation of the policy page passes.

Rollout sequence:

1. Review and merge the concise OpenGHG policy page and zero-debt Ruff ratchet in
   PR 1738.
2. Link PR 1730 or its replacement to the canonical policy after its stack is resolved.
3. Pilot the instruction-only review skill assessment-only on a few pull requests.
4. Resolve module, package, empty-docstring, and parameter-completeness debt in bounded
   changes before enabling more rules.
5. Consider preview Ruff `DOC` rules and Vale terminology checks only after collecting
   false positives and pinning the intended behaviour.

This order makes the written policy authoritative before tools begin enforcing a
partial or accidental interpretation of it.
