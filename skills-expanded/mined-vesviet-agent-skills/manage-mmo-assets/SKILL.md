---
name: manage-mmo-assets
description: Manage and share MMO assets (Business Managers, Via, Pixels/Datasets, Anti-Detect profiles) using Role-Based Access Control (RBAC), RFC 6238 2FA/TOTP programmatic generation, Vault secret storage, and VCC isolation with BIN diversity. Use when onboarding new ad accounts, sharing BMs with team members, auditing asset health, or recovering from a cascading ban incident.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
version: "1.0.0"
---

# Manage MMO Assets

Use this skill to securely acquire, organize, and share marketing assets using RBAC-based access control, programmatic 2FA/TOTP handling, secrets vault isolation, and virtual card (VCC) compartmentalization to eliminate cascading ban blast radiuses.

## Legal & Compliance Notice

Ad platforms (Meta, Google, TikTok) prohibit circumventing their account, ownership, or verification policies — sharing Business Managers/Vias to route around identity or ownership checks, or maintaining "clean backup" assets specifically to survive a ban that would otherwise apply, can violate platform ToS regardless of the isolation hygiene used. This skill documents access-control and compartmentalization mechanics only. It does not authorize policy circumvention; any step that exists specifically to defeat a platform's account-integrity or ownership verification system falls under `REVIEW-SYSTEM LOCK` in the `mmo-engineer` role and requires explicit written user authorization plus Security Engineer review before implementation.

## When to Use

- onboarding new ad accounts, Vias, or Business Managers (BMs) into isolated operational silos
- automating 2FA/TOTP login verification codes using programmatic RFC 6238 generation from secrets vaults
- allocating virtual commercial cards (VCCs) with distinct BINs across ad accounts to prevent billing bans
- migrating plain text credentials and session cookies into HashiCorp Vault or AWS Secrets Manager
- auditing asset health, ASN boundaries, and VCC usage to prevent cascading ban ("chét chùm") incidents

## Example (TOTP Programmatic Handling & VCC BIN Diversity)

```python
# Programmatic RFC 6238 2FA/TOTP token generation via Vault
import os, pyotp, hvac

vault = hvac.Client(url="https://vault.internal:8200", token=os.environ["VAULT_TOKEN"])
secret = vault.secrets.kv.v2.read_secret_version(path="mmo/silos/silo-a/account-01")
totp_seed = secret["data"]["data"]["totp_seed"]

# Generate 6-digit TOTP token with 30s window
totp = pyotp.TOTP(totp_seed, interval=30, digits=6)
verification_token = totp.now()

# Virtual card (VCC) allocation with BIN diversity
def allocate_silo_vcc(silo_id: str, provider: str) -> dict:
    card = issuing_client.cards.create(
        cardholder=silo_id,
        currency="USD",
        type="virtual",
        spending_controls={"spending_limits": [{"amount": 50000, "interval": "daily"}]},
        metadata={"silo": silo_id, "issuer": provider}
    )
    return {"card_id": card.id, "last4": card.last4, "bin": card.bin}
```

```yaml
# Silo compartmentalization map with VCC BIN diversity and Vault integration
silos:
  - id: silo-alpha
    asn: AS15169 # Distinct ISP / ASN peer
    vcc:
      provider: "Stripe-Issuing"
      bin: "424242"
      daily_velocity_limit: 500.00
      currency: "USD"
    assets: [bm-101, via-22, adacct-7]
    vault_path: "secret/data/mmo/silos/silo-alpha"
  - id: silo-beta
    asn: AS7018 # Distinct mobile / ASN peer
    vcc:
      provider: "Airwallex"
      bin: "532959" # Diverse BIN to prevent billing graph links
      daily_velocity_limit: 500.00
      currency: "USD"
    assets: [bm-102, via-23, adacct-8]
    vault_path: "secret/data/mmo/silos/silo-beta"
```

## Core Rules

- **ISOLATION-LOCK**: Never share the same residential proxy IP, ASN, or virtual payment card across unrelated ad accounts or profile silos.
- **ASSET-LOCK**: Do not connect clean backup assets (Vias/BMs/Pixels) to currently restricted or flagged assets until the restriction is fully resolved.
- **RFC6238-TOTP-AUTOMATION**: Store TOTP base32 secret seeds strictly in encrypted vaults; generate dynamic 6-digit verification codes programmatically (`pyotp`/`otplib`) during automation login flows with ±1 time-step drift tolerance. Store emergency one-time recovery codes in KMS-sealed secrets.
- **VAULT-SECRETS-HYGIENE**: All platform credentials, cookies, proxy tokens, and 2FA seeds MUST be stored in HashiCorp Vault or AWS Secrets Manager with KMS envelope encryption. Enforce strict RBAC least privilege — zero plaintext credentials in source code, configuration files, or logs.
- **VCC-BIN-DIVERSITY**: Enforce 1:1 binding between Virtual Commercial Card (VCC) and Ad Account. Allocate VCCs across diverse Bank Identification Numbers (BINs) and multiple issuers (Stripe Issuing, Airwallex, Privacy, Mercury) to prevent payment-network-wide account freezes. Enforce strict spend velocity caps per card.
- **PAYMENT-QUARANTINE**: If a billing hold or payment failure occurs on any account, immediately isolate and quarantine the associated VCC. Never reassign a flagged card to another ad account.
- **ASN-SILO-ISOLATION**: Each operational silo MUST use proxy pools from distinct ASNs. Platform fraud engines correlate accounts sharing identical ASN pools; distinct ASNs minimize cascading ban blast radius.
- **EXPONENTIAL-BACKOFF-RATE-LIMIT**: Platform API requests MUST implement adaptive rate limiting with Poisson-distributed intervals and automatic backoff on HTTP 429, 503, or platform checkpoint responses.
- **BAN-BLAST-RADIUS-AUDIT**: Following any restriction, audit the entire entity graph (shared BMs, pixels, domains, admin profiles, and VCCs) before reactivating assets in the affected silo.

## Suggested Process

1. **Vault Secret Ingestion**: Ingest account credentials, session cookies, RFC 6238 TOTP seeds, and backup recovery codes into HashiCorp Vault or AWS Secrets Manager under silo-partitioned paths.
2. **VCC Allocation with BIN Diversity**: Provision dedicated virtual cards per ad account from diverse issuing providers (Stripe, Airwallex, Privacy). Set daily velocity limits and link card billing addresses to the ad account country.
3. **Programmatic 2FA Integration**: Integrate `pyotp`/`otplib` into login automation workflows to resolve 2FA challenges on-the-fly without manual intervention.
4. **RBAC & Silo Isolation Mapping**: Organize profiles, BMs, and proxies into independent silos with zero overlap in ASNs, payment cards, or admin identities.
5. **Blast-Radius Audit & Recovery**: Run automated graph audits periodically to detect unintentional cross-silo linkage. Immediately quarantine flagged assets and their bound payment cards upon platform restrictions.

## Checklist

- [ ] All account credentials, cookies, and 2FA seeds secured in Vault/Secrets Manager.
- [ ] Programmatic RFC 6238 TOTP token generation tested with 30s window drift tolerance.
- [ ] Emergency account recovery codes stored in separate encrypted vault paths.
- [ ] Virtual cards (VCCs) allocated 1:1 to ad accounts with diverse BINs and distinct issuers.
- [ ] Daily spend velocity caps enforced on all active VCCs.
- [ ] Silos operate on distinct ASNs with zero IP or subnet overlap.
- [ ] No raw passwords, cookies, or card numbers stored in plaintext or repository files.
- [ ] Payment quarantine protocol triggers automatically on billing disputes or card declines.
- [ ] Graph audit confirms zero admin, pixel, domain, or payment overlap between clean and active silos.
- [ ] Adaptive Poisson-distributed rate limiting active for platform API calls.

## Output Contracts

When the asset inventory or silo configuration is updated for operational handoff, emit:

- **`contracts/schemas/deployment-plan.json`** capturing silo topologies, asset IDs, Vault paths, VCC metadata (masked BINs, limits), rotation cadence, and rollback procedures.
- Markdown summary of silo asset inventories, ASN allocations, and compliance boundaries.

Skip emission for local asset lookups that do not cross role boundaries.

## Failure Modes

- **Cascading billing ban ("chết chùm payment")**: Reusing a payment card across multiple ad accounts causes platform fraud systems to terminate all accounts linked to the card. Mitigation: enforce strict 1:1 VCC allocation and diverse BIN sourcing.
- **TOTP clock drift de-synchronization**: Server clock drift causes generated 6-digit tokens to fail authentication. Mitigation: sync server NTP clocks and allow ±1 step window validation.
- **Credential exposure in logs**: Printing secret responses or OTP codes in CI/CD or automation logs. Mitigation: mask all sensitive token outputs and enforce secret filtering.
- **Silo leakage via shared admin**: Adding the same admin personal profile across two silos bridges the isolation boundary. Mitigation: enforce strict RBAC and check admin overlap in automated graph audits.
- **VCC billing limit decline**: An ad account exhausts card spend limit unexpectedly, causing billing failure and account suspension. Mitigation: monitor account spend velocity against card limits and trigger pre-emptive threshold alerts.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: Platform credentials, TOTP seeds, and card details must be fetched at runtime with scoped least-privilege RBAC; never commit credentials into version control.
- **ASI04 Supply Chain**: Cryptographic TOTP libraries (`pyotp`, `otplib`) and vault clients must be pinned to verified package digests; avoid unverified third-party authenticator SDKs.
- **ASI05 RCE Guard**: Never construct Vault CLI commands, secret queries, or card provisioning payloads from unsanitized external web parameters.
- **ASI07 Inter-Agent Communication**: Silo asset topology and masked VCC configurations must be emitted via `contracts/schemas/deployment-plan.json` for validation by deployment workers.
- **ASI09 Human-Agent Trust Exploitation**: Surface account restriction histories and payment dispute rates transparently; do not guarantee immunity from platform reviews.

## Related Skills

- **deploy-mmo-infrastructure**: Provision isolated Anti-Detect Browser profiles and proxy networks bound to these asset silos.
- **setup-tracking-system**: Configure tracking assets (Pixels/Datasets) referenced in the catalog.
- Companion reference: `references/mmo-asset-rbac-and-vault-isolation.md`
- Companion example: `examples/mmo-asset-vault-manager.py`
