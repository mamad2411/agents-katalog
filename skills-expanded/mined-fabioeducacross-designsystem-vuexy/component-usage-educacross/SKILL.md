---
name: component-usage-educacross
description: Use reusable components from Educacross Front Office component library (ESelect, ListTable, MediaCard, ProgressBar, etc.). Use when user mentions "ESelect", "ListTable", "select", "table", "tabela", "componente reutilizável", "card", "progress bar", "gráfico", or any component name from src/components/.
---

# Component Usage Guide - Educacross Front Office

Comprehensive guide for using all reusable components in `src/components/`.

## Quick Reference

| Component | Path | Use When |
|-----------|------|----------|
| **ESelect** | `@/components/selects/ESelect.vue` | ANY dropdown/select (NEVER use v-select) |
| **ListTable** | `@/components/table/ListTable.vue` | Server-side paginated tables |
| **ListTableLocalSorting** | `@/components/table/ListTableLocalSorting.vue` | Client-side tables (<1000 records) |
| **MediaCard** | `@/components/cards/MediaCard.vue` | Content cards with image/icon |
| **ProgressBarHorizontal** | `@/components/progress/ProgressBarHorizontal.vue` | Horizontal progress bars |
| **BarChart** | `@/components/charts/BarChart.vue` | Bar charts with ApexCharts |

---

## ⚠️ CRITICAL RULES

### 1. ALWAYS Use ESelect

**NEVER use:**
- `v-select` (deprecated)
- `<select>` native HTML
- `<b-form-select>` Bootstrap Vue

**ALWAYS use:**
```vue
<ESelect
  v-model="selected"
  :options="options"
  label="name"
/>
```

### 2. Choose Correct Table Component

| Records | Pagination | Component |
|---------|-----------|-----------|
| Any | Server-side | `ListTable` |
| <1000 | Client-side | `ListTableLocalSorting` |
| Any + Selection | Server-side | `ListTableSelect` |
| <1000 + Selection | Client-side | `ListTableSelectLocal` |

---

## Selects

### ESelect

**Primary select component** — supports single/multiple selection, search, pagination, and modal for selected options.

#### Basic Usage

```vue
<template>
  <ESelect
    v-model="selected"
    :options="options"
    label="name"
    placeholder="selectAnOption"
    clearable
  />
</template>

<script>
import ESelect from '@/components/selects/ESelect.vue'

export default {
  components: { ESelect },
  data() {
    return {
      selected: null,
      options: [
        { id: 1, name: 'Option 1' },
        { id: 2, name: 'Option 2' },
      ],
    }
  },
}
</script>
```

#### Multi-Select with Modal

```vue
<ESelect
  v-model="selectedItems"
  :options="items"
  label="name"
  :multiple="true"
  :table-columns="tableColumns"
  table-title="Selected Items"
  prefix="items"
  gender="M"
/>
```

**Props:**
```javascript
{
  value: null,              // Selected value(s)
  options: [],              // REQUIRED - Array of options
  label: 'name',            // Property to display
  trackBy: undefined,       // Unique identifier property
  loading: false,           // Show spinner
  variant: 'primary',       // Bootstrap variant
  state: null,              // Validation state (false = invalid)
  multiple: false,          // Enable multi-select
  closeOnSelect: true,      // Close after selection (single mode)
  clearable: false,         // Show clear button
  searchable: false,        // Enable search input
  placeholder: 'selectAnOption', // i18n key
  paginated: false,         // Enable infinite scroll pagination
  page: 1,                  // Current page
  totalPages: 1,            // Total pages available
  disabled: false,          // Disable select
  prefix: '',               // i18n prefix for count text
  gender: 'F',              // Gender for i18n plurals ('M'/'F')
  tableColumns: [],         // Columns for modal table
  tableTitle: '',           // Modal title
  searchPlaceholder: '',    // Search placeholder i18n key
  usePortalOnModal: false,  // Use Portal for modal isolation
  skipInitialRequest: false // Skip first API request
}
```

**Events:**
```javascript
@input="onInput"           // Value changed
@change="onChange"         // Dropdown closed with changes
@nextPage="onNextPage"     // Scroll reached end (paginated mode)
@close="onClose"           // Dropdown closed
@clear="onClear"           // All options cleared
@closeModal="onCloseModal" // Modal closed
```

**Slots:**
```vue
<!-- Custom selected option display -->
<template #selected-option="{ option }">
  <strong>{{ option.name }}</strong>
</template>

<!-- Custom option display -->
<template #option="{ option }">
  <div class="d-flex align-items-center">
    <feather-icon :icon="option.icon" class="mr-1" />
    {{ option.name }}
  </div>
</template>

<!-- Custom selected count badge -->
<template #selectedOptionsCountLabel="{ selectedLength }">
  {{ selectedLength }} selecionados
</template>
```

#### Paginated Select

```vue
<ESelect
  v-model="selected"
  :options="options"
  :paginated="true"
  :page="currentPage"
  :total-pages="totalPages"
  label="name"
  searchable
  @nextPage="loadNextPage"
/>
```

```javascript
methods: {
  loadNextPage({ search, page, totalPages }) {
    if (page >= totalPages) return
    
    this.currentPage = page + 1
    // Fetch more data and append to options
    this.fetchOptions(search, this.currentPage)
  }
}
```

---

### InfinityScroll

**Wrapper around ESelect** with built-in pagination logic.

```vue
<InfinityScroll
  v-model="selected"
  :options="fetchOptionsAsync"
  :total-pages="10"
  label="name"
  :searchable="true"
/>
```

**With Async Function:**
```javascript
async fetchOptionsAsync({ page, search, pageSize }) {
  const response = await api.getOptions({ page, search, pageSize })
  return response.data.items
}
```

**With Static Array:**
```vue
<InfinityScroll
  v-model="selected"
  :options="staticOptions"
  label="name"
/>
```

---

### SelectInfinityScroll

**Direct API integration** with infinite scroll.

```vue
<SelectInfinityScroll
  v-model="selected"
  api="/v2/endpoint"
  :father-params="{ ClassId: classId }"
  label="name"
  placeholder="Selecione uma opção"
  :multiple="false"
  :clearable="true"
  :get-on-created="true"
  @isReady="onReady"
/>
```

**For Classes (with SchoolYearBadge):**
```vue
<SelectInfinityScroll
  v-model="selectedClass"
  api="/v2/classes"
  label="name"
  :is-class="true"
/>
```

This enables custom slots for class display with year badges.

---

## Tables

### ListTable

**Server-side paginated table** — use for large datasets.

```vue
<template>
  <ListTable
    :table-columns="tableColumns"
    :data-table="data"
    :loading="loading"
    :per-page="perPage"
    :total-items="totalItems"
    :current-page="currentPage"
    :sort-by="sortBy"
    :is-sort-dir-desc="isSortDirDesc"
    :show-export-excel="true"
    excel-file-name="report"
    @change="onTableChange"
  >
    <!-- Custom column rendering -->
    <template #cell(name)="{ item }">
      <strong>{{ item.name }}</strong>
    </template>
    
    <template #cell(status)="{ item }">
      <b-badge :variant="item.status === 'active' ? 'success' : 'secondary'">
        {{ item.status }}
      </b-badge>
    </template>
    
    <template #cell(actions)="{ item }">
      <b-button size="sm" variant="primary" @click="onEdit(item)">
        Editar
      </b-button>
    </template>
  </ListTable>
</template>

<script>
import ListTable from '@/components/table/ListTable.vue'

export default {
  components: { ListTable },
  
  data() {
    return {
      tableColumns: [
        { key: 'name', label: 'Nome', sortable: true },
        { key: 'status', label: 'Status', sortable: true },
        { key: 'actions', label: 'Ações' },
      ],
      data: [],
      loading: false,
      perPage: 10,
      totalItems: 0,
      currentPage: 1,
      sortBy: '',
      isSortDirDesc: false,
    }
  },
  
  methods: {
    onTableChange({ perPage, currentPage, sortBy, isSortDirDesc, searchQuery }) {
      this.perPage = perPage
      this.currentPage = currentPage
      this.sortBy = sortBy
      this.isSortDirDesc = isSortDirDesc
      this.fetchData()
    },
    
    async fetchData() {
      this.loading = true
      try {
        const response = await api.getData({
          PageSize: this.perPage,
          Page: this.currentPage,
          OrderBy: this.sortBy,
          IsDesc: this.isSortDirDesc,
        })
        this.data = response.data.items
        this.totalItems = response.data.totalItems
      } catch (error) {
        console.error(error)
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
```

**Key Props:**
```javascript
{
  tableColumns: [],         // REQUIRED - Column definitions
  dataTable: [],            // REQUIRED - Data array
  loading: false,           // Show loading state
  perPage: 10,              // Items per page
  totalItems: 0,            // Total records from API
  currentPage: 1,           // Current page
  sortBy: '',               // Column to sort by
  isSortDirDesc: false,     // Sort direction
  showExportExcel: false,   // Show Excel export button
  excelFileName: 'data',    // Export filename
  excelTitle: '',           // Optional Excel title
  variant: 'hover',         // Table variant
  emptyText: 'Sem dados',   // Empty state text
}
```

---

### ListTableLocalSorting

**Client-side pagination** — use for <1000 records.

```vue
<ListTableLocalSorting
  :table-columns="tableColumns"
  :data-table="allData"
  :loading="loading"
  :per-page="10"
  :show-export-excel="true"
>
  <template #cell(name)="{ item }">
    {{ item.name }}
  </template>
</ListTableLocalSorting>
```

**Differences from ListTable:**
- No `totalItems` prop (calculated from data length)
- No `currentPage` prop (managed internally)
- Sorting/pagination handled client-side
- Pass ALL data at once

---

### ListTableSelect / ListTableSelectLocal

**Tables with row selection** — use when bulk actions needed.

```vue
<ListTableSelect
  :table-columns="tableColumns"
  :data-table="data"
  :loading="loading"
  :per-page="perPage"
  :total-items="totalItems"
  :selected-items="selectedItems"
  @change="onTableChange"
  @update:selectedItems="selectedItems = $event"
>
  <template #cell(name)="{ item }">
    {{ item.name }}
  </template>
</ListTableSelect>
```

**Bulk Actions:**
```javascript
methods: {
  async bulkDelete() {
    if (!this.selectedItems.length) return
    
    try {
      await Promise.all(
        this.selectedItems.map(item => api.delete(item.id))
      )
      this.selectedItems = []
      this.fetchData()
    } catch (error) {
      console.error('Bulk delete error:', error)
    }
  }
}
```

---

## Cards

### MediaCard

**Content card with image/icon, title, description, and action button.**

```vue
<MediaCard
  :image="item.imageUrl"
  :title="item.title"
  :description="item.description"
  :button-text="$t('viewDetails')"
  :show-button="true"
  @click="onCardClick(item)"
/>
```

**Props:**
```javascript
{
  image: '',              // Image URL
  icon: null,            // Feather icon name (if no image)
  title: '',             // Card title
  description: '',       // Card description
  buttonText: '',        // Action button text
  showButton: true,      // Show/hide button
  variant: 'primary',    // Button variant
  disabled: false,       // Disable card
}
```

**Events:**
```javascript
@click="onCardClick"      // Card clicked
@button-click="onAction"  // Button clicked
```

---

### DynamicMediaCard

**Auto-switching between portrait/landscape layouts.**

```vue
<DynamicMediaCard
  :item="book"
  :title="book.title"
  :description="book.author"
  :image="book.coverUrl"
  orientation="portrait"
/>
```

**Orientations:**
- `portrait` — Vertical layout (books, posters)
- `landscape` — Horizontal layout (videos, wide images)

---

## Progress Bars

### ProgressBarHorizontal

**Horizontal progress bar with percentage.**

```vue
<ProgressBarHorizontal
  :percentage="75"
  :show-label="true"
  variant="success"
  height="20px"
/>
```

**Props:**
```javascript
{
  percentage: 0,          // Progress value (0-100)
  showLabel: true,        // Show percentage text
  variant: 'primary',     // Bootstrap variant
  height: '15px',         // Bar height
  animated: false,        // Animated stripe effect
  striped: false,         // Striped pattern
}
```

---

### CircularProgressBar

**Circular progress indicator.**

```vue
<CircularProgressBar
  :percentage="85"
  :size="100"
  :stroke-width="10"
  color="#28c76f"
/>
```

---

### RainbowProgressBar

**Multi-segment colored progress bar.**

```vue
<RainbowProgressBar
  :segments="[
    { percentage: 30, color: '#28c76f', label: 'Excellent' },
    { percentage: 50, color: '#ff9f43', label: 'Good' },
    { percentage: 20, color: '#ea5455', label: 'Needs Improvement' },
  ]"
/>
```

---

## Charts

### BarChart

**Vertical/horizontal bar charts with ApexCharts.**

```vue
<BarChart
  :data="chartData"
  :categories="chartCategories"
  :colors="['#28c76f', '#00cfe8', '#ff9f43']"
  height="350"
  :horizontal="false"
/>
```

**Data Format:**
```javascript
chartData: [
  { name: 'Series 1', data: [30, 40, 35, 50, 49, 60] },
],
chartCategories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
```

---

### LineChart

**Line/area charts for trends.**

```vue
<LineChart
  :series="seriesData"
  :categories="months"
  :show-grid="true"
  :show-legend="true"
/>
```

---

### RadialBar

**Circular progress (single or multiple values).**

```vue
<RadialBar
  :value="75"
  label="Completion"
  color="#7367f0"
/>

<!-- Multiple values -->
<RadialBar
  :values="[75, 60, 85]"
  :labels="['Math', 'Science', 'History']"
/>
```

---

## Badges & Status

### BadgeStatus

**Status indicator badge.**

```vue
<BadgeStatus
  :status="item.status"
  :status-map="{
    active: { variant: 'success', text: 'Active' },
    inactive: { variant: 'secondary', text: 'Inactive' },
    pending: { variant: 'warning', text: 'Pending' },
  }"
/>
```

---

### ConditionalValueDisplay

**Show value or default message.**

```vue
<ConditionalValueDisplay
  :value="item.score"
  :show-condition="item.score !== null"
  default-message="N/A"
  :format="value => `${value}%`"
/>
```

---

## Forms

### EFormCheck

**Styled checkbox with custom labels.**

```vue
<EFormCheck
  v-model="accepted"
  label="I accept the terms"
  :disabled="false"
  variant="primary"
/>
```

---

### ButtonWaitAction

**Button with loading state and action cooldown.**

```vue
<ButtonWaitAction
  :loading="isSubmitting"
  :disabled="!canSubmit"
  variant="primary"
  @click="onSubmit"
>
  Submit Form
</ButtonWaitAction>
```

---

## Tabs

### Tab / Tabs

**Tabbed navigation component.**

```vue
<Tabs v-model="activeTab">
  <Tab title="General" icon="settings">
    <!-- General content -->
  </Tab>
  
  <Tab title="Security" icon="lock">
    <!-- Security content -->
  </Tab>
</Tabs>
```

---

### TabRouter

**Tabs with Vue Router integration.**

```vue
<TabRouter
  :tabs="[
    { title: 'Dashboard', route: '/dashboard', icon: 'home' },
    { title: 'Reports', route: '/reports', icon: 'file-text' },
  ]"
/>
```

---

## Common Patterns

### Paginated Select with API

```vue
<template>
  <ESelect
    v-model="selected"
    :options="options"
    :paginated="true"
    :page="page"
    :total-pages="totalPages"
    :loading="loading"
    label="name"
    searchable
    @nextPage="loadMore"
  />
</template>

<script>
export default {
  data() {
    return {
      selected: null,
      options: [],
      page: 1,
      totalPages: 1,
      loading: false,
    }
  },
  
  methods: {
    async loadMore({ search, page }) {
      if (page > this.totalPages || this.loading) return
      
      this.loading = true
      try {
        const response = await api.getOptions({ page, search })
        this.options.push(...response.data.items)
        this.totalPages = response.data.totalPages
        this.page = page
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
```

---

### Table with Export

```vue
<ListTable
  :table-columns="columns"
  :data-table="data"
  :loading="loading"
  :per-page="perPage"
  :total-items="totalItems"
  :show-export-excel="true"
  excel-file-name="report"
  :excel-title="$t('reportTitle')"
  @change="onTableChange"
/>
```

---

### Responsive Cards Grid

```vue
<b-row>
  <b-col
    v-for="item in items"
    :key="item.id"
    cols="12"
    sm="6"
    md="4"
    lg="3"
  >
    <MediaCard
      :title="item.title"
      :image="item.image"
      @click="onItemClick(item)"
    />
  </b-col>
</b-row>
```

---

## Component Don'ts

❌ **DON'T:**
- Use `v-select` or native `<select>`
- Use `<b-table>` directly (use ListTable)
- Fetch all data for client-side tables with >1000 records
- Create custom select components
- Copy-paste table markup (use components)

✅ **DO:**
- Always use `ESelect` for dropdowns
- Choose correct table component (server vs client pagination)
- Use slots for custom column rendering
- Integrate with `useFilters()` when needed
- Follow component prop patterns
