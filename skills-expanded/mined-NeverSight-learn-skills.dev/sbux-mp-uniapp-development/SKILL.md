---
name: sbux-mp-uniapp-development-skill
description: Complete development guide for UniApp WeChat mini-program project, covering tech stack, naming conventions, directory structure, page/component/composable development, routing, service layer, state management, tracking, monitoring, build and deployment. Use when developing pages, components, composables, services, stores, or any feature in this UniApp mini-program project.
---

# UniApp Mini-Program Development Guide

## Quick Command Reference

Load the corresponding command workflow or reference file based on the development scenario:

| Command | Scenario / Intent | Read File |
|---------|-------------------|-----------|
| `/page` | Create new page, page Vue patterns, lifecycle management | [commands/page.md](commands/page.md) |
| `/component` | Create new component, dialog components, complex component splitting | [commands/component.md](commands/component.md) |
| `/composable` | Write main/sub composable, watch management | [commands/composable.md](commands/composable.md) |
| `/service` | Create new service domain, API integration, request config | [commands/service.md](commands/service.md) |
| `/store` | Define/use Store, defineStore | [commands/store.md](commands/store.md) |
| `/deploy` | Build & deploy, CI/CD, environment variables | [commands/deploy.md](commands/deploy.md) |
| `/monitor` | Monitoring & reporting, Tingyun SDK, exception capture | [commands/monitor.md](commands/monitor.md) |
| `/use-sbux-mp` | End-to-end business feature development (full spec) | [commands/use-sbux-mp.md](commands/use-sbux-mp.md) |

**Detailed Reference Docs** (in-depth content from command workflows):

| Topic | Read File |
|-------|-----------|
| Composable full architecture, watch conventions | [reference/composables.md](reference/composables.md) |
| Component full patterns, dialog/container components | [reference/component.md](reference/component.md) |
| Service layer directory, request config, multi-channel routing | [reference/services.md](reference/services.md) |
| Store full usage, read/write examples | [reference/store.md](reference/store.md) |
| Transaction Store (cart/store/transaction aggregate) | [reference/transaction-store.md](reference/transaction-store.md) |
| SharedCache cross-page shared cache | [reference/shared-cache.md](reference/shared-cache.md) |
| Dialog Composables (Alert/Slide/Prompt) | [reference/dialog.md](reference/dialog.md) |
| Static asset management, imgUrl usage | [reference/static-assets.md](reference/static-assets.md) |
| CI/CD pipeline, GitHub Actions | [reference/deployment.md](reference/deployment.md) |
| Tingyun SDK API, business monitoring hooks | [reference/monitor.md](reference/monitor.md) |
| Complete code examples | [examples.md](examples.md) |

**Usage**:
- When the user mentions a specific development task, first read the corresponding `commands/xxx.md` for step-by-step workflow
- When more detailed specs are needed, read the corresponding `reference/xxx.md`
- When no specific scenario is mentioned, the summary in SKILL.md is sufficient

---

## 0. Tech Stack

| Category | Technology |
|----------|------------|
| Framework | UniApp 2.0.2 + Vue 2.6.10 + Composition API (@vue/composition-api) |
| Build | Vue CLI 4.x + Webpack |
| Package Manager | pnpm + Node.js 18 |
| Code Standards | ESLint 6.8.0 + Prettier 2.8.8 + Husky pre-commit |
| State Management | Vuex 3.2.0 + Pinia 2.1.7 |
| Testing | Jest + @vue/test-utils + @vue/cli-plugin-unit-jest |
| Styling | Less |
| Mini-Program Lifecycle | @dcloudio/uni-app |
| Environment Variables | `UNI_PLATFORM` (platform), `NODE_CUSTOM_ENV` (environment) |
| Memory Optimization | `NODE_OPTIONS="--max-old-space-size=4096"` |

---

## 1. Naming Conventions

All files and directories use **camelCase**. Hooks use **use + PascalCase**.

| Type | Convention | Example |
|------|-----------|---------|
| Directory | camelCase | `userInfo/`, `orderDetail/` |
| Page | camelCase | `orderDetail.vue` |
| Hook | use + PascalCase | `useOrderDetail.js` |
| Service | camelCase | `orderService.js` |
| Store | camelCase | `useMainStore.js` |
| Component Directory | camelCase | `productCard/index.vue` |
| Platform-specific File | name.platform.js | `payment.weixin.js` |
| Track File | camelCase | `srkitDetail.js` |

### Hook Naming Subtypes

- Page Hook: `use[PageName].js`
- Component Hook: `use[ComponentName].js`
- General Hook: `use[FeatureDescription].js`

### Platform-specific Files

- WeChat: `xxx.weixin.js` | Alipay: `xxx.alipay.js` | Douyin: `xxx.douyin.js` | H5: `xxx.h5.js`

### Store Naming

- Business Store: `use[BusinessName]Store.js` (e.g., `useMainStore.js`, `useOrderStore.js`)
- Mutation Constants: `UPDATE_[ACTION_NAME]` (internal use only, not exported)

---

## 2. Directory Structure

### Page Directory

```bash
pages/
└── pay/                       # Page directory
    ├── index.vue              # Page component
    ├── usePay.js              # Main composable (manages lifecycle)
    └── composables/           # Sub-composables (pure logic, no lifecycle)
        ├── useOrder.js
        ├── usePayMethod.js
        └── usePayTrack.js
```

### Legacy Page Refactoring

Create a same-name directory at the same level, gradually extract logic to the new directory, keep the old `.vue` file unchanged:

```bash
pages/
├── orderDetail.vue              # Old page (keep unchanged)
└── orderDetail/                 # New directory
    ├── composables/
    └── useOrderDetail.js
```

### Component Directory

```bash
components/
├── cardItem/                    # Simple component → index.vue
├── orderDetailPanel/           # Complex component → index.vue + useOrderDetailPanel.js
└── svcPay/                      # Component group → payMent.vue, payPop.vue, paySuccess.vue
```

**Organization Principles**:
- All components use directory form, main component named `index.vue`
- Simple component: only `index.vue`
- Complex component: `index.vue` + `use[ComponentName].js`
- Component group: multiple related sub-components in the same directory, each with independent naming
- Global shared components in `common/components/`, package components in the package's `components/`

### Service Layer Directory

```bash
src/services/
├── index.js              # Unified export entry
├── user/                 # User domain
│   ├── index.js          # Service methods
│   ├── api.js            # API definitions
│   ├── user.weixin.js    # WeChat platform implementation
│   └── user.h5.js        # H5 platform implementation
├── order/
├── payment/              # Multi-channel scenario
└── map/                  # Multi-channel map
```

### Track Directory

```bash
[packageName]/track/
├── index.js              # Export entry
├── srkitList.js          # Split by page
└── srkitDetail.js
```

---

## 3. Page Development

### Vue File Patterns

**`<script setup>` (recommended, when no platform differences)**:

```vue
<template>
  <view class="order-detail">
    <order-header :info="orderInfo" />
  </view>
</template>

<script setup>
import { useOrderDetail } from './useOrderDetail';
const { orderInfo, fetchOrder } = useOrderDetail();
</script>
```

**Options `setup()` (required when `#ifdef` conditional compilation is used)**:

```vue
<script>
import { useOrderDetail } from './useOrderDetail';
// #ifdef H5
import H5Navigation from '../components/h5Header/index.vue';
// #endif

export default {
  components: {
    // #ifdef H5
    H5Navigation,
    // #endif
  },
  setup() {
    return useOrderDetail();
  }
};
</script>
```

### Lifecycle Management

**Core Principle: Main composable manages all lifecycles, sub-composables contain no lifecycles.**

```javascript
// usePay.js - Main composable
import { onLoad, onShow, onUnload, onPageScroll } from '@dcloudio/uni-app';

export function usePay() {
  onLoad((params) => { initPage(params); });
  onShow(() => { trackPageView(); });
  onPageScroll((e) => { handlePageScroll(e); });
  onUnload(() => { cleanup(); });

  // Import sub-composables (pure logic, no lifecycle)
  const { orderReviewData } = useOrder();
  const { selectedPayMethod } = usePayMethod();

  // Cross-composable watches only in main composable
  watch(selectedPayMethod, (newVal) => { trackPaymentToolAction(newVal); });

  return { orderReviewData, selectedPayMethod };
}
```

### Lifecycles Requiring Manual Declaration

In the Vue 2 + @vue/composition-api environment, some hooks need explicit empty method declarations in `.vue` files:

| Lifecycle | Manual Declaration Required | Notes |
|-----------|---------------------------|-------|
| `onLoad` | No | Auto-injected |
| `onShow` | No | Auto-injected |
| `onReady` | No | Auto-injected |
| `onHide` | No | Auto-injected by Babel |
| `onUnload` | No | Auto-injected by Babel |
| `onReachBottom` | **Yes** | Scroll-to-bottom loading |
| `onShareAppMessage` | **Yes** | Share functionality |
| `onPullDownRefresh` | **Yes** | Pull-to-refresh |
| `onPageScroll` | **Yes** | Page scroll |

```javascript
// Declare in Options setup()
export default {
  onReachBottom() {},
  onShareAppMessage() {},
  onPullDownRefresh() {},
  onPageScroll() {},
  setup() { return usePay(); }
};
```

---

## 4. Composable Development Essentials

> Full architecture and examples: [reference/composables.md](reference/composables.md)

### Main/Sub Layering Principle

| Layer | Location | Responsibility | Lifecycle |
|-------|----------|---------------|-----------|
| Main composable | `pages/[pageName]/use[PageName].js` | Manage lifecycle + coordinate sub-composables | Yes |
| Sub - Data layer | `composables/use[Feature]Data.js` | Data fetching and state management | No |
| Sub - Business layer | `composables/use[Feature]Logic.js` | Business logic processing | No |
| Sub - Utility layer | `composables/use[Feature].js` | Utility function encapsulation | No |
| Sub - Track layer | `composables/use[Feature]Track.js` | Tracking logic | No |
| Package shared | `[package]/composables/` | Multi-page shared logic within package | No |
| Global shared | `common/composables/` | Cross-package common logic | No |

### Key Constraints

1. **Sub-composables must not contain lifecycles** (onLoad, onShow, etc.)
2. **Cross-composable watches are managed only in the main composable**
3. **Sub-composables can depend on other sub-composables**, forming a dependency tree
4. **Named exports**: `export function useXxx() {}`, default exports are prohibited

---

## 5. Component Development Essentials

> Full patterns and examples: [reference/component.md](reference/component.md)

### Component Categories

| Type | Description | Examples |
|------|-------------|---------|
| Business logic components | Split by functional module | paymentList, orderType, address, submit |
| Interactive components | Popups/modals | SVCCardListPopup, PayMethodPopup, CompleteAddressDialog |
| Container components | Layout and style containers | addressAndOrderContain, scrollFloatButton |
| Option row components | Form item variants | optionRow/priceRow.vue, radioRow.vue, selectRow.vue |

### Best Practices

1. **Props passing**: Use props for data in complex pages, avoid over-reliance on global state
2. **Event communication**: Use `$emit` to pass events to parent, maintain unidirectional data flow
3. **Dialog components**: Support open/close methods, call via ref
4. **Image fallback**: Use `imgUrl` function for image paths
5. **Style isolation**: Use scoped styles

---

## 6. Route Navigation

Use route constants from `common/router.config`, avoid hardcoding paths.

### Route Constants

| Constant | Description | Example |
|----------|-------------|---------|
| MOD | MOD package routes | `MOD.menu`, `MOD.orderDetail` |
| MOP | MOP package routes | `MOP.menu`, `MOP.cart` |
| EC | EC package routes | `EC.ecHome` |
| USER | User package routes | `USER.memberCode`, `USER.login` |

### Navigation Methods

```javascript
import { navigateTo, redirectTo, switchTab, webviewTo } from 'common/utils/router.js';
import { MOD, MOP, USER } from 'common/router.config';

navigateTo({ url: MOD.menu });
navigateTo({ url: USER.memberCode });
navigateTo({ url: MOP.orderDetail, params: { orderId: '123' } });
webviewTo(termInfo.url);

// H5 DeepLink
// #ifdef H5
import { DeepLinkNavigate } from '@sbux/sbuxjs-jsbridge';
DeepLinkNavigate(`sbuxcn://h5-webview?url=${encodeURIComponent(url)}`);
// #endif
```

**Prohibited**: Hardcoded paths `navigateTo({ url: '/shares/mod/pages/menu' })`

---

## 7. Service Layer Essentials

> Full guide: [reference/services.md](reference/services.md)

### Responsibility Boundaries

**Only responsible for**: API requests + simple data transformation
**Prohibited**: Route navigation logic, complex business logic (should be in page hooks)

### Usage

```javascript
// Unified entry import (recommended)
import { userService, orderService } from 'services';

// Domain-level import
import { getUserInfo } from 'services/user';
```

### Steps to Create a New Domain Service

1. Create domain directory `src/services/[domain]/`
2. Create `api.js` to define interfaces
3. Create `index.js` to export service functions
4. Register in `src/services/index.js`: `export * as productService from './product'`

---

## 8. Store Usage Essentials

> Full usage: [reference/store.md](reference/store.md)

Currently in transition phase — Store data still comes from Vuex, syntax is only extended.

### Quick Start

```javascript
// Definition
import { defineStore } from './defineStore.js';
export const useMainStore = defineStore('main', ({ state, commit }) => {
  const riskInfo = computed(() => state.riskInfo.value);
  const setRiskInfo = (data) => commit('UPDATE_MAIN_RISKINFO', data);
  return { riskInfo, setRiskInfo };
});

// Usage
const mainStore = useMainStore();
mainStore.riskInfo.value;          // Read in JS (requires .value)
mainStore.setRiskInfo({ data });   // Modify (direct .value assignment is prohibited)
// <template> {{ riskInfo }}       // Template auto-unwraps, no .value needed
```

### Key Constraints

| Scenario | Pattern |
|----------|---------|
| Read value in JS | `mainStore.riskInfo.value` |
| Read value in template | `{{ riskInfo }}` (auto-unwrapped) |
| Modify state | `mainStore.setRiskInfo({ data: xxx })` |
| Watch | `watch(() => mainStore.riskInfo.value, ...)` |
| **Prohibited** | `mainStore.riskInfo.value = xxx` (direct assignment) |

---

## 8.5. SharedCache Quick Start

> Full API: [reference/shared-cache.md](reference/shared-cache.md)

Lightweight cross-page shared cache (lighter than Vuex, faster than Storage).

```javascript
import { defineCache } from 'common/sharedCache';
import { useCacheActions } from 'common/sharedCache';

// Define
export const useOrderCache = defineCache('order', () => ({ currentOrder: null, cartItems: [] }));

// Read/Write
const orderCache = useOrderCache();
orderCache.currentOrder = { id: 123 };  // Direct assignment
console.log(orderCache.currentOrder);    // Read

// watch + patch
const { watch, patch, reset } = useCacheActions(useOrderCache);
const unwatch = watch('currentOrder', (newVal) => { /* ... */ });
patch({ currentOrder: null });
reset();
```

**Note**: Call `unwatch()` on `onUnload` to avoid memory leaks; cache is not persistent and clears on restart.

---

## 8.6. Dialog Composables

> Full API: [reference/dialog.md](reference/dialog.md)

| Composable | Component | Usage |
|-----------|-----------|-------|
| `useAlertDialog` | `uni-alert` | Confirm/cancel dialogs (supports Promise) |
| `useSlideDialog` | `slide-dialog` | Information display dialogs (supports rich text) |
| `usePromptDialog` | `uni-prompt` | Multi-button selection dialogs |

```javascript
import { useAlertDialog } from 'common/composables/useAlertDialog.js';
const { alertState, showAlert, handleAlertConfirm, handleAlertCancel } = useAlertDialog();

// Callback mode
showAlert({ title: 'Delete Confirmation', onConfirm: () => { /* ... */ } });

// Promise mode
const confirmed = await showAlert({ title: 'Confirm Action', cancelEnable: true });
```

---

## 8.7. Transaction Store

> Full API: [reference/transaction-store.md](reference/transaction-store.md)

Core transaction stores, all imported from `common/stores/useTransactionStore.js`:

| Store | Responsibility |
|-------|---------------|
| `useCartStore` | Cart state (product list, coupons) |
| `useShopStore` | Store state (current store, reservation time) |
| `useTransactionStore` | Aggregate layer (baseOrder, strategy) |

```javascript
import { useCartStore, useShopStore } from 'common/stores/useTransactionStore.js';
const { shoppingCartDetail, cartMutations } = useCartStore(channel);
const { currentStore, shopMutations } = useShopStore(channel);
```

---

## 8.8. Static Assets

> Full spec: [reference/static-assets.md](reference/static-assets.md)

Image references must use the `imgUrl()` method:

```vue
<image :src="imgUrl('shares/public/images/mod/banner.png')" />
<image src="imgUrl('shares/common/icon.png')" />
```

Relative paths auto-prepend `/static/` prefix, full URLs remain unchanged. Only `imgUrl()` is supported, not `$imgUrl()`.

---

## 9. Tracking Development Essentials

### Naming Conventions

| Track Type | Naming Format | Example |
|-----------|--------------|---------|
| Page view | `trackPageView` | `trackPageView()` |
| Click event | `track[Element]Click` | `trackCouponClick()` |
| Exposure event | `track[Element]Expose` | `trackBannerExpose()` |
| Submit event | `track[Form]Submit` | `trackOrderSubmit()` |

### Design Principles

1. **Encapsulate as functions**: Tracking code goes in `track/` directory, not scattered in business logic
2. **Split by page**: Each page has its own track file
3. **Handle platform differences**: Use `#ifdef` inside track functions
4. **Call in hooks**: Business hooks import track functions and call them at appropriate times

```javascript
// track/srkitDetail.js
export function trackCouponClick(detailData, extData, title) {
  // #ifdef MP-WEIXIN
  newSendTrackEx('SRKIT_DETAIL_CLICK', 'SRKIT_DETAIL_PAGE', { ... }, true);
  // #endif
}

// composables/useSrkitDetail.js
import { trackCouponClick } from '../track/srkitDetail';
const handleCouponClick = () => {
  trackCouponClick(detailData.value, extData.value, 'Coupon');
};
```

---

## 10. Monitoring Quick Start

> Full API and patterns: [reference/monitor.md](reference/monitor.md)

```javascript
import { useMonitorReport } from 'tingyun/index.js';

const monitorReport = useMonitorReport();

// Report by level
monitorReport.error({ name: 'OrderSubmitError', message: 'Order submission failed', stack: error.stack });
monitorReport.info({ name: 'OrderSubmitStart', message: 'Starting order submission' });
monitorReport.warn({ name: 'LowBalance', message: 'Insufficient balance' });
```

**Log Levels**: error > warn > info > debug > log

**Notes**: Reporting must not block business, high-frequency operations need throttling, no sensitive data in reports

---

## 11. Build & Run

> Full CI/CD config: [reference/deployment.md](reference/deployment.md)

### Common Build Commands

```bash
# WeChat Mini Program
pnpm run app:dev:mp-weixin       # Development
pnpm run app:stg:mp-weixin       # Staging
pnpm run app:prod:mp-weixin      # Production

# Alipay Mini Program
pnpm run app:dev:mp-alipay

# H5 Business Lines
pnpm run dev:h5-module-config
pnpm run stg:h5-module-config

# Customization (offline package)
pnpm run dev:h5-customization-mod
pnpm run build:customization-mod
```

### Build Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `NODE_CUSTOM_ENV` | Environment | dev / stg / prod |
| `UNI_PLATFORM` | Platform | mp-weixin / mp-alipay / h5-xxx |
| `BUILD_TYPE` | Build type | OfflinePackage (optional) |
| `CURR_MACHINE` | Device | android / ios (offline package) |
| `BUSINESS_TYPE` | Business type | MOD / MOP (offline package) |

---

## Additional Resources

- Composable full architecture → [reference/composables.md](reference/composables.md)
- Component full patterns → [reference/component.md](reference/component.md)
- Service layer full guide → [reference/services.md](reference/services.md)
- Store full usage → [reference/store.md](reference/store.md)
- Transaction Store → [reference/transaction-store.md](reference/transaction-store.md)
- SharedCache shared cache → [reference/shared-cache.md](reference/shared-cache.md)
- Dialog Composables → [reference/dialog.md](reference/dialog.md)
- Static asset management → [reference/static-assets.md](reference/static-assets.md)
- Build & deploy full config → [reference/deployment.md](reference/deployment.md)
- Monitoring full API → [reference/monitor.md](reference/monitor.md)
- Complete code examples → [examples.md](examples.md)
