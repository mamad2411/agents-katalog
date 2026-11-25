---
name: incident-response-bec
description: "BEC and AiTM incident-response skill for suspicious sign-ins, mailbox abuse, forwarding, inbox rules, session theft, token replay, consent abuse, and secondary phishing."
---

# Business Email Compromise and AiTM Analysis

## Mission
Determine whether a Microsoft identity and mailbox event is consistent with BEC, AiTM session theft, or another compromise pattern. Keep the assessment advisory; final decision belongs to the human analyst.

## Use when
- Suspicious sign-ins are paired with mailbox forwarding, inbox rules, or unexpected sent mail.
- A user reports phishing, strange mailbox behavior, or external recipients the user did not send to.
- The incident includes suspected session theft, token replay, or unauthorized app consent.
- The same workflow applies to non-Microsoft cases when equivalent sign-in and mailbox evidence exists.
- The Microsoft Incident Response Playbook at `https://github.com/crtvrffnrt/Microsoft-Incident-Response-Playbook/blob/main/README.md` can be used as an optional reference when current external context is available and would materially improve compromise assessment.


## Required context
- Preferred inputs: UPN, incident window, alert or incident ID, and any phishing message identifiers.
- If UPN is missing and Microsoft telemetry is required, ask for it before querying.

## Investigation flow
1. Confirm the compromise hypothesis
   - identify the first suspicious sign-in or mailbox event
   - note source IP, geo, ASN, device, client app, and MFA context
2. Extract all IPs from the prompt, phishing artifacts, logs, and mailbox evidence and enrich every unique public IP
   - classify each IP as public or non-public before enrichment
   - prefer `/root/Tools/IncidentResponseScripts/vpnchecker.sh <ip>` and `/root/Tools/IncidentResponseScripts/ipir.sh <ip>` for every public IP when present
   - keep the raw outputs and use them in the verdict
3. Review authentication
   - look for impossible travel, session reuse, token replay, claim-based MFA satisfaction, repeated MFA prompts, or suspicious non-interactive activity
4. Review mailbox and collaboration activity
   - check inbox rules, forwarding, transport rules, sent items, deleted items, search behavior, delegated access, and OAuth consent
   - look for MailItemsAccessed or equivalent mailbox access evidence when available
5. Review downstream actions
   - identify secondary phishing, data exfiltration, file sharing changes, role or group changes, and privileged app consent
6. Contain and preserve
   - preserve the suspicious events, then revoke sessions, reset credentials, remove malicious rules, disable forwarding, and remove unauthorized consent
   - isolate the host if endpoint evidence shows active malware or credential theft

## Identity and BEC Compromise Logic

For suspicious sign-ins, MFA anomalies, AiTM suspicion, token theft, mailbox abuse, or BEC cases, do not stop at the sign-in result.
Always try or help to evaluate:

- Whether the password appears compromised, especially when correct-password activity is followed by MFA denial, MFA fatigue, or blocked Conditional Access.
- Whether MFA was freshly performed, satisfied by claim, bypassed, not required, denied, or reused through an existing session.
- Whether the source IP, ASN, country, city, device, browser, user agent, app, and resource match the user's 14- to 30-day baseline.
- Whether session IDs, correlation IDs, or token identifiers link activity across unexpected IPs, apps, or non-interactive sign-ins.
- Whether phishing delivery, URL clicks, Safe Links activity, or suspicious mail interaction happened before the suspicious sign-in.
- Whether post-authentication activity occurred: mailbox access, MailItemsAccessed, inbox rules, forwarding, deletes, suspicious sends, OAuth consent, file downloads, Azure actions, or role changes.
- Whether mailbox persistence exists through forwarding, hidden inbox rules, delegates, SendAs/SendOnBehalf, mailbox permissions, OAuth apps, or Power Automate flows.
- Whether the case is confirmed compromise, suspected compromise, attempted compromise, historical activity, benign, or inconclusive.

## Public IP rule
- If a public IP is present anywhere in the prompt or evidence, enrichment is required before closing the assessment.
- `vpnchecker.sh` is the fast VPN and provider signal.
- `ipir.sh` is the deeper multi-source reputation and infrastructure scoring pass.
- A VPN, proxy, or datacenter result alone is not enough to call the IP malicious.
- Use the enrichment results together with sign-in behavior, mailbox activity, and timeline context.
- If the tools cannot be executed, state the limitation explicitly in the analyst note and continue with available telemetry.

## Microsoft Graph guidance
- Use `az rest` or the best available Microsoft telemetry path.
- Scope every query to the user and time window under investigation.
- Do not rely on the last sign-in date alone.
- Treat MFA as one control signal, not proof of safety.
- Do not alert the user before initial scoping if doing so could tip off an attacker.

## Evidence to preserve
- IPs, user agents, device IDs, session IDs, timestamps, and app IDs
- mailbox rule definitions, forwarding targets, and transport rule changes
- OAuth consents, delegated permissions, role changes, and group changes
- phishing message details or sender infrastructure when available

## Assessment output
- State whether the incident is confirmed, suspected, likely benign, or inconclusive.
- Separate facts from indicators and hypotheses.
- Explain whether the likely path is AiTM or session theft, mailbox compromise, or another access path.
- Include public IP enrichment results for every material public IP.
- List immediate containment actions and remaining gaps.
- Include optional generic memory candidates only for reusable investigation patterns, not case details, if the runtime supports memory.
