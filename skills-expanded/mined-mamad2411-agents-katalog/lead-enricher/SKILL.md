---
name: lead-enricher
description: Enrichit un lead BtoB depuis un input minimal (prénom + nom + domaine entreprise) — devine l'email pro, le titre, signaux ICP (taille boîte, secteur, levée récente). Heuristiques + sources publiques uniquement (pas d'Apollo / Hunter / Clearbit en mode shadow, intégration optionnelle P13.B si budget). Score BANT 0-100 selon `ICP.md`. Utilise ce skill quand le user prépare une séquence outbound, importe une liste CSV depuis LinkedIn Search, ou pendant /enrich-lead.
---

# lead-enricher

Skill **éditorial + analytique**. Transforme une ligne CSV brute
(« Marc Dupont, RSSI, acme.fr ») en une fiche prospect actionnable :
email pro deviné, signaux ICP scorés, BANT 0-100.

> **Mode shadow P13-DRAFT (futur P13)** : pas d'appel API à Apollo /
> Hunter / Clearbit. Heuristiques déterministes + recherche manuelle
> via sources publiques (LinkedIn profile public si fourni, page
> "À propos" du domaine, dépôts GitHub publics si entreprise tech, etc.).
> Le passage à un enrichment API est conditionné à un budget marketing
> dédié (~50-100 €/mois pour Apollo trial ou Hunter, P13.B).

## Inputs

```yaml
# Minimal — au moins l'une des combinaisons suivantes
full_name: "Marc Dupont"
domain: "acme.fr"          # ou
linkedin_url: "https://linkedin.com/in/marc-dupont-rssi"
# Optionnel — accélère + précise l'enrichissement
title_hint: "RSSI"          # déjà connu via LinkedIn search
company_name: "ACME"
```

## Outputs

Fichier markdown dans `data/outbound/enriched/YYYY-MM-DD-<slug>.md` :

```yaml
---
status: draft | validated | rejected | dnq    # draft / validé / rejeté / does-not-qualify
date_enriched: 2026-05-14
full_name: "Marc Dupont"
email_guesses:                                  # par ordre de confiance
  - email: "marc.dupont@acme.fr"
    confidence: 0.85
    pattern: "firstname.lastname"
  - email: "m.dupont@acme.fr"
    confidence: 0.55
    pattern: "f.lastname"
domain: "acme.fr"
linkedin_url: "https://linkedin.com/in/marc-dupont-rssi"
company_name: "ACME"
title: "RSSI"                                   # ou null si pas trouvé
title_seniority: "C-level" | "lead" | "ic" | "unknown"
icp_signals:
  persona: "marc"                               # marc / sarah / thomas / null
  company_size_band: "50-200" | "200-1000" | ...
  industry: "SaaS BtoB" | "MSP" | "fintech" | ...
  recent_funding: null | "series_a" | "series_b" | ...
  hiring_security: true | false                 # poste sécu ouvert récemment ?
  cloud_migration: true | false                 # signaux migration cloud récents
bant_score: 0-100
bant_breakdown:
  budget: 0-25
  authority: 0-25
  need: 0-25
  timeline: 0-25
disqualifiers: []                               # raisons éventuelles de skip
sources:                                        # traçabilité, public uniquement
  - "https://linkedin.com/in/..."
  - "https://acme.fr/about"
  - "https://github.com/acme"
---

## Notes sur le lead

<2-3 phrases factuelles : pourquoi ce lead colle à l'ICP, signaux forts
observés, accroche personnalisée potentielle pour outbound-personalizer.>
```

## Heuristiques email (par ordre de fréquence en BtoB FR/EN)

| Pattern | Exemple (Marc Dupont @ acme.fr) | Confiance baseline |
|---|---|---|
| `firstname.lastname@` | `marc.dupont@acme.fr` | 0.85 |
| `f.lastname@` | `m.dupont@acme.fr` | 0.55 |
| `firstname@` | `marc@acme.fr` | 0.40 |
| `flastname@` | `mdupont@acme.fr` | 0.50 |
| `firstname_lastname@` | `marc_dupont@acme.fr` | 0.15 |
| `lastname.firstname@` | `dupont.marc@acme.fr` | 0.20 |

Ajustements :

- Domaine `gmail.com / outlook.com / yahoo.fr / hotmail.fr` (perso) →
  **disqualify** (intérêt légitime BtoB ne s'applique pas sur emails
  perso, cf. COMPLIANCE.md § 2)
- Domaine MX pointe vers Google Workspace (`google.com`) → `firstname.lastname`
  est très probable (Google Workspace défaut)
- Domaine MX pointe vers Microsoft 365 → `firstname.lastname` aussi
  fréquent
- Boîte < 50 personnes → `firstname@` plus probable
- Boîte > 1000 personnes → `firstname.lastname@` quasi systématique

## Scoring BANT (référentiel `ICP.md`)

| Axe | Signaux qui donnent des points |
|---|---|
| **Budget (0-25)** | Levée série A/B récente +10 ; ARR connu > 5M€ +8 ; pricing plan Argos compatible (Pro 39 € / Team 129 € / Pro Max 249 €) selon taille +5-7 |
| **Authority (0-25)** | Title `C-level` (CISO/RSSI/CTO/VP Eng) +25 ; `lead` (Head of / Lead / Manager) +15 ; `ic` (IC senior) +8 ; `unknown` +0 |
| **Need (0-25)** | Job sécu ouvert dans la boîte +10 ; mention « DAST / SAST / pentest » dans bio/posts publics +8 ; secteur réglementé (fintech, santé, RGPD-sensible) +7 |
| **Timeline (0-25)** | Migration cloud / refonte produit annoncée récemment +15 ; annonce d'audit sécurité externe imminent +20 ; sinon estimer 0-10 selon signaux faibles |

Total :

- **80-100** : `lead_chaud` — outbound immédiat, séquence courte (3
  touches)
- **60-79** : `lead_tiede` — outbound nurture (séquence 5 touches,
  espacée)
- **40-59** : `lead_froid` — newsletter / content only, pas d'outbound 1:1
- **< 40** ou disqualifiers présents : `dnq` (does not qualify) —
  skip, ne pas relancer

## Disqualifiers (skip immédiat — pas de relance, pas de stockage CRM
au-delà de l'audit anti-spam) :

- Email perso (gmail / outlook / yahoo / hotmail / icloud / proton)
- Domaine dans `data/outbound/blocklist.txt` (liste interne, mainted manuellement)
- Boîte concurrente directe (Acunetix, Detectify, Burp/PortSwigger,
  Intruder, Pentera, HackerOne, Bugcrowd, etc. — cf. `competitor_compare.md`)
- Title non-décideur sécu (RH, comm, finance pure, juridique pur)
  — sauf si la boîte est très petite (< 20 pers, le RSSI peut être
  le CEO/CTO directement)
- Boîte < 10 personnes (sub-ICP, budget probablement insuffisant pour
  Pro Max — éventuellement Pro 39 €/mois mais ROI outbound faible)

## Procédure

### 1. Validation input

- Si `full_name` ou (`domain` OU `linkedin_url`) manquants → demander
- Si `domain` ressemble à email perso → flag immédiat `dnq` + raison

### 2. Recherche publique (humain-in-the-loop)

L'humain (toi en lisant ce skill, ou le fondateur) :

- Ouvre `linkedin_url` (si fourni) ou cherche LinkedIn par nom +
  domaine
- Note : title exact, durée dans le poste, secteur, séniorité visible
- Ouvre `https://<domain>` page "À propos" + page Carrières
- Si tech : check `https://github.com/<orgname>` pour activité +
  stack signalée
- Recherche « `<company> levée fonds` » sur Google News pour signal funding

### 3. Email guess

- Générer les 3-5 patterns candidats avec confidence baseline
- Si MX domaine connu (Google Workspace / Microsoft 365) → boost le
  pattern le plus probable
- **Aucune validation SMTP** — pas de vérif par bounce (RGPD + risque
  flag spam au domaine source). On envoie au top guess et on accepte
  le bounce rate.

### 4. BANT score

- Compute selon la grille § « Scoring BANT »
- Si total < 40 OU disqualifier → `status: dnq` direct, pas
  d'écriture si l'humain le préfère
- Sinon → drafter le markdown

### 5. Validation finale

- Preview frontmatter complet + notes
- Demander : « OK pour écrire dans
  `data/outbound/enriched/<filename>.md` ? »
- Slug : kebab-case de `<full_name>-<domain>` tronqué 50 chars

### 6. Notif Discord (optionnel)

Pousser sur `DISCORD_WEBHOOK_OPS_LOGS` :
« Lead enrichi : <name> @ <domain> · BANT <score> · status=<status> ».

## Anti-patterns à refuser

- **Email guess sans sources** — toujours lister 1-3 sources publiques
- **Score BANT inventé** — chaque point doit pouvoir être justifié par
  un signal observé (lister les signaux dans `bant_breakdown` mental)
- **Skipper les disqualifiers** — RGPD strict, on ne stocke pas en
  CRM un lead qu'on a marqué `dnq`
- **Scraper des données privées** — pas de credentials LinkedIn,
  pas de Sales Navigator scrape, pas de bypass paywalls. Sources
  publiques uniquement.
- **Persona forcé** — si les signaux ne pointent pas clairement vers
  Marc/Sarah/Thomas → `persona: null`, sans forcer

## Liens

- ICP : `data/knowledge_base/ICP.md` (référentiel personas + signaux)
- Anti-disparagement : `data/knowledge_base/competitor_compare.md` (liste boîtes concurrentes)
- Skill cousin : `outbound-personalizer` (1 ligne hyper-perso à partir
  du fichier enriched)
- Compliance : `docs/COMPLIANCE.md` § 2 (intérêt légitime BtoB, opt-out)
- Plan P13 OutboundBot : `docs/ARGOS_OPS_PLAN.md` § Partie 13
