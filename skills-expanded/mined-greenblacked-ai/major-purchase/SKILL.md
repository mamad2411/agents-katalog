---
name: major-purchase
description: "Decide on something expensive you will live with for years, in a fixed order: write the requirement before looking at any option, price total cost of ownership rather than the sticker — depreciation, insurance, maintenance, financing interest and resale — compare options that are each better at something without inventing a single score, refuse the upsell and the capability you would use twice a year, and write a pre-commitment that survives a showroom. Use this skill whenever someone is choosing a car, a flat, a laptop, an appliance, a bike or a course and says \"should I buy or lease\", \"new or used\", \"is this worth it\", \"which of these should I get\", \"do I actually need the bigger one\", \"they are offering 0% finance\", or is being sold an extended warranty. Not for company purchasing (vendor-evaluation), budgets, debt order and affordability (personal-finance), or salary decisions (offer-negotiation)."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(python3:*)
---

# Major Purchase

A finished decision names one option, the requirement it satisfies, its total cost of ownership over a stated holding period, the axis on which it is worse than the runner-up, and the walk-away conditions written down before any shopping began.

Expensive durable purchases go wrong in six repeatable ways. The requirement is written after the options are seen, so it describes the option the buyer already wants rather than the job to be done. Only the sticker price is compared, when on a car the sticker is roughly two-thirds of the five-year cost — AAA's *Your Driving Costs 2025* sets a sales-weighted average sticker of $38,938 against $57,885 to own and operate over five years and 75,000 miles — and on a house it is a smaller fraction still. The third that never appears on an invoice is larger than any discount you will negotiate. Financing is judged on the monthly payment, which is the one number a seller can set to any value by lengthening the term. The first price seen anchors everything after it, so a discount from an inflated list feels like a gain. Research already done becomes a reason to continue, which is the sunk cost in its purest form. And the rare case drives the specification — the towing trip once a year, the video edit twice — so the buyer pays a permanent premium for an occasional need. This skill fixes the order: requirement first and written down, total cost second, comparison on explicit axes third, and a pre-commitment that makes the decision before the room is designed to change it.

## Scope

Use for: cars, motorbikes and bicycles; property purchase as a purchase decision; laptops, phones and desktop machines; white goods and large appliances; furniture; musical instruments; tools; a paid course, bootcamp or qualification; and any other single purchase large enough that the buyer would be stuck with a mistake for years.

Do not use for: company or team purchasing, supplier selection, procurement and contract terms (`vendor-evaluation`); building the overall money picture, budgeting, emergency-fund sizing and debt payoff order (`personal-finance`) — bring the affordability answer here as an input; salary, equity and job offers (`offer-negotiation`); whether to rent or buy at all, which is `personal-finance` — the buy-and-sell break-even is computed here and handed over to feed that comparison; or planning the week (`weekly-review`).

Affordability and purchase choice are different questions. If the user does not yet know whether they can afford it, that is `personal-finance`; this skill assumes a budget exists and decides what to buy inside it.

## Where a regulated professional is actually needed

Three triggers, and none of them is "it costs a lot":

| Trigger | Who | Why |
| --- | --- | --- |
| The purchase moves title to land or property | A solicitor or conveyancer | Searches, title defects, lease terms and covenants are legal findings that the price comparison cannot surface, and they are discovered after exchange if nobody looks. |
| A used vehicle above roughly a few thousand in value, or any vehicle where the history is unclear | An independent inspection, and a finance and write-off history check | Outstanding finance on a used car can leave the buyer without the car and without the money, and a repaired write-off is invisible in photographs. |
| A structural, electrical or damp question on a property, or an installation that touches gas or mains electricity | A surveyor or the relevant certified trade | The cost of being wrong is four to five figures and, for gas and electrics, a safety certificate is a legal requirement in most jurisdictions. |

For everything else — specification, comparison, financing arithmetic — do the work fully.

## What varies by country

Name the variable rather than hedging the whole answer:

- **Consumer protection**: the length of the statutory return or cooling-off window, whether it applies to a distance sale only, and how long a fault is presumed to have existed at delivery. This changes how much a warranty is worth buying.
- **Vehicle taxes and duties**: purchase tax, annual road tax by emissions, low-emission-zone charges, and whether an electric vehicle keeps a tax advantage over the holding period.
- **Property transaction tax**, which ranges from negligible to over 10% of value and is the single largest transaction cost in most markets.
- **Financing regulation**: whether the lender is jointly liable for a faulty good bought on credit, which in some markets makes paying part of the price by credit card a protection worth the fee.
- **Warranty and repairability rules**, including a right-to-repair regime and mandated spare-parts availability, which change the realistic service life of an appliance.

## Workflow

### 1. Write the requirement before seeing any option

Write it down, in this order, before opening a single listing or review. A requirement written after browsing is a description of the thing already wanted.

- **The job.** One sentence on what this has to do, in the user's life rather than in specification terms. "Carry two adults, a dog and a week of luggage 400 miles four times a year, and do a 12-mile commute daily" is a requirement. "A reliable estate car" is a preference in disguise.
- **Hard constraints.** Budget ceiling, physical fit (the parking space, the doorway, the desk), a deadline, a compatibility that cannot be broken.
- **Must-haves.** Under five. Each one has to be a sentence the user would walk away over.
- **Nice-to-haves.** Explicitly ranked, and explicitly not decisive.
- **Frequencies.** For every capability, how many times a year it is genuinely used. This is the line that stops the rare case setting the specification.
- **Holding period.** How many years this is expected to be kept. Every cost number downstream depends on it, and it is the input people never state.

Then separate requirement from desire honestly. Both are legitimate — enjoying a thing is a real reason to buy it — but they must be on separate lines. A want moved into the must-have list quietly eliminates every cheaper option before the comparison begins. Say plainly which parts of the budget are buying capability and which are buying pleasure.

### 2. Price total cost of ownership, not the sticker

Compute over the holding period from step 1. The seven components, and the one people forget is the first:

| Component | How to get it | Why it dominates |
| --- | --- | --- |
| Depreciation | Current price of the same model at the target age and mileage, subtracted from purchase price. | On a new car this is usually the largest single cost of ownership — commonly 40-50% of the price over the first three years — and it never appears on any invoice. |
| Financing interest | Total repaid minus cash price, from the schedule rather than the headline rate. | It is invisible in a monthly payment and is frequently four figures. |
| Insurance | A real quote for the specific model, not a category estimate. | Varies by a factor of two or more between models in the same price bracket, and is paid every year. |
| Maintenance and servicing | Scheduled service costs at the interval, plus an allowance for wear items: tyres, brakes, belts, a battery. | A cheap purchase with expensive parts availability inverts the ranking. |
| Consumables and running costs | Fuel or electricity at the user's real annual distance or usage, plus anything metered. | This is where the frequency numbers from step 1 earn their place. |
| Taxes, licences and standing charges | Annual road tax, zone charges, permits, service charges, subscriptions the device requires to work. | A subscription that the product needs is part of the price, not an extra. |
| Resale or disposal | Expected value at the end of the holding period, minus the cost of selling or disposing. | Turns a purchase into a rental at a known rate, which is the honest way to see it. |

Express the result two ways: the total over the holding period, and the cost per year or per unit of use. Cost per year is what makes two options with different lifetimes comparable — a 900 appliance lasting twelve years is cheaper per year than a 500 one lasting four, and only the per-year number shows it.

Where a component is unknown, put a range on it and say which component the answer is most sensitive to. A total with one honest range beats a total with a false decimal place.

### 3. Do the financing arithmetic

Three numbers, always, before any comparison of deals: the cash price, the total amount repayable, and the APR.

APR and term interact to hide the total. Lengthening the term lowers the monthly payment and raises the total paid, which is why a seller asked for a lower payment will offer a longer term rather than a lower price. A 20,000 borrowing at 7% nominal costs 2,232 in interest over three years at 617.54 a month, and 3,761 over five at 396.02 — the payment falls by about 35%, the total cost rises by about 70%.

Rules that decide most financing questions:

- Compare on total repaid over the same term. A deal that only wins on monthly payment is winning on term length.
- A 0% offer is genuinely free money if the cash price is identical with and without it. Ask for the cash price both ways; a manufacturer discount withheld from finance buyers is a real interest rate in disguise, and computing it as one usually puts it in the mid single figures or higher.
- Deferred-interest arrangements that backdate interest to the purchase date if the balance is not cleared in time are priced on a different basis to an ordinary loan. Establish which it is before treating a promotional rate as a rate.
- On a personal contract plan or lease, the comparison against buying is the total of deposit, payments and any final balloon or purchase fee, against the purchase price minus the expected resale. Mileage penalties and condition charges belong in the total.
- Guaranteed future value in a lease contract is a cap on the buyer's depreciation risk and has a price. Price it by comparing that total against the buy-and-sell total; it is sometimes worth it and sometimes not, and only the arithmetic says which.

### 4. Decide new against used

The depreciation curve is steepest at the start and flattens, so the used question is really about where on the curve the risk becomes worth the saving.

| Category | Where the curve bends | The practical rule |
| --- | --- | --- |
| Cars | Steepest in year one — commonly 20-30% — and flattening from roughly year three. | One to three years old, with history, captures most of the saving while a manufacturer warranty may still run. Above roughly eight years or high mileage, maintenance variance grows faster than the price falls. |
| Laptops and phones | Fast for the first two years, then limited by the end of software and security support. | Buy used only inside the supported-software window; a device dropped from security updates has a hard end of life regardless of condition. |
| Large appliances | Shallow, because service life is long and second-hand markets are thin. | Buy new. The saving is small and there is no warranty or return route when a machine fails in month three. |
| Bicycles, tools, instruments, furniture | Very steep and then near-flat; many hold value for decades. | Used is usually the strongest value in these categories, and condition is assessable by inspection rather than by hidden history. |

Two costs sit on the used side and belong in the total: an inspection, and a contingency for the repair that arrives early. Budget 5-10% of the purchase price as a first-year contingency on a used mechanical item and it stops being a shock.

### 5. Compare options on named axes

Pick three to five axes from the requirement — never more, because an axis nobody would trade on adds noise rather than information. Score each option per axis in its own units, not on a scale out of ten.

Do not sum the axes into a single number. A weighted total looks objective and is not: the weights are usually chosen, consciously or otherwise, to make the preferred option win, and the composite hides the one axis the decision actually turns on. Compare pairwise instead, and answer one question per pair: what does the more expensive option buy, and is that worth the difference?

| Axis | Option A | Option B | The trade |
| --- | --- | --- | --- |
| Total cost over [n] years | [amount] | [amount] | [which is cheaper and by how much] |
| [capability from the requirement] | [in real units] | [in real units] | [what the gap means in use] |
| [risk or reliability] | [evidence] | [evidence] | [what the worse one costs if it goes wrong] |

Then name the losing axis explicitly for whichever option is chosen. A decision with no acknowledged downside has not been made; the downside has been suppressed and will resurface as regret.

Where two options are genuinely close on every axis, say so and pick on the cheapest reversal cost — which one is easier to sell, return or replace if it turns out wrong. Close decisions should be made quickly and cheaply, not researched further; the additional research does not separate them.

### 6. Run the trap checklist

Check the decision against each of these before committing. The full list, with how each one shows up in conversation and the specific counter, is in `references/decision-traps.md` — read it when the user is close to committing, or when a decision keeps reversing.

- **Anchoring.** The first price seen sets the scale for everything after it, and a discount from an inflated list reads as a gain. Counter: set the budget and the target price from independent data before looking at any seller's price.
- **Sunk cost on research.** Forty hours of reading is not a reason to buy; it is spent either way. Counter: ask whether this option would be chosen by someone arriving fresh today.
- **Specifying for the rare case.** Paying permanently for the twice-a-year need. Counter: use the frequency numbers from step 1, and price hiring or borrowing for the rare case instead.
- **The discount as a reason.** A saving on something not needed is a cost, not a saving. Counter: decide the option first, then the price.
- **Monthly payment framing.** Any total can be made to look small by lengthening the term. Counter: compare total repayable only.
- **Deadline pressure.** "This price is only today" is a manufactured scarcity in almost every retail context. Counter: the pre-commitment in step 7, which includes a mandatory pause.
- **Specification creep at the point of sale.** Trim levels, bundles, extended warranties and add-ons are priced at the moment commitment is highest and resistance is lowest.

### 7. Write a pre-commitment before shopping

Write this down before entering a showroom, opening a checkout, or taking a call, and read it back at the point of decision. This is the step that makes the rest survive contact with a seller.

The pre-commitment fixes: the maximum total price including every extra; the specification agreed, with add-ons named as excluded; the two or three walk-away conditions; a mandatory pause of at least 24 hours between the best offer and accepting it, which is what defeats manufactured urgency; and who else has to agree, where the purchase is shared.

Treat any pressure to decide before the pause expires as information about the seller rather than about the deal. A genuine price is available tomorrow.

A worked pre-commitment, plus the negotiation sequence that goes with it and the specific questions to ask at the point of sale, is in `references/purchase-playbook.md` — read it before a showroom visit, a viewing, or a negotiation.

## Output format

```text
## The requirement
Job: [one sentence, in use rather than in specification]
Holding period: [years] · Budget ceiling: [amount, all-in]
Must-haves: [under five, each a walk-away]
Frequencies: [capability — times per year]
Desire, stated honestly: [what is being bought for pleasure rather than capability]

## Total cost of ownership over [n] years
| Component | Option A | Option B | Option C |
| Purchase price | | | |
| Depreciation / resale | | | |
| Financing interest | | | |
| Insurance | | | |
| Maintenance | | | |
| Running costs | | | |
| Tax and standing charges | | | |
| Total | | | |
| Per year | | | |
Most sensitive to: [the component, and the range on it]

## Comparison
| Axis | A | B | The trade |

## Recommendation
[One option.] Chosen because [the deciding axis].
Worse than [runner-up] on [axis] — accepted because [reason].
New or used: [which, and where on the depreciation curve].
Financing: cash price [amount] · total repayable [amount] · APR [x]%

## Pre-commitment
Maximum all-in: [amount] · Excluded: [add-ons named]
Walk away if: [two or three conditions]
Pause: [24 hours minimum] · Also has to agree: [who]

## Needs a professional
[trigger and who, or "none of the triggers apply"]
```

## Anti-patterns

- **Writing the requirement after browsing.** The list then describes the option already wanted, every cheaper alternative is eliminated before the comparison starts, and the process reads as diligence while functioning as justification. Write it first and date it.
- **Comparing sticker prices.** On a car the purchase price is roughly two-thirds of the five-year cost of ownership and operation — $38,938 against $57,885 in AAA's *Your Driving Costs 2025* — and the third that never reaches an invoice is larger than any discount you will negotiate; on a property the transaction and running costs run to years of the difference between options. Ranking on sticker regularly picks the more expensive option.
- **Negotiating on the monthly payment.** It is the one number a seller can set to any value by extending the term, and doing so raises the total. Quote the total repayable instead and the deal stops moving.
- **Specifying for the rare case.** The once-a-year tow, the twice-a-year long drive, the occasional big render. Paying a permanent premium for an occasional need costs more than hiring for it, usually by a wide margin over a holding period.
- **A weighted score out of ten.** The weights get tuned until the preferred option wins, and the composite hides the single axis the decision turns on. Compare pairwise and name what the extra money buys.
- **Treating research as an investment.** Hours already spent are gone whichever option is chosen, and the only effect of counting them is to lock in the option researched first. Ask what someone arriving fresh today would pick.
- **Buying because it is discounted.** Buying the wrong thing at 40% off is a loss of 100% of the price paid, not a saving of the difference. Decide the option, then the price, in that order and never the reverse.
- **Deciding inside the seller's environment.** Showrooms, viewings and checkout flows are designed to compress the time between wanting and committing. The 24-hour pause is the entire defence, and skipping it is where extended warranties and add-ons get sold.
- **Ignoring the cost of being wrong.** Two close options are separated by which is easier to sell, return or replace, not by more research. Reversal cost is a real axis and it is usually the tiebreaker.
- **Leaving the holding period unstated.** Every cost figure depends on it, so an unnamed holding period means the totals cannot be compared at all and the cheapest per-year option stays invisible.

## Reference files

- `references/cost-of-ownership.md` — read at step 2 when building the totals: per-category component checklists for vehicles, property, computing, appliances and courses, typical depreciation curves, and the ranges to use when a real figure cannot be obtained.
- `references/decision-traps.md` — read at step 6, or whenever the decision keeps reversing: each trap with how it sounds in conversation, why it works, and the specific counter-question that defuses it.
- `references/purchase-playbook.md` — read before a showroom visit, a viewing or a negotiation: the pre-commitment template, the sequence for negotiating on total price, the questions to ask at the point of sale, and the add-ons to refuse by name.
