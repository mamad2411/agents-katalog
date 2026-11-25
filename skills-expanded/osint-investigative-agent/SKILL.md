---
name: osint-investigative-agent
description: >-
  Plan and document privacy-respecting investigations using public, lawfully accessible sources. Use for organization and domain research, public-interest reporting, source verification, public document analysis, and investigations into a person's own digital footprint or a consenting subject. Do not use to identify, locate, track, profile, or expose a private person, or to obtain credentials, bypass access controls, or exploit systems.
---

# OSINT Investigative Agent

A careful workflow for answering a defined question from public sources. The goal is a concise, reproducible account of what sources establish, what is inference, and what remains unknown. Minimize collection and avoid turning scattered clues into a dossier on a private person.

## Scope and boundaries

Proceed only when the purpose and subject fit one of these scopes:

- An organization, public-facing service, public-interest issue, or domain researched for a legitimate reporting, research, or defensive purpose.
- The requester's own digital footprint, or a person who has clearly consented to the specific research.
- A public figure, only for information relevant to their public role and from sources intended for public access.

Do not help identify an anonymous or pseudonymous private person, find their home or real-time location, infer sensitive traits, map their family or private associates, monitor their routine, or compile contact details for targeting. Do not use leaked or stolen datasets, credential dumps, private groups, account recovery or contact-sync features, deceptive pretexts, or data broker lookups to expose personal information. If a request crosses these boundaries, explain the limit briefly and offer a safer alternative such as researching an organization, verifying a public claim, or helping the person audit their own exposure.

For technical research, stay within public registries, indexes, archives, and documents. Do not scan, enumerate, fingerprint, or send crafted requests to a target's systems; do not evade rate limits, access controls, or blocks. A query against a search index is not permission to interact with the indexed host. Respect source terms, robots directives where applicable, copyright, and applicable law. If scope or authorization is unclear, narrow the work to public-source context that does not expose or target a person.

## Workflow

### 1. Define the question and collection limits

Write down the question, subject type, time window, intended use, allowed sources, and excluded data. Collect only what is needed to answer the question. Do not broaden from one selector into unrelated people or sensitive personal information. Prefer aggregate or organization-level findings where they answer the question.

### 2. Build a source plan

Use sources in roughly this order:

1. Primary records and first-party statements (registries, filings, official documentation, signed releases, or the organization's own public pages).
2. Reputable reporting and research with named methods and sources.
3. Search indexes, public archives, and specialist databases as discovery aids.

Treat search snippets, reposts, scraped profile sites, and AI-generated summaries as leads, not evidence. Confirm important claims at the underlying source. Check source publication and event dates separately, and note when a page may have changed since capture.

### 3. Search and pivot proportionately

Use narrowly scoped search terms based on the stated question. For an organization or domain, reasonable public-source pivots can include official filings, published contact channels, RDAP, DNS and certificate-transparency records, public code repositories, and archived versions of the organization's own pages. For public documents, inspect ordinary metadata only when relevant to provenance or authenticity.

Do not perform broad handle permutations, search for a private person's associates, exploit account recovery or address-book discovery, or use exposed personal identifiers to resolve identity. For organization or domain research, do not infer asset ownership from a shared IP, analytics ID, name, or timestamp without strong, independent evidence and a clear public-interest need. Never use those pivots to resolve a private person's identity.

For cybersecurity work, passive public-source review can establish what is indexed or published. It cannot establish that a service is vulnerable or authorized for testing. Refer active validation to an explicitly authorized security assessment.

### 4. Record and assess evidence

Keep a finding log with one claim per row. Record:

| Field | What to record |
| --- | --- |
| Claim | A neutral, narrowly worded statement |
| Source | Publisher, title, direct URL, and source type |
| Dates | Publication/event date and retrieval time in UTC, if available |
| Support | Relevant excerpt or short paraphrase and archive/capture reference |
| Assessment | Fact, inference, or unresolved lead; confidence and rationale |
| Limits | Missing context, possible staleness, conflicts, and alternative explanations |

Preserve only the minimum evidence needed to make the result reviewable. Do not copy sensitive personal data into notes or outputs unless it is essential, within scope, and safe to disclose. Never reproduce passwords, access tokens, private keys, or other credentials. A URL and retrieval time improve reproducibility; they do not by themselves prove authenticity or chain of custody.

### 5. Corroborate and separate fact from inference

Use independent sources, not multiple pages repeating the same underlying claim. Assess source reliability separately from whether a particular claim is credible. Explain what would change the assessment. Avoid numerical certainty that the evidence cannot support.

Do not claim identity or ownership from a single match. Similar names, reused handles, shared hosting, privacy-protected registration, and copied content are common. If attribution is not necessary to the question, leave it out. If it is necessary, state the competing explanations and keep the confidence proportionate to the evidence.

### 6. Report and minimize

Answer the original question first. Include only relevant findings, methods, source links, confidence, material conflicts, and gaps. Avoid publishing personal contact details, precise personal locations, security-sensitive infrastructure details, or a step-by-step trail that would enable harassment or intrusion. Give the subject or organization a fair chance to respond when the work is consequential and the context allows it.

## Suggested report format

```markdown
# Public-source research: [question or subject]

- **Assessment date:** [YYYY-MM-DD UTC]
- **Scope and purpose:** [brief statement]
- **Sources reviewed:** [source types and time window]

## Summary
[Direct answer, with the most important qualification.]

## Findings
| Claim | Evidence and source | Assessment | Confidence and limits |
| --- | --- | --- | --- |

## Conflicts and gaps
[What is unresolved, missing, stale, or disputed.]

## Method and exclusions
[High-level method; note important data or methods excluded for scope/privacy.]
```

## Quality checks

Before returning a report, verify that:

- Each material claim links to the source that directly supports it.
- Facts, source claims, and your own inferences are visibly distinct.
- Dates, time zones, attribution, and confidence are not overstated.
- Repeated or derivative sources are not counted as independent corroboration.
- The report answers the stated question without unnecessary personal data.
- No step instructs the reader to contact, track, compromise, or probe a target.

## Helper scripts

The scripts in [`scripts/`](scripts/) use built-in APIs available in Node.js 18+ and emit JSON. The workspace package follows this repository's Node.js 20+ minimum. They support public-source research about an organization or domain and are designed to avoid exposing personal details or credentials. They do not replace the scope limits above.

- [`favicon-shodan.js`](scripts/favicon-shodan.js) reads a local favicon and calculates its signed MurmurHash3 fingerprint using RFC 2045 Base64 formatting. It makes no network request and does not generate queries for locating origin servers.
- [`ct-subdomain-enum.js`](scripts/ct-subdomain-enum.js) searches public certificate-transparency entries for a domain and validates candidate names against the exact root-domain boundary. It does not resolve DNS by default; `--resolve` optionally queries A records and should be used only for an organization domain in scope.
- [`github-patch-recon.js`](scripts/github-patch-recon.js) downloads a public GitHub commit patch, scans added lines for common credential patterns, and reports only file, line, and rule. It does not print author names, email addresses, or matched values. Treat matches as leads and never test or use them.
- [`email-recon.js`](scripts/email-recon.js) inspects public MX and TXT records for an organization domain and reports recognized mail/service markers without printing raw TXT values. It accepts a domain, not a personal email address, and does not query Gravatar or identify account owners.
- [`exif-gps.js`](scripts/exif-gps.js) reports ordinary EXIF fields for a local image and indicates whether GPS data exists while redacting exact coordinates by default. To reveal GPS for an image you own or have permission to inspect, set `OSINT_GPS_ACK=self-or-consented` and pass `--show-gps`. The optional EXIF parser can be installed for local use with `npm install --no-save --package-lock=false exif-parser`.

Examples:

Run these commands from `skills/osint`, or prefix each script path with `skills/osint/` when running from the repository root.

```sh
node scripts/favicon-shodan.js ./favicon.ico
node scripts/ct-subdomain-enum.js example.org
node scripts/ct-subdomain-enum.js example.org --resolve
node scripts/github-patch-recon.js https://github.com/OWNER/REPO/commit/COMMIT_SHA
node scripts/email-recon.js example.org
OSINT_GPS_ACK=self-or-consented node scripts/exif-gps.js ./my-photo.jpg --show-gps
```

The network-backed helpers use public endpoints or DNS and may be subject to provider rate limits or availability. Run them only for the scoped organization/domain or public repository relevant to the user's request; keep result files private when they contain infrastructure details.

## Reference guides

These guides provide detailed source-selection, interpretation, and reporting practices for common OSINT domains. Use them alongside the scope and privacy rules above; they do not authorize collection or interaction that those rules exclude.

- [Corporate and financial records](references/finint-corporate.md) explains how to search and validate legal-entity registries, filings, ownership claims, LEIs, trade datasets, and financial disclosures while handling jurisdictional gaps and name collisions.
- [Geospatial and telemetry data](references/geoint-telemetry.md) covers imagery provenance, map comparison, metadata and timestamp limits, satellite and public transport telemetry, location uncertainty, and safe precision in reporting.
- [Network and edge records](references/network-edge.md) covers RDAP, DNS, certificate-transparency, routing, hosting, and public-index records, including historical data, shared infrastructure, and the limits of ownership inference.
- [Telecom records](references/telecom-hlr.md) explains numbering plans, portability, carrier data, public business listings, subscriber-data risks, and safe responses to phone-account security incidents.
- [Crypto and blockchain records](references/crypto-forensics.md) provides a workflow for reading transactions, token and contract events, bridges, custodial services, labels, clustering heuristics, and attribution uncertainty.
- [Messaging services and access-limited sources](references/closed-networks.md) covers public-channel provenance, identifiers, deleted and indexed material, access boundaries, and safe handling of illicit or exposed content.
