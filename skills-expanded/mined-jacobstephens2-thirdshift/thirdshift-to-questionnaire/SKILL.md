---
name: thirdshift-to-questionnaire
description: "Write a forwardable questionnaire when a Triage issue needs information."
---

Write a questionnaire for a Triage issue whose outcome is `needs-info`. For `ready-for-human`, describe the needed decision or operator action in the issue body instead. Use the Report and investigation as evidence. Continue investigating everything the repository can answer before asking a person.

Address the person or role with the answer: the reporter, an operator, or the Day shift making a decision. Open with enough context that the Day shift can forward the text on its own. Number the questions; ask for concrete missing observations or decisions and explain briefly what each answer will resolve. Ask only what the repository could not answer. Request redacted evidence rather than credentials or secrets.

Return the complete forwardable Markdown as that proposed issue's `questionnaire` string, separate from its diagnosis and evidence. The questionnaire is complete when each unresolved fact or decision needed to proceed has an answerable question and an intended respondent. Other outcomes have no questionnaire.

thirdshift posts the text on the repository issue and includes it in the Run notification for the Day shift to forward. Never contact a reporter outside the repository or send the questionnaire yourself. Return to the Triage recommendation without waiting for answers.
