# Optimize Bundle Size

Réduit la taille des bundles pour un chargement plus rapide.

## Instructions

1. **Analyse actuelle**
   - `npx vite build` → noter les tailles des chunks
   - Identifier les top 5 plus gros chunks
   - `npx vite-bundle-visualizer` si disponible

2. **Stratégies de réduction**
   - **Tree shaking** : imports nommés au lieu de `import *`
   - **Code splitting** : React.lazy() pour les routes
   - **Dynamic imports** : `import()` pour les features lourdes
   - **Externalization** : CDN pour les grosse libs si approprié

3. **Cibles spécifiques Aurion**
   - Framer Motion : importer uniquement `motion` depuis `framer-motion`
   - Lucide React : `import { Icon } from 'lucide-react'` pas `import * as Icons`
   - Three.js (chat) : lazy load du viewer 3D
   - Monaco Editor (IDE, 1code) : dynamic import avec loading state
   - Fabric.js (ai-marketing) : import dynamique

4. **Images & Assets**
   - Convertir PNG/JPG → WebP
   - Sprites SVG pour les icônes récurrentes
   - Fonts : subset des caractères utilisés

5. **Validation**
   - `npx vite build` → comparer avant/après
   - Objectif : -20% minimum sur le bundle principal
