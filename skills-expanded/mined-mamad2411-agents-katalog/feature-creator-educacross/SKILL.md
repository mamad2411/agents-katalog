---
name: feature-creator-educacross
description: Create complete features for Educacross Front Office following DDD pattern (Index/Filter/List/Composable/Vuex module/Service). Use when user says "create feature", "new feature", "implement feature", "DDD pattern", "criar feature", "nova funcionalidade", or mentions creating a complete module with filters and lists.
---

# Feature Creator - Educacross Front Office

Create production-ready features following Domain-Driven Design patterns with Vue 2.7 Composition API, Vuex modules, and reusable components.

## Architecture Overview

**Tech Stack:**
- Vue 2.7 (Composition API built-in)
- Vuex 3 (state management)
- Vue Router 3 (lazy-loaded routes)
- Bootstrap Vue 2.23
- VeeValidate 3 (form validation)
- Axios (HTTP with token refresh)

**Path Aliases:**
```javascript
'@/'           → 'src/'
'@core/'       → 'src/@core/'
'@components/' → 'src/layouts/components/'
'@axios'       → 'src/libs/axios'
'@validations' → 'src/@core/utils/validations/validations.js'
```

---

## Feature Structure (DDD Pattern)

Every feature follows this structure:

```
feature-name/
├── Index.vue              # Orchestrator: registers Vuex module, composes children
├── Filter.vue             # Filters and search (uses useFilters + ESelect)
├── List.vue               # Data display (uses ListTable or ListTableLocalSorting)
├── useDomainName.js       # Composable: bridge between components and Vuex
├── Title.vue              # Page header (optional)
├── Dashboard.vue          # Summary cards/metrics (optional)
└── components/            # Feature-specific components (optional)
    ├── ItemCard.vue
    ├── ItemModal.vue
    └── ...
```

**Real Example: Meet Books (Educateca > Conhecer Livros)**
```
meet-books/
├── MeetBooks.vue          # Index — registers moduleLibrayBooks
├── MeetBooksFilter.vue    # Search by title, author/genre filters, bulk actions
├── MeetBooksList.vue      # Grid of cards with pagination and detail modals
├── useMeetBooks.js        # Composable with state, fetch, filters, pagination
└── components/
    ├── MeetBookCard.vue   # Individual book card
    └── BookDetails.vue    # Book details modal
```

---

## Step-by-Step Implementation

### Step 1: Create Vuex Module

**Location:** `src/store/pageModules/{domain}/module-{feature-name}.js`

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
    searchQuery: '',
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
    searchQuery: state => state.searchQuery,
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
    searchQuery: (state, payload) => { state.searchQuery = payload },
    
    // REQUIRED: Reset mutation for cleanup on unmount
    reset: state => {
      state.data = []
      state.loading = false
      state.totalPages = 0
      state.totalItems = 0
      state.perPage = 10
      state.currentPage = 1
      state.sortBy = ''
      state.isSortDirDesc = false
      state.searchQuery = ''
    },
  },
  
  actions: {
    // Actions for API calls if needed
  },
}
```

**Key Principles:**
1. **Always `namespaced: true`** — prevents conflicts
2. **Getter for every state property** — enables computed reactivity
3. **Mutations are simple setters** — `(state, payload) => { state.prop = payload }`
4. **Required `reset` mutation** — cleanup on unmount

---

### Step 2: Create API Service

**Location:** `src/services/{context}/{domain}/{FeatureName}.service.js`

```javascript
import axiosIns from '@/libs/axios'
import { urlString } from '@/utils/utils'

const resource = '/v2/feature-name'

export const getFeatureList = filters => {
  const parameters = urlString(filters)
  return axiosIns.get(`${resource}?${parameters}`)
}

export const getFeatureById = id => {
  return axiosIns.get(`${resource}/${id}`)
}

export const createFeature = data => {
  return axiosIns.post(resource, data)
}

export const updateFeature = (id, data) => {
  return axiosIns.put(`${resource}/${id}`, data)
}

export const deleteFeature = id => {
  return axiosIns.delete(`${resource}/${id}`)
}
```

**Naming Conventions:**
- `get*` → GET requests
- `create*` → POST requests
- `update*` → PUT requests
- `delete*` → DELETE requests
- `enable*`/`disable*` → Toggle endpoints

**Helper:** `urlString()` converts objects to query strings, supports arrays:
```javascript
{ ClassId: 1, PageSize: 10 } → "&ClassId=1&PageSize=10"
{ Ids: [1, 2, 3] } → "&Ids=1&Ids=2&Ids=3"
```

---

### Step 3: Create Domain Composable

**Location:** `src/views/pages/{context}/{domain}/{feature}/useFeatureName.js`

```javascript
import store from '@/store'
import useFilters from '@/store/filters/useFilters'
import { computed } from 'vue'
import { getFeatureList } from '@/services/{context}/{domain}/FeatureName.service'

const moduleName = 'FeatureName'

export default function useFeatureName() {
  const { subject, classe } = useFilters()
  
  // Bidirectional computed properties (get/set pattern)
  const data = computed({
    get: () => store.getters[`${moduleName}/data`],
    set: val => store.commit(`${moduleName}/data`, val),
  })
  
  const loading = computed({
    get: () => store.getters[`${moduleName}/loading`],
    set: val => store.commit(`${moduleName}/loading`, val),
  })
  
  const totalPages = computed({
    get: () => store.getters[`${moduleName}/totalPages`],
    set: val => store.commit(`${moduleName}/totalPages`, val),
  })
  
  const totalItems = computed({
    get: () => store.getters[`${moduleName}/totalItems`],
    set: val => store.commit(`${moduleName}/totalItems`, val),
  })
  
  const perPage = computed({
    get: () => store.getters[`${moduleName}/perPage`],
    set: val => store.commit(`${moduleName}/perPage`, val),
  })
  
  const currentPage = computed({
    get: () => store.getters[`${moduleName}/currentPage`],
    set: val => store.commit(`${moduleName}/currentPage`, val),
  })
  
  const sortBy = computed({
    get: () => store.getters[`${moduleName}/sortBy`],
    set: val => store.commit(`${moduleName}/sortBy`, val),
  })
  
  const isSortDirDesc = computed({
    get: () => store.getters[`${moduleName}/isSortDirDesc`],
    set: val => store.commit(`${moduleName}/isSortDirDesc`, val),
  })
  
  const searchQuery = computed({
    get: () => store.getters[`${moduleName}/searchQuery`],
    set: val => store.commit(`${moduleName}/searchQuery`, val),
  })
  
  // Build filters for API request
  const buildFilters = () => ({
    SubjectId: subject.value?.id,
    ClassId: classe.value?.id,
    PageSize: perPage.value,
    Page: currentPage.value,
    OrderBy: sortBy.value,
    IsDesc: isSortDirDesc.value,
    SearchQuery: searchQuery.value,
  })
  
  // Fetch data from API
  const fetchData = async () => {
    loading.value = true
    try {
      const filters = buildFilters()
      const response = await getFeatureList(filters)
      
      data.value = response.data.items
      totalPages.value = response.data.totalPages
      totalItems.value = response.data.totalItems
    } catch (error) {
      console.error('Error fetching data:', error)
      data.value = []
    } finally {
      loading.value = false
    }
  }
  
  return {
    // State
    data,
    loading,
    totalPages,
    totalItems,
    perPage,
    currentPage,
    sortBy,
    isSortDirDesc,
    searchQuery,
    
    // Methods
    fetchData,
    buildFilters,
  }
}
```

**Pattern:** Computed get/set allows v-model binding and direct assignment in components.

---

### Step 4: Create Index.vue (Orchestrator)

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
    // Register Vuex module dynamically
    const moduleName = 'FeatureName'
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
- **Dynamic registration** prevents global pollution
- **`onUnmounted`** cleanup is mandatory
- **Check `hasModule`** before registering (prevents hot-reload errors)

---

### Step 5: Create Filter.vue

```vue
<template>
  <b-card no-body class="mb-1">
    <b-card-body>
      <b-row>
        <!-- Search input -->
        <b-col cols="12" md="4">
          <b-form-group label="Buscar" label-for="search">
            <b-form-input
              id="search"
              v-model="search"
              placeholder="Digite para buscar..."
            />
          </b-form-group>
        </b-col>
        
        <!-- Filter select -->
        <b-col cols="12" md="4">
          <b-form-group label="Filtro" label-for="filter">
            <ESelect
              v-model="selectedFilter"
              :options="filterOptions"
              label="name"
              placeholder="Selecione um filtro"
              clearable
              @clear="onClearFilter"
            />
          </b-form-group>
        </b-col>
        
        <!-- Action button -->
        <b-col cols="12" md="4" class="d-flex align-items-end">
          <b-button
            variant="primary"
            @click="fetchData"
          >
            Buscar
          </b-button>
        </b-col>
      </b-row>
    </b-card-body>
  </b-card>
</template>

<script>
import { defineComponent, ref, watch } from 'vue'
import ESelect from '@/components/selects/ESelect.vue'
import useFilters from '@/store/filters/useFilters'
import useFeatureName from './useFeatureName'
import { debounce } from '@/utils/debounce'

export default defineComponent({
  components: { ESelect },
  
  setup() {
    const { classe } = useFilters()
    const { searchQuery, fetchData } = useFeatureName()
    
    const search = ref('')
    const selectedFilter = ref(null)
    const filterOptions = ref([])
    
    // Debounced search
    const debouncedSearch = debounce(() => {
      searchQuery.value = search.value
      fetchData()
    }, 500)
    
    watch(search, debouncedSearch)
    
    // React to class changes (REQUIRED for useFilters integration)
    watch(classe, () => {
      if (classe.value?.id) {
        fetchData()
      }
    })
    
    const onClearFilter = () => {
      selectedFilter.value = null
      fetchData()
    }
    
    return {
      search,
      selectedFilter,
      filterOptions,
      fetchData,
      onClearFilter,
    }
  },
})
</script>
```

**Key Patterns:**
- **ALWAYS use `ESelect`** (never `v-select` or native `<select>`)
- **Debounce search** with 500ms delay
- **Watch `classe` from `useFilters()`** — mandatory for educational features
- **Call `fetchData()` on class change**

---

### Step 6: Create List.vue

```vue
<template>
  <b-card no-body>
    <ListTable
      :table-columns="tableColumns"
      :data-table="data"
      :loading="loading"
      :per-page="perPage"
      :total-items="totalItems"
      :current-page="currentPage"
      :sort-by="sortBy"
      :is-sort-dir-desc="isSortDirDesc"
      @change="onTableChange"
    >
      <!-- Custom column slots -->
      <template #cell(name)="{ item }">
        <strong>{{ item.name }}</strong>
      </template>
      
      <template #cell(actions)="{ item }">
        <b-button
          variant="primary"
          size="sm"
          @click="onEdit(item)"
        >
          Editar
        </b-button>
      </template>
    </ListTable>
  </b-card>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue'
import ListTable from '@/components/table/ListTable.vue'
import useFeatureName from './useFeatureName'

export default defineComponent({
  components: { ListTable },
  
  setup() {
    const {
      data,
      loading,
      totalItems,
      perPage,
      currentPage,
      sortBy,
      isSortDirDesc,
      fetchData,
    } = useFeatureName()
    
    const tableColumns = ref([
      { key: 'name', label: 'Nome', sortable: true },
      { key: 'status', label: 'Status', sortable: true },
      { key: 'actions', label: 'Ações' },
    ])
    
    const onTableChange = params => {
      perPage.value = params.perPage
      currentPage.value = params.currentPage
      sortBy.value = params.sortBy
      isSortDirDesc.value = params.isSortDirDesc
      fetchData()
    }
    
    const onEdit = item => {
      console.log('Edit:', item)
    }
    
    onMounted(() => {
      fetchData()
    })
    
    return {
      tableColumns,
      data,
      loading,
      totalItems,
      perPage,
      currentPage,
      sortBy,
      isSortDirDesc,
      onTableChange,
      onEdit,
    }
  },
})
</script>
```

**Table Components:**
- **`ListTable`** — server-side pagination (use for large datasets)
- **`ListTableLocalSorting`** — client-side pagination (<1000 records)
- **`ListTableSelect`** — server-side with row selection
- **`ListTableSelectLocal`** — client-side with row selection

---

## useFilters Integration (REQUIRED)

For features with subject/class filters, **ALWAYS integrate `useFilters()`**:

```javascript
import useFilters from '@/store/filters/useFilters'

const {
  // Subject
  subject,           // computed (get/set)
  subjects,          // available subjects array
  
  // Class
  classe,            // computed (get/set)
  classes,           // available classes array
  
  // Role checks
  isTeacher,         // boolean
  isStudent,         // boolean
  isNetworkManager,  // boolean
} = useFilters()

// React to class changes
watch(classe, () => {
  if (classe.value?.id) {
    fetchData()
  }
})
```

---

## Feature Checklist

Before submitting PR, verify:

- [ ] Vuex module created in `src/store/pageModules/{domain}/`
- [ ] Module has `namespaced: true`
- [ ] Module has `reset` mutation
- [ ] All state properties have corresponding getters
- [ ] API service created in `src/services/{context}/{domain}/`
- [ ] Service uses `urlString()` helper for query parameters
- [ ] Composable created with computed get/set pattern
- [ ] `Index.vue` registers/unregisters module dynamically
- [ ] `Filter.vue` uses `ESelect` (NOT v-select)
- [ ] Search is debounced (500ms)
- [ ] `useFilters()` integrated and watches `classe` changes
- [ ] `List.vue` uses appropriate table component
- [ ] Route added to `src/router/{role}-routes.js`
- [ ] Navigation item added to `src/navigation/{role}/*`
- [ ] i18n keys added to locale files
- [ ] Permissions configured with CASL if needed

---

## Common Patterns

### Pagination Reset on Filter Change

```javascript
watch([subject, classe, selectedFilter], () => {
  currentPage.value = 1  // Reset to first page
  fetchData()
})
```

### Loading Multiple Dropdowns

```javascript
const loadFilterOptions = async () => {
  try {
    const response = await getFilterOptions()
    filterOptions.value = response.data
  } catch (error) {
    console.error('Error loading options:', error)
    filterOptions.value = []
  }
}

onMounted(() => {
  loadFilterOptions()
})
```

### Bulk Actions

```javascript
const selectedItems = ref([])

const onBulkDelete = async () => {
  if (!selectedItems.value.length) return
  
  try {
    await Promise.all(
      selectedItems.value.map(item => deleteFeature(item.id))
    )
    selectedItems.value = []
    fetchData()
  } catch (error) {
    console.error('Error bulk deleting:', error)
  }
}
```

---

## References

- **Components Guide:** See `component-usage-educacross` skill
- **Vuex Module Patterns:** See `vuex-module-creator` skill
- **API Service Patterns:** See `api-service-creator` skill
- **Form Validation:** See `form-validation-educacross` skill
