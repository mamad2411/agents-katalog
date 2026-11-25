---
name: evidence-screenshot
description: >
  Evidence-capture skill for genuine visual proof of authorized security findings.
  Produces chronological, reproducible evidence packages where every screenshot is a
  real capture from an actual tool/browser/terminal session — never fabricated,
  AI-generated, reconstructed, or imitated via rendered HTML/CSS.
---

## Purpose

Given a validated security finding and its testing steps, produce a chronological
evidence package where every important action/result is supported by one or more
**real screenshots captured from the actual target or testing tool**.

This skill is an **evidence-capture workflow**, not a report-design workflow.

## Core Rule (Non-Negotiable)

> IF THE TEST DID NOT ACTUALLY HAPPEN, THERE MUST BE NO SCREENSHOT.

If a required piece of evidence is missing, report "Evidence not captured" rather
than creating an approximation. Never fill evidence gaps with generated
screenshots.

---

## Screenshot Principles

Every screenshot must be:

- captured from the actual target, application, or testing tool
- chronological (matches the real testing sequence)
- reproducible (same steps yield same evidence)
- unedited except for safe cropping if absolutely necessary
- free from fabricated UI, fake browser chrome, fake terminal output,
  AI-generated elements, fake request/response panels, or invented timestamps

**Do not:**
- create a beautiful "finding evidence" graphic combining copied request/response text
- turn raw evidence into a presentation slide
- use generated HTML/CSS to imitate Burp, browser, terminal, Postman, curl,
  or application output
- render proof text into styled HTML pages and screenshot those
- produce "proof" graphics, marketing-style presentations, or synthetic panels

**Do:**
- use whatever real tool was actually used during testing
- capture the actual page/response/terminal state after the relevant action
- keep the original application/tool interface visible in the screenshot

---

## Evidence Granularity

Each testing step produces ONE OR MORE screenshots depending on what is
necessary to prove that step.

Use multiple screenshots when:

- the request and response cannot fit clearly in one view
- the UI action and resulting state are separate
- authentication state needs to be demonstrated
- an identifier changes between steps
- a server response is important
- the vulnerability requires comparison
- the impact appears later in the workflow

Avoid unnecessary screenshots when one genuine screenshot completely
proves the step.

Naming convention per screenshot:

```
F02-S01-A    (Finding 02, Step 01, screenshot A)
F02-S01-B    (Finding 02, Step 01, screenshot B — same step, second capture)
F02-S02-A
F02-S03-A
```

---

## What Each Screenshot Should Prove

For every screenshot determine:

1. What action is being performed?
2. What exact evidence is visible?
3. Why does this evidence matter?
4. Which finding step does it support?

The screenshot itself is evidence — do not put large decorative titles
over it. The original application/tool interface should remain visible.

---

## Real Capture Methods (Preferred)

Use whatever real tool was actually used during testing:

- **Playwright / Puppeteer screenshots** — `page.screenshot()` during browser automation
- **Chrome DevTools screenshots** — `--headless --screenshot=...` on live page
- **Browser screenshots** — manual screenshot of actual browser session
- **Terminal screenshots** — actual terminal output during testing
- **Burp Suite screenshots** — actual Burp Repeater/Proxy/Intruder panes
- **HTTP client screenshots** — actual Postman / Insomnia / curl output in terminal
- **curl output captured from the real terminal** — raw terminal output as-is
- **application UI screenshots** — actual application state during testing

If browser automation is used, capture the actual page after the relevant action.
If HTTP requests are used, capture the actual request/response using the actual
testing tool. If terminal commands are used, capture the actual terminal output.

**Never manufacture evidence after the fact.**

---

## Screenshot Naming Convention

Deterministic filenames only:

```
F02-S01-A.png
F02-S01-B.png
F02-S02-A.png
F02-S03-A.png
```

Never use names like: `final-proof.png`, `awesome-result.png`,
`vulnerability.png`, `ai-generated-proof.png`.

---

## Evidence Directory Structure

```
evidence/
  F01/
    screenshots/
      F01-S01-A.png
      F01-S01-B.png
      F01-S02-A.png
      F01-S03-A.png
    evidence.md
    manifest.json
  F02/
    screenshots/
      F02-S01-A.png
      F02-S02-A.png
      F02-S03-A.png
    evidence.md
    manifest.json
```

---

## Evidence Explanation (Separate from Raw Evidence)

RAW EVIDENCE = the actual screenshot.

EVIDENCE EXPLANATION = a short text file explaining what the screenshot
demonstrates. Store in `evidence.md`.

Each entry in `evidence.md` follows this structure:

```
### Evidence ID: F02-S03-A

**Step:** Submit application

**Screenshot:** F02-S03-A.png

**Description:**
Actual application response after submission.

**What it proves:**
The server accepted the application containing the self-declared income
value of 1.

**Expected security control:**
The server should independently verify or enforce the means-test requirement
before accepting eligibility-related data.

**Observed behavior:**
The submitted record retains the attacker-controlled income value.
```

Do not write fake values into the explanation that are not visible in or
otherwise supported by the actual test evidence.

---

## Manifest

Each finding's `manifest.json` contains:

```json
{
  "finding_id": "F-02",
  "title": "Self-Declared Income Bypasses Means Test",
  "target": "13.222.104.89",
  "captured_at": "2026-09-10T11:30:00Z",
  "steps": [
    {
      "step": 1,
      "description": "Create application with annual_income=1",
      "screenshots": ["F02-S01-A.png"]
    },
    {
      "step": 2,
      "description": "Complete required workflow steps",
      "screenshots": ["F02-S02-A.png"]
    },
    {
      "step": 3,
      "description": "Submit application",
      "screenshots": ["F02-S03-A.png", "F02-S03-B.png"]
    }
  ]
}
```

Only include information actually known from the assessment. Never invent
timestamps, identifiers, requests, responses, users, or results.

---

## Sensitive Data Handling

Screenshots may contain:

- JWTs, session cookies, usernames, email addresses
- personal information, internal identifiers

Rules:

- Do not expose secrets unnecessarily.
- If a secret is irrelevant to the finding, redact it in the final evidence copy.
- Never replace secrets with fake text like `<JWT>`, `<REDACTED_TOKEN>`,
  or `example-token` unless the redaction is clearly visually distinguishable
  from actual application output.
- Maintain an original evidence copy when appropriate; create a redacted copy
  for reporting.
- Never alter evidence in a way that changes its meaning.

---

## Quality Checklist (Run Before Finalizing)

For every screenshot check:

- [ ] Is this a real screenshot from an actual tool/session?
- [ ] Does it correspond to an actual testing action?
- [ ] Is the relevant evidence readable?
- [ ] Is the target/application visible where useful?
- [ ] Is the screenshot chronological?
- [ ] Does the screenshot support the claimed step?
- [ ] Is there any fabricated text or recreated output?
- [ ] Is any output manually recreated rather than captured?
- [ ] Is sensitive information unnecessarily exposed?
- [ ] Can the evidence be independently understood?

**Reject any evidence that appears fabricated or reconstructed.**

---

## Failure Handling

If a required piece of evidence is missing:

- Report: "Evidence not captured"
- Explain why (e.g., application state changed, access revoked, tool not available)
- Document what was observed during testing, without fabricating proof

If the application state cannot be reproduced:

- Document that limitation
- Note the timestamp when the state was observed
- Note whether the state was transient

---

## Workflow

Given:

- target
- finding ID and title
- vulnerability type
- testing steps (with expected and observed behavior)
- available tool session (browser, HTTP client, terminal)

Then:

1. Parse the finding and break it into atomic evidence steps.
2. Identify what each step needs to prove.
3. Execute or guide the authorized test (live, not retrospectively).
4. Capture real screenshots **during** the test.
5. Assign deterministic evidence IDs.
6. Store screenshots chronologically in the evidence directory.
7. Generate `evidence.md` (explanation) and `manifest.json` (metadata).
8. Validate every screenshot against the quality checklist.
9. Produce a concise evidence index.

---

## Anti-Fabrication Rules (Zero Tolerance)

The following are **never acceptable** as evidence:

- HTML/CSS rendered to imitate terminal, browser, or application output
- AI-generated screenshots or UI mockups
- Manually recreated request/response text placed in image format
- Fake browser windows, fake terminal windows, fake Burp panes
- Screenshots from a different target or a different session
- Post-hoc reconstructions of what the evidence "would have looked like"
- Decorative graphics, neon dashboards, fake report cards
- Excessive arrows, highlighting, annotation overlays covering the evidence
- Synthetic request/response panels

The goal is **credibility and reproducibility**, not visual spectacle.

---

## Output

Final output per finding:

```
evidence/
  F01/
    screenshots/
      F01-S01-A.png
      F01-S01-B.png
      F01-S02-A.png
      F01-S03-A.png
    evidence.md
    manifest.json
```

The `evidence.md` should contain:

- Finding title
- Evidence index table
- Reproduction sequence (facts only, established during testing)
- Evidence limitations (anything that could not be captured)

---

## Integration with Assessment Workflow

This skill is called **after** a finding is validated (passes the 7-question
gate from `triage-validation`). It is called **before** the finding is written
into the final report.

Workflow order:

1. Reconnaissance
2. Hunting
3. Triage and validation
4. **Evidence capture (this skill)**
5. Report writing
6. Remediation plan

When this skill completes, the finding folder contains both the raw evidence
and the explanation — ready for the report-writer to reference.
