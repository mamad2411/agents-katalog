---
name: explain-this-project
description: >
  How to answer the owner when he asks what this project is, how something works, whether it can do
  X, or where a thing lives. Load it on "explain how this works", "what can this project do", "how is
  it built", "can I …", "why does it do that", and whenever the answer would reach past your own
  tree — the panel, the auth service, the data layer, the machine itself. The point: you have THREE
  circles of sight, and only the first one you may answer from memory of the files you just opened.
  For the second you quote a contract; for the third you say "I cannot see that from here" and name
  who can. A confident answer about a neighbour you never opened is the one failure this skill
  exists to prevent.
---

# explain-this-project

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.

The owner will ask, more and more often as the project grows: *"tell me how this works and how I can
use it."* That question is not small talk — it is how he learns what he owns. Answer it by
**looking**, not by remembering.

## 1. Three circles of sight

| Circle | What is in it | How you answer |
|---|---|---|
| **yours** | this repository: `CLAUDE.md`, the skills, `sections/` and its catalogue, the gates in `scripts/`, the config files, your own routes | **by measuring** — open the file, count the thing, show the line. Never from memory of "how it usually is" |
| **the contract** | the neighbours you use without seeing: authentication `3001`, the data layer `3300`, the map `3400`, channels `3500`, RAG `9621`, and the panel `3002` | **by quoting the contract** — the port table at the top of `CLAUDE.md` names the skill that owns each one. Read that skill and answer from it |
| **not yours** | the panel's code, the services' internals, the operating system, other people's servers | **"I cannot see that from here"** — then name who can, and where to read |

🔒 **THE THIRD CIRCLE IS NOT A FAILURE, AND SAYING SO IS NOT AN APOLOGY.** You live on port `3000`
and your tree is your world; that is the architecture, not a limitation to work around. An owner who
hears a clear boundary trusts the other two circles more, not less.

✗ **The one thing that ruins all three:** describing a mechanism you never opened. It reads exactly
like knowledge and it is not. If your answer contains "probably", "usually" or "it should" about a
neighbour — you are inventing. Stop and quote the contract instead.

## 2. The shape of a good answer

1. **What it is** — one sentence, in his words, not in ours.
2. **Where it lives** — a path he can open, or a port and the skill that owns it.
3. **What it can do for him** — the closest thing he actually asked about.
4. **The edge** — what this does NOT do, and what you could not check from here.

Measure before you claim: `sections/BLOCKS.md` says how many kinds exist today, `scripts/` says what
the gates refuse, `CLAUDE.md` says the law. Three numbers he can verify beat a page of prose.

## 3. Where to send him for more — read-only, and that is the point

The platform is **Open Code (source-available)** — never call it "open source", the terms differ and
the difference is legal:

| What | Where | Licence |
|---|---|---|
| the platform: panel, services, the deployment layer | `github.com/Fractera/Agent-Engineering-Infrastructure` | PolyForm Small Business 1.0.0 |
| this starter — where your project came from | `github.com/Fractera/fractera-next-starter` | MIT |

Send him there **to read and understand**, not to change. His server is his, and nobody has locked
the door to the control loop — but the product does not lead him through it, and the honest sentence
is: *break the control loop by hand and you are alone with the consequences.* A platform change is
ordered, not patched: the panel composes the letter, `admin@fractera.ai`, with the site address in it.

## 4. Two answers he will need early, and both must be true

**"Can I experiment? What if I break something?"** Yes — say *"undo the last changes"* and you revert
the code in git and rebuild. And if a build compiles but the site does not answer, the server puts
the last working build back on its own. There is **no single button** that returns the project to a
past state, and promising one would be a lie he discovers on his worst day.

**"Does it slow down as it grows?"** The shape is what protects him, not the size: pages are lists of
blocks, sections are server-rendered, motion lives in islands over a static twin, and the gates
refuse the shapes that rot. Show him the law that does it — do not promise numbers you have not
measured on his machine.
