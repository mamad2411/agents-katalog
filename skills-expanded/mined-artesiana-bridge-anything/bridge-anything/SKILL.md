---
name: bridge-anything
description: Connect an app or agent to software that has no usable API by building a bridge (REST, MCP, CLI) next to it, using REA (Reverse Engineer Anything) to find where the data lives and how the software reads and writes it. Use when an app, automation or agent needs data from an on-premise or legacy system (practice management, dealer, tax, ERP or other desktop software), or someone wants an MCP server for such a system.
metadata:
  version: "1"
---

# Bridge Anything

A **bridge** is a small service that runs next to a legacy **system of record** and exposes its data through a typed **contract**: REST, MCP and optionally a CLI. Its first client is the user's own app or agent. You build it in seven steps. Each step ends on a completion criterion; finish it before starting the next one.

**Evidence** is the leading word of this skill. Every table, column, file, query and write path the bridge relies on traces back to something REA showed you (a schema dump, a SQL string in an assembly, a recorded file write) or to a document from the vendor. A mapping without evidence is a guess; mark it as an unknown and keep going.

Keep three files in the bridge repository from step 1 on:

- `BRIDGE.md`: the data map, each data area's mapping, the access path chosen and the evidence for each line.
- `UNKNOWNS.md`: open questions, each with the probe that would answer it.
- `DATA-PROTECTION.md`: what personal data the bridge touches and where it goes.

## Prerequisites

REA must be connected (`npx rea-agents setup`, then restart the agent). If REA tools are missing, load REA's own `reverse-engineer-anything` skill and follow its connection guide. Work on a **copy**: a test installation, a restored backup or a database snapshot. The live system of a practice or business is reached only in step 4, read-only, after the user says so.

## Step 1. Establish the right to do this

Ask the user, and record in `BRIDGE.md`:

1. Whose installation this is, and who agreed to the analysis (their own licence, or the licensed customer's written go-ahead).
2. The purpose: interoperability with the user's own software. That purpose is what the legal exceptions for reverse engineering protect.
3. Whether the vendor offers an API, SDK, export or partner programme, even a paid one.

Read [references/legal-and-data-protection.md](references/legal-and-data-protection.md) when any answer is unclear, when the data is health, financial or employee data, or when the user is in the EU.

The bridge uses the access a licensed user or administrator already has. When the only way in is past a licence check, an encrypted credential, DRM or another access control, the path ends there: the user asks the vendor or the customer's administrator for access instead (a database user, an export, a partner key).

**Done when** `BRIDGE.md` names the installation, the person who authorised the work, the purpose, and the vendor's official options with a link or "none found".

## Step 2. Find where the data lives

Point REA at the installation directory (`inspect_desktop_application`) and work outward: the database engine, its files, how the app connects, export folders, interface files. [references/find-the-data.md](references/find-the-data.md) lists what each common engine leaves on disk and which REA tool reads it.

**Done when** `BRIDGE.md` has a data map: engine and version, file or server location, how the app connects (with the config file or code location as evidence), and every export or interface folder found.

## Step 3. Map each data area

Agree with the user on the **data areas** in scope (for a medical practice: patients, appointments, diagnoses, invoices; for a dealer: vehicles, customers, work orders). For each area, record in `BRIDGE.md`:

- tables or files, key columns, IDs and how they are generated;
- how deletion works (hard, soft flag, archive table) and how changes can be detected (timestamps, row versions, sequence numbers);
- encodings, date formats, code tables and magic values;
- **how the app writes**: the SQL or file operations it performs, found in its data-access code with `inspect_managed_artifact` (.NET) or `open_binary` (native), and confirmed on the test installation by diffing the database before and after one action in the app, or with the engine's own trace (see the reference for each engine).

Run the read queries against the copy and compare the results with what the app shows on screen for three to five real records.

**Done when** every data area in scope has a mapping whose every line cites evidence, the on-screen comparison matches for each area, and whatever did not match is in `UNKNOWNS.md`.

## Step 4. Choose the access path per data area

Take the first path that works, per area:

1. Vendor API, SDK or documented export (`vendor_api_official` or `vendor_api_partner`).
2. A standard interface the app already speaks: interface files, import folders, industry formats (`file_export`).
3. Read-only database access through a dedicated database user, ideally on a replica or snapshot (`local_database_readonly`).
4. UI automation, when nothing else reaches the data (`ui_automation`).

Writes go only through a path the app itself uses and that you have recorded: its import function, its interface files, or its own SQL reproduced exactly with the same transaction boundaries, triggers and sequence updates. Otherwise the area stays read-only in this version.

**Done when** `BRIDGE.md` has a table of data area → access path → `read` or `read_write`, each with the reason, and the user has approved it.

## Step 5. Build the bridge

Write the contract first, then the code. [references/bridge-blueprint.md](references/bridge-blueprint.md) has the layout, the contract rules, write safeguards, packaging and the test setup.

**Done when** all of these hold:

- the test suite passes against a snapshot fixture of the copy;
- every endpoint and MCP tool links to its lines in `BRIDGE.md`;
- an agent connected to the bridge's MCP server answered one real question per data area on the test installation;
- `DATA-PROTECTION.md` lists every personal-data field the bridge returns, where it is sent, and how long anything is kept.

## Step 6. Connect the app

Wire the user's app or agent to the bridge: generate a typed client from `contract/` for the app, or register the bridge's MCP server in the agent. The app talks to the bridge only, never to the legacy database, so a vendor update changes the bridge and nothing else.

**Done when** the user's app or agent shows real data from the test installation through the bridge, at least one screen or answer per data area.

## Step 7. Share it (optional)

Ask whether others should be able to use the bridge: inside the user's own product, as open source, or listed on OpenCoupler, a marketplace where software companies and IT service providers look for integrations into systems without an open API. For OpenCoupler, follow [references/publish-to-opencoupler.md](references/publish-to-opencoupler.md). Whatever the channel, the description states what step 5 built and nothing more.

**Done when** the user has chosen a channel, or none, and has read and confirmed any public text before it goes out.
