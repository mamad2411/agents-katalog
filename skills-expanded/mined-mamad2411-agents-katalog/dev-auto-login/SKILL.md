---
name: dev-auto-login
description: "Setup dev auto-login and ViewComponent reload. Use for localhost authentication setup."
allowed-tools: Bash(grep:*), Bash(touch:*), Bash(git check-ignore:*), Bash(git rev-parse:*), Bash(echo:*), Edit(config/*), Write(config/*)
---

# Auto-login dev

**Contexte :** Certains skills ont besoin de naviguer sur le serveur de dev local en étant authentifié (screenshots, tests visuels, démo). Plutôt que de patcher `ApplicationController` et risquer de commiter le patch, on utilise un initializer séparé qui rouvre la classe — git-ignoré.

**Fichier :** `config/initializers/dev_auto_login.rb`

## Setup

**1. Vérifier que le fichier est ignoré** dans le repo cible, AVANT de le créer :
```bash
git check-ignore -v config/initializers/dev_auto_login.rb
```
Si la commande ne retourne rien, ajouter l'entrée à **`.git/info/exclude`** — ignore local, jamais versionné, partagé par tous les worktrees du dépôt :
```bash
echo 'config/initializers/dev_auto_login.rb' >> "$(git rev-parse --git-common-dir)/info/exclude"
```

⚠️ **Ne JAMAIS toucher au `.gitignore` versionné pour ça.** Cette ligne se retrouve dans le commit de la feature et pollue la PR (constaté sur #13964 : un commit i18n embarquait `+/config/initializers/dev_auto_login.rb`). Si l'entrée a déjà été ajoutée au `.gitignore` par une exécution précédente, la retirer avant de committer.

**2. Vérifier si le fichier existe déjà :**
```bash
grep -l auto_sign_in_dev_user config/initializers/dev_auto_login.rb
```

**3. Si absent → le créer :**

```ruby
# config/initializers/dev_auto_login.rb
# ⚠️ Git-ignoré — auto-login dev + reload ViewComponent
# Rouvre ApplicationController pour ajouter le auto-login sans modifier le fichier original.
return unless Rails.env.development?

# ⚠️ NE PAS référencer ApplicationController dans un `to_prepare` : ce hook s'exécute AVANT
# le chargement des routes (finisher `run_prepare_callbacks` < `set_routes_reloader_hook`),
# donc avant que `devise_for :users` n'ait défini les helpers `current_user` /
# `user_signed_in?`. Forcer l'autoload de ApplicationController à ce moment-là fait planter
# le boot sur toute ligne qui suppose Devise chargé (ex : `alias_method :pundit_user, :current_user`).
# Le callback Zeitwerk ci-dessous s'accroche à l'autoload réel de la classe (premier usage,
# et à chaque reload) : les routes sont alors dessinées.
Rails.autoloaders.main.on_load("ApplicationController") do |klass, _abspath|
  klass.class_eval do
    prepend_before_action :auto_sign_in_dev_user

    def auto_sign_in_dev_user
      return if user_signed_in?
      raise "[dev_auto_login] ENV['DEV_EMAIL'] non définie — auto-login désactivé" if ENV['DEV_EMAIL'].blank?
      user = User.find_by(email: ENV['DEV_EMAIL'])
      raise "[dev_auto_login] aucun User avec l'email #{ENV['DEV_EMAIL']}" if user.nil?
      sign_in(user, scope: :user)
      current_user.instructeur&.update(bypass_email_login_token: true)
    end
  end
end

# Invalidation cache ViewComponent — permet de switcher .haml → .erb sans redémarrer le serveur
Rails.application.config.to_prepare do
  ViewComponent::CompileCache.invalidate!

  ObjectSpace.each_object(Class).select { |klass| klass < ViewComponent::Base }.each do |klass|
    if klass.instance_variable_defined?(:@__vc_compiler)
      compiler = klass.instance_variable_get(:@__vc_compiler)
      compiler.instance_variable_set(:@templates, nil) if compiler.instance_variable_defined?(:@templates)
    end
  end
end
```

**Points de vigilance :**
- Le `on_load` Zeitwerk doit être enregistré **au top-level** de l'initializer, jamais dans un `to_prepare` (sinon un callback en double est enregistré à chaque reload).
- Ne pas redéfinir `pundit_user` : `ApplicationController` l'alias déjà sur `current_user`. Si le repo cible ne le fait pas, ajouter `alias_method :pundit_user, :current_user` **dans le bloc `class_eval` ci-dessus**, pas ailleurs.

**4. Redémarrer le serveur** pour charger l'initializer :
```bash
touch tmp/restart.txt
```

**5. Vérifier que le boot passe** (l'erreur type est un `NameError` sur `current_user` au boot) :
```bash
bin/rails runner 'puts ApplicationController.name'
```

## Désactivation

Supprimer ou renommer le fichier. Rien d'autre à faire — `ApplicationController` n'a jamais été modifié.
