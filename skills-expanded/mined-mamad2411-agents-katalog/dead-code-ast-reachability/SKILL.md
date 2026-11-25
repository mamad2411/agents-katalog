---
name: dead-code-ast-reachability
description: >-
  Build a call graph by parsing source to an abstract syntax tree, and use it to
  separate findings that are false positives about risk from findings that are
  false positives about code. Use when a queue is full of unreachable findings,
  when deciding whether a function is dead, or when a scanner reports a defect
  in code nothing calls.
allowed-tools: Read, Grep, Glob
---

# Dead code is a true positive about the code and a false positive about the risk

Both halves matter and teams act on only one.

The finding is **correct**: the concatenation is there, the sink is real, and a
reviewer who opens the file will agree. What is wrong is the implied
consequence, because nothing untrusted reaches it. Triaging it costs exactly as
much as triaging one on the login path, and there are usually far more of them —
so a queue that does not separate the two is a queue engineers learn to ignore,
which costs you the reachable ones as well.

Deciding which is which needs a **call graph**, and a call graph needs the
**abstract syntax tree**. Grep cannot do it: `def report` and `report(` and
`# report` are the same string to a regex, and a function named `run` appears in
every file in the repository. Parsing to an AST gives you the two node types the
question actually needs — `FunctionDef` for what exists, `Call` for what invokes
it — with their real nesting, so "which functions call this one" stops being a
text search and becomes a graph walk.

The AST is also honest about its own limits, which is the more useful half. It
resolves a literal call and it cannot resolve `getattr(mod, name)()`, a dispatch
dictionary, or a handler a framework wires by decorator at import time. Those
are not unreachable. They are **undecided**, and filing them as unreachable is
how a pipeline drops real bugs quietly.

## When to use this
When reachability analysis produces a large unreachable bucket, before any bulk
suppression, and during any dead-code or deprecation sweep — the security queue
is the cheapest available list of which dead code to delete first. Also
whenever a finding is about to be dismissed as "that code isn't called": this
is how that sentence gets evidence behind it.

## Step-by-step

**1 — Parse, do not grep.** `ast.parse(source)` per file. Collect every
`FunctionDef` and `AsyncFunctionDef` as a node; collect every `Call` as an edge
from its enclosing function.

**2 — Resolve each call to a name.** `Call.func` is a `Name` for `f()` and an
`Attribute` for `obj.f()`. Take `.id` or `.attr`. This is deliberately naive
about which `f` is meant — two functions of the same name in different modules
merge — and it errs toward *reachable*, which is the safe direction.

**3 — Mark entry points.** Anything decorated as a route or handler, anything
exported, anything a scheduler names. An entry point is reachable by definition,
and getting this list wrong is the largest source of error in the whole
procedure.

**4 — Walk from the entry points.** Everything reached is `reachable`.
Everything not reached is *either* dead *or* undecided, and step 5 decides.

**5 — Separate `unreachable` from `unknown`, never collapse them.** If the file
contains a dynamic call the AST could not resolve — `getattr`, a dispatch table,
a decorator that registers — every unreached function in that module is
`unknown`, not `unreachable`. Report the three buckets separately.

**6 — Only then classify the findings.** A finding on a reachable unit keeps its
severity. One on a genuinely dead unit is a false positive about risk and a true
positive about code, and belongs in a deletion list rather than a triage queue.
One on an `unknown` unit is unresolved work, not a clean result.

## Example

Input — two files, one entry point, one dynamic call:

```python
# api.py
@route("/reports")            # entry point
def list_reports(request):
    return render(load(request.args["id"]))

def load(rid): ...            # called by list_reports
def legacy_export(path): ...  # called by nothing

# jobs.py
def dispatch(name):
    return getattr(handlers, name)()   # unresolvable by AST
def nightly(): ...
```

Output:

```
reachable    list_reports, load           reached from an entry point
unreachable  legacy_export                no caller, no dynamic call in api.py
unknown      dispatch, nightly            jobs.py contains getattr(...)()
```

`nightly` is not dead. It is in a module the AST could not fully resolve, so
*every* unreached function in that module is undecided — and saying so is the
whole difference between this procedure and a shorter one.

## Output contract

```json
{
  "graph": {"functions": 0, "edges": 0, "entry_points": ["str"]},
  "buckets": {"reachable": 0, "unreachable": 0, "unknown": 0},
  "unresolved_calls": [{"file": "str", "why": "getattr|dispatch-table|decorator"}],
  "findings": [{"id": "str", "unit": "str", "bucket": "str",
                "true_about_code": true, "true_about_risk": false}],
  "queue": {"before": 0, "after": 0}
}
```

`unresolved_calls` is what makes the `unknown` bucket auditable. A report with
an empty `unknown` bucket and no `unresolved_calls` entry has either a very
simple codebase or a bug.

## Common edge cases

- **Two functions with the same name.** The naive resolver merges them and
  over-reports reachability. That is the safe direction; the unsafe one is a
  clever resolver that guesses wrong and marks a live function dead.
- **A decorator that registers the function.** `@app.route`, `@celery.task`,
  `@click.command`. The function has no caller in the source and is reachable
  from outside it. Treat every decorated function as an entry point unless you
  know the decorator.
- **Tests as callers.** A function called only from tests is dead in
  production. Exclude test files from the graph or you will never find any.
- **A method called through an instance.** `Attribute` gives you `.attr`, which
  is the method name without the class. Same over-reporting, same safe
  direction.
- **`__init__.py` re-exports.** A function imported and re-exported has no call
  edge at all and is reachable by import. Follow `ImportFrom` or accept it as
  `unknown`.

## Failure modes

- **Grepping for the name instead of parsing.** Comments, strings and unrelated
  functions with the same name all match, and the answer is unusable in either
  direction.
- **Collapsing `unknown` into `unreachable`.** It makes the queue shorter and
  it is how framework-wired handlers get dropped.
- **Trusting the entry-point list.** Every function is unreachable if you forgot
  the routes file.
- **Deleting on the graph's word alone.** Reachability from *untrusted* entry
  points is not reachability from anywhere; check both before a deletion.
