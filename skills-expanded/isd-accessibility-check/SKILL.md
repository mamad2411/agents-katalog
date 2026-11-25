---
name: isd-accessibility-check
description: Prepares a first accessibility review of a course screen by screen, producing a results table marked pass, fail or cannot check here, the list a person must test with assistive technology, and a fix list with owners. Use for "run isd-accessibility-check", "first accessibility pass on this storyboard", "check the alt text and headings", "are the captions and transcript there", "what do I need to test with a screen reader", "accessibility before the build is locked", "keyboard test checklist for this course", "which accessibility fails block release", part of the Claude for Instructional Designers Pack by 90n.
---

# Accessibility Check

## When To Use
Accessibility is found after the build, when every fix costs a rebuild. Use this on the storyboard, on screenshots or on the exported file, as early as there is something to look at and again on the finished build. It answers one question: can everyone perceive and operate this course, and what still has to be tested by a person?

## When Not To Use
This is a first review, not a conformance evaluation and not a statement about legal duties: for either, check with a qualified adviser. How the course feels to one learner taking it start to finish is Designer Run-Through. Writing the alt text in the first place belongs to E-Learning Storyboard Template.

## Inputs
- The level you work to (A or AA) and who owns accessibility in your organisation. I do not choose the level.
- The storyboard or screen text with alt text, screenshots, or the exported file; caption and transcript files for any media; who will test with a keyboard and a screen reader, by role.
If you have none of this, I start from the screen text alone, mark most checks "cannot check here", and mark the output as a first draft.

## Approach
The standard is WCAG 2.2, a W3C Recommendation with levels A, AA and AAA. The pass follows W3C WAI's "Easy Checks, A First Review of Web Accessibility", which W3C describes as "designed to be quick and easy, rather than definitive". The judgment is in the third result: "cannot check here" is honest, and a guessed pass is the failure this skill exists to prevent. Picture the report that says "keyboard accessible: pass" written from a storyboard, and the learner who meets a drag-and-drop with no key that moves it.

## Workflow
1. Ask up to three questions: which level you work to, who owns accessibility and decides what blocks release, and who will run the person tests.
2. Go through the Easy Checks list item by item, for each screen and each media file: page or screen title, image text alternatives, headings, contrast, text resize, keyboard access and visible focus, forms, labels and errors, moving, flashing or blinking content, multimedia alternatives, basic structure.
3. Give each one of three results: pass, fail, or cannot check here with what a person must do to check it. Claude can read from text and files: missing or empty alt text, alt text that begins "image of", heading order, link text such as "click here", whether captions and a transcript exist, instructions that rely on colour or position alone.
4. Send to the person-test list everything a description cannot show: real keyboard order, focus visibility, contrast on the rendered screen, screen reader behaviour, timing and time limits.
5. Write the person-test list as a script: keyboard only from the first screen to the last, a screen reader on a sample of screens you pick (include every interaction type), zoom and text resize, captions read against the audio. A named tester by role runs it and records what happened.
6. Give each fail a fix owner by role. Whether it blocks release is decided by the person who owns accessibility, not by you alone and not by Claude. Rerun the pass on fixed screens and record the version checked.

## Output Format
```markdown
# Accessibility Check
This is a first review, not a conformance evaluation. Legal conformance: check with a qualified adviser.
Course: [name, version] | Level worked to: [A or AA, set by whom] | First pass prepared by: [designer, role], [date] | Accessibility owner: [name, role]
## First pass, by screen or media file
| Screen or file | Check | Result (pass / fail / cannot check here) | What was seen | What a person must do to check it |
|---|---|---|---|---|
| [screen] | [image text alternatives] | [result] | [observation] | [step, or n/a] |
## Person-test list
| Test | Screens covered | Tester (role) | Date run | What happened |
|---|---|---|---|---|
| Keyboard only, start to finish | [all] | [role] | [date] | [tester fills] |
| Screen reader | [sample you chose] | [role] | [date] | [tester fills] |
| Zoom and text resize | [sample] | [role] | [date] | [tester fills] |
| Captions against the audio | [media files] | [role] | [date] | [tester fills] |
## Fails and fix owners
| Fail | Screen or file | Fix | Fix owner (role) | Blocks release? (accessibility owner decides) | Fixed in version |
|---|---|---|---|---|---|
| [fail] | [screen] | [fix] | [role] | [yes / no, decided by whom] | [version] |
## Decision
First pass prepared by [designer, role] on [date]; person tests run by [tester, role] on [date]. [Accessibility owner, name] decides which fails block release by [date]; each fix owner closes their fails by [date].
```

## Done When
- Every screen and media file has a result for every check that applies.
- No result is a pass unless something was read or seen that supports it.
- Every fail has a fix owner and a blocking decision with the name of who made it, and every person test has a tester by role and a date.

## Quality Bar
- The first line of the output says it is a first review, not a conformance evaluation.
- A storyboard can never earn a pass on keyboard order, focus, rendered contrast or screen reader behaviour.
- No assumption is made about any learner's disability; colleagues who test are invited, never assigned, and the notes are about the course.
- The level is the one you stated; the skill never restates or interprets a legal duty.
- Claude does a first pass and says what it cannot check; a person tests with assistive technology, and a named person decides what blocks release.

## Next
Run isd-designer-run-through (Designer Run-Through) to take the whole course yourself.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
