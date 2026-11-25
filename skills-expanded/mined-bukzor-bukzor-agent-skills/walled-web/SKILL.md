---
name: walled-web
description: "Agent MUST load when WebFetch hits a login/JS wall (empty shell, 403, \"enable JavaScript\"), when reading a browser capture (*.cdp.jsonl, *.har), or when calling a positional-JSON/JSPB web API."
---

# Working the walled web

Some pages exist only inside a logged-in browser running JavaScript.
WebFetch cannot see them and retrying costs turns. The way through is a
capture taken by the user's browser, read once, and reduced to a plain
HTTP call you can repeat.

## Recognize the wall immediately

Stop after the first WebFetch that returns navigation chrome with no
content, a 403/consent interstitial, or a "please enable JavaScript"
shell. That is the wall, not a transient failure. Rephrasing the prompt
or refetching never fixes it.

## Ask for a capture, with the clicks specified

The user runs the browser; you never run this yourself (it needs their
session and a display):

```bash
~/repo/github.com/bukzor/prototype.chatfs/node_modules/.bin/har-browse URL \
  > HOST.cdp.jsonl
```

It opens a browser and records the CDP event stream until closed.
(It currently lives inside that project's `node_modules`; if the path
has moved, ask rather than guess.)

Ask **early** -- a capture takes the user a minute and unblocks
everything downstream -- and ask **precisely**. The capture only
contains requests the page actually made, so say what to do in the
window: which page to land on, the exact string to type in the search
box, which control to click. One well-specified run beats three vague
ones.

## Handle the capture as a credential

Before opening it: `.gitignore` must already carry `*.cdp.jsonl`,
`*.har`, and the scratch dir. A capture holds live session cookies; a
committed capture is a credential leak with the user's name on it.

The obvious event is misleading. `Network.requestWillBeSent` shows clean
headers; the secrets ride in the `*ExtraInfo` events. Audit names, never
values:

```bash
jq -r 'select(.method=="Network.requestWillBeSentExtraInfo")
       | .params.headers.cookie // empty' F.cdp.jsonl \
  | tr ';' '\n' | sed 's/=.*//' | sort -u        # cookie NAMES only
```

Then decide what you're holding. If the only cookies are analytics and
the XSRF header is empty, the endpoint is **anonymous** -- the best
possible outcome: your reproduction needs no credentials, and nothing
sensitive can leak into a tool, a report, or a commit. If real session
cookies are present, keep them out of files and out of your output; ask
before using them, and prefer finding the anonymous path first.

## Read the capture

Each line is one CDP event: `{"method": ..., "params": ...}`.

```bash
jq -r 'select(.method=="Network.requestWillBeSent")
       | [.params.request.method, .params.request.url] | @tsv' F.cdp.jsonl
jq -r 'select(.method=="Network.requestWillBeSent")
       | select(.params.request.method=="POST")
       | .params.request.postData' F.cdp.jsonl
```

Response *bodies* are generally not in the stream (`Network.dataReceived`
carries sizes only). That is fine: the capture teaches you the request,
and you get the body by replaying it.

## Reduce to the minimum request

Replay the POST with curl, then delete things one at a time -- headers,
cookies, body slots -- rerunning after each. What survives is the actual
API. This is what turns a one-off capture into a repeatable tool, and it
is where you learn whether auth was ever required.

## Positional-JSON (JSPB) APIs

Google's `/action/...` endpoints and similar take arrays whose *index*
is the field number. Four traps:

- Responses are armored with a `)]}'` prefix. Strip it before parsing;
  assert it was there, since its absence means you got something other
  than the API (a login page, an error page).
- Named JSON is rejected outright. Positional arrays only, nulls
  included as placeholders.
- Unknown or misplaced slots are **silently ignored**. A wrong guess
  returns a plausible wrong answer, not an error -- verify against a
  query whose answer you already know.
- Errors come back as a JSON *object* that parses fine and indexes into
  zero results. Assert the response shape (list vs dict) before
  extracting, or you will report "nothing found" when you mean
  "malformed request".

Be a polite client: one request at a time, no loops, cache the response
in the scratch dir and re-read that while iterating on parsing. Send a
User-Agent naming your tool.

## Encode what you learned

Wire knowledge earned this way is expensive and perishable. When an
endpoint will be used more than once, put the request builder and the
response parser in a real tool with tests over recorded fixtures --
never in a shell snippet that only exists in a transcript.
