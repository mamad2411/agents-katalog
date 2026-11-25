---
name: hci-usability-testing
description: Plans, runs and analyzes usability tests with real users. Use whenever the user wants to test a design, prototype or app with people, write test tasks or a moderator script, choose how many participants, score a SUS questionnaire, calculate task success rates and times with confidence intervals, compare versions, or turn observations into prioritized findings, even if they only say "how do I know if users can use this?". Includes tested scripts for SUS and task metrics.
---

# hci-usability-testing

Find out whether real people can complete real tasks with a product, and report the result with honest numbers. Builds on `hci-foundations`.

```
hci-usability-testing/
├── SKILL.md
├── scripts/
│   ├── sus_score.py           SUS scoring: per participant, mean, SD, 95 percent CI, curved grade
│   └── task_metrics.py        success rate (adjusted Wald interval), median and geometric mean time, errors
├── references/
│   └── running-tests.md       stages, sample size, tasks, recruiting, moderating, analysis, ethics
└── templates/
    ├── test-plan.md           plan skeleton
    ├── moderator-script.md    neutral script and prompts
    ├── sus-responses.csv      example input for sus_score.py
    └── task-results.csv       example input for task_metrics.py
```

## When to use

- Planning a first usability test, or improving an existing process
- Writing tasks, screeners, consent text and a moderator script
- Scoring SUS or computing success rates and time on task
- Comparing two designs or two versions
- Converting session notes into prioritized, evidence-based findings

## Workflow

1. **Define the decision** the test will inform, the user groups and the stage (concept, prototype, build, live). Ask for what is missing.
2. **Plan**: fill `templates/test-plan.md`. Write 3 to 5 realistic tasks (goal and context, no interface words), choose measures, and decide the number of participants: about 5 per group to find problems, 20 or more to measure against a benchmark.
3. **Prepare**: moderator script (`templates/moderator-script.md`), consent, prototype, test data, recording. Include at least one participant using assistive technology when accessibility matters.
4. **Run** with think-aloud and neutral prompts only. Record success, time, errors, confidence and quotes per task.
5. **Compute the numbers**:
   `python3 scripts/sus_score.py responses.csv`
   `python3 scripts/task_metrics.py results.csv --benchmark 0.78`
   Report confidence intervals. With 5 participants the intervals are wide; say so, and describe what the sample can and cannot show.
6. **Analyze**: list problems with evidence, rate severity 0 to 4, count how many participants hit each, find root causes, and write the top three first with a quote, a count and a specific fix.
7. **Follow up**: fix, then retest. Keep the tasks the same so results compare across versions.

## Rules

- Test with the real audience, not colleagues; pay fairly and get informed consent
- Never lead, hint or defend the design during a session
- Report behavior and counts, not opinions; separate observation from interpretation
- Never overstate small samples: show intervals and avoid percentages without n
- Use the geometric mean for task times and include only successful attempts
- Protect participants' data and keep recordings secure
- Do not invent participants, data or quotes; label anything that is an example
- Static review and testing answer different questions: use both

## What to report back

| Field | Content |
|-------|---------|
| Study | goal, participants (n and groups), tasks, method |
| Numbers | success rate with interval, time, errors, SUS with interval and grade |
| Findings | top problems with severity, count, evidence, fix |
| Strengths | what worked |
| Limits | sample size, prototype fidelity, what was not tested |
| Next step | fixes and the retest plan |

## Related skills

- `hci-foundations`: severity scale, heuristics and report format
- `hci-web-accessibility`: include assistive technology users and WCAG checks
- `hci-rtl-localization`: recruit and test in the target language
- `hci-microcopy`: test wording of labels and messages
