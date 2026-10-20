---
name: burp-extension-dev-basics
description: >
  Develop Burp Suite extensions for authorized testing: Montoya API / legacy API basics,
  UI tabs, HTTP listeners, scanners, persistence, packaging, and safe handling of traffic.
  Use when writing Burp extensions, Montoya extension, custom scan checks, or automating
  Burp for owned labs — not for weaponizing against out-of-scope targets.
---

# Burp Extension Dev Basics

## Scope And Authorization

- **In scope:** Extensions used on targets you own or are authorized to test; lab traffic.
- **Out of scope:** Using custom extensions to attack third parties without authorization; shipping malware as extensions.
- Extensions see **full traffic including tokens** — protect project files and logs.
- Redact secrets in shared extension code samples.
- Pair testing methodology with web skills and `bug-bounty-methodology` / RoE docs.

## When To Use

- Automating repetitive Burp tasks (header inject, custom match/replace logic beyond built-ins).
- Custom passive/active scan checks for your org’s frameworks.
- Integrating Burp with internal issue trackers (carefully).
- Learning Montoya API for Java/Kotlin or Jython legacy paths.
- Packaging an extension for a private team store.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General web vuln testing | specific vuln skills / methodology |
| Browser extension security | `browser-extension-security` |
| ZAP add-ons | ZAP-specific skills if present |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Piece | Role |
| --- | --- |
| Montoya API | Current extension API (Burp 2023.12+ era) |
| Extender (legacy) | Older `IBurpExtender` interfaces still seen |
| HttpHandler / listeners | Observe/modify requests/responses |
| ScannerCheck | Passive/active custom findings |
| Persistence | Extension data store / project file |
| UI | Suites tabs, context menus |

## Workflow

### 1. Confirm scope and success criteria

1. Burp edition (Community/Pro), Java version, private vs shared extension.
2. Success: extension loads without error; performs intended transform/check only on in-scope hosts; no secret leakage in UI defaults.
3. Define host allowlist behavior for any active modification.

### 2. Scaffold project

```bash
# Example Gradle Java project (structure varies)
mkdir -p burp-ext/src/main/java/com/example/ext
# Build jar with Montoya API dependency per PortSwigger docs for your Burp version
./gradlew jar
```

**Montoya entry sketch:**

```java
import burp.api.montoya.BurpExtension;
import burp.api.montoya.MontoyaApi;

public class Extension implements BurpExtension {
  @Override
  public void initialize(MontoyaApi api) {
    api.extension().setName("Owned Lab Helper");
    api.logging().logToOutput("Loaded Owned Lab Helper");
    // register handlers...
  }
}
```

1. Pin API dependency version compatible with team Burp versions.
2. Prefer Java/Kotlin for Montoya; treat Jython as legacy.

### 3. Register handlers safely

**HTTP handler considerations:**

1. Scope: check `httpRequest.httpService().host()` against allowlist.
2. Do not infinite-loop on your own modified requests.
3. Performance: avoid heavy work on every history item in passive path without filtering.
4. Active checks: throttle; respect target health; no destructive payloads by default.

```java
// Pseudocode passive check
api.scanner().registerScanCheck(new ScanCheck() {
  // produce AuditIssue only with evidence, confidence, remediation
});
```

### 4. UI and configuration

1. Store config (allowlist, feature flags) via extension preferences API — not hardcoded secrets.
2. Context menu actions for “send to custom analyzer” on selected requests.
3. Clear logging levels; never log full `Authorization` headers by default.

### 5. Package and load

```text
Burp → Extensions → Add → Java → select jar
Check Output/Errors tabs
```

1. Document required Burp version.
2. Sign or checksum jars for internal distribution.
3. Avoid shading conflicting JSON libraries carelessly (classpath issues).

### 6. Test in lab

1. Proxy a known lab app; verify modifications only when host matches.
2. Unit-test pure parsing logic outside Burp where possible.
3. Negative: out-of-scope host unchanged.
4. Memory: long history + extension should not OOM (profile if needed).

### 7. Hand off

1. README: build, load, config, threat notes (traffic sensitivity).
2. Changelog for extension versions.
3. Apply `code-quality-standards`; dependency scan the jar build.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Scope | Host allowlist for active mods | Global replace on all sites |
| Secrets | Redacted logs | Dump cookies to Output always |
| Findings | Clear evidence + remediation | Spam low-value issues |
| API | Montoya maintained | Ancient undocumented forks only |
| Distribution | Versioned jar + checksum | Random Drive jar “final2” |
| Performance | Filter by tool/path | Heavy ML on every response |

## Output Checklist

- [ ] Burp edition/API version documented
- [ ] Project builds reproducible jar
- [ ] Handlers respect scope allowlists
- [ ] No default secret logging
- [ ] Lab verification allow + deny hosts
- [ ] Install docs for team
- [ ] Version/changelog maintained
- [ ] Dependencies reviewed
- [ ] `code-quality-standards` applied

## Rules

- Extensions inherit your testing authorization — do not widen scope silently.
- Protect project files containing production traffic.
- Prefer passive analysis; active checks require explicit enablement.
- Do not package offensive tooling aimed at unauthorized use.
- Deep vuln methodology lives in other skills; this is extension engineering.
