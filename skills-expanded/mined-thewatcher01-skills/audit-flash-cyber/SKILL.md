---
name: audit-flash-cyber
description: "Audit passif OSINT de sécurité sur un domaine. Vérifie DNS (SPF/DKIM/DMARC), headers HTTP (HSTS, CSP, X-Frame-Options), certificat SSL. Utiliser quand l'utilisateur demande d'auditer la sécurité d'un site ou domaine."
metadata: { "openclaw": { "emoji": "🛡️" } }
user-invocable: true
---

# Audit Flash Cyber

## Objectif

Réaliser un **audit de sécurité passif** (OSINT uniquement) sur un domaine cible et produire une note de A à F avec les findings détaillés.

## Déclencheurs

- `/audit example.com`
- `/audit-cyber example.com`
- "audite la sécurité de example.com"
- "vérifie les headers de sécurité de ce site"
- "est-ce que example.com est bien sécurisé ?"

## IMPORTANT — Audit passif uniquement

**Aucun scan actif autorisé.** Ce skill utilise uniquement :
- Des requêtes DNS publiques (`dig`, `nslookup`)
- Des requêtes HTTP standard (`curl` avec headers)
- La lecture du certificat SSL (`openssl s_client`)

Pas de port scan, pas de fuzzing, pas de tentative d'intrusion.

## Script

Le script `scripts/audit.sh` exécute les vérifications. Outils disponibles dans le conteneur Docker : `curl`, `dig`, `openssl`.

### Usage

```bash
bash scripts/audit.sh example.com
```

## Vérifications effectuées

### 1. DNS — Authentification email

| Check | Commande | Critère OK |
|-------|----------|------------|
| SPF | `dig TXT example.com` | Enregistrement `v=spf1` présent |
| DKIM | `dig TXT default._domainkey.example.com` | Enregistrement `v=DKIM1` présent |
| DMARC | `dig TXT _dmarc.example.com` | Enregistrement `v=DMARC1` avec `p=reject` ou `p=quarantine` |

### 2. Headers HTTP — Sécurité web

| Check | Commande | Critère OK |
|-------|----------|------------|
| HSTS | `curl -sI https://example.com` | Header `Strict-Transport-Security` présent avec `max-age >= 31536000` |
| CSP | `curl -sI https://example.com` | Header `Content-Security-Policy` présent |
| X-Frame-Options | `curl -sI https://example.com` | Header `X-Frame-Options` = `DENY` ou `SAMEORIGIN` |
| X-Content-Type-Options | `curl -sI https://example.com` | Header `X-Content-Type-Options` = `nosniff` |
| Referrer-Policy | `curl -sI https://example.com` | Header `Referrer-Policy` présent |
| Permissions-Policy | `curl -sI https://example.com` | Header `Permissions-Policy` présent |

### 3. SSL/TLS — Certificat

| Check | Commande | Critère OK |
|-------|----------|------------|
| Certificat valide | `openssl s_client -connect example.com:443` | Pas d'erreur de vérification |
| Expiration | Lecture du champ `notAfter` | Expire dans > 30 jours |
| Émetteur | Lecture du champ `issuer` | CA reconnue (Let's Encrypt, DigiCert, etc.) |

## Grille de notation

| Note | Critères |
|------|----------|
| **A** | Tous les checks passent (10/10) |
| **B** | 8-9 checks OK, aucun critique manquant |
| **C** | 6-7 checks OK, ou DMARC absent |
| **D** | 4-5 checks OK, ou HSTS absent |
| **E** | 2-3 checks OK, problèmes multiples |
| **F** | 0-1 check OK, ou certificat expiré/invalide |

Checks critiques (font baisser d'un cran automatiquement si absents) : HSTS, DMARC, certificat valide.

## Format de sortie

```json
{
  "domaine": "example.com",
  "date_audit": "2026-03-20",
  "note": "C",
  "score": "6/10",
  "checks": {
    "dns": {
      "spf": { "status": "OK", "detail": "v=spf1 include:_spf.google.com ~all" },
      "dkim": { "status": "KO", "detail": "Aucun enregistrement DKIM trouvé" },
      "dmarc": { "status": "WARN", "detail": "v=DMARC1; p=none — politique trop permissive" }
    },
    "headers": {
      "hsts": { "status": "OK", "detail": "max-age=31536000; includeSubDomains" },
      "csp": { "status": "KO", "detail": "Header absent" },
      "x_frame_options": { "status": "OK", "detail": "SAMEORIGIN" },
      "x_content_type_options": { "status": "OK", "detail": "nosniff" },
      "referrer_policy": { "status": "OK", "detail": "strict-origin-when-cross-origin" },
      "permissions_policy": { "status": "KO", "detail": "Header absent" }
    },
    "ssl": {
      "certificat_valide": { "status": "OK", "detail": "Vérifié par Let's Encrypt" },
      "expiration": { "status": "OK", "detail": "Expire le 2026-06-15 (87 jours)" },
      "emetteur": { "status": "OK", "detail": "Let's Encrypt Authority X3" }
    }
  },
  "recommandations": [
    "Configurer un enregistrement DKIM pour l'authentification email",
    "Passer la politique DMARC de p=none à p=quarantine minimum",
    "Ajouter un header Content-Security-Policy",
    "Ajouter un header Permissions-Policy"
  ],
  "approche_commerciale": "Le domaine présente des lacunes classiques en sécurité web. Un accompagnement DevSecOps permettrait de corriger ces points rapidement."
}
```

## Règles

- **JAMAIS de scan actif** : uniquement requêtes DNS publiques, HTTP HEAD/GET, et lecture certificat SSL.
- Timeout de 10 secondes par requête. Si timeout, noter `"status": "TIMEOUT"`.
- Si le domaine ne résout pas, retourner une erreur claire.
- Toujours inclure des recommandations actionnables.
- L'approche commerciale doit être factuelle et non alarmiste.
