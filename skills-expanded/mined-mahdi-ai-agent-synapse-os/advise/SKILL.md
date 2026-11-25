---
name: advise
description: Thinks a problem, a worry or a decision through from what the vault knows — projects, goals, habits, people, recent days — asks what is missing, answers with a grounded view, options and one next step; read-only. Use in consult mode or for "مشاوره بده", "چی کار کنم", "نظرت چیه", "گیر کردم", "advise me", "what should I do", "help me decide", "I'm stuck".
---

# advise

Read-only: never create or edit a node while advising. Offer to save what came out of it at the end, and only `/capture` it when the user says yes.

## Steps

1. Read `index/INDEX.md` and `memory/profile.md`. Name the categories the question touches and read their `index/by-area/<area>.md` — the character map's voice and values too when it is in reach — and skim the last seven days in `index/by-type/journal.md`; open at most 5 nodes (the goal or project in question, the newest journal, a person involved). The runtime context's **Scope** line, when present, says which maps are in reach; never read one outside it.
2. If a fact that changes the advice is missing — what they already tried, how much time they have, what "better" means to them — ask up to three focused questions in one message and stop there; advise on the answer in the next turn.
3. Answer per [references/approach.md](references/approach.md): what the vault shows (with `[[Title]]` links), the real options and their trade-offs, one recommendation with the reasoning, one next step. Say what you are unsure of. Never invent facts about the user.
4. End with one line offering to keep what came out of it (a decision as a note, a step as a task, a change to a goal); file nothing unless they say so.
