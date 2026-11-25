---
name: haml-migration
description: "Migrate HAML to ERB with visual validation. Use when user says 'migrate haml', 'convert to erb', or provides a .haml file."
allowed-tools: Skill(dev-auto-login), Skill(rails-routes), Skill(screenshot-gist), Agent, Bash(git status:*), Bash(git mv:*), Bash(git add:*), Bash(git commit:*), Bash(git diff:*), Bash(git log:*), Bash(git rebase:*), Bash(bun lint:herb:*), Bash(bun format:herb *), Bash(bundle exec rspec spec/components:*), Bash(bundle exec erb_lint:*), Bash(bundle exec rake lint:apostrophe:fix), Bash(bundle exec rubocop:*), Bash(bundle exec brakeman:*), Edit(config/brakeman.ignore), Bash(bin/rails runner:*), Bash(shuf:*), Bash(grep:*), Bash(echo:*), Bash(touch:*), Bash(stat:*), Bash(curl:*), Bash(.claude/skills/screenshot-gist/create-gist.sh:*), Bash(bash .claude/skills/screenshot-gist/create-gist.sh:*), Bash(.claude/skills/screenshot-gist/push-gist.sh:*), Bash(bash .claude/skills/screenshot-gist/push-gist.sh:*), Bash(gh gist create:*), Bash(gh auth setup-git:*), Bash(git clone:*), Bash(mkdir:*), Bash(cp:*), Edit(app/*), Edit(spec/*), Edit(config/*), Write(app/*), Write(spec/*), Write(config/*), Write(tmp/**), Write(pr-description.md)
---

# Migration HAML → ERB

**Contexte :** Migration d'un fichier HAML vers ERB avec validation visuelle via screenshots

**Input :**
- Fichier à migrer : `$ARGUMENTS` (ex: `app/components/alert/alert_component.html.haml`)
- Remote git pour push/PR : `origin`

**⚠️ Règle URLs** : ne JAMAIS naviguer en dehors de `localhost:$PORT`. Toutes les URLs doivent commencer par `http://localhost:$PORT/`.

**⚠️ Règle Bash** : ne jamais utiliser de commandes qui déclenchent une approbation de sécurité. Concrètement :
- Pas de `$()` (command substitution) — stocker dans une variable via un appel séparé
- Pas de `;` ou `&&` pour chaîner — faire des appels Bash séparés
- Pas de pipes complexes (`cmd1 | cmd2`) — découper en étapes
- 1 commande simple = 1 appel Bash
- **Repo cible** : ne JAMAIS utiliser `git -C` — le working directory est déjà le repo cible, exécuter `git mv`, `git add`, `git commit`, etc. directement.
- **Remplacement du HAML** : utiliser `git mv fichier.html.haml fichier.html.erb` pour renommer, puis écraser le contenu avec l'ERB généré. Un seul commit propre, pas de suppression séparée.
- **Rebase** : pour les rebase interactifs : `git rebase --continue`.
- **Permission refusée** : si une commande est refusée, ne JAMAIS réessayer la même commande. Ne PAS chercher d'alternative — abandonner immédiatement.
- **INTERDIT** : `kill`, `pkill`, `lsof`, `bin/dev`, `overmind`, `env` — ne JAMAIS tenter de lancer, tuer ou diagnostiquer des processus. Le serveur et Playwright sont gérés par le harness nightshift.

**⚠️ Règle screenshots** : **TOUJOURS** déléguer les captures Playwright à l'agent `visual-verify`. Ne JAMAIS appeler les outils `mcp__playwright__*` directement — ils polluent le contexte avec du base64. Utiliser :
```
Agent(subagent_type: "visual-verify", prompt: "port: <PORT>, urls: ['/path1', '/path2'], selector: 'body', output_dir: 'tmp/<nom>/', prefix: 'haml'")
```
Si l'agent retourne `{"status": "playwright_unavailable"}` → écrire `pr-description.md` en notant "screenshots non disponibles" et terminer **sans commit**.

**⚠️ Règle serveur** : le serveur de dev est déjà lancé par nightshift. Vérifier avec `curl -s -o /dev/null -w '%{http_code}' http://localhost:$PORT/` — si pas de réponse, **ARRÊTER** immédiatement. Ne PAS essayer de lancer le serveur.

---

## Prérequis

**MCP Playwright** doit être enregistré via la CLI (le `.mcp.json` seul n'est PAS détecté par Claude Code) :
```bash
claude mcp add playwright -- npx -y @playwright/mcp@latest
# Le -- est obligatoire pour séparer les args
# Relancer Claude Code après ajout (/exit puis claude)
```

**Routes** : `data/routes-reference.txt` doit exister. Si absent → lancer le skill `rails-routes` pour le générer.

**Serveur de dev** doit tourner dans le repo courant. Vérifier que `.overmind.sock` existe à la racine du repo — sinon le serveur tourne dans un autre workspace et le patch de connexion ne fonctionnera pas.

**Chrome doit être fermé** avant de lancer le skill. Playwright lance Chrome avec son propre profil isolé — si Chrome est déjà ouvert, Playwright échoue silencieusement.

**Adaptations dev temporaires** — git-ignorées, **NE JAMAIS COMMITER** :

Utiliser le skill [`/dev-auto-login`](../dev-auto-login/SKILL.md) qui crée `config/initializers/dev_auto_login.rb` (git-ignoré, rouvre ApplicationController pour l'auto-login + invalidation cache ViewComponent).

⚠️ **CRITIQUE** : ce fichier doit être ignoré via **`.git/info/exclude`** (ignore local), jamais via le `.gitignore` versionné — sinon la ligne `+/config/initializers/dev_auto_login.rb` atterrit dans le commit de migration. `/dev-auto-login` s'en charge. Avant de committer, vérifier que `git status` ne montre pas `.gitignore` modifié.

---

## Règle de commit

**1 commit par fichier migré** : `refactor(haml): migrate NomDuComposant to ERB` — inclut le `.html.erb`, les fichiers i18n et le preview si créé.

Les screenshots ne sont JAMAIS commités dans le repo cible. Ils vivent dans `tmp/<nom-composant>/` et sont uploadés sur un gist GitHub.

---

## Workflow (1 fichier)

**⚠️ OBLIGATION** : le workflow n'est TERMINÉ que quand la PR est créée/mise à jour (Étape 6). Ne JAMAIS s'arrêter avant.

### Étape 0 : Vérifications + lancement Playwright + préparation gist

**1. Identifier le port du serveur** :
```bash
grep '^PORT=' .env.development.local
```
Lire le port depuis `.env.development.local` (source de vérité). Utiliser cette valeur pour **toutes** les URLs : `http://localhost:<PORT>/...`. Si le fichier n'existe pas, utiliser 3000 par défaut.

**2. Vérifier que les routes sont disponibles** :
```bash
stat data/routes-reference.txt
```
Si absent → lancer le skill `/rails-routes` pour le générer. Ce fichier est utilisé à l'étape 2 pour trouver les URLs des pages à capturer.

**3. Appliquer le auto-login si absent** :
```bash
grep auto_sign_in_dev_user config/initializers/dev_auto_login.rb
```
Si absent → appliquer le skill `/dev-auto-login` (crée l'initializer + redémarre le serveur).

**4. Vérifier Playwright** — lancer un test rapide via l'agent visual-verify :
```
Agent(subagent_type: "visual-verify", prompt: "port: $PORT, urls: ['/'], selector: 'body', output_dir: 'tmp/test/', prefix: 'check'")
```
Si retour `playwright_unavailable` → **ARRÊTER** (écrire pr-description.md "screenshots non disponibles" et terminer **sans commit**). Sinon supprimer `tmp/test/`.

Lancer le skill `/screenshot-gist NomDuComposant` pour créer le gist et cloner dans `tmp/<nom-composant>/`. Les screenshots sont stockés à plat dedans (ex: `usage1-component-1.png`).

### Étape 1 : Analyse

**⚠️ CRITIQUE :** Lire le HAML ET le fichier Ruby

1. Lire le fichier HAML
2. **Lire le fichier Ruby** associé (même dossier, `.rb`)
3. Identifier les méthodes utilisées dans le template :
   - Si retourne `Array` → utiliser `.join(' ')` en ERB
   - Si retourne `String` → utiliser directement
   - Si retourne `Hash` → utiliser `tag.attributes(method)` (positionnel, PAS kwargs)
   - **⚠️ Si retourne HTML (helpers) → NE PAS interpoler dans string**
4. Rechercher les tests :
   ```bash
   grep -r "NomDuComposant" spec/
   ```

### Étape 2 : Inventaire des utilisations + screenshots HAML

**1. Trouver TOUTES les utilisations du template** :
```bash
grep -r "NomDuComposant\|render.*nom_du_composant" app/views/ app/components/
```
Lister chaque point d'utilisation avec la page correspondante. Consulter `data/routes-reference.txt` pour trouver les URLs correctes (`localhost:$PORT/...`).

**2. Sélectionner jusqu'à 3 points d'entrée** pour les screenshots :
- **Préférer les pages réelles** = preuve plus forte qu'une page de démo
- Choisir des usages variés (contextes différents, paramètres différents)
- Nommer les screenshots par point d'entrée : `usage1-component-1.png`, `usage2-component-1.png`, etc.

**3. Évaluer la faisabilité de chaque point** (dans cet ordre de préférence) :

   **a. Page réelle disponible** → capturer directement (cas idéal)

   **b. Pas de page réelle mais composant simple** → créer un **preview ViewComponent** :
   - Évaluer la complexité : le composant peut-il se rendre avec des données mockées simples ?
   - Si oui (< 5min de setup) → créer un preview dans `spec/components/previews/` :
     ```ruby
     # frozen_string_literal: true

     # spec/components/previews/nom_du_composant_preview.rb
     class NomDuComposantPreview < ViewComponent::Preview
       def default
         render NomDuComposant.new(param: valeur_simple)
       end
     end
     ```
   - Lancer Rubocop auto-correct sur le fichier preview :
     ```bash
     bundle exec rubocop -A spec/components/previews/nom_du_composant_preview.rb
     ```
   - Visiter `localhost:$PORT/rails/view_components/nom_du_composant/default`
   - Commiter le preview avec le commit de migration (il restera dans le projet — utile pour la suite)

   **c. Composant trop complexe** → skip UNIQUEMENT après avoir tenté au moins 3 approches :
   1. Page réelle (autre route, autre contexte)
   2. Preview ViewComponent avec données mockées
   3. Page de test créée ad hoc
   Si les 3 échouent → skip le screenshot, documenter les 3 tentatives dans la PR

**4. Capturer via visual-verify** (pour chaque point d'entrée sélectionné) :

   ```
   Agent(subagent_type: "visual-verify", prompt: "port: $PORT, urls: ['/path/usage1', '/path/usage2'], selector: '.component-selector', output_dir: 'tmp/<nom-composant>/', prefix: 'haml'")
   ```

   L'agent gère le viewport, la navigation et les captures. Il retourne la liste des fichiers créés.

**5. Noter les utilisations non couvertes** — pour l'Étape 6, on les listera dans la PR.

### Étape 3 : Migration HAML → ERB → commit

#### 3a. Conversion

**Règles de conversion :**

```haml
%div.class-name          →  <div class="class-name">
  = content              →    <%= content %>
                         →  </div>

- if condition           →  <% if condition -%>
  = content              →    <%= content %>
                         →  <% end -%>

%div{ class: my_class }  →  <div class="<%= my_class %>">
                            (⚠️ Si my_class est un Array → .join(' '))

%div{ **options }        →  <div <%= tag.attributes(options) %>>

= expr                   →  <%= expr %>        (échappé des deux côtés)
&= expr                  →  <%= expr %>        (échappé explicite)
!= expr                  →  <%= raw(expr) %>   (⚠️ NON échappé en HAML)
-# commentaire           →  <%# commentaire %>
```

**⚠️ Règles critiques :**

1. **Arrays de classes** : Si la méthode retourne un array, ajouter `.join(' ')`
2. **Pas de balises auto-fermantes** : `<input>` pas `<input />`
3. **Contrôler l'espacement** : Utiliser `<%-` et `-%>` pour supprimer newlines
4. **Guillemets** : Utiliser simples quotes `'` si tests sensibles
5. **String interpolation avec helpers HTML** :
   - ❌ `<%= "#{link_to('text', url)}." %>` (échappe le HTML)
   - ✅ `<%= link_to('text', url) %>.` (sortir le texte de l'interpolation)
6. **Ne JAMAIS introduire de `html_safe` ni de `raw`** : une migration est iso-comportement. Les `html_safe` déjà présents dans le HAML se reportent **à l'identique** — on ne les « corrige » pas dans le commit de migration, même s'ils paraissent suspects. Si un `html_safe` existant porte sur une clé i18n, c'est un candidat au renommage en `_html` : le **signaler dans les points d'attention de la PR** (étape 6), pas le traiter ici.

   Piège associé : Rails n'auto-`html_safe` les clés `_html` qu'à travers le helper de vue `t`/`translate`, **jamais** via `I18n.t`. Un `I18n.t('...._html').html_safe` a donc un `.html_safe` porteur, pas redondant — ne pas le supprimer.
7. **Extraction i18n obligatoire** : tout texte français en dur dans le HAML doit être extrait en clé i18n dans l'ERB. Ne PAS recopier les textes tels quels. **Toujours les deux locales** : chaque clé extraite doit exister en FR et EN. Traduire le texte français en anglais naturel (pas du mot-à-mot).

   **Pour un ViewComponent** (`app/components/`) : sidecars **scindés par locale**, un fichier par locale à côté du `.rb` (convention dominante du repo, ~160 composants). **NE JAMAIS** mettre `fr:` et `en:` dans un seul `<nom>_component.yml` — c'est l'ancienne forme, minoritaire, à ne pas reproduire (cf. skill `/i18n-hardcoded`) :
   ```yaml
   # app/components/export_dropdown/export_dropdown_component.fr.yml
   fr:
     standard: "Standard"
     cancel: "Annuler"
   ```
   ```yaml
   # app/components/export_dropdown/export_dropdown_component.en.yml
   en:
     standard: "Standard"
     cancel: "Cancel"
   ```
   ```erb
   <%= t(".standard") %>
   <%= t(".cancel") %>
   ```

   **Pour une vue classique** (`app/views/`) : utiliser le namespace Rails standard correspondant au chemin du fichier. Créer les fichiers FR **et** EN :
   ```yaml
   # config/locales/views/dossiers/show.fr.yml
   fr:
     dossiers:
       show:
         submit_button: "Envoyer le dossier"
   ```
   ```yaml
   # config/locales/views/dossiers/show.en.yml
   en:
     dossiers:
       show:
         submit_button: "Submit the file"
   ```
   ```erb
   <%= t(".submit_button") %>
   ```


#### 3b. Validation locale

**⚠️ OBLIGATOIRE - Ne JAMAIS skip cette étape**

1. **Formatter herb** (ne JAMAIS utiliser `bun lint:herb`, uniquement `format:herb`) :
   ```bash
   bun format:herb -- <fichier.html.erb>
   ```

2. **Tests locaux (si identifiés)** :
   ```bash
   bundle exec rspec spec/path/to/test_spec.rb
   ```
   **⚠️ CRITIQUE :** Le linter détecte la syntaxe, PAS la logique métier (SafeBuffer, helpers)

3. **Vérifier patterns à risque** (1 grep par appel Bash) :
   - `grep '/>' <fichier.html.erb>` → doit être vide (pas de balises auto-fermantes)
   - `grep 'link_to' <fichier.html.erb>` → vérifier qu'aucun n'est dans une interpolation `"#{}"`
   - `grep 'button_to' <fichier.html.erb>` → idem
   - `grep -c 'html_safe\|raw(' <fichier.html.haml>` puis `<fichier.html.erb>` → **les deux comptes doivent être identiques** (aucun ajout, aucune suppression)

4. **Linter apostrophes typographiques** :
   ```bash
   bundle exec rake lint:apostrophe:fix
   ```

5. **Check i18n** : relire le fichier ERB et vérifier qu'aucun texte français n'est resté en dur (cf. règle 7 étape 3a)

6. **Brakeman après rename** — piège récurrent, ne PAS le sauter :
   ```bash
   grep '<chemin>.html.haml' config/brakeman.ignore
   ```
   Si le fichier y figure, le rename casse l'entrée : Brakeman hashe le **chemin** dans son fingerprint, donc l'entrée devient obsolète **et** le même warning ressurgit non-ignoré sur le chemin `.erb`.
   ```bash
   bundle exec brakeman -q --no-pager    # montre les deux symptômes ensemble
   bundle exec brakeman -f json          # fournit le nouveau fingerprint
   ```
   Mettre à jour dans `config/brakeman.ignore` : `fingerprint`, `file`, `line` et `render_path[*].rendered.file`. **Conserver la `note` telle quelle** (`config/brakeman.yml` impose `:ensure_ignore_notes`).

   ⚠️ Ce n'est **pas** une régression de sécurité : le périmètre est inchangé, seul le chemin a bougé. Ne pas rédiger la PR comme si un nouveau risque était apparu — mais le mentionner dans les points d'attention (étape 6).

#### 3c. Remplacement HAML → ERB + commit

1. **Renommer le fichier via `git mv`** (préserve l'historique git) :
   ```bash
   git mv <fichier.html.haml> <fichier.html.erb>
   ```
   Puis écrire le contenu ERB dans le fichier renommé.
   ⚠️ **Ne PAS faire de `rm` sur l'ancien fichier** — `git mv` s'en charge déjà.

2. **Si ViewComponent** — forcer le reload du cache :
   ```bash
   touch <fichier.rb>
   ```
   (Uniquement pour les composants ViewComponent, pas pour les vues classiques)

3. **Commit** (inclure les fichiers i18n FR + EN si créés) :
   ```bash
   git add <fichier.html.erb>
   git add <fichiers_i18n_fr_et_en>
   git commit -m "refactor(haml): migrate NomDuComposant to ERB"
   ```

### Étape 4 : Screenshot ERB (local uniquement — PAS de commit)

Capturer les mêmes pages que l'étape 2 via visual-verify avec le prefix `erb` :
```
Agent(subagent_type: "visual-verify", prompt: "port: $PORT, urls: ['/path/usage1', '/path/usage2'], selector: '.component-selector', output_dir: 'tmp/<nom-composant>/', prefix: 'erb'")
```

### Étape 5 : Comparaison

1. **Comparer les screenshots** (identique au byte = preuve forte) :
   - Pour chaque fichier `erb-*.png` dans `tmp/<nom-composant>/`, comparer sa taille avec le fichier `haml-*.png` correspondant
   - Utiliser `stat -f%z` sur chaque fichier (1 appel Bash par fichier)
   - Identique au byte = ✅, différence = ❌

2. **Si tous les screenshots sont ✅** → passer directement à l'étape 6

3. **Si un ou plusieurs screenshots sont ❌** :
   - **Comparer visuellement** : ouvrir les images HAML et ERB côte à côte (utiliser `Read` sur les PNG)
   - **Identifier la différence** : positionnement, espacement, contenu manquant, attributs perdus, etc.
   - **Diagnostiquer la cause** :
     - Différence de rendu PNG non significative (artefact < 0.1%) → documenter et continuer
     - Problème de conversion ERB (classe manquante, attribut perdu, helper mal converti) → **fixer**
   - **Si fix nécessaire** :
     1. Corriger le fichier `.html.erb`
     2. Valider (linter + tests)
     3. `touch` le `.rb` du composant
     4. Reprendre les screenshots ERB (dans `tmp/<nom-composant>/erb-*.png`)
     5. Commit le fix :
        ```bash
        git add <fichier.html.erb>
        git commit -m "fix(haml): fix conversion NomDuComposant — <description du problème>"
        ```
     6. Relancer la comparaison (retour au point 1)

### Étape 6 : Push gist + écrire pr-description.md

**⚠️ Ne PAS push la branche ni créer la PR — c'est le runner nightshift qui s'en charge.**

1. **Construire le résultat de comparaison** : reprendre les résultats de l'étape 5 (✅/❌ par fichier)

2. **Pousser les screenshots sur le gist** : lancer la Phase 3+4 du skill `/screenshot-gist` via `push-gist.sh` (add, commit, push depuis `tmp/<nom-composant>/`).

3. **Écrire `pr-description.md`** à la racine du worktree :

   Pour construire les URLs des images du gist :
   - Récupérer le gist ID depuis l'URL (dernière partie du path)
   - Format des URLs raw : `https://gist.githubusercontent.com/<user>/<gist-id>/raw/<filename>` (ex: `haml-component-1.png`)

   **Template :**
   ```markdown
   ---
   title: "Tech: migrer <NomDuComposant> de HAML vers ERB"
   ---

   # Probleme

   On migre HAML → ERB. C'est lent, pénible, et c'est une charge mentale.

   # Solution

   Skill [`/haml-migration`](https://github.com/mfo/night-shift/blob/main/.claude/skills/haml-migration/SKILL.md)

   <!-- Répéter ce bloc pour chaque composant migré.
        Résultat selon la comparaison réelle :
        ✅ identique au byte — fichiers PNG strictement identiques (stat -f%z)
        🟡 diff marginale — différence < quelques pixels, non significative (expliquer)
        🟠 diff explicable — différence visible mais attendue (expliquer pourquoi)
        ❌ régression — différence non expliquée, à investiguer -->

   ### NomDuComposant — RÉSULTAT + explication si non ✅

   **Validation :** formatter herb ✅, tests ✅, apostrophes ✅

   <!-- Section à inclure UNIQUEMENT si le fichier contient un html_safe/raw repris du HAML,
        ou si config/brakeman.ignore a dû être mis à jour. Sinon, la supprimer. -->
   **Points d'attention :**
   - `html_safe` ligne N — **repris tel quel du HAML**, non introduit par la migration. Sûr parce que <source du contenu + renderer utilisé>.
   - `config/brakeman.ignore` : fingerprint recalculé suite au rename (Brakeman hashe le chemin). Warning et périmètre de sécurité inchangés.

   **Avant :**
   ![haml](https://gist.githubusercontent.com/<user>/<gist-id>/raw/haml-usage1-component-1.png)

   **Après :**
   ![erb](https://gist.githubusercontent.com/<user>/<gist-id>/raw/erb-usage1-component-1.png)

   **Couverture visuelle (X/Y utilisations) :**
   - ✅ `localhost:$PORT/path/page1` — usage dans contexte A
   - ✅ `localhost:$PORT/path/page2` — usage dans contexte B
   - ⏭️ `localhost:$PORT/path/page3` — raison du skip

   [Voir tous les screenshots](https://gist.github.com/<user>/<gist-id>)

   Generated with [Claude Code](https://claude.com/claude-code)
   ```

4. **Fermer Playwright** : déléguer à visual-verify :
   ```
   Agent(subagent_type: "visual-verify", prompt: "close the browser")
   ```

---

## Checklist

- [ ] Serveur vérifié (.overmind.sock présent)
- [ ] Routes disponibles (`data/routes-reference.txt`, sinon `/rails-routes`)
- [ ] Auto-login dev en place (`/dev-auto-login`)
- [ ] Playwright lancé + navigation localhost:$PORT OK
- [ ] Viewport configuré (browser_resize 1280×800)
- [ ] Gist créé via `/screenshot-gist` dans `tmp/<nom-composant>/`
- [ ] Fichier HAML + fichier Ruby lus (vérifier types de retour)
- [ ] Screenshot HAML capturé dans `tmp/<nom-composant>/haml-*.png`
- [ ] Conversion complète (arrays `.join`, pas de `/>`, espacement, pas d'interpolation helpers)
- [ ] Textes français extraits en i18n (pas de texte en dur dans l'ERB) avec traductions EN
- [ ] Aucun `html_safe`/`raw` introduit (`grep -c` identique entre le HAML et l'ERB)
- [ ] Formatter herb passé
- [ ] Linter apostrophes passé
- [ ] Tests passés (si identifiés)
- [ ] `bundle exec brakeman` : 0 warning et aucune entrée obsolète (si le fichier était dans `config/brakeman.ignore`, fingerprint + chemins mis à jour, note conservée)
- [ ] Points d'attention documentés dans `pr-description.md` si `html_safe`/`raw` repris ou `brakeman.ignore` touché
- [ ] `git mv` HAML → ERB + `touch` du `.rb` + fichiers i18n → commit migration
- [ ] Screenshot ERB capturé dans `tmp/<nom-composant>/erb-*.png`
- [ ] Comparaison : tous ✅ ou différences investiguées et fixées
- [ ] Screenshots pushés sur le gist (via `/screenshot-gist` Phase 2)
- [ ] `pr-description.md` écrit à la racine du worktree
- [ ] Playwright fermé
