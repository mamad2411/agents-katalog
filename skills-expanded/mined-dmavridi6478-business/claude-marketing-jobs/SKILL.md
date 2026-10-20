---
name: claude-marketing-jobs
description: Library of 50 named, single-output marketing jobs across 10 functions (strategy, ICP, offers, content, search, social, email, paid, analytics, agencies), each with a copy-paste prompt and one defined deliverable, organised under the 11-chapter "Complete Claude Marketing Guide 2026" structure. Every job reads the five operating-system context files in docs/marketing-context/ first. Use when the user asks for a specific marketing job by name ("run Ten Ranked Fixes", "do an Unevidenced Claim Check", "Five Angle Variants"), wants to know which marketing job fits a problem, or wants a full-function marketing run. Specialist layer of `governed-marketing-team`; run via `/marketing-job`.
---

# Claude Marketing Jobs (50 jobs · 10 functions · 11 chapters)

Sources (uploaded, both by prosp — the same author as the "Governed Marketing
Team" infographic already in `governed-marketing-team`):
- "Claude Team for MARKETING — 50 marketing jobs. One complete Claude team." (CEO → Claude as Head of Marketing reading "the five operating system files" → 10 functions × 5 jobs).
- "The Complete Claude Marketing Guide 2026 — eleven chapters, 50 prompts, 25 templates, 20 workflows and 10 audits."

**[Certain]** the job names, chapter names and "what you get" column are transcribed from the images.
**[Guessing]** the prompt wording for each job: the actual guide is gated behind "comment MARKETING", so these prompts are reconstructed from each job's name and its chapter's stated purpose. They are written to be useful, not to match prosp's text.

## Always first
Every job reads `docs/marketing-context/` (voice, proof, pillars, banned, last-quarter) — the five operating-system files. Missing file → stop and name it (gate G3 in `governed-marketing-team`). Every output goes through the `brand-reviewer` agent before a human sees it as final.

## The 11 chapters → what you get

| Ch | Name | What it does | Deliverable | Jobs |
|---|---|---|---|---|
| 1 | Marketing strategy | The one number to move this quarter, and the channel to stop | A number, X to Y | Strategy 1–5 |
| 2 | Market & customer research | Twelve verbatim buyer phrases and the honest competitor read | 12 real phrases | Strategy 2–4, ICP 5 |
| 3 | ICP & positioning | ICP derived from closed-won, and who it deliberately repels | A filter string | ICP 1–4 |
| 4 | Brand, messaging & offers | Offer spec and three-pillar message hierarchy | One offer page | Offers 1–5 |
| 5 | Content strategy & production | Three pillars, five hooks per piece, the AI-tell strip | A pillar set | Content 1–5 |
| 6 | SEO, AEO & AI search | Ten ranked fixes and one verdict per URL | A fix list | Search 1–5 |
| 7 | Social media & LinkedIn | Velocity scanning, scored comments, delivery maths | A posting plan | Social 1–5 |
| 8 | Email, lifecycle & CRM | Trigger, exit, deliverability thresholds | A flow map | Email 1–5 |
| 9 | Paid ads & CRO | Five angle variants, one job per landing page | A variant set | Paid 1–5 |
| 10 | Analytics & automation | Diagnostic chain, stopped at the first failure | One change | Analytics 1–5 |
| 11 | Running it across clients | Client ICPs, voice files, margin ranked worst first | A margin ranking | Agencies 1–5 |

## The 50 jobs

Replace `[ ]` inputs. Each prompt ends with the deliverable in bold.

### Strategy
| Job | Prompt |
|---|---|
| One Number To Move | From last-quarter.md, pick the single metric whose movement most changes revenue this quarter. State current value X, target Y, and the one channel we stop to fund it. **Output: "Metric: X → Y by [date]; stop: [channel]".** |
| Twelve Buyer Phrases | From these call transcripts/reviews/tickets [paste], extract 12 verbatim phrases buyers use for the problem. No paraphrase. Tag each: pain, outcome, objection, trigger. **Output: 12 quoted phrases with source.** |
| Honest Competitor Gaps | For [competitors], list where each genuinely beats us and where they are weak, citing public evidence only. **Output: table — competitor, their real advantage, their gap, our response.** |
| Unfiltered Ticket Read | Read these support tickets [paste] and tell me the 5 problems customers actually have, ranked by frequency, without softening. **Output: ranked list with counts and one quote each.** |
| Two Contrarian Beliefs | Propose two beliefs we hold that most of our market disagrees with, each backed by a proof row. **Output: 2 beliefs + proof ID + the post each would anchor.** |

### ICP
| Job | Prompt |
|---|---|
| Closed-Won Attributes | From these closed-won deals [paste CRM export], find the attributes shared by ≥ 70 %. Ignore attributes also common in closed-lost. **Output: attribute list with % won vs % lost.** |
| Signer Title Gap | Compare who signs the contract vs who we currently target. **Output: title we target, title that signs, the gap, the fix.** |
| Positioning Line | Write one positioning line: For [ICP] who [trigger], [product] is the [category] that [outcome], unlike [alternative]. Give 3 options scored for specificity. **Output: 1 recommended line.** |
| Six Disqualifiers | List six attributes that mean a prospect should NOT be pursued, from closed-lost and churn data. **Output: filter string usable in a CRM/prospecting tool.** |
| Problem-Based Segments | Segment the market by the problem being solved, not firmographics. **Output: 3–5 segments with trigger, pain phrase, size estimate (marked as estimate).** |

### Offers
| Job | Prompt |
|---|---|
| Offer Spec | Write the offer spec: who, problem, outcome, mechanism, deliverables, timeline, price logic, guarantee, proof rows used. **Output: one-page offer spec.** |
| Message Hierarchy | Build a three-pillar message hierarchy: one umbrella promise, three pillars, three proof points each (proof IDs only). **Output: hierarchy table.** |
| Contents Inventory | Inventory every asset we already have per pillar and funnel stage. **Output: matrix with gaps marked.** |
| Angle Lever Pick | For this offer, score the 8 persuasion levers (`marketing-psychology`) for fit and pick the single strongest. **Output: lever + why + one headline using it.** |
| Unevidenced Claim Check | Scan this copy [paste]. List every claim with no row in proof.md. **Output: claim → missing evidence → rewrite or delete.** |

### Content
| Job | Prompt |
|---|---|
| Three Content Pillars | Propose three content pillars tied to the message hierarchy and buyer phrases. **Output: pillar set with weighting and example titles.** |
| Long Asset Splitter | Split this long asset [paste] into 10 channel-native pieces without new claims. **Output: list with channel, format, hook, source paragraph.** |
| Five Hook Test | Write five hooks for this piece using different mechanisms (question, number, contrarian, story, specificity) and rank them. **Output: 5 hooks, ranked with reason.** |
| AI Tell Stripper | Remove AI tells from this draft (em-dash chains, "delve", triplets, hedges, generic openers) while keeping voice.md rules. **Output: clean draft + list of what was stripped.** |
| Transcript POV Finder | From this transcript [paste], extract the three strongest points of view the speaker holds. **Output: 3 POVs with quotes and post angle.** |

### Search
| Job | Prompt |
|---|---|
| Ten Ranked Fixes | Audit [URL/site] for SEO, AEO and AI-search readiness. Rank the ten fixes by impact ÷ effort. **Output: fix list 1–10.** |
| First Party Words | List terms only we can credibly own (proprietary data, method names, local terms). **Output: term list + page each belongs on.** |
| Passage Claim Split | Rewrite this page into self-contained passages, each answering one question with one claim and its proof. **Output: passage list ready for AI citation.** |
| Keep Refresh Kill | For each URL in [list + traffic data], give one verdict: keep, refresh or kill, with reason. **Output: verdict per URL.** |
| Content Brief | Write an SEO/AEO brief for [topic]: intent, questions to answer, entities, sources, structure, internal links. **Output: brief.** |

### Social
| Job | Prompt |
|---|---|
| Velocity Post Scan | From these posts with timestamps and first-hour engagement [paste], identify which formats gain velocity fastest. **Output: format ranking with first-hour medians.** |
| Five Comment Set | Write five substantive comments for these target accounts' posts [paste] that add a point, not praise. **Output: 5 comments.** |
| Comment Scorer | Score these comments on our posts for buying intent (0–3). **Output: ranked list + suggested reply for 2–3.** |
| Lead Magnet Post | Write a LinkedIn post offering [asset] with a comment CTA, following voice.md. **Output: post + DM follow-up text.** |
| Delivery Capacity Maths | Given [hours/week] and [channels], calculate sustainable posts/week and what to drop. **Output: posting plan with the maths shown.** |

### Email
| Job | Prompt |
|---|---|
| Missing Flow Check | Compare our live email flows to the standard set (welcome, nurture, post-purchase, win-back, re-engagement). **Output: missing flows ranked by revenue impact.** |
| Trigger And Exit | For [flow], define the entry trigger, exit condition and suppression rules. **Output: flow map.** |
| Five Email Set | Write a five-email sequence for [flow] with one job per email. **Output: 5 emails with subject, preview, body, CTA.** |
| Deliverability Check | Review these metrics [paste] against thresholds: spam complaints < 0.1 %, bounces < 2 %, SPF/DKIM/DMARC aligned. **Output: pass/fail per threshold + fix.** |
| Downloaded Never Bought | Design a sequence for people who downloaded [asset] but never bought. **Output: 3-email flow + segment definition.** |

### Paid
| Job | Prompt |
|---|---|
| Five Angle Variants | Write five ad variants for [offer], each on a different angle (pain, outcome, proof, objection, contrarian). **Output: variant set with headline, body, CTA.** |
| One Job Audit | Audit [landing page URL] — does it do exactly one job? List every element competing with the primary CTA. **Output: remove/keep list.** |
| Exit Counter | Write the counter to the top 3 reasons visitors leave [page], from heatmap/survey data [paste]. **Output: 3 objection-answer blocks.** |
| Fatigue Evidence | From ad data [paste], identify fatigued creatives (frequency ↑, CTR ↓ over 7 days). **Output: list with evidence + replace/rest call.** |
| Single Biggest Change | Name the single change to this campaign that would most move CPA. **Output: one change + expected direction + how to test.** |

### Analytics
| Job | Prompt |
|---|---|
| Metric With A Decision | For each dashboard metric, name the decision it drives. Remove metrics with none. **Output: kept metrics + decision each.** |
| Diagnostic Chain | Walk the funnel impressions → clicks → leads → SQL → won and stop at the first stage below benchmark. **Output: the failing stage + one change.** |
| Source Tagging Rule | Write a UTM and source-tagging rule set that makes attribution possible. **Output: naming convention + validation rules.** |
| Conversations Not Reach | Re-report this month's social results as conversations started, not reach. **Output: conversation count by channel + trend.** |
| One Change A Month | From all findings this month, pick the one change to implement next month. **Output: one change, owner, success metric.** |

### Agencies (running it across clients)
| Job | Prompt |
|---|---|
| Client ICP Derivation | Run Closed-Won Attributes for [client] from their CRM export. **Output: client ICP filter string.** |
| Client Voice File | Build voice.md for [client] from 10 approved pieces. **Output: filled voice file.** |
| Margin Per Client | From hours and fees [paste], compute margin per client. **Output: margin ranking, worst first.** |
| List Overlap Check | Check prospect list overlap between clients [lists] to avoid conflicts. **Output: overlap report.** |
| Cadence Pushback | Draft the email pushing back on a client's unrealistic cadence, using Delivery Capacity Maths. **Output: email.** |

## Honest limits
- 50 jobs is a menu, not a to-do list. Run the Strategy jobs first; most teams need 8–10 of these, not 50.
- "Ready on demand" (on the graphic) assumes the context files are filled. With empty files every job produces generic output.
- Jobs that need data (Closed-Won, Velocity, Fatigue, Margin) must be given real exports. Never let the model estimate the data itself.
