---
name: fr-recherche-emploi
description: Structure a job search for the French/European market — CV format europass, cover letter VOUS-MOI-NOUS, job evaluation scoring, interview prep STAR, salary negotiation with French conventions.
version: "1.0.0"
last-updated: "2026-04-22"
model_tested: "claude-sonnet-4-6"
category: metier-fr
platforms: [claude-code, codex, gemini-cli, cursor, copilot, windsurf, cline]
language: fr
geo_relevance: [fr, eu]
priority: medium
dependencies:
  mcp: []
  skills: []
  apis: []
  data: []
update_sources:
  - url: "https://www.service-public.gouv.fr/particuliers/vosdroits/N500"
    check_frequency: "yearly"
    last_checked: "2026-04-22"
license: MIT
---

# Recherche d'Emploi France / Europe

> **AVERTISSEMENT** : Orientations generales. Ne constitue pas un conseil en carrieres professionnel.

## Quand Utiliser

- Structurer sa recherche d'emploi
- Adapter son CV au format francais/europeen
- Rediger une lettre de motivation
- Evaluer une offre d'emploi
- Preparer un entretien
- Negocier un salaire

## CV Format Francais

### Structure Recommandee
1. **En-tete** : Nom, titre vise, coordonnees, LinkedIn
2. **Accroche** : 2-3 lignes resumant profil + valeur ajoutee
3. **Experience professionnelle** : Anti-chronologique, verbes d'action, resultats chiffres
4. **Formation** : Diplomes avec annee et etablissement
5. **Competences** : Techniques + soft skills + langues (CECRL)
6. **Centres d'interet** : Optionnel, uniquement si pertinent

### Regles FR Specifiques
- **Photo** : Optionnelle (non recommandee pour eviter discrimination)
- **Age/date de naissance** : Optionnel
- **Situation familiale** : Ne pas inclure
- **Longueur** : 1 page (junior), 2 pages max (senior)
- **Format** : PDF uniquement (jamais Word pour ATS)
- **Langue** : Francais sauf poste international

### Optimisation ATS
- Reprendre les mots-cles exacts de l'offre
- Titres de sections standards (Experience, Formation, Competences)
- Pas de tableaux, colonnes, ou mise en page complexe
- Pas d'images ou icones dans le corps

## Lettre de Motivation (VOUS-MOI-NOUS)

### Structure
1. **VOUS** (1 paragraphe) : Ce que vous savez de l'entreprise, pourquoi elle vous interesse
2. **MOI** (1-2 paragraphes) : Vos competences et realisations pertinentes pour le poste
3. **NOUS** (1 paragraphe) : Ce que vous apporteriez ensemble, projection dans le poste

### Regles
- Personnalisee par entreprise (jamais generique)
- Max 1 page
- Resultats chiffres ("+30% de CA", "equipe de 8 personnes")
- Ton professionnel mais pas rigide

## Evaluation d'Offre (Scoring /5)

| Dimension | Poids | Questions |
|-----------|-------|-----------|
| Adequation competences | 25% | Mes competences couvrent-elles 70%+ des exigences ? |
| Evolution de carriere | 20% | Ce poste me fait-il progresser dans ma trajectoire ? |
| Remuneration | 15% | Dans ma fourchette ? Avantages (mutuelle, RTT, teletravail) ? |
| Culture entreprise | 15% | Valeurs compatibles ? Management style ? |
| Localisation/flexibilite | 10% | Teletravail ? Temps de trajet acceptable ? |
| Stabilite/perspectives | 10% | Sante financiere ? Croissance ? |
| Processus recrutement | 5% | Nombre d'etapes raisonnable ? Transparence ? |

Score < 3.0 = Ne pas postuler. Score 3.0-3.9 = Postuler si marche difficile. Score >= 4.0 = Postuler.

## Preparation Entretien (STAR)

Pour chaque competence cle de l'offre, preparer une histoire STAR :

- **S**ituation : Contexte (ou, quand, quel projet)
- **T**ask : Votre responsabilite specifique
- **A**ction : Ce que VOUS avez fait (pas l'equipe)
- **R**esultat : Impact mesurable, chiffre

Preparer 5-8 histoires STAR couvrant : leadership, resolution de probleme, echec+apprentissage, travail d'equipe, initiative, gestion de conflit.

## Negociation Salariale (France)

### Conventions
- Salaire annonce en **brut annuel** (pas mensuel, pas net)
- Conversion brut → net : environ x0.78 (cadre) ou x0.80 (non-cadre)
- Negocier APRES l'offre ecrite, jamais avant

### Fourchette
- Rechercher sur Glassdoor, levels.fyi, talent.io pour le poste
- Demander 10-15% au-dessus de votre minimum acceptable
- Ne jamais donner son salaire actuel en premier

### Elements Negociables (hors salaire)
- Teletravail (jours/semaine)
- RTT supplementaires
- Formation (budget annuel)
- Titre de poste
- Variable/bonus
- Actions/BSPCE (startups)
- Frais de transport/mobilite

## Droits du Candidat (Code du Travail)

- Pas de discrimination (age, sexe, origine, handicap, grossesse)
- Droit de connaitre le motif de refus (demander par ecrit)
- Periode d'essai : 2 mois (employes), 3 mois (agents de maitrise), 4 mois (cadres), renouvelable 1 fois
- Preavis demission : convention collective applicable

## Ce Que Ce Skill Ne Fait PAS

- Ne postule pas a votre place
- Ne garantit pas d'obtenir un emploi
- Ne remplace pas un coach carriere
- Ne couvre pas le droit du travail en profondeur
- Ne gere pas les cas de licenciement/rupture conventionnelle
