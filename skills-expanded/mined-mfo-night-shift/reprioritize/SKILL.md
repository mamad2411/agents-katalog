---
name: reprioritize
description: "Re-prioritize a skill's backlog using live Skylight production data. Triggered every 5 completed items."
allowed-tools: Bash(echo:*), Bash(cat:*), mcp__skylight__list_endpoints, mcp__skylight__get_endpoint_detail, mcp__skylight__get_trace_node_detail, mcp__skylight__select_app, mcp__skylight__select_component
---

# Reprioritize backlog

**Contexte :** Re-prioriser le backlog d'un skill en utilisant les donnees de production Skylight.
Ce skill est un meta-skill : il ne produit pas de PR, il met a jour les priorites du backlog.

**Input :**
- Skill a reprioriser : `$ARGUMENTS` (ex: `n1-query-fix`)
- Backlog actuel : `.skill-context.json` contient le dump du backlog pending

---

## Etape 1 : Lire le backlog actuel

Lire `.skill-context.json` qui contient :
```json
{
  "skill": "n1-query-fix",
  "items": [
    {
      "id": 42,
      "item": "app/models/dossier.rb",
      "priority": 8,
      "context": { "total_waste_ms": 5400, "endpoints": ["..."] }
    }
  ]
}
```

## Etape 2 : Query Skylight

1. **Selectionner l'app** : `select_app` → "DS", puis `select_component` → "web:production"
2. **Lister les endpoints** : `list_endpoints(sort_by: "agony", limit: 50)`
3. **Pour chaque endpoint avec inspection N+1** : `get_endpoint_detail` pour obtenir les patterns N+1 avec tables, reps, waste

## Etape 3 : Calculer les nouvelles priorites

Pour chaque item du backlog :

1. **Croiser avec les endpoints Skylight** : trouver les endpoints qui touchent le model/concern de l'item
2. **Calculer le score** :
   ```
   waste = SUM(endpoint_rpm * avg_reps * per_query_ms) pour chaque pattern N+1 lie
   ```
3. **Normaliser en priorite 0-10** :
   - 10 : waste > 10000ms (critique)
   - 7-9 : waste 3000-10000ms (haut)
   - 4-6 : waste 1000-3000ms (moyen)
   - 1-3 : waste < 1000ms (bas)
   - 0 : aucun N+1 detecte en prod (peut-etre deja fixe)

4. **Detecter les items resolus** : si un endpoint n'a plus d'inspection N+1 sur la table concernee → l'item a ete fixe upstream, marquer priority 0

## Etape 4 : Produire le resultat

Ecrire le resultat sur stdout en JSON **et rien d'autre** :

```json
{
  "updates": [
    { "id": 42, "priority": 9, "reason": "waste 8200ms (DossiersController#index 50reps)" },
    { "id": 43, "priority": 0, "reason": "N+1 resolved in prod — skip" }
  ],
  "skip_ids": [43],
  "summary": "3 items reprioritized, 1 resolved upstream"
}
```

Le champ `skip_ids` liste les items dont la priorite tombe a 0 (N+1 plus detecte en prod).
Le reconciler lira ce JSON pour appliquer les updates.

---

## Regles critiques

1. **Pas de PR** : ce skill ne modifie aucun code, il produit uniquement du JSON
2. **Pas de modification du backlog** : le reconciler applique les updates, pas le skill
3. **Skylight obligatoire** : sans acces MCP Skylight, le skill ne peut pas fonctionner — echouer proprement
4. **Idempotent** : relancer le skill doit produire le meme resultat (aux variations de trafic pres)
5. **Format strict** : le JSON de sortie doit etre parseable par le reconciler
