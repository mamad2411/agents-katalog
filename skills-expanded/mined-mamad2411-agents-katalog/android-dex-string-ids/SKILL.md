---
name: android-dex-string-ids
description: >
  DEX string_ids triage for owned/lab Android reverse engineering: locate string pool
  entries, map to code xrefs, hunt URLs/secrets/flags, and handle obfuscation. Use with
  jadx/apktool/dexdump on authorized APKs/CTFs — not for piracy or unauthorized app cracking.
---

# Android DEX string_ids Triage

## Scope And Authorization

- **In scope:** APKs/DEXes you own, CTF samples, or authorized mobile assessments.
- **Out of scope:** Removing license checks on third-party software without permission.
- Keep malware samples in isolated VMs.
- Redact live secrets found in strings from public notes.
- Pair broader RE with `android-pentesting-tricks` / Ghidra skills as needed.

## When To Use

- Fast triage of interesting constants in `classes*.dex`.
- Hunting API endpoints, API keys, feature flags, crypto constants.
- CTF flag-in-strings or encoded string recovery.
- Comparing string pools across app versions.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Full Android pentest workflow | `android-pentesting-tricks` |
| Exported components focus | `android-exported-components` |
| Native .so RE | `Ghidra_IDAReverseEngineeringSkill` |
| R8 mapping recovery | `android-proguard-r8-mapping` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| DEX item | Role |
| --- | --- |
| `string_ids` | Index of unique strings in the DEX |
| `string_data` | MUTF-8 payloads |
| Type/proto/method ids | Reference strings for names |
| Multi-dex | `classes2.dex` … each has its own pool |
| Obfuscation | Encrypted strings decrypted at runtime |

## Workflow

### 1. Confirm sample and success criteria

1. Record APK hash, package name, authorization.
2. Success: prioritized string list with categories; xrefs to code for top items; follow-ups for encrypted strings.
3. Immutable original APK stored.

### 2. Extract DEX

```bash
sha256sum app.apk
unzip -l app.apk | rg 'classes.*\.dex'
mkdir -p apk_out && unzip -o app.apk 'classes*.dex' -d apk_out
```

### 3. Dump string pools

```bash
# dexdump (build-tools)
dexdump -f apk_out/classes.dex | head
# strings-like extraction
strings -n 6 apk_out/classes.dex | sort -u > strings_raw.txt
# baksmali / jadx for structured view
jadx -d jadx_out app.apk
rg -n "https?://|api[_-]?key|secret|password|Bearer|-----BEGIN" jadx_out/ | head
```

**Python sketch to parse string_ids (lab):** use `androguard` or `dexlib` if available; otherwise jadx is enough for triage.

### 4. Categorize hits

| Category | Examples | Next step |
| --- | --- | --- |
| Endpoints | `https://api.`, paths | Map to network client code |
| Secrets | keys, tokens | Verify if live; rotate if owned app leak |
| Crypto | `AES`, IVs, salts | Find algorithms |
| IPC | action strings, authorities | Exported component review |
| Debug | `TODO`, staging hosts | Environment confusion |
| Flags/CTF | `flag{`, base64 blobs | Decode |

```bash
rg -n "https?://" strings_raw.txt
rg -n "AKIA|AIza|ghp_|xox[baprs]-" strings_raw.txt || true
```

### 5. Map strings to code

1. In jadx: right-click string → Find usage.
2. In smali: search const-string.
3. Note if string is only in resources (`resources.arsc`) vs DEX.

```bash
apktool d app.apk -o apktool_out
rg -n "const-string" apktool_out/smali* | head
```

### 6. Handle missing/encrypted strings

| Observation | Approach |
| --- | --- |
| Few readable strings | Heavy obfuscation / packing |
| Base64 blobs assigned to fields | Decode; if fail, runtime decrypt |
| Strings built by concatenation | Grep pieces; dynamic hooks |
| Loaded from native | Open `.so` in Ghidra |

Authorized dynamic: Frida hook `String.<init>` or decrypt methods (owned apps only).

### 7. Hand off

1. Deliver table: string, category, file/method xref, risk.
2. For owned apps: file secrets for rotation; move secrets off client.
3. Continue with component/network testing skills.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Coverage | All classes*.dex + resources | Only `classes.dex` |
| Secrets | Redact in reports; rotate | Paste live keys publicly |
| RE | Xrefs to prove use | “String exists so vuln” |
| Dynamic | Authorized lab hooks | Hooking random Play apps |

## Output Checklist

- [ ] APK hash and auth recorded
- [ ] All DEX files extracted
- [ ] String dump + categorized hits
- [ ] Xrefs for high-value strings
- [ ] Encrypted/obfuscated strings noted with plan
- [ ] Secrets handling/rotation if owned
- [ ] Handoff to pentest/RE next steps

## Rules

- Authorized samples only.
- Strings are leads, not proof of vulnerability alone.
- Redact credentials found during triage.
- Prefer jadx xrefs over raw `strings` for conclusions.
- Do not use findings to pirate software.
