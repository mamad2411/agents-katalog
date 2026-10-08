# Configuration des environnements - Règles Cursor

## Accès à la configuration

Toujours utiliser le module centralisé pour accéder aux variables d'environnement:

```typescript
// ✅ BON - Utiliser le module de configuration
import { config, isProduction, isDevelopment } from '@/config/env';

const stripeKey = config.stripe.secretKey;
const dbUrl = config.database.url;

if (isProduction) {
  // Code spécifique production
}

// ✅ BON - Accès direct pour les variables publiques côté client
const appUrl = process.env.NEXT_PUBLIC_APP_URL;

// ❌ MAUVAIS - Accès direct aux variables privées
const stripeKey = process.env.STRIPE_SECRET_KEY;
```

## Validation des variables

Avant tout déploiement, toujours valider:

```bash
npm run env:validate
```

## Sécurité

- Ne JAMAIS committer les fichiers `.env*`
- Utiliser `env.template` pour documenter les nouvelles variables
- Préfixer les variables publiques avec `NEXT_PUBLIC_`
- Générer des secrets forts avec `npm run env:secret`

## Documentation

- Configuration complète: `ENVIRONMENT.md`
- Guide rapide: `QUICK_START_ENV.md`
- Template: `env.template`
