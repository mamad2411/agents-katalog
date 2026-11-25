---
name: ui-ux-review
description: Comprehensive heuristic evaluation (Nielsen Norman 10 heuristics), cognitive walkthroughs, usability severity scoring (0-4), ergonomic interaction audits, and actionable remediation.
---

# UI/UX Heuristic Review & Usability Audit Contract

## 1. Purpose
Conduct rigorous, expert-level UI/UX heuristic evaluations and cognitive walkthroughs across digital product interfaces. Systematically identify usability defects, cognitive friction, visual hierarchy failures, and accessibility gaps, assigning standardized severity ratings (0 to 4) and delivering actionable engineering remediations.

---

## 2. Use When
- Evaluating existing screens, features, or design prototypes prior to release.
- Conducting structured pre-implementation design reviews of wireframes and mockups.
- Auditing user conversion funnels, checkout flows, or complex enterprise SaaS workflows experiencing user drop-off.
- Benchmarking interface ergonomics against industry standards and platform design guidelines (Apple HIG, Google Material Design).

---

## 3. Do Not Use When
- Implementing or modifying code directly in components or stylesheets (use `ui-implementation` or `design-system`).
- Automating pixel-by-pixel regression image diffing in CI (use `visual-regression`).
- Formulating initial user flows from scratch (use `user-flows`).

---

## 4. Required Context
Before conducting a UI/UX review, obtain:
1. **Target User Persona & Mental Model**: Intended technical proficiency, domain knowledge, and frequent tasks.
2. **Feature Acceptance Criteria & Workflows**: What user goal is this interface intended to fulfill?
3. **Target Platforms & Devices**: Web desktop, tablet, mobile viewports, native apps.
4. **Interface Assets**: Interactive prototype, staging URL, wireframes, or high-fidelity screenshots.

---

## 5. Procedure

### Step 1: Cognitive Walkthrough (Task-Centric Evaluation)
Evaluate each sequential step of the core user workflow against the 4 Cognitive Walkthrough questions:
1. *Will the user try to achieve the right effect?* (Is the goal obvious?)
2. *Will the user notice that the correct action is available?* (Is the CTA or control visible and recognizable?)
3. *Will the user associate the correct action with the intended effect?* (Is the label/affordance intuitive?)
4. *If the correct action is performed, will the user see that progress is being made?* (Is system feedback immediate and clear?)

### Step 2: Nielsen Norman 10 Usability Heuristics Audit
Audit the interface systematically against the 10 foundational heuristics:
1. **Visibility of System Status**: Real-time feedback, loading states, progress bars.
2. **Match Between System and Real World**: User-centric language, familiar metaphors, natural conventions.
3. **User Control and Freedom**: Clear emergency exits, Cancel, Undo, Redo.
4. **Consistency and Standards**: Platform conventions, uniform terminology, consistent component styling.
5. **Error Prevention**: Slip prevention, confirmation for destructive actions, smart defaults.
6. **Recognition Rather Than Recall**: Visible options, minimized memory load, persistent contextual cues.
7. **Flexibility and Efficiency of Use**: Keyboard shortcuts, accelerators, progressive disclosure.
8. **Aesthetic and Minimalist Design**: High signal-to-noise ratio, zero visual clutter, strong typographic hierarchy.
9. **Help Users Recognize, Diagnose, and Recover from Errors**: Plain language error text, precise problem location, actionable next steps.
10. **Help and Documentation**: Contextual tooltips, search-friendly help, onboarding micro-copy.

### Step 3: Defect Severity Scoring
Assign each discovered issue a standardized Nielsen Norman severity rating:
- **0 - Not a usability problem**: Discarded or purely subjective preference.
- **1 - Cosmetic problem only**: Minor aesthetic flaw, does not impede task completion.
- **2 - Minor usability problem**: Causes brief hesitation or minor annoyance; low priority fix.
- **3 - Major usability problem**: Significantly impairs task completion or causes user confusion; high priority fix.
- **4 - Usability catastrophe**: Blocks user completely from completing goal or causes critical data loss; imperative blocker.

### Step 4: Formulation of Actionable Engineering Remediations
1. For every severity 2, 3, or 4 issue:
   - Cite the violated heuristic.
   - Describe the exact user impact and failure mode.
   - Propose a concrete, unambiguous design/engineering solution with token or component references.

---

## 6. Decision Rules
1. **Zero Unjustified Opinions**: Every reported defect must cite a specific heuristic, empirical cognitive principle (Fitts's Law, Hick's Law), or accessibility standard.
2. **Blockers for Severity 4**: Any Severity 4 defect (e.g. unrecoverable destructive action without confirmation) constitutes an automatic gate failure.
3. **Prioritize Error Recovery & Prevention**: Heuristic 5 (Error Prevention) and Heuristic 9 (Error Recovery) take precedence over purely visual polish (Heuristic 8).
4. **Preserve User Agency**: Interfaces must never employ dark patterns (confirmshaming, hidden opt-ins, forced continuity).

---

## 7. Evidence Required
- **Heuristic Audit Scorecard**: Tabular matrix of all identified defects with severity ratings and heuristic references.
- **Cognitive Walkthrough Log**: Step-by-step evaluation of the primary task flow.
- **Remediation Specification**: Clear recommendations categorized by engineering priority.

---

## 8. Output Contract
A production UI/UX review deliverable must contain:
1. Heuristic Evaluation Report (`templates/heuristic-evaluation-report.md`).
2. Defect summary table with severity metrics (Count of Catastrophic, Major, Minor, Cosmetic).
3. Prioritized action items for product design and engineering sprints.

---

## 9. Stop Conditions
- 100% of defined task flows evaluated against all 10 heuristics.
- All severity 3 and 4 issues paired with actionable remediations.
- Executive summary with pass/conditional/fail sign-off provided.

---

## 10. Escalation Rules
- Escalate to Product Owner if business objectives inherently conflict with user transparency (e.g. pressure to implement dark patterns).
- Escalate to Security/Legal if privacy policies, cookie consents, or terms of service flows fail regulatory compliance.
