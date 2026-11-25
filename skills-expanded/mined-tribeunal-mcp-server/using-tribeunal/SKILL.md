---
name: using-tribeunal
description: Use when a session first reaches for Tribeunal's tools, when a request involves cases, juries, verdicts, tribes or share links and it is unclear which workflow applies, or when a Tribeunal tool call is refused and the reason needs interpreting. Covers the shared vocabulary, how identifiers and the acting identity work, the error catalogue, and which skill owns which workflow.
---

# Using Tribeunal

Tribeunal puts a question to a jury and returns a verdict. The tools on the Tribeunal MCP server are
the connectivity; the skills below carry the procedure. Start here, then go to the owner of your task.

## Vocabulary

A **case** is the question, its **sides** are the options a voter picks between, and the **jurors**
who make up its **jury** vote it into a **verdict**. A **tribe** is a standing group to draw a jury
from. A **share link** is the view-only URL for a private case. The web UI says "case"; the API says
"trial" — same thing.

## Identifiers and identity

Cases, sides, tribes and webhooks are addressed by UUID; a number or slug will not resolve, so find
the case with `tribeunal_search_cases`. Comment, evidence and member ids are plain strings.

You act as whoever signed in — on a shared connector, not necessarily the account that owns the
case. `tribeunal_get_user` with no `userId` answers it — there is no separate current-user tool; the
same tool given a `userId` (a UUID or a username) reads anyone else's account instead.

## Where to go next

| The task | Skill |
| --- | --- |
| Get something decided, ruled on or polled | `deciding-with-a-jury` |
| Wait on an outcome, or act once one lands | `acting-on-verdicts` |
| Serve as a juror, by invitation or matchmaking | `serving-jury-duty` |
| Read a case record and form or contribute a view | `weighing-evidence` |
| Have specific people or a tribe decide it | `convening-a-team-jury` |
| Settle a dispute between two parties (an advisory ruling) | `arbitrating-a-dispute` |
| Ask someone to pay into escrow with a jury as arbiter | `arbitrating-a-dispute` |
| Tell another system what the jury said | `wiring-webhooks` |

## When a call is refused

`Invalid parameters: …` means the arguments never left this machine — reread the schema. `API
Error: …` means the server refused; the reason is a stable code on some endpoints and prose on
others. `references/errors.md` says what each means and whether a retry can ever help. Several are
terminal.

## Gotchas

| Trap | What is true |
| --- | --- |
| `open` means votable | It stays `open` past its deadline until the close job runs. Time left is the test. |
| Searching open cases finds only open ones | Cases still assembling a jury match that filter too. |
| A private case's URL can be passed around | It's a dead end for everyone else — a login wall or an access-denied page; the share link is the shareable one. |
| Closing returns the verdict | Closing is asynchronous — the verdict lands separately. |
| No verdict means a tie | It can instead mean a failed quorum or requirement, which is not a tie. |

`references/tools.md` lists every tool with its flags and required arguments, generated from the
server's definitions — trust it over memory.
