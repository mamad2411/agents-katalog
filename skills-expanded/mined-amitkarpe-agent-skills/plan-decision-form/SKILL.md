---
name: plan-decision-form
description: "Create a self-contained offline Decision Studio HTML form with explicit owner confirmations and portable JSON import/export. Use for reviewing multiple decisions, skill-exposure preferences, roadmap choices, tradeoffs, or when asked for Decision Studio, a decision form, or a portable HTML notebook. Use a short text question instead of a form for a trivial decision."
---

# Decision Studio (portable)

Use **Decision Studio** as the human-facing name. Keep this existing skill ID
`plan-decision-form` and path for installed references; do not create a second
skill or depend on a running web server.

Decision Studio reviews and records choices. An interactive "grill me" interview
clarifies uncertain requirements **before** building the Studio, when useful;
it is not a replacement for confirmation, comparison, or JSON export.

## Workflow

1. Read the exact owning Issue/PR and current evidence. Propose defaults with
   brief tradeoffs. For one trivial decision, use normal text. When requested
   explicitly, create an HTML form without seeking another UI approval.
2. Prepare a **sanitized JSON specification** with 1–30 stable decisions.
   Every decision needs `id`, `title`, `choices`, `recommended`, and
   `rationale`. Defaults are `proposed`, never silently owner-accepted.
3. Render one offline file using the existing stdlib renderer:

   ```bash
   python3 scripts/render_portable.py --spec decisions.json --out decision-studio.html
   ```

4. Give the owner the portable `decision-studio.html` file. Open it locally in
   a browser (**file://**, no localhost or service). The page supports
   search, dark/light themes, recommended choice, explicit confirmation,
   local resume when browser storage permits, **Import JSON**, and
   **Export JSON**. Import/export never contacts a service.
5. On return, validate the exported packet against the original spec:

   ```bash
   python3 scripts/render_portable.py --spec decisions.json --check-packet decision-packet.json
   ```

6. Summarize **accepted** versus **proposed/unresolved**. Recheck the owning
   SPEC, approvals and safety gates before any implementation. A decision packet
   records preferences; it never grants GitHub merge, AWS, PROD, IAM, secrets,
   cost, or deployment authority.

## Example spec

```json
{
  "schema_version": "decision-packet/1",
  "source": "https://github.com/amitkarpe/work/issues/179",
  "title": "Daily skill exposure",
  "confirmation_mode": "proposal_first",
  "decisions": [
    {
      "id": "skill-profile",
      "title": "Which daily skill profile?",
      "choices": ["default", "no-aws"],
      "recommended": "default",
      "rationale": "Default is AWS-first; no-aws enables only core skills."
    }
  ]
}
```

The output packet preserves IDs, choices, recommended/selected values, per-item
`state` and `frozen`, source, confirmation mode, and export time. The page
never treats suggested defaults as accepted until the owner checks confirmation.
Only the previous, separately opted-in Portfolio Sprint Studio used
`owner_opt_in_default_agreed`; **this general-purpose skill deliberately
starts with `proposal_first`**.

Use text-only source facts, not credentials, tokens, internal screenshots,
private host details, or sensitive inventories. HTML and exported JSON can be
forwarded or opened outside the original machine; assess confidentiality first.

## Legacy compatibility (explicit only)

The older server-bound `scripts/plan_decision_form.py` remains in the same
skill for existing Agent Web/Agent Share consumers. It is **not** the default
and should not be invoked for portable forms. Do not start or install
`/opt/agent-web`, publish forms, or migrate old saved decisions automatically.
