---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, says "grill me", or asks to poke holes in, challenge, or be interviewed about a plan or design, even without the word "grill".
license: MIT
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask at most four frontier questions in one round, or the selected native question tool's lower per-call limit, starting with the ones whose answers remove the most other questions: number each question and give your recommended answer. Before sending, test each pair: when any option of one question would answer or reshape another, the second moves to the next round. Then wait for the user's answers before the next round.

Every choice question includes the smallest option: do nothing, reuse what exists, or defer. Recommend it unless you can name a concrete case the user will hit where it fails. When you recommend more, name what it adds (a field, a state, a command, a file, a concept) and what breaks without it.

## Decision mode

Interactive mode is the default. Only `triage` may select delegated mode under the [delegated triage contract](../../references/harnesses.md#delegated-triage-decisions), passing the user's explicit delegation and its scope. A caller's preference, an unanswered question, or an unavailable user does not select it.

In delegated mode, replace this skill's human question, answer, and final-confirmation waits with recorded decisions inside that scope. For each frontier decision, gather the needed facts, compare the options, choose the recommendation, and record its reason and assumptions before advancing. Keep the same dependency order and smallest-option rule. Do not invent unavailable facts or call an agent's choice a user answer or shared understanding. Missing facts, decisions outside the delegated scope, and separate approval requirements stay unresolved; return them to `triage` instead of claiming completion. Done means every in-scope decision is settled on evidence or explicitly returned as unresolved. Ordinary interactive behavior resumes if delegation is withdrawn.

## Asking questions

Ask in the main conversation through the host's live question capability when it is available, permitted in the current mode, and can represent the question:

- **Claude Code:** `AskUserQuestion`.
- **Codex:** `request_user_input`, or `request_user_input_async` when that is the exposed permitted form.
- **Cursor:** its ask-question capability.
- **OMP:** `ask`.

Follow the live schema instead of copying another host's field names or limits. Put the recommended option first, mark it as recommended when the schema supports that, and describe each option's tradeoff. Keep each question's Q-number in its prompt and a stable question id where supported. Use the tool's built-in custom-answer field rather than adding an `Other` option. Ask each question the native tool can represent through it, even when another question in the round needs chat. An open question can use a native tool that supports free-text-only questions; otherwise ask it in chat. When no native question capability is usable, use chat.

Wait for the user's actual answers before dependent work, the next round, or confirmation of shared understanding. An asynchronous question call returning is not an answer: continue only independent exploration while its reply is pending. A preselected option, timeout, cancellation, or unanswered question leaves that decision open.

For chat questions, use this fallback format:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it when available; otherwise look it up yourself and report that no independent context was available. Anything you could look up yourself is never a question for the user. Don't block unrelated questions: an unfinished lookup is an unsettled prerequisite, so only the questions downstream of it wait for the evidence; ask the rest of the frontier now. A question's premise is a fact too: when sources disagree on it or the user disputes it, settle it with the most direct evidence you can get, such as running the tool in a scratch directory, before the decision that rests on it goes back to the user. The _decisions_ are the user's: put each to them and wait.

Ask only questions whose answer changes what gets built or what the user sees. A detail the implementer can settle alone is not a question, so it never joins the tree. The session is done when the frontier is empty: every decision that changes what gets built is settled. Do not act on it until the user confirms you have reached a shared understanding.
