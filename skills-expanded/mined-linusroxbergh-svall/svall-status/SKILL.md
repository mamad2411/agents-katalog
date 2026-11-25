---
name: svall-status
description: Report what every robot is doing and which ones need the user, and save the report as this robot's note.
---

# Report on the fleet

Change nothing except your own note.

1. `svall status` lists every id, name, island and state.
2. For each robot that is `blocked`, `done`, or otherwise seems to want
   something, run `svall robot read <name>`, and
   `svall robot read <name> --transcript --lines 30` when the screen is not
   enough.
3. Print a one-line count, then a block for each island where a robot waits
   on the user, the island with most waiting first. List only robots that wait
   on the user, each on its own, never merged with another: Status, one
   sentence on what it was doing and where that stands; Action, one sentence on
   what the user should do, with the options. Write each island and robot name
   as a link to its id, which selects it on click (`svall status` lists island
   ids):

       12 robots: 1 needs you, 2 to review, 2 working, 7 quiet

       **[svall](svall://island/i_abc123)**

       [bob](svall://robot/c_abc123) · needs you
       - Status: Stopped fixing SV-41 because the auth test fails on main too, not only on its branch.
       - Action: Tell it to drop the test, skip it for now, or fix main first.

       [review-472](svall://robot/c_def456) · to review
       - Status: Reviewed PR #472 and drafted 2 blocking comments on token refresh, not posted yet.
       - Action: Read them, then have it post or soften them.

       **[website](svall://island/i_def456)**

       [deploy](svall://robot/c_ghi789) · to review
       - Status: Shipped 0.8.1 to svall.dev and the smoke check passed.
       - Action: Glance at the site, then close it.

   Needs you: blocked, or asking a question. To review: done or unread, PRs
   waiting on the user, failures only the user can fix.
4. Save the same report as your own note, so it shows on your card. The card
   shows the note as plain text, so write it there without links or bold. Your
   id is the `c_…` in the `svall robot show` line that ends your Svall context.
   Write the id out: a command holding `$SVALL_ROBOT_ID` waits for the user's
   approval. The quoted heredoc keeps quotes and backticks copied from other
   agents intact:

       svall robot update c_abc123 --note-file /dev/stdin <<'EOF'
       3 robots: 1 needs you, 1 to review, 1 quiet

       svall

       bob · needs you
       - Status: Stopped fixing SV-41 because the auth test fails on main too, not only on its branch.
       - Action: Tell it to drop the test, skip it for now, or fix main first.

       review-472 · to review
       - Status: Reviewed PR #472 and drafted 2 blocking comments on token refresh, not posted yet.
       - Action: Read them, then have it post or soften them.
       EOF
