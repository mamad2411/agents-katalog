---
name: stripe-ops
description: Lit les abonnements et factures Stripe, calcule MRR/ARR, détecte les impayés J+3/J+7/J+15 et envoie des relances par email via Zimbra. Utilise ce skill quand le user demande de lancer la sync finance, drafter une relance manuelle, ou débugger un MRR incorrect.
---

# stripe-ops

Skill technique pour P7 FinanceBot. Encapsule la lecture des abonnements
+ factures Stripe et le pilotage du dunning automatique. Réutilisé par
le digest matinal (`/morning-digest` consomme le MRR via `output_summary`)
et par toute commande devant interroger Stripe en lecture.

> **Compte Stripe** : partagé avec SecHunter (cf. P0 décision). Mode
> test recommandé en dev (`sk_test_...`), prod uniquement quand le
> backfill MRR est validé.

## Inputs (variables d'environnement)

| Variable | Source | Requise ? |
|---|---|---|
| `STRIPE_SECRET_KEY` | `.env.local` | Oui (sinon l'agent renvoie status=failed) |
| `STRIPE_WEBHOOK_SECRET` | `.env.local` | Optionnel (P7 polling, pas webhook) |
| `EMAIL_USER` / `EMAIL_PASSWORD` | `.env.local` | Oui (pour envoyer les relances) |
| `DISCORD_WEBHOOK_ALERTS` | `.env.local` | Optionnel (alerte MRR -5%) |

## API Python

```python
from argos_ops.integrations.stripe_client import (
    fetch_active_subscriptions,
    fetch_open_invoices,
    compute_mrr_eur,
    compute_arr_eur,
    classify_dunning_level,
)

subs = await fetch_active_subscriptions(api_key)         # toutes statuts
invoices = await fetch_open_invoices(api_key)            # status='open' uniquement

mrr = compute_mrr_eur(subs)                              # somme active+trialing
arr = compute_arr_eur(mrr)                               # mrr * 12

for invoice in invoices:
    level = classify_dunning_level(invoice)              # 'J+3' | 'J+7' | 'J+15' | 'none'
    if level != "none":
        # cf. argos_ops.agents.finance_bot pour le pipeline complet
        ...
```

## Pipeline FinanceBot (cron `0 6 * * *`)

```
1. Pull subs Stripe (toutes statuts)
   ↓
2. Upsert companies (stripe_customer_id, subscription_status, mrr_eur)
   match par stripe_customer_id → domaine email → création
   ↓
3. Calcul MRR (sum active+trialing) + ARR + delta vs MRR il y a 7 jours
   ↓
4. Pull invoices status='open'
   ↓
5. Pour chaque invoice :
   - classify_dunning_level (J+3 / J+7 / J+15 / none)
   - skip si relance déjà envoyée à ce niveau
     (interactions.judge_verdict='dunning_X' AND subject LIKE %invoice_id%)
   - Sinon : render_dunning_email(level, invoice) → send_email via zimbra-ops
   - Log interaction(direction='out', agent_name='FinanceBot',
     judge_verdict='dunning_X')
   ↓
6. Notif Discord embed (canal alerts, fallback ops_logs)
   couleur RED si MRR baisse > 5 %, YELLOW si dunning > 0, sinon GREEN
   ↓
7. Logger agent_runs.output_summary :
   "mrr=X arr=Y mrr_delta=+Z% active_subs=N/M open_inv=K
    dunning_sent_3=A dunning_sent_7=B dunning_sent_15=C
    companies_synced=D"
```

## Templates de relance (3 niveaux dégradés)

| Niveau | Délai | Ton | Action visible |
|---|---|---|---|
| J+3 | 3-6 j | Amical, "petit rappel" | Lien Stripe hosted_invoice_url |
| J+7 | 7-14 j | Ferme, "merci de régulariser sous 7 j" | + invitation à répondre humain |
| J+15 | 15+ j | Escalade, "suspension imminente sous 48 h" | + ouverture solution amiable |

Tous les emails partent depuis `contact@omnividens.fr` avec la signature
canonique (variante C, mémoire `reference_argos_email_signature.md`).

## Calcul MRR canonique

- **Mensuel** : `unit_amount * quantity / 100`
- **Annuel** : `(unit_amount * quantity / 100) / 12`
- **Total MRR** : somme des subs `status in ('active', 'trialing')`
- **ARR** : `MRR * 12`
- Devise non-EUR : ignorée + warning loguru (Argos en EUR-only, cf. `pricing.md`)

## Conformité facture FR (P7.2)

Stripe Tax peut générer des factures conformes FR si activé côté compte
(SIREN, TVA intracommunautaire, conditions de paiement, taux de pénalité
de retard, indemnité forfaitaire 40 €). Vérifier au premier vrai paiement
et activer ``Stripe Tax > France`` si pas déjà fait. Sinon helper Python
à ajouter en P17.

## Setup cron — Windows Task Scheduler

```powershell
$uvExe = "C:\Users\pauzzle\.local\bin\uv.exe"
$workDir = "C:\Users\pauzzle\Desktop\argos-ops"
$action = New-ScheduledTaskAction -Execute $uvExe `
  -Argument 'run python scripts/run_finance_bot.py' `
  -WorkingDirectory $workDir
$trigger = New-ScheduledTaskTrigger -Daily -At 6:00am
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable `
  -DontStopIfGoingOnBatteries -AllowStartIfOnBatteries `
  -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName "argos-ops-finance-bot" `
  -Action $action -Trigger $trigger -Settings $settings `
  -Description "Argos Ops FinanceBot — sync Stripe + dunning quotidien (P7)"
```

## Test live immédiat

```bash
uv run python scripts/run_finance_bot.py
```

Premier run en mode test recommandé (`sk_test_...`). Le compte Stripe
test peut être peuplé via le dashboard Stripe avec quelques subs/invoices
fictives pour valider le calcul MRR + dunning.

## Tests

Cf. `tests/test_finance_bot.py` :

- `test_classify_dunning_level_*` — 4 frontières (J+0/+3/+7/+15)
- `test_compute_mrr_eur_*` — mensuel, annuel, mix, devise non-EUR ignorée
- `test_render_dunning_email_*` — 3 niveaux, placeholders rendus
- `test_finance_stats_summary` — format `output_summary`
- `test_build_finance_embed_*` — couleurs (green/yellow/red selon état)

## Limites connues

- **Polling toutes les 24 h** : pas de réaction temps réel aux échecs
  Stripe. À reconsidérer si on observe des frictions clients (passer
  aux webhooks Stripe en P15 ou P19)
- **Pas de retry** sur échec SMTP relance : si Zimbra plante, la relance
  ne sera pas re-tentée avant 24 h. Acceptable pour P7
- **Multi-devise** : ignoré, on log uniquement EUR. Si Argos s'ouvre
  à USD plus tard, étendre `_eur_from_cents`
