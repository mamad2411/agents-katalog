---
name: "vant-ui-skills"
description: "Vant UI Skills Library - A comprehensive skill library for AI agents to understand and utilize Vant UI components. Invoke when user needs to work with Vant mobile components, theming, i18n, or mobile-first design patterns."
metadata:
author: jiaiyan
version: "1.0.0"
---

# Vant Skills Library

A comprehensive skill library for Vant UI framework, designed for AI agents to understand and utilize Vant mobile components effectively.

## When to Invoke

Invoke this skill when:

- User needs to implement any Vant component
- User asks about Vant configuration or setup
- User wants to customize themes for mobile apps
- User needs internationalization (i18n) support
- User asks about mobile-first design patterns
- User encounters issues with Vant components
- User is building mobile web applications or hybrid apps

## Skill Library Overview

Vant is a lightweight, reliable mobile component library. This library contains **102 skills** organized into the following categories:

| Category              | Count | Description                     | Path Pattern                        |
| --------------------- | ----- | ------------------------------- | ----------------------------------- |
| Basic Components      | 10    | Essential UI components         | `./components/van-{name}/SKILL.md`  |
| Form Components       | 19    | Form input and validation       | `./components/van-{name}/SKILL.md`  |
| Action Components     | 12    | User interaction components     | `./components/van-{name}/SKILL.md`  |
| Display Components    | 26    | Data display components         | `./components/van-{name}/SKILL.md`  |
| Navigation Components | 10    | Navigation and routing          | `./components/van-{name}/SKILL.md`  |
| Business Components   | 9     | Business-specific components    | `./components/van-{name}/SKILL.md`  |
| Composables           | 11    | Vue 3 composition API utilities | `./composables/use-{name}/SKILL.md` |
| Foundation Skills     | 5     | Core setup and configuration    | `./vant-{name}/SKILL.md`            |

## How to Locate Skills

### 1. Component Skills (86 skills)

All component skills follow the naming convention `van-{component-name}` and are located in the `components/` directory.

**Path Pattern:**

```
./components/van-{component-name}/SKILL.md
```

**Examples:**

- Button: `./components/van-button/SKILL.md`
- Form: `./components/van-form/SKILL.md`
- List: `./components/van-list/SKILL.md`
- Popup: `./components/van-popup/SKILL.md`

### 2. Composables Skills (11 skills)

Composables provide Vue 3 composition API utilities for common mobile patterns.

**Path Pattern:**

```
./composables/use-{name}/SKILL.md
```

**Examples:**

- useCountDown: `./composables/use-count-down/SKILL.md`
- useLazyRender: `./composables/use-lazy-render/SKILL.md`
- useRect: `./composables/use-rect/SKILL.md`

### 3. Foundation Skills (6 skills)

Foundation skills cover core setup and configuration.

| Skill Name     | Path                             | Description                |
| -------------- | -------------------------------- | -------------------------- |
| Quickstart     | `./vant-quickstart/SKILL.md`     | Installation and setup     |
| Theming        | `./vant-theming/SKILL.md`        | Theme customization        |
| i18n           | `./vant-i18n/SKILL.md`           | Internationalization       |
| Advanced Usage | `./vant-advanced-usage/SKILL.md` | Advanced patterns          |
| Components     | `./vant-components/SKILL.md`     | Component overview index   |
| Composables    | `./vant-composables/SKILL.md`    | Composables overview index |

## Skill Invocation Guide

### Step 1: Identify User Intent

Analyze the user's request to determine which skill category is needed:

| User Request Pattern           | Skill Category | Example Skill                        |
| ------------------------------ | -------------- | ------------------------------------ |
| "Create a button/form/list..." | Component      | `van-button`, `van-form`, `van-list` |
| "How to set up Vant"           | Foundation     | `vant-quickstart`                    |
| "Customize theme colors"       | Foundation     | `vant-theming`                       |
| "Add multi-language support"   | Foundation     | `vant-i18n`                          |
| "Use countdown timer"          | Composable     | `use-count-down`                     |
| "Implement lazy loading"       | Composable     | `use-lazy-render`                    |

### Step 2: Locate the Skill File

Use the path patterns above to locate the appropriate skill file:

```markdown
# For component skills
./components/van-{component-name}/SKILL.md

# For composables skills
./composables/use-{name}/SKILL.md

# For foundation skills
./vant-{name}/SKILL.md
```

### Step 3: Read and Apply Skill Content

Each skill file contains:

- **When to Invoke**: Specific conditions for using the skill
- **Features**: Component capabilities and options
- **API Reference**: Attributes, events, slots, exposes
- **Usage Examples**: Code snippets for common patterns
- **Best Practices**: Recommended implementation guidelines

## Component Skill Index

### Basic Components (10)

| Component      | Skill Path                                  | Description    |
| -------------- | ------------------------------------------- | -------------- |
| Button         | `./components/van-button/SKILL.md`          | Buttons        |
| Cell           | `./components/van-cell/SKILL.md`            | Cell items     |
| CellGroup      | `./components/van-cell-group/SKILL.md`      | Cell groups    |
| ConfigProvider | `./components/van-config-provider/SKILL.md` | Global config  |
| Icon           | `./components/van-icon/SKILL.md`            | Icons          |
| Image          | `./components/van-image/SKILL.md`           | Images         |
| Layout         | `./components/van-layout/SKILL.md`          | Layout system  |
| Popup          | `./components/van-popup/SKILL.md`           | Popup overlay  |
| Toast          | `./components/van-toast/SKILL.md`           | Toast messages |
| Transition     | `./components/van-transition/SKILL.md`      | Transitions    |

### Form Components (19)

| Component      | Skill Path                                  | Description         |
| -------------- | ------------------------------------------- | ------------------- |
| AddressEdit    | `./components/van-address-edit/SKILL.md`    | Address editor      |
| AddressList    | `./components/van-address-list/SKILL.md`    | Address list        |
| Area           | `./components/van-area/SKILL.md`            | Area picker         |
| Calendar       | `./components/van-calendar/SKILL.md`        | Calendar            |
| Cascader       | `./components/van-cascader/SKILL.md`        | Cascading selection |
| Checkbox       | `./components/van-checkbox/SKILL.md`        | Checkboxes          |
| ContactCard    | `./components/van-contact-card/SKILL.md`    | Contact card        |
| ContactEdit    | `./components/van-contact-edit/SKILL.md`    | Contact editor      |
| ContactList    | `./components/van-contact-list/SKILL.md`    | Contact list        |
| DatePicker     | `./components/van-date-picker/SKILL.md`     | Date picker         |
| Field          | `./components/van-field/SKILL.md`           | Input fields        |
| Form           | `./components/van-form/SKILL.md`            | Form management     |
| NumberKeyboard | `./components/van-number-keyboard/SKILL.md` | Number keyboard     |
| PasswordInput  | `./components/van-password-input/SKILL.md`  | Password input      |
| Picker         | `./components/van-picker/SKILL.md`          | Picker              |
| Radio          | `./components/van-radio/SKILL.md`           | Radio buttons       |
| Rate           | `./components/van-rate/SKILL.md`            | Star rating         |
| Search         | `./components/van-search/SKILL.md`          | Search bar          |
| Slider         | `./components/van-slider/SKILL.md`          | Slider              |
| Stepper        | `./components/van-stepper/SKILL.md`         | Stepper             |
| Switch         | `./components/van-switch/SKILL.md`          | Toggle switch       |
| TimePicker     | `./components/van-time-picker/SKILL.md`     | Time picker         |
| Uploader       | `./components/van-uploader/SKILL.md`        | File uploader       |

### Action Components (12)

| Component      | Skill Path                                  | Description       |
| -------------- | ------------------------------------------- | ----------------- |
| ActionSheet    | `./components/van-action-sheet/SKILL.md`    | Action sheet      |
| Dialog         | `./components/van-dialog/SKILL.md`          | Dialog modal      |
| DropdownMenu   | `./components/van-dropdown-menu/SKILL.md`   | Dropdown menu     |
| FloatingBubble | `./components/van-floating-bubble/SKILL.md` | Floating bubble   |
| FloatingPanel  | `./components/van-floating-panel/SKILL.md`  | Floating panel    |
| Loading        | `./components/van-loading/SKILL.md`         | Loading indicator |
| Notify         | `./components/van-notify/SKILL.md`          | Notification      |
| Overlay        | `./components/van-overlay/SKILL.md`         | Overlay           |
| PickerGroup    | `./components/van-picker-group/SKILL.md`    | Picker group      |
| PullRefresh    | `./components/van-pull-refresh/SKILL.md`    | Pull to refresh   |
| ShareSheet     | `./components/van-share-sheet/SKILL.md`     | Share sheet       |
| SwipeCell      | `./components/van-swipe-cell/SKILL.md`      | Swipe cell        |

### Display Components (26)

| Component     | Skill Path                                 | Description        |
| ------------- | ------------------------------------------ | ------------------ |
| Badge         | `./components/van-badge/SKILL.md`          | Badge              |
| Collapse      | `./components/van-collapse/SKILL.md`       | Collapse           |
| CountDown     | `./components/van-count-down/SKILL.md`     | Countdown          |
| Divider       | `./components/van-divider/SKILL.md`        | Divider            |
| Empty         | `./components/van-empty/SKILL.md`          | Empty state        |
| Grid          | `./components/van-grid/SKILL.md`           | Grid               |
| ImagePreview  | `./components/van-image-preview/SKILL.md`  | Image preview      |
| Lazyload      | `./components/van-lazyload/SKILL.md`       | Lazy loading       |
| List          | `./components/van-list/SKILL.md`           | Infinite list      |
| Loading       | `./components/van-loading/SKILL.md`        | Loading            |
| Marquee       | `./components/van-marquee/SKILL.md`        | Marquee            |
| NoticeBar     | `./components/van-notice-bar/SKILL.md`     | Notice bar         |
| Pagination    | `./components/van-pagination/SKILL.md`     | Pagination         |
| PasswordInput | `./components/van-password-input/SKILL.md` | Password input     |
| Picker        | `./components/van-picker/SKILL.md`         | Picker             |
| Progress      | `./components/van-progress/SKILL.md`       | Progress bar       |
| RollingText   | `./components/van-rolling-text/SKILL.md`   | Rolling text       |
| Skeleton      | `./components/van-skeleton/SKILL.md`       | Skeleton           |
| Slider        | `./components/van-slider/SKILL.md`         | Slider             |
| Step          | `./components/van-step/SKILL.md`           | Steps              |
| Sticky        | `./components/van-sticky/SKILL.md`         | Sticky positioning |
| Swipe         | `./components/van-swipe/SKILL.md`          | Swipe carousel     |
| Tag           | `./components/van-tag/SKILL.md`            | Tag                |
| TextEllipsis  | `./components/van-text-ellipsis/SKILL.md`  | Text ellipsis      |
| TreeSelect    | `./components/van-tree-select/SKILL.md`    | Tree select        |
| Watermark     | `./components/van-watermark/SKILL.md`      | Watermark          |

### Navigation Components (10)

| Component  | Skill Path                              | Description     |
| ---------- | --------------------------------------- | --------------- |
| BackTop    | `./components/van-back-top/SKILL.md`    | Back to top     |
| Grid       | `./components/van-grid/SKILL.md`        | Grid navigation |
| IndexBar   | `./components/van-index-bar/SKILL.md`   | Index bar       |
| NavBar     | `./components/van-nav-bar/SKILL.md`     | Navigation bar  |
| Pagination | `./components/van-pagination/SKILL.md`  | Pagination      |
| Sidebar    | `./components/van-sidebar/SKILL.md`     | Sidebar         |
| Tab        | `./components/van-tab/SKILL.md`         | Tabs            |
| Tabbar     | `./components/van-tabbar/SKILL.md`      | Tab bar         |
| TreeSelect | `./components/van-tree-select/SKILL.md` | Tree select     |

### Business Components (9)

| Component   | Skill Path                               | Description    |
| ----------- | ---------------------------------------- | -------------- |
| AddressEdit | `./components/van-address-edit/SKILL.md` | Address editor |
| AddressList | `./components/van-address-list/SKILL.md` | Address list   |
| Area        | `./components/van-area/SKILL.md`         | Area picker    |
| Card        | `./components/van-card/SKILL.md`         | Card           |
| ContactCard | `./components/van-contact-card/SKILL.md` | Contact card   |
| ContactEdit | `./components/van-contact-edit/SKILL.md` | Contact editor |
| ContactList | `./components/van-contact-list/SKILL.md` | Contact list   |
| Coupon      | `./components/van-coupon/SKILL.md`       | Coupon         |
| SubmitBar   | `./components/van-submit-bar/SKILL.md`   | Submit bar     |

## Composables Index (11)

| Composable          | Skill Path                                      | Description         |
| ------------------- | ----------------------------------------------- | ------------------- |
| useCountDown        | `./composables/use-count-down/SKILL.md`         | Countdown timer     |
| useCustomFieldValue | `./composables/use-custom-field-value/SKILL.md` | Custom field value  |
| useEventListener    | `./composables/use-event-listener/SKILL.md`     | Event listener      |
| useId               | `./composables/use-id/SKILL.md`                 | Unique ID generator |
| useLazyRender       | `./composables/use-lazy-render/SKILL.md`        | Lazy rendering      |
| usePageVisibility   | `./composables/use-page-visibility/SKILL.md`    | Page visibility     |
| useRect             | `./composables/use-rect/SKILL.md`               | Element rect        |
| useRelation         | `./composables/use-relation/SKILL.md`           | Component relation  |
| useResetState       | `./composables/use-reset-state/SKILL.md`        | Reset state         |
| useRtl              | `./composables/use-rtl/SKILL.md`                | RTL support         |
| useWindowSize       | `./composables/use-window-size/SKILL.md`        | Window size         |

## Usage Examples

### Example 1: User asks about button implementation

**User Request:** "How do I create a primary button with loading state?"

**Agent Action:**

1. Identify intent: Component skill - Button
2. Locate skill: `./components/van-button/SKILL.md`
3. Read skill content
4. Provide response with API reference and code example

**Response:**

```vue
<template>
  <van-button type="primary" :loading="loading" @click="handleClick">
    {{ loading ? 'Loading...' : 'Submit' }}
  </van-button>
</template>

<script setup>
import { ref } from 'vue'

const loading = ref(false)

const handleClick = async () => {
  loading.value = true
  try {
    await submitData()
  } finally {
    loading.value = false
  }
}
</script>
```

### Example 2: User asks about form validation

**User Request:** "How do I create a form with validation?"

**Agent Action:**

1. Identify intent: Component skill - Form
2. Locate skill: `./components/van-form/SKILL.md`
3. Read skill content
4. Provide response with validation example

**Response:**

```vue
<template>
  <van-form @submit="onSubmit">
    <van-field
      v-model="username"
      name="username"
      label="Username"
      placeholder="Username"
      :rules="[{ required: true, message: 'Please input username' }]"
    />
    <van-field
      v-model="password"
      type="password"
      name="password"
      label="Password"
      placeholder="Password"
      :rules="[{ required: true, message: 'Please input password' }]"
    />
    <div style="margin: 16px;">
      <van-button round block type="primary" native-type="submit">
        Submit
      </van-button>
    </div>
  </van-form>
</template>

<script setup>
import { ref } from 'vue'

const username = ref('')
const password = ref('')

const onSubmit = (values) => {
  console.log('submit', values)
}
</script>
```

### Example 3: User asks about infinite list

**User Request:** "How do I implement an infinite scroll list?"

**Agent Action:**

1. Identify intent: Component skill - List
2. Locate skill: `./components/van-list/SKILL.md`
3. Read skill content
4. Provide response with list example

**Response:**

```vue
<template>
  <van-list
    v-model:loading="loading"
    :finished="finished"
    finished-text="No more data"
    @load="onLoad"
  >
    <van-cell v-for="item in list" :key="item" :title="item" />
  </van-list>
</template>

<script setup>
import { ref } from 'vue'

const list = ref([])
const loading = ref(false)
const finished = ref(false)

const onLoad = () => {
  setTimeout(() => {
    for (let i = 0; i < 10; i++) {
      list.value.push(list.value.length + 1)
    }
    loading.value = false
    
    if (list.value.length >= 40) {
      finished.value = true
    }
  }, 1000)
}
</script>
```

### Example 4: User asks about countdown timer

**User Request:** "How do I implement a countdown timer?"

**Agent Action:**

1. Identify intent: Composable skill - useCountDown
2. Locate skill: `./composables/use-count-down/SKILL.md`
3. Read skill content
4. Provide response with composable example

**Response:**

```vue
<template>
  <van-count-down :time="time" />
</template>

<script setup>
import { useCountDown } from '@vant/use'

const countDown = useCountDown({
  time: 24 * 60 * 60 * 1000,
  autostart: true,
})

const time = countDown.current
</script>
```

### Example 5: User asks about theme customization

**User Request:** "How do I customize Vant theme colors?"

**Agent Action:**

1. Identify intent: Foundation skill - Theming
2. Locate skill: `./vant-theming/SKILL.md`
3. Read skill content
4. Provide response with CSS variables example

**Response:**

```css
:root {
  --van-primary-color: #1989fa;
  --van-success-color: #07c160;
  --van-danger-color: #ee0a24;
  --van-warning-color: #ff976a;
  --van-info-color: #1989fa;
}
```

## Configuration Requirements

### Prerequisites

Before using this skill library, ensure:

1. **Vue 3.3+** is installed
2. **Vant 4+** is installed
3. **Node.js 18+** for development

### Installation

```bash
npm install vant
```

### TypeScript Support

Add to `tsconfig.json`:

```json
{
  "compilerOptions": {
    "types": ["vant/global"]
  }
}
```

### Import Styles

```javascript
import 'vant/lib/index.css'
```

### On-Demand Import (Recommended)

```javascript
import { Button, Cell, Form } from 'vant'
```

## Input Parameters

When invoking skills, consider these parameters:

| Parameter | Type   | Description                                             | Required |
| --------- | ------ | ------------------------------------------------------- | -------- |
| component | string | Component name (e.g., "button", "form")                 | Yes      |
| feature   | string | Specific feature needed (e.g., "validation", "loading") | No       |
| context   | object | Additional context (framework, TypeScript usage)        | No       |

## Output Format

Each skill provides:

1. **API Reference**: Complete attributes, events, slots, exposes
2. **Code Examples**: Working code snippets
3. **Best Practices**: Recommended implementation patterns
4. **Common Issues**: Troubleshooting tips
5. **Component Interactions**: How to use with other components

## Important Notes

### 1. Skill Priority

When multiple skills could apply, prioritize in this order:

1. Component-specific skills (most specific)
2. Composable skills (composition API utilities)
3. Foundation skills (configuration)

### 2. Cross-References

Many skills reference related skills. Always check:

- Related components in the same category
- Foundation skills for configuration
- Composables for common patterns

### 3. Version Compatibility

This skill library is based on Vant 4+. Some features may not be available in earlier versions.

### 4. Naming Conventions

- Component skills use `van-{name}` format (matches Vue component tags)
- Composables use `use-{name}` format (matches Vue composition API naming)
- Foundation skills use `vant-{name}` format

### 5. File Structure

```
vant-skills/
├── SKILL.md                          # This file (main entry)
├── README.md                         # English documentation
├── README_CN.md                      # Chinese documentation
├── AGENTS.md                         # Agents documentation
├── components/                       # 86 component skills
│   ├── van-button/
│   │   └── SKILL.md
│   ├── van-form/
│   │   └── SKILL.md
│   └── ...
├── composables/                      # 11 composable skills
│   ├── use-count-down/
│   │   └── SKILL.md
│   ├── use-lazy-render/
│   │   └── SKILL.md
│   └── ...
├── vant-quickstart/                  # Foundation skills
├── vant-theming/
├── vant-i18n/
├── vant-advanced-usage/
└── vant-components/
```

### 6. Mobile-First Design

Vant is designed for mobile devices. Key considerations:

- Touch-friendly interactions
- Responsive layouts
- Performance optimization for mobile
- Native-like UI patterns

## Best Practices for Agents

1. **Always start with this file** when user mentions Vant
2. **Locate the specific skill** based on user intent
3. **Read the complete skill file** before responding
4. **Provide code examples** from the skill documentation
5. **Reference related skills** when applicable
6. **Include best practices** from the skill content
7. **Mention common issues** if relevant to user's context
8. **Consider mobile-first patterns** in all recommendations

## Related Resources

- [Vant Documentation](https://vant-ui.github.io/vant/)
- [Vue 3 Documentation](https://vuejs.org/)
- [Vant GitHub](https://github.com/youzan/vant)
- [Vant Icons](https://vant-ui.github.io/vant/#/en-US/icon)

