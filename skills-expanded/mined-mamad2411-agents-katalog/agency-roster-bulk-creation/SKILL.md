---
name: agency-roster-bulk-creation
description: Bulk-create hundreds of AI agent skills for the Agency Roster repo — naming, conflict resolution, batch delegation, GitHub sync, and monetization prep.
author: "Ziri Yahi"
tags: [agency-roster, bulk-creation, agents, skills, github, delegation]
---

# Agency Roster — Bulk Agent Creation

## Rôle
Workflow complet pour créer des centaines d'agent skills en masse, les pousser sur GitHub, et préparer la monétisation.

## Quand l'utiliser
- Création en masse d'agents pour l'Agency Roster
- Expansion du repo github.com/ziri22/agency-roster
- Préparation de packs pour Gumroad/Fiverr

## Workflow typique

### 1. Planification des vagues
- Organiser les agents par domaines (Engineering, Data, Business, Algérie, etc.)
- 25-30 agents par vague (limite pratique du delegate_task)
- Vérifier les conflits de noms AVANT de créer

### 2. Création par délégation
```
delegate_task(role=orchestrator, toolsets=["skills"])
```
- Le subagent utilise `skills_list` pour vérifier les doublons
- Puis `skill_manage(action='create', category='business')` pour chaque agent
- YAML frontmatter obligatoire: name, description, author: "Ziri Yahi", tags
- Contenu markdown en français: Rôle, Quand l'utiliser, Compétences clés, Workflow typique, Pièges connus, Connexions Knowledge Graph

### 3. Convention de nommage
- Format: `agent-<domaine>-<specialite>[-vN]`
- Exemples: `agent-backend-python-v2`, `agent-fintech-dz-v3`
- Si un nom existe déjà → ajouter suffixe `-v2`, `-v3`, `-v4`
- Toujours vérifier avec `skills_list` avant création

### 4. Structure de chaque SKILL.md
```markdown
---
name: Agent Name
description: Description courte en français
author: "Ziri Yahi"
tags: [tag1, tag2, tag3]
---

# Agent Name

## Rôle
Description du rôle en 2-3 phrases.

## Quand l'utiliser
- Cas d'usage 1
- Cas d'usage 2

## Compétences clés
- **Compétence 1** : détail
- **Compétence 2** : détail

## Workflow typique
1. Étape 1
2. Étape 2
3. Étape 3

## Pièges connus
- Piège 1
- Piège 2

## Connexions Knowledge Graph
- `agent-connexe-1` — Relation
- `agent-connexe-2` — Relation
```

### 5. Synchronisation GitHub
Après chaque vague majeure (50+ agents):
```bash
cd /tmp/agency-roster
rm -rf skills/business/agent-* skills/business/agency-* skills/business/affiliate-*
cp -r ~/.hermes/skills/business/agent-* skills/business/
cp -r ~/.hermes/skills/business/agency-* skills/business/ 2>/dev/null
cp -r ~/.hermes/skills/business/affiliate-* skills/business/ 2>/dev/null
git add -A && git commit -m "🏢 N agents — description" && git push
```

### 6. Mise à jour du README
- Mettre à jour le count d'agents
- Lister les nouvelles divisions si nécessaire
- Commit avec le même push

### 7. Préparation monétisation
- `GUMROAD-COPIER.md` — Description produit prête à copier
- `FIVERR-COPIER.md` — Gig complet avec 3 tiers de prix
- `auto-publish.sh` — Script de publication via API (nécessite token)
- Zip pack: `zip -r agency-roster-pack.zip skills/ LICENSE README.md GUMROAD.md FIVERR.md`

## Pièges connus
- **Conflits de noms** : Toujours vérifier avec `skills_list` avant création. Les subagents ajoutent parfois des suffixes `-v2`/`-v3` automatiquement.
- **Limite de délégation** : 25-30 agents par subagent. Au-delà, le subagent atteint la limite d'itérations.
- **Git sync** : Toujours `rm -rf` les anciens fichiers avant de copier les nouveaux pour éviter les fichiers orphelins.
- **Author consistency** : Toujours `author: "Ziri Yahi"` (avec guillemets).
- **Langue** : Contenu en français, tags en anglais.
- **Nombre d'agents** : Le count dans `~/.hermes/skills/business/` peut différer du repo Git si le sync n'est pas fait.
- **Mémoire contextuelle** : Après 600+ agents, les subagents prennent plus de temps. Préférer des vagues de 25-30.

## Références
- Repo: https://github.com/ziri22/agency-roster
- Skills directory: `~/.hermes/skills/business/`
- Category: `business`
- Author: Ziri Yahi