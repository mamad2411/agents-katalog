---
name: dx-companion
description: "Work with Homeric DX, the developer-experience companion: when to check the person's DX status and consent, offer to log friction (with a category and the minutes lost), share a numbers-only session summary they confirm, and record their monthly time split, following its privacy rules. Use whenever the Homeric DX tools (dx_*) are available."
license: "Proprietary: Homeric Skills License v1.0"
metadata:
  version: "0.2.0"
---

<!--
Licensed: Homeric Skills License v1.0 — V1 (Free Skill).
This skill content is proprietary to Homeric. Distribution prohibited.
-->

# Homeric DX companion

> **What this skill is.** How a coding agent works with Homeric DX (`/dx`): the engineer's loop, when to call each DX tool, how to log friction well, and the privacy rules. On the server it is read through `homeric_get_anchor` and `resources/read`; the client packages (the Claude, Cursor and Codex plugins) ship it as their skill.

> **Resource-only.** No tool of its own: the tools are `dx_status_get`, `dx_friction_log`, `dx_signals_submit`, `dx_pulse_get` and `dx_time_declare`, and their own words are in `dx-base`.

---

<!-- @anchor: dx-companion.loop -->
## The loop

Homeric DX helps an engineer see and remove what slows them down, and gives their team the group numbers to fix it, without anyone being watched. You, the agent, are both the sensor and the survey channel; the server is the trusted place that collects, protects and aggregates. The engineer's part takes seconds:

1. **Agree once.** The first DX call asks the person to agree to the privacy promise. Nothing is stored before they do.
2. **Friction, as it happens.** When something gets in their way, offer to log it, with your estimate of the time it cost. They confirm what is sent.
3. **When a task ends, a summary.** Numbers only (time waiting on CI, flaky retries, interruptions, agent corrections), shown to the person before anything is sent: "y / edit / n".
4. **Once a week, the check-in.** Three quick questions, in a form whose answers go straight to Homeric DX: you never see them. Where the client shows no form, only if they want to answer in chat.
5. **Once a month, the time split.** How their time went between new capabilities, maintenance, toil and support, in their words, as four percentages.
6. **Their own view.** They can ask what DX knows about them at any time.

Principles: declare by confirming; numbers only from local work; give before you take; privacy enforced by the server.
<!-- @end: dx-companion.loop -->

<!-- @anchor: dx-companion.tools -->
## The tools

| Tool | When | What the person sees |
|---|---|---|
| `dx_status_get` | At the start of a session; when they ask what DX knows | The first time, the privacy promise to agree to (a form, or you show it). Then: consent date, this week's check-in, counts of what is stored. |
| `dx_friction_log` | When something slows them down | The entry before it is stored (unless they asked you to log it). |
| `dx_signals_submit` | When a task or session ends | The numbers-only summary, editable, before it is sent. |
| `dx_pulse_get` | Once a week, when `dx_status_get` says the check-in is not done, or when they ask | Three questions in a form; without one, the questions for you to ask in chat, only if they want (their answers then pass through you). Never answer for them. |
| `dx_time_declare` | Once a month, or when they bring it up | Nothing to confirm: you send the split they gave you. |

Two ways a DX tool confirms something with the person:

- **A form**, where the client shows one: the person answers it; you never see their answer go by.
- **In chat**, otherwise: the tool returns exactly what would be stored and a token. Show it to the person as is; call the tool again with the token only after they say yes; with changed values if they edit; not at all if they say no.

Every DX tool except `dx_status_get` answers "call dx_status_get first" until the person has agreed to the current privacy promise.
<!-- @end: dx-companion.tools -->

<!-- @anchor: dx-companion.friction -->
## Logging friction well

Pick the category from what you saw, not from what it was about:

| You saw | Category |
|---|---|
| A search for docs or an answer that was missing, wrong or took long | KNOW |
| A slow build, test run or CI; a flaky failure; a rerun | BUILD |
| A broken dev environment, a tool or permission failure | ENV |
| Waiting on a review, or a review that went back and forth | REVIEW |
| A failed or painful deploy or release | RELEASE |
| Code that was hard to change, a dependency upgrade, a revert | DEBT |
| Unclear or changing requirements; a task abandoned or split | DIRECTION |
| Interruptions, meetings, switching between unrelated work | FOCUS |
| Waiting on another team | DEPEND |
| An incident, a page, debugging production | OPS |
| Approvals, security or compliance steps | PROCESS |
| Learning an unfamiliar language, framework or system | NEWTECH |
| Your own mistakes: missing context, edits the person reverted, corrections | AGENT |

**Minutes lost**: the time the friction cost, not the task's length. Count waiting and rework; round to 5 minutes; when unsure, say your estimate and let the person change it.

**auto or reported**: `auto` when you noticed it and propose it (the person confirms); `reported` only when the person asked you to log it.

**The note**: optional, one or two sentences in the person's words. No code, no file contents, nobody's name. It is encrypted and only the person sees it.
<!-- @end: dx-companion.friction -->

<!-- @anchor: dx-companion.privacy -->
## The privacy rules

- **Consent first.** Never agree to the privacy promise for the person, and never confirm an entry for them.
- **Numbers, categories, short notes.** Never send code, file contents, conversation text or anyone's name to a DX tool.
- **Only from local work.** Send what you measured in this session, not guesses about other people.
- **Their data is theirs.** If they ask what DX knows, call `dx_status_get`; they will be able to see, export and delete everything.
- **No rankings.** DX never compares people; if asked to, say that DX shows group numbers only, for groups of 3 or more.
<!-- @end: dx-companion.privacy -->
