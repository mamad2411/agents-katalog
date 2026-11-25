---
name: analyzing-mobile-app-packages
description: 'Mobile-app forensics — analyze an Android APK (or another mobile package such as XAPK / IPA / mini-program) as forensic evidence. Use for ANY APK / mobile-app question: package metadata & attribution (package name, version, signatures, permissions, SDKs, 调证 / evidence-request values, hardening, entry Activity), decompiled source structure, malicious behaviour, decrypting bundled assets, and runtime / on-device app-data values. Import the package into the dedicated mobile-app analysis capability and query it there FIRST — do NOT hand-roll offline decompilation unless that capability is unavailable. 中文触发词: 分析 APK/APP/应用/安装包/小程序包的任何取证问题(元数据、源码、运行时数据),先用本 skill,禁止手写脚本离线解析。'
domain: cybersecurity
subdomain: digital-forensics
tags:
- mobile-forensics
- android
- apk
- app-analysis
- malware-analysis
- decompilation
version: 1.1.0
author: honglian
---

# Analyzing Mobile App Packages

For mobile-app forensics — an Android `.apk` / `.xapk`, an iOS `.ipa`, a mini-program package — the authentic and most reliable way to answer a question is to **import the package into the dedicated mobile-app analysis capability and query it there**: normalized static analysis (identity, permissions, SDKs, hardening, Activities), full source decompilation with a searchable class/method index, and dynamic unpack/dump of runtime artifacts on a device. This playbook drives that chain and handles the three states of the analysis environment. Hand-rolling `apktool` / `jadx` offline is only a fallback, for when that capability is genuinely unavailable.

## When to use this

If the package has **not been isolated yet** — the APK sits somewhere inside a computer / phone exhibit or a VM / emulator disk — do NOT hunt for it by hand-unpacking images with archive tools: run the whole-exhibit pass (`analyzing-device-images-as-cases`) first to locate and export that one package file (it also covers nested emulator disks), then return here with the package's local path.

For essentially every APK / mobile-app question, go through the dedicated capability first — do **not** jump straight to manual `apktool` / `jadx` / `aapt`. It covers, among others:

- **App identity / metadata** — package name (Application ID), app name, version, signatures, hashes.
- **Manifest facts** — the entry (main) Activity's full class name, declared permissions (and how many are dangerous/sensitive), exported components.
- **Third-party & attribution** — bundled SDKs, providers, packer/hardening, suspected forensic clues / 调证 (evidence-request) values.
- **Source-level questions** — locate the class/method implementing a behaviour (e.g. the SMS-interception receiver), find a hard-coded upload / C2 URL, locate the routine and key that decrypt a bundled asset (e.g. `assets/config.enc`).
- **Produced / runtime values** — the decrypted *content* of an encrypted asset, a database encryption key (e.g. a SQLCipher key for `stolen.db`), exfiltrated contacts, the original user inputs (username, phone number) the app captured.

Most identity / manifest / permission / SDK / source-structure questions are answered statically, from the package itself. But some questions ask for a **produced or runtime value**, and these must NOT be answered by reading or guessing from static source:

- The **decrypted content of an encrypted asset** (e.g. the plaintext of `assets/config.enc`) is a value you must actually *produce* — by running the decryption (reproduce the routine with the key recovered from source, or read the runtime-decrypted data), never by describing the algorithm or inferring the plaintext.
- **On-device app-data** — a database encryption key (e.g. for `stolen.db`), exfiltrated contacts, the original user inputs the app captured — exists only after the app has run on a device (emulator or physical). Obtain it by selecting a device and dumping the app's data directory (the analysis capability manages device selection and unpacking); never fabricate it from static decompilation.

## The analysis chain (main path)

When the capability is available, a `thunder-app-analysis` skill is present among your skills — it drives `thunder-app-cli` against a running `Thunder-App-Analysis` backend service. **FIRST open and read that skill, and follow its Decision Workflow for the exact commands, arguments, and ordering.** This playbook only routes you to it; it is NOT a command reference. The stages below are a high-level map of *which stage answers which kind of question* — do not invoke any CLI command directly from this list; get the real commands from that skill.

Stage map (see the `thunder-app-analysis` skill for the actual commands):

1. **Open/create a case, then add the package as evidence.** The source file is referenced in place by path (a local path or a URL) — keep it read-only and in place; this is not a file upload.
2. **Static identity & manifest facts → static-analysis queries.** Any package metadata / attribution field: package name / version; Activities (including the entry/main Activity), signatures, hardening; the count of dangerous/sensitive permissions; bundled SDKs / providers / suspected clues / 调证 values.
3. **Source-level questions → decompile and search the source index.** Locate the implementing class/method (e.g. the SMS-interception receiver), the hard-coded upload / C2 URL string, or the routine and key that decrypt a bundled asset.
4. **Produced / runtime values → run the operation.** Decrypt an encrypted asset to its actual plaintext; for on-device data (DB keys, captured inputs, stolen contacts) select a device and unpack/dump the app's data directory. The deliverable is the produced value, not the algorithm.
5. **Report the findings — see "Answering & output" below.** Base every answer on the structured results the skill returns; never invent results.

### If the analysis backend is installed but not started

`thunder-app-cli` talks to a backend service ("master") that **must already be running** (default endpoint `http://127.0.0.1:9112`). If a command (e.g. `health`) fails with a **connection error / the backend is not reachable** (connection refused on its port), the "雷电APP智能分析" (AppAnalyzer) application that hosts that backend is not running. Do **not** treat this as a real failure and do **not** fall back to offline analysis. Instead:

1. Call the `open_application` tool with the application identifier `appanalysis` (equivalently `AppAnalyzer`) to start "雷电APP智能分析".
2. Wait a few seconds for it to initialize and for its backend to come up on port `9112`.
3. Retry the original command (a few attempts at most); re-run `health` to confirm the backend is reachable before continuing.

Only conclude there is a real problem if the backend is still unreachable after the app has been started and given time to become ready.

## If the capability is NOT available

> If there is no `thunder-app-analysis` skill among your skills, the "雷电APP智能分析" (AppAnalyzer) application that provides it is not installed. Do NOT silently fall back to offline analysis. First guide the user to install "雷电APP智能分析" from the application library; once installed, the skill becomes available and you resume the analysis chain. Only if the user cannot or will not install it, fall back to offline, by-hand decompilation of the package with `exec` and Android CLIs, and clearly state that the full analysis capability was not available (and that runtime / on-device values may not be recoverable offline).

You cannot install the application yourself. Use the conversation and the `ask_user` tool to confirm with the user and guide them to install "雷电APP智能分析" from the application library, then resume the chain once it is available.

## Offline fallback (last resort)

Only when the user genuinely cannot or will not install "雷电APP智能分析":

- **Static facts** can often still be answered by hand: unzip the package and read `AndroidManifest.xml` for the package name, the launcher (main) Activity, and declared permissions; decompile with `apktool` / `jadx` (or read the dex/smali) to locate a behaviour's class, a hard-coded URL, or the routine and key that decrypt a bundled asset. If a needed CLI is missing, install a portable build into the bundled tools directory (see the environment instructions) and call it from `exec`.
- **Produced / runtime values** are NOT facts you read off the source. If you recover the key and algorithm from the decompiled source you may *reproduce* a decryption yourself with `exec` (e.g. `openssl` / a small Python script) and report the literal output you produced. But values that exist only after the app has run on a device — the data-directory contents: captured user inputs, stolen contacts/phone numbers, runtime-bound database keys — are usually **not recoverable offline**. If you cannot run the app, state plainly that the value is unrecoverable offline; never report a value read or guessed from source.

Always state clearly that the full analysis capability was not available and that what follows is an offline, by-hand analysis with its inherent limits.

## Answering & output

- **Answer in the conversation by default.** For most questions the user just wants the answer in chat — state it directly and cite the basis (the command and the result it came from, or the file/line for offline analysis). Do NOT create a report file or other workspace artifacts for a simple question.
- **Write files to the workspace only when the deliverable is itself a file** — e.g. the user explicitly asks for a report/export, or you dump artifacts (extracted source trees, the app's data directory, carved files) too large to inline. Put those under the workspace directory.
- The **source package stays in place, read-only** — never copied into the workspace, never modified.
- State the basis for every conclusion (which command/query returned it, or which decompiled file).
