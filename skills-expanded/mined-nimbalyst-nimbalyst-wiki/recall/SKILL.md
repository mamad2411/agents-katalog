---
name: recall
description: Answer from the project's wiki what was decided, why, and what it says about an area. Use when the user asks "why did we", "what did we decide", "is there a decision on" or "what does the wiki say", and before starting design or a non-trivial change in an area the wiki may cover.
argument-hint: "[question or area]"
---

Find what the project's wiki already says before answering or changing code. This skill only reads; the `capture` and `update` skills write.

Question or area: $ARGUMENTS (empty means the area of the work at hand)

1. Choose the wiki exactly as the `connect` skill says, in its order: the desktop app's wiki tools when they are available (then use them, not this plugin's), a local wiki whose `.nimbalyst/local-wiki.json` has `migratedTo` (it moved to that team project; its local files are an archive), a `.nimbalyst/wiki.json` pin, and only then the local wiki. `listMarks` and `pagesForFiles` exist only on the `nimbalyst-local` server; on the team wiki or the desktop tools use `searchPages` and `readCollabDoc` for steps 2 to 4. Never answer from a moved wiki's local archive as if it were current; if a local result carries a `movedToTeam` note, switch to the team wiki or say the answer comes from the archive. If there is no wiki at all, say so in one line and stop; do not offer to create one unless the user asks.
2. Decisions and open questions: call `listMarks` with `query` set to two or three key words from the question. Add `kind: "decided"` for "what did we decide" and "why did we", `kind: "open"` for "what is still open", and `by` when the user names a person. With nothing found, try other words once before giving up.
3. Pages: call `searchPages` for the area. When the work is about to change code, call `pagesForFiles` with those files (no arguments checks the working tree) and treat its pages as required reading.
4. Read the few pages that answer it best with `readCollabDoc`, about five at most. A mark's reasoning is in the sentences around it, so read the page, not only the mark.
5. Answer from what you read: each decision with who made it, when, and what it was chosen over; each open question with its owner. Name every page you used with its path in the wiki folder. Say when a page is `stale` (from `pagesForFiles`) or has `status: outdated`, and keep what the wiki says apart from what you infer.
6. If the wiki has nothing on the question, say that plainly in one line and answer from the code or the conversation, labelled as such. If the user then decides something, the `capture` skill records it.
