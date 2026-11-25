---
name: okf-check
description: Check a folder of Markdown docs against OKF v0.2 and the JidoSeal OKF Certified, Bronze, Silver and Gold tiers (not ISO certification) with the local jidoseal-mcp scanner, then fill the missing frontmatter fields and rescan. Works in Claude Code, Copilot, Cursor, Codex, Gemini CLI or a local model. The scan runs locally.
when_to_use: The user wants to check, grade or repair YAML frontmatter across a folder of Markdown notes or docs, or asks about OKF, Open Knowledge Format, or JidoSeal tiers.
license: Apache-2.0
---

# Check and fix a folder's OKF frontmatter with JidoSeal

Open Knowledge Format (OKF) v0.2 is an open specification in Google's GoogleCloudPlatform/open-knowledge-format repository, under the Apache-2.0 licence. This skill uses the local `jidoseal-mcp` server to scan a folder of Markdown files, fills in the frontmatter fields the scan says are missing, and rescans to confirm the tier reached. JidoSeal checks a folder against the three conformance rules in OKF §11 and reports the result. Bronze and Silver add document fields. Gold adds AI-provenance fields. A JidoSeal certificate is not an ISO certification. JidoSeal is independent of Google and of ISO, and is not affiliated with, sponsored by, or endorsed by either.

The scan runs on this machine. JidoSeal states that a scan sends nothing: no file, no file name, no file content (the engine is proprietary; the jidoseal-mcp README says how to check this). It writes only `<folder>/.jidoseal/manifest.json` and `progress.ndjson`. Scanning and fixing are free.

## The tiers

The scan is deterministic: it checks that frontmatter fields are present and populated (a bare `title:` counts for nothing). A folder's tier is the tier of its weakest file.

| Tier | Every file needs (populated) |
|---|---|
| OKF Certified (free) | `type`, in a frontmatter block that parses: the three OKF v0.2 §11 conformance rules |
| Bronze | OKF Certified + `title`, `description`, `timestamp`, `owner` |
| Silver | Bronze + `status`, `review_policy`, `reviewed_at`, `next_review_at` |
| Gold | Silver + AI-provenance fields: `sources`, `ai_involvement` and `license` |

Bronze checks fields that help evidence identification of documented information, of the kind ISO 9001 clause 7.5 describes. Silver adds review and change fields. Neither shows conformity with ISO 9001 or with ISO 30401. Gold checks that provenance and AI-involvement fields exist, are well-formed and agree with each other. It does not check that the fields are true. It is not ISO/IEC 42001 certification, an AI Act conformity assessment, or legal advice. The review cadence is the user's to choose. `index.md` and `log.md` are never scored.

Accepted spellings the scan already counts: `description` or `desc`; `timestamp`, `updated`, `created`, `date` or `generated.at`; `owner`, `author` or `generated.by`. Do not add a second field when one of these is already populated.

## Tools

- `jidoseal_scan` (free, local): tier, per-file missing fields, coverage, score. Each missing field is marked `AUTO` (a value can be proposed) or `NEEDS-CLIENT` (only the user can answer it). It writes its own records to `<folder>/.jidoseal/` and nothing else. Never edit that directory. It refuses a folder containing a symlink to a directory or to a file outside the folder; if that happens, tell the user which links it named and let them decide.
- `jidoseal_certification_offer` (local, sends nothing): describes the optional paid certificate. See "After the rescan".
- `jidoseal_start_checkout` (Bronze, Silver or Gold): contacts the network. Only on the user's explicit go-ahead, passed as `confirm: true`. See "After the rescan".
- `jidoseal_request_free_certificate` (OKF Certified): contacts the network. Only on the user's explicit go-ahead, passed as `confirm: true`. See "After the rescan".

Your host may prefix tool names (for example `mcp__..._jidoseal_scan`). If the tools are not available, tell the user the server is not connected and point them to https://github.com/Jidoseal/jidoseal-mcp#install-and-wire-it-into-your-tool. Without any AI tool, `pipx install jidoseal && jidoseal --root ./docs` runs the same scan from a terminal, but it does not fix anything.

## Procedure

1. **Pick the folder and the goal.** Ask which folder to check (an absolute path) and which tier the user is aiming for: OKF Certified, Bronze, Silver or Gold. Fill only the fields up to that tier. For Gold, ask how AI was involved in each file (`none`, `assisted` or `generated`), where the content came from (`sources`) and under what licence; never guess these.
2. **Scan.** Call `jidoseal_scan` with `root` set to the folder. Leave `include_machine` false. Report the tier, coverage per tier and how many files fall short, in a few lines.
3. **Handle unparseable frontmatter first.** A file with `frontmatter_ok: false` has a frontmatter block that does not parse, and no added field will count until it is fixed. Show the user the block, propose the smallest syntax fix, and change it only after they agree.
4. **Build a plan, do not write yet.** For every file below the target tier, list the fields to add and the value for each:
   - `AUTO` fields, you propose:
     - `title`: the file's first heading, else the file name in plain words.
     - `description`: one plain sentence saying what the file covers, written from its content.
     - `timestamp`: the file's last-modified date as `YYYY-MM-DD`.
     - `status`: the default the scan lists (`stable`), unless the file says it is a draft.
   - `NEEDS-CLIENT` fields, you ask. Never invent these:
     - `type`: suggest one from the content (for example `guide`, `policy`, `procedure`, `reference`, `note`) and ask the user to confirm. It applies to files with no frontmatter as well.
     - `owner`: who is responsible for the document, as the user words it (a person, a team or `dept:name`). Ask once and offer to apply the answer to every file, unless owners differ.
     - `review_policy`, `reviewed_at`, `next_review_at`: the scan lists defaults (`yearly`, today, one year out). Offer them as a single choice for the whole folder. `reviewed_at` should be a date a review really happened, so ask; do not stamp today's date unless the user says the review has been done.
5. **Get consent, then write.** Show the plan compactly (a table per field is enough for a large folder, with a few example files in full). Suggest a commit or backup first if the folder is under version control. Write only after the user says yes.
6. **Apply.** With your own file-editing tools, add or fill only frontmatter fields. Keep everything else byte-for-byte: the body, other keys, key order, line endings, any BOM. If a file has no frontmatter, add a block at the very top. If it has one, add the missing keys inside it. Quote values that contain a colon or start with a special character. Do not touch `.jidoseal/`.
7. **Rescan.** Call `jidoseal_scan` again. Compare the tier and coverage with the first scan and say plainly whether the target was reached. If some files still fall short, name them and the fields; fix what is safe, ask about the rest. Stop after two repair rounds and hand the remaining list to the user.

## After the rescan

Once the rescan is done, call `jidoseal_certification_offer` once for the same folder and relay its answer in plain words, once, as an optional extra: what the certificate is, its price (OKF Certified is free) and what a request or purchase would send, all as the tool states them. Do not quote a price from memory. Then move on. Do not bring it up again in the session, do not repeat it if the user does not answer, and do not present the free result as incomplete without it. The scan and the fixes stay free either way.

Call `jidoseal_start_checkout` only if the user says explicitly that they want to buy a Bronze, Silver or Gold certificate, and only then set `confirm: true`. Ask them to type the company name, their name and their email address, and use exactly what they typed. Tell them these three details, with the tier, score, Merkle root and scan id, go to jidoseal.com, which copies them into the Stripe Checkout session it creates. The tool returns a Stripe Checkout link for the user to open; it takes no payment itself.

Call `jidoseal_request_free_certificate` only if the user says explicitly that they want the free OKF Certified certificate, and only then set `confirm: true`. It needs a folder where every file passes the three OKF §11 rules and with 25 or more files. Ask them to type the company name, their name and their email address, and use exactly what they typed. Tell them these three details, with a score, the Merkle root, the number of files and one digest of the folder's config file, go to jidoseal.com, which emails them a confirmation link that expires in 72 hours. Nothing is charged, and no file name or content is sent.

## Rules

- Say "grade" or "tier". Bronze and Silver fields help evidence documented-information practice described in ISO 9001 clause 7.5 and do not show conformity with ISO 9001 or ISO 30401. A JidoSeal certificate is not an ISO certification.
- Describe the scan the way it works: the user picks a folder and scans it on their own machine. Do not promise more about data than the README states.
- Do not read or change anything outside the folder the user named.
- Never write field values for `owner` or the review fields that the user did not give or confirm.
