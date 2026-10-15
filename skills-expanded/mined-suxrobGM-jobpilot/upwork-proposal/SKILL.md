---
name: upwork-proposal
description: Write a short Upwork proposal from a job description and the user's resume, in a plain human voice that doesn't repeat the user's recent proposals.
argument-hint: "<proposal_id | job_description>"
---

# Upwork Proposal

Clients skim proposals on their phones between other things. If one takes more than about 30 seconds to read, it's gone. Write for that skim: their problem first, one piece of proof, one question.

## Setup

Follow `../_shared/setup.md`, then load the structured resume for `user.primaryResumeId` (`jobpilot-api GET /api/resumes/<id>`) and write from its `content`. Don't `Read` the source PDF.

## Step 1: Resolve the input

The argument is a **proposal id** (from the JobPilot UI) or a raw **job description** (manual use).

- **Id** → fetch the draft and use its `jobDescription` as the posting, with `jobTitle` / `clientName` / `jobUrl` for context. Keep the id for Step 6. Drafts from an Upwork search recommendation (`source:"search"`) work the same way.

  ```bash
  jobpilot-api GET "/api/upwork/proposals/$ARG"
  ```

- **Anything else** → the argument is the job description. There's no row yet; Step 6 creates one.

## Step 2: Read the job and your recent proposals

From the posting, note what the client needs built or fixed, the tech, scope and timeline hints, and any direct questions they ask. Pick one detail unique to this posting to show you read it.

Then read your last five proposals so this one doesn't come out the same:

```bash
jobpilot-api GET /api/upwork/proposals --query page=1 --query limit=5
```

From each `.items[].proposalText`, note the first line, the project it used, and the closing question.

## Step 3: Pick one case study

Choose the single project from the resume that matches their problem, not just their stack. Keep its link if it has one. Prefer a different project from the last two proposals when another one fits just as well.

## Step 4: Write

Under 150 words, in this order:

1. **Hook (line 1, in `**bold**`).** Why you in one line: the closest thing you've done to their problem ("I built the Stripe Connect payouts for a two-sided marketplace last year."). Upwork renders the bold, so this line is what gets read. Don't paraphrase their posting back to them; they know what they wrote. Not "Hi", "Dear client", "I'm excited to apply", or "I came across your posting".
2. **Proof (one or two lines).** The case study: what you built, one real result, and the link. Don't narrate your career.
3. **Question (one line).** One specific question about their project that shows you thought about it (a scope choice, an edge case, a decision they'll face). This is the call to action; don't add "Looking forward to hearing from you" after it. Use a calendar link instead only if the profile has one.

Match their tone: a casual posting gets a casual reply. Don't mention Top Rated or JSS unless the posting asks; the profile already shows it. No lists, headers, or emoji in the body. Don't reuse the first line or closing question of a recent proposal.

**Screening questions.** Answer each one short and direct. "How many years with React?" → "4 years, most recently on [project]." A one-line question gets a one- or two-line answer.

## Step 5: Humanize

Invoke the `humanizer` skill in embedded mode on the proposal, then on the screening answers.

## Step 6: Save

Write the body to `"$JOBPILOT_TEMP/proposal.json"` (proposal text breaks inline quoting). `screeningAnswers` is `[{ "question", "answer" }]`, or `[]` when there were none.

- **Launched with an id** → `PATCH` the draft; its status stays `draft`. Body `{ "proposalText", "screeningAnswers" }`:

  ```bash
  jobpilot-api PATCH "/api/upwork/proposals/$ARG" --data @"$JOBPILOT_TEMP/proposal.json"
  ```

- **Launched with a job description** → `POST` a new row. Body `{ "jobTitle", "clientName", "jobUrl", "jobDescription", "proposalText", "screeningAnswers" }`; `jobTitle` is required (derive it from the posting), and include `clientName` / `jobUrl` when the posting gives them:

  ```bash
  jobpilot-api POST /api/upwork/proposals --data @"$JOBPILOT_TEMP/proposal.json"
  ```

Then print the proposal, and each screening answer under its question, so the user can paste them into Upwork.

## Rules

1. **No fabrication.** Every project, metric, and link comes from the resume.
2. **One case study, one question.** Relevance beats volume.
