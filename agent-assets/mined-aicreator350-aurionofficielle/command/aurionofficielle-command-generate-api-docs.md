# Generate API Documentation

Génère la documentation API automatiquement depuis le code.

## Instructions

1. **Scan des endpoints**
   - Lis tous les fichiers dans api/*.ts
   - Lis tous les handlers dans api/_handlers/
   - Identifie METHOD + PATH + AUTH + PARAMS + RESPONSE

2. **Format de documentation**
   Pour chaque endpoint :
   ```markdown
   ### METHOD /api/endpoint
   **Auth**: Required/Public
   **Headers**: X-CSRF-Token (si POST auth'd)
   **Body**: { param: type, ... }
   **Response**: { data: type } | { error: string }
   **Rate Limit**: X req/min
   **Credits**: X crédits par appel
   ```

3. **Catégorisation**
   - Auth endpoints (/api/auth/*, /api/tool-token)
   - AI endpoints (/api/ai-proxy, /api/deep-research)
   - Payment endpoints (/api/payments/*, /api/stripe-webhook)
   - Account endpoints (/api/account/*)
   - Tool-specific endpoints
   - Infrastructure (/api/health, /api/infra/*)

4. **Mise à jour de docs/API.md**
   - Préserve le contenu existant
   - Ajoute les nouveaux endpoints
   - Met à jour les descriptions modifiées
   - Ajoute des exemples curl

5. **Validation**
   - Vérifie que chaque endpoint documenté existe dans le code
   - Vérifie que chaque endpoint dans le code est documenté
