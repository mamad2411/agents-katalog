---
name: fortax-hr-compliance-calendar
description: Build and keep a client's employment compliance calendar in India — PF ECR, ESI, professional tax per state, salary TDS and 24Q / Form 16, bonus return, shops or factory renewal, contract labour — plus the statutory registers, displays, nominations, POSH duties, the Labour Codes check and the annual sweep, as a sourced spreadsheet the CA runs from. Typical asks: "HR compliance calendar banao", "PF ESI PT ki due dates", "kaunse registers maintain karne hain", "labour law compliance checklist".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
---

# HR compliance calendar

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

Registration ends and obligation begins. `fortax-payroll-registrations` gets the codes; this skill turns
each code into a live calendar, and keeps the registers and records the labour laws require to exist
whether or not anyone asks for them. **Every due date, frequency, rate, fee, penalty and retention
period here is looked up, per period, per state.** Run
`python3 scripts/fortax.py kb "ESI half-yearly return due date" --topics pf,esi` first and quote its
source and captured date; where the reply is `weak` or `none`, or the fact is stale, read the portal or
the state notification, and say the age of the data before the CA acts on it. The obligations below are
real and their sequence is stable; their dates are not, and several are state law.

## Step 1 — scope the client

From the client's own records take the PF code, ESI code, TAN, PT registration and enrolment numbers,
the shops or factory licence, the states and cities with employees, and the headcount. One calendar per
registration, not per client: employees in three states means three PT lines and possibly three shops
and establishment lines. Confirm what is actually applicable — some Acts bite only above a headcount,
some only on a scheduled employment, some not at all in a given state — so look up each trigger and
never assume. Confirm too whether a contractor's workers are on site: contract labour brings its own
registration, registers and returns onto the principal employer.

## Step 2 — the recurring filings

| Head | Cycle | What is filed | Payment |
|---|---|---|---|
| PF | Monthly | ECR from the salary register on the EPFO unified portal | Challan from the ECR |
| PF | Event-driven, annual | UAN and KYC for joiners, exit marking for leavers, transfer claims; the annual position as currently prescribed | — |
| ESI | Monthly | Contribution file on the ESIC portal | Challan |
| ESI | Event-driven, half-yearly | IP registration and e-Pehchan card for each new coverable employee; the return of contributions where it still applies | — |
| PT | State frequency, annual | State return per state; enrolment certificate renewal where that state requires it | State challan |
| TDS on salary | Monthly, quarterly, annual | 24Q with annexures each quarter; Form 16 to each employee after year end | Monthly challan against the client's TAN |
| Bonus | Annual | Annual return under the Payment of Bonus Act | Paid within the statutory window |
| Shops or factory | State cycle | Renewal or annual intimation, plus the annual return where prescribed | Fee |
| Contract labour, maternity, gratuity, minimum wages | As prescribed | Principal employer's return where contract workers are engaged; the notices, nominations and returns each Act requires | — |

The cycle column is the usual pattern, to be confirmed for the period and the state. And where the
Labour Codes have been brought into force for a state or a subject, they replace or restate several of
these — check the commencement position before rebuilding a calendar on the old Acts, and record it.

## Step 3 — registers and records

These exist to be produced on an inspection. A register not maintained is a default even if every
challan was paid on time. Confirm the prescribed form and retention period for the state before
naming either.

| Register or record | Arises under |
|---|---|
| Register of employees, and of wages with the wage slips issued each period | The state shops and establishment Act or the Factories Act; Minimum Wages and Payment of Wages |
| Attendance and overtime register, and the leave-with-wages register | State Act, Factories Act |
| Register of fines, deductions and damage or loss, and the muster roll | Payment of Wages Act; Contract Labour Act, Factories Act |
| Register of bonus, allocable surplus, set-on and set-off | Payment of Bonus Act |
| Gratuity nominations and notice of opening; maternity benefit register; accident register | Payment of Gratuity Act; Maternity Benefit Act; ESI Act and Factories Act |
| PF nominations, member declarations, contribution card | EPF Act and Schemes |
| POSH complaints record and annual report to the district officer | POSH Act, where its trigger is met |

Many states now permit combined registers and electronic maintenance under simplification rules; where
the client wants that, read that state's notification before agreeing it covers a register.

## Step 4 — display and standing duties

Distinct from filing — these must be visible or in place continuously, and inspectors look for them.
The registration and licence certificates displayed at the premises; abstracts of the applicable Acts
and the notice of wage period, wage rates, working hours, weekly holiday and the inspector's name, in
the language the state prescribes; the PF and ESI code numbers where the rules require them, with the
ESI dispensary details; an internal committee constituted and named where the POSH Act's trigger is
met; nominations collected for PF, gratuity and ESI dependants, since a missing one surfaces at the
worst possible moment; and notices of the weekly closing and of leave where the state prescribes.

## Step 5 — build the calendar and keep it alive

1. Write `<date>_HR_compliance_calendar_<client>_<FY>.xlsx` in the client's payroll folder: one row per
   obligation, with the registration it belongs to, the state, the cycle, the form, the portal, the
   owner at the firm, the due date, days left (a formula), and a **source and date-checked column on
   every date**. No date without a source.
2. If the firm keeps a compliance tracker, calendar app or practice-management tool, prepare the rows in
   the format it imports (CSV is usually safest) and show the CA exactly what will be created. The CA
   adds them, or tells you to, after a clear yes. Anything not in the firm's tracker will not be chased.
3. Where the firm's tracker and this calendar disagree, that is a defect: find which is stale before
   anyone messages a client.
4. Re-verify at the start of each FY and whenever a notification lands. Use `fortax-deep-research` for
   what changed, then update the calendar, say what moved, and minute the annual registers-and-displays
   audit in the same file with what was seen and what is missing.
5. **The annual sweep**, in one pass: 24Q Q4 filed and Form 16 issued; the PF annual position closed
   and all exits marked; the ESI half-yearly return where applicable; the PT annual return and
   enrolment renewal per state; bonus paid and its annual return filed; the shops or factory renewal
   done; gratuity, bonus and leave provisions from `fortax-gratuity-bonus-leave` tied into the accounts;
   the POSH annual report where due; every register written up to the last day.

## Hand over

Calendar and audit notes to the client's payroll folder for the FY (for example
`<Client>/<FY 2026-27>/Payroll/`), dated. Registers and raw client records stay where the client keeps
them and are never renamed or deleted. Employee-level data stays in the client folder — a reminder
message (drafted for the CA to send, see `fortax-client-comms`) carries the obligation, the period and
the file name, never a name, a salary or a bank detail.

- Which registrations are live, which Acts apply, and the calendar rows created for each.
- What is missing today — registers not maintained, nominations not collected, displays absent,
  returns not filed for past periods — and the exposure on each.
- **Check before filing**: every date carries a source and a date checked; state obligations read for
  each state separately, this session; the Labour Codes commencement position checked; registers and
  nominations verified as existing, not assumed; rows ready for the firm's tracker; nothing submitted,
  paid or sent without the CA's explicit yes.
