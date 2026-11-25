---
name: blast-radius
description: Find what a change breaks outside its diff and prove by running code the one fact that makes it safe. Use before merging shared code, data shapes or APIs.
---

# Know what a change breaks

Listing the callers is not the job; a search does that in a second. The job is the breakage a search does not show.

## The proof ladder

A write-up that sounds right proves nothing. For each fact the change depends on, climb as far as is cheap and say where you stopped:

1. **Said.** Your belief. Worth nothing alone.
2. **Pointed.** A real `file:line`, in this repo or in the library's own source.
3. **Walked.** You followed the bad case step by step and it cannot happen.
4. **Ran.** A small script or test calls the real code and fails loudly if you are wrong.
5. **Reproduced.** You saw it in the running app.

Step 4 is usually a short script that imports the same library at the same version and calls the exact function in doubt. Keep it outside the repository.

## Steps

1. **Read the change.** What it adds, changes and deletes, and what it now does differently, including what the diff does not spell out.
2. **Find the one fact.** Most risky-looking changes are safe because of a single fact, such as "this only drops cache entries that are already dead". If it holds, most risks fall with it. Spend your time here.
3. **Look where search stops.** The library's code at the installed version. When things run: teardown, queues, timers, retries. What symbol search misses: the JSON an API returns, a database column, a message another service reads, an environment variable, a feature flag, code three calls away.
4. **Weigh each risk honestly.** A real chance and a real cost for each. Keep confirmed risks apart from the ones you checked and cleared. A search that finds nothing is an answer too; never invent a caller.
5. **Prove the fact.** Write the script, run it, paste the output.

## Hand back

- **What changes**, including the non-obvious part.
- **The fact that makes it safe**, the rung it reached, and the proof. If you could not prove it, write "unproven".
- **Risks:** how each breaks, `file:line`, chance and cost, how to check.
- **Cleared:** what you checked and why it is fine.
- **Before merging:** the cheapest test or reproduction that catches the real failure.
