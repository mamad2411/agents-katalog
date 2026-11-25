---
name: build-design-system-brief
description: Writes a brief for bringing your design system into Claude Design, covering what to import and from where, the components and tokens the prototype must use, a three-screen spot check and the gaps for the system owner. Use for "run build-design-system-brief", "make the prototype look like our product", "import our design system", "the prototype looks generic", "use our real components", "design tokens for the prototype", "match our brand in Claude Design", part of the Claude for Product Builders Pack by 90n.
---

# Design System Brief

## When To Use
Every prototype comes out in the same generic style and nobody mistakes it for your product. Or worse, they do. Use this before you build the flow. It answers: what does Claude need from the design system, who agreed to share it, and how will you know the output matches?

## When Not To Use
Not for the product's words and facts: use Product Context File. Not for judging whether the finished prototype is usable: use Prototype Heuristic Review. If the test is about a flow and a rough look is enough, skip the import and say so on the screens.

## Inputs
- Where the design system lives: a code repository, design files, or files you can upload
- The role that owns it, whether they have agreed to share it, and two or three screenshots of the real product
If you have none of this, I start from screenshots of the real product and mark the output as a first draft.

## Approach
The method is the design system import in Claude Design (Anthropic help, https://support.claude.com/en/articles/14604416-get-started-with-claude-design), with design tokens as the Design Tokens Community Group defines them (https://www.designtokens.org/): the named decisions on colour, type and spacing that a system stores in a shared format. The help page warns that an import is "only as good as its source". So the judgment is choosing a small, current source over a large, messy one. The failure this prevents: you link the whole codebase without asking, and the prototype faithfully reproduces three generations of buttons.

## Workflow
1. I ask up to three questions. Where does the design system live and which role owns it? Has that owner agreed in writing to link it? Which flow is the prototype for?
2. I pick the import source from the four the help page lists: a code repository, design files, raw uploads, or a local codebase brought in from Claude Code. For a large codebase, only the relevant package or directory. No link is made until the owner's written agreement is recorded with its date.
3. I list the components the prototype must use, by their real names, because prompts that name components get those components. You do not audit token files: I draft the question that asks the owner which colour, type and spacing tokens are current.
4. I write the import and prompt wording for Claude Design, including a visible prototype label on every screen. The closer the match, the more the label matters.
5. I set up the spot check: three generated screens beside the real product, checked for the six failures the Nielsen Norman Group study found in AI prototypes (https://www.nngroup.com/articles/ai-prototyping/): generic type, weak hierarchy, poor grouping, contrast, colour overuse, uneven spacing. You look; I record match or mismatch per screen.
6. I list what the system does not cover as gaps for the owner. You do not patch them with a component of your own and call it the system.

## Output Format
```markdown
# Design System Brief
Flow: [name] · Design system owner: [role] · Prototype label: [exact wording, and where it sits on every screen]
## Import
| Source | Scope (package, directory or files) | Owner agreement (date, where recorded) |
|---|---|---|
| [code repository / design files / uploads / local codebase] | [scope] | [date and link, or "not yet"] |
## Components the prototype must use
| Component (real name) | Used on screen | Notes for the prompt |
|---|---|---|
| [name] | [screen] | [variant or state] |
## Tokens the owner confirmed as current
Colour: [token names] · Type: [token names] · Spacing: [token names] · Confirmed on: [date]
## Three-screen spot check
| Screen | Type | Hierarchy | Grouping | Contrast | Colour use | Spacing |
|---|---|---|---|---|---|---|
| [screen] | [match / mismatch] | [..] | [..] | [..] | [..] | [..] |
## Gaps for the owner
- [What the system does not cover] · needed for [screen] · stand-in used: [what, marked as a stand-in]
## Decision
[Design system owner, by role] agrees the import source and scope by [date]; [builder role] decides after the spot check whether the match is close enough to build the flow.
```

## Done When
- The import source and scope are named, with the owner's agreement and its date, or "not yet" and no link made
- Every required component is listed by its real name, and three screens have been checked beside the real product by a person
- Gaps are written for the owner, with any stand-in marked as a stand-in

## Quality Bar
- A gap is a gap in the system, never a comment on the people who maintain it.
- Token names come from the owner, not from my guess at a file.
- Linking company code is a security question as well as a courtesy: check with your engineering or security lead.
- The closer it looks to the real product, the more it must carry a visible prototype label; the design system owner agrees any link to company code.

## Next
Run build-clickable-prototype (Clickable Prototype) to build the flow with the real components.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
