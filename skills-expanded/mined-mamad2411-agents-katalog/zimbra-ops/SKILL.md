---
name: zimbra-ops
description: Lit, drafte, envoie et marque des emails sur la boîte OVH Zimbra contact@omnividens.fr (IMAP/SMTP D-018). Utilise ce skill quand le user demande de répondre à un email, drafter un mail outbound, classer un email lu, ou débugger l'EmailBot inbound.
---

# zimbra-ops

Skill technique pour toute opération email côté Argos Ops. Réutilisable
par EmailBot inbound (P5), OutboundBot cold email (P13), FinanceBot
relances (P7) et `/check-emails` slash command (humain-in-the-loop).

> Stack figée par **D-018** : OVH Zimbra IMAP/SMTP (pas Gmail Workspace,
> pas self-host). Boîte canonique `contact@omnividens.fr`. Hôte
> `ssl0.ovh.net`, ports `993` (IMAP SSL) / `465` (SMTP SSL).

## Inputs (variables d'environnement)

| Variable | Source | Requise ? |
|---|---|---|
| `EMAIL_USER` | `.env.local` | Oui (login Zimbra, ex `contact@omnividens.fr`) |
| `EMAIL_PASSWORD` | `.env.local` | Oui (mot de passe Zimbra, **pas** celui du compte OVH) |
| `EMAIL_IMAP_HOST` | `.env.local` ou défaut `ssl0.ovh.net` | Non |
| `EMAIL_IMAP_PORT` | défaut `993` | Non |
| `EMAIL_SMTP_HOST` | défaut `ssl0.ovh.net` | Non |
| `EMAIL_SMTP_PORT` | défaut `465` | Non |
| `EMAIL_REPLY_NAME` | défaut `Argos par Omnividens` | Non |

## API du wrapper `argos_ops.integrations.zimbra`

```python
from argos_ops.integrations.zimbra import (
    fetch_unread, mark_seen, send_email, is_noreply, extract_domain,
    EmailMessage,
)

# 1) Pull non lus (n'altère pas le flag \Seen)
messages: list[EmailMessage] = await fetch_unread(
    host=..., port=..., user=..., password=SecretStr(...), limit=50,
)

# 2) Marquer un UID comme lu (à appeler après ingestion réussie)
await mark_seen(host=..., port=..., user=..., password=..., uid="42")

# 3) Envoyer un email (texte ou multipart text+html)
await send_email(
    host=..., port=..., user=..., password=...,
    from_name="Argos par Omnividens",
    to="prospect@example.com",
    subject="Re: question pricing",
    body_text="Bonjour ...",
    body_html=None,                    # optionnel
    in_reply_to="<msg-id>",            # threading
    references=["<msg-id-thread>"],    # threading
)
```

## Drafter une réponse (humain-in-the-loop)

Pattern recommandé pour `/check-emails` :

1. Lis les `interactions` non répondues (`channel='email'`, `direction='in'`,
   pas d'`out` postérieur du même thread)
2. Pour chaque email :
   - Invoque le skill `email-classifier` → tag
   - (P6+) Invoque `kb-rag` pour récupérer contexte produit
   - Drafte la réponse en respectant `tone_of_voice.md`
3. Soumets la draft à l'opérateur (humain valide ou rejette)
4. Sur validation : appelle `send_email(...)` avec `in_reply_to` du message
   d'origine, et logge une `interaction(direction='out', judge_verdict='human_validated')`

## Garde-fous

- **Filtrer noreply** : utiliser `is_noreply(from_email)` avant tout envoi
  (la liste de patterns inclut `noreply@`, `mailer-daemon@`, `bounces@`...)
- **Threading propre** : toujours passer `in_reply_to` + `references` quand
  c'est une réponse, pour ne pas casser les fils côté client mail
- **Limite warm-up** : pas active en P5 (envoi humain-validé). À ré-activer
  en P14 (agent-juge) : 50 envois auto / jour pendant 1 mois

## Tests

Cf. `tests/test_zimbra.py` :

- `test_is_noreply_*` — détection des expéditeurs auto
- `test_extract_domain_*` — extraction du domaine d'une adresse

Cf. `tests/test_email_bot.py` :

- `test_email_bot_skips_noreply` — un email noreply ne crée pas d'interaction
- `test_email_bot_persists_email` — crée company + lead + interaction
- `test_email_bot_imap_failure_returns_failed` — IMAP fetch qui crash → status=failed
- `test_build_inbox_embed_*` — formatage Discord embed

## Setup cron — Windows Task Scheduler

EmailBot tourne sur l'ordi du fondateur (D-017). Cadence : `*/15 * * * *`
en heures ouvrées. Pour réduire le bruit la nuit, on peut passer à
`*/15 8-22 * * *` (toutes les 15 min entre 8 h et 22 h Paris).

### Création de la tâche (PowerShell, scriptable)

```powershell
$action = New-ScheduledTaskAction -Execute "claude" `
  -Argument '--print "/run-email-bot"' `
  -WorkingDirectory "C:\Users\pauzzle\Desktop\argos-ops"
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).Date.AddHours(8) `
  -RepetitionInterval (New-TimeSpan -Minutes 15) `
  -RepetitionDuration (New-TimeSpan -Hours 14)
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable `
  -DontStopIfGoingOnBatteries -AllowStartIfOnBatteries `
  -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName "argos-ops-email-bot" `
  -Action $action -Trigger $trigger -Settings $settings `
  -Description "EmailBot inbound — toutes les 15 min, 8h-22h Paris (D-017/D-018)"
```

### Test immédiat (sans attendre le cron)

```powershell
Start-ScheduledTask -TaskName "argos-ops-email-bot"
```

ou en CLI direct :

```bash
uv run python scripts/run_email_bot.py
```

## Métriques de succès

- **Latence** : < 10 s pour une boîte avec ≤ 5 emails non lus (IMAP TCP +
  TLS handshake dominant)
- **Taux de succès** : > 95 % (échec dominant attendu = creds expirés
  côté OVH)
- **Coût Claude Code** : 0 token (le script ne fait pas d'appel LLM —
  D-017). Le coût Claude Code arrive avec `/check-emails` quand l'opérateur
  drafte les réponses

## Limites connues

- **Pas de IMAP IDLE** : on poll toutes les 15 min, pas de push temps réel.
  Suffisant pour P5. À reconsidérer si le SLA passe sous 5 min
- **Pas de pièces jointes** : le body est du texte brut (HTML fallback). Les
  attachements ne sont pas parsés. À ajouter quand un cas concret se présente
- **Pas de gestion multi-boîtes** : une seule boîte (`contact@omnividens.fr`).
  Suffisant tant qu'on n'a pas de `support@` séparé
