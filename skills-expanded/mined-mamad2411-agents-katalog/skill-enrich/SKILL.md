---
name: skill-enrich
description: Enrichit la section "Learnings" d'un skill existant à partir des apprentissages de la session en cours. À invoquer quand un pattern, piège, ou bonne pratique a émergé et mérite d'être capitalisé pour les sessions futures.
---

# Skill : Skill Enrich

Ajoute des apprentissages durables dans la section `## Learnings` d'un skill existant.

## Procédure

1. **Identifier le skill cible** (si pas fourni par l'utilisateur) :
   - Lister les skills disponibles : `ls ~/.claude/skills/`
   - Proposer le plus pertinent en fonction du sujet de l'apprentissage

2. **Distiller l'apprentissage** :
   - Formuler en **règle ou pattern actionnable**, pas en récit
   - Indiquer **quand** ça s'applique (contexte)
   - Indiquer **pourquoi** (raison, incident, contrainte)
   - Garder **concis** : 2-5 lignes max par entrée

3. **Ouvrir le `SKILL.md` du skill cible** :
   `~/.claude/skills/<nom>/SKILL.md`

4. **Ajouter une entrée** sous la section `## Learnings` (créer la section si absente) :

   ```markdown
   ## Learnings

   ### YYYY-MM-DD — <titre court>
   <règle ou pattern>

   **Quand :** <contexte d'application>
   **Pourquoi :** <raison, incident>
   ```

5. **Ne pas dupliquer** : si un learning similaire existe, le compléter plutôt qu'ajouter une nouvelle entrée

6. **Confirmer** à l'utilisateur ce qui a été ajouté (+ diff court)

## Exemples de learnings à capturer

**Dans `/terraform`** :
> ### 2026-04-14 — Éviter `ignore_changes = all` sur OVH MKS
> Utiliser des `ignore_changes` ciblés (ex: `ignore_changes = [nodes[*].flavor_name]`), sinon les drifts sérieux passent inaperçus.
>
> **Quand :** managed K8s OVH, après un update en console
> **Pourquoi :** perdu 2h à chercher un drift masqué par `ignore_changes = all`

**Dans `/bash`** :
> ### 2026-04-14 — `jq -r` + fallback `// empty` pour champs optionnels
> Préférer `$(jq -r '.field // empty' <<<"$json")` à `$(jq -r '.field' <<<"$json")` — évite `null` en string.

## Règles

- **Skill existant seulement** : ne pas créer de skill via enrich (utiliser une invocation dédiée)
- **Date ISO** systématique pour traçabilité et tri
- **Déduplication** : check avant d'ajouter
- **Skill pertinent** : si l'apprentissage croise plusieurs skills, le mettre dans le plus central + éventuellement un pointer ("voir aussi /xxx") dans les autres
- **Ne pas polluer** : tout apprentissage ne mérite pas d'être sauvé. Si c'est évident / trivial / déjà dans la doc officielle → passer.

## Anti-patterns

- Transformer `## Learnings` en journal de bord (trop verbeux)
- Copier des passages de docs officielles
- Ajouter un learning pour chaque micro-détail
- Oublier la date
- Formulations type "j'ai appris que…" → préférer impératif ou description de règle
