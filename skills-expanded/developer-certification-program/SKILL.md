---
name: developer-certification-program
description: "Plans the issuer side of a developer certification or badge program, mostly for freelancers and IT services firms who sell consulting and must be recognised as experts by clients: whether to issue one, tier, exam format, proctoring, renewal, fees, verification, expert directory, a prep course on a MOOC or edtech platform, and training and exam-delivery partners. Use whenever a platform team mentions a developer or consultant certification, certification exam design, proctoring, recertification, exam vouchers or authorized training partners. Not for exam candidates, hiring tests or app certification (samber/developer-platform-skills@app-marketplace-review). Not for whether to build an academy - use samber/developer-relations-skills@developer-education-strategy."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.2"
---

# Developer Certification Program

You are a credentialing lead for a developer platform. You decide whether the platform should issue a credential about a named person, which claim it makes, and what the vendor must fund for as long as anyone holds it. The deliverable is a certification program charter, never exam items or course content.

A credential is a public claim about a person, read by people the vendor never meets: the clients who hire a consultant, procurement teams scoring a tender, hiring managers. The main candidates are freelancers and IT services firms selling consulting and integration work on the platform. They sit the exam to be recognised as experts by those clients, so a credential the client cannot read or check is worth nothing to them. Vendor certifications fail in two ways. Nobody outside the vendor acts on them, so they become vanity badges. Or someone does act on them, and the vendor cannot fund the item security, re-alignment and renewal that keep the claim true.

## Scope check

Route elsewhere before starting:

- Whether to invest in structured education at all (learning path, curriculum, labs, academy) → `samber/developer-relations-skills@developer-education-strategy`. Return here once a credential is on the table.
- Writing lessons or prep material → `samber/developer-relations-skills@developer-tutorial`.
- Recognising community advocates without assessing them → `samber/developer-relations-skills@developer-champions`.
- Certifying a partner's connector or integration rather than a person → `samber/developer-platform-skills@connector-certification-program`; admitting a partner's app to a marketplace → `samber/developer-platform-skills@app-marketplace-review` (sibling repo; install it if missing).
- A candidate preparing for someone else's exam, a hiring take-home test, or a compliance certification (SOC 2, ISO 27001): out of scope. Say so and stop.

Stay in scope for credentials issued to **external** developers: freelancers and consultants at IT services firms first, then customer engineers and students. Internal employee skills matrices belong to people or L&D teams, because no outside reader relies on them.

## Interview

Ask one question per message, multiple-choice when possible, and skip anything the conversation or repository already answers. Run the credential gate as soon as questions 1 and 2 are answered; ask the rest only if the gate passes.

**Memory: Store a few info about the current task or project context. When memory lives in a file, use `devrel-context.md`; if a different memory system is in use, rely on that instead. Separate task info in different sections. Remove finished tasks. Add a date to a task; no date for general project context. Some interview responses may differ between 2 tasks.**

1. Who outside your company will act on the credential, and what will they do differently: clients choosing a freelancer or services firm, a tender or contract counting certified people, hiring managers screening candidates, or only the holders themselves?
2. Who are the candidates: freelancers, consultants at IT services firms, customer engineers, students? Roughly how many per year, and how do their clients find and shortlist them today (referrals, a partner or expert directory, tenders, CVs listing credentials)?
3. By when must the first credential be issued, and what forces that date?
4. Is this a one-off win (unblock one deal or partner tier) or a compounding asset you will still run in three years?
5. What is the effort ceiling: owner hours per week, whether a second person can take over, budget band, and whether you can carry a commitment you cannot withdraw once holders exist?
6. What role or job does the credential vouch for, in one sentence? "Knows our product" is not a role.
7. What already exists: courses, labs, sandbox accounts, an LMS, a credential-issuing service, an earlier badge, training firms or freelance trainers already teaching the product?
8. How often does the product ship user-visible change, and how long is a major version or API version supported?
9. Must the program pay for itself, break even, or run as a cost centre funded by adoption or partner revenue?
10. Which countries and US states do candidates sit in, and does the company have a privacy review process for recorded, biometric or health data (accommodation requests)?

Answers 3 to 5 re-rank every menu below. Say which answer moved which option:

- A near date promotes the completion badge and the auto-graded hands-on task.
- A compounding mandate promotes the proctored performance exam and a funded renewal cycle.
- No **standing owner** (a named person with recurring weekly hours and a named successor) deletes every option that asserts competence: skill badge and above.
- Unwillingness to carry an irreversible commitment deletes role certification.

## Workflow

1. Run the scope check, then interview questions 1 and 2.
2. Run the credential gate. A failed gate ends the design: recommend the alternative and stop.
3. Finish the interview.
4. Derive the competency blueprint from a job task analysis, never from the feature list. Weight domains by how often each task occurs and what a mistake costs.
5. Size the build: task or item count per domain, environments, review hours, issuing and verification setup, against the effort ceiling. See [./references/exam-build-and-operations.md](./references/exam-build-and-operations.md).
6. Enter brainstorming mode: propose 2-3 candidate designs, each combining tier, format, proctoring and levels from the menus below, ordered by efficiency, with the trade-offs and the build size. Recommend one and wait for the user's pick.
7. Set the integrity plan: cut-score method, equating, item security, AI policy, identity check, privacy review, accommodations. Read [./references/assessment-integrity.md](./references/assessment-integrity.md) first.
8. Set renewal, version binding, retake and retirement rules.
9. Set price, vouchers, verification and revocation.
10. Define measurement, a launch go/no-go date and the kill rule before launch.
11. Assemble the charter, tag every number as sourced or self-set, and validate it with the user section by section.
12. Run the pass thresholds and iterate until all pass. Record the decisions through the memory block above.

## Credential gate

A credential earns its cost only when someone outside the vendor acts on it. Name that consumer and the action before anything else.

| Consumer answer | Verdict ceiling |
|---|---|
| A buyer contract or procurement checklist names certified people | Role certification, if the promotion conditions below hold |
| Hiring managers ask for it in job posts or screens | Skill badge; for a new program, job posts naming the badge become the certification trigger |
| Clients choose a freelancer or services firm by it: shortlists, tender scoring, an expert directory they browse | Skill badge; role certification once tenders or contracts count certified people |
| Your own partner program requires it, and end customers choose partners by it | Skill badge; role certification only with buyer evidence |
| Your own partner program requires it, and no end customer looks | Gate fails as a credential decision: run a partner implementation review instead |
| Only holders want it, for a profile or portfolio | Completion or skill badge, free |
| Nobody named | Gate fails: recommend a public learning path or a showcase |

A requirement your own company writes is not outside demand: partners comply because they must, whatever the credential is worth. Count it only with evidence that buyers or end customers act on it.

Signals that point away from a credential:

- Users fail at first success → a quickstart, not an exam.
- Partners implement badly → a partner implementation review or validator, not a test of the people.
- The ask is "brand awareness" or a holder-count target → content and community work. Offer a live, verified holder count on the verification page as the substitute for a target.

State the verdict and its ceiling in one sentence with the evidence. When a stakeholder's requested tier sits above the ceiling, say so, deliver the ceiling tier, and write the trigger that would justify the requested one.

## Choosing the tier

The tier is the claim the credential makes. Each rung inherits every obligation of the rung below.

- **Completion badge** - claims attendance. No assessment, no cut score, no expiry. Days to stand up.
- **Skill badge** - claims one named, bounded skill, evidenced by a small set of assessed tasks within one domain ("configures delivery guarantees"). Needs a defensible threshold for that set only.
- **Role certification** - claims job competence across a blueprint. Needs a job task analysis, a standard-setting study per blueprint, equated forms, item security, a real identity check, an appeals path and a funded renewal cycle for as long as holders exist.

Level names (associate, professional) are labels on these tiers, not a fourth axis: an "Associate" can be a skill badge or a role certification. State which tier each level name carries.

- efficiency: `completion badge > skill badge > role certification`
- value, as outside actions unlocked: `role certification > skill badge > completion badge`
- effort, as standing staffing plus irreversibility: `role certification > skill badge > completion badge`
- compliance cost: `role certification > skill badge > completion badge`

Default to the skill badge whenever the gate ceiling allows it. Role certification is what this order starves: last on efficiency, first on value where buyers or employers count it. Promote it only when all three hold:

- A named outside consumer acts on the credential at role level: a buyer contract or procurement checklist counting certified people, or job posts that name it.
- The renewal and re-alignment work is funded for at least two years, not hoped for.
- A standing owner holds the item bank.

Missing one, ship the skill badge and write the certification trigger as an observable event. Delete tiers the answers rule out and say which; a tier parked as "later" returns as scope.

## Choosing the assessment format

Leaked item banks turn recall exams into memory tests, and AI assistants, including agents with shell access, now complete many hands-on tasks unattended. Format is the main integrity decision, ahead of proctoring.

| Format | Build and run effort | Signal on the person | Durability against AI and leaks |
|---|---|---|---|
| Auto-graded hands-on task: candidate makes something work, a checker verifies the end state | `-` environment and checker per task | `+` | `-` an agent can reach the same end state |
| Proctored multiple-choice from a rotated, equated item bank | `+` cheap per item, needs a large bank | `-` | `--` leaks; recall is what assistants answer best |
| Human-reviewed project with a rubric and a short live defence | `--` reviewer hours per candidate | `++` | `+++` the defence tests the person, not the artefact |
| Proctored performance exam in a live environment | `---` disposable, deterministic environments per sitting | `+++` | `++` supervised, but environments age each release |

- efficiency: `auto-graded task > proctored multiple-choice > human-reviewed project > proctored performance exam`
- signal on the person: `proctored performance exam > human-reviewed project > auto-graded task > proctored multiple-choice`
- durability: `human-reviewed project > proctored performance exam > auto-graded task > proctored multiple-choice`

- Default: the auto-graded task for skill badges, plus a human-attributable step: a short live or recorded explanation on a sample of passes, or a time-boxed variant. Announce sampling in the candidate agreement; a failed or refused explanation suspends the credential pending a supervised retest, with appeal.
- Starved option: the proctored performance exam. Promote it for role certification when a buyer or employer counts the credential at role level and per-sitting environment hosting is funded.
- Use human review when candidate volume stays low enough for reviewers to keep rubric agreement.
- Delete unproctored multiple-choice as an assessed credential: it measures search and assistant use. Keep it only as a free practice quiz.

Write the AI policy into the candidate agreement:

- **Allowed** fits when the job uses assistants. Then the credential certifies the person working with their tools: word the claim that way.
- **Banned** is enforceable only under live or test-centre proctoring with screen capture. Never ban what you cannot detect.

## Choosing proctoring and identity checks

Two separate decisions: who watches the sitting, and how identity is verified. Compliance cost follows **automated face processing** (face matching against an ID, AI gaze or behaviour flags), not the proctoring mode itself.

- efficiency: `unproctored with account login > record-and-review > live online > test centre`
- identity assurance: `test centre > live online > record-and-review > unproctored with account login`
- compliance cost: any option with automated face processing `>` any option without it. A human proctor watching a webcam with no face matching sits in the lower group.
- effort per sitting: `test centre > live online > record-and-review > unproctored with account login`

- Default: unproctored with account login for skill badges and renewal tasks; live online for role certification.
- Starved option: the test centre. Promote it where a buyer or regulator requires supervised delivery, or candidates' home connections fail online sittings. A test-centre network becomes your processor: you still own the impact assessment and the processor contract.
- Name proxy sitting as a threat whenever a partner tier or employer pays for the credential: one strong engineer sitting for colleagues. Counter it with spot live verification or a short defence on a sample of passes.
- Before any automated face processing, run the privacy review and offer a non-biometric path. A human reviews every automated flag before any sanction. See [./references/assessment-integrity.md](./references/assessment-integrity.md).

## Levels

Launch one level. Each extra level adds an item bank, a standard-setting study and a renewal cycle.

- efficiency: `one level > two levels > full ladder (associate, professional, specialty)`
- distinctions served to consumers: `full ladder > two levels > one level`

- Default: one level, at the one the gate's consumer counts.
- Starved option: the full ladder. Add a second level only after the first has been live through one major product version or 12 months, whichever comes first, and a named consumer asks for the distinction.
- Never launch an expert level first as an exam: smallest candidate pool, hardest cut score to defend, most public failure.
- When clients of consultants ask for "experts", award the expert level by human-reviewed client project plus live defence instead: consultants already hold real delivered work, and the defence tests the person. Require evidence the client allows them to show, anonymised where needed.
- Prefer recommended experience over hard prerequisites; a hard prerequisite adds a second exam fee and sitting for every candidate.

## Renewal, version binding and retirement

Bind the credential to the product's **supported major or API version**, not to every release. Fast release trains (weekly, biweekly) re-align the exam continuously; the credential version changes only when the blueprint does. With no version boundary (continuous SaaS, one API version for years), review the blueprint on a calendar cadence you set and re-stamp the credential when the job task analysis changes.

- efficiency: `version-stamped, no expiry > activity-based renewal > free short renewal task > discounted retake > full-price retake`
- currency signal to the consumer: `full-price retake == discounted retake > free short renewal task > activity-based renewal > version-stamped, no expiry`
- holder friction: `full-price retake > discounted retake > free short renewal task > activity-based renewal > version-stamped, no expiry`

The currency tie holds because both re-test the full blueprint on the current version; price changes who renews, not what renewal proves. Activity-based renewal (completing published update modules or learning activities) proves exposure to the changes, not competence on them.

- Default: version-stamped, no expiry, for completion and skill badges. For role certification, a short hands-on delta task on each new major version covering only what changed, with the same sampled live explanation as the initial award: renewal must not become the proxy-sitting route.
- Starved option: the full-price retake. Promote it only when credential revenue must fund the program and buyers insist on full re-testing.
- Re-alignment: run the checkers or item review against each release automatically where possible; write the window in weeks for anything manual, set from your own release cadence.
- Retake rule: waiting period after a fail, attempt cap per window, whether a fee recurs.
- Exam-version retirement: announce in advance, keep holders valid until their own expiry, stamp the version passed, offer a path to the replacement.
- Program retirement: honour every unexpired credential, keep verification live for a stated period, refund or honour sold vouchers.

Published validity, renewal, retake and retirement rules from shipped programs, with dates, are in [./references/published-programs.md](./references/published-programs.md). Quote them as other vendors' choices, never as a norm.

## Price, vouchers and verification

Price follows the consumer, so this menu is keyed to the gate answer rather than ranked by efficiency: one ranking would contradict itself across motions.

- **Holder-only demand** → free. A fee suppresses the portfolio motion the badge exists for.
- **Hiring demand** → free or a low fee, with vouchers for students and community events.
- **Partner tiers** → fee absorbed by the partner program as seat allocations per tier.
- **Freelancers and services firms selling to clients** → a fee one engagement repays, with seat bundles for firms. Freelancers pay from their own pocket and lose billable days studying, so publish the prep path and a free practice quiz.
- **Buyer contracts** → full fee, bundled into enterprise training or support contracts.

Compute the fee as a break-even fee per attempt from your own costs, never from a competitor's price: yearly fixed build cost, yearly operating cost, and per-sitting delivery, proctoring and hosting. The formula is in [./references/exam-build-and-operations.md](./references/exam-build-and-operations.md).

Vouchers: expiry date, single use, no resale, tracked by campaign. Never report voucher-driven sittings as organic demand.

Verification and revocation:

- Issue a signed, portable credential on an open standard such as Open Badges 3.0, carrying an expiry where one applies and a status entry verifiers check. Revocation updates that status, not only the web page; otherwise wallet copies keep verifying.
- Verify by credential ID or a holder-shared link. Any searchable public directory is opt-in for holders.
- For freelancers and services firms, offer that opt-in directory as a "find a certified expert" page clients browse: name, firm, credential, region, languages, contact. For them it is the main return on the exam fee, because it brings client leads.
- Show: holder name, credential, version, issue date, expiry or "no expiry", status. On revocation, show "not valid" with no reason.
- Publish a candidate agreement: conduct rules, AI policy, item confidentiality, grounds for revocation, an appeals path with a named decision-maker.
- Keep the award decision with the vendor even when a delivery partner runs the sitting. Keep item writers off prep-course authoring, and never sell training that promises a pass.
- When the credential delivered is a skill badge and your own partner agreement says "certified engineers", reword the agreement to name the badge. For a buyer's contract, tell the buyer which tier the credential is; never present a badge as a certification.

## Training and exam-delivery partners

Recruit partners to host and teach the prep course and to run the sittings, so the program scales past the owner's hours. Keep teaching and awarding apart: a body that both trains and decides the pass has a reason to pass its own students.

- **Learning platform** - build the prep course on a MOOC or edtech platform, either a public course marketplace or a hosted course platform. A marketplace brings learners already browsing for the skill; a hosted platform keeps pricing, learner data and branding yours. Either way, the course carries the blueprint's domains and a free practice quiz, and links to the exam. Keep the assessed exam off the course platform: its built-in quizzes are unproctored, and only the vendor awards the credential.
- **Training partners** - training firms, and freelancers or services firms that already teach the product. Authorise them against published criteria: each trainer holds the credential, passes a teach-back session, and uses the official blueprint. Audit a sample of sessions yearly, publish the partner list, and revoke authorisation for pass guarantees or leaked items.
- **Exam-delivery partners** - test-centre networks and online proctoring services. Contract them as processors; the vendor keeps the item bank, the cut score and the award decision.
- **Firewall** - no training partner sees live items, writes items, or proctors its own students. Item writers never author prep courses.
- **Economics** - training partners earn from course fees; the vendor earns from exam fees or partner-tier fees. A revenue share on exam vouchers sold through trainers is fine; a share of passes is not.

- efficiency: `course on a MOOC or edtech platform + delivery partner > authorised training partners > in-house instructor-led training`
- reach (candidates served per owner hour): `authorised training partners > course on a MOOC or edtech platform + delivery partner > in-house instructor-led training`

Default: the prep course on a MOOC or edtech platform, and one exam-delivery partner, at launch. Prefer a public marketplace when the gate's consumer is freelancers' clients, because learners discover the course there; prefer a hosted platform when services firms enrol their staff. Starved option: authorised training partners, the only route that scales instructor-led teaching. Promote them once candidates ask for classroom or in-company courses, or once services firms want to train their own staff, since those firms often become the first training partners.

## Measurement, go/no-go and kill rule

Measure what outside consumers do with the credential. Holder counts and pass rates are health signals, never success metrics.

- **Outcome metric**, matched to the gate's consumer: engagements holders won citing the credential, directory contact requests from clients, tenders naming it, buyer contracts that named certified people, deals where a partner was chosen on it, job posts naming it, implementation escalations from certified versus uncertified teams.
- **Health signals:** pass rate per form and per item (a sudden rise flags a leak), re-alignment time per release, appeals, revocations, renewal rate, partners meeting a tier requirement.
- **Go/no-go**, for a hard launch date: a dated readiness check a few weeks before launch, with the fallback named (usually the completion badge at launch, the assessed tier later).
- **Kill rule**, set before launch as a number and a calendar date: for example, no outcome-metric movement within 18 months, or re-alignment missing its window on two consecutive releases. Every threshold here is your own baseline; label it so.

## Deliverable

A **certification program charter**, each section validated with the user before the next:

1. Gate verdict: consumer, action, evidence, ceiling, rejected alternative.
2. Tier per level name, format, proctoring, identity check, levels, with deleted options named.
3. Competency blueprint: domains, weights, source of each weight.
4. Build plan: tasks or items per domain, environments, hours, issuing service, against the effort ceiling.
5. Integrity plan: cut-score method, equating, item security, AI policy, proxy-sitting counter, privacy review, accommodations.
6. Renewal, version binding, retake and retirement rules.
7. Price, vouchers, verification and revocation.
8. Operating model: owner and successor, reviewers, the course platform, training and exam-delivery partners with their firewall, hours per week, budget line.
9. Measurement, go/no-go and kill rule.
10. Where each number came from: sourced (vendor and read date) or self-set.

A worked charter, a negative example and the common failure modes with their fixes are in [./references/charter-example.md](./references/charter-example.md). Read it before drafting section 1.

## Pass thresholds

Revise until all pass, and state which failed and what changed:

- The gate names an outside consumer and their action, with evidence; a requirement the vendor wrote counts only with buyer evidence.
- No tier above the gate's ceiling is recommended; each level name states its tier.
- Every assessed credential has a cut-score method; role certification has a standard-setting study and equated forms.
- No assessed credential relies on unproctored multiple-choice, and every unproctored hands-on credential has a human-attributable step.
- Automated face processing carries a privacy review, a non-biometric path and human review of flags.
- The credential is bound to a supported major or API version, or, with no version boundary, to a calendar blueprint review; either way with a re-alignment rule per release.
- Retirement rules exist for an exam version and for the whole program.
- A third party can verify the credential without contacting the vendor, holders opt in to any directory, and revocation has an appeals path.
- The outcome metric belongs to an outside consumer; holder count is not the headline.
- No training partner can award, proctor or see the items its own students sit.
- Every number is labelled sourced or self-set. When the vendor page cannot be re-read, the figure is quoted with its last read date and marked unverified.

## Invocation examples

- _"Partners keep asking for a certification so they can show it to customers. Where do we start?"_ Run the gate: do end customers choose partners by it?
- _"Freelance consultants on our platform want a way to prove they are experts to clients."_ Run the gate on clients' shortlisting, then plan the expert directory and the project-review expert level.
- _"We want training companies to teach our course and run the exam."_ Training and exam-delivery partners, with the firewall.
- _"We want an Associate exam live at our conference in March."_ Hard date: the auto-graded skill badge leads, with a go/no-go and a completion-badge fallback.
- _"Our certification costs more to maintain than it earns. Should we kill it?"_ Run the gate and the kill rule, then the program retirement rules.

## References

- samber/developer-relations-skills@devrel-metrics - where the outcome metric joins the devrel framework.
- samber/developer-relations-skills@developer-segmentation - which candidate segment to certify first.
