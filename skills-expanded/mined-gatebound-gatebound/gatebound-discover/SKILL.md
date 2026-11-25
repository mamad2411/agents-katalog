---
name: gatebound-discover
description: Find a problem worth building when the user does not yet know what to build — a free-ranging conversation with no fixed question slots surfaces pains, summarizes the improvement opportunities that emerge, confirms the summary into spec/00-discovery.md, then hands off to interview. Korean triggers — "뭘 만들지 모르겠어", "아이디어가 없어", "만들 만한 거 찾아줘", "뭐부터 시작하지", "문제 발굴". English triggers — "I don't know what to build", "help me find a project", "what should I make", "discover a problem". NOT for a user who can already name one real user and their pain — that goes to gatebound-interview.
user-invocable: false
---

# gatebound-discover

Invoke `/gatebound:discover` with the user's text as the argument, or with no
argument when they have nothing yet.

Do not run the discovery conversation here. `plugin/commands/discover.md` is the
execution instruction; this file only routes to it.

Pass the user's own wording through, unparaphrased — the command detects the
output language from it.

If the user already names one real person and what that person struggles
with, route to `/gatebound:interview` instead.

Under a host without slash commands (Codex), `/gatebound:discover` does not exist:
read `commands/discover.md` two directories above this skill's folder and follow
it, applying `policy/codex.md` from the same plugin.
