---
name: vuex-module-creator
description: Create Vuex modules for page-level state management following Educacross patterns (dynamic registration, reset mutations, getter/setter pairs). Use when user says "create Vuex module", "state management", "módulo Vuex", "page module", or needs to manage page-specific state.
---

# Vuex Module Creator - Page Modules Pattern

Create production-ready Vuex modules for page-level state management with dynamic registration/unregistration and complete cleanup.

## Core Principles

### 1. Always Namespaced

```javascript
export default {
  namespaced: true,  // REQUIRED - prevents global pollution
  // ...
}
```

**Why:** Prevents naming conflicts between modules and enables module isolation.

### 2. Dynamic Registration

Modules are registered when the page mounts and unregistered when it unmounts:

```javascript
// In Index.vue
import { onUnmounted } from 'vue'
import store from '@/store'
import moduleFeatureName from '@/store/pageModules/{domain}/module-feature-name'

const moduleName = 'FeatureName'

// Register on mount
if (!store.hasModule(moduleName)) {
  store.registerModule(moduleName, moduleFeatureName)
}

// Cleanup on unmount
onUnmounted(() => {
  store.commit(`${moduleName}/reset`)
  store.unregisterModule(moduleName)
})
```

**Why:** Prevents memory leaks and keeps global store clean.

### 3. Reset Mutation (REQUIRED)

Every module MUST have a `reset` mutation:

```javascript
mutations: {
  reset: state => {
    state.data = []
    state.loading = false
    state.totalPages = 0
    // Reset ALL state properties to initial values
  },
}
```

**Why:** Ensures clean state when navigating away and back to the page.

### 4. Getter for Every State Property

```javascript
state: {
  data: [],
  loading: false,
},

getters: {
  data: state => state.data,        // Getter mirrors state
  loading: state => state.loading,
}
```

**Why:** Enables computed get/set pattern in composables for reactive v-model binding.

### 5. Mutations Are Simple Setters

```javascript
mutations: {
  data: (state, payload) => { state.data = payload },
  loading: (state, payload) => { state.loading = payload },
}
```

**Why:** Keeps mutations predictable and traceable in Vue DevTools.

---

## Module Location

```
src/store/pageModules/
├── library/
│   └── module-libray-books.js
├── missions/
│   └── list-missions-module.js
├── reports/
│   └── module-report-access.js
└── {domain}/
    └── module-{feature}.js
```

**Naming Convention:** `module-{feature-name}.js` (kebab-case)

---

## Complete Module Template

### Basic CRUD Module

```javascript
export default {
  namespaced: true,
  
  state: {
    // Data
    data: [],
    item: null,
    
    // Loading states
    loading: false,
    saving: false,
    
    // Pagination
    totalPages: 0,
    totalItems: 0,
    perPage: 10,
    currentPage: 1,
    
    // Sorting
    sortBy: '',
    isSortDirDesc: false,
    
    // Filtering
    searchQuery: '',
    filters: {},
    
    // UI State
    showModal: false,
    selectedId: null,
  },
  
  getters: {
    // Data getters
    data: state => state.data,
    item: state => state.item,
    
    // Loading getters
    loading: state => state.loading,
    saving: state => state.saving,
    
    // Pagination getters
    totalPages: state => state.totalPages,
    totalItems: state => state.totalItems,
    perPage: state => state.perPage,
    currentPage: state => state.currentPage,
    
    // Sorting getters
    sortBy: state => state.sortBy,
    isSortDirDesc: state => state.isSortDirDesc,
    
    // Filtering getters
    searchQuery: state => state.searchQuery,
    filters: state => state.filters,
    
    // UI getters
    showModal: state => state.showModal,
    selectedId: state => state.selectedId,
    
    // Computed getters
    hasData: state => state.data.length > 0,
    selectedItem: state => state.data.find(item => item.id === state.selectedId),
  },
  
  mutations: {
    // Data mutations
    data: (state, payload) => { state.data = payload },
    item: (state, payload) => { state.item = payload },
    
    // Loading mutations
    loading: (state, payload) => { state.loading = payload },
    saving: (state, payload) => { state.saving = payload },
    
    // Pagination mutations
    totalPages: (state, payload) => { state.totalPages = payload },
    totalItems: (state, payload) => { state.totalItems = payload },
    perPage: (state, payload) => { state.perPage = payload },
    currentPage: (state, payload) => { state.currentPage = payload },
    
    // Sorting mutations
    sortBy: (state, payload) => { state.sortBy = payload },
    isSortDirDesc: (state, payload) => { state.isSortDirDesc = payload },
    
    // Filtering mutations
    searchQuery: (state, payload) => { state.searchQuery = payload },
    filters: (state, payload) => { state.filters = payload },
    
    // UI mutations
    showModal: (state, payload) => { state.showModal = payload },
    selectedId: (state, payload) => { state.selectedId = payload },
    
    // Array operations
    addItem: (state, item) => {
      state.data.push(item)
      state.totalItems += 1
    },
    
    updateItem: (state, updatedItem) => {
      const index = state.data.findIndex(item => item.id === updatedItem.id)
      if (index !== -1) {
        state.data.splice(index, 1, updatedItem)
      }
    },
    
    removeItem: (state, itemId) => {
      state.data = state.data.filter(item => item.id !== itemId)
      state.totalItems -= 1
    },
    
    // REQUIRED: Reset mutation
    reset: state => {
      state.data = []
      state.item = null
      state.loading = false
      state.saving = false
      state.totalPages = 0
      state.totalItems = 0
      state.perPage = 10
      state.currentPage = 1
      state.sortBy = ''
      state.isSortDirDesc = false
      state.searchQuery = ''
      state.filters = {}
      state.showModal = false
      state.selectedId = null
    },
  },
  
  actions: {
    // Example action for API calls
    async fetchData({ commit, state }) {
      commit('loading', true)
      try {
        const response = await api.getData({
          Page: state.currentPage,
          PageSize: state.perPage,
          OrderBy: state.sortBy,
          IsDesc: state.isSortDirDesc,
          SearchQuery: state.searchQuery,
        })
        
        commit('data', response.data.items)
        commit('totalPages', response.data.totalPages)
        commit('totalItems', response.data.totalItems)
      } catch (error) {
        console.error('Error fetching data:', error)
        commit('data', [])
      } finally {
        commit('loading', false)
      }
    },
    
    async saveItem({ commit }, item) {
      commit('saving', true)
      try {
        if (item.id) {
          // Update existing
          await api.update(item.id, item)
          commit('updateItem', item)
        } else {
          // Create new
          const response = await api.create(item)
          commit('addItem', response.data)
        }
        return true
      } catch (error) {
        console.error('Error saving item:', error)
        return false
      } finally {
        commit('saving', false)
      }
    },
    
    async deleteItem({ commit }, itemId) {
      try {
        await api.delete(itemId)
        commit('removeItem', itemId)
        return true
      } catch (error) {
        console.error('Error deleting item:', error)
        return false
      }
    },
  },
}
```

---

## Module Patterns

### List/Table Module (Simple)

For basic list pages with pagination:

```javascript
export default {
  namespaced: true,
  
  state: {
    data: [],
    loading: false,
    totalPages: 0,
    totalItems: 0,
    perPage: 10,
    currentPage: 1,
    sortBy: '',
    isSortDirDesc: false,
  },
  
  getters: {
    data: state => state.data,
    loading: state => state.loading,
    totalPages: state => state.totalPages,
    totalItems: state => state.totalItems,
    perPage: state => state.perPage,
    currentPage: state => state.currentPage,
    sortBy: state => state.sortBy,
    isSortDirDesc: state => state.isSortDirDesc,
  },
  
  mutations: {
    data: (state, payload) => { state.data = payload },
    loading: (state, payload) => { state.loading = payload },
    totalPages: (state, payload) => { state.totalPages = payload },
    totalItems: (state, payload) => { state.totalItems = payload },
    perPage: (state, payload) => { state.perPage = payload },
    currentPage: (state, payload) => { state.currentPage = payload },
    sortBy: (state, payload) => { state.sortBy = payload },
    isSortDirDesc: (state, payload) => { state.isSortDirDesc = payload },
    
    reset: state => {
      state.data = []
      state.loading = false
      state.totalPages = 0
      state.totalItems = 0
      state.perPage = 10
      state.currentPage = 1
      state.sortBy = ''
      state.isSortDirDesc = false
    },
  },
}
```

---

### Filter Module (with useFilters integration)

For pages with subject/class filters:

```javascript
export default {
  namespaced: true,
  
  state: {
    data: [],
    loading: false,
    
    // Pagination
    totalPages: 0,
    totalItems: 0,
    perPage: 10,
    currentPage: 1,
    
    // Filters (in addition to useFilters subject/class)
    searchQuery: '',
    statusFilter: null,
    dateFrom: null,
    dateTo: null,
  },
  
  getters: {
    data: state => state.data,
    loading: state => state.loading,
    totalPages: state => state.totalPages,
    totalItems: state => state.totalItems,
    perPage: state => state.perPage,
    currentPage: state => state.currentPage,
    searchQuery: state => state.searchQuery,
    statusFilter: state => state.statusFilter,
    dateFrom: state => state.dateFrom,
    dateTo: state => state.dateTo,
    
    // Computed: Active filter count
    activeFiltersCount: state => {
      let count = 0
      if (state.searchQuery) count++
      if (state.statusFilter) count++
      if (state.dateFrom) count++
      if (state.dateTo) count++
      return count
    },
  },
  
  mutations: {
    data: (state, payload) => { state.data = payload },
    loading: (state, payload) => { state.loading = payload },
    totalPages: (state, payload) => { state.totalPages = payload },
    totalItems: (state, payload) => { state.totalItems = payload },
    perPage: (state, payload) => { state.perPage = payload },
    currentPage: (state, payload) => { state.currentPage = payload },
    searchQuery: (state, payload) => { state.searchQuery = payload },
    statusFilter: (state, payload) => { state.statusFilter = payload },
    dateFrom: (state, payload) => { state.dateFrom = payload },
    dateTo: (state, payload) => { state.dateTo = payload },
    
    // Clear all filters
    clearFilters: state => {
      state.searchQuery = ''
      state.statusFilter = null
      state.dateFrom = null
      state.dateTo = null
    },
    
    reset: state => {
      state.data = []
      state.loading = false
      state.totalPages = 0
      state.totalItems = 0
      state.perPage = 10
      state.currentPage = 1
      state.searchQuery = ''
      state.statusFilter = null
      state.dateFrom = null
      state.dateTo = null
    },
  },
}
```

---

### Form/Modal Module

For pages with create/edit modals:

```javascript
export default {
  namespaced: true,
  
  state: {
    data: [],
    loading: false,
    
    // Modal state
    showModal: false,
    editMode: false,
    currentItem: null,
    saving: false,
    
    // Form validation
    formErrors: {},
  },
  
  getters: {
    data: state => state.data,
    loading: state => state.loading,
    showModal: state => state.showModal,
    editMode: state => state.editMode,
    currentItem: state => state.currentItem,
    saving: state => state.saving,
    formErrors: state => state.formErrors,
    
    modalTitle: state => state.editMode ? 'Editar' : 'Novo',
    hasErrors: state => Object.keys(state.formErrors).length > 0,
  },
  
  mutations: {
    data: (state, payload) => { state.data = payload },
    loading: (state, payload) => { state.loading = payload },
    showModal: (state, payload) => { state.showModal = payload },
    editMode: (state, payload) => { state.editMode = payload },
    currentItem: (state, payload) => { state.currentItem = payload },
    saving: (state, payload) => { state.saving = payload },
    formErrors: (state, payload) => { state.formErrors = payload },
    
    openCreateModal: state => {
      state.showModal = true
      state.editMode = false
      state.currentItem = {}
      state.formErrors = {}
    },
    
    openEditModal: (state, item) => {
      state.showModal = true
      state.editMode = true
      state.currentItem = { ...item }
      state.formErrors = {}
    },
    
    closeModal: state => {
      state.showModal = false
      state.currentItem = null
      state.formErrors = {}
    },
    
    reset: state => {
      state.data = []
      state.loading = false
      state.showModal = false
      state.editMode = false
      state.currentItem = null
      state.saving = false
      state.formErrors = {}
    },
  },
}
```

---

## Registration Pattern

### In Index.vue

```vue
<template>
  <section>
    <FeatureFilter />
    <FeatureList />
  </section>
</template>

<script>
import { defineComponent, onUnmounted } from 'vue'
import store from '@/store'
import moduleFeatureName from '@/store/pageModules/{domain}/module-feature-name'
import FeatureFilter from './FeatureFilter.vue'
import FeatureList from './FeatureList.vue'

export default defineComponent({
  components: {
    FeatureFilter,
    FeatureList,
  },
  
  setup() {
    const moduleName = 'FeatureName'
    
    // Register module (check prevents hot-reload errors)
    if (!store.hasModule(moduleName)) {
      store.registerModule(moduleName, moduleFeatureName)
    }
    
    // Cleanup on unmount
    onUnmounted(() => {
      store.commit(`${moduleName}/reset`)
      store.unregisterModule(moduleName)
    })
  },
})
</script>
```

**Key Points:**
1. **Check `hasModule()`** before registering (prevents duplicate registration on hot-reload)
2. **Call `reset` mutation** before unregistering (cleans state)
3. **Use `onUnmounted`** hook (runs when component is destroyed)

---

## Composable Integration

Composables connect components to Vuex modules with computed get/set:

```javascript
// useFeatureName.js
import store from '@/store'
import { computed } from 'vue'

const moduleName = 'FeatureName'

export default function useFeatureName() {
  // Bidirectional computed (get/set)
  const data = computed({
    get: () => store.getters[`${moduleName}/data`],
    set: val => store.commit(`${moduleName}/data`, val),
  })
  
  const loading = computed({
    get: () => store.getters[`${moduleName}/loading`],
    set: val => store.commit(`${moduleName}/loading`, val),
  })
  
  // Methods
  const fetchData = () => {
    store.dispatch(`${moduleName}/fetchData`)
  }
  
  return {
    data,
    loading,
    fetchData,
  }
}
```

**Usage in component:**
```vue
<script>
import useFeatureName from './useFeatureName'

export default {
  setup() {
    const { data, loading, fetchData } = useFeatureName()
    
    // Read: data.value
    // Write: data.value = newValue
    // v-model works: v-model="loading"
    
    return { data, loading, fetchData }
  },
}
</script>
```

---

## Common Patterns

### Pagination Reset on Filter Change

```javascript
mutations: {
  applyFilters: (state, filters) => {
    state.filters = filters
    state.currentPage = 1  // Reset to first page
  },
}
```

### Optimistic Updates

```javascript
mutations: {
  optimisticUpdate: (state, item) => {
    const index = state.data.findIndex(i => i.id === item.id)
    if (index !== -1) {
      // Update immediately (optimistic)
      state.data.splice(index, 1, item)
    }
  },
  
  revertUpdate: (state, originalItem) => {
    const index = state.data.findIndex(i => i.id === originalItem.id)
    if (index !== -1) {
      // Revert on error
      state.data.splice(index, 1, originalItem)
    }
  },
}
```

### Bulk Selection

```javascript
state: {
  selectedIds: [],
  allSelected: false,
},

mutations: {
  toggleSelection: (state, itemId) => {
    const index = state.selectedIds.indexOf(itemId)
    if (index === -1) {
      state.selectedIds.push(itemId)
    } else {
      state.selectedIds.splice(index, 1)
    }
    state.allSelected = state.selectedIds.length === state.data.length
  },
  
  toggleSelectAll: state => {
    if (state.allSelected) {
      state.selectedIds = []
      state.allSelected = false
    } else {
      state.selectedIds = state.data.map(item => item.id)
      state.allSelected = true
    }
  },
  
  clearSelection: state => {
    state.selectedIds = []
    state.allSelected = false
  },
}
```

---

## Checklist

Before using a Vuex module:

- [ ] Module has `namespaced: true`
- [ ] All state properties have corresponding getters
- [ ] All mutations are simple setters: `(state, payload) => { state.prop = payload }`
- [ ] Module has `reset` mutation that resets ALL state
- [ ] Module is registered dynamically in Index.vue
- [ ] `store.hasModule()` check prevents duplicate registration
- [ ] `onUnmounted` hook calls `reset` then `unregisterModule`
- [ ] Composable uses computed get/set pattern
- [ ] Module file located in `src/store/pageModules/{domain}/`

---

## References

- **Feature Creator:** See `feature-creator-educacross` skill for complete feature setup
- **Composables:** See step 3 in feature creator for composable patterns
- **API Integration:** See `api-service-creator` skill for service layer
