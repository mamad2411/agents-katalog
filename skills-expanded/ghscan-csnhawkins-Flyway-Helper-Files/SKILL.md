---
name: flyway-generate-migration
description: Generates a Flyway migration script from the current schema model and code-reviews it - the "generate & review" half of the Flyway MCP workflow, using the Flyway MCP tools (mcp__flyway__*). Use this whenever asked to generate, create, or write a migration script, or to review one already generated - even if the request doesn't mention "Flyway" or "MCP" by name (e.g. "make me a migration for this", "generate a script", "review the migration"). This assumes the schema model already reflects the intended change; if the database hasn't been diffed and captured yet, that's the separate flyway-capture-schema skill.
allowed-tools: mcp__flyway__load_project, mcp__flyway__reload_project, mcp__flyway__create_diff_migrations, mcp__flyway__generate_migrations, mcp__flyway__review_code, Read, Bash(git fetch:*), Bash(git status:*), Bash(git log:*)
---

# Flyway - Generate & Review a Migration

Turns whatever's currently captured in the Flyway schema model into a migration script, then runs
Flyway's code review against it. This is one of two independent Flyway MCP skills - it does not
diff a database or update the schema model. If the schema model doesn't already reflect the change
you're expecting, say so and ask whether the caller wants it captured first (`flyway-capture-schema`)
rather than assuming it's already up to date.

## Step 0: preflight check

Before anything else, run the check described in `../_shared/flyway-preflight.md` - confirms the
local checkout isn't behind on migrations before generating one, so you don't pick a version
number a teammate has already claimed upstream. This is mandatory, not optional, and comes before
Step 1 below.

## Steps

1. **`load_project`** (or `reload_project` if a project is already loaded and might be stale) -
   always first.
2. **`create_diff_migrations`** then **`generate_migrations`** - produce the migration script from
   the current schema model.
3. **`review_code`** - always run this on what you generated. Never skip it, and never report a
   result you haven't actually run.

See `../_shared/flyway-guardrails.md` for how to handle destructive/ambiguous changes, environment
scope, and what this skill doesn't do - those rules apply here in full.

## Never hand-edit what you generated

If something about a generated script looks wrong, regenerate it from an updated schema model
instead of patching the SQL directly. This skill has no edit tools available - that's deliberate,
not an oversight, and it's what keeps the schema model and the script in sync as a single source
of truth.

## Never suppress or soften a code review finding

Report the review result exactly as returned - full findings, not just a pass/fail, and never a
severity downgraded because it "felt minor." That decision isn't this skill's to make.

## Output format

**If the calling prompt asks for structured/JSON output** (an automation script or pipeline will
say so explicitly - look for it), respond with ONLY a single, raw JSON object and nothing else,
even if there was nothing to generate. Do not wrap it in a markdown code fence. Do not add
commentary before or after it. Use exactly these field names:

```json
{
  "status": "clean" | "issues_found" | "no_changes",
  "migrationFile": "<path to the generated migration script, relative to the project folder, or null>",
  "description": "<short one-line description of the change, or null>",
  "reviewSummary": "<one paragraph plain-English summary of the code review result, or a one-line note that there was nothing to change>",
  "rulesChecked": <number, or 0>,
  "issues": ["<issue text, prefixed with its severity>", "..."]
}
```

If there was nothing in the schema model to generate a migration for, still reply with exactly this
shape:

```json
{"status": "no_changes", "migrationFile": null, "description": null, "reviewSummary": "No schema model changes were found to generate a migration for.", "rulesChecked": 0, "issues": []}
```

This exact schema exists because looser instructions ("respond with a summary and the file path")
have reliably drifted into different field names and shapes across runs, breaking whatever is
parsing the output on the other end.

**Otherwise** (a person is talking to you directly, no structured-output instruction was given),
just communicate naturally - a short explanation of what was generated and what the review found is
more useful to a person reading a terminal than a JSON blob.

## Naming

Migration descriptions should be short, specific, and filename-safe: no spaces or punctuation - use
hyphens between words instead, since this text becomes part of the actual file name Flyway writes
to disk (e.g. "add-offers-table-and-getoffers-procedure" - not "add offers table and getOffers
procedure", "schema update", or "misc changes"). Follow whatever versioning/naming convention
already exists in the project's `migrations/` folder rather than inventing a new one.