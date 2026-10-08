# Codex Skill Prompt

maverick-oss-skill is an adaptation of [maverick-oss](https://github.com/edujbarrios/maverick-oss) for structured visual interpretation, accessibility-oriented image description, and domain-specific visual reasoning.

Use this prompt when asking Codex or another agent to apply the skill:

```text
Use the maverick-vision skill to interpret the attached image.

User context:
- Mode:
- Domain or task:
- Desired detail level:
- Any specific questions:

Apply the workflow adapted from maverick-oss:
https://github.com/edujbarrios/maverick-oss
1. Identify salient visual evidence, spatial relations, visible text, hazards, uncertainties, and domain-relevant details.
2. Draft a structured description.
3. Critique the draft for unsupported claims, ambiguity, missing uncertainty, and user-relevant omissions.
4. Return a concise refined answer adapted to the user's context.

Do not claim medical, legal, safety-critical, navigation, or professional reliability. Treat the result as assistive visual interpretation.
```
