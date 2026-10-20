---
name: analyzing-device-images-as-cases
description: 'First-pass analysis of a computer, server, or phone forensic exhibit (检材) — a whole disk image, server image, phone image, or phone backup — by examining it as a parsed forensic case: search and read the extracted chats, calls, contacts, accounts, transactions, app data, databases, media and files, plus the exhibit''s raw filesystem under /evidence_mounts/. Use this FIRST for any "analyze this computer / server / phone 检材" question, before dropping to lower-level tools that target a single loose artifact and before booting the image. NOT for a single loose artifact file (one APK / one database / one capture); and for a server question, boot/emulate only AFTER this pass — when the answer is runtime-only state the parsed case cannot supply, or when the task is to rebuild/restore/run the exhibit''s own services (重建网站/还原数据库), which is done inside the emulated guest, never on the analysis workstation.'
domain: cybersecurity
subdomain: digital-forensics
tags:
- disk-image
- phone-image
- case-analysis
- chat-records
- evidence-triage
- mobile-forensics
version: 1.2.0
author: honglian
license: Apache-2.0
---

# Analyzing Device Images as Forensic Cases

Most "analyze this computer / phone 检材 (exhibit)" questions are answered fastest by letting the forensic suite parse the **whole exhibit** into a structured case — the extracted chats, calls, contacts, accounts, transactions, app data, databases, media and files — and then querying that parsed case, instead of hand-parsing raw artifacts. This playbook is the **first pass** for such exhibits. It chains case preparation with case analysis and handles the three states of the analysis environment.

## When to use this (and when not)

Use this FIRST when the evidence is a **whole device exhibit** and the question is about its contents:

- A computer / disk image, a **server image**, a phone image, or a phone backup.
- Communications (chats, calls, SMS), contacts, accounts, transactions, app / user data, media, files, timeline.
- Anything on the exhibit's filesystem — web application source and config, databases, logs, cron / systemd units, installed packages. The parsed case mounts the raw filesystem at `/evidence_mounts/`, so you do not need to boot the image to read its files.

It is the **first pass even when a lower-level skill also exists**: parse the whole exhibit as a case first, then drop to a specific skill only if the parsed case does not answer the question, or the evidence turns out to be a single loose artifact.

Do **NOT** use this for:

- A **single loose artifact file** — one APK, one database, one network capture. Use the matching specific skill instead (mobile-app-package / sqlite-database / network-traffic …).

A server image is **not** an exception — parse it here first, like any other exhibit. Boot it only afterwards, and only when (a) the answer is **runtime-only state** the parsed case cannot supply — which services / processes are actually running, which ports are actually listening, the effective configuration after startup — or (b) the task is to **rebuild / restore / run the exhibit's own services** (重建网站、还原数据库、让系统跑起来登录后台): use this pass to locate the pieces (web root, DB config, backup dumps), then do the reconstruction itself INSIDE the booted guest — never by installing server software or Docker stacks on the analysis workstation. In either case open the `investigating-disk-images-by-emulation` skill and follow it. The same holds for a Windows image.

## The analysis environment (two states)

This path uses a `ges` command-line tool that drives the "火眼证据分析" (GoldenEyes) suite. When GoldenEyes is installed, `ges` has already been put on the PATH for your `exec` tool. **You do not start GoldenEyes yourself** — the `ges` CLI launches and connects to the suite on its own (no `open_application` call). Just run the `ges` commands and let them bring the suite up as needed.

1. **`ges` works** → proceed with the chain below. Because `ges` auto-starts the suite, a first command that has to spin it up may take a while — let it block and do **not** give up on the first slow call.
2. **`ges` is not found / not callable** → GoldenEyes is not installed (or it was just installed and a new session is needed to wire it up). Do **NOT** silently fall back to offline analysis. First guide the user to install "火眼证据分析" (GoldenEyes) from the application library; once installed, retry the chain. Only if the user cannot or will not install it, fall back to offline analysis (see below).

## The chain: prepare the case, then analyze it

Do not restate the `ges` command details here — they track the CLI version and belong to the two skills below. Open each skill and follow its own procedure.

1. **Prepare the case** — open the `ges-case-management` skill and follow it. It checks the current context, then: uses an already-parsed case if one is open; if you were given an **exhibit file path**, creates and imports it (the suite is launched and the exhibit is parsed — this can take a while, so let it block and do **not** poll task APIs); if you were given a **case number**, opens that case.
2. **Analyze the parsed case** — once parsing is complete, open the `ges-case-analysis` skill and follow it: start from the case context, then search and read the extracted data (communications, accounts, transactions, app data, databases, files). Access the case's virtual paths **only** through `ges`, never with local read / grep.

Base every answer on what `ges` returns, and state which record it came from.

## Nested images inside the exhibit (VM / emulator disks)

Parsing a computer exhibit often surfaces **nested disk images** — virtual-machine or emulator disks (VMDK / VDI / VHD / qcow2; VirtualBox, VMware, Hyper-V, 雷电/LDPlayer, 夜神, MuMu …), typically listed by the suite's nested-evidence recognition (嵌套证据识别). A nested image is itself a **whole-device exhibit**. When the answer likely lives inside one (e.g. an app installed in an emulator), recurse this same playbook:

1. If the parsed case already contains the nested image's **extracted contents**, query them like any other case data.
2. If the case merely **recognized** the nested image (a listing entry such as a `data.csv` row, with no extracted contents), **import the nested image itself as an additional evidence**: open the `ges-case-management` skill and follow its evidence-import procedure against the nested image's path, let the suite parse it, then query the parsed results. Note that `ges glob` / `ges grep` / `ges search` only see parsed case records (`/case/`) and mounted filesystems (`/evidence_mounts/`) — they cannot see inside an unparsed image file, so a "no matches" for a file you expect (e.g. `*.apk`) is a signal to import the nested image, after which the SAME search will cover its contents.
3. Once the target artifact is located (an APK, a database, a capture …), export **that single artifact file** (e.g. `ges copy`) if the follow-up skill needs a local path, and hand off to the matching specific skill as described below.

**Never hand-unpack a disk image.** Do not copy a VM / emulator disk out of the evidence, and do not open any disk image with archive tools (`7z x` and the like) — not even "just to pull one partition". VM disks are usually **sparse**: a 155 MB `.vmdk` can hold a partition whose *logical* size is 137 GB (7-Zip lists this as `Size` vs `Packed Size`), and extraction materializes every empty block — it will fill the local system disk and crash the analysis environment (this has actually happened: ENOSPC, session lost). Parsing disk images — nested or not — is the suite's job, never the shell's.

## If the parsed case does not answer it → drop to the specific skill

The parsed case is a triage layer, not the only tool. If, after parsing, the question targets a single artifact the case did not fully cover — decrypt an app's bundled resource, recover a database key, deep-decompile an APK, parse a capture — switch to the matching specific skill (mobile-app-package / sqlite-database / network-traffic …) and continue there.

## Offline fallback (last resort)

Only when GoldenEyes genuinely cannot be installed or used: analyze the exhibit at the file level with `exec` and forensic CLIs, and state clearly that 火眼 case analysis was not possible and that what follows is a more limited, file-level analysis.

## Output

- Answer in the conversation; simple questions need no local report.
- Write any derived files you generate into the **workspace** directory.
- The **exhibit / source image stays in place, read-only** — never copied into the workspace, never modified.
