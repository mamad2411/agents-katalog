---
name: zalo-mini-app
description: Build Zalo Mini Apps - lightweight React web apps running inside the Zalo super-app. Use for Zalo Mini App setup, zmp-cli/devtools, ZaUI 1.11.x components, zmp-sdk APIs, permissions, token-based phone number flow, user info, storage, local file storage, camera/media, document preview, payment/Checkout, Open APIs, partner APIs, KYB/eKYC, publication, testing, and Zalo design guidelines.
---

# Zalo Mini App Development

Build Mini Apps for the Zalo platform using React, ZaUI, zmp-sdk, Zalo Mini App CLI/Extension, and platform Open APIs.

Docs baseline: official Zalo Mini App docs checked on **2026-06-24**.

## Quick Start

```bash
npm install -g zmp-cli
zmp create my-app
cd my-app
zmp start
```

Core packages:

```bash
npm install zmp-ui zmp-sdk
```

```tsx
import { App, Page, Button, Input, Modal } from "zmp-ui";
import "zmp-ui/zaui.css";
import { getUserInfo, authorize } from "zmp-sdk/apis";
```

Current package versions observed on 2026-06-24:

- `zmp-sdk`: 2.51.x
- `zmp-ui`: 1.11.x
- `zmp-cli`: 4.0.x

Always verify package types in the installed project when implementing exact props or SDK return types.

## References

### Setup & Release
- [getting-started.md](./references/getting-started.md) - Create app, auth, permissions, CLI/Extension, test, publish
- [design-guidelines.md](./references/design-guidelines.md) - Zalo design standards and review checklist
- [web-design-guidelines.md](./references/web-design-guidelines.md) - Accessibility, mobile UX, forms, performance
- [react-best-practices.md](./references/react-best-practices.md) - Waterfalls, bundle size, re-renders, JS performance

### SDK APIs
- [api-overview.md](./references/api-overview.md) - API groups, import patterns, error handling
- [api-user.md](./references/api-user.md) - authorize, getUserInfo, token-based getPhoneNumber, getAccessToken
- [api-storage.md](./references/api-storage.md) - Storage APIs and legacy aliases
- [api-ui.md](./references/api-ui.md) - toast, navigation bar, webview, routing
- [api-device.md](./references/api-device.md) - location, camera, media picker, document, QR/NFC, network
- [api-local-file-storage.md](./references/api-local-file-storage.md) - Local File Storage APIs
- [api-permission-biometric.md](./references/api-permission-biometric.md) - permissions and biometric auth
- [api-advertising-widgets.md](./references/api-advertising-widgets.md) - ads and function/OA widgets
- [api-zalo.md](./references/api-zalo.md) - OA, chat, sharing, profile, shortcuts

### Payment / Backend APIs
- [payment-checkout.md](./references/payment-checkout.md) - Payment integration, order, callback, status, refund
- [open-apis.md](./references/open-apis.md) - Open APIs, partner APIs, signature verification, KYB notes
- [ekyc-apis.md](./references/ekyc-apis.md) - eKYC API map and secure integration notes

### ZaUI Components
- [zaui-overview.md](./references/zaui-overview.md) - Component list and design tokens
- [zaui-layout.md](./references/zaui-layout.md) - App, Page, Header, Router, BottomNavigation, Box utilities
- [zaui-display.md](./references/zaui-display.md) - Avatar, Icon, List, Swiper, Calendar, Text
- [zaui-form.md](./references/zaui-form.md) - Button, Input, Select, DatePicker, OTP, Slider
- [zaui-overlay.md](./references/zaui-overlay.md) - Modal, Sheet, ActionSheet, SnackbarProvider

## Critical Current Patterns

### Phone Number: Token Flow, Not Direct Number

```ts
import { getPhoneNumber } from "zmp-sdk/apis";

const { token } = await getPhoneNumber({});
// Send token to backend immediately.
// Backend exchanges token with Zalo Open API to get the actual phone number.
// Token is single-use and short-lived.
```

Do **not** expect `getPhoneNumber` to return `{ number }` in current docs.


### Location: Token Flow, Not Direct Coordinates

```ts
import { getLocation } from "zmp-sdk/apis";

const { token } = await getLocation();
// Send token to backend for Zalo Open API exchange.
```

Do **not** expect `getLocation` to return direct `{ latitude, longitude }` in current docs.

### Local File Storage: LFSStorage Namespace

```ts
import { LFSStorage } from "zmp-sdk/apis";

const { support } = await LFSStorage.isSupportLFS();
const { savedPath } = await LFSStorage.saveFile({ filePath: "local-temp-path" });
```

Use `filePath` / `savedPath`, not old `tempFilePath` helpers.

### Media Picker: Current Shape

```ts
import { openMediaPicker } from "zmp-sdk/apis";

const { data } = await openMediaPicker({
  type: "photo",
  maxSelectItem: 5,
  serverUploadUrl: "https://example.com/upload"
});
```

Use `maxSelectItem`, not `maxSelection`.

### Basic Page Layout

```tsx
import { App, Page, Header, List, Icon, BottomNavigation } from "zmp-ui";

export default function Root() {
  return (
    <App>
      <Page>
        <Header title="Home" />
        <List>
          <List.Item title="Item" suffix={<Icon icon="zi-chevron-right" />} />
        </List>
      </Page>
      <BottomNavigation fixed>
        <BottomNavigation.Item key="home" label="Home" icon={<Icon icon="zi-home" />} />
      </BottomNavigation>
    </App>
  );
}
```

## Resources

- Docs: https://miniapp.zaloplatforms.com/documents/
- API: https://miniapp.zaloplatforms.com/documents/api/
- ZaUI: https://miniapp.zaloplatforms.com/documents/zaui/
- Payment: https://miniapp.zaloplatforms.com/documents/payment/
- Open APIs: https://miniapp.zaloplatforms.com/documents/open-apis/
- Mini App Center: https://miniapp.zaloplatforms.com/
