---
name: dossierfacile-complete-dossier
description: Complète intégralement un dossier DossierFacile à partir d'un prompt en langage naturel. Orchestre l'authentification, la collecte d'informations, la lecture du profil existant et le remplissage via l'API. Utilise ce skill quand un usager demande à remplir, compléter ou soumettre son dossier DossierFacile.
---

# Complétion d'un dossier DossierFacile

**Périmètre : dossier individuel (`ALONE`), sans garant.**

## Environnement

Si l'usager n'a pas précisé d'environnement, utiliser **preprod par défaut**.  
Lire [`dossierfacile-config/environments.md`](../dossierfacile-config/environments.md) pour résoudre `${SSO_URL}`, `${API_URL}`, `${TENANT_URL}` et transmettre l'environnement choisi aux skills appelés.

## Checklist de progression

Copier et suivre cette checklist :

```
- [ ] 0. Authentification — token obtenu
- [ ] 1. Profil lu — sections manquantes identifiées
- [ ] 2. Informations collectées auprès de l'usager
- [ ] 3a. Noms enregistrés
- [ ] 3b. Type de candidature enregistré (ALONE)
- [ ] 4a. Pièce d'identité soumise
- [ ] 4b. Situation d'hébergement soumise
- [ ] 4c. Situation professionnelle soumise
- [ ] 4d. Ressources financières soumises
- [ ] 4e. Avis d'imposition soumis
- [ ] 5. Profil re-vérifié — 5 catégories présentes
- [ ] 6. Déclaration sur l'honneur soumise
- [ ] 7. Dossier confirmé en statut TO_PROCESS
```

## Étape 0 — Authentification

Lire et suivre [`dossierfacile-auth/SKILL.md`](../dossierfacile-auth/SKILL.md).

Résultat attendu : `access_token` valide, vérifié par un `GET /api/tenant/profile` retournant `200 OK`.

## Étape 1 — Lecture du profil existant

Lire et suivre [`dossierfacile-read-profile/SKILL.md`](../dossierfacile-read-profile/SKILL.md).

Identifier ce qui est **déjà rempli** et ce qui **manque** parmi :
- `firstName` / `lastName` / `zipCode`
- `applicationType`
- Documents : `IDENTIFICATION`, `RESIDENCY`, `PROFESSIONAL`, `FINANCIAL`, `TAX`
- `honorDeclaration`

Ne collecter et ne soumettre que ce qui manque.

## Étape 2 — Collecte des informations manquantes

Lire [`dossierfacile-collect-info/SKILL.md`](../dossierfacile-collect-info/SKILL.md).

Ne poser que les questions correspondant aux sections absentes du profil.  
Attendre la confirmation de l'usager sur le récapitulatif avant de procéder.

## Étape 3 — Soumission des données via l'API

Lire [`dossierfacile-write-api/SKILL.md`](../dossierfacile-write-api/SKILL.md) et [`dossierfacile-write-api/api-reference.md`](../dossierfacile-write-api/api-reference.md).

Appeler les routes dans cet ordre :

1. `POST /api/register/names` — si noms manquants
2. `POST /api/register/application/v2` — si `applicationType` absent (`{ "applicationType": "ALONE" }`)
3. Les routes de documents manquantes, **dans n'importe quel ordre** :
   - `POST /api/register/documentIdentification`
   - `POST /api/register/documentResidency`
   - `POST /api/register/documentProfessional`
   - `POST /api/register/documentFinancial`
   - `POST /api/register/documentTax`

Après chaque appel, vérifier que la réponse est `200 OK` ou `201 Created`.

## Étape 4 — Vérification avant validation

Faire un nouveau `GET /api/tenant/profile` et vérifier que les 5 catégories de documents sont présentes.

Si une catégorie est encore absente : soumettre le document manquant avant de continuer.

## Étape 5 — Déclaration sur l'honneur

Une fois les 5 catégories confirmées :

```
POST /api/register/honorDeclaration
{ "honorDeclaration": true }
```

Informer l'usager : *« Votre dossier a été soumis avec succès. Il est maintenant en cours de vérification par un opérateur DossierFacile. »*

Faire un dernier `GET /api/tenant/profile` et vérifier que `status === "TO_PROCESS"`.

## Gestion des erreurs

| Situation | Action |
|---|---|
| Token expiré (`401`) | Rafraîchir via `dossierfacile-auth` → étape 5 (refresh_token) |
| Document refusé (`documentStatus: "DECLINED"`) | Lire `documentDeniedReasons`, informer l'usager, redemander le fichier corrigé et resoumettre |
| Upload échoué (`400`, `413`) | Vérifier le format/taille du fichier, réessayer avec un fichier valide |
| Profil vide après soumission | Attendre 2–3 secondes et re-GET (traitement asynchrone possible) |

### Détails utiles pour les `400` sur endpoints multipart

- Si l'API signale `noDocument must not be null`, envoyer explicitement `noDocument=false` avec un upload.
- Si l'API signale `categoryStep ... can not be null`, renseigner la valeur attendue selon le sous-type (ex. `TENANT_RECEIPT`, `SALARY_EMPLOYED_MORE_3_MONTHS`, `TAX_FRENCH_NOTICE`).
- Pour `typeDocumentFinancial=SALARY`, fournir `monthlySum` strictement positif.
