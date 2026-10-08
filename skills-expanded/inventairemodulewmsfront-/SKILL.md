# 🏗️ Règles Cursor - Inventaire WMS Front

## 📋 Contexte du Projet
- **Application** : Système de gestion d'inventaire WMS (Warehouse Management System)
- **Stack** : Vue 3 + TypeScript + Vite + Pinia + Tailwind CSS
- **Architecture** : Composition API avec `<script setup>`, séparation en couches
- **Langue** : Interface et code en français

## 🎯 Conventions de Code

### 📁 Structure des Fichiers
- **Views** : `src/views/` - Pages principales (PascalCase)
- **Composants** : `src/components/` - Composants réutilisables
- **Composables** : `src/composables/` - Logique métier (`use*.ts`)
- **Services** : `src/services/` - Couche service métier
- **Stores** : `src/stores/` - État global Pinia
- **Types** : `src/models/` ou `src/types/` - Interfaces TypeScript

### 🔧 TypeScript
- Toujours utiliser TypeScript strict
- Définir des interfaces pour tous les objets métier
- Préférer `interface` à `type` pour les objets
- Utiliser `const assertions` pour les tableaux et objets readonly
- Types obligatoires pour les props, emits, et retours de fonctions

### 🖥️ Vue 3 Composition API
- **TOUJOURS** utiliser `<script setup lang="ts">`
- Préférer `ref()` pour les primitives, `reactive()` pour les objets
- Utiliser `computed()` pour les valeurs dérivées
- Déstructurer les stores Pinia avec `storeToRefs()`
- Organiser les imports : Vue, composables, services, types

```vue
<script setup lang="ts">
// 1. Imports Vue
import { ref, computed, onMounted } from 'vue'
// 2. Imports composables
import { useAuthStore } from '@/stores/auth'
// 3. Imports services
import { UserService } from '@/services/UserService'
// 4. Imports types
import type { User } from '@/models/User'

// Props et emits en premier
interface Props {
  userId: number
}
const props = defineProps<Props>()

// État réactif
const user = ref<User | null>(null)
const loading = ref(false)

// Computed
const displayName = computed(() => user.value?.name || 'Utilisateur inconnu')

// Méthodes
const loadUser = async () => {
  // logique...
}

// Lifecycle
onMounted(() => {
  loadUser()
})
</script>
```

### 🧩 Composables
- Nommer avec le préfixe `use` (ex: `usePlanning`, `useJobManagement`)
- Une responsabilité par composable
- Retourner un objet avec propriétés nommées
- Gérer les erreurs avec `ErrorHandlerService`

```typescript
export const useJobManagement = (deps?: JobManagementDependencies) => {
  const jobs = ref<Job[]>([])
  const loading = ref(false)

  const loadJobs = async () => {
    try {
      loading.value = true
      const result = await JobService.getJobs()
      jobs.value = result
    } catch (error) {
      await ErrorHandlerService.handleError(error, 'chargement des jobs')
    } finally {
      loading.value = false
    }
  }

  return {
    // État
    jobs: readonly(jobs),
    loading: readonly(loading),
    // Actions
    loadJobs,
    // Computed si nécessaire
    jobsCount: computed(() => jobs.value.length)
  }
}
```

### 🏪 Stores Pinia
- Un store par domaine métier (inventory, job, location, etc.)
- Utiliser `defineStore` avec syntaxe setup
- Actions asynchrones avec gestion d'erreurs
- État réactif avec `ref()` et `computed()`

```typescript
export const useJobStore = defineStore('job', () => {
  const jobs = ref<Job[]>([])
  const loading = ref(false)

  const getJobs = computed(() => jobs.value)

  const fetchJobs = async () => {
    try {
      loading.value = true
      const response = await JobService.getAll()
      jobs.value = response.data
    } catch (error) {
      throw error // Laisser le composable gérer l'erreur
    } finally {
      loading.value = false
    }
  }

  return { jobs, loading, getJobs, fetchJobs }
})
```

### 🎨 Styles et Design
- **Couleurs** : Utiliser les variables CSS personnalisées
  - Primaire : `#FECD1C` (jaune)
  - Secondaire : `#B4B6BA` (gris)
- **Classes Tailwind** : Privilégier les utilitaires
- **Responsive** : Mobile-first avec breakpoints Tailwind
- **Dark mode** : Supporter avec `dark:` prefix

### 🛠️ DataTable et Composants
- Utiliser le composant `DataTable` personnalisé pour les tableaux
- Props obligatoires : `columns`, `rowDataProp`
- Activer les fonctionnalités : `enableFiltering`, `enableGlobalSearch`, `pagination`
- Badges pour les statuts avec `rendererType: 'badge'`

```vue
<DataTable
  :columns="jobsColumns"
  :rowDataProp="jobs"
  :enableFiltering="true"
  :enableGlobalSearch="true"
  :pagination="true"
  :rowSelection="true"
  @selection-changed="onSelectionChanged"
  @filter-changed="onFilterChanged"
/>
```

### 🔄 Gestion d'Erreurs
- Utiliser `ErrorHandlerService.handleError()` pour toutes les erreurs
- Ne pas faire de double gestion d'erreurs (store + composable)
- Messages d'erreur en français, contextuels

```typescript
try {
  await jobStore.deleteJob(id)
} catch (error) {
  await ErrorHandlerService.handleError(error, 'suppression du job')
  // L'erreur est déjà affichée, pas besoin d'autre action
}
```

### 📡 Services API
- Un service par domaine (JobService, InventoryService, etc.)
- Méthodes async/await
- Typage des réponses API
- Gestion des erreurs HTTP

```typescript
export class JobService {
  static async getAll(): Promise<ApiResponse<Job[]>> {
    const response = await api.get('/jobs')
    return response.data
  }

  static async delete(ids: number[]): Promise<DeleteJobResponse> {
    const response = await api.delete('/jobs', { data: { ids } })
    return response.data
  }
}
```

### 🌐 Routing
- Routes groupées par module dans `src/router/`
- Lazy loading pour les pages
- Guards d'authentification si nécessaire

### 📝 Nommage
- **Variables** : camelCase français (`nombreEmplacements`)
- **Fonctions** : verbes d'action (`chargerJobs`, `validerInventaire`)
- **Composants** : PascalCase (`JobManagement.vue`)
- **Types/Interfaces** : PascalCase (`interface Job`)
- **Constantes** : SCREAMING_SNAKE_CASE (`MAX_ITEMS_PER_PAGE`)

### 🚫 À Éviter
- Ne pas utiliser `any` - toujours typer
- Éviter les `console.log` en production
- Ne pas mélanger français/anglais dans les noms
- Éviter les composants monolithiques (> 300 lignes)
- Ne pas faire de mutations directes des props

### ✅ Bonnes Pratiques
- Extraire la logique complexe dans des composables
- Utiliser les slots pour la personnalisation des composants
- Préférer la composition à l'héritage
- Tester les cas d'erreur
- Documenter les interfaces publiques
- Utiliser `readonly()` pour exposer l'état des composables

### 🔧 Outils de Développement
- **Bundler** : Vite avec HMR
- **Linter** : Configuration TypeScript stricte
- **Build** : `npm run build` (inclut type checking)
- **Dev** : `npm run dev` (port 3000)

### 📦 Imports Spéciaux
- `@/` : Alias pour `src/`
- `@/components/` : Composants
- `@/composables/` : Composables
- `@/services/` : Services
- `@/types/` : Types TypeScript

Cette configuration garantit un code maintenable, performant et conforme aux standards Vue 3 + TypeScript.
