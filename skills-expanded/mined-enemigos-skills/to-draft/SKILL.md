---
name: to-draft
description: Writes the PR title and body for work that is already built, for a person deciding whether to merge, then opens or updates the PR. Use when asked to open a PR or to write or rewrite its body.
disable-model-invocation: true
---

Turn the built work into a PR body a person can skim in a minute. Synthesize. Don't interview the user.

Review agents read the diff, so the body leaves the code to them. It tells a person how risky the merge is, what works now and which decisions were made on the way.

## Steps

1. **Gather.** Read the conversation, the diff against the base branch, the issue and the plan file if the work has one. Report what was built. Where the build left the plan, that's a decision to report. Read the `CLAUDE.md` sections named in Repo requirements.
2. **Prove.** Collect evidence for each result by the rules in Evidence. Start with what the work already produced, like test runs in the conversation and checks on the branch. Done when every result has evidence or is marked `NOT VERIFIED`.
3. **Draft** into the template below. Only the intro and Merge danger are in every body. Any other section stays only when it passes its test in Cut.
4. **Cut.** Go through the draft line by line with the tests in Cut and delete what fails. Done when no line fails.
5. **Check** the draft against Voice and rewrite every line that breaks a rule. When a `humanize` skill is loaded, run it on the whole body, because a person reads all of it. It may reword or delete, but it adds nothing, uses no idioms and leaves headings, labels, markers and required repo lines alone. When it isn't loaded, the Cut and Voice rules are the whole check.
6. **Self-review.** Fix what fails and check again until all of these hold.
   - Skim test. Reading only the title, the bold door verdict and `Review first` tells a person what happened, whether it's safe and what to do next.
   - No section is there because the template has it.
   - Every result is something a person can see or do, not a change to the code.
   - Every decision is one a person might have made differently.
   - No file paths or code names outside `Review first` and the diagrams.
   - The prose before the diagrams is under about 400 words, and under about 150 when the PR changes one behavior, like a copy fix or one new button. These are ceilings. A body that says it in 60 words stops at 60. When it runs over, delete lines anywhere but Merge danger. Don't squeeze sentences to fit.
   - Every sentence has one idea and reads smoothly out loud.
   - No "as mentioned", "see below" or "above". Each section stands alone.
   - Every line the repo requires is present (see Repo requirements).
7. **Publish.** When the branch has a PR, replace its title and body. When it doesn't, open one by the rules in `CLAUDE.md`, which name the checks to run first and the base branch. When a check can't run where you are, open the PR and name that check in your reply. When this PR finishes the last slice of a plan, delete the plan file and its row in `docs/README.md` in the same PR. Read the published body back. When something added a line you didn't write, like a tool credit, tell the user. Reply with the PR link.

## Template

    <Up to 3 short sentences, no heading. Say what the feature does now, the way you would tell a teammate who hasn't heard of it. For a fix, say what was wrong first.>

    ## Merge danger
    **<One-way or Two-way> door.** <What makes it so, and how to roll it back.>

    **Blast radius:** <What else could break, and who would notice.>

    Review first: <the one place a person should look before merging>.

    ## Results
    - <one thing that works now, as the user sees it>. <evidence>.

    ## Decisions
    - <the risk or question>. <what was decided and why>.

    ## No-gos
    - <what this doesn't do>. <where it lives instead, when it has a home>.

    ## Schema change

    <details>
    <summary><what the migration changes></summary>

    <Mermaid erDiagram, only when the PR adds a migration>

    </details>

    ## Flow

    <details>
    <summary><the path from entry point to outcome></summary>

    <Mermaid diagram of the user's path, only when the PR adds or changes one>

    </details>

    Linear [<ID>](<url>)

Mark a point that still needs a person inline as `NEEDS CLARIFICATION (<who>)` on the bullet it blocks.

A small change needs only the intro and Merge danger. Write those two and stop.

The user is whoever the change is for. For internal work that's a teammate or an operator.

Both diagrams sit in collapsed `<details>` blocks, and Flow goes last on purpose. The intro already explains the change, so the diagrams are for checking it, not for orienting. Keep a blank line after `<summary>` and before `</details>`, or GitHub won't render the Mermaid.

## Cut

A template invites filling, and a filled section reads as bloat. Never write a bullet to fill a section. Being true, or being in the conversation, doesn't earn a line its place. A section has to pass its own test first, and then each line in it gets this test. Delete it, then ask whether the reader would decide differently or come back with a question. When the answer is no, it stays deleted.

Two kinds of line fail most.

- **Redundant.** The title or another section already says it, or it describes code the diff already shows. The intro and Results may overlap, because the intro is the claim and Results is its proof.
- **Obvious.** The reader would assume it unprompted, like a no-go nobody expected this PR to cover or a decision nobody would have made differently.

Each optional section has its own test.

- **Results** has one bullet for each thing a person can now see or do, not one for each commit.
- **Decisions** stays when someone on the team could have chosen otherwise and the choice still matters after merge. Expect none to three, though that isn't a limit.
- **No-gos** stays for an option that was really on the table and turned down, like polling. A scope edge listed for completeness isn't one. A turned-down option goes here and not under Decisions, so it's said once. Most PRs have none.
- **Flow** stays when the PR adds or changes a user's path.

In every list, put first the bullet that would cost the most if it were missed. Leave out preamble, recap and a closing line. Cut whole lines. Never shorten a sentence by packing more into it, because a dense sentence is harder to read than a long one.

## Merge danger

A two-way door can be undone by reverting the PR. A one-way door can't, like a migration that drops data, a message already sent to clients, money that moved or a contract another system starts to depend on.

Open with the verdict in bold, like "**Two-way door.**", so it reads at a glance. Judge the door for the system and for the user, and name both when they differ, like "**Two-way door for the system, one-way for the client.** The schema reverts cleanly, but getting the account back means signing again."

Blast radius is what else could break and who would notice, like another flow that runs through the same code or the same screen on the other platform.

Write both in the words the team says out loud. `Review first` is the one line that names code.

This is the one section the Cut step leaves whole. A way the merge can hurt someone stays in, even when the body is long.

A step a person must take around the merge, like a sign-off or a command to run by hand, goes here too.

## Evidence

A result without evidence is a claim. Use the strongest kind the change allows.

- When the result is on screen, show a screenshot or a short recording, with a before when the screen already existed. A parity-tracked screen needs web and mobile.
- When the result is behavior, say what was run and what happened, like "Signing twice in a row removes the account once." A test in the diff that passes on the branch counts. Say what it covers and leave out its name.
- When the result is a number, give before and after with the unit.
- When nothing visible changes, say so in one result. Its evidence is the existing tests passing unchanged.
- When nobody ran it, write `NOT VERIFIED` and why. Don't write that it works.

When an on-screen result was checked but you have no image to attach, leave `SCREENSHOT NEEDED (<what it shows>)` in its place and tell the user. That marker means the picture is missing. `NOT VERIFIED` means the check is.

## Decisions

Report the decisions a person might have made differently, like a product rule, a tradeoff, an option turned down or a place the build left the plan. Leave out choices about how the code is arranged. Name the risk or question first, so a reader sees why each decision exists.

A plan is deleted once its work ships, so the body can't point at it. Its rabbit holes become Decisions and its no-gos stay No-gos. Carry over only the ones that pass the tests in Cut.

## Repo requirements

Read the source section in `CLAUDE.md` each time instead of working from memory, because the rules change. CI checks some of them. Copy a required line as `CLAUDE.md` gives it, even where that breaks a Voice rule.

- **Migration.** Follow "Schema changes need an ER diagram". Put the `erDiagram` under `## Schema change`. A data-only migration gets the `ER diagram: not-needed` line that section gives instead of a diagram.
- **Web change without mobile.** Follow "Web/Mobile Parity" and add its `Mobile-parity: not-needed` line with a reason.

## Voice

- Write the intro with no heading. Leave out "This PR" and "This change".
- Sound like a teammate talking, not release notes.
- Write the title as what changes for the user. Keep it free of words that stop being true after merge, like "plan", "WIP" or "draft". Keep a prefix like `feat:` when the branch's commits use one.
- Join clauses with a word like "and", "so", "but" or "because", or start a new sentence. Keep colons for code, labels like `Review first:` and the line before a list.
- Write results and decisions as short bullets, one per point. Leave out tables.
- Use the word the user sees, not the internal one. Write "monthly deposit" even if the code calls it a draft.
- Write for a teammate whose first language isn't English. Keep one idea in each sentence, and put the subject first.
- Give a definition or a side note its own sentence. Don't tuck it into the middle of another one.
- Use common words and say things literally. Leave out idioms.
- Define a business word a teammate might not know, the first time it appears.
- Give an example only when the idea fails without it.
- Use only hyphens and straight quotes. Leave out checkboxes.
- Leave out any "Generated by" line and any other tool credit.
