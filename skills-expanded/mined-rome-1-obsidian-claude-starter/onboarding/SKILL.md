---
name: onboarding
description: Sets up this vault for a new user. Interviews them briefly, fills in the "About me" and Git sections of AGENTS.md, tailors the writing guide, creates their first real project and person notes from the templates, and offers to remove the fictional examples. Use when the user says "set up my vault", "onboard me", "get me started", "personalize this", runs /onboarding, or opens a fresh copy of this template where AGENTS.md still says "(your name)".
---

# Onboarding

Goal: in about ten minutes, turn the template into the user's vault, with their context in `AGENTS.md` and at least one real note of their own.
Keep the interview short. Ask a few questions at a time, accept short answers, and do not lecture about features.

## 1. Check the state

- Read `AGENTS.md`. If "About me" is already filled in, ask whether to update it or skip to step 4.
- Check whether `_examples/` folders still exist.
- Run `git status` to see whether the vault is a git repo and whether `origin` still points at the template's repository (`git remote -v`).

## 2. Interview

Ask, in two or three short rounds:

1. Their name, and what they do (role, field, or main focus).
2. What they want this vault for: projects, research, people, writing, a mix.
3. How they want answers: length, tone, anything that annoys them in AI writing.
4. Git: do they want agents to commit? To push? Is the remote private?

## 3. Write it down

- Fill in "About me" in `AGENTS.md` with their answers, in their words, a line each.
- In the Git section, keep the push option they chose and delete the other.
- Add anything they said about tone or phrasing to `System/writing-guide.md` under "Your additions".
- Show them the diff (`git diff AGENTS.md System/writing-guide.md`) and ask if it reads right.

## 4. First real notes

- Ask for one current project. Create it from `System/Templates/Project.md` as `Projects/<Name>.md`, with today's date and at least one next action.
- Ask for one person they work with or want to keep in touch with. Create `People/<First-Last>.md` from `System/Templates/Person.md` and link it to the project if they are connected.
- Run `python3 scripts/check_vault.py` and fix anything it reports.

## 5. Clean up and hand over

- Offer to remove the examples: `./setup.sh --remove-examples` (it asks before deleting).
- If `origin` still points at the template repository, explain that pushing there will fail and offer the commands to point it at their own private repository; do not run them without a yes.
- Commit with `vault: onboarding - personalize AGENTS.md, first notes` if they agreed to agent commits.
- Finish with three things to try next, picked for what they said they want:
  `/meeting-notes` after their next meeting, `/inbox-triage` once something lands in `Inbox/`, `/weekly-review` at the end of the week.
