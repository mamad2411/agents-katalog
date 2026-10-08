# Skill: redteam-attack
# Trigger: exploit, PoC, attack, penetration test, break in, bypass, payload, red team
# Scope: offensive minions (recon, exploit, red coordinator)
# ROE: cybersec-minion-contract.md — own code / authorized sandbox ONLY. STOP after proof.

## GOLDEN RULE
Prove impact, then STOP. No real-world targets. No exfiltration. No persistence.
Every PoC is minimal and reversible. If proof needs out-of-scope action -> BLOCK.

## METHOD (per finding)
1. RECOGNIZE: match code to a catalog pattern (detection signal).
2. HYPOTHESIZE: what breaks, where, expected impact, proof criterion.
3. EXPLOIT (lab): smallest payload that proves it; capture one reproducible step.
4. RECORD: breached=true/false, evidence, kill chain.
5. HANDOFF: to blue. Tear down lab state.

## WORKED EXAMPLES (recognize -> lab exploit)
- SQLi (CWE-89): `' OR '1'='1' -- ` against dev DB -> auth bypass; UNION SELECT -> schema.
- Stored XSS (CWE-79): persist `<img src=x onerror=...>` in a comment on the lab instance.
- Weak JWT (CWE-347): forge `alg:none` token, `role:admin` -> privilege escalation.
- SSRF (CWE-918): point url param at lab metadata endpoint -> internal data.
- IDOR (CWE-862): auth as A, request B's id -> A gets B's data.
- Deserialization (CWE-502): gadget payload to sandbox service -> controlled exec, then STOP.
- TOCTOU (CWE-367): N concurrent redeems on lab wallet -> double-spend.
- Secrets (CWE-798): `git log -p | grep -Ei 'secret|api[_-]?key|token'`.

Full catalog: `packages/cybersec/src/patterns.ts`, `docs/cybersec/ATTACK-DEFENSE-PLAYBOOK.md`.

## OUTPUT
```
FINDING id=<pattern> severity=<...> breached=<bool>
EVIDENCE: <reproducible step>
KILL_CHAIN: recon -> entry -> impact
```
