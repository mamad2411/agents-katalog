---
name: separate-content-from-formatting-commits
description: When a file's diff mixes reformatting with semantic changes, build N intermediate states — one per content change in the original format — commit each atomically, then optionally finish with a pure style reformat commit.
category: Git & Repository Management
---

# Separate Content Changes from Formatting Commits

> **Skill ID:** `separate-content-from-formatting-commits`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

When a tool (editor, formatter, runtime) has reformatted a file AND the
user made several semantic changes in the same working-tree edit, the
resulting diff is unreadable and cannot be cleanly split with
`git add -p`. This skill turns that messy diff into a chain of pristine
atomic commits:

1. **Content commits first** — each content change is applied to the
   file in its **original format** (byte-preserving, no whitespace churn).
2. **Reformat commit last** (optional) — a single `style:` commit that
   applies the new formatting to the fully-changed content.

This produces a history that reviewers can follow change-by-change,
bisect correctly, and revert surgically.

## Source Rules

This skill operationalizes
[`git-atomic-commit-construction/SKILL.md` — Step 13 (Intermediate State Synthesis)](../git-atomic-commit-construction/SKILL.md)
for the specific case of format-mixed file diffs.

## Prerequisites

| Requirement | Minimum |
| --- | --- |
| Python | 3.7+ (stdlib only — `json`, `pathlib`, `argparse`) |
| Git | 2.x+ |
| Working knowledge | The caller must identify the ordered semantic changes manually |

Verify Python is available:

```bash
python3 --version
```

## When to Apply

Apply this skill when **ALL** of the following are true:

- A single file in the working tree has both formatting changes (indent
  style, key sort order, trailing newline changes) AND content changes
  (renamed keys, new values, added/removed entries).
- The formatting changes are pervasive enough that `git add -p` cannot
  cleanly isolate individual content hunks.
- The user wants each semantic change in its own atomic commit.

This skill works for **any file type** — JSON, YAML, TOML, INI, XML,
plain text — as long as the content changes can be expressed as ordered
textual substitutions.

## Script Inventory

| Script | Approach | When to use |
| --- | --- | --- |
| [`scripts/build-states-textual.py`](scripts/build-states-textual.py) | Plain-text substring replace | **Default.** Preserves original format byte-for-byte. Content commits land on the old format; the optional final commit reformats. |
| [`scripts/build-states-json-roundtrip.py`](scripts/build-states-json-roundtrip.py) | JSON parse → mutate → re-serialize | Use only when the user wants the reformat baked into the FIRST commit (all states carry the new format). |

**Python justification (§Script Language Mandate override):** Both scripts
manipulate structured text best expressed via Python's `json` module and
string operations. Python is the de-facto standard for this domain and
matches the precedent set by `json-deep-sort` and `json-block-indent-override`.

## Step-by-Step Procedure

### Step 1 — Capture the Baseline

```bash
# Baseline = last committed state of the file
git show HEAD:<relative-path-to-file> > /tmp/baseline.txt
```

### Step 2 — Identify Ordered Semantic Changes

Read the full diff carefully:

```bash
git diff <file>
```

List every semantic change in the order you want them committed.
Ignore formatting noise — those lines are handled automatically.

Example ordered list (for a JSON config):

1. Rename API key `openRouterApiKey` → `openrouter_api_key`
2. Change default model value
3. Add two new hook subscriptions
4. Enable a plugin flag
5. Set `effortLevel` to `max`

### Step 3 — Build the Edits File

For `build-states-textual.py`, write a JSON edits file where each element
corresponds to one atomic commit:

```bash
cat > /tmp/edits.json << 'EOF'
[
  {"kind": "replace_unique", "old": "\"openRouterApiKey\"", "new": "\"openrouter_api_key\""},
  {"kind": "replace_unique", "old": "\"old-model-name\"",   "new": "\"new-model-name\""},
  {"kind": "append_before_suffix", "suffix": "  }\n}\n", "insert": "    <new-hook-block>\n"}
]
EOF
```

Edit kinds:

| Kind | Behaviour |
| --- | --- |
| `replace` | Replace ALL occurrences. Asserts at least one found. |
| `replace_unique` | Assert old appears EXACTLY once, then replace. Prevents accidental multi-site edits. |
| `append_before_suffix` | Insert text immediately before the file's trailing suffix (e.g., closing braces). |

### Step 4 — Run the Builder Script

```bash
python3 /path/to/skills/separate-content-from-formatting-commits/scripts/build-states-textual.py \
  --baseline /tmp/baseline.txt \
  --edits    /tmp/edits.json \
  --out-dir  /tmp/states \
  --target   <working-tree-file>   # optional: verifies final state matches
```

Output: `/tmp/states/state-1.out`, `state-2.out`, … one per edit.

### Step 5 — Commit Each Intermediate State

For each state N:

```bash
# Place the intermediate state onto the working tree
cp /tmp/states/state-N.out <working-tree-file>

# Stage only that file
git add <working-tree-file>

# Commit with a focused message
git commit -m "chore(<scope>): <description of this one semantic change>

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

Repeat for every state until N = total edits.

### Step 6 — Optional: Reformat Commit (style:)

If a tool had reformatted the file, restore the working-tree version to
the fully-reformatted final state and commit it as a `style:` commit:

```bash
# The actual working-tree file already has the reformat — just stage it
git add <working-tree-file>
git commit -m "style(<scope>): apply <formatter-name> formatting

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

### Step 7 — Verify

```bash
# Working tree should be clean
git status

# Final commit should match what the tool originally produced
git diff HEAD
```

### Manual Approach (Restore-and-Reapply)

When the automated script pipeline is disproportionate or the edits are
hand-crafted semantic changes to a skill/rule/doc file (not tool-driven
reformatting), use the manual restore-and-reapply workflow instead.

**Use this variant when:**

- Changes are authored by hand (new sections, paragraphs, protocol steps)
  rather than produced by a formatter or linter fix.
- Each change deserves independent review (skill docs, rule files,
  configuration narratives).
- The user requests "maximum atomic commits" with per-change visibility.
- The file has 3–8 logical changes — the overhead of writing an `edits.json`
  manifest exceeds the benefit.

**Do NOT use when:**

- The diff is large (10+ changes) — the script pipeline is faster and less
  error-prone.
- The formatting change is pervasive (e.g., indent style, key sort) and
  applies to a structured file (JSON, YAML, TOML) — use the script pipeline.
- `git add -p` can cleanly isolate content hunks — use `add -p` directly.

#### Step 1 — Catalog the Diff

Read the full diff and classify each hunk as either **content** (semantic
meaning changes) or **formatting** (whitespace, heading level, table style,
blank line insertion):

```bash
git diff <file-path>
```

Create a mental or written ordered list of content changes (top to bottom
in the file), then a separate list of formatting changes.

#### Step 2 — Restore to Clean Baseline

```bash
git checkout -- <file-path>
git diff HEAD -- <file-path>   # verify: must be empty
```

This discards the dirty working-tree state. All content changes will be
re-applied from scratch — the original diff is your change list.

#### Step 3 — Apply Content Changes One by One

For each content change in the catalog (top-to-bottom order):

1. Apply the change using a text-editor tool or script.
2. Stage and commit:

   ```bash
   git add <file-path>
   git commit -m "feat(<scope>): <description of this one change>"
   ```

3. Verify the commit:

   ```bash
   git log -1 --oneline
   git diff HEAD~1 HEAD --stat
   ```

Continue until all content changes are committed. Track progress against
your catalog to avoid missing or duplicating a change.

#### Step 4 — Apply Formatting Changes

After all content commits are landed, apply the formatting-only changes:

1. Apply each formatting fix (heading demotion, table separator style,
   blank line insertion, etc.).
2. Stage and commit:

   ```bash
   git add <file-path>
   git commit -m "refactor(<scope>): fix formatting — heading levels, table layout, blank lines"
   ```

The formatting commit MUST always be last — never interleave formatting
between content commits, as that breaks `git blame` traceability.

#### Step 5 — Verify

```bash
git status                       # must be clean
git log --oneline -5             # review commit chain
git diff HEAD                    # must be empty (matches clean tree)
```

The final commit history should show N content commits followed by 0 or 1
formatting commit — never mixed.

**Live-session example** (this skill's companion `git-stash-triage` skill,
2026-06-15): a single SKILL.md had accumulated 4 content additions (Phase 0
timestamp capture, Phase 2 blob-hash supersession check + timeline analysis,
§4d non-destructive extraction, traceability update) interleaved with
formatting drift (heading levels, table separator style, blank lines before
code blocks). The restore-and-reapply workflow produced 4 content commits
(`feat:`, `feat:`, `docs:`) and 1 final formatting commit (`refactor:`).
No mixed-content commit reached the log.

## JSON Round-Trip Variant

Use [`scripts/build-states-json-roundtrip.py`](scripts/build-states-json-roundtrip.py)
when the user wants the reformat embedded in the FIRST commit. Each state
is re-serialized with the new indent style, so all commits after state-1
are already on the new format.

Mutations file schema — each top-level array element covers one commit's
worth of operations:

```bash
cat > /tmp/mutations.json << 'EOF'
[
  [{"op": "rename_key", "parent_path": ["hooks"], "from": "OldKey", "to": "NewKey"}],
  [{"op": "set",        "parent_path": [], "key": "effortLevel", "value": "max"}]
]
EOF

python3 /path/to/skills/separate-content-from-formatting-commits/scripts/build-states-json-roundtrip.py \
  --baseline  /tmp/baseline.txt \
  --mutations /tmp/mutations.json \
  --out-dir   /tmp/states \
  --indent    tab \
  --target    <working-tree-file>
```

## Guardrails

- **Never skip the `--target` check** on the final state — it proves the
  builder reproduced the working-tree file exactly.
- **Use `replace_unique`** for edits where the old string might appear in
  multiple locations; a `replace` that changes the wrong site will corrupt
  subsequent states.
- **Preserve commit order** — each intermediate state must be a strict
  superset of the previous one's changes.
- **Do not reformat between content commits** — the reformat commit MUST
  come last (or first in the round-trip variant), never sandwiched between
  content commits.

## Related Skills

- [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md) — parent skill; this skill
  extends Step 13 (Intermediate State Synthesis) for format-mixed files.
- [`json-block-indent-override`](../json-block-indent-override/SKILL.md) — re-indents a specific JSON key block
  (useful as a post-content-commits formatting step for JSON files).
- [`json-deep-sort`](../json-deep-sort/SKILL.md) — sorts JSON keys alphabetically (complementary reformatter).
- [`skill-factory`](../skill-factory/SKILL.md) — governs skill-doc editing discipline (§5); the manual
  approach is the recommended technique when enriching existing skill files.

## Traceability

This skill was extracted from a live session in which `claude/settings.json`
in a private configurations repository contained 5 semantic changes that
needed to be split into 5 atomic commits. An initial JSON round-trip
approach (re-serializing with tab indent) was rejected by the user because
the working-tree file's actual format was 2-space indent with
insertion-order keys — the round-trip would have introduced a spurious
reformat. The format-preserving textual script then produced 5 commits,
each landing on the original 2-space format with zero whitespace churn,
and no trailing `style:` reformat commit was needed.

Session target log: `<private-config-repo>` branch `stash/changes-on-macOS`,
commits `421a63e` → `718c8b3`.

The lesson — **always inspect the baseline's actual byte-level format
before choosing a script variant** — is encoded in Step 1 (Capture the
Baseline) and the script-selection table above.

- A subsequent session enriched `git-stash-triage/SKILL.md` with 4 content
  additions (Phase 0 timestamp capture, Phase 2 blob-hash supersession check,
  timeline analysis, §4d non-destructive extraction, traceability update)
  while the file also carried formatting drift (heading level fixes, table
  separator style, blank lines before code blocks from `markdownlint-cli2
  --fix`). The manual restore-and-reapply workflow produced 4 content commits
  followed by 1 formatting-only commit — demonstrating the manual approach
  documented in this skill.
