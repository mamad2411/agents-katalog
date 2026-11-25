---
name: the-tether
description: >-
  How to install this Book of Spells into a conduit so its gathered skills become
  usable — by symlink, not by copy. Use whenever the user wants to install, set
  up, enable, add, or "load" the Book's spells into their agent; asks where skills
  go or how a conduit finds them; or asks how to keep the spells up to date. The
  companion to the-grimoire (which *finds* spells once they are installed): this
  one *shelves the Book* so the grimoire has something to find.
---

# 🔗 The Tethering of the Book — Installing the Spells

You do **not** install the spells one by one. The Book holds hundreds, and no
conduit could carry them all in its head at once. Instead you install the single
keystone — **`the-grimoire`** — and tether it to the living Book. From that one
thread, the grimoire discovers and summons every other spell on demand
(progressive disclosure). Tether the index; the index reaches the rest.

A *tether* is a **symlink**, not a copy. This matters:

- **The Book stays live.** `git pull` in the repo updates every spell at once —
  no re-installing.
- **The paths still resolve.** The grimoire reads its catalogue at `../skills/`,
  *relative to its real home in the repo.* A symlink keeps that thread intact; a
  loose copy would sever it.

## The Rite of Tethering

1. **House the Book.** Clone (or keep) this repository somewhere permanent — the
   tether will point here forever, so don't put it in `/tmp`.

   ```bash
   git clone https://github.com/Pyfagorass/bookofspells.git ~/grimoires/bookofspells
   ```

2. **Find your conduit's skills-shelf.** Each harness keeps its spells in a known
   directory:
   - **Claude Code** — `~/.claude/skills/` (personal) or `<project>/.claude/skills/`
     (one project only).
   - **The open standard** ([agentskills.io](https://agentskills.io/specification))
     — `~/.agents/skills/` (user) or `<repo>/.agents/skills/` (project). Codex,
     Gemini, OpenCode and other honouring conduits read this universal shelf.

   If unsure, consult that conduit's own docs; the tether mechanism is the same
   wherever the shelf lives. The standard guarantees what we rely on: **symlinked
   folders are followed**, and two spells of the same `name` are **never merged**
   — which is why the Book gives each spell a house-prefixed true name.

3. **Cast the tether.** Symlink the keystone folder onto the shelf. Use an
   absolute path to the repo so the link never goes stale:

   ```bash
   BOOK=~/grimoires/bookofspells          # wherever you housed it
   SHELF="$HOME/.agents/skills"           # YOUR conduit's shelf from step 2 (e.g.
                                          # ~/.claude/skills for Claude Code)
   mkdir -p "$SHELF"
   ln -s "$BOOK/the-grimoire" "$SHELF/the-grimoire"
   ```

   Tether **only `the-grimoire`** — it is the single entry point, and routes
   through its catalogue to every other keystone (`the-spellwright` to forge,
   `the-emissary` to summon an MCP server, `the-tether` itself) and to all the
   gathered spells. You need not — and should not — symlink the whole `skills/`
   shelf, nor the other keystones; the grimoire reaches them for you. *(If you
   want one of them to trigger on its own description, you may symlink it
   directly too — but it is not required.)*

4. **Confirm the binding.** Start your conduit and bid it cast a spell the Book
   holds — *"is there a spell for Figma?"* If the grimoire stirs and greps
   `../skills/_index/` back inside the repo, the tether holds.

## Wards

- **Don't move the Book after tethering.** The symlink remembers an absolute
  path; relocate the repo and the thread snaps. Move it, then re-cast the tether.
- **One thread, not eight hundred.** Tether only the keystone(s). The whole point
  of `the-grimoire` is that you carry the index, not the library.
- **A copy is a corpse.** If you copy `the-grimoire/SKILL.md` instead of linking
  it, its `../skills/` paths point at nothing and the spell finds an empty Book.
  Always symlink.

*One thread to the living Book, and every spell is within reach.* 🕯️
