## Development

When starting the dev server, use background mode:

```
astro dev --background
```

Manage the background server with `astro dev stop`, `astro dev status`, and `astro dev logs`.

## Project structure

- `src/data/pierres/*.yml` — source de vérité des pierres
- `public/images/pierres/{id}/` — photos des pierres
- `src/lib/pierres.ts` — loader YML vers TypeScript
- `src/lib/auth.ts` — hash et vérification du mot de passe
- `src/lib/github.ts` — Octokit pour commit YML + images
- `src/middleware.ts` — HTTP Basic Auth : protège `/edit/*` et `/api/pierres`

## Environnement

Copier `.env.example` vers `.env` et remplir :

```
# Générer un hash : bun -e "import('./src/lib/auth.ts').then(m=>console.log(m.hashPassword('m-dp')))"
EDIT_PASSWORD_HASH=salt:hash
GITHUB_TOKEN=ghp_...
GITHUB_REPO=xHemera/gem
```

Le username est ignoré — seul le mot de passe compte. La boîte de dialogue du navigateur s'affiche automatiquement.

## Documentation

Full documentation: https://docs.astro.build

Consult these guides before working on related tasks:

- [Adding pages, dynamic routes, or middleware](https://docs.astro.build/en/guides/routing/)
- [Working with Astro components](https://docs.astro.build/en/basics/astro-components/)
- [Using React, Vue, Svelte, or other framework components](https://docs.astro.build/en/guides/framework-components/)
- [Adding or managing content](https://docs.astro.build/en/guides/content-collections/)
- [Adding styles or using Tailwind](https://docs.astro.build/en/guides/styling/)
- [Supporting multiple languages](https://docs.astro.build/en/guides/internationalization/)
