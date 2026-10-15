---
name: wikicommit-review
description: Validate and review a manually created or edited wiki page, then mark it reviewed
disable-model-invocation: true
---

# wikicommit-review

For a page under `.wikicommit/entity/`, this proposes frontmatter completions, checks that `sources` exists, checks the consistency between `sources.hash` and the actual file, re-fetches the page's `sources` and performs an independent, source-grounded fact-check against them (Issue #455 — presenting per-criterion findings for the reviewer's explicit confirmation, rather than just re-displaying the page's full text and asking the human to do the checking unaided), and finally records the review as complete. How that last step is recorded depends on which route the page came from (Issue #313):

- **Route B** (a page a human directly created or edited locally, with no tracking Issue): writes `review_status: reviewed` to the page's frontmatter locally. This serves as proof that a human completed the review on the spot; the user then runs `/wikicommit-merge` to commit and merge it as `reviewed`.
- **Route A** (a page `wikicommit-generate` produced, tracked by an open `wikicommit-review`-labeled Issue that `wikicommit-merge` Step 8 created): closes that tracking Issue via `gh issue close`, rather than writing `review_status` locally. Closing the Issue is what triggers `.github/workflows/review-issue-close-sync.yml` to flip `review_status` to `reviewed` on `main` and auto-merge that change once quality checks pass. Running `wikicommit-review` on a Route A page no longer bypasses anything — closing its tracking Issue *is* the mandatory review gate for Route A, now that a solo operator can actually close an Issue they opened (unlike approving their own PR, which GitHub disallows).

Which of the two applies is determined automatically per page (Step 5) — the user does not need to know which route a given page came from.

## Usage

```
/wikicommit-review <page>   # e.g. /wikicommit-review .wikicommit/entity/ja/Person/yamada-taro.md
/wikicommit-review          # if the argument is omitted, present candidates for the user to choose from
```

## Processing Flow

### Step 0: Determine the Target Page

If an argument is given, use it as the target page.

If the argument is omitted:

```bash
git -c core.quotePath=false status --porcelain -- ".wikicommit/entity/**/*.md"
```

List pages with uncommitted changes (untracked or modified) and let the user pick one. If the output is empty, display "No target pages" and stop.

If the target file does not exist, display an error and stop.

### Step 1: Complete Frontmatter

1. Run:

   ```bash
   python .wikicommit/scripts/validate_frontmatter.py <page>
   ```

2. Extract the names of missing fields from the `ERROR:` lines in the output (lines containing the literal string `必須フィールドがありません`, which is what `validate_frontmatter.py` currently prints for a missing required field; format-violation errors are not subject to completion proposals — they are only presented to the user in step 4).
3. Determine the corresponding schema file from the target page's `type`:
   - `schema:Person` → `.wikicommit/schema/Person.md`
   - `schema:custom/Decision` → `.wikicommit/schema/custom/Decision.md`
   - Fall back to `.wikicommit/schema/default.md` if it does not exist
4. If there are missing fields, have the LLM propose completions using the page body and the type schema's `properties:` block (its keys and any inline template comments) as clues. **Get the user's confirmation before** writing to the frontmatter (never rewrite without asking). Leave any field the user declines to complete as-is. A completion for a key that belongs under `properties:` (Issue #495) must be nested there, not written flat at the top level.
5. If there are format-violation errors (missing `sha256:` prefix, invalid date format, etc.), likewise present them to the user and fix them only after confirmation.
6. After completion, re-run `python .wikicommit/scripts/validate_frontmatter.py <page>` to check for any remaining errors. Errors caused by fields the user declined to complete may remain — proceeding to the next step is fine (whether to proceed overall is ultimately left to the user in step 4).

### Step 2: Check `sources`

- If the target page is a translated page with `translated_from`, exempt it from the `sources` check (same exception rule as `validate_frontmatter.py` — source information is inherited from the parent page).
- If `sources` does not exist (and the page is not a translated page), prompt to set `type: manual`. Confirm `author` (the creator's name) and `created_at` (`YYYY-MM-DD` format; suggest today's date if omitted) with the user, and add to `sources` in the following form:

  ```yaml
  sources:
    - type: manual
      author: "<user input>"
      created_at: "<YYYY-MM-DD>"
  ```

### Step 3: Consistency Check

For each element of `sources` with `type: path`:

1. Recompute the SHA-256 of the actual file at `sources[].path`:

   ```bash
   python3 -c "
   import hashlib, sys
   h = hashlib.sha256()
   with open(sys.argv[1], 'rb') as f:
       for chunk in iter(lambda: f.read(65536), b''):
           h.update(chunk)
   print(f'sha256:{h.hexdigest()}')
   " "<sources[].path>"
   ```

2. Compare the recomputed result with `sources[].hash`.
3. If they don't match, present it to the user and confirm whether to update `hash` to the recomputed value (never overwrite without asking). If the user declines, leave it as-is.

If `sources[].path` does not exist in the repository, this has already been detected as an ERROR in step 1, so skip recomputation here.

### Step 4: Independent Fact-Check Against Sources

Steps 1–3 only validate structure (frontmatter shape, `sources` presence, hash consistency) — none of them actually check the page's content against anything. This step does that (Issue #455), reusing the source-fetching logic `wikicommit-fix` Step 3 already implements and the same review perspective the tracking-Issue template in `docs/DesignDoc-pipeline.md` §6.2 asks human reviewers to apply.

**For the strongest result, run this Skill in a separate session (and, if practical, a different model) from whichever one generated the page** — see step 2 below for why, and `docs/DesignDoc-skills.md` §11.0/§11.4 for why WikiCommit's BYOLLM, agent-native design makes this possible without any extra setup.

1. **Fetch the source documents** (same routing as `wikicommit-fix` Step 3, extended with a third route for synthesized pages — Issue #537):
   - If `sources` is non-empty, use the normal per-element routing below — `derived_from` (`DesignDoc-data.md` §4.2) and `translated_from` only exempt a page from `sources` being *required*, not from carrying one (`validate_frontmatter.py` skips the required-field check for these pages but still format-validates `sources` if present; `wikicommit-fix` Step 3's translated-page branch draws the same "permitted, not required" distinction).
   - Otherwise, if the page has `derived_from` (a `wikicommit-synthesize` output, Issue #283), read each `derived_from[].path` entry directly with the Read tool — these are `.wikicommit/entity/` pages within this repo, not external sources needing extraction or fetching. A page written before the Issue #477 `.wikicommit/wiki/` → `.wikicommit/entity/` rename may still store the old prefix in this field with no auto-migration (`DesignDoc-data.md` §3.1); if the literal stored path doesn't exist, retry after substituting `.wikicommit/entity/` for a leading `.wikicommit/wiki/` before concluding the entry is missing (same tolerance Step 5 item 1 applies to the tracking-Issue marker path). Treat each entry independently — a page with several `derived_from` entries where only some paths resolve should still fact-check against whichever entries were successfully read.
   - Otherwise, if `sources` is empty and the page is a translated page with `translated_from`, read the parent page's `sources` instead (source information is inherited per `DesignDoc-data.md` §4.2).
   - For each element of `sources`:
     - `type: path` and `.md`/`.txt` → read directly with the Read tool
     - `type: path` with any other extension → call the corresponding extraction skill per the "Prerequisite Skills (Text Extraction)" table in `.claude/skills/wikicommit-generate/SKILL.md`. If the required skill is not installed, guide the user through the install command and stop.
     - `type: url` / `type: wikicommit` → fetch `source.url` with the WebFetch tool
     - `type: manual` → no source document exists for this page
   - If no source document could be obtained at all (fetch failure, `type: manual`, empty `sources` with no parent page to fall back to, or every `derived_from` entry's path unresolvable), there is no ground truth to check the page against — skip step 3 and go straight to the full-text fallback in step 4.

2. **Self-report the currently running model ID** (the same self-identification pattern `wikicommit-generate` Pass 3 uses — see that SKILL.md's "Set `generated_by` to the currently running model ID" step) and compare it to the page's frontmatter `generated_by` (or, for a translated page with `translated_from`, its `translated_by` — the field `wikicommit-translate` writes instead of `generated_by`), whichever is present. If they match, note in your output that this review is not independent of the generation/translation that produced the page, and recommend re-running `/wikicommit-review` in a separate session and/or under a different model for a stronger check. Skip this note entirely if neither field is present (typical for Route B pages a human created or edited directly, which never went through `wikicommit-generate`/`wikicommit-translate`).

3. **Check the page against the fetched source documents**, reporting one finding per item (`OK`, or `要確認: <reason>`), using the checklist that matches the page's provenance field — the same three-way split `wikicommit-merge` Step 8's tracking-Issue template uses (`docs/DesignDoc-pipeline.md` §6.2, Issue #525):
   - **Page has `translated_from`** (a translation): does the translation accurately reflect the meaning of the source page? Is terminology consistent with the `DefinedTerm/` glossary? Does the translation read naturally (not awkward or overly literal)?
   - **Page has `derived_from`** (a `wikicommit-synthesize` output): does the content accurately reflect the pages listed in `derived_from`? Are there no claims unsupported by those pages? Are the WikiLink targets appropriate?
   - **Otherwise** (a `sources`-based page): does the content match the source document(s)? Are there factual errors or hallucinations? Are the WikiLink targets appropriate? Only if this page's `type` was newly added to `.wikicommit/schema/` during the batch that generated it (i.e. via `wikicommit-generate` Pass 2b, Issue #315) — is the type/`recommended`-field selection appropriate?

   Apply the same evidence-binding discipline `wikicommit-generate` Pass 4 uses (Issue #442): judge each claim solely against the literal text of the fetched source document in front of you, never against your own world knowledge of whether the claim happens to be true. A well-known-to-be-true claim still fails this check if the source text doesn't actually state it; an obscure or surprising claim passes if the source text does state it.

4. **Do not display the page's full text by default.** Present only the findings from steps 2–3 to the reviewer. Fall back to displaying the full content (frontmatter + body) when either the reviewer explicitly asks to see it, or step 1 found no usable source document — this preserves Issue #313's original guarantee (a human actually read the page) for exactly the cases where the fact-check above has no ground truth to lean on.

5. Ask the reviewer to explicitly confirm they've reviewed the findings (and full text, if shown) and it looks correct. Phrase this confirmation prompt per `docs/DesignDoc-skills.md` §11.8 — describe what confirming will do (e.g. "so I can record this review as complete") rather than naming the internal step that follows. If the reviewer declines or flags a problem, stop here without doing anything in Step 5; let them fix the page (directly, or via `/wikicommit-fix`) and re-run `/wikicommit-review` afterward.

### Step 5: Check for a Tracking Issue, Then Record Review Completion

1. Check whether the target page has an open tracking Issue (created by `wikicommit-merge` Step 8 for Route A pages):

   ```bash
   gh issue list --label wikicommit-review --state open --json number,body --limit 1000
   ```

   Scan the returned `body` values locally for the exact marker `<!-- wikicommit-page: <page> -->`, where `<page>` is the target page's repo-relative path (e.g. `.wikicommit/entity/ja/Person/yamada-taro.md`) **or** the same marker with `.wikicommit/entity/` replaced by the pre-Issue-#477 `.wikicommit/wiki/` (an Issue opened before that rename still embeds its marker with the old prefix verbatim; no auto-migration, `docs/DesignDoc-data.md` §4.3's coexistence precedent) — matching only the current-prefix form would misclassify such a page as Route B (no Issue found) and write `review_status: reviewed` locally instead of closing the real Issue, leaving it open and orphaned. Do not rely on `gh issue list --search` for this (same tokenization caveat as `wikicommit-merge` Step 8's "Checking for Existing Tracking Issues" — an HTML comment containing `/`, `.`, `-`, `:` is not guaranteed to be treated as one exact-match search token).

2. **If a matching open Issue is found** (Route A page): confirm with the user, then close it:

   ```bash
   gh issue close <number>
   ```

   Do not write `review_status` locally in this case. Closing the Issue is what triggers `.github/workflows/review-issue-close-sync.yml` (Issue #313), which flips `review_status` from `pending` to `reviewed` on `main` via its own PR once quality checks pass. If the target page *also* has local uncommitted edits, tell the user to run `/wikicommit-merge` first so the version on `main` reflects those edits, then come back and close the Issue — closing it now would sync `review_status` against the older `main` version, not the local edits.

3. **If no matching open Issue is found** (Route B page — created or edited locally, never routed through `wikicommit-merge` Step 8): fall back to the original local write.

   1. Check the target page's current `review_status` value (available from the frontmatter read in step 1). If the value is neither `pending` nor unset (e.g. already `reviewed`), explicitly confirm with the user whether it's okay to overwrite it (tell them what will be lost — e.g. "review_status is currently `reviewed`. Overwriting it will discard that state. Continue?").
   2. Present the results of steps 1–4 to the user and confirm whether to proceed. Only write `review_status: reviewed` to the target page's frontmatter (locally only, do not commit) if the user approves.

   ```bash
   python .wikicommit/scripts/set_frontmatter_field.py "<page>" --set review_status=reviewed
   ```

   This rewrites (or appends) only the `review_status` line inside the frontmatter block, leaving every other field, the body, and the original line-ending/BOM convention untouched (`set_frontmatter_field.py` uses regex substitution rather than re-serializing with pyyaml, which would change indentation, quoting, and key order). This same script is shared with `.github/workflows/review-issue-close-sync.yml`'s equivalent rewrite for Route A pages (Issue #371 — both previously carried independent copies of this logic, which had already drifted once: the workflow guarded on the current value being exactly `pending` before Issue #370's review surfaced that this Step did not).

   If no frontmatter is found (`FRONTMATTER_RE` does not match), stop and display an error.

### Guidance After Completion

Give the user status- and action-oriented guidance (`docs/DesignDoc-skills.md` §11.8 — never echo the internal `Route A`/`Route B` labels themselves; describe the actual state instead). The conditions below are for you to select between, not text to output — send the user only the sentence(s) that follow the matching condition:

If the target page had a tracking Issue that was just closed:

```
This page had a tracking Issue, and it's now closed.
Next steps:
- Nothing further to do. .github/workflows/review-issue-close-sync.yml will open its own PR
  for this page and auto-merge it once quality checks pass.
```

If the target page had no tracking Issue, so review_status was written locally:

```
No tracking Issue was found for this page, so review_status: reviewed was recorded locally.
Next steps:
- Run /wikicommit-merge to perform quality checks, PR creation, and merge
  (pages with review_status: reviewed are excluded from tracking-Issue generation)
```

## Notes

- Do not commit or create a PR against `main` or any branch (that is `wikicommit-merge`'s responsibility)
- Do not write to `.wikicommit/schema/` (read-only)
- Never overwrite frontmatter without user confirmation (applies to steps 1, 2, 3, and 5 alike)
- Never close a tracking Issue without user confirmation (Step 5)
