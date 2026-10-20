---
name: post-incident-learning
version: 1.0.0
min_mindforge_version: 10.1.0
status: stable
triggers: post-incident learning, systemic pattern, defense mechanism, recurrence prevention, incident class, contributing factor analysis, improvement measurement, learning review, incident pattern, failure class prevention, defense layer, systemic fix
compose: incident-management
---

# Post-Incident Learning

## When this skill activates

This skill activates after an incident has been resolved and the team needs to extract
lasting organizational learning. It goes beyond traditional postmortems (which document
what happened) to identify failure classes, build defense mechanisms, and measure
whether the organization is actually getting better at preventing recurrence.

## Mandatory actions when this skill is active

### Before

1. **Gather incident data** — Timeline, logs, communications, actions taken, resolution
   steps. Ensure the raw facts are documented before memory fades.
2. **Identify participants** — Who was involved in detection, response, and resolution?
   Schedule the learning review within 72 hours of resolution.
3. **Set the frame** — This is a learning exercise, not a blame exercise. Establish
   psychological safety explicitly. No individual fault-finding.

### During

4. **Distinguish postmortem from learning:**
   - Postmortem = What happened? (timeline, root cause, impact)
   - Learning = What patterns do we now defend against? (systemic improvement)
   - This skill focuses on the LEARNING phase that follows the postmortem.

5. **Contributing factor analysis (go beyond root cause):**
   - **Proximate cause** — The immediate trigger (e.g., bad deploy, config change).
   - **Contributing factors** — Conditions that allowed the trigger to cause harm
     (e.g., missing validation, no canary, insufficient monitoring).
   - **Systemic conditions** — Organizational patterns that created the contributing
     factors (e.g., time pressure, unclear ownership, technical debt tolerance).
   - Map all three levels. Fixes at only the proximate level guarantee recurrence.

6. **Identify the incident CLASS:**
   - This is not just one incident — what CLASS of failure does it represent?
   - Examples: "deploy without validation," "silent dependency failure," "config
     drift between environments," "cascading timeout."
   - Name the class explicitly. Search history for past incidents of the same class.
   - If this class has occurred before, the previous fixes were insufficient.

7. **Design defense mechanisms (layered):**
   - **Layer 1: Automated prevention** — Make the failure impossible through code,
     infrastructure, or tooling changes (strongest defense).
   - **Layer 2: Automated detection** — If prevention is impossible, detect instantly
     and auto-remediate or alert within seconds.
   - **Layer 3: Process improvement** — Checklists, review steps, approval gates
     (weakest defense — humans forget).
   - Never accept "be more careful" as a defense mechanism.
   - Prefer Layer 1 > Layer 2 > Layer 3 always.

8. **Define improvement measurements:**
   - **Mean time between incidents of same class** — Trending up means defenses work.
   - **Detection time** — Time from failure occurrence to human awareness.
   - **Recovery time** — Time from awareness to full resolution.
   - **Blast radius** — Users/systems affected (should shrink over time).
   - Set specific targets for each metric.

9. **Create action items with teeth:**
   - Each action item must have: owner, deadline, definition of done, and verification
     method.
   - Classify priority: P0 (fix this week), P1 (fix this sprint), P2 (fix this quarter).
   - Track completion publicly. Incomplete incident actions are organizational debt.

### After

10. **Share the learning broadly** — Publish findings to the engineering organization.
    Other teams may have the same class of vulnerability.
11. **Update runbooks and alerts** — Ensure the detection and response improvements are
    codified in operational documentation.
12. **Schedule verification** — In 30 days, verify that defense mechanisms are in place
    and metrics show improvement. If not, escalate.
13. **Feed into incident class tracker** — Maintain an organizational record of incident
    classes, their defenses, and recurrence rates.

## Self-check before task completion

- [ ] Contributing factors analyzed at all three levels (proximate, contributing, systemic)
- [ ] Incident class identified and named (not just this one incident)
- [ ] Historical incidents of same class searched and referenced
- [ ] Defense mechanisms designed with preference for automation over process
- [ ] No action item says "be more careful" or equivalent
- [ ] Metrics defined with specific improvement targets
- [ ] All action items have owner, deadline, and verification method
- [ ] Learning shared beyond the immediate team
- [ ] 30-day verification scheduled
