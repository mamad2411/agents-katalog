---
name: vapa-proposal
description: Create a new VAPA proposal with AI-assisted drafting, preview, and confirmation before submitting to GitHub Issues.
disable-model-invocation: true
allowed-tools: Bash(git remote get-url origin) Bash(gh issue list *) Read Write AskUserQuestion Bash(${CLAUDE_SKILL_DIR}/scripts/vapa-proposal.sh *)
---

# /vapa-proposal

Create a new VAPA proposal on a GitHub repository. The skill helps you turn a one-line idea into a complete, well-structured proposal, shows a preview, and only creates the Issue after you confirm.

## Modes

- **With a subject**: AI gathers repository context, infers the Issue Type, asks clarifying questions if needed, drafts the full proposal, previews it, and creates the Issue upon confirmation.
- **With a subject and explicit Issue Type**: skip type inference and use the provided type.
- **Without arguments**: list pending proposals (`status: draft`, `status: refining`, `status: ready-for-review`).

## Proposal numbering

Every approved proposal receives a `VEP-XXXX` prefix (4-digit, zero-padded). The shell backend computes the next number from existing issue titles at submission time.

## Usage

```
/vapa-proposal "让VAPA变得可被一键安装，推广VAPA的理念和SKILLS"
/vapa-proposal "调整 Q3 战略重心" "Vision Amendment"
/vapa-proposal
```

## Requirements

- `gh` CLI installed and authenticated with permission to create issues on the target repo.
- Run from inside a git repo, or set `VAPA_REPO=owner/repo`.
- The organization must have the required VAPA issue types and issue fields (`Align`, `Size`, `Shaper`, `Reviewed By`, `Validator`, `Sponsor`).

Org-level fields (`Align`, `Size`, `Shaper`, `Reviewed By`, `Validator`, `Sponsor`) are set manually on the created Issue. The skill may ask for an estimated `Size` during clarification, but it does not write fields automatically.

## Execution

### Step 1: Detect repository

Run:

```bash
git remote get-url origin
```

Parse `owner/repo`. If detection fails, explain that the user should run `/vapa-proposal` from a git repo with a GitHub origin remote, or set `VAPA_REPO=owner/repo`.

### Step 2: Gather context

Read the following files when they exist:

- `${CLAUDE_PROJECT_DIR}/VISION.md`
- `${CLAUDE_PROJECT_DIR}/README.md`

Fetch recent issues for context and duplicate detection:

```bash
gh issue list --repo <owner/repo> --state all --limit 30 --json number,title,labels,body
```

### Step 3: Infer Issue Type

Use the user's subject and the gathered context to choose the most likely VAPA Issue Type:

| Trigger words / context | Type |
|---|---|
| 愿景, VISION, 战略重心, 修正, amend | `Vision Amendment` |
| Describes a pain/observation without a clear solution | `Problem` |
| 实验, 验证, poc, spike, prototype | `Experiment` |
| 重构, 技术债, 性能, cleanup | `Technical Debt` or `Improvement` |
| 调研, 研究, research | `Research` |
| Default | `Feature` |

If confidence is low, present the top two options and ask the user to choose. If the user provided a second argument, use it and skip inference.

### Step 4: Ask clarifying questions

Check required fields per type. If any are missing or vague, ask one focused question at a time. The user may answer, skip, or ask you to draft a placeholder.

| Type | Required fields |
|---|---|
| `Feature` / `Improvement` | target user, problem, core idea, "this is not", acceptance criteria, estimated `Size` |
| `Problem` | affected users, observable evidence, impact if not solved |
| `Vision Amendment` | current VISION.md text, proposed text, rationale, 如果不修改可能产生的误导 |
| `Experiment` | hypothesis, validation method, success metric, scope |
| `Research` | research question, expected output/deliverable, why it matters now, estimated `Size` |

### Step 5: Draft the proposal

Select the bundled template that matches the type:

| Type | Template |
|---|---|
| `Feature`, `Improvement`, `Technical Debt`, `Research` | `${CLAUDE_SKILL_DIR}/references/feature-proposal.md` |
| `Problem` | `${CLAUDE_SKILL_DIR}/references/problem-statement.md` |
| `Vision Amendment` | `${CLAUDE_SKILL_DIR}/references/vision-amendment.md` |
| `Experiment` | `${CLAUDE_SKILL_DIR}/references/experiment.md` |

`Research` reuses `feature-proposal.md`: the "问题陈述" section becomes the research question, "提案内容" becomes the expected output and methodology, and "验收标准" becomes the deliverable criteria.

After reading the template, remove its YAML frontmatter (the block from the first `---` to the closing `---`) before filling sections; the submission backend sets labels and type separately, so the frontmatter must not appear in the issue body.

Read the template, replace the title placeholder with the user's subject, and fill each section using:

- the user's original sentence,
- answers to clarifying questions,
- `VISION.md` for alignment,
- recent issues for related context.

Leave unknown sections as bracketed placeholders like `[待补充：具体受影响的角色]`.

### Step 6: Preview

Show the complete proposal in the terminal:

```markdown
📝 提案预览

类型：<type>
标题：VEP-XXXX <subject>

---

<full body>
```

Compute a best-effort preview number by running `${CLAUDE_SKILL_DIR}/scripts/vapa-proposal.sh --next-number --repo <owner/repo>`. Use the returned value in the preview title. The actual number is recomputed at submission time, so it may differ if another proposal is created in between.

Then ask:

> 请选择：① 提交 ② 编辑某节 ③ 取消

- **① 提交**: proceed to Step 7.
- **② 编辑某节**: ask which section, regenerate only that section, and return to the preview.
- **③ 取消**: stop and confirm that no Issue was created.

### Step 7: Submit

Write the final body to a unique temporary file and invoke the submission backend.

First create a per-proposal temp file (never reuse a fixed path — concurrent or back-to-back proposals would otherwise clobber each other or leak stale content into the new submission):

```bash
BODY_FILE=$(mktemp /tmp/vep-body-XXXXXXXX.md)
```

Write the final body to `$BODY_FILE`, then submit:

```bash
${CLAUDE_SKILL_DIR}/scripts/vapa-proposal.sh \
  --repo <owner/repo> \
  --subject "<user subject>" \
  --body-file "$BODY_FILE" \
  --type "<type>"
```

After the script exits (success or failure), remove the temp file:

```bash
rm -f "$BODY_FILE"
```

On success, report the created issue URL and VEP number.

## Output handling

- On success, report the assigned `VEP-XXXX` number and the created issue URL.
- On cancellation, confirm that no Issue was created.
- On failure, show the script output and explain the likely cause (e.g., missing `gh` auth, no repo detected, invalid issue type, missing org-level issue fields).

## References

The proposal templates are bundled at `${CLAUDE_SKILL_DIR}/references/`:

- `feature-proposal.md`
- `problem-statement.md`
- `vision-amendment.md`
- `experiment.md`
