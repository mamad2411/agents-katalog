---
name: api-service-creator
description: Create API service modules for backend communication following Educacross patterns (organized by domain, consistent naming, urlString helper). Use when user says "create service", "API service", "endpoint", "axios", "serviço API", or needs to communicate with backend.
---

# API Service Creator - Educacross Front Office

Create organized, reusable API service modules for backend communication with consistent patterns and error handling.

## Service Organization

```
src/services/
├── teacher-context/
│   ├── books/
│   │   └── BookLibrary.service.js
│   ├── guides/
│   │   └── Guides.Service.js
│   └── missions/
│       └── Missions.service.js
├── student-context/
│   ├── missions/
│   │   └── StudentMissions.service.js
│   └── progress/
│       └── Progress.service.js
├── shared/
│   ├── classes/
│   │   └── Classes.service.js
│   └── institutions/
│       └── Institutions.service.js
└── auth-context/
    └── Auth.service.js
```

**Structure:**
```
services/
└── {context}/         # User role context (teacher, student, admin, shared)
    └── {domain}/      # Business domain (missions, books, reports)
        └── {Feature}.service.js
```

---

## Naming Conventions

### File Names

- **PascalCase + `.service.js`**: `BookLibrary.service.js`, `Missions.service.js`
- **Match domain**: Service name reflects the domain it serves

### Function Names

| HTTP Method | Prefix | Example |
|-------------|--------|---------|
| GET | `get*` | `getBooksLibrary()`, `getMissionById()` |
| POST | `create*` | `createMission()`, `createGuide()` |
| PUT | `update*` | `updateMission()`, `updateGuide()` |
| DELETE | `delete*` | `deleteMission()`, `deleteGuide()` |
| PUT/POST | `enable*` / `disable*` | `enableDisableBooksLibrary()` |
| PUT/POST | `activate*` / `deactivate*` | `activateMission()` |
| POST | `submit*` | `submitAssignment()` |
| GET | `fetch*` | `fetchReportData()` |

---

## Complete Service Template

### Basic CRUD Service

```javascript
import axiosIns from '@/libs/axios'
import { urlString } from '@/utils/utils'

const resource = '/v2/feature-name'

/**
 * Get paginated list of items
 * @param {Object} filters - Query filters
 * @param {number} filters.Page - Page number
 * @param {number} filters.PageSize - Items per page
 * @param {string} filters.OrderBy - Sort column
 * @param {boolean} filters.IsDesc - Sort direction
 * @param {string} filters.SearchQuery - Search term
 * @returns {Promise<AxiosResponse>}
 */
export const getFeatureList = filters => {
  const parameters = urlString(filters)
  return axiosIns.get(`${resource}?${parameters}`)
}

/**
 * Get single item by ID
 * @param {number} id - Item ID
 * @returns {Promise<AxiosResponse>}
 */
export const getFeatureById = id => {
  return axiosIns.get(`${resource}/${id}`)
}

/**
 * Create new item
 * @param {Object} data - Item data
 * @returns {Promise<AxiosResponse>}
 */
export const createFeature = data => {
  return axiosIns.post(resource, data)
}

/**
 * Update existing item
 * @param {number} id - Item ID
 * @param {Object} data - Updated data
 * @returns {Promise<AxiosResponse>}
 */
export const updateFeature = (id, data) => {
  return axiosIns.put(`${resource}/${id}`, data)
}

/**
 * Delete item
 * @param {number} id - Item ID
 * @returns {Promise<AxiosResponse>}
 */
export const deleteFeature = id => {
  return axiosIns.delete(`${resource}/${id}`)
}
```

---

## urlString Helper

**Location:** `src/utils/utils.js`

Converts filter objects to URL query strings, supporting arrays.

### Usage

```javascript
import { urlString } from '@/utils/utils'

// Simple filters
const filters = {
  ClassId: 1,
  PageSize: 10,
  Page: 1,
}
const params = urlString(filters)
// Result: "&ClassId=1&PageSize=10&Page=1"

// With arrays
const filters = {
  Ids: [1, 2, 3],
  Types: ['A', 'B'],
}
const params = urlString(filters)
// Result: "&Ids=1&Ids=2&Ids=3&Types=A&Types=B"

// With null/undefined (skipped)
const filters = {
  ClassId: 1,
  SubjectId: null,
  SearchQuery: undefined,
}
const params = urlString(filters)
// Result: "&ClassId=1"

// Usage in service
export const getData = filters => {
  const parameters = urlString(filters)
  return axiosIns.get(`${resource}?${parameters}`)
}
```

**Key Features:**
- Skips `null`, `undefined`, and empty string values
- Handles arrays by repeating the key: `Ids=1&Ids=2&Ids=3`
- Starts with `&` for easy concatenation
- URL-encodes values automatically

---

## Real-World Examples

### Books Library Service

```javascript
// src/services/teacher-context/books/BookLibrary.service.js
import axiosIns from '@/libs/axios'
import { urlString } from '@/utils/utils'

const resource = '/v2/books-library'

export const getBooksLibrary = filters => {
  const parameters = urlString(filters)
  return axiosIns.get(`${resource}?${parameters}`)
}

export const getBookById = id => {
  return axiosIns.get(`${resource}/${id}`)
}

export const enableDisableBooksLibrary = (id, classId) => {
  return axiosIns.put(`${resource}/${id}/enable-disable`, { classId })
}

export const getBooksByMission = missionId => {
  return axiosIns.get(`${resource}/by-mission/${missionId}`)
}

export const addBookToMission = (bookId, missionId) => {
  return axiosIns.post(`${resource}/${bookId}/missions`, { missionId })
}

export const removeBookFromMission = (bookId, missionId) => {
  return axiosIns.delete(`${resource}/${bookId}/missions/${missionId}`)
}
```

---

### Missions Service

```javascript
// src/services/teacher-context/missions/Missions.service.js
import axiosIns from '@/libs/axios'
import { urlString } from '@/utils/utils'

const resource = '/v2/missions'

export const getMissions = filters => {
  const parameters = urlString(filters)
  return axiosIns.get(`${resource}?${parameters}`)
}

export const getMissionById = id => {
  return axiosIns.get(`${resource}/${id}`)
}

export const createMission = data => {
  return axiosIns.post(resource, data)
}

export const updateMission = (id, data) => {
  return axiosIns.put(`${resource}/${id}`, data)
}

export const deleteMission = id => {
  return axiosIns.delete(`${resource}/${id}`)
}

export const publishMission = id => {
  return axiosIns.post(`${resource}/${id}/publish`)
}

export const unpublishMission = id => {
  return axiosIns.post(`${resource}/${id}/unpublish`)
}

export const getMissionStudents = (id, filters) => {
  const parameters = urlString(filters)
  return axiosIns.get(`${resource}/${id}/students?${parameters}`)
}

export const assignMissionToClass = (missionId, classId) => {
  return axiosIns.post(`${resource}/${missionId}/assign`, { classId })
}
```

---

### Classes Service (Shared)

```javascript
// src/services/shared/classes/Classes.service.js
import axiosIns from '@/libs/axios'
import { urlString } from '@/utils/utils'

const resource = '/v2/classes'

export const getClasses = filters => {
  const parameters = urlString(filters)
  return axiosIns.get(`${resource}?${parameters}`)
}

export const getClassById = id => {
  return axiosIns.get(`${resource}/${id}`)
}

export const getClassStudents = (id, filters) => {
  const parameters = urlString(filters)
  return axiosIns.get(`${resource}/${id}/students?${parameters}`)
}

export const getClassSubjects = classId => {
  return axiosIns.get(`${resource}/${classId}/subjects`)
}
```

---

## Service Patterns

### Paginated List

```javascript
/**
 * Get paginated list
 * Standard pagination parameters are:
 * - Page: Current page number (1-based)
 * - PageSize: Items per page
 * - OrderBy: Column name to sort by
 * - IsDesc: Sort direction (true = descending)
 * - SearchQuery: Search term
 */
export const getList = filters => {
  const parameters = urlString(filters)
  return axiosIns.get(`${resource}?${parameters}`)
}

// Usage
const response = await getList({
  Page: 1,
  PageSize: 10,
  OrderBy: 'name',
  IsDesc: false,
  SearchQuery: 'search term',
})

// Expected response structure:
// {
//   items: [...],
//   totalItems: 100,
//   totalPages: 10,
//   currentPage: 1,
//   pageSize: 10,
// }
```

---

### Nested Resources

```javascript
// Parent resource
export const getMissions = filters => {
  const parameters = urlString(filters)
  return axiosIns.get('/v2/missions' + `?${parameters}`)
}

// Nested: missions/{id}/students
export const getMissionStudents = (missionId, filters) => {
  const parameters = urlString(filters)
  return axiosIns.get(`/v2/missions/${missionId}/students?${parameters}`)
}

// Nested: missions/{id}/guides
export const getMissionGuides = missionId => {
  return axiosIns.get(`/v2/missions/${missionId}/guides`)
}

// Nested: missions/{id}/progress
export const getMissionProgress = (missionId, filters) => {
  const parameters = urlString(filters)
  return axiosIns.get(`/v2/missions/${missionId}/progress?${parameters}`)
}
```

---

### File Upload

```javascript
/**
 * Upload file
 * @param {File} file - File to upload
 * @param {Function} onUploadProgress - Progress callback
 * @returns {Promise<AxiosResponse>}
 */
export const uploadFile = (file, onUploadProgress) => {
  const formData = new FormData()
  formData.append('file', file)
  
  return axiosIns.post(`${resource}/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    onUploadProgress,
  })
}

// Usage
const file = event.target.files[0]
const response = await uploadFile(file, progressEvent => {
  const percentCompleted = Math.round(
    (progressEvent.loaded * 100) / progressEvent.total
  )
  console.log(`Upload progress: ${percentCompleted}%`)
})
```

---

### Bulk Operations

```javascript
/**
 * Bulk delete
 * @param {number[]} ids - Array of IDs to delete
 * @returns {Promise<AxiosResponse>}
 */
export const bulkDelete = ids => {
  const parameters = urlString({ Ids: ids })
  return axiosIns.delete(`${resource}/bulk${parameters}`)
}

/**
 * Bulk update
 * @param {Object[]} items - Array of items to update
 * @returns {Promise<AxiosResponse>}
 */
export const bulkUpdate = items => {
  return axiosIns.put(`${resource}/bulk`, items)
}

// Usage
await bulkDelete([1, 2, 3, 4, 5])
// Request: DELETE /v2/resource/bulk?Ids=1&Ids=2&Ids=3&Ids=4&Ids=5
```

---

### Export/Download

```javascript
/**
 * Export data to Excel
 * @param {Object} filters - Export filters
 * @returns {Promise<Blob>}
 */
export const exportToExcel = filters => {
  const parameters = urlString(filters)
  return axiosIns.get(`${resource}/export?${parameters}`, {
    responseType: 'blob',
  })
}

// Usage
const blob = await exportToExcel({ ClassId: 1 })
const url = window.URL.createObjectURL(blob)
const link = document.createElement('a')
link.href = url
link.download = 'export.xlsx'
link.click()
```

---

## Integration with Vuex Actions

```javascript
// In Vuex module actions
import { getFeatureList, createFeature, updateFeature } from '@/services/.../Feature.service'

actions: {
  async fetchData({ commit, state }) {
    commit('loading', true)
    try {
      const filters = {
        Page: state.currentPage,
        PageSize: state.perPage,
        OrderBy: state.sortBy,
        IsDesc: state.isSortDirDesc,
        SearchQuery: state.searchQuery,
      }
      
      const response = await getFeatureList(filters)
      
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
  
  async saveItem({ commit, dispatch }, item) {
    commit('saving', true)
    try {
      if (item.id) {
        await updateFeature(item.id, item)
      } else {
        await createFeature(item)
      }
      
      await dispatch('fetchData')
      return { success: true }
    } catch (error) {
      console.error('Error saving:', error)
      return { success: false, error }
    } finally {
      commit('saving', false)
    }
  },
}
```

---

## Direct Usage in Components

```vue
<script>
import { getFeatureList, createFeature } from '@/services/.../Feature.service'
import { ref } from 'vue'

export default {
  setup() {
    const data = ref([])
    const loading = ref(false)
    
    const fetchData = async () => {
      loading.value = true
      try {
        const response = await getFeatureList({
          Page: 1,
          PageSize: 10,
        })
        data.value = response.data.items
      } catch (error) {
        console.error('Error:', error)
        data.value = []
      } finally {
        loading.value = false
      }
    }
    
    const createItem = async itemData => {
      try {
        await createFeature(itemData)
        await fetchData()
        return true
      } catch (error) {
        console.error('Error creating:', error)
        return false
      }
    }
    
    return {
      data,
      loading,
      fetchData,
      createItem,
    }
  },
}
</script>
```

---

## Error Handling

### In Services (Keep Simple)

```javascript
// ❌ DON'T handle errors in services
export const getData = async filters => {
  try {
    return await axiosIns.get(`${resource}?${urlString(filters)}`)
  } catch (error) {
    // Don't handle here - let caller decide
    console.error(error)
  }
}

// ✅ DO let errors bubble up
export const getData = filters => {
  return axiosIns.get(`${resource}?${urlString(filters)}`)
}
```

### In Vuex Actions (Handle with Context)

```javascript
actions: {
  async fetchData({ commit }) {
    commit('loading', true)
    try {
      const response = await getFeatureList(filters)
      commit('data', response.data.items)
    } catch (error) {
      console.error('Error fetching data:', error)
      commit('data', [])
      
      // Show toast notification
      this._vm.$toast({
        component: ToastificationContent,
        props: {
          title: 'Erro ao carregar dados',
          icon: 'AlertCircleIcon',
          variant: 'danger',
        },
      })
    } finally {
      commit('loading', false)
    }
  },
}
```

---

## Axios Configuration

Services use pre-configured `axiosIns` from `@/libs/axios`:

```javascript
// src/libs/axios.js (reference only - don't modify)
import axios from 'axios'
import router from '@/router'

const axiosIns = axios.create({
  baseURL: process.env.VUE_APP_API_URL,
  timeout: 30000,
})

// Request interceptor: Add auth token
axiosIns.interceptors.request.use(
  config => {
    const token = localStorage.getItem('accessToken')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

// Response interceptor: Handle token refresh
axiosIns.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401) {
      // Token refresh logic or redirect to login
      router.push({ name: 'auth-login' })
    }
    return Promise.reject(error)
  }
)

export default axiosIns
```

---

## Service Checklist

Before using a service:

- [ ] Service file in correct location: `src/services/{context}/{domain}/`
- [ ] File named with PascalCase + `.service.js`
- [ ] Uses `axiosIns` from `@/libs/axios`
- [ ] Uses `urlString()` helper for query parameters
- [ ] Function names follow conventions (get*, create*, update*, delete*)
- [ ] JSDoc comments for complex functions
- [ ] Errors bubble up to caller (no try/catch in service)
- [ ] Returns raw Axios promise (not async/await in service)
- [ ] Named exports (not default export)

---

## Common Mistakes

❌ **DON'T:**
```javascript
// Don't use axios directly
import axios from 'axios'
axios.get('/v2/endpoint')

// Don't manually build query strings
`${resource}?ClassId=${classId}&Page=${page}`

// Don't default export
export default {
  getData,
  createData,
}

// Don't handle business logic in services
export const getData = async () => {
  const response = await axiosIns.get(resource)
  return response.data.items.filter(item => item.active)
}
```

✅ **DO:**
```javascript
// Use axiosIns
import axiosIns from '@/libs/axios'

// Use urlString helper
import { urlString } from '@/utils/utils'
const params = urlString({ ClassId: classId, Page: page })

// Named exports
export const getData = () => { ... }
export const createData = () => { ... }

// Keep services simple, logic in composables/actions
export const getData = filters => {
  return axiosIns.get(`${resource}?${urlString(filters)}`)
}
```

---

## References

- **Feature Creator:** See `feature-creator-educacross` skill for complete integration
- **Vuex Integration:** See `vuex-module-creator` skill for actions pattern
- **Component Usage:** Call services from composables, not components directly
