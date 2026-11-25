---
name: screenshot-gist
description: "Create GitHub gist for screenshots. Internal agent called by haml-migration and harden-fix."
allowed-tools: Bash(.claude/skills/screenshot-gist/create-gist.sh:*), Bash(bash .claude/skills/screenshot-gist/create-gist.sh:*), Bash(.claude/skills/screenshot-gist/push-gist.sh:*), Bash(bash .claude/skills/screenshot-gist/push-gist.sh:*), Bash(cp:*), Bash(ls:*)
---

# Screenshot → Gist

**⚠️ RÈGLE ABSOLUE : utiliser UNIQUEMENT les scripts fournis. Ne JAMAIS appeler `gh`, `git clone`, `git push`, `mkdir` ou `echo >` directement — ces commandes ne sont PAS autorisées. Seuls `create-gist.sh` et `push-gist.sh` le sont.**

**Contexte :** `gh gist create` ne supporte PAS les fichiers binaires (PNG). Ce skill contourne la limitation via deux scripts shell qui encapsulent toute la logique.

**Répertoire de travail :** `tmp/<nom>/` — les screenshots ET le clone git du gist vivent dans le même répertoire.

**Input :**
- `$ARGUMENTS` : `<nom> [fichier1.png fichier2.png ...]`
  - 1er argument (obligatoire) : nom du gist (utilisé dans la description et comme nom de répertoire `tmp/<nom>/`)
  - Arguments suivants (optionnels, 1..n) : chemins de screenshots à inclure (déjà dans `tmp/`)

**Output :**
- Si screenshots fournis → gist créé, screenshots poussés, URLs affichées
- Si pas de screenshots → gist créé + `tmp/<nom>/` prêt (le skill appelant dépose ses fichiers après)

**Usage autonome :**
```bash
claude -p "/screenshot-gist <nom> [fichier1.png ...]" --allowedTools "Bash(.claude/skills/screenshot-gist/*),Bash(cp:*),Bash(ls:*)"
```

---

## Phase 1 : Créer le gist + cloner

⚠️ **Appeler le script — ne PAS reproduire les commandes manuellement.**

```bash
.claude/skills/screenshot-gist/create-gist.sh "<nom>"
```

Le script fait tout : crée `tmp/`, le readme, le gist public, configure git auth, clone dans `tmp/<nom>/`.
Il affiche en sortie `GIST_URL=<url>` et `GIST_ID=<id>`. Extraire le user et le gist ID depuis l'URL.

---

## Phase 2 : Copier les screenshots (si fournis)

Si des fichiers ont été passés en arguments :

```bash
cp <fichier1.png> <fichier2.png> ... tmp/<nom>/
```

Puis pousser immédiatement (phase 3+4).

Si aucun fichier passé → s'arrêter ici. Le skill appelant dépose ses screenshots directement dans `tmp/<nom>/` quand il est prêt, puis rappelle la phase 3+4.

---

## Phase 3+4 : Pousser et afficher les URLs

⚠️ **Appeler le script — ne PAS reproduire les commandes manuellement.**

```bash
.claude/skills/screenshot-gist/push-gist.sh <nom> <user> <gist-id> <fichier1.png> [fichier2.png ...]
```

Le script fait `git add` uniquement sur les fichiers listés, commit, push, puis affiche les URLs raw en markdown :

```
![capture.png](https://gist.githubusercontent.com/<user>/<gist-id>/raw/capture.png)
```
