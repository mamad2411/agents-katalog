---
name: submit-706-project
description: Guide a 706 Human & Vicinity hackathon team through a five-round interview, preview and revise its public project page, then submit it as a pull request to the fixed 706 Beijing CoWiki Space. Use when a participant wants to submit, revise, preview, or publish a 706 hackathon project.
---

# Submit a 706 Project

Collect a project's public facts conversationally, render one deterministic
Markdown page, and submit it through the installed `cowiki-space` skill. Do not
invent facts, expose private information, or bypass the confirmation gates.

## Fixed target

- Cloud origin: `https://api.cowiki.app`
- Space ID: `fd04236e-b49c-4525-aa5e-1492e9c0466a`
- Space name: `706 Beijing`
- Public Space: `https://cowiki.app/spaces/706-beijing`
- Review page: `https://cowiki.app/cloud/spaces/fd04236e-b49c-4525-aa5e-1492e9c0466a/reviews`
- Project directory: `submissions/`

Never substitute another Space unless the user explicitly stops this workflow
and asks for a different task.

## Prepare the shared Space

1. Locate the installed `cowiki-space/SKILL.md` and read it completely. Resolve
   its `scripts/cowiki.mjs` path relative to that file.
2. If the full `cowiki-space` bundle is unavailable, explain that it provides
   secure login, clone, and pull-request submission. Ask permission before
   installing it:

   ```text
   npx skills add https://github.com/wfnuser/cowiki --skill cowiki-space -g -y
   ```

   Then read the installed copy before continuing.
3. Before the first Cloud-changing command in this Agent session, follow the
   `cowiki-space` update-check rule. Never update a skill without permission.
4. A participant needs an organizer-provided **Editor invitation**. Never embed,
   request for publication, or store an invitation token in the project page.
   If membership is missing, ask the participant to open the organizer's invite
   link, accept it, and return here.
5. If authentication is missing, run:

   ```text
   node <cowiki-skill-dir>/scripts/cowiki.mjs login --server https://api.cowiki.app
   ```

6. Ask the participant to choose an empty local directory. Clone the fixed Space:

   ```text
   node <cowiki-skill-dir>/scripts/cowiki.mjs clone --server https://api.cowiki.app --space fd04236e-b49c-4525-aa5e-1492e9c0466a --directory <chosen-path>
   ```

   Reuse an existing linked clone only after the user identifies it and
   `cowiki-space status` confirms it is this Space.
7. Run `cowiki-space status` before the interview. Stop on conflicts or unrelated
   local changes; do not discard, overwrite, commit, rebase, or force them.

Keep the interview draft as JSON outside the cloned Space. Use a temporary file
with restrictive local permissions when practical. Never place private notes or
the draft JSON in the Space.

## Conduct five rounds

Tell the participant there will be five short rounds. Ask one round at a time,
summarize the captured answer, and let them correct it before moving on. Natural
conversation is preferred over presenting a long form.

### Round 1 — Project identity

Ask for:

- Project name — required.
- Team or display name — required.
- One-sentence description — required.
- Current stage — optional.
- One or more “附近” themes — optional. Examples: body, perception, encounter,
  labor, stories, objects, nature, time; accept the participant's own wording.

### Round 2 — Participants

Collect at least one participant. For each person ask for a public display name
and role or contribution. A GitHub handle is optional.

Before collecting, say not to provide phone numbers, email addresses, WeChat,
home or shipping addresses, passwords, tokens, or other private contact details.
If the user supplies one, do not put it in the draft; ask for a public-safe
replacement.

### Round 3 — Observation and build

First ask for:

- The local phenomenon or problem actually observed.
- Who it affects.
- A concrete place, moment, or situation where it occurs.
- Real observation, interview, participation, or fieldwork completed so far.

It is acceptable to state that fieldwork has not happened. Never invent people,
quotes, counts, research, outcomes, or evidence.

Then ask for:

- What the team built.
- At least one core feature or component; two to five is a useful target.
- How a visitor or user experiences it.
- Optional technical, design, or creative highlights.
- Current completion state.
- Optional known limitations.

### Round 4 — Booth experience and links

Ask how someone should experience the project at the event: ordered steps,
expected result, optional prerequisites, and optional现场限制. Aim for an
experience that can be understood in three to five minutes, but preserve the
team's real plan.

Then offer these links. **Every link is optional**, including the source-code
repository:

- Source-code repository.
- Website, app, download, or online experience.
- Demo video.
- Other named links.

Accept only `http://` or `https://` URLs. A demo video must be a URL; never copy,
upload, or commit a local video or any other binary file.

### Round 5 — Preview, revise, and confirm

Create the draft JSON described below and preview it with the bundled renderer:

```text
node <this-skill-dir>/scripts/render-submission.mjs --input <draft.json> --preview
```

Show the exact `submissions/<team>--<project>.md` path and the complete rendered
Markdown. Invite changes to any answer, member, section, link, team name, or
project name. Apply requested edits to the JSON and re-run preview. Repeat until
the participant is satisfied.

Do not write or submit merely because the participant says the preview looks
interesting or asks a question. Ask for an explicit final confirmation. The
exact reply `确认提交` is sufficient; accept only equally unambiguous wording.
Cancellation or uncertainty creates no file and no pull request.

## Draft JSON

Use exactly this public schema. Omit absent optional values or use the empty
array/object form accepted by the renderer. Do not add contact or internal-note
fields.

```json
{
  "projectName": "项目名",
  "teamName": "团队名",
  "oneLiner": "一句话介绍",
  "stage": "可选阶段",
  "themes": ["可选主题"],
  "members": [
    { "name": "公开姓名", "role": "角色或贡献", "github": "可选用户名" }
  ],
  "problem": {
    "observation": "观察到的现象",
    "audience": "影响的人",
    "scenario": "具体场景",
    "fieldwork": "真实调研、观察或尚未开展的说明"
  },
  "build": {
    "summary": "做了什么",
    "features": ["核心功能"],
    "experience": "如何体验",
    "highlights": ["可选亮点"],
    "status": "当前状态",
    "limitations": "可选限制"
  },
  "booth": {
    "steps": ["现场体验步骤"],
    "expectedResult": "预期结果",
    "requirements": "可选条件",
    "limitations": "可选现场限制"
  },
  "links": {
    "repository": "可选 HTTPS URL",
    "product": "可选 HTTPS URL",
    "video": "可选 HTTPS URL",
    "other": [{ "label": "名称", "url": "HTTPS URL" }]
  }
}
```

The renderer requires Node.js 20 or newer. Treat its validation errors as
requests to correct the interview data; do not bypass its validation.

## Write and submit

After explicit confirmation:

1. If the target page does not exist, write exactly one page:

   ```text
   node <this-skill-dir>/scripts/render-submission.mjs --input <draft.json> --cwd <space-path> --write
   ```

2. If the renderer says the page exists, stop. Show the existing file and a new
   preview. Explain that the update will replace that project page, then obtain a
   **second explicit update confirmation**. Only then run the same command with
   `--update`.
3. Run:

   ```text
   node <cowiki-skill-dir>/scripts/cowiki.mjs status --cwd <space-path>
   ```

   Verify that the only dirty path is the intended Markdown page. Stop if any
   unrelated file is dirty.
4. Submit through `cowiki-space`; do not reproduce its Git or API operations:

   ```text
   node <cowiki-skill-dir>/scripts/cowiki.mjs submit --cwd <space-path> --message "Submit <team> — <project>"
   ```

5. Report the command's pull-request result and the review page. Explain that an
   Editor can submit but cannot approve or merge; an Owner or Manager performs
   review and merge.
6. Construct the public document URL by percent-encoding every path segment:

   ```text
   https://cowiki.app/spaces/706-beijing/<encoded-submission-path>
   ```

   Label it “available after an administrator merges the pull request.” Do not
   claim the page is public before merge.

## Failure handling

- Missing membership: request the organizer's Editor invite; never expose a
  reusable token from this public skill.
- Login, clone, or status failure: report the exact safe error and stop.
- Invalid URL or missing required fact: keep the draft and ask for correction or
  removal; optional links may simply be removed.
- Existing page: require the second update confirmation.
- Conflict or unrelated dirty files: stop and report paths. Never force, abort,
  or choose a side without the participant.
- Submit failure: keep the local Markdown and draft, give a recovery summary,
  and do not claim a pull request exists.

Never read or print a CoWiki credential, implement raw Git push/rebase, call the
Cloud API directly, or approve/merge on behalf of an Editor.
