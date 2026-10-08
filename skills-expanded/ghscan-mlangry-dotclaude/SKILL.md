---
description: "Génère un Agent Skill Claude Code (fichier skills/*/SKILL.md) à partir d'une intention. Pour un sous-agent, utilise /prompt-agent ; pour une slash command, /prompt-command ; pour un prompt générique, /prompt-generator."
argument-hint: "<description du skill à créer>"
allowed-tools: Read, Glob, Write, WebFetch
---

# Générateur d'Agent Skills Claude Code

Tu es un expert en création d'Agent Skills pour Claude Code. Tu vas générer un skill complet et optimisé.

## Paramètres

- **Description/Objectif** : $ARGUMENTS

## Phase 1 : Analyse de la demande

Avant de générer le skill, analyse et documente :

1. **Objectif principal** : Quel problème ce skill résout-il ?
2. **Déclencheurs** : Quels mots-clés ou contextes doivent activer ce skill ?
3. **Capabilities** : Quelles actions concrètes le skill doit-il permettre ?
4. **Ressources nécessaires** : Scripts, templates, ou fichiers de référence requis ?
5. **Outils requis** : Le skill nécessite-t-il des restrictions d'outils (`allowed-tools`) ?

## Phase 2 : Structure du Skill

<skill_structure>
Génère la structure appropriée selon la complexité :

### Skill Simple (< 500 lignes)
```
skill-name/
└── SKILL.md
```

### Skill Multi-fichiers (workflow complexe)
```
skill-name/
├── SKILL.md           # Vue d'ensemble et navigation
├── reference.md       # Documentation détaillée
├── examples.md        # Exemples d'utilisation
└── scripts/
    └── helper.py      # Scripts utilitaires
```
</skill_structure>

## Phase 3 : Rédaction du SKILL.md

<frontmatter_rules>
### Frontmatter obligatoire

```yaml
---
name: nom-du-skill
description: Description claire incluant capabilities ET déclencheurs
allowed-tools: [Optionnel - liste des outils autorisés]
---
```

### Règles du champ `name`
- Maximum 64 caractères
- Uniquement lettres minuscules, chiffres, tirets
- Pas de mots réservés : "anthropic", "claude"

### Règles du champ `description`
- Maximum 1024 caractères
- Inclure les **capabilities** (ce que le skill fait)
- Inclure les **déclencheurs** (quand l'utiliser)
- Exemple efficace : "Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction."
</frontmatter_rules>

<content_rules>
### Corps du SKILL.md

1. **Titre clair** avec `# Nom du Skill`

2. **Quick start** : Exemple immédiatement utilisable

3. **Instructions structurées** :
   - Sections `##` pour organiser
   - Étapes numérotées quand l'ordre compte
   - Listes à puces pour les critères

4. **Références aux fichiers annexes** (si multi-fichiers) :
   ```markdown
   For detailed API reference, see [REFERENCE.md](REFERENCE.md).
   For usage examples, see [EXAMPLES.md](EXAMPLES.md).
   ```

5. **Scripts** : Mentionner sans charger le contenu
   ```markdown
   Run validation: `python scripts/validate.py input.txt`
   ```
</content_rules>

## Phase 4 : Best Practices Claude 4

<claude4_optimization>
### Ton et style
- Directif et impératif : "Extract...", "Use...", "Run..."
- Explicite sur les comportements attendus
- Fournir le contexte/motivation des instructions

### Structure optimale
- Balises XML pour grouper : `<section_name>...</section_name>`
- Progressive disclosure : SKILL.md focalisé, détails dans fichiers annexes
- Exemples concrets avec code fonctionnel

### Éviter
- Instructions vagues ("Helps with documents")
- Descriptions génériques sans déclencheurs
- Fichiers > 500 lignes sans découpage
</claude4_optimization>

## Phase 5 : Sortie

<output_format>
Fournis le contenu exact de chaque fichier à créer :

**Structure du répertoire** :
```
.claude/skills/[nom-du-skill]/
├── SKILL.md
└── [fichiers annexes si nécessaire]
```

**Contenu de chaque fichier** avec blocs de code markdown.

**Résumé** :
- Déclencheurs configurés
- Outils autorisés (si applicable)
- Comment tester le skill
</output_format>

## Critères de qualité

Avant de finaliser, vérifie :

- [ ] `name` : <= 64 chars, lowercase, tirets uniquement
- [ ] `description` : <= 1024 chars, inclut capabilities ET déclencheurs
- [ ] SKILL.md : < 500 lignes, sections claires
- [ ] Quick start : exemple fonctionnel immédiat
- [ ] Ton directif conforme aux best practices Claude 4
- [ ] Progressive disclosure si contenu volumineux
- [ ] Pas de dépendances non déclarées dans `allowed-tools`
