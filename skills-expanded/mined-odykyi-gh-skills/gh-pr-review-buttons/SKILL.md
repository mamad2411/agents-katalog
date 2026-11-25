---
name: gh-pr-review-buttons
description: Add "Review this PR in" Grok, Claude and Codex buttons to a GitHub repository's pull request descriptions. Use when someone asks how the review buttons work, wants them in their own repo, or wants to explain how to review a PR with AI.
license: MIT
compatibility: Requires a GitHub repository with GitHub Actions and Node.js 20+. Does not deploy and calls no AI API.
metadata:
  author: tdk-landscape
  version: "1.0"
  source: https://github.com/tdk-landscape/tdk-skills/tree/main/skills/tdk-pr-review-buttons
---

# PR review buttons (Grok, Claude, Codex)

The buttons are plain Markdown links appended to the end of a PR description. Clicking one opens that AI's website with a prompt already typed in. Nothing runs in CI and no API key is needed. The whole feature is one Node script, one GitHub Actions workflow, and a marker string.

Reference implementation: `tdk-cli-core` — `scripts/ai-review-buttons.mjs`, `.github/workflows/ai-review-buttons.yml`, `docs/contributing/04-review-a-pr.md`.

## Screenshot

![Review this PR in buttons on a PR description](https://raw.githubusercontent.com/odykyi/gh-skills/main/skills/gh-pr-review-buttons/images/review-buttons.png)

## Install in a repository (do this when asked)

Installing means changing the target repo: creating two files, committing them, and opening a PR with the review buttons workflow included. Do not merge the PR unless the user asks. Work in the target repo, on a new branch, never on its default branch.

1. Confirm the target is a GitHub repo with `gh auth status` OK and a clean working tree (`git status --short` is empty). Stop and report if not.
2. Create the branch: `git checkout -b add-ai-review-buttons`.
3. Create `scripts/ai-review-buttons.mjs` from Step 1 below and `.github/workflows/ai-review-buttons.yml` from Step 2 below. The Codex SVG path is already filled in; do not change it.
4. Test the transform: run the Step 3 command twice and confirm the second run prints `skip`.
5. Commit: `git add scripts/ai-review-buttons.mjs .github/workflows/ai-review-buttons.yml && git commit -m "Add AI review buttons to PR descriptions"`.
6. Push and open the PR: `git push -u origin add-ai-review-buttons`, then `gh pr create --base <default-branch> --title "Add AI review buttons to PR descriptions" --body "Adds Grok, Claude and Codex review buttons to PR descriptions. See the gh-pr-review-buttons skill."` Use the repo's default branch for `--base`.
7. Tell the user the PR URL.
8. Buttons do not appear until the workflow is on the default branch. A PR that only adds the workflow gets no buttons, and a merged PR is never re-triggered. So after this PR is merged, run the backfill once: **Actions → AI review buttons → Run workflow**. Open PRs get buttons. Test on a PR opened after the merge, or on a PR that is open at merge time.
9. Do not test on a PR that already added the workflow and was merged. Open a new test PR after the workflow is on the default branch.

### Workflow file (`.github/workflows/ai-review-buttons.yml`)

```yaml
name: 🤖 AI review buttons

on:
  pull_request_target: # never checks out or runs PR code; only writes the PR body
    types: [opened, reopened, edited]
  workflow_dispatch:

permissions: {}

concurrency:
  group: ai-review-buttons-${{ github.event.pull_request.number || 'backfill' }}
  cancel-in-progress: false

jobs:
  append:
    name: Append AI review buttons
    if: github.event_name == 'pull_request_target'
    runs-on: ubuntu-latest
    timeout-minutes: 2
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.repository.default_branch }}
          persist-credentials: false
      - name: Append AI review buttons
        env:
          GH_TOKEN: ${{ github.token }}
          PR_NUMBER: ${{ github.event.pull_request.number }}
          PR_URL: ${{ github.event.pull_request.html_url }}
          OUT_FILE: ${{ runner.temp }}/pr-body-new.md
          PATCH_FILE: ${{ runner.temp }}/pr-body-patch.json
        run: |
          set -euo pipefail
          gh api "repos/${GITHUB_REPOSITORY}/pulls/${PR_NUMBER}" --jq '(.body // "") | @base64' > "${OUT_FILE}.b64"
          base64 -d < "${OUT_FILE}.b64" > "${OUT_FILE}.in"
          export BODY_FILE="${OUT_FILE}.in"
          node scripts/ai-review-buttons.mjs
          if cmp -s "${OUT_FILE}.in" "$OUT_FILE"; then
            echo "Body unchanged; nothing to PATCH."
            exit 0
          fi
          # Lost-update guard: skip if the author changed the body since the snapshot.
          gh api "repos/${GITHUB_REPOSITORY}/pulls/${PR_NUMBER}" --jq '(.body // "") | @base64' > "${OUT_FILE}.now.b64"
          base64 -d < "${OUT_FILE}.now.b64" > "${OUT_FILE}.now"
          if ! cmp -s "${OUT_FILE}.in" "${OUT_FILE}.now"; then
            echo "Body changed since snapshot; skipping PATCH to avoid a lost update."
            exit 0
          fi
          jq -n --rawfile body "$OUT_FILE" '{body: $body}' > "$PATCH_FILE"
          gh api --method PATCH "repos/${GITHUB_REPOSITORY}/pulls/${PR_NUMBER}" --input - < "$PATCH_FILE" > /dev/null

  backfill:
    name: Backfill open PRs
    if: github.event_name == 'workflow_dispatch'
    runs-on: ubuntu-latest
    timeout-minutes: 15
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.repository.default_branch }}
          persist-credentials: false
      - name: Backfill open PRs
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          set -euo pipefail
          gh pr list --repo "${GITHUB_REPOSITORY}" --state open --limit 100 \
            --json number,title,url --jq '.[] | [.number, .title, .url] | @tsv' |
          while IFS=$'\t' read -r number title url; do
            export PR_NUMBER="$number" PR_URL="$url"
            export BODY_FILE="${RUNNER_TEMP}/in-${number}.md"
            export OUT_FILE="${RUNNER_TEMP}/out-${number}.md"
            export PATCH_FILE="${RUNNER_TEMP}/patch-${number}.json"
            gh api "repos/${GITHUB_REPOSITORY}/pulls/${number}" --jq '(.body // "") | @base64' > "${BODY_FILE}.b64"
            base64 -d < "${BODY_FILE}.b64" > "$BODY_FILE"
            node scripts/ai-review-buttons.mjs
            if cmp -s "$BODY_FILE" "$OUT_FILE"; then
              continue
            fi
            gh api "repos/${GITHUB_REPOSITORY}/pulls/${number}" --jq '(.body // "") | @base64' > "${BODY_FILE}.now.b64"
            base64 -d < "${BODY_FILE}.now.b64" > "${BODY_FILE}.now"
            if ! cmp -s "$BODY_FILE" "${BODY_FILE}.now"; then
              echo "PR #${number} body changed since snapshot; skipping."
              continue
            fi
            jq -n --rawfile body "$OUT_FILE" '{body: $body}' > "$PATCH_FILE"
            gh api --method PATCH "repos/${GITHUB_REPOSITORY}/pulls/${number}" --input - < "$PATCH_FILE" > /dev/null
            echo "Patched PR #${number}"
          done
```

Pin `actions/checkout` to a full commit SHA in your repo if its policy requires it.

## What the reader sees

```
---

# Review this PR in
[Grok badge](https://grok.com/?q=...)&nbsp;[Claude badge](https://claude.ai/new?q=...)&nbsp;[Codex badge](https://chatgpt.com/?q=...)
```

The prompt in every link is the same single sentence:

```
Review this pull request. Read the title and diff at https://github.com/<owner>/<repo>/pull/<n>.
```

## Why it is built this way

- **Shields.io badges, not raw buttons.** GitHub strips buttons and custom CSS from PR bodies. A linked image is the only reliable "button".
- **`&nbsp;` between badges, no blank line inside the section.** A blank line makes GitHub render each badge as its own block, so they stack vertically. Keep them on one line.
- **Heading outside the badges.** Put `# Review this PR in` on its own line, then the badges on the next line. Otherwise the badges can drop below the heading.
- **Marker comment `<!-- ai-review-buttons -->`.** The script finds the section by this marker and rewrites only that tail. Keep the legacy `<!-- grok-review-button -->` marker in the list so old PRs are migrated, not duplicated.
- **Author text is never touched.** The section is appended after the author's bytes. The script never trims, reformats or re-wraps the author's text.
- **The Codex logo is an inline SVG data URI.** Shields no longer ships a Codex logo slug. The SVG fill must be `#fff`, because `logoColor` does not recolor data URIs.
- **Runs on the default branch only.** The workflow uses `pull_request_target` so forks get buttons too. It never checks out the PR head and never runs PR code. The only write is the PR body.

## Step 1: add the script

Create `scripts/ai-review-buttons.mjs`. It must be a pure transform with no network calls: read the body, compute the new body, write it out. The core logic:

```js
#!/usr/bin/env node
import { readFileSync, writeFileSync } from "node:fs";

export const MARKER = "<!-- ai-review-buttons -->";
export const LEGACY_MARKER = "<!-- grok-review-button -->";
export const MARKERS = [MARKER, LEGACY_MARKER];

export function buildPrompt(prUrl) {
  return `Review this pull request. Read the title and diff at ${prUrl}.`;
}

export function buildButtonsHtml(prUrl) {
  const q = encodeURIComponent(buildPrompt(prUrl));
  const badge = (name, color, logo) =>
    `https://img.shields.io/badge/${encodeURIComponent(name)}-${color}?style=for-the-badge&logo=${logo}&logoColor=white`;
  const codexLogo = encodeURIComponent(
    "data:image/svg+xml;base64," +
      Buffer.from(
        `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="#fff" d="M22.28 9.82a6 6 0 0 0-.52-4.91 6.05 6.05 0 0 0-6.51-2.9A6.07 6.07 0 0 0 4.98 4.18a6 6 0 0 0-4 2.9 6.05 6.05 0 0 0 .74 7.1 6 6 0 0 0 .51 4.91 6.05 6.05 0 0 0 6.52 2.9A6 6 0 0 0 13.26 24a6.06 6.06 0 0 0 5.77-4.21 6 6 0 0 0 4-2.9 6.06 6.06 0 0 0-.75-7.07z"/></svg>`,
      ).toString("base64"),
  );
  return [
    `[![Grok](${badge("Grok", "111111", "x")})](https://grok.com/?q=${q})`,
    `[![Claude](${badge("Claude", "D97757", "anthropic")})](https://claude.ai/new?q=${q})`,
    `[![Codex](${badge("Codex", "10A37F", codexLogo)})](https://chatgpt.com/?q=${q})`,
  ].join("&nbsp;");
}

export function buildGeneratedSection(prUrl) {
  return [MARKER, "", "---", "", "# Review this PR in", buildButtonsHtml(prUrl), "", "<sub>Shared by [@tdk-landscape](https://github.com/tdk-landscape) · [tdk-cli-core](https://github.com/tdk-landscape/tdk-cli-core) · If this helps, please ⭐ [star tdk-cli-core](https://github.com/tdk-landscape/tdk-cli-core)</sub>", ""].join("\n");
}

export function joinAuthorAndSection(authorBody, section) {
  if (authorBody === "") return section;
  if (authorBody.endsWith("\n\n")) return `${authorBody}${section}`;
  if (authorBody.endsWith("\n")) return `${authorBody}\n${section}`;
  return `${authorBody}\n\n${section}`;
}

function markerIndex(body) {
  let idx = -1;
  for (const m of MARKERS) {
    const i = body.indexOf(m);
    if (i !== -1 && (idx === -1 || i < idx)) idx = i;
  }
  return idx;
}

export function transformBody(body, prUrl) {
  const url = (prUrl ?? "").trim();
  if (!url) return { action: "skip", body, reason: "missing pr url" };

  const section = buildGeneratedSection(url);
  const idx = markerIndex(body);
  if (idx === -1) {
    return { action: "patch", body: joinAuthorAndSection(body, section), reason: "append review buttons" };
  }
  const authorPart = body.slice(0, idx);
  const existing = body.slice(idx).replace(/\s+$/, "");
  if (existing === section.replace(/\s+$/, "")) {
    return { action: "skip", body, reason: "marker present and prompt matches" };
  }
  return {
    action: "patch",
    body: joinAuthorAndSection(authorPart, section),
    reason: "regenerate review buttons for current url",
  };
}

const bodyFile = process.env.BODY_FILE;
const outFile = process.env.OUT_FILE;
if (bodyFile && outFile) {
  const result = transformBody(readFileSync(bodyFile, "utf8"), process.env.PR_URL ?? "");
  writeFileSync(outFile, result.body, "utf8");
  console.log(`${result.action}: ${result.reason}`);
}
```

Replace `M22.28 9.82a6 6 0 0 0-.52-4.91 6.05 6.05 0 0 0-6.51-2.9A6.07 6.07 0 0 0 4.98 4.18a6 6 0 0 0-4 2.9 6.05 6.05 0 0 0 .74 7.1 6 6 0 0 0 .51 4.91 6.05 6.05 0 0 0 6.52 2.9A6 6 0 0 0 13.26 24a6.06 6.06 0 0 0 5.77-4.21 6 6 0 0 0 4-2.9 6.06 6.06 0 0 0-.75-7.07z` with the path data from the OpenAI mark (copy it from `tdk-cli-core/scripts/ai-review-buttons.mjs`, do not retype it). Use the exact badge colours above so the buttons match the reference.

## Step 2: add the workflow

Create `.github/workflows/ai-review-buttons.yml`. Keep these properties, which are the reason it is safe:

- Triggers: `pull_request_target` with types `[opened, reopened, edited]`, plus `workflow_dispatch` for backfill. No `synchronize`.
- `permissions: {}` at the top level. Each job grants only `contents: read` and `pull-requests: write`.
- `concurrency` per PR number, `cancel-in-progress: false`, so two quick edits cannot PATCH in parallel.
- Checkout with `ref: ${{ github.event.repository.default_branch }}` and `persist-credentials: false`.
- Pass PR fields through `env:`, never interpolate `${{ github.event.pull_request.title }}` into a `run:` string.
- Read the body with `gh api`, run the script, then **re-read the body before PATCH**. If the author changed it since the snapshot, skip. This prevents a lost update.
- Patch with `jq -n --rawfile body ... | gh api --method PATCH ... --input -`.
- A `backfill` job loops over `gh pr list --state open --limit 100` and runs the same steps per PR. Use `timeout-minutes: 15` for backfill and `2` for the event job.

Pin third-party actions to a full commit SHA. `actions/checkout` is the only one needed.

## Step 3: backfill and test

1. Merging the workflow does not re-run it on already-open PRs. Run **Actions → AI review buttons → Run workflow** once after merge.
2. Test the transform locally with no network:

```bash
BODY_FILE=/tmp/body.md OUT_FILE=/tmp/out.md PR_URL=https://github.com/owner/repo/pull/1 node scripts/ai-review-buttons.mjs
```

Any temp path works in place of `/tmp`. Run the script twice on the same input: the second run must print `skip`. Add a unit test for these cases: empty body, body with no marker, body with the marker and a matching URL (skip), body with the marker and a changed URL (regenerate), and body with only the legacy marker (migrated).

3. Open a test PR, check the description renders three badges on one row under the heading, then click each one and confirm the prompt is pre-filled.

## Pitfalls

- **Badges stack vertically.** A blank line was added inside the section, or `&nbsp;` was dropped.
- **Codex badge is blank or broken.** The SVG was not base64-encoded inside the data URI, or its fill is not `#fff`.
- **Duplicate sections.** The marker was changed. Keep `MARKER` and `LEGACY_MARKER` stable; they are how the script finds its own section.
- **Author edits vanish.** Someone reordered the logic to trim or rewrite the body. Always append after the author's bytes.
- **Workflow runs PR code.** Never add a checkout of `github.event.pull_request.head`. This is the reason the trigger is safe.
- **Star or attribution line missing on a PR.** The PR was opened before the new script reached `main`, or it was merged before the change. Merged PRs are never rewritten. Open a new PR after the script is on the default branch.
- **Buttons do not appear on forks.** Only happens if the trigger was changed from `pull_request_target` to `pull_request`. Keep `pull_request_target`.

## Telling people how to review with the buttons

Point readers to the PR review guide in the repo (`docs/contributing/04-review-a-pr.md` in tdk-cli-core). The rule for every reviewer: click a button for a first pass, check each AI point against the diff, then write your own review and say what you did not check. The AI chat is private to the reviewer and does not post to GitHub.
