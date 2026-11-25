---
name: rename-product
description: Use when turning this starter into a specific product ("rename this to Fashion Girl", "make it my product"). Renames every app, package, bundle ID, namespace, folder and doc in one step and verifies nothing broke.
---

# Rename the product

`scripts/rename.mjs` renames everything in one pass: display names, the iOS target and bundle IDs, the Android application ID and Kotlin packages (with their folders), the .NET solution, projects and namespaces, web titles, `package.json` names, storage keys, placeholder API domains, Maestro flows, docs, README links and screenshot links. Credits to the starter and the licence are kept, and a **Built with Agentic Product Starter** badge is added under the README title (keep it: it is how others find products built with the starter).

## 1. Agree the names with the user

Ask for, or propose and confirm:

| Input | Example | Rules |
|---|---|---|
| Product name | `Fashion Girl` | Shown to users. Starts with a letter |
| App ID | `com.fashiongirl.app` | Reverse domain the user owns, lowercase, at least three parts. **Cannot change after the apps are in the App Store or Google Play**, so get it right now |
| Repository | `my-org/fashion-girl` | Their GitHub copy. Detected from `git remote` if not given |

The code name (`FashionGirl`) and slugs (`fashion-girl`, `fashiongirl`) are derived automatically.

## 2. Preview, then apply

On a new branch, with a clean working tree:

```bash
git switch -c chore/rename-product
node scripts/rename.mjs --name "Fashion Girl" --id com.fashiongirl.app --dry-run   # review the list
node scripts/rename.mjs --name "Fashion Girl" --id com.fashiongirl.app
```

Show the user the summary line: files changed, files moved, and the derived names.

## 3. Verify

Run every app's checks (they all must pass before committing):

```bash
node design/build.mjs --check
(cd backend && dotnet test)
(cd apps/web-app && npm install && npm run lint && npm run typecheck && npm test)
(cd apps/back-office && npm install && npm run lint && npm run typecheck && npm test)
(cd apps/android && make test-unit)
(cd apps/ios && make generate && make test-unit)      # on a Mac
```

Then confirm nothing was missed (for example a new hard-coded name added to the starter later):

```bash
node scripts/rename.mjs --check
```

## 4. Finish

* Commit as `chore: rename the product to <name>` and open a pull request. The **Rename check** workflow confirms nothing is left.
* Update the product description in the README intro and `docs/product/` with the real product.
* Keep `LICENSE` as it is (the MIT licence requires the starter's notice); add your own copyright line under it if you like.
* Set the real SYST and Prod API URLs later (`apps/ios/Config/*.xcconfig`, `apps/android/app/src/<flavor>/`, web `src/config/env.ts`).
* If not done yet, apply the GitHub settings a template copy misses: `node scripts/setup.mjs repo` (the `setup-integrations` skill).
* Suggest the next steps: `security-audit`, then `grill-me` on the first feature.

## Rules

* Run it once, on the fresh copy of the starter. It renames from the starter's names; after that, change names with normal pull requests.

* Never rename by hand with search and replace across the repo: the word "agentic" is also used for the way of working (agentic SDLC, agentic layer) and must stay.
* If you add a new place that contains the product name to the starter, teach `scripts/rename.mjs` about it in the same pull request, otherwise **Rename check** fails.
