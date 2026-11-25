---
name: pdes-design-system-rules-file
description: Write your design system as a rules file Claude can follow, with tokens by name and role, component rules with states, layout rules, a list of what the system lacks and a five-prompt test. Use for "run pdes-design-system-rules-file", "design system rules file", "Claude keeps inventing hex values", "make Claude use our components", "design system for AI", "write rules for our tokens", "Claude made up a card component", "test my design system rules", part of the Claude for Product Designers Pack by 90n.
---

# Design System Rules File

## When To Use
Your design system reads well to people, and Claude still invents hex values and a card component you do not have. Documentation written for a designer assumes judgement a model does not bring, so it fills every silence with a plausible guess. This skill answers one question: what does Claude need in writing to stay inside the system you already have?

## When Not To Use
Not for describing the product, its users, its voice or its constraints: that is the Product Context File, and the two never repeat each other. Not for adding to the system either. If your feature needs a part that does not exist, use the Design System Change Record.

## Inputs
- The token file or variables list (names and descriptions; values can stay out)
- Component documentation with variants and states, and the layout and spacing rules as written today, even if scattered
- Two or three real screens: ones that follow the system and ones where a draft went wrong
If you have none of this, I start from the component names you can list from memory and mark the output as a first draft.

## Approach
Tokens are written in the format of the Design Tokens Community Group (designtokens.org, first stable version 2025.10), where a token is a name with a role and never a loose value. Anthropic's help article on setting up a design system in Claude Design says an import is only as good as its source and tells you to test the result with a sample project. The five-prompt test at the end is this skill's own addition to that advice, with no outside source. The failure this prevents: a screen that looks on brand at a glance and contains greys that are in no token file and a card nobody maintains.

## Workflow
1. I ask up to three questions: where the system's source of truth lives (code, library, documents), which five small design tasks you want as the test, and what you count as a pass.
2. Tokens first. I list each one by name and role ("color.text.primary: body text on the default surface"). No rule may contain a raw value; where your notes use one, I flag it and ask which token it should be.
3. Components. For each: what it is for, when to use it, when not to, its states, and the nearest wrong substitute (the part a draft reaches for by mistake).
4. Layout and spacing rules as short imperatives, then do and do not pairs taken from your real screens. Where you have no screen for a rule, the pair reads `[example needed]`.
5. The "missing from the system" list: what Claude must stop and ask about instead of inventing. This is the list that prevents the made-up card.
6. The five-prompt test. You run the five tasks with the file loaded and paste the results back. For each I log which rule held and which failed (an invented value, an invented component, a wrong state), then tighten the failed rule. I add one line linking to the product context file and name the system owner who decides on every gap.

## Output Format
```markdown
# Design System Rules File
Source of truth: [where] · System owner: [role] · Last checked: [date] · Product context: [link]
## Tokens
| Token name | Role | Use it for | Never use it for |
|---|---|---|---|
| [name] | [role] | [case] | [case] |
## Components
| Component | For | Use when | Do not use when | States | Nearest wrong substitute |
|---|---|---|---|---|---|
| [name] | [purpose] | [case] | [case] | [states] | [component] |
## Layout and spacing rules, with do and do not
| Rule (imperative, tokens by name) | Do (real screen) | Do not (real screen) |
|---|---|---|
| [rule] | [frame, or example needed] | [frame, or example needed] |
## Missing from the system
- [What is absent] · Ask [role] instead of inventing
## Five-prompt test
| Task | Rules that held | What failed | Rule changed |
|---|---|---|---|
| [task] | [rules] | [invented value, invented component, wrong state, or none] | [new wording] |
## Decision
[The system owner] decides which items in "Missing from the system" get added, by [date]. [You] rerun the test after each change to the file.
```

## Done When
- No rule contains a raw colour, size or spacing value, and every component has a "do not use when" line and its states
- The missing list exists, even if it has one item
- All five test tasks are logged with what held and what failed, and the file links to the product context file in one line without repeating it

## Quality Bar
- Rules are written as instructions a model can follow, never as descriptions of intent. You set the pass line for the test; I never call a run a pass on my own.
- Do and do not pairs come from your screens. An invented example is worse than `[example needed]`, and a gap in the system stays a gap.
- Works in a plain chat with pasted input. Claude Design can import a design system from a codebase, documents or brand assets and check its output against it, and Anthropic names a `/design-sync` command in Claude Code for that system. This file sits beside the import: paste it, or attach it to a Project so every chat starts with it. The Figma connector is optional: it reads variables and components and has a design system rules tool.
- The rules file reports what the system says; the system owner decides what is added, and a passed five-prompt test is not a tested design.

## Next
Run pdes-product-context-file (Product Context File) to give Claude the product as well as the parts.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
