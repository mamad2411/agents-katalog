# CLAUDE.md — Instructions permanentes ImmoGest

## LIRE EN PREMIER à chaque session
1. `BRAND_BRIEF.md` — identité, design, vision, utilisateurs
2. `APP_SPEC.md` — chaque écran, formulaire, document généré
3. `DATA_DICTIONARY.md` — tous les champs exacts de la DB
4. `FEATURE_BACKLOG.md` — ce qui est fait / en cours / planifié
5. `INTEGRATIONS.md` — APIs tierces, credentials, statuts
6. `ERROR_LOG.md` — bugs déjà résolus, ne pas reproduire

---

## Règles de code

### Variables CSS — TOUJOURS utiliser ces variables, jamais de couleurs hardcodées
```
--bg (fond principal)       --bg2 (fond carte)        --bg3 (fond section)
--bg4 (fond input)          --text (texte principal)   --text2 (texte secondaire)
--text3 (texte tertiaire)   --border (bordure légère)  --border2 (bordure input)
--accent (#0E6AAF bleu)     --green (#0E7A45)          --red (#B93020)
--radius (8px)              --shadow                   --glass-blur
```

### SESSION — champs exacts (ne jamais inventer d'autres)
```javascript
session.userId       // ID utilisateur
session.tenantId     // ID du cabinet/tenant
session.role         // 'admin' | 'coordinateur' | 'gestionnaire' | 'comptable' | 'agent' | 'bailleur' | 'locataire'
session.type_profil  // 'proprietaire' | 'gestionnaire' | 'cabinet'
session.nom          // prénom + nom
session.telephone    // téléphone (PAS session.tel)
session.nomCabinet   // nom du cabinet
session.plan         // 'gratuit' | 'trial' | 'starter' | 'pro' | 'cabinet'
session.plan_expire  // date expiration plan
// ⚠️ N'EXISTENT PAS : session.ville, session.email, session.tel, session.signataire
```

### Champs critiques — erreurs fréquentes à éviter
```
locataire.entree        (PAS date_entree)
locataire.arrieres      (arriérés en FCFA)
locataire.mois_arrieres (nombre de mois)
immeuble.nom_immeuble   (PAS immeuble.nom seul)
immeuble.ville          (utiliser imm.ville, PAS session.ville)
paiement.remisAuBailleur (avec majuscule A et B)
```

### Scripts index.html
Tous les scripts doivent avoir l'attribut `defer` — ne jamais enlever.

### Commits
Format : `type: description courte`
Types : feat / fix / refactor / docs / style

---

## Workflow obligatoire
1. Lire les specs avant de coder
2. Preview du formulaire/document avant modification
3. Valider avec l'utilisateur
4. Coder la modification
5. Commit
6. Push

---

## Architecture
- **Frontend** : Vanilla JS SPA, app.css, index.html
- **Backend** : Cloudflare Worker (`immogest1.fofefranklin57.workers.dev`)
- **DB** : Supabase PostgreSQL (`uggxfmwpttfsfcirmeqx.supabase.co`)
- **Storage** : Supabase Storage, bucket `marketplace`
- **Deploy** : Cloudflare Pages (auto sur push GitHub `fofefranklin57-rgb/immogest`)
- **Offline** : Service Worker `sw.js` cache-first assets, network-first API

---

## Règles métier importantes
- Honoraires cabinet : ne s'affichent PAS si `session.type_profil === 'proprietaire'`
- `remisAuBailleur` : ne s'affiche PAS si `type_profil === 'proprietaire'`
- Plans : gratuit (1 immeuble / 10 locataires) → starter → pro → cabinet (illimité)
- Invitation locataire/bailleur : générée AUTOMATIQUEMENT à la création
- Invitation collaborateurs : générée MANUELLEMENT avec choix du rôle
