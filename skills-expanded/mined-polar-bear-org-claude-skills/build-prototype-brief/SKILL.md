---
name: build-prototype-brief
description: Writes a one-page prototype brief that sets how real the prototype must be on three separate dimensions, what is real and what a person fakes by hand, which Claude surface fits, the visual direction, the out list and a time box. Use for "run build-prototype-brief", "how real does this prototype need to be", "sketch, clickable or working", "which Claude surface should I build this in", "can I fake this part by hand", "write the brief before I prompt", "build me an app", part of the Claude for Product Builders Pack by 90n.
---

# Prototype Brief

## When To Use
You are about to type "build me an app" and have not decided how much of it has to work. Use it once the belief to test is written and before any screen exists. It answers one question: what is the least real thing that would still test this belief with real users?

## When Not To Use
If nobody has written the belief or the pass line yet, run Prototype Test Card first; a brief with no belief only decides how polished to make a guess. If you need the list of behaviours and their checks, that is Prototype Spec. This brief holds no numbered requirements.

## Inputs
- The belief and the pass line from your test card, pasted as written
- Who will try the prototype and where (in a room with you, on a call, alone with a link), and the time you can give it
- Anything that already exists: sketches, screenshots, a design system, sample content
If you have none of this, I start from your idea in one sentence and mark the output as a first draft, with the belief listed as the first open item.

## Approach
Fidelity is not one dial. Nielsen Norman Group splits it into interactivity, visuals and content (https://www.nngroup.com/articles/ux-prototype-hi-lo-fidelity/), and describes the Wizard of Oz method, where a hidden person produces what the system would (https://www.nngroup.com/articles/wizard-of-oz/). Each dimension is set on its own from the belief, then matched to the Claude surface Anthropic describes for that job (https://support.claude.com/en/articles/14604416-get-started-with-claude-design, https://support.claude.com/en/articles/9487310-what-are-artifacts-and-how-do-i-use-them, https://code.claude.com/docs/en/overview). The failure it prevents: a week spent polishing screens for a belief that was about whether people finish the flow, shown to onlookers who then ask for a date.

## Workflow
1. I ask at most three questions: what belief are we testing and what is its pass line, who tries it and in what setting, and what is your time box?
2. Set the three dimensions one by one, each with a reason tied to the belief. Interactivity: do the controls work. Visuals: look and layout. Content: final or placeholder. A belief about a flow needs working controls, not polish. Then name the overall level: sketch, clickable or working.
3. State the trade out loud. A rough prototype tells everyone it is unfinished and invites honest negative reactions; a polished one makes users behave more as they would with live software and makes onlookers think it is done. Pick the side this test needs.
4. Split real from faked. For every faked part choose the Wizard of Oz form: closed responses from a preset list, open responses written live, or a mix. Write who plays the part and what they may answer, and pilot it once. Record what it cannot show: speed, scale, and what happens with nobody behind it.
5. Choose the surface, the least that tests the belief. Claude Design makes interactive prototypes from a conversation. An artifact is a small interactive app described in chat. Claude Code reads and edits files and runs commands in a folder. Working code is the last resort, not the default.
6. Write the visual direction in specific terms: named components, type, spacing, the states to draw. Vague prompts give generic output (https://www.nngroup.com/articles/ai-prototyping/), so "clean and modern" is replaced with specifics or cut.
7. Close with the out list and the time box you set. I never set the time box for you, and I name every faked part as faked.

## Output Format
```markdown
# Prototype Brief
Idea: [name] | Belief tested: [one line from the test card] | Overall level: [sketch, clickable or working] | Date: [date]
## How real
| Dimension | Level chosen | Why the belief needs this |
|---|---|---|
| Interactivity | [none, some controls, full flow] | [reason] |
| Visuals | [rough, close to real] | [reason] |
| Content | [placeholder, realistic sample] | [reason] |
## Real and faked
| Part | Real or faked | If faked: who plays it, closed or open responses | What this cannot show |
|---|---|---|---|
| [part] | [real or faked] | [role, response type] | [limit] |
Pilot run: [date] | Testers told afterwards by: [role]
## Surface
[Claude Design, an artifact or Claude Code], because [reason]. Ruled out: [surface], because [reason].
## Visual direction
- Components: [names] | Type: [detail] | Spacing: [detail] | States to draw: [list]
## Out
- [Thing a reasonable reader would expect and will not get]
## Decision
[Role who owns the test] agrees the level, the faked parts and the time box of [length] by [date]; the build starts only after that.
```

## Done When
- Each of the three dimensions has its own level and a reason that names the belief
- Every faked part has a person, a response type and a stated limit
- One surface is chosen and at least one is ruled out with a reason
- The visual direction contains no adjective that could describe any app

## Quality Bar
- The level follows the belief, never how good it would look in a demo, and real target users try it, not colleagues.
- No numbered requirements or checks here, and no invented timings or findings; unknowns stay as [placeholders].
- If a person plays the system, testers are told afterwards and can withdraw what they said. On consent, check with a qualified adviser.
- Faked parts are named as faked in the brief, and the brief never calls the result a product.

## Next
Run build-user-flow (Screen-by-Screen User Flow) to list every screen before any is drawn.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
