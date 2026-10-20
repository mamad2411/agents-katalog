---
name: incident-communication
version: 1.0.0
min_mindforge_version: 10.3.0
status: stable
triggers: incident communication, war room coordination, customer incident message, postmortem facilitation, blameless culture, incident status page, outage communication, stakeholder notification incident, incident timeline, root cause communication, severity classification, incident bridge
compose:
  - incident-management
---

# Incident Communication

## When this skill activates

This skill activates during production incidents when coordinating war rooms, writing customer-facing incident messages, updating status pages, communicating to stakeholders, facilitating postmortems, or establishing blameless culture. It applies to on-call engineers, incident commanders, and engineering managers responsible for incident response and communication.

## Mandatory actions when this skill is active

### Before incident communication begins

1. **Classify severity immediately** — SEV1 (business-critical service down), SEV2 (degraded performance, partial outage), SEV3 (minor issue, workaround available), SEV4 (cosmetic issue, no user impact). Severity determines communication cadence and escalation.
2. **Assign roles explicitly** — Incident Commander (coordinates response), Communications Lead (stakeholder updates), Tech Lead (drives technical resolution), Scribe (documents timeline). Ambiguous roles cause chaos.
3. **Establish communication channels** — War room (Slack/Teams/Zoom for internal), status page (for customers), stakeholder channel (for execs/product). Don't mix internal and external comms.
4. **Start the incident timeline immediately** — Document: when did it start, when was it detected, who's working on it, what's been tried, what's the current status. Real-time notes prevent memory loss.

### During incident response

#### War Room Coordination

- **Run structured check-ins every 15-30 minutes** — Incident Commander asks: (1) What's the current status? (2) What are we trying next? (3) Do we need more people? Prevents chaos and ensures everyone is aligned.
- **Use threaded communication** — Main channel for status updates only. Threads for technical debugging. Don't pollute the main channel with noisy debugging logs.
- **Limit the war room to essential people** — Too many cooks slow resolution. Core team: 3-5 people. Observers can follow in a read-only channel.
- **Escalate when stuck** — If the team is stuck for >30 minutes, escalate. Call in the architect, the team that owns the upstream service, or the engineer who built the system. Ego has no place in incidents.
- **Declare resolution criteria upfront** — What does "fixed" mean? Service is healthy? All users can transact? Error rate below threshold? Prevents premature "all clear" declarations.

#### Customer-Facing Communication

- **Acknowledge fast, diagnose later** — Within 15 minutes of detection, post to status page: "We are investigating reports of [service] being unavailable. Updates to follow." Don't wait for root cause.
- **Use the 3-part update structure** — (1) Current status (what's broken), (2) Customer impact (what can't they do), (3) Next steps (when's the next update). No jargon, no excuses.
- **Update cadence by severity** — SEV1: every 30 minutes. SEV2: every 60 minutes. SEV3: every 2 hours. Customers hate silence more than bad news.
- **Avoid over-promising** — Don't say "Fixed in 10 minutes" if you're unsure. Say "Actively working on resolution. Next update in 30 minutes."
- **Post resolution message** — Once resolved, post: what broke, how long it lasted, how many users were impacted, what we did to fix it, what we're doing to prevent recurrence. Transparency builds trust.

#### Stakeholder Notification

- **Notify executives immediately for SEV1** — Execs need to know ASAP, especially if customers are complaining or revenue is impacted. One-line summary: "Service X is down. Y% of users impacted. We're on it."
- **Use BLUF (Bottom Line Up Front)** — Don't bury the lede. "The payment service is down" comes before "We suspect a database connection pool exhaustion."
- **Provide ETA cautiously** — If you estimate 2 hours to fix, tell stakeholders 3-4 hours. Better to resolve early than overpromise and underdeliver.
- **Summarize after resolution** — Once the incident is resolved, send a concise executive summary: what broke, how long, customer impact, resolution, next steps. Save the detailed RCA for the postmortem.

#### Incident Timeline Documentation

- **Scribe logs everything in real-time** — Timestamp every key event: detection, escalation, hypothesis tested, mitigation applied, resolution. Future-you will thank present-you.
- **Capture decisions and reasoning** — Don't just log "Rolled back to v1.3." Log "Rolled back to v1.3 because v1.4 introduced N+1 query causing DB saturation."
- **Include dead ends** — Document failed attempts: "Restarted service at 10:15am. Did not resolve issue." Prevents repeating failed approaches.
- **Link to relevant artifacts** — Logs, dashboards, PRs, alerts. Timeline should be a navigation hub, not a standalone document.

#### Root Cause Communication

- **Distinguish proximate cause from root cause** — Proximate: "The database ran out of connections." Root: "We didn't set a connection pool limit, so a spike in traffic exhausted connections." Root cause prevents recurrence.
- **Use the Five Whys** — Why did X happen? Because Y. Why did Y happen? Because Z. Repeat 5 times until you reach the systemic failure, not the surface symptom.
- **Avoid blame in RCA communication** — Don't say "Engineer A deployed bad code." Say "A deployment bypassed our automated testing due to a gap in CI pipeline." Focus on systems, not individuals.
- **Define prevention actions** — Every RCA must end with: what are we doing to prevent this from happening again? Action items with owners and deadlines.

#### Blameless Culture

- **Assume good intent** — Engineers don't cause incidents on purpose. Treat incidents as learning opportunities, not witch hunts.
- **Focus on systems, not people** — If one engineer's mistake caused an outage, the real failure is the system that allowed a single mistake to cascade. Fix the system.
- **Celebrate transparency** — When someone admits a mistake, praise their honesty. If people fear punishment, they hide mistakes until they explode.
- **Conduct blameless postmortems** — Postmortem facilitator enforces: no blame, no naming individuals (unless volunteering credit), focus on system improvements. If someone says "X person messed up," redirect: "What system gap allowed this to happen?"

#### Postmortem Facilitation

- **Schedule postmortem within 3-5 days** — Too soon: emotions are high, data is incomplete. Too late: memory fades, urgency disappears.
- **Invite all incident responders + key stakeholders** — Engineers who responded, on-call rotation, product/exec if customer-facing.
- **Use a structured template** — Summary, Timeline, Root Cause Analysis, What Went Well, What Went Poorly, Action Items (with owners and deadlines). Don't free-form it.
- **Timebox to 1 hour** — Longer meetings lose focus. If you can't cover it in 1 hour, schedule a follow-up.
- **Publish postmortem widely** — Share in engineering all-hands, team wikis, or public blog (if appropriate). Transparency accelerates learning across the org.

### After incident resolution

- **Close the loop with customers** — If customers were impacted, follow up: apologize, explain what broke, what you're doing to prevent recurrence. Consider service credits if appropriate.
- **Track action items to completion** — 70% of postmortem action items don't get done. Assign a DRI (Directly Responsible Individual) and review progress in sprint planning.
- **Measure incident response effectiveness** — Track: detection time, resolution time, communication cadence, customer satisfaction. Improve the metrics that matter.
- **Update runbooks** — Every incident reveals gaps in runbooks. After resolution, update the runbook so future responders have better context.

## Self-check before task completion

- [ ] Severity is classified (SEV1-4) and roles are assigned (IC, Comms Lead, Tech Lead, Scribe)
- [ ] War room check-ins happen every 15-30 minutes with structured updates
- [ ] Customer-facing communication acknowledges the issue within 15 minutes
- [ ] Status page updates use 3-part structure (status, impact, next steps) with no jargon
- [ ] Incident timeline is documented in real-time with timestamps and decisions
- [ ] Root cause distinguishes proximate cause from systemic root cause
- [ ] Postmortem is scheduled within 3-5 days and uses blameless facilitation
- [ ] Action items from postmortem have owners, deadlines, and are tracked to completion
