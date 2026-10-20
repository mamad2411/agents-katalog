---
name: deserialization-gadget-awareness
description: >
  AppSec awareness of deserialization gadget chains: how POP/gadget classes turn untrusted
  native deserialize into RCE or file/JNDI effects in Java, .NET, PHP, Python pickle, and
  Ruby; inventory dependencies for known gadget libraries; prioritize allowlists and safe
  formats. Use when ysoserial-class thinking, ObjectInputStream gadgets, BinaryFormatter
  chains, pickle __reduce__, PHP phar/meta gadgets, or reviewing classpath for gadget risk
  during authorized assessments — not for building weaponized multi-stage exploits for
  unauthorized targets (use deserialization-insecure for finding sinks; safe-formats for remediations).
---

# Deserialization Gadget Awareness

## Scope And Authorization

- **In scope:** Owned applications, labs, CTFs, and written-authorization AppSec reviews.
- **Out of scope:** Developing or deploying gadget exploits against systems without authorization; sharing weaponized payloads as the primary deliverable when a non-weaponized proof suffices.
- Prefer static inventory and design review; dynamic proof only with RoE and non-destructive oracles when possible.
- Redact internal hostnames, secrets in serialized blobs, and full exploit chains from public tickets.
- Pair with `deserialization-insecure` (find/test sinks) and `deserialization-safe-formats` (remediate).

## When To Use

- Explaining *why* `ObjectInputStream.readObject`, `BinaryFormatter`, `pickle.loads`, or `yaml.load` is dangerous even with “trusted types” myths.
- Auditing classpaths/dependencies for libraries commonly used in gadget chains.
- Prioritizing patching/removal of gadget-enabling components after a sink is found.
- Training developers on POP gadgets without turning the session into an exploit workshop for unauthorized use.
- Threat modeling caches, session stores, message queues, and RMI/IIOP that carry serialized objects.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| End-to-end find + safely test sinks | `deserialization-insecure` |
| Migrate to JSON/Protobuf/safe loaders | `deserialization-safe-formats` |
| Java/.NET heap or ROP after RCE | binary exploitation skills (authorized only) |
| Generic injection when class unknown | `injection-checking` |
| Code quality baseline | `code-quality-standards` |

## What is a gadget?

A **gadget** is existing application or library code that performs dangerous operations (reflection, class loading, command exec, JNDI lookup, file write) when its deserialization callbacks or property setters run. A **gadget chain** links multiple classes so that deserializing one attacker-controlled graph reaches a dangerous sink—without the attacker uploading new classes if they are already on the classpath.

| Stack | Common themes |
| --- | --- |
| Java | `readObject` / `readResolve`; InvokerTransformer-style chains; JNDI; Commons-Collections historical chains; classpath-dependent |
| .NET | `BinaryFormatter` / legacy LOB serializers; type binders; gadget types in gadgets dumps |
| PHP | `unserialize` magic methods (`__wakeup`, `__destruct`); Phar metadata deserialization |
| Python | `pickle` opcodes calling `__reduce__` / reducible callables |
| Ruby | `Marshal.load` object hooks |
| YAML | Runtime class instantiation tags (`!!python/object`, Java beans) |

## Workflow

### 1. Confirm scope and success criteria

1. Authorization and whether dynamic chain verification is allowed vs inventory-only.
2. Success: gadget risk rating per sink; dependency hit list; remediation path to allowlist/safe format.
3. Agree non-weaponized impact proofs (e.g. controlled DNS/sleep/file in lab) when needed.

### 2. Map deserialize entry points (context)

1. From `deserialization-insecure` or code review: list sinks and whether input is attacker-controlled (HTTP cookie, queue, cache, SSO token, admin import).
2. Note trust boundaries: “internal Kafka” is still untrusted if any producer can be compromised.

### 3. Inventory gadget-enabling dependencies

```bash
# Owned repo / built artifact examples
# Java
rg -n "ObjectInputStream|readObject|Serializable" --type java | head
# list deps
mvn -q dependency:tree -Dverbose=false 2>/dev/null | head -n 80
gradle dependencies 2>/dev/null | head -n 80
# .NET
rg -n "BinaryFormatter|NetDataContractSerializer|LosFormatter|SoapFormatter" -g '*.cs'
# Python
rg -n "pickle\\.loads|yaml\\.load\\(|marshal\\.loads" -g '*.py'
# PHP
rg -n "unserialize\\(|Phar::" -g '*.php'
```

1. Compare libraries to known public research *for awareness and patching*—do not treat public exploit kits as something to run on production.
2. Heavy reflection, expression languages, and template libraries near deserialize paths raise priority.

### 4. Assess chain feasibility (AppSec judgment)

| Factor | Higher risk |
| --- | --- |
| Attacker controls full blob | HTTP parameter, cookie, job payload |
| No type allowlist / filter | Default Java serialization, unrestricted binder |
| Rich classpath | Many commons/*, Spring, invokers |
| Dangerous callbacks | Custom `readObject`, finalizers, proxies |
| Outbound network allowed | JNDI/LDAP/HTTP exfil or second stage |

1. **No gadgets found ≠ safe** if sink still accepts attacker types—future deps can introduce gadgets.
2. **Gadgets present ≠ auto-RCE** without a reachable sink and suitable chain; still prioritize removal of sink.

### 5. Awareness controls (before full migration)

1. Prefer eliminating native deserialize for untrusted data (`deserialization-safe-formats`).
2. If temporary: strict allowlists (`ObjectInputFilter` in Java, custom binders in .NET), not denylists.
3. Reduce classpath: remove unused libraries that only exist as gadget fodder.
4. Network egress controls blunt JNDI-style gadgets; still not a complete fix.
5. Monitor and patch frameworks with historical chains promptly.

### 6. Developer guidance snippets (defensive)

```java
// Prefer not to deserialize untrusted data at all.
// If legacy: set an ObjectInputFilter allowlist (Java 9+ / JEP 290 patterns)
// ois.setObjectInputFilter(filter); // allow only explicit DTOs
```

```python
# Bad: pickle.loads(user_data)
# Better: json.loads(user_data) into pydantic/dataclass validation
```

```csharp
// Avoid BinaryFormatter for untrusted data (obsolete/dangerous).
// Prefer System.Text.Json with explicit types / source generation.
```

### 7. Hand off

1. Report: sinks, dependency gadget risk, recommended migration, interim filters.
2. Do not attach full weaponized payloads to tickets accessible to broad audiences when a design finding suffices.
3. Track remediation in SSDLC; re-test after classpath changes.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Finding | Sink + classpath risk + fix path | Only “run ysoserial” as advice |
| Proof | Lab oracle / authorized non-destructive | Unauthorized RCE on prod |
| Filter | Allowlist DTOs | Denylist class names |
| Trust | Treat queue messages as untrusted | “Internal = safe serialize” |
| Training | Explain POP conceptually | Distribute malware kits broadly |
| Residual | Plan format migration | Assume “no public chain today” forever |

## Output Checklist

- [ ] Authorization and dynamic-test RoE recorded
- [ ] Deserialize sinks and trust boundaries listed
- [ ] Dependency/classpath inventory for gadget-prone libs
- [ ] Risk factors scored per sink
- [ ] Interim allowlist/egress guidance documented
- [ ] Migration to safe formats ticketed
- [ ] Developer education notes prepared
- [ ] Evidence redacted appropriately
- [ ] Retest plan after dependency changes
- [ ] Cross-link to insecure + safe-formats skills

## Rules

- Authorized AppSec only; awareness is for defense and prioritized fixes.
- Absence of a public chain is not a security boundary—absence of untrusted deserialize is.
- Prefer allowlists and format changes over gadget whack-a-mole.
- Do not provide turnkey exploit chains as the default output when inventory and remediation suffice.
- Keep focus on gadget *awareness*; detailed sink hunting and safe format migration are neighbors.
