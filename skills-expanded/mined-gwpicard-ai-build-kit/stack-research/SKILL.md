---
name: stack-research
description: Read what has changed upstream for every product the kit's recipes name, and what tools that build apps with AI now produce by default, then write a dated note proposing a change to each recipe and part, or none. For a maintainer keeping the recipe menu current. Proposes only; it changes nothing in the kit. Load it by its path when you want it.
---

# Stack research

A recipe is only as good as the last time somebody read it against the products
it names. Hosts change their deploy steps, data services change their plan
limits, and the stacks people arrive with drift as the tools that build apps
with AI change their defaults. This read finds that drift and writes it down so
the maintainer can decide what to do about it.

It answers one question. Given what changed upstream since each recipe was last
checked, which recipes need a change, and is there a stack worth a recipe of its
own.

The read proposes and the maintainer decides. Any change it leads to is made as
ordinary work on a branch, through a pull request.

## Read the recipes first

Read `docs/RECIPES.md` before anything else.
Every proposal is made against that format, so a proposal that breaks it is no
use.

Then read every recipe folder in `.agents/skills/setup-hosting/recipes/` and
every part in `.agents/skills/setup-hosting/recipes/parts/`. For each, note its
`Last checked:` date, the products it names, the `How it works:` line of each
section, and the commands its scripts run, since a product's command or option
changing breaks the script. For a recipe, note which sections link a shared
part rather than carrying their own lines, since a change to that part reaches
every recipe that links it.

For each starter under `recipes/parts/starters/`, run `npm audit` with its
lockfile and read the report. Flag any high or critical finding affecting
`next`; list tooling-only findings separately. This check needs npm's current
advisory data, so it belongs in this read before a release, not in CI.

Where the folder holds no recipe yet, say so at the top of the note and carry on
with the rest of the read. The upstream sources and the default stacks are
still worth reading, and a new recipe can still be proposed.

Read the hosting request in
`.agents/skills/setup-hosting/recipes/nextjs-supabase-on-coolify/hosting-request.md`
as well, and the `scripts/hosting-request.sh` beside it. It is the block of
fields the Coolify recipe prints on a first launch, for a tool that runs on a
server somebody else runs.

## Read upstream

Read what changed since each recipe's `Last checked:` date, from the product's
own changelog and documentation. A supplier's own page is the evidence. A
secondary summary site, such as a newsletter, a comparison page or a blog post
about the product, is a pointer only. Where one says something changed, follow
it to the product's own page and cite that, or leave the claim out.

For the products the first recipes name:

- Vercel: the changelog at <https://vercel.com/changelog> and the documentation
  at <https://vercel.com/docs>, for preview deployments, promotion, instant
  rollback, environment variables, logs and plan limits.
- Supabase: the changelog at <https://supabase.com/changelog> and the
  documentation at <https://supabase.com/docs>. Read the backups page at
  <https://supabase.com/docs/guides/platform/backups> for what each plan keeps
  and for how long, and the self-hosting page at
  <https://supabase.com/docs/guides/self-hosting> for what a self-hosted copy
  loses. Plan limits move the backup and restore sections more often than
  anything else does.
- shadcn/ui: the changelog at <https://ui.shadcn.com/docs/changelog> and
  the command documentation at <https://ui.shadcn.com/docs/cli>. Check the
  Radix option and the generated component dependencies against the starter.
- Tailwind CSS: the releases at <https://github.com/tailwindlabs/tailwindcss/releases>
  and the documentation at <https://tailwindcss.com/docs>, including CSS
  configuration and compatibility with the starter's lint plugin.
- The Supabase CLI releases at <https://github.com/supabase/cli/releases>, for
  any change to the commands a recipe's checks run.
- Coolify: the releases at <https://github.com/coollabsio/coolify/releases> and
  the documentation at <https://coolify.io/docs>.
- coolify-devops at <https://github.com/KasperHonore/coolify-devops>: its
  CHANGELOG, and the fields its `host` skill expects in a hosting request. The
  fields are in `skills/host/SKILL.md`, in the section "AI Build Kit: the
  hosting request is the report". Compare those fields with the kit's hosting request, field by field. The two
  have drifted apart before, and a request the server's side cannot read leaves
  a first launch waiting on an answer that never comes.

A recipe added later names its own products. Read those products' changelogs
and documentation the same way, and add them to this list in the same change
that adds the recipe.

## Read what people arrive with

Somebody building with the kit has often started in a tool that builds apps with
AI, and that tool chose a stack for them. Read what each one produces by default
now:

- Lovable, from its documentation at <https://docs.lovable.dev>.
- Bolt, from its documentation at <https://support.bolt.new>.
- v0, from its documentation at <https://v0.app/docs>.

Then read what is established more widely, from sources that publish on a
schedule and say how they reached their view:

- The Thoughtworks Technology Radar, at <https://www.thoughtworks.com/radar>.
- The Stack Overflow Developer Survey, at <https://survey.stackoverflow.co>.
- State of JS, at <https://stateofjs.com>.
- Boring Stack, at <https://boringstack.org>, for plain and proven defaults.

These say what is common and what is settled. They do not say what the kit can
check. A stack earns a proposal only when it is common among the people the kit
serves and it could be checked the way the recipe format asks.

## Write the note

Write the note to `.agents/tmp/stack-research/YYYY-MM-DD.md`, named for the day
of the read. That folder is ignored by git, so the note is never a tracked file
and never reaches a release. Print the same note in the reply.

Name no issue or pull request by number in the note. A note is read later, and a
number there is a pointer that may not survive. Where a proposal is worth
keeping, the maintainer turns it into an issue.

The note has a fixed shape:

```
Stack research, YYYY-MM-DD

RECIPES
<recipe file name>                         last checked YYYY-MM-DD
  Upstream: what changed since that date, each with the page it came from.
            Or: nothing changed that this recipe relies on.
  Proposed: the change, section by section, in the format's own lines.
            Or: no change.
  Real run: needed before the next release, because <section>'s
            How it works line changes. Or: not needed.

PARTS
<part file name>, linked from <recipe>, <recipe>
  Upstream, Proposed and Real run, the same as a recipe.
  Security audit: for a starter, `npm audit` findings affecting `next` and any
                   tooling-only findings. Or: not a starter.

HOSTING REQUEST
  The fields coolify-devops expects against the kit's, and any that differ.
  Or: the fields match.

WHAT PEOPLE ARRIVE WITH
  Each tool's default stack now, and what changed since the last read.

PROPOSED NEW RECIPE
  The stack and place, why it is worth one, and what its real run would need.
  Or: none proposed.

SOURCES
  Every page read, with its address.
```

List every recipe and every part, including those where nothing changed. A
recipe missing from the note reads as one that was not checked, and "no change"
is an answer the maintainer can act on.

### A change to a How it works line

The format says a change to what any section does, in a recipe, a part it
links, or a script either names, needs a new real run before the next release.
A command moved from prose into a script, unchanged and in the same order, does
not. Say so on
every proposal that changes one. For a part, name every recipe that links it,
because each of those needs its own real run. A change to `How it is checked:`
or `Who runs it:` alone does not need a real run, though the recipe's rehearsal
may need the same change.

### Last checked

Moving a `Last checked:` date is a claim that somebody read the recipe against
the current documentation of everything it names. This read does that work, so
where it covered every product a recipe names, the note may propose moving the
date to the day of the read. The date moves only when the maintainer agrees, in
the same change as any other edit to that recipe. Where a product's page could
not be reached, say so, and do not propose moving the date.

### A new recipe

A new recipe is a proposal and nothing more. Do not write a recipe file, since
the folder is the menu and a file there is offered to people. The proposal says
what the recipe would pair, why people arrive with that stack, and what one real
run would need.

## What this read never does

It changes nothing in the kit without the maintainer. It does not edit a recipe,
a part, a rehearsal or the hosting request. It does not move a `Last checked:`
date, open an issue, or open a pull request. Where it finds something worth
changing, it says so in the note and leaves the decision with the maintainer.

## Done when

The note is in `.agents/tmp/stack-research/` under today's date and printed in
the reply. It lists every recipe and every part with what changed upstream and a
proposed change or "no change", says for each change whether it needs a new real
run, and names every page it read. Nothing in the kit has changed.
