# Not Actually A Skill

This file is named SKILL.md but has no YAML frontmatter at the head, so it
is not a real Skill package. SkillScanner should emit SKILL-000 only and
suppress all behavioral analysis for this file (PLAN §2.1: the gate that
keeps non-Skill files out of the behavioral denominator).

```python
# Even with code blocks present, this file is not a Skill and should not
# enter the behavioral evaluation. Layer 2 may still surface code findings,
# but Layer 3 (SKILL-010) must not fire.
def hello():
    return "world"
```
