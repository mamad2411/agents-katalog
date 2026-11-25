---
name: spike-investigation
description: Runs a time-boxed technical spike on a throwaway branch and writes up what was learned, with evidence and a clear recommendation.
---

# Spike investigation

Answer one question. Throw the code away. Keep the findings.

## Steps

1. Write the question as a sentence that can be answered yes, no or with a number. Write the success and failure criteria before you start, for example "p95 under 200 ms for 10,000 rows". Ask the user for the time box if none is given, and default to 90 minutes of work.
2. Create a branch named `spike/<topic>` or a scratch directory. Never commit spike code to the main branch.
3. Test the riskiest assumption first. Skip error handling, styling, config and tests unless they are the thing in question.
4. Record as you go in a running log: what you tried, the exact command or snippet, and the result with numbers. Paste real output, not summaries.
5. Stop at the time box or when the question is answered, whichever comes first. If it is not answered, say what blocked you and what the next cheapest experiment would be.
6. Check the result once for a bias: was the test data realistic, did you run it more than once, and does the winning option fail on any case you skipped?
7. Write `docs/spikes/<topic>.md` unless the user names another place, with the headings Question, Criteria, What I tried, Findings, Recommendation, Risks, Next steps.

## Rules

- No dependencies added to the real project, and no production credentials or data.
- Do not extend the scope because something interesting appears. List it under Next steps.
- A recommendation names one option and says what would change your mind.

## Report

The answer to the question in one sentence, the evidence, and the path of the write-up.
