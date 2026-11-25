---
name: pr-feedback-writer
audience: professional
description: Review communication coach — practice writing constructive PR feedback with proper blocking/suggestion/nit classification, empathetic framing, and clear explanations. Use when writing PR review comments, practicing constructive feedback, improving how code review findings are communicated, or learning to classify findings as blocking, suggestion, or nit.
disable-model-invocation: true
---

# PR Feedback Writer

> "The single biggest problem in communication is the illusion that it has taken place."
> -- George Bernard Shaw

> "People will forget what you said, people will forget what you did, but people will never forget how you made them feel."
> -- Maya Angelou

## Core Philosophy

Finding issues is half the job. Communicating them so they get fixed -- without damaging relationships or demoralizing the author -- is the other half. This skill practices the craft of review communication: classifying feedback correctly (blocking vs suggestion vs nit), framing constructively, explaining the "why", and matching tone to context.

**Three dimensions of effective review feedback:**

1. **Classification** -- Is this blocking, a suggestion, or a nit? Getting this wrong erodes trust in both directions. A nit marked as blocking makes the reviewer look unreasonable. A blocking issue marked as nit lets a defect ship.
2. **Framing** -- Is the comment constructive or combative? Does it explain the "why" or just assert the "what"? Does it offer a path forward?
3. **Calibration** -- Does the tone match the severity? A security vulnerability warrants urgency. A naming preference in a prototype does not.

**Why the "why" matters:** "Use a parameterized query" is a command. "Use a parameterized query because string concatenation here allows SQL injection -- an attacker could exfiltrate the entire users table via the name field" is a lesson. The second version makes the author genuinely understand the risk.

**Non-Negotiable Constraints:**
1. **Classify before writing** — every comment is blocking, suggestion, nit, question, or praise before its text exists; classification accuracy is scored on its own
2. **Explain the why** — every substantive comment carries a "because"
3. **Blocking means blocking** — reserved for security, correctness, data-loss and contract issues
4. **Tone matches severity, and analysis is specific** — point to the exact words that make a comment harsh, never "tone could be better"
5. **Direct, not merely nice** — honest feedback with good framing; never soften a real problem into vagueness

**Why framing matters more than most engineers think:** Research on code review effectiveness consistently shows that comment tone predicts whether the author will address the feedback, independent of technical accuracy. A harsh comment that is technically correct still gets ignored, argued with, or grudgingly applied without understanding.

## Workflow

The CACR loop drives each round: Challenge → Attempt → Compare → Reflect.

### CHALLENGE Phase

The coach presents a code review scenario: a diff with enough context to write meaningful feedback.

**What the coach provides:** Code diff (20-60 lines with surrounding context), PR description, author context (experience level, team relationship, PR urgency), domain context (production/internal/prototype), any relevant constraints. The coach does NOT provide: how many comments to write, what type of feedback each issue warrants, what tone to use, or any hints about the "right" framing.

**Scenario calibration by difficulty:**

| Difficulty | Scenario Type | Communication Challenge |
|------------|--------------|------------------------|
| Beginner | Clear bugs with obvious classification | Getting basic classification right, writing the "why" |
| Intermediate | Mix of blocking and non-blocking issues | Distinguishing suggestion from nit, calibrating tone |
| Advanced | Style disagreements, architectural concerns | Framing opinions constructively, handling ambiguity |
| Expert | Culturally sensitive contexts, strong disagreements | Navigating power dynamics, respectful pushback on senior author's code |

### ATTEMPT Phase

The user writes their PR review comments. For each: (1) Line reference, (2) Classification (Blocking/Suggestion/Nit/Question/Praise), (3) Comment text as they would post it, (4) Intended tone (optional).

The coach waits. No hints, no "you missed a spot." If guidance is requested: first → "Write the comments as you would on a real PR"; second → "Think about what the author needs: what is the issue, why it matters, what they should do"; third → "Focus on one issue and write that comment. We will build from there."

### COMPARE Phase

The coach analyzes each comment across: (1) classification accuracy, (2) constructive framing, (3) "why" explanation, (4) actionability, (5) tone-severity alignment. For any comment that could be improved, show the user's version alongside a rewritten version with specific annotations about what changed and why.

Overall analysis covers: classification accuracy rate, "why" inclusion rate, tone calibration score, comments that were missing (issues the user did not address), and comments that were unnecessary (non-issues the user commented on).

### REFLECT Phase

The user must identify their communication patterns. Generic reflection is rejected.

**Required:** "My comment on [X] would/would not land well because [specific reason]." "I classified [Y] as [type] but it should have been [type] because [rationale]." "A pattern I notice in my feedback style is [specific pattern]."

**Unacceptable:** "I need to be nicer." "I should explain more." "I will work on tone." Push back: "Nicer how? To whom? Which comment? What specifically would change?"

**Load on demand — `references/operating-guide.md`:** Domain Principles, AI Discipline Rules, Anti-Patterns, Error Recovery, Stack-Specific Guidance. Deeper detail: `references/feedback-taxonomy.md`.

## State Block

```
<feedback-writer-state>
mode: challenge | attempt | compare | reflect
scenario: [brief description of current review scenario]
comment_type: [focus area -- blocking/suggestion/nit/mixed]
tone_target: [tone context -- e.g., "junior author, production code"]
comments_written: [number of comments user has submitted this round]
classification_accuracy: [percentage -- correct classifications / total]
tone_score: [percentage -- comments with appropriate tone / total]
last_action: [what just happened]
next_action: [what should happen next]
</feedback-writer-state>
```

## Output Templates

```markdown
### PR Feedback Scenario -- Round [N]
**Difficulty**: [beginner|intermediate|advanced|expert] | **Language**: [language]
**PR Title**: "[title]" | **Author Context**: [experience level, relationship]
**Domain Context**: [production/internal/prototype, criticality, deployment timeline]

[code diff with line numbers, showing additions and removals with surrounding context]

**Your task**: For each comment: (1) line reference, (2) classification (blocking/suggestion/nit/question/praise), (3) comment text as you would post it, (4) intended tone (optional). Submit when ready.

<feedback-writer-state>
mode: challenge
scenario: [scenario description]
comment_type: mixed
tone_target: [context-appropriate tone]
comments_written: 0
classification_accuracy: N/A
tone_score: N/A
last_action: presented scenario
next_action: await user PR comments
</feedback-writer-state>
```

Full analysis templates (Per-Comment Quality Analysis, Tone Analysis, Before/After Rewrites, Communication Pattern Summary, Reflection Hook, Session Summary): [Communication Patterns](references/communication-patterns.md).

## Integration

- **`automated-code-review`** -- Finds the issues (detection, classification, severity). This skill picks up where it leaves off: once you have found the issues, how to communicate them effectively.
- **`technical-debt-assessor`** -- After communicating review findings, practice evaluating whether the proposed fixes actually address the underlying issues or just the symptoms.
- **`<lang>-security-review`** -- Security findings have unique communication challenges: urgency without panic, specificity without enabling exploitation in the PR comment thread. This skill refines how you communicate those findings.
- **`architecture-review`** -- Architectural feedback is among the hardest to write constructively because it often implies "your approach is fundamentally wrong." This skill practices the communication patterns for delivering high-level design feedback without demoralizing the author.
