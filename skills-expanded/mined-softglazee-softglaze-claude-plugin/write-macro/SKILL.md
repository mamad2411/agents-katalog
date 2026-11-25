---
name: write-macro
description: "Turns a plain-language task into a SoftGlaze Browser macro, saves it and dry-runs it on one test profile. Use when the user asks to automate a task in SoftGlaze, write or record a macro, or build steps for a site."
argument-hint: "\"<what the macro should do>\" <site URL>"
arguments: [goal, site]
---

# Write a macro from a description

Follow the softglaze-browser skill: read `softglaze://memory/workspace` and
`softglaze://guide/how-softglaze-works` first and follow them. Anything that changes something asks
the user for approval in the SoftGlaze app, so tell them what you are about to change and why first.
Stop every profile you start when you are done.

Goal: $goal. Site: $site. If either is empty, ask the user for it.

1. Pick one test profile (ask the user which, or use one the workspace memory names for testing) and
   start it with start_profile.
2. Open the site with page_navigate and study it with page_snapshot. Find stable selectors: prefer
   ids, name, data-testid or aria labels over long positional paths.
3. Write the steps (goto, click, type, keypress, scroll, wait, waitFor, select, check, clear, submit,
   hover, move). Use waitFor before clicking things that load late. Use {{placeholders}} for any
   personal value, never real passwords.
4. Save it with save_macro. If it fails validation, fix the step it names.
5. Dry-run it with run_macro on that one profile and follow get_run_status. If a step fails, look at
   the page again (page_snapshot), fix the selector and save again.
6. Stop the test profile when done and give the user a short summary of what each step does.

Only automate the user's own, permitted work on that site; never sign-ups, posting at scale or
anything that would break the site's rules.
