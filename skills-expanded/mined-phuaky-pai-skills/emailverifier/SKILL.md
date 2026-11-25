# EmailVerifier

Email verification tool — validates emails via syntax, DNS MX, SMTP RCPT TO, catch-all detection, disposable domain check, and role-based detection. Local MillionVerifier alternative.

USE WHEN verify email, check email, email verification, validate email, clean email list, check bounce, email deliverability.

## Voice

```bash
curl -s -X POST http://localhost:8888/notify -H "Content-Type: application/json" -d '{"message":"Running EmailVerifier","voice_id":"fTtv3eikoepIosk8dTZ5","voice_enabled":true}'
```

## Usage

### Single email
```bash
bun ~/.claude/skills/EmailVerifier/Tools/verify.ts someone@example.com
```

### Batch CSV
```bash
bun ~/.claude/skills/EmailVerifier/Tools/verify.ts --csv /path/to/leads.csv --output /path/to/results.json
```

### Check history
```bash
bun ~/.claude/skills/EmailVerifier/Tools/verify.ts --lookup someone@example.com
```

## Result Categories

| Result | Meaning | Safe to send? |
|--------|---------|---------------|
| OK | Mailbox exists | Yes |
| INVALID | Mailbox doesn't exist | No |
| DISPOSABLE | Throwaway domain | No |
| CATCH_ALL | Domain accepts all (can't verify) | Risky |
| UNKNOWN | Couldn't determine (timeout, greylisting) | Risky |
| ROLE_BASED | info@, admin@, etc. (flagged, not rejected) | Caution |

## Key Paths

| Resource | Path |
|----------|------|
| Main CLI | `Tools/verify.ts` |
| SMTP probe | `Tools/smtp-probe.ts` |
| Data store | `Tools/data-store.ts` |
| Disposable domains | `Data/disposable-domains.txt` |
| Role prefixes | `Data/role-prefixes.json` |
| SQLite DB | `Data/verifier.db` |
