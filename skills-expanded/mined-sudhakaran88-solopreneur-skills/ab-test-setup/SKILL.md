---
name: ab-test-setup
description: When the user wants to plan, design, or implement an A/B test or experiment. Also trigger on "A/B test", "split test", "experiment", "test this change", "variant", "multivariate test", "hypothesis", "conversion test", "statistical significance". Also use when deciding BETWEEN testing and qualitative research for low-traffic sites.
metadata:
  version: 1.0.0
  author: Sudhakar
  license: MIT
---

You are a CRO experimentation expert helping solopreneurs run tests that actually mean something — starting with whether A/B testing is even the right tool for their traffic level.

---

## 1. When to Use (and When NOT To)

**Use this skill when:**
- Planning a conversion experiment on a landing page, pricing page, onboarding flow, or email
- Deciding what to change and whether data can actually validate it
- Choosing between A/B testing and faster qualitative methods
- Interpreting test results and deciding what to ship

**Do NOT run an A/B test when:**
- You have fewer than ~1,000 conversions per variant available in the test window
- The change is low-risk and directionally obvious — just ship it
- You're testing tiny cosmetic changes (button color, font weight) with <50k monthly visitors
- You need an answer in less than one full business cycle (typically 2–4 weeks)
- Your gut + 5 user interviews would be faster and just as valid

---

## 2. Check for Context First

Before doing anything, check for:
- `solopreneur-context.md` — product, audience, traffic, goals
- `product-marketing-context.md` — offer, positioning, conversion funnel

If neither exists, ask:
1. How many monthly visitors does the page get?
2. What is the current conversion rate on the target action?
3. What is the primary conversion goal (signup, purchase, trial, demo)?
4. Which page or flow do you want to test?
5. What change are you considering — and why do you think it will help?

---

## 3. The Honest Traffic Check

**Most solopreneurs cannot run statistically valid A/B tests. This is not an opinion — it's math.**

Here is the reality:

| Monthly Visitors | Baseline Conv. Rate | Conversions/Month | Can You A/B Test? |
|---|---|---|---|
| 2,000 | 3% | 60 | No |
| 5,000 | 3% | 150 | No |
| 10,000 | 3% | 300 | Barely (6+ months) |
| 20,000 | 3% | 600 | Maybe (2–3 months) |
| 50,000 | 3% | 1,500 | Yes |

**The rule of thumb:** You need roughly **1,000 conversions per variant** to detect a meaningful lift (>10% relative improvement) at 80% power, 95% confidence. That means 2,000 total conversions for a standard A vs B test.

Peep Laja (CXL) recommends a minimum of 250–350 conversions per variation before calling a result. Below that, your "winner" is coin-flip noise.

**The test duration problem:** Never run a test shorter than two full business cycles (typically 2–4 weeks minimum). Day-of-week effects, seasonal patterns, and novelty bias will invalidate a 5-day test every time.

**If you're below threshold:** Skip to Section 5 (qualitative alternatives). Come back to A/B testing when you've grown.

---

## 4. Sample Size Calculator Guidance

Use a sample size calculator **before** starting any test. Good free options:
- [Optimizely Sample Size Calculator](https://www.optimizely.com/sample-size-calculator/)
- [Evan Miller's Calculator](https://www.evanmiller.org/ab-testing/sample-size.html)

**Inputs you need:**
- **Baseline conversion rate** — your current rate, not a guess
- **Minimum Detectable Effect (MDE)** — the smallest lift worth acting on (e.g., 10% relative = 3% → 3.3%)
- **Statistical power** — use 80% (standard)
- **Significance level** — use 95% (p < 0.05)

**Key insight:** Count conversions, not visitors. A page with 10,000 visitors/month but a 0.5% conversion rate gives you only 50 conversions/month. You would need 20+ months to complete that test. Don't start it.

**MDE reality check:** Testing for a 5% relative lift requires roughly 4x more traffic than testing for a 20% lift. With low traffic, only test changes bold enough to move the needle by 20%+.

---

## 5. If You CAN'T Test: Qualitative Alternatives for <10k Visitors/Month

These are not consolation prizes. For most solopreneurs at early stages, qualitative research delivers better ROI per hour than failed A/B tests.

### User Testing (highest ROI)
- 5 user interviews will surface ~85% of usability problems
- Ask: "Walk me through what you'd do on this page." Watch where they hesitate
- Tools: Lyssna, Maze, or just a Zoom call with screen share
- Cost: $0–$50 per session, often done with existing users

### Session Replay
- Watch real users struggle, rage-click, or abandon
- Tools: Microsoft Clarity (free, unlimited), PostHog (free tier), Hotjar (limited free)
- Look for: rage clicks, dead clicks, unexpected scroll stops, form abandonment

### Heatmaps & Scroll Maps
- Scroll maps show where users stop reading — everything below is invisible
- Click maps show what gets attention vs what gets ignored
- Tools: Microsoft Clarity (free), Crazy Egg, Mouseflow

### Exit-Intent Surveys
- One question on exit: "What stopped you from signing up today?"
- Tools: Hotjar, Tally, or a simple Typeform popup
- 50 responses will reveal patterns faster than 3 months of A/B testing

### 5-Second Test
- Show users your page for 5 seconds. Ask: "What is this? Who is it for?"
- Brutal but effective for diagnosing value proposition clarity
- Tool: Lyssna (free tier available)

### Direct Customer Interviews
- Ask churned users: "What almost stopped you from signing up?"
- Ask active users: "What made you trust us enough to pay?"
- Their words become your copy hypotheses

**Use qualitative findings to generate hypotheses. Then A/B test those hypotheses once you have the traffic.**

---

## 6. If You CAN Test: Hypothesis Framework

Every test needs a proper hypothesis. Without one, you're decorating, not optimizing.

**The format:**

> **Observation:** [What you noticed in data or research]
> **Hypothesis:** We believe that [specific change] will [expected outcome]
> **Prediction:** We will see [metric] increase by [X%] among [audience segment]
> **Rationale:** Because [psychological or behavioral reason]

**Example:**

> **Observation:** Session replay shows 60% of visitors don't scroll past the hero section. The CTA is below the fold on mobile.
> **Hypothesis:** Moving the primary CTA above the fold on mobile will increase mobile signups.
> **Prediction:** Mobile conversion rate will increase by 15%+ within 4 weeks.
> **Rationale:** Users don't know there's an action to take if they can't see it without scrolling.

A vague hypothesis ("let's test a different headline") produces uninterpretable results even when you win.

---

## 7. Test Priority Matrix

Not everything is worth testing. Score your ideas on two axes:

| | High Impact | Low Impact |
|---|---|---|
| **Easy to implement** | Test first | Quick wins — just ship |
| **Hard to implement** | Test second (prioritize) | Skip |

**Highest-impact test locations for solopreneurs:**
1. Hero headline and subheadline (value proposition clarity)
2. Primary CTA — copy, color, placement
3. Pricing page layout and anchoring
4. Signup/checkout flow friction points
5. Social proof placement and type

**Lowest-impact (don't waste tests here at low traffic):**
- Background image variations
- Button color alone
- Footer copy
- Icon choices

---

## 8. Statistical Concepts in Plain English

**Statistical Significance (p-value)**
The probability that your result happened by chance. p < 0.05 means there's less than a 5% chance the difference is random noise. This is not proof — it's a threshold for action.

**Confidence Level**
95% confidence = if you ran this test 100 times, 95 of them would show the same direction. The standard. Some teams use 90% for lower-risk decisions.

**Statistical Power**
The ability to detect a real effect when it exists. 80% power means a 20% chance of missing a real winner (Type II error). Increase power by increasing sample size.

**Type I Error (False Positive)**
You declare a winner that isn't actually better. More likely when: sample size is too small, you peek at results early, or you run many simultaneous tests. Also called alpha error.

**Type II Error (False Negative)**
You miss a real winner and call the test inconclusive. More likely when: sample size is too small or MDE is set too small. Also called beta error.

**Minimum Detectable Effect (MDE)**
The smallest lift your test is designed to detect. Smaller MDE = more traffic needed. Set your MDE based on what lift would actually matter to your business, not what you hope to see.

**Novelty Effect**
Early test results are often inflated because users notice something different and engage more. Always run tests for at least 2 full business cycles before calling results, regardless of sample size milestones.

---

## 9. Bayesian vs Frequentist: The Pragmatic Take

**Frequentist (traditional):** Set a fixed sample size before starting. Do not look at results until done. Call a winner only when p < 0.05. Rigid but well-understood.

**Bayesian:** Express results as "Probability that B beats A." Updates continuously as data arrives. More intuitive for business decisions. Still affected by early stopping — Bayesian is NOT immune to the peeking problem.

**Sequential Testing:** A middle path. Uses alpha-spending to allow controlled interim looks without inflating Type I error. Tools like Statsig and AB Tasty use this. Good for solopreneurs who can't resist checking results.

**Practical recommendation for solopreneurs:**
- Use **PostHog or GrowthBook** — both handle statistics automatically
- If you're using a tool with Bayesian output, treat 95% probability to beat baseline as your threshold, not 80%
- Don't obsess over the statistical religion — obsess over running enough volume

---

## 10. The Peeking Problem and Minimum Run Duration

**Peeking** = checking results before your pre-set sample size is reached and stopping early when you see significance.

Why it's fatal: The p-value fluctuates randomly throughout a test. If you check daily and stop when it hits 0.05, you will find false positives far more than 5% of the time. Studies show peeking can inflate false positive rates to 25–40%.

**Rules to avoid peeking failures:**
- Set your required sample size before launch
- Set a hard end date before launch
- Do not look at results until both are met (or use sequential testing)
- If you must peek: use a sequential testing framework (Statsig, Eppo, AB Tasty)

**Minimum run duration rules:**
- Never less than 7 days (to capture weekend/weekday behavior)
- Ideally 14–28 days (two full business cycles)
- Stop early only with sequential testing tools, never manually

---

## 11. Tools for Solopreneurs

### Free / Open Source
| Tool | Best For | Cost |
|---|---|---|
| **GrowthBook** | Engineering teams, feature flags + stats | Free (self-host or cloud) |
| **PostHog** | All-in-one: analytics + A/B + session replay | Free up to 1M events/mo |
| **Microsoft Clarity** | Heatmaps + session replay only | Free, unlimited |

### Paid (Worth It at Scale)
| Tool | Best For | Starting Price |
|---|---|---|
| **VWO** | Visual editor, no-code A/B testing | ~$199/mo |
| **AB Tasty** | Sequential testing, enterprise features | ~$300/mo |
| **Statsig** | Data warehouse native, rigorous stats | Free tier, then usage-based |
| **Convert** | Privacy-focused, strong stats engine | ~$199/mo |

### Dead / Avoid
- **Google Optimize** — shut down in September 2023. Do not use.
- **Optimizely** — enterprise pricing, not solopreneur-friendly

**Recommendation for most solopreneurs:**
Start with PostHog (free). It handles analytics, session replay, feature flags, and A/B testing in one platform. Upgrade to VWO or AB Tasty if you need a visual editor and have consistent 20k+ monthly visitors.

---

## 12. Interpreting Results

**A "win" is not a win until:**
- Sample size target was reached
- Test ran for at least 2 business cycles
- The winning variant was implemented and held its lift for 2+ weeks post-launch
- You've checked for novelty effect decay

**What to check after declaring a winner:**
1. **Segment analysis** — Did the variant win for all users or just mobile? Just new visitors? A global winner might be a loser for your best segment.
2. **Secondary metrics** — Did the signup rate increase but 30-day retention drop? Optimize for the metric that matters, not the one you measured.
3. **Novelty effect** — Run the winner in production for 2 weeks and check if the lift holds before celebrating.
4. **Sample ratio mismatch** — Did traffic split exactly 50/50? If not, something went wrong with your implementation.

**Inconclusive results are valid outcomes.** They mean the change doesn't matter enough to detect, not that testing failed. File it, document the hypothesis, and move on.

---

## 13. Common Mistakes

**Mistake 1: Stopping when it "looks significant"**
Peeking and early stopping is the #1 cause of false wins. Set the sample size and end date before launch.

**Mistake 2: Testing too many things at once**
Multivariate tests require exponentially more traffic. A 3-variable MVT with 2 options each needs 8x the traffic of a simple A/B test.

**Mistake 3: Testing insignificant changes**
A font size tweak or image swap will never move the needle enough to measure with limited traffic. Test bold, meaningful changes.

**Mistake 4: Running tests for arbitrary durations**
"I'll run it for a week" is not a plan. Calculate required sample size first. Duration follows from traffic, not calendar preference.

**Mistake 5: Not controlling for external factors**
Running a test during a product launch, PR spike, or holiday will contaminate results. Check your traffic sources and time tests during stable periods.

**Mistake 6: Ignoring the losing variant**
The "loser" often contains the most useful insight. Analyze why it underperformed — that's your next hypothesis.

**Mistake 7: No hypothesis, just a change**
Testing "what happens if I change the headline" without a WHY means you can't learn from the result even when it's statistically clean.

---

## 14. Contrarian Takes

**Most CRO doesn't require A/B testing.**
If your value proposition is unclear, fix the positioning. If your onboarding is broken, fix the UX. These are diagnosable without statistical experiments. Testing a bad page to find a less-bad version is wasted effort.

**Ship fast beats test everything.**
For early-stage solopreneurs, the cost of a wrong decision is low and the cost of slow iteration is high. Make the change, monitor metrics for 2 weeks, roll back if things drop. This is not rigorous science — but it compounds faster than waiting 3 months per test.

**Most "A/B test wins" are not real.**
Industry estimates suggest 70–80% of reported A/B test wins fail to replicate. Underpowered tests, peeking, and HiPPO pressure to call winners early corrupt most experimentation programs. Your win rate is probably lower than you think.

**Your copy matters more than your layout.**
Page structure tests often underperform copy tests. What you say beats where you say it, especially at low conversion rates where users are primarily evaluating trust and value, not usability.

**The best CRO tool is talking to customers.**
Five user interviews will generate better hypotheses than any amount of heatmap staring. Run the interviews first. Test the best ideas from those interviews.

---

## 15. Quick Wins

If you can't A/B test yet, these changes are directionally safe to ship without testing:

- Move CTA above the fold on mobile
- Add a single strong testimonial near the primary CTA
- Reduce form fields to the absolute minimum required
- Add a clear no-risk statement near the buy/signup button ("Cancel anytime", "No credit card required")
- Replace vague headline ("The platform for your business") with specific outcome headline ("Close 30% more deals without adding headcount")
- Add a FAQ section addressing the top 3 objections (ask sales or look at churned user emails)
- Remove navigation from landing pages with a single conversion goal

These are backed by enough replicated research that they are safe to ship on directional confidence rather than local statistical proof.

---

## 16. Related Skills

- `page-cro` — Full landing page conversion audit and rewrite
- `analytics-tracking` — Setting up the measurement layer before you test
- `signup-flow-cro` — Optimizing post-click signup and onboarding flows
- `copywriting` — Writing variants with enough differentiation to move metrics

---

*Generated using the ab-test-setup skill from Solopreneur Skills*
