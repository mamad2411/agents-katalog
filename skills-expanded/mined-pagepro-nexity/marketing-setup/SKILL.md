---
name: marketing-setup
description: Walk a marketer with no terminal experience through setting up the marketing skills (brand-kit, site-contradictions, blog-post-quality-review, internal-links, blog-post-update, and source-review, which blog-post-update uses) step by step, by their preferences, whether they came as the Claude Code plugin `nexity-marketing-skills`, through `npx skills add Pagepro/nexity`, or in a downloaded ZIP of the repository. Checks where the skills are, says what to install and how (click by click), installs and builds what it can itself with permission, runs a short test of each chosen skill, and ends with what the person can now ask for. Use when someone says "Help me setup these skills for marketers", "set up the marketing skills", "skonfiguruj skille marketingowe", "pomóż mi to uruchomić", or has just installed the marketing skills and asks how to start.
---

# Nexity Marketing Skills setup

The person in front of you is a marketer, not a developer. They installed the marketing skills
(as a plugin, with `npx skills`, or by downloading the repository as a ZIP) and typed a
sentence like "Help me setup these skills for marketers". Get them from there to working
skills, one small step at a time.

You do the technical work yourself: you run the commands, read the output and fix what you
can. The person only installs apps, clicks through dialogs and answers your questions.

## Rules

- **Speak their language** (the one they wrote in) and plain words. No jargon without a
  short explanation ("Node.js is a free program the skills run on").
- **One step at a time.** Say what you are about to do and why in a sentence, do it, say what
  happened. When the person has to act (install an app, restart), give numbered clicks and
  wait for them to say "done".
- **Ask before you install or change anything on their computer.** Running a read-only check
  (`node --version`) needs no permission; an install or a build does. Never use `sudo`, admin
  rights or a system package manager unless the person agrees and understands it.
- **Never ask for passwords, API keys or tokens in the chat**, and never read or print `.env`
  files or key files. If a skill needs a key later, say where it goes, not what it is.
- **Do not edit the skills' files.** The exceptions are the `source-review` build (step 3)
  and, in a ZIP, repairing `.claude/skills` (step 1). Working folders the skills create
  (`.brand-kits/`, `.site-contradictions/`, `.source-review/`, `.internal-links/`, `.blog-updates/`) are expected.
- **Stop at the first failure**, explain it in one or two sentences and say exactly what the
  person should do, or what you will try next. Don't pile up errors.
- When a step is fine, say so briefly and move on. Don't explain what already works.

## Step 0: what they want

Ask these together, in one short message, and offer the defaults:

1. **Which skills?** Describe each in one line of their language and let them pick (default:
   all):

   | Skill | In plain words | Needs |
   |---|---|---|
   | `brand-kit` | A `BRAND.md` (voice, audiences, offer, facts with sources) and a report of what the site contradicts, from a company's website | Python 3 for the report builder; without it the skill fills the report by hand |
   | `blog-post-quality-review` | A critical review of one post or draft, with a 0–10 score and the three fixes that matter most | nothing extra |
   | `site-contradictions` | Finds every place where the site says two different things about the same fact (prices, numbers, plans, names), with a fix or a question for each | nothing extra |
   | `internal-links` | Finds links between the site's own articles that are missing, for the editor to add | Node.js |
   | `blog-post-update` | Why a post lost traffic and what to change in it, as a change list for the editor | Node.js and a one-time build of `source-review`, which it uses to check facts; Chrome or Edge for images; Google data optional. Also uses `blog-post-quality-review` and `work-humanizer` |

2. **Which website** should the tests use? Their own company site is best. Ask for one blog
   post URL too, if they picked `blog-post-quality-review` or
   `blog-post-update`.
3. **For `blog-post-update` only:** Search Console and GA4 data are optional. Don't set up
   Google access now; say that the skill asks about it on its first run and that it works
   without it (exports, or no data at all).

## Step 1: where the skills are

`<skills>` below is the folder that holds this skill's folder: the parent of the folder this
`SKILL.md` was loaded from. The other skills sit next to it (`<skills>/source-review`, …). Use
its absolute path in every command. Work out how they were installed from that path, without
asking:

- **Claude Code plugin** (a path under `~/.claude/plugins/`; the skills show as
  `nexity-marketing-skills:<name>`): nothing to check here. Tell the person that a plugin update
  replaces this folder, so `source-review` has to be built again after one (step 3).
- **`npx skills`** (a path under `.claude/skills/`, `.agents/skills/` or `~/.agents/skills/`
  outside a copy of the repository): check that every picked skill is there, plus
  `work-humanizer` when `blog-post-update` is picked. If one is missing, offer to add it with
  `npx skills add Pagepro/nexity --skill <name>` (ask first).
- **A copy of the repository** (ZIP or clone; `<skills>` is `<repo>/.agents/skills` and
  `<repo>/.agents/catalog.json` exists):
  - The person should work in the root of that copy. If they opened a subfolder (`base/`,
    `theme-meridian/`, `web/`), the marketing skills are not there: tell them to open the
    folder one level up, the one made by unzipping (often `nexity-main`).
  - Claude Code finds skills in `.claude/skills`, which should be a link to `.agents/skills`.
    A ZIP unpacked on Windows (and by some unzip tools) turns that link into a small text file
    containing `../.agents/skills`. If `.claude/skills` is a file, not a folder, ask to repair
    it, then replace the file with a copy of `.agents/skills` (on Windows, PowerShell:
    `Remove-Item .claude\skills; Copy-Item .agents\skills .claude\skills -Recurse`). Do the
    same for `.claude/agents` if it is a file. A repaired copy has to be repaired again after
    a newer ZIP (step 5). Then Claude Code needs a new session to see the skills: tell the
    person to start a new conversation in the same folder and write "continue the setup".
  - Codex reads `.agents/skills` directly; nothing to repair.

In any other agent, a skill is used by asking it to "follow `<skills>/<name>/SKILL.md`"; tell
the person so.

**The working folder** is the folder the agent is open in. The skills put their results
there. With a plugin or `npx skills -g`, suggest a folder of its own (e.g. `Documents/Marketing
AI`) rather than the home folder or the Desktop, and tell them to always open that one.

## Step 2: programs

Skip this step when they picked only `brand-kit` and `blog-post-quality-review`: those need
nothing besides the agent, and the agent's web access (step 4 tests it).

**Node.js 20.12 or newer** (22 or newer for the images of `blog-post-update`). Check with
`node --version`.

- Missing or too old: the person installs the **LTS** version from nodejs.org (the big green
  button, then the installer with the default options). On a Mac it may ask for their computer
  password: that is the system's dialog, not you, and it is fine to type it there. If a
  package manager is already installed (`brew` on a Mac, `winget` on Windows), you may offer
  to install it for them instead (`brew install node`, `winget install OpenJS.NodeJS.LTS`);
  ask first.
- After an install, the agent app often does not see Node until it is restarted. Ask them to
  quit the app completely, open it again in the same folder, and write "continue the setup".
  Check `node --version` again before moving on.
- `npm` comes with Node; check `npm --version` when `blog-post-update` is picked (its `source-review` needs a build).

**Chrome or Edge** (only for `blog-post-update`, which renders images through the installed
browser). Ask whether they have one; if not, the skill still works, only without images.

The skills do not need Git.

## Step 3: build

Only when `blog-post-update` is picked (it uses `source-review` to check facts), and
`<skills>/source-review/ts/dist/cli.js` does not exist yet. Ask, then run:

```bash
(cd "<skills>/source-review/ts" && npm install && npm run build)
```

It downloads its packages from the internet and takes a minute or two. Warnings from `npm`
about deprecated packages or "vulnerabilities" are normal; only a line with `ERR!` or a failed
build is a problem. A company network that blocks npm is the usual cause: say so, and ask them
to try at home or ask IT to allow `registry.npmjs.org`.

## Step 4: short tests

Run one test per picked skill, from the working folder. Each should take seconds; say what you
are checking in plain words and report "works" or what failed.

| Skill | Test | Works when |
|---|---|---|
| any | List the skills you can see (Claude Code: type `/` and look, or your own skill list) | Every picked skill is listed |
| `brand-kit`, `site-contradictions`, `blog-post-quality-review` | Open the test site's home page with your web tool | You can read its text (these skills need web access, not Node) |
| `source-review` (with `blog-post-update`) | `node "<skills>/source-review/ts/dist/cli.js" help` | It prints the command list |
| `internal-links` | `node "<skills>/internal-links/scripts/internal-links.mjs" check --site=<their site>` | It finds the sitemap and prints a sample article. Show them the first lines of the sample: if it is the menu or a cookie banner, that is fine for now; the skill fixes it on the first real run |
| `blog-post-update` | `node "<skills>/blog-post-update/scripts/blog-post-update.mjs" setup` | It prints what is configured. "No Google access" is a valid answer |

A failure here goes back to the step it belongs to (Node, the build, the folder). A site that
blocks robots or renders with JavaScript only is a limit of the site, not of the setup: say so,
and suggest another URL or pasting the text.

Then offer **one real run** of a cheap skill, so they see a result: a
`blog-post-quality-review` of the post URL they gave, or a `brand-kit` of their site (longer,
several minutes). Do it only if they say yes.

## Step 5: what they can do now

End with a short summary in their language:

1. **What works** and what was left out (and the one step to add it later).
2. **What to ask for**, as sentences they can copy, one or two per skill they picked, e.g.:
   - "Make a brand kit for https://company.com"
   - "Review this post: https://company.com/blog/…" (or paste the text)
   - "Find contradictions on https://company.com"
   - "Find missing internal links on https://company.com/blog/"
   - "This post dropped in Google, what should we change? https://…"
   In Claude Code they can also type `/` and the skill's name.
3. **Where results land:** in the working folder, in `.brand-kits/`, `.site-contradictions/`,
   `.internal-links/`, `.blog-updates/` and `.source-review/` (hidden folders: the agent opens the reports for
   them on request). Reports are HTML pages that open in the browser.
4. **Nothing is published.** The skills read public pages and propose; a person makes the
   change in the CMS. `internal-links` can write Sanity drafts only when asked and given access.
5. **Updating**, by how they installed:
   - plugin: `/plugin` → Marketplaces → `nexity` → Update (or turn on auto-update there), then
     "Help me setup these skills for marketers" once, to rebuild `source-review`;
   - `npx skills`: ask the agent to run `npx skills update`;
   - ZIP: download it again, unzip it next to the old folder, move the working folders above
     into the new one and say "Help me setup these skills for marketers" there.
