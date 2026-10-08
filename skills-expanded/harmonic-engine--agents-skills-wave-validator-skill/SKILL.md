---
name: wave-validator
description: >-
  Vérifier automatiquement l'écosystème ondulatoire : les 13 primitives wave_lang contre
  leurs valeurs de référence, les 19 adaptateurs wave_bridge contre leurs contrats,
  et les tables d'équivalence (fichiers, imports, statuts). Utilise ce skill dès que
  l'utilisateur veut valider l'écosystème, exécuter les tests, vérifier la conformité,
  détecter une désynchronisation tables/code, préparer une release, ou intégrer des
  gates de validation en CI.
---

# Wave Validator — Conformité automatisée de l'écosystème ondulatoire

Ce skill vérifie que l'écosystème ondulatoire respecte ses contrats.
C'est le **verdict objectif** entre les tables d'équivalence (la spécification)
et le code réel (l'implémentation).

## Les 3 niveaux de validation

| Niveau | Cible | Ce qui est vérifié |
|--------|-------|--------------------|
| **1. Primitives** | `wave_lang.py` | Les 13 primitives contre les valeurs de référence (norme, résonance, roundtrip, déterminisme) |
| **2. Adaptateurs** | `wave_bridge.py` | Les 19 adaptateurs contre leurs contrats (normalisation, bornes, roundtrip, comportement) |
| **3. Équivalences** | Tables LLM + TTS | Chaque équivalence ✅ → fichier existe ; chaque 🆕 → fichier réellement manquant |

Bonus : **détection de dérive** root vs vital-ka (copies divergentes).

## Usage

```bash
# Tout valider (3 niveaux + dérive)
python validator.py

# Niveau spécifique
python validator.py --level 1   # primitives uniquement
python validator.py --level 2   # adaptateurs uniquement
python validator.py --level 3   # équivalences uniquement

# Rapport JSON
python validator.py --json

# Depuis un autre répertoire
python validator.py --root ../.. --python-dir vital-ka/core/python
```

## Exit code (pour CI)

- `0` : tous les tests passent → la release est verte
- `1` : au moins un test échoue → la release est bloquée

## Valeurs de référence (niveau 1)

Source : `.agents/skills/langage-ondulatoire/references/primitives.md`

| Test | Attendu |
|------|---------|
| \|encode(x)\| | 1.000 |
| decode après encode "lumiere" | score 1.0 (top-1 = lumiere) |
| unbind(bind(a,b), b) | recovery ≈ 0.73 |
| resonate(ψ, ψ) / orthogonal | 1.0 / ≈ 0.04 |
| rotate(ψ, π) | résonance −1.000 |
| interfere ε=0.15 | préserve la base (0.99) |
| diffract → diffract(inverse) | identité 1.000 |
| phase_shift(ψ, π/2) | orthogonal 0.000 |
| abc_kernel | K(0)=1, K(100)→0 |
| superpose / emerge / mémoire | normalisés et finis |
| encode déterministe | identique à 1e-6 |

## Contrats des adaptateurs (niveau 2)

Chaque adaptateur wave_bridge promet :
1. **Même API** que le module remplacé (drop-in)
2. **Délégation** aux primitives wave_lang (pas de numpy maison)
3. **Sorties normalisées** (‖ψ‖ = 1, scores bornés)
4. **Roundtrip** stable (synthèse après analyse, unbind après bind)

Voir `references/contracts.md` pour le détail par adaptateur.

## Intégration avec les autres skills

- **wave-orchestrator** : `orchestrator.py verify` lance ce validator et rapporte
- **wave-bridge** : après la création d'un adaptateur, le validator confirme la conformité
- **langage-ondulatoire** : les valeurs de référence du niveau 1 viennent de ce skill
- **wave-ir-compiler** : le validator couvre les primitives ; `validate()` couvre les programmes AST
