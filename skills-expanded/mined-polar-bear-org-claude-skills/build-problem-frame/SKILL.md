---
name: build-problem-frame
description: Writes a Problem Frame that turns an idea you are already attached to into one testable question with no feature inside it, the decision it feeds and its owner by role, scope in three lists, a "how might we" line and one alternative framing. Use for "run build-problem-frame", "frame the problem", "what question does my idea answer", "I have the screens in my head", "take the feature out of the question", "who decides on this idea", "what is out of scope", "write a how might we", part of the Claude for Product Builders Pack by 90n.
---

# Problem Frame

## When To Use
You already have the idea and the screens in your head, and nobody has said what question it answers. You are one prompt away from building. This skill answers one thing first: what single question, if answered, lets a named role make which decision, and by when?

## When Not To Use
If the question and its owner are already agreed and you need a go-ahead for prototype time, run Idea One-Pager. If nobody has the authority to decide, a frame will not fix that: find the owner first, because a frame with no owner is a wish.

## Inputs
- The idea as you would pitch it today, screens and features included.
- What you saw or heard that started it (a support theme, a session, a number, a complaint).
- Anything already decided that the work must take as given, and how much time you have.
If you have none of this, I start from the idea in one sentence and mark the output as a first draft.

## Approach
The frame is the first of the six requirements of Decision Quality (Strategic Decisions Group, https://www.sdg.com/decision-quality): the right frame, alternatives, meaningful data, clear values and trade-offs, sound reasoning, commitment to action. A decision is only as good as its weakest requirement, and the frame comes first. The open question comes from "How might we" (IDEO Design Kit, https://www.designkit.org/methods/how-might-we.html). The failure this prevents: "users need a dashboard" gets built and tested, and the test can only say whether people liked the dashboard, never whether the need behind it was real. It runs in any Claude chat.

## Workflow
1. Ask at most three questions: what will someone decide with the answer, and which role decides; what did you observe that started the idea; what is already decided, and how much time is there?
2. Start from the idea as it stands and pull the feature out. For every noun that names a feature or a screen, ask what outcome it was meant to move, then restate the need without it. If the need cannot be said without the feature, that is the first thing to tell the owner.
3. Write the trigger apart from the decision. The trigger is what was observed; the decision is what someone will choose. "People drop off at step three" is a fact to look into, not proof that step three needs a redesign.
4. Restate the idea as one question that evidence from real users could answer either way. Two questions means two frames.
5. Set scope in three lists: in, out, and taken as given (already decided). If the time cannot hold everything, move one item from in to out and say which.
6. Write the "how might we" line: begin from the insight, then add "How might we". Test it both ways. If it allows only one answer, broaden it; if it gives no clear place to start, narrow it.
7. Offer one alternative framing and say what you would look at differently under it. Name the decision owner as a role; that role picks the frame. If no role can be named, record "no owner yet" as an open item instead of guessing.

## Output Format
```markdown
# Problem Frame
**The question:** [one question, answerable with evidence, no feature or screen in it]
**How might we:** [insight] How might we [open but bounded]?
## Trigger and decision
| What was observed | What will be decided | Owner (role) | Decide by |
|---|---|---|---|
| [fact and its source] | [the choice] | [role] | [date] |
## Feature set aside
| Feature or screen in the first idea | Outcome it was meant to move |
|---|---|
| [feature] | [need, restated] |
## Scope
| In | Out | Taken as given |
|---|---|---|
| [item] | [item, and why it moved] | [decision already made] |
**Alternative framing:** [other frame] / [what you would look at differently]
## Decision
[Decision owner, by role] agrees, corrects or swaps this frame by [date]. Nothing is built until then.
```

## Done When
- The question names no feature, screen or fix, and evidence could answer it either way.
- The trigger and the decision sit in separate columns, and the trigger has a source.
- All three scope lists hold at least one item, and the "how might we" line passed both the broaden and the narrow test.
- One alternative framing is on the page, and an owner role and a date are named.

## Quality Bar
- The feature you started with is listed as set aside, not deleted: it may still be the answer, it is just not the question.
- Constraints are in your words and unknowns are marked unknown. The frame asks for nothing: time and access to users belong on the next page.
- The owner is a role, never a judgement of the person in it. A loud opinion in the room is recorded as a decision with no owner, not as anyone's fault.
- Claude drafts the frame; the decision owner, named by role, agrees it before anything is built.

## Next
Run build-idea-one-pager (Idea One-Pager) to turn the question into a one-page ask for prototype time.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
