---
name: dependency-updates
description: "Use when user asks about updating outdated Drupal packages, upgrading Drupal core minor or patch versions, updating contrib modules, or resolving composer version conflicts."
license: Proprietary
compatibility: composer>=2.x
metadata:
    category: maintenance
    author: Acquia
    version: "1.0.0"
    tags: "drupal, composer, updates, outdated, core, contrib"
    software_requirements: "composer>=2.x"
---

# Dependency Updates for Drupal with Composer

Use when:
- Checking which packages are outdated
- Updating Drupal core to a newer minor or patch release
- Updating contrib modules or libraries
- Resolving composer version conflicts after an update

---

## Before You Start — Create a Branch

> **This step is mandatory. Do not run any composer commands until a new branch is created and confirmed.**
> Never update packages directly on `main` or `master`.

Check the current branch first:

```bash
git branch --show-current
```

If the user is on `main`, `master`, or any protected branch, stop and ask: **"What would you like to name the new branch for these updates?"**

Suggest a default if they are unsure (e.g., `deps/drupal-updates-YYYY-MM-DD`).

```bash
git checkout -b <branch-name>
```

Confirm the new branch is active before proceeding:

```bash
git branch --show-current
```

Only continue to the next step once the output confirms a non-protected branch.

---

## Check for Outdated Packages

```bash
composer outdated
```

Shows all packages with newer versions available. Columns: current version → latest available.

### Check only direct dependencies

```bash
composer outdated --direct
```

### Check a specific package

```bash
composer outdated drupal/core-recommended
```

---

## Update a Specific Package

```bash
composer update drupal/package --with-all-dependencies
```

### Update multiple packages at once

```bash
composer update drupal/package1 drupal/package2 --with-all-dependencies
```

---

## Update Drupal Core (Minor or Patch)

Drupal core is split across multiple packages. Update all together:

```bash
composer update drupal/core-recommended drupal/core-composer-scaffold drupal/core-project-message --with-all-dependencies
```

> **Note:** Minor upgrades (e.g., 10.2 → 10.3) may require relaxing the version constraint in `composer.json` first:
>
> ```json
> "drupal/core-recommended": "^10.3"
> ```
>
> Then run the update command above.

### Verify the installed version

```bash
composer show drupal/core | grep versions
```

---

## Update All Packages

Update everything within existing `composer.json` constraints:

```bash
composer update
```

> This updates `composer.lock` but will not change version constraints in `composer.json`. Packages pinned to an older major will not cross that boundary.

---

## Update All Drupal Contrib Modules

```bash
composer update "drupal/*" --with-all-dependencies
```

---

## Resolving Conflicts

### "Your requirements could not be resolved"

Find what is blocking the update:

```bash
# What requires the package you're trying to update?
composer why drupal/package

# What prevents the target version?
composer why-not drupal/package 2.x
```

Adjust the conflicting constraint in `composer.json` and retry.

### Conflict between two contrib modules

```bash
# Check full dependency chain
composer depends drupal/module-a
composer depends drupal/module-b
```

Update both together to let composer find a compatible set:

```bash
composer update drupal/module-a drupal/module-b --with-all-dependencies
```

### Revert a bad update

If `composer update` introduced a regression, restore the previous lock file from version control and reinstall:

```bash
git checkout composer.json composer.lock
composer install
```

If the update was already committed, revert the commit:

```bash
git revert HEAD
composer install
```

---

## Verify the Update

```bash
# Confirm installed versions
composer show drupal/core-recommended
composer show --outdated
```

Run `composer audit` after any update to confirm no new advisories were introduced:

```bash
composer audit
```

### Confirm Drupal still bootstraps

If Drush is available locally:

```bash
drush status
```

Expected: `Drupal bootstrap: Successful`. If bootstrap fails, do not commit — investigate before proceeding.

> **After verification, always ask the user these questions in order:**
>
> **1. "Do you want to commit these changes?"**
> - If yes:
>   ```bash
>   git add composer.json composer.lock
>   git commit -m "Update Drupal dependencies"
>   ```
> - If no → remind the user that `composer.json` and `composer.lock` are uncommitted before proceeding.
>
> **2. "Do you want to deploy these changes to an Acquia environment?"**
> - If yes → follow the **[Drupal Update and Deploy playbook](../../playbooks/drupal-update-deploy/SKILL.md)** to push code, switch the environment, and optionally trigger a pipeline build.
> - If no → done.
>
> **3. After deployment:** Run database updates on the target environment before marking the work complete:
> ```bash
> drush updb --yes
> drush cr
> ```

---

## Troubleshooting

| Problem | Command |
|---------|---------|
| Update ignored — package still old | Check constraint in `composer.json`; relax if needed |
| `composer install` fails after update | Run `composer why-not package version` to find conflict |
| Unexpected packages changed | Review `git diff composer.lock` before committing |
| Memory limit error | `COMPOSER_MEMORY_LIMIT=-1 composer update` |

---

## Related

- **[Security Updates](../security-updates/SKILL.md)** — Fix specific vulnerability advisories
