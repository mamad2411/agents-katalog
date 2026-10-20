---
name: log-a-mileage-expense
domain: business
locale: [generic]
interface: mixed
difficulty: basic
est_time: 5min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Log a business mileage trip with enough detail to support reimbursement, billing, or tax records.

## Preconditions

- You know the trip date, start and end locations, business purpose, and miles or kilometers driven.
- The vehicle and mileage rate are known if reimbursement or deduction is calculated.
- Personal commuting and nonbusiness mileage can be separated.

## Steps

1. **Open mileage tracking.** Go to expenses, mileage, trips, or reimbursement and create a new mileage entry. → *Expect:* a mileage form is visible.
2. **Enter trip date and route.** Add date, start location, destination, and optional odometer readings. → *Expect:* the trip route and timing are recorded.
3. **Enter distance.** Use odometer readings, map distance, or tracker data for miles or kilometers. → *Expect:* the entry shows a measurable business distance.
4. **Add business purpose.** Describe the client visit, delivery, supply run, meeting, or job site. → *Expect:* the purpose explains why the trip was business-related.
5. **Apply rate or category.** Select mileage rate, vehicle, customer, project, or expense category. → *Expect:* the system calculates the reimbursement or expense amount if supported.
6. **Attach support if available.** Add calendar event, job record, receipt, or map note. → *Expect:* the trip can be substantiated later.
7. **Save the mileage entry.** Save or submit for approval if required. → *Expect:* the mileage appears in reports or reimbursement queue.

## Decision points

- Trip includes personal stops → record only the business portion.
- Commute from home to regular workplace → do not treat it as business mileage unless local rules allow.
- Actual vehicle costs are being tracked instead of mileage rate → record fuel, maintenance, insurance, and depreciation separately.
- Mileage is customer-billable → assign the customer or project before invoicing.

## Failure modes & recovery

- **F1 Missing purpose:** detect by blank or vague description → recover by adding the client, job, or business reason.
- **F2 Personal miles included:** detect by route including errands or commute → recover by reducing distance to business miles only.
- **F3 Wrong rate:** detect by reimbursement amount using outdated or incorrect rate → recover by updating the mileage rate and recalculating.
- **F4 Duplicate trip:** detect by same date, route, and distance already logged → recover by deleting or merging the duplicate.

## Verification

The mileage entry shows date, route, business distance, purpose, vehicle or rate, category, and reimbursement or billable status if applicable.

## Variations

- [BRANCH: QuickBooks | Xero | generic] QuickBooks has mileage tracking in some plans; Xero often uses expenses or third-party mileage apps; generic tools may use reimbursement forms.
- `us`: IRS standard mileage rates and documentation rules are year-specific, and commuting is generally not deductible.

## Safety & privacy

Medium risk because mileage logs may affect tax deductions and reveal travel locations. Do not expose home addresses or client locations beyond authorized accounting records.
