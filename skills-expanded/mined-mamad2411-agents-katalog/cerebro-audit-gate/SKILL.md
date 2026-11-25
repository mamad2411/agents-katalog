---
name: cerebro-audit-gate
description: The audit gate for high-blast-radius plans -- the blast-radius definition, the AFTER-approval-BEFORE-execute ordering, the single audit round, and the fix-vs-clarify exception (user corrections are ground truth, not audited). Invoke for high-blast-radius plans (many files / core shared module / public API / schema or migration / auth-security-money / build-CI / multi-plan suite).
---
# Audit high-blast-radius plans before executing them

A plan's BLAST RADIUS is how much of the codebase its change reaches. A
plan is HIGH blast radius when it would touch many files, a core or
shared module that many call sites depend on, a public API / interface /
type that has external or wide internal use, a data model, schema, or
migration, auth / security / money paths, build or CI config, or when it
is a multi-plan suite. A localized, single-file, few-caller change is LOW
blast radius and skips this gate.

For LOW blast-radius plans, follow the normal loop: draft, then propose.

For HIGH blast-radius plans, the audit gate runs AFTER the user approves
the readable plan and BEFORE you execute -- the user reads the plan
first, then a fresh-eyes audit grounds it against the real code:

  1. DRAFT the plan yourself -- ground it in the actual code with the
     read-only bridges -- and record both the technical `<name>.md` and
     its `-readable` companion.
  2. SHOW the readable companion to the user FIRST and let them approve
     it. Do NOT run `cerebro audit` before they have seen and approved
     the plan: the reviewer<->plan back-and-forth is slow and token-heavy,
     and the user can audit a plan they can read. Echo the COMPANION
     path and wait for "go".
  3. ONLY AFTER approval, run `cerebro audit <repo> <plan-path>
     --context "<crucial context>"` ONCE against the technical
     `<name>.md` (never the `-readable` companion). In --context give the
     fresh-eyes child what it cannot know on its own: the key source
     paths involved, decisions the user already made, and constraints
     from the conversation that the spec does not capture. The child
     checks the plan against the real repo -- reach (phantom or missed
     files / symbols / call sites), scope creep, over-engineering,
     misread requirements -- and its findings file ends with
     `PLAN AUDIT: VIABLE` or `PLAN AUDIT: ISSUES FOUND`. READ the
     findings file it echoes, judge each finding (the auditor lacks your
     conversation context, so a "finding" that contradicts something the
     user explicitly asked for is wrong, not the plan), fold in the REAL
     findings by rewriting the plan (`cerebro plan "<full revised plan>"
     --out <same-name>` OVERWRITES; regenerate its companion), then
     execute. Cap at ONE audit round by default; re-audit only when the
     user asks for further plan changes.

When the user is FIXING or CLARIFYING a plan -- a fact, path, detail,
wording, or how the code/system actually works -- rather than asking for
NEW or scope-changing work, apply their correction directly and do NOT
audit it: their word is authoritative ground truth. The audit gate checks
plans drafted from your OWN understanding, not corrections the user handed
you. If the user says skip the audit, skip it.
