---
description: 
globs: *.vue
alwaysApply: false
---
# PrimeVue Components

This project uses PrimeVue for user interface components. It's a comprehensive Vue 3 component library with built-in accessibility support, themes, and Tailwind CSS integration.

## Component Usage

Import components directly from the PrimeVue package:

```vue
<script setup>
import Button from "primevue/button";
import MultiSelect from "primevue/multiselect";
import Password from "primevue/password";
import Calendar from "primevue/calendar";
import InputText from "primevue/inputtext";
import Dropdown from "primevue/dropdown";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
</script>
```

## PrimeIcons Usage

PrimeIcons is the official icon library for PrimeVue components. It provides over 250+ icons that integrate seamlessly with PrimeVue components.

### Basic Icon Usage

Use icons with the `pi` class prefix followed by the icon name:

```vue
<template>
  <!-- Basic icon usage -->
  <i class="pi pi-check"></i>
  <i class="pi pi-times"></i>
  <i class="pi pi-user"></i>
  <i class="pi pi-home"></i>
  
  <!-- Icons with custom styling -->
  <i class="pi pi-star text-yellow-500 text-2xl"></i>
  <i class="pi pi-heart text-red-500"></i>
</template>
```

### Icons in PrimeVue Components

PrimeVue components have built-in support for PrimeIcons:

```vue
<template>
  <!-- Button with icons -->
  <Button label="Save" icon="pi pi-check" />
  <Button label="Delete" icon="pi pi-trash" severity="danger" />
  <Button icon="pi pi-search" aria-label="Search" />
  
  <!-- Input with icons -->
  <InputGroup>
    <InputGroupAddon>
      <i class="pi pi-user"></i>
    </InputGroupAddon>
    <InputText placeholder="Username" />
  </InputGroup>
  
  <!-- Menu items with icons -->
  <Menu :model="items" />
</template>

<script setup>
const items = ref([
  {
    label: 'New',
    icon: 'pi pi-plus',
    command: () => { /* action */ }
  },
  {
    label: 'Open',
    icon: 'pi pi-folder-open',
    command: () => { /* action */ }
  },
  {
    label: 'Save',
    icon: 'pi pi-save',
    command: () => { /* action */ }
  }
]);
</script>
```

### Icon Categories and Examples

#### Navigation Icons
```vue
<template>
  <i class="pi pi-home"></i>          <!-- Home -->
  <i class="pi pi-arrow-left"></i>    <!-- Back -->
  <i class="pi pi-arrow-right"></i>   <!-- Forward -->
  <i class="pi pi-chevron-up"></i>    <!-- Up -->
  <i class="pi pi-chevron-down"></i>  <!-- Down -->
  <i class="pi pi-bars"></i>          <!-- Menu -->
</template>
```

#### Action Icons
```vue
<template>
  <i class="pi pi-plus"></i>          <!-- Add -->
  <i class="pi pi-minus"></i>         <!-- Remove -->
  <i class="pi pi-pencil"></i>        <!-- Edit -->
  <i class="pi pi-trash"></i>         <!-- Delete -->
  <i class="pi pi-save"></i>          <!-- Save -->
  <i class="pi pi-copy"></i>          <!-- Copy -->
  <i class="pi pi-download"></i>      <!-- Download -->
  <i class="pi pi-upload"></i>        <!-- Upload -->
</template>
```

#### Status Icons
```vue
<template>
  <i class="pi pi-check"></i>         <!-- Success -->
  <i class="pi pi-times"></i>         <!-- Error -->
  <i class="pi pi-exclamation-triangle"></i> <!-- Warning -->
  <i class="pi pi-info-circle"></i>   <!-- Info -->
  <i class="pi pi-spinner pi-spin"></i> <!-- Loading -->
</template>
```

#### User Interface Icons
```vue
<template>
  <i class="pi pi-user"></i>          <!-- User -->
  <i class="pi pi-users"></i>         <!-- Users -->
  <i class="pi pi-cog"></i>           <!-- Settings -->
  <i class="pi pi-search"></i>        <!-- Search -->
  <i class="pi pi-filter"></i>        <!-- Filter -->
  <i class="pi pi-sort"></i>          <!-- Sort -->
  <i class="pi pi-calendar"></i>      <!-- Calendar -->
  <i class="pi pi-clock"></i>         <!-- Time -->
</template>
```

#### Communication Icons
```vue
<template>
  <i class="pi pi-envelope"></i>      <!-- Email -->
  <i class="pi pi-phone"></i>         <!-- Phone -->
  <i class="pi pi-comment"></i>       <!-- Comment -->
  <i class="pi pi-comments"></i>      <!-- Comments -->
  <i class="pi pi-bell"></i>          <!-- Notification -->
</template>
```

### Icon Sizing and Styling

Icons can be styled using CSS classes or inline styles:

```vue
<template>
  <!-- Size variations -->
  <i class="pi pi-star text-xs"></i>    <!-- Extra small -->
  <i class="pi pi-star text-sm"></i>    <!-- Small -->
  <i class="pi pi-star text-base"></i>  <!-- Base -->
  <i class="pi pi-star text-lg"></i>    <!-- Large -->
  <i class="pi pi-star text-xl"></i>    <!-- Extra large -->
  <i class="pi pi-star text-2xl"></i>   <!-- 2x large -->
  <i class="pi pi-star text-3xl"></i>   <!-- 3x large -->
  
  <!-- Color variations -->
  <i class="pi pi-heart text-red-500"></i>
  <i class="pi pi-check text-green-500"></i>
  <i class="pi pi-info text-blue-500"></i>
  <i class="pi pi-exclamation-triangle text-yellow-500"></i>
  
  <!-- Custom styling -->
  <i class="pi pi-star" style="font-size: 2rem; color: gold;"></i>
</template>
```


### Icon Buttons and Interactive Elements

Create icon-only buttons and interactive elements:

```vue
<template>
  <!-- Icon-only buttons -->
  <Button icon="pi pi-check" aria-label="Confirm" />
  <Button icon="pi pi-times" severity="danger" aria-label="Cancel" />
  <Button icon="pi pi-cog" severity="secondary" aria-label="Settings" />
  
  <!-- Toggle buttons with icons -->
  <ToggleButton 
    v-model="checked" 
    onIcon="pi pi-check" 
    offIcon="pi pi-times" 
  />
  
  <!-- Speed dial with icons -->
  <SpeedDial 
    :model="speedDialItems" 
    direction="up" 
    :transitionDelay="80"
    showIcon="pi pi-bars" 
    hideIcon="pi pi-times" 
  />
</template>

<script setup>
const checked = ref(false);
const speedDialItems = ref([
  {
    label: 'Add',
    icon: 'pi pi-plus',
    command: () => { /* action */ }
  },
  {
    label: 'Update',
    icon: 'pi pi-refresh',
    command: () => { /* action */ }
  },
  {
    label: 'Delete',
    icon: 'pi pi-trash',
    command: () => { /* action */ }
  }
]);
</script>
```

### Accessibility with Icons

Always provide proper accessibility attributes when using icons:

```vue
<template>
  <!-- Icon with aria-label -->
  <Button icon="pi pi-save" aria-label="Save document" />
  
  <!-- Icon with screen reader text -->
  <button>
    <i class="pi pi-download" aria-hidden="true"></i>
    <span class="sr-only">Download file</span>
  </button>
  
  <!-- Decorative icons -->
  <i class="pi pi-star" aria-hidden="true"></i>
  <span>Featured content</span>
</template>
```

### Complete Icon List

PrimeIcons includes 250+ icons. Some popular categories include:

- **Arrows**: pi-arrow-up, pi-arrow-down, pi-arrow-left, pi-arrow-right, pi-chevron-*
- **Actions**: pi-plus, pi-minus, pi-times, pi-check, pi-pencil, pi-trash, pi-save
- **Navigation**: pi-home, pi-bars, pi-th-large, pi-list, pi-search
- **Media**: pi-play, pi-pause, pi-stop, pi-volume-up, pi-volume-down
- **Files**: pi-file, pi-folder, pi-download, pi-upload, pi-copy
- **Communication**: pi-envelope, pi-phone, pi-comment, pi-share-alt
- **Status**: pi-info-circle, pi-exclamation-triangle, pi-check-circle, pi-times-circle
- **User**: pi-user, pi-users, pi-user-plus, pi-user-minus
- **Commerce**: pi-shopping-cart, pi-credit-card, pi-money-bill
- **Technology**: pi-wifi, pi-mobile, pi-desktop, pi-tablet

For a complete list of available icons, visit the [PrimeIcons documentation](mdc:https:/primevue.org/icons).

## Example Component Usage

### Basic Form Components

```vue
<template>
  <!-- Button with different variants -->
  <Button label="Primary Button" />
  <Button label="Secondary" severity="secondary" />
  <Button label="Success" severity="success" />
  <Button label="Danger" severity="danger" />
  <Button label="Outlined" outlined />
  
  <!-- Input Text -->
  <InputText v-model="value" placeholder="Enter text" />
  
  <!-- Password with toggle mask -->
  <Password v-model="password" :toggleMask="true" />
  
  <!-- Calendar/DatePicker -->
  <Calendar v-model="date" dateFormat="dd/mm/yy" />
</template>
```

### Selection Components

```vue
<template>
  <!-- Dropdown -->
  <Dropdown 
    v-model="selectedCity" 
    :options="cities" 
    optionLabel="name" 
    placeholder="Select a City"
    class="w-full md:w-56" 
  />
  
  <!-- MultiSelect -->
  <MultiSelect
    v-model="selectedCities"
    :options="cities"
    optionLabel="name"
    filter
    placeholder="Select Cities"
    :maxSelectedLabels="3"
    class="w-full md:w-80"
  />
</template>

<script setup>
const selectedCity = ref();
const selectedCities = ref();
const cities = ref([
  { name: "New York", code: "NY" },
  { name: "Rome", code: "RM" },
  { name: "London", code: "LDN" },
  { name: "Istanbul", code: "IST" },
  { name: "Paris", code: "PRS" },
]);
</script>
```

### Data Components

```vue
<template>
  <!-- DataTable -->
  <DataTable :value="products" tableStyle="min-width: 50rem">
    <Column field="code" header="Code"></Column>
    <Column field="name" header="Name"></Column>
    <Column field="category" header="Category"></Column>
    <Column field="quantity" header="Quantity"></Column>
  </DataTable>
</template>
```

### Navigation and Layout Components

```vue
<template>
  <!-- Card -->
  <Card style="width: 25rem">
    <template #title>Simple Card</template>
    <template #content>
      <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit.</p>
    </template>
  </Card>
  
  <!-- Panel -->
  <Panel header="Header">
    <p>Lorem ipsum dolor sit amet</p>
  </Panel>
  
  <!-- Accordion -->
  <Accordion :activeIndex="0">
    <AccordionTab header="Header I">
      <p>Lorem ipsum dolor sit amet</p>
    </AccordionTab>
    <AccordionTab header="Header II">
      <p>Sed ut perspiciatis unde omnis iste natus</p>
    </AccordionTab>
  </Accordion>
</template>
```

## Available Components

PrimeVue offers over 90 components divided into categories:

### Form Components
- **AutoComplete** - autocomplete field
- **Calendar** - date picker
- **Checkbox** - checkbox field
- **Chips** - tag input
- **ColorPicker** - color selector
- **Dropdown** - dropdown list
- **Editor** - rich text editor
- **InputGroup** - field grouping
- **InputMask** - masked field
- **InputNumber** - numeric field
- **InputOtp** - OTP field
- **InputSwitch** - switch
- **InputText** - text field
- **Knob** - knob control
- **Listbox** - selection list
- **MultiSelect** - multiple selection
- **Password** - password field
- **RadioButton** - radio button
- **Rating** - star rating
- **SelectButton** - selection buttons
- **Slider** - slider
- **Textarea** - multiline text field
- **ToggleButton** - toggle button
- **TreeSelect** - tree selection

### Data Components
- **DataTable** - data table
- **DataView** - data view
- **OrderList** - sortable list
- **OrganizationChart** - organization chart
- **Paginator** - pagination
- **PickList** - pick list
- **Tree** - tree
- **TreeTable** - tree table
- **Timeline** - timeline
- **VirtualScroller** - virtual scrolling

### Panel Components
- **Accordion** - accordion
- **Card** - card
- **DeferredContent** - deferred content
- **Divider** - divider
- **Fieldset** - fieldset
- **Panel** - panel
- **ScrollPanel** - scroll panel
- **Splitter** - splitter
- **Stepper** - stepper
- **TabView** - tabs
- **Toolbar** - toolbar

### Overlay Components
- **ConfirmDialog** - confirmation dialog
- **ConfirmPopup** - confirmation popup
- **Dialog** - dialog
- **DynamicDialog** - dynamic dialog
- **OverlayPanel** - overlay panel
- **Sidebar** - sidebar
- **Tooltip** - tooltip

### File Components
- **FileUpload** - file upload

### Menu Components
- **Breadcrumb** - breadcrumb navigation
- **ContextMenu** - context menu
- **Dock** - dock
- **Menu** - menu
- **Menubar** - menu bar
- **MegaMenu** - mega menu
- **PanelMenu** - panel menu
- **Steps** - steps
- **TabMenu** - tab menu
- **TieredMenu** - tiered menu

### Message Components
- **Message** - message
- **InlineMessage** - inline message
- **Toast** - toast notification

### Media Components
- **Carousel** - carousel
- **Galleria** - gallery
- **Image** - image

### Misc Components
- **Avatar** - avatar
- **AvatarGroup** - avatar group
- **Badge** - badge
- **BlockUI** - block UI
- **Chip** - chip
- **Inplace** - in-place editing
- **MeterGroup** - meter group
- **ProgressBar** - progress bar
- **ProgressSpinner** - progress spinner
- **ScrollTop** - scroll to top
- **Skeleton** - loading skeleton
- **Tag** - tag
- **Terminal** - terminal

## Component Styling

### Using Tailwind Classes

PrimeVue components can be styled using Tailwind CSS classes:

```vue
<template>
  <Button 
    label="Styled Button" 
    class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
  />
  
  <InputText 
    v-model="value" 
    class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
  />
</template>
```

### PassThrough API

For advanced styling, use the PassThrough API:

```vue
<script setup>
const ptOptions = {
  root: { class: 'custom-button-root' },
  label: { class: 'custom-button-label' }
};
</script>

<template>
  <Button label="Custom Button" :pt="ptOptions" />
</template>
```

## Accessibility

PrimeVue components comply with WCAG 2.1 AA standards:

```vue
<template>
  <!-- Automatic ARIA labels -->
  <InputText 
    v-model="username" 
    aria-label="Username"
    placeholder="Enter username"
  />
  
  <!-- Keyboard navigation -->
  <DataTable :value="products" :tabindex="0">
    <Column field="name" header="Name"></Column>
  </DataTable>
</template>
```

## Form Validation

Integration with validation libraries:

```vue
<script setup>
import { useField, useForm } from 'vee-validate';
import * as yup from 'yup';

const schema = yup.object({
  email: yup.string().email().required(),
  password: yup.string().min(6).required(),
});

const { handleSubmit } = useForm({ validationSchema: schema });
const { value: email, errorMessage: emailError } = useField('email');
const { value: password, errorMessage: passwordError } = useField('password');
</script>

<template>
  <form @submit="handleSubmit">
    <InputText 
      v-model="email" 
      :class="{ 'p-invalid': emailError }"
      placeholder="Email"
    />
    <small class="p-error">{{ emailError }}</small>
    
    <Password 
      v-model="password" 
      :class="{ 'p-invalid': passwordError }"
      placeholder="Password"
    />
    <small class="p-error">{{ passwordError }}</small>
    
    <Button type="submit" label="Submit" />
  </form>
</template>
```

## Responsiveness

PrimeVue components are responsive by default, but can be further customized:

```vue
<template>
  <!-- Responsive columns in DataTable -->
  <DataTable :value="products" responsiveLayout="scroll">
    <Column field="code" header="Code" class="min-w-12rem"></Column>
    <Column field="name" header="Name" class="min-w-16rem"></Column>
  </DataTable>
  
  <!-- Responsive sizes -->
  <MultiSelect 
    v-model="selectedCities"
    :options="cities"
    class="w-full md:w-80"
  />
</template>
```
