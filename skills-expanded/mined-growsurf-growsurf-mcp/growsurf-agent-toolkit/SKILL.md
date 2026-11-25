---
name: growsurf-agent-toolkit
description: Use when an agent needs to create, configure, verify, or operate a GrowSurf referral or affiliate program through the GrowSurf MCP/REST API. Triggers include "create a referral program", "create an affiliate program", "set up GrowSurf", "embed the referral widget", "configure rewards", "wire webhooks", "verify my program", "screenshot proof", or "read GrowSurf analytics".
---

# GrowSurf Agent Toolkit

Use this skill to turn a user goal into a real GrowSurf program, not just API calls. Prefer the GrowSurf MCP tools when available; otherwise use the REST v2 API with the same order and checks.

## Ground Rules

- Use the user's own GrowSurf API key. If they do not have an account, have them sign up at `https://app.growsurf.com` and create an API key in the dashboard. If they cannot store a secret past the current conversation, have them connect `https://mcp.growsurf.com` and sign in instead.
- If the user wants to work on an existing program and did not provide a `campaignId`, call `growsurf_list_campaigns` first and pick or confirm the target program.
- If the user wants to inspect or operate on an existing participant and did not provide a participant ID/email, call `growsurf_list_participants` first. If they gave an identifier from their own system, such as a customer ID stored in participant metadata, pass it as the `metadata` filter instead of paging.
- After `growsurf_create_campaign`, pass the returned `id` as `campaignId` to every campaign-scoped tool. Do not rely on a process-level default after creating a new program.
- Campaign create seeds type-specific starter content across Design, Emails, Options, Installation, rewards, and the GrowSurf Window. Fetch and review it before patching. Preserve starter content unless the user asks for a specific change.
- Treat starter content as the default source for Window copy, referred-friend copy, email copy, share settings, landing-page content, and rewards. Do not rebuild the program from scratch unless the user asks for a custom program.
- Keep rewards conservative until the user confirms money movement, payout funding, tax collection, and approval settings.
- Fetch before patching large config surfaces. Use `growsurf_get_campaign_design`, `growsurf_get_campaign_emails`, `growsurf_get_campaign_options`, or `growsurf_get_campaign_installation`, then patch only the fields that must change.
- Finish by proving what changed: fetch the campaign, key configs, and rewards again. Review the returned settings before reporting back.
- Show the draft, do not just describe it. After a draft program is saved, and again when later work changes or installs a browser-visible GrowSurf flow, call `growsurf_capture_referral_flow_screenshots` and show the returned referrer Window and referred-friend images inline as GrowSurf preview screenshots. Skip this for read-only lookups, config summaries, and server-only API tasks. If they want proof of their own installed site, use the host agent's browser automation tool, such as Playwright or a built-in browser tool, against the real installed page. Do not substitute a mock page unless the real page is unavailable, and say so if that happens.

## Referral Program Workflow

1. Create the program:
   - Tool: `growsurf_create_campaign`
   - Minimum body: `{ "type": "REFERRAL", "name": "...", "companyName": "..." }`
   - Capture the returned `id`.

2. Inspect defaults:
   - `growsurf_get_campaign` with `campaignId`
   - `growsurf_list_campaign_rewards`
   - `growsurf_get_campaign_design`
   - `growsurf_get_campaign_emails`
   - `growsurf_get_campaign_options`
   - Check GrowSurf Window header/share copy, referred-friend and landing-page content, email templates, rewards, and install settings.

3. Configure only what the user requested:
   - Design: brand colors, copy, GrowSurf Window sections, share channels, landing-page/referred-friend experience.
   - Emails: participant lifecycle email copy and enabled states.
   - Options: approval, fraud, referral cookie/credit windows, notification emails.
   - Installation: share URL, tracking method, referral trigger.

4. Confirm:
   - Fetch the campaign, Design, Emails, Options, Installation, and Rewards again.
   - Check that the referrer Window settings keep normal share options, not QR-only sharing.
   - Check that the referred-friend settings include the needed visible motivators, such as sticky banner and inline heading. The browser tab title motivator should be configured when relevant.
   - Summarize the referrer view, referred-friend view, reward state, install step, and any user action still needed.

## Affiliate Program Workflow

1. Create the program:
   - Tool: `growsurf_create_campaign`
   - Minimum body: `{ "type": "AFFILIATE", "name": "...", "companyName": "...", "currencyISO": "USD" }`
   - Capture the returned `id`.

2. Inspect the default commission and payout posture:
   - `growsurf_list_campaign_rewards`
   - `growsurf_get_campaign_options`
   - `growsurf_get_campaign_design`
   - Check starter content for the affiliate portal, GrowSurf Window, commissions, payouts, participant settings, email templates, `affiliateApplicationMode`, and the GrowSurf Program Page.

3. Configure carefully:
   - Confirm commission basis, payout threshold, refund/hold period, participant auth, payout instructions, and tax-document collection before enabling anything that can create payable obligations.
   - Public applicants in `MANUAL_REVIEW` or `AUTO_APPROVE` must use the configured GrowSurf Program Page application flow. Do not use trusted REST Add Participant to bypass review.
   - Use direct participant enrollment only when the customer intentionally enrolls a known affiliate. Set `isAffiliate` explicitly.
   - Patch Options before publishing if the default payout/tax settings do not match the user's business.
   - Patch Design for affiliate portal sections: affiliate summary, commissions, payouts, participant settings, leaderboard.

4. Confirm:
   - Fetch the campaign, Design, Emails, Options, Installation, and Rewards again.
   - Check that the referrer Window settings keep normal share options, not QR-only sharing.
   - Check that the referred-friend settings include the needed visible motivators, such as sticky banner and inline heading. The browser tab title motivator should be configured when relevant.
   - Summarize the application mode, Program Page readiness, commission defaults, payout/tax readiness, portal sections, and remaining launch blockers.

## Common Tasks

### Embed The Widget

Use `growsurf_integration_guide` for the user's stack. If no stack is known, give the universal install snippet and ask where their signup event happens. Verify the installed script with the campaign's Installation config and the user's site URL when available. When placing or styling a GrowSurf Window launcher or embeddable element inside the user's app, use `frontend-design` or the closest available design-focused workflow before changing UI. If the user wants screenshot proof of the installed site, drive the real page with the host browser automation tool instead of asking them to inspect it manually.

### Design A Program

Before proposing rewards or a qualifying action, call `growsurf_program_design_advisor` with the closest `industry` and `goal`, plus any budget, business model, audience, and qualifying action the user gave, and follow its output. Turn the returned configuration plan into the create and patch calls above, and keep rewards non-awarding until the user confirms the incentive and its funding.

### Troubleshoot Referral Tracking

When referrals, participants, rewards, or emails misbehave, call `growsurf_troubleshoot_referral_tracking` with the matching `symptom` (or the problem as `description`), the `campaignId`, and the affected participant when known, then follow its output: run the checks in order with the named read tools before drawing a conclusion.

### Check Agent Steering

Use `growsurf_agent_program_creation_eval` when you need one-shot eval prompts or acceptance checks for program creation. A passing eval creates a program through MCP, reviews starter content, keeps rewards conservative, and verifies the config for visible motivators, share options, header copy, and clean public copy.

### Adjust Rewards

Use `growsurf_list_campaign_rewards` first. Prefer updating existing reward configs over creating duplicates. For new rewards, state whether the reward is visible, active, referrer-only or double-sided, and whether the value has tax-reporting implications.

To give some participants different rewards, such as partners, use a group. Call `growsurf_list_campaign_groups` first. `growsurf_create_campaign_group` creates an empty group. Add Campaign Rewards with the group's `groupId` only after the person confirms the amounts, and before adding participants or rules. Omit `rules` when creating the group; add them with `growsurf_update_campaign_group` after configuring rewards. Move existing participants with `growsurf_bulk_move_participants`. A move applies to new referrals only.

### Connect an Integration

Use `growsurf_list_integrations` first to see what the program can connect and what is already on. An
integration that is `connected` but not `enabled` needs switching back on, not reconnecting, and one
that is `autoDisabled` keeps its credentials but delivers nothing until the user reconnects it. Then
call `growsurf_get_integration_connect_link` and hand the user the link — connecting an account
happens in the GrowSurf dashboard, never through the API, and you cannot do it for them.

### Wire Webhooks

Use `growsurf_list_campaign_webhooks`, then create or update with the exact event list the user requested. Use `growsurf_test_campaign_webhook` after saving. Never expose or echo webhook secrets.

### Use A Custom Domain

Call `growsurf_get_campaign_custom_domain` first. If a different domain is already set, confirm before replacing it: `growsurf_set_campaign_custom_domain` removes the old domain right away. After you set the hostname, give the user the `CNAME` record from `dnsRecord` (`name` pointing to `value`) to add at their DNS provider. Then call `growsurf_verify_campaign_custom_domain`. If `isVerified` is still `false`, the record is wrong or has not propagated yet; check again later. Use `growsurf_remove_campaign_custom_domain` only when the user wants landing pages back on their GrowSurf URL.

### Manage Program Resources

Use `growsurf_list_program_resources` first. Create LINK resources with an HTTPS URL and TEXT
resources with plain text. For a FILE, read the local file, call
`growsurf_prepare_program_resource_file` with its safe file name, matching MIME type, and padded
base64 bytes. That tool requests the ticket and completes the host-allowlisted upload. Then pass its
`uploadTicket` and `uploadResult` unchanged to create or update. Never provide an upload URL or
credential. Files must use an allowed type, have a file name of 120 characters or fewer, and be 10 MB
or smaller. Keep unfinished resources as drafts, then fetch the list again to confirm title, type,
publication state, and order.

### Read Analytics

Use `growsurf_get_campaign_analytics`. Add `include=rates,statusCounts` for overall performance, `email` for email delivery metrics, and `engagement` for participant activity grouped by when portal views and share actions occurred. Use `growsurf_get_campaign_activation_analytics` for participants grouped by eligibility date with a fixed 7- or 30-day observation window. Referral cohorts use `enrolledAsAdvocateAt`; affiliate cohorts use `approvedAsAffiliateAt`.

Read `coverageStartAt`, `state`, and `reason` before interpreting a zero or null. Pre-coverage and unavailable values are unknown, not proof that an action never happened. For one participant, use `growsurf_get_participant_analytics` with `include=activation`; add `series` only when covered portal-view or share-action trends matter.

## Final Response Checklist

Include:

- Program type, name, and `campaignId`
- What was created or changed
- Reward and money-movement posture
- Installation or launch action still needed
- GrowSurf preview screenshots from `growsurf_capture_referral_flow_screenshots`, shown inline
- A What's next block: the Program Editor link `https://app.growsurf.com/editor/<campaignId>`, one question about who installs GrowSurf (the agent with approval, a developer invited at `https://app.growsurf.com/settings#team-members` with the Installation step link `https://app.growsurf.com/editor/<campaignId>/installation/instructions`, or the user), then integrations via `growsurf_get_integration_connect_link`
- Program Editor URL when the user wants to inspect design defaults

## One-Shot Eval Examples

Call `growsurf_agent_program_creation_eval` for the current referral and affiliate one-shot prompts. Pass `programType` to get only one type.
