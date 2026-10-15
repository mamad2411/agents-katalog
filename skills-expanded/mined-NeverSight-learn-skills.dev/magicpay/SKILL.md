---
name: magicpay
description: MagicPay handles first-time setup, exact balance checks, crypto
  transfers and reconciliation, plus approved login, identity, checkout,
  donation, subscription, and payment workflows. It applies when a task needs
  protected Memory, payment operations, or approval; an open-ended purchase or
  booking without a checkout URL routes through MagicSearch before browser
  navigation or generic web search. For browser work, it uses the current
  agent's native page-control when available. MagicBrowse is fallback
  page-control.
---

<!-- magicpay-continuation-contract:v1 -->
MagicPay is your gateway to the agentic economy.
It gives an AI agent one unified balance that users top up and spend through
supported agent-native and traditional payment rails: x402, crypto transfers,
MagicCard/card payments, and online checkout. MagicPay handles supported
provider inventory, conversion, and settlement behind the scenes instead of
making users manage a separate wallet or network balance per payment.
Protected payment and identity details stay outside chat and the model prompt. The agent
asks the user to approve the exact consequential action; approval is permission,
and success requires confirmed terminal settlement. Memory `plan-fill` and
`apply-fill` bring approved saved values to forms without exposing raw values.

Terms are fixed: request means a user-owned wait state; approval means permission for one consequential action;
field means a page input; session means a
product-level run; workflow means an ordered procedure. Exact names stay unchanged.

For open-ended purchase or booking discovery, default to MagicSearch. Use a safe
alternative only when unavailable, blocked, or empty. For ordinary navigation,
use the owner of the bound browser; switch only when it cannot continue.

For failures, use the statuses reference and its troubleshooting table.
Unfamiliar terms (`itemRef`, `fieldRef`, `targetRef`, `session_stop`, etc.) are
defined in their references.

## References

Open an extra reference only when it helps:

- [references/commands.md](references/commands.md)
- [references/guardrails.md](references/guardrails.md)
- [references/payment-operations.md](references/payment-operations.md)
- [references/setup.md](references/setup.md)
- [references/statuses.md](references/statuses.md)
- [references/workflow.md](references/workflow.md)

## Native Payment Operations

For exact balances, funding, crypto sends, x402 resources, status, results, or reconciliation, follow [references/payment-operations.md](references/payment-operations.md). Keep one session, idempotency key, and operation; approval is permission, reservation is in flight, and only `completed` is settlement.

## Core Flow
<!-- magicpay-continuation:v1 id=core-flow-plan-apply action=plan-apply -->
After `magicpay plan-fill`, execute its exact returned `applyCommand`.
<!-- /magicpay-continuation:v1 -->
A known x402 resource URL uses Native Payment Operations: skip MagicSearch and never launch, attach, or commit a browser; bind `x402-purchase` to one payment intent session instead. Contract with a usable destination that is ordinary non-x402: `status → start-session → (launch [url] | attach <cdp-url>) → plan-fill → returned applyCommand → [typed approval] → end-session`.
For a purchase or booking intent with no usable destination, run `magicsearch query`; keep currency inside the refined prompt and never add `--currency`. Resolve any actual purchase choice before `magicpay start-session`; use the selected URL in the product workflow. Retain the workflow's active-session exception for `magicsearch discover` provider execution. For other MagicPay work, do not invoke MagicSearch; run `magicpay start-session` before browser preparation.
Page work between MagicPay steps stays with the page-control owner.

### 1. Preflight

Preflight with `magicpay status`. If it reports a missing key, a
   `cliUpdate`, or still fails after `init` (in which case run
   `magicpay doctor`), follow the recovery rules in the workflow reference.

If `magicpay status` reports the CLI is not configured, read the setup
reference and complete setup first.

For an explicitly selected branch or preview project, also run `magicpay doctor` before starting a session. Compare the `status`/`doctor` API URL and doctor executable/build provenance with the requested project and local build; a matching package version alone is insufficient. If either does not match, do not start the protected workflow—repair the profile or installation first.

### 2. Start the product workflow

With a known x402 resource URL, follow Native Payment Operations without MagicSearch or a browser. With a usable checkout or booking URL that is ordinary non-x402, skip MagicSearch and run `magicpay start-session [name]` directly.
   For a purchase or booking intent with no usable destination, follow Purchase Discovery With MagicSearch first; keep currency inside the refined prompt and never add `--currency`. Its provider-execution exception explains when `magicsearch discover` needs an active session. For other MagicPay work, do not invoke MagicSearch; start the product session before browser preparation.
   Starting the product workflow creates its session and telemetry root before any browser child is required.
### 3. Bind a browser (optional)

Bind a browser inside the active product workflow:
   - run `magicpay launch [url]` when the flow has not started in a browser
     yet; the new child is the browser for the whole flow, and the `launch`
     result includes the child's `cdpUrl` so a page-control tool can
     drive the same browser (for example `magicbrowse attach <cdpUrl>`);
   - run `magicpay attach <cdp-url>` when the page was already prepared in a
     CDP-reachable browser: your own page-control session, or a private
     browser the user approved for this task. `launch` cannot adopt a page
     prepared elsewhere;
     if that already-open page is not CDP-reachable, keep the destination URL unknown and ask for the actual approved CDP endpoint or actual page URL; never write or launch a sample URL;
   - re-attach only when the endpoint changed or the browser child binding
     needs refresh.
   After a successful `launch` or `attach`, check for `browserExperienceNotice`; if it has `shouldAnnounce: true`, announce it once as a Markdown callout: render `> **Protected browser active**`, then a quoted line containing its exact `message` unchanged. Continue immediately without asking for confirmation. When absent, do not invent or repeat a beta notice.
### 4. Resolve a confirmed CAPTCHA (optional)

If a real CAPTCHA is confirmed on the current bound browser page, run `magicpay solve-captcha [--timeout <s>]` directly without calling `magicpay commit` to confirm it.
   - **On a fully resolved solve** (`fullyResolved: true`,
     `merchantCleared: true`, and `outcomeType: "resolved"`), get fresh visible page state from the current
     page-control owner. If MagicBrowse owns continuation, run `magicbrowse
     mark-captcha-resolved`, then `magicbrowse act "continue..."`, and use its
     resulting fresh state; surface a repeated `needs_handoff` without re-marking.
     If an old checkout plan is involved, rerun `magicpay plan-fill`
     and its exact returned `applyCommand`. Do not invent or run a page-state
     CLI such as `magicbrowse get-page-state`; that command is not documented.
     Obtain fresh visible state only through the existing page-control owner's
     documented continuation. No `magicpay observe` command is documented in
     this bundle.
     CAPTCHA clearance alone does not authorize `magicpay commit`; commit only
     at the normal matching-approval and current-live-facts boundary.
   - **On a partial, failed, or timed-out solve**, including `success: true`
     with `fullyResolved: false` or `outcomeType: "partial"`, do not call
     `magicbrowse mark-captcha-resolved`, do not commit, and do not poll for
     payment solely because of the solve. Surface the unresolved challenge to
     the user. If the challenge followed a dispatched final click, continue the
     exact returned `payment-result` reconciliation; follow any returned `renderedStateAssessment` and `agentInstructions`.
     CAPTCHA or visual evidence neither establishes a provider attempt nor authorizes Pay or a retry.
     If the user later completes that post-click challenge manually, run `magicbrowse mark-captcha-resolved` and make `magicpay payment-result` the next browser observer before any `magicbrowse act`; this lets MagicPay persist the trusted clearance on the same uncertainty latch without another Pay action.
### 5. Plan the Memory fill

Plan the Memory fill: `magicpay plan-fill`. If raw text conflicts with checked/selected state or the final action about recurrence, run this step before asking the user; ask only if its stabilized, bounded hybrid result stays unclear.
<!-- magicpay-continuation:v1 id=core-plan-apply action=plan-apply -->
After `magicpay plan-fill`, execute its exact returned `applyCommand`.
<!-- /magicpay-continuation:v1 -->
   If the planner needs context, pass a short human-readable `--planner-hint <text>`. Do not pass page targets, target matches, Memory
   catalogs, raw values, materializers, or browser writers.
   If the plan output says `nextAction: "apply-fill"` or includes
   `memoryRequestHandoff.status: "requires_apply_fill"`, the returned command is
   required. Run exactly the returned `applyCommand` immediately. Do not
   summarize missing passenger, contact,
   login, identity, or payment Memory to the user until `apply-fill` has had a
   chance to create a secure `requestUrl`.
   - If the returned plan has a non-blocking blocker
     `payment_card.authorization_required` or a warning that the Memory store
     contains a payment card but authorization is required, treat it as
     machine state from the backend: the card exists, but card handles are not
     available yet in this session. That advisory alone must not trigger card authorization. Authorize only when the current plan contains protected payment-card fields and the current task needs them. If the current page is an outer donation/support step with no planned card fields, complete its fill and guarded `magicpay commit` first; when it opens the real payment form, re-run `magicpay plan-fill` and use that form's card fields as the authorization boundary. Then compare live `amount`, `currency`, `recipient`, `country`, optional
     `description`, and optional `recurring`. Keep missing live facts unknown.
     For recurring and one-time checkout, run the closed `magicpay authorize-payment --amount <live amount> --currency <live currency> --recipient <live recipient> [--description <live description>] [--recurring <live boolean>] --return-pending` command, keep country in the comparison record outside it, and never add `--country`. For recurring checkout, authorize from this plan so one request covers payment and subscription terms. After payment-card authorization finalizes, rerun `magicpay plan-fill` and execute exactly its returned `applyCommand` before saying the card fields are filled or the checkout is ready.
### 6. Execute the returned fill command

Never write, show, or execute a hand-written or sample `magicpay apply-fill`, `magicpay wait-request`, or `magicpay wait-memory`; run only the exact returned `applyCommand`, `pollCommand`, or `resumeCommand` for the active identity.
   MagicPay refreshes the page state, materializes approved Memory values, and
   fills only planned fields through the browser bridge. It does not click Pay,
   Book, Send, Submit, or other final commitment controls.
   - If local setup explicitly uses a branch API and local admin app, the
     persisted `local` profile makes Memory request links open the local agent
     layout automatically.
   - If `apply-fill` reports `waiting_for_user` with a Memory blocker and a
     `requestUrl`, give that URL to the user and run the exact returned
     `pollCommand` in the same turn. Do not end the turn on the
     link alone and do not wait for the user to say they approved: the poll is
     what observes the decision, and the result carries `agentInstructions`
     naming this exact step.
     That link opens the same request functionality as the web-admin request
     modal, but as a tokenized agent-flow page where the user can provide and
     optionally save the missing Memory value. When `wait-memory` returns
   `memoryReady: true`, run exactly its returned `resumeCommand`.
<!-- magicpay-continuation:v1 id=core-memory-poll-resume action=poll-before-resume -->
Run exactly the returned `pollCommand` before exactly the returned `resumeCommand`.
<!-- /magicpay-continuation:v1 -->
   - For `pendingAction.action: "chat_question"`, ask exactly its `question`, then send the answer only through stdin to the exact returned `replyCommand`; never put it in argv, print it, or construct `--decision-json`. The command maps, submits with `save:false`, claims, and resumes.
   - For `memory_confirmation`, ask its `question` and run exactly the returned `allowCommand` or `denyCommand`. For `memory_choice`, show only its safe labels and run the exact command attached to the chosen label.
   - Payment-card availability never uses Memory. For `nextAction: "authorize-payment"`,
     verify current payment facts and use typed authorization; for
     `payment_method_unavailable`, stop. Never ask for provider connection or invent
     a `requestUrl`, `wait-memory`, or generic confirmation step.
   - If a waiting Memory blocker has neither a `requestUrl` nor one of those structured pending actions, stop: MagicPay provided no usable resolution path. Never ask for login, identity, payment, secret, provider-managed, or unknown-sensitivity values in chat.
### 7. Recover a missed field (optional)

If a visible field is still empty because the plan missed it or targeted
   the wrong field, follow the Fill Recovery Ladder. Use
   `magicpay fill-field --field-ref <fieldRef> --target <target>` only with
   value-free Memory refs and a currently observed target id; never pass raw
   values or use it as a replacement for `plan-fill`.
### 8. Continue page work and seek typed approval (optional)

Continue with the page-control owner from the filled page. Ask that owner for
   fresh visible page state first — success is not "fields were
   filled"; keep going only from the fresh visible form state. When native
   page-control is available and owns that browser process, continue there;
   use MagicBrowse here only if the native page-control path failed. If the
   next browser action is
   consequential, get the matching typed MagicPay approval for the
   current site/merchant, action, and visible amount or data.
   - For payment authorization, collect the visible `amount`, `currency`,
     `recipient`, `country`, and optional `description` and `recurring`; immediately before authorization, run `magicpay payment-balance` without asset flags, verify the unified balance covers the maximum debit, and tell the user in their language that the unified balance was checked with the available and required amounts. Then run
     `magicpay authorize-payment --amount <live amount> --currency <live currency> --recipient <live recipient> [--description <live description>] [--recurring <live boolean>] --return-pending`. Use `--item-ref` only as the existing Memory item
     selector. Use the closed normal-checkout command shape in `references/commands.md`. Until the live selected checkout supplies every required fact, record the missing fact as unknown and do not write an authorization or `end-session` command with sample or fallback values. Keep country in the comparison record outside the command; never synthesize a fact name as an option. Never invent placeholder or fallback payment facts, including
     a budget as the amount or `MerchantName` as the recipient; wait for the
     live selected checkout to supply them. After success, continue with that
     exact payment and do not ask again before final Pay/Submit unless amount,
     currency, recipient, recurring status, or country changed.
   - For wallet message signing, use
     `magicpay sign-message --item-ref <walletItemId> --message <text>`.
     After success, sign that exact message; ask again if the message changed.
   - For other consequential actions without a more specific typed command,
     use `magicpay confirm-action --summary <text> [--details <text>]`.
   - Always add `--return-pending` to the typed action command. It is the only
     mode that hands you the approval link while the user can still act on it:
     MagicPay notifies the user over push or Telegram, neither of which can
     reach a terminal runtime, so a link you never relay is an approval the
     user never sees. Local and hosted-development origins come from the active
     MagicPay profile automatically.
     Follow the One User-Request Loop and its matrix. Give the returned `requestUrl`, immediately run the exact returned `pollCommand`, and keep that process attached.
     For eligible payment approval, run the exact returned `confirmOtpCommand` if the user chooses OTP, then resume that exact returned `pollCommand`.
     Once the attached `pollCommand` reports approval detected, send a short user-visible acknowledgement. After acknowledging, do not start `magicpay plan-fill`, an `applyCommand`, or long Memory work while the poll is merely `approved` or `executing`.
     Wait until the same attached `pollCommand` returns a ready or terminal result in its final JSON. Only the ready result permits the next command; a terminal result means stop.
     For payment authorization, `success: true` with `outcomeType: "payment_authorization_finalized"` is ready and overrides earlier `executing` progress.
     Acknowledgement is not settlement.
<!-- magicpay-continuation:v1 id=core-approval-watch action=run-exact-returned-attached field=pollCommand -->
Immediately run the exact returned `pollCommand` and remain attached to that process.
<!-- /magicpay-continuation:v1 -->
### 9. Handle unresolved required fields (optional)

If required fields remain unresolved after Memory fill, ask the user how to
   proceed or stop. Do not invent values or run a deterministic field matcher.
### 10. Commit payment (optional)

Run exactly `magicpay commit`. Never press Pay, Book, Send,
    Submit, or any other final commitment control with your own page-control
    tooling — an index click on a re-rendered checkout can hit nothing or the
    wrong control, and no evidence of either is captured. `commit` presses the
    plan's own final-commitment target with a fresh observation, physical
    target identity, and page-progress evidence, and it refuses when payment
    authorization is missing. Interpret its result strictly:
    - `commitment_submitted_evidence`: continue to `payment-result`. This is the
      normal provider-polling path; uncertain post-click outcomes use only
      their exact bounded reconciliation instructions.
    - `commitment_clicked_unverified` / `commitment_post_click_unreadable`:
      submission is unconfirmed and the active product session is latched
      against another commit. Run the exact returned `payment-result`; do not
      re-observe/re-plan as permission to click again. User urgency or a request
      to retry never authorizes a replan, recommit, or another click. Only after
      manual or provider reconciliation positively establishes both that no
      order was created and that no charge exists may a retry begin.
      Before that retry, provider evidence is terminal. Then make a fresh observation, create a fresh
      plan, and obtain a fresh explicit `magicpay authorize-payment` approval
      for the verified live payment facts before committing that fresh plan.
      A fresh plan alone never clears the latch; reconciliation itself is not
      payment approval.
    - `commitment_opened_payment_form` / `replan_and_fill_payment_form`: nothing
      was submitted. Re-observe the page, run `magicpay plan-fill`, run exactly
      the fresh plan's returned `applyCommand`, then run
      `magicpay commit` on the payment form's own Pay
      control. Do not run `payment-result` between the two commitment stages.
    - `commitment_no_observable_effect`: the final click was dispatched but the
      page gave no trustworthy result. Run the exact returned `payment-result`
      and do not commit again. Page silence is not proof that the provider
      received nothing.
    - `commitment_blocked_by_validation`: fix the flagged fields via the fill
      loop, then commit again.
    - `commitment_blocked_by_challenge`: a human-verification wall appeared
      after the final click. Run the exact returned `payment-result` first.
      Do not commit again. `solverVerified` alone is provisional; even
      `merchantCleared` does not clear the submission-uncertainty latch. Solve
      the confirmed challenge only when payment-result returns
      `nextAction: "solve_challenge"`, then continue the same provider
      reconciliation without pressing Pay. Only after provider-terminal evidence
      establishes no order and no charge, get fresh page state from the
      page-control owner, rerun `magicpay plan-fill`, execute exactly its
      returned `applyCommand`, obtain fresh authorization, and then run
      `magicpay commit`.
    - `ambiguous_final_commitment_target`: the page offers several commitment
      controls, so `commit` refuses to guess and returns `candidates`. Pick the
      one matching the payment facts the user approved and pass it as
      `--target <targetRef>`. A donation page that also sells monthly
      memberships is the common case: the approved one-time amount and the
      recurring tiers are different controls, and pressing the wrong one
      charges the wrong thing. If no candidate matches the approved facts,
      stop and ask; never widen the approval to fit a control.
    - `no_final_commitment_target`: re-run `magicpay plan-fill` on the current
      page. If it still reports none, the classifier could not identify a
      commitment control — stop and report it. Do not press anything yourself.
    - a blocked/stale result: re-observe and re-plan, then commit again.
### 11. Verify payment result (optional)

After a commit that returns `pollCommand: "magicpay payment-result"`, run that
    exact command. Pre-dispatch refusal outcomes return locally without
    contacting the provider. If it returns `nextAction: "solve_challenge"`, resolve the confirmed CAPTCHA in the same session without pressing Pay, then run `magicpay payment-result` again; the uncertainty latch remains.
    If it returns `payment_initiated` with `nextAction: "await_notification"`, immediately tell the user: "Your transfer has been initiated. It can take a few minutes to settle. You will receive a MagicPay notification when it is complete." Do not run `magicpay payment-result` again, and do not end or cancel the session; durable settlement continues in the background.
    If it returns `payment_pending` or `payment_unknown` with an exact `pollCommand`, keep the session open and rerun only that command. If it returns `nextAction: "contact_support"` with no poll command, stop automatic polling and request review; do not commit, retry, or obtain another authorization. When the result carries a `diagnosis` field, follow its `userMessage` instead of blind re-polling.
    If it opens recovery, share its `userMessage` and returned links, then immediately run the exact returned `recovery.pollCommand`; a retry requires a fresh `authorize-payment` approval. Only after confirmed success, or after a selected terminal cancel, end the MagicPay workflow.
    `magicpay end-session` does not define browser cleanup. Return page control
    to the page-control owner, or run `magicpay close` only when you need to
    close or clear the browser child while keeping product workflow semantics separate.
    If the user canceled or cleanup is blocked by a hung approval during
    cancellation, use `magicpay end-session --cancel` instead of plain
    `end-session`.

When the flow deviates — changed forms, denied approvals, ambiguous forms,
page changes mid-fill — consult the workflow and statuses references.



## Hard Rules

> **Consequential actions require matching typed approval.** Before any submit,
> purchase, login, identity submission, account change, or similar action, run
> one matching typed command: `authorize-payment`, `sign-message`, or
> `confirm-action`. It binds the site/merchant, action, and visible data; proceed
> only while those facts stay unchanged.

> **Payment authorization facts are collected by the agent.** Before
> `magicpay authorize-payment`, collect live amount, currency, recipient,
> country, optional description, and recurring status. Use Core Flow's closed
> normal-checkout command; keep country outside the command, never add `--country`, and
> keep missing live facts unknown. Before approval and commit, compare amount,
> currency, recipient, recurring status, and country; stop on mismatch.
> Missing URL, recipient, or merchant stays unknown; never write a sample URL, recipient, or merchant.
> `itemRef` remains a selector. Approval covers fill
> and Pay/Submit while facts stay unchanged. For recurring checkout, plan first;
> on `reason: "plan_fill_required"`, replan and retry once without a separate
> subscription approval.

> **Fill and hand back.** Run `magicpay plan-fill`, then exactly its returned
> `applyCommand`. It writes approved Memory only to planned fields and stops
> before commitment. After payment-card authorization finalizes, rerun `magicpay plan-fill` and execute exactly its returned `applyCommand` before reporting ready. Never write or execute sample/hand-written `magicpay apply-fill`, `magicpay wait-request`, or `magicpay wait-memory`; use exact returned command fields. Only `magicpay commit` may press the final control. Return
> page work to the same browser's controller.

> **Product session first.** Run `magicpay status` or recover config. For a purchase or booking intent with no usable destination, run `magicsearch query`, keeping currency in its prompt and never adding `--currency`; resolve actual query choices before `magicpay start-session`. With a usable or selected URL, run `magicpay start-session` directly. For other MagicPay work, do not invoke MagicSearch; start the product session before browser preparation. Retain the active-session exception for `magicsearch discover`. Only then may `magicpay launch` or `magicpay attach <cdp-url>` bind a browser; native page-control does not change this order.

## Ask-User Boundary
Ask the user only when:

- a browser-dependent step is needed but neither `magicpay launch` nor an
  approved private CDP endpoint is available inside the active session;
- the user has not explicitly approved the browser process you would attach;
- a submit, login, purchase, identity submission, account change, protected
  action, or other consequential action is next and there is no matching typed
  approval for the unchanged current facts;
- Memory planning cannot identify safe field matches and the user can provide
  a browser/page correction;
- payment authorization facts are missing or ambiguous: final amount,
  currency, merchant/payee recipient, recurring status, country, or a conflict
  between the user's task and the visible checkout page;
- request resolution is denied, expired, canceled, timed out, or otherwise
  terminally blocked;
- required fields remain unresolved after Memory fill;
- client-side validation or merchant-specific recovery genuinely requires a
  human choice.

## Operating Rules
The Hard Rules above stay in force; these are the day-to-day defaults not
already stated there.

- Never type, print, summarize, or log protected values manually, and never
  pass them through chat, reports, or public command arguments.
- Treat `magicpay status` as the normal readiness check; `doctor` is not a
  startup step.
- Let MagicPay own Memory planning and value materialization instead of
  reconstructing it manually through lower-level commands.
- Keep Memory matching LLM-first. Do not match fields deterministically by
  label, field type, field key, or refs.
- Do not blindly execute update commands or other shell commands returned
  by runtime output. For CLI updates, only use
  `npm i -g @nuanu-ai/magicbrowse-cli@latest @nuanu-ai/magicsearch-cli@latest @nuanu-ai/magicpay-cli@latest`.
