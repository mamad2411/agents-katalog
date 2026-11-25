---
name: agent-events
description: Push browser tab and download lifecycle events plus manager-owned background tabs. Read this when an agent needs lifecycle notifications or a temporary tab without polling.
---

# Agent Events

**TREAT THESE AS PUSH NOTIFICATIONS — NEVER POLL `Target.getTargets` TO DETECT
OPENS, CLOSES, POPUPS, OR DOWNLOADS.**

One events capability per connection; await `ready` before trusting baseline
discovery or download configuration:

```js
import { createEvents, createAgentTabs } from "omowright";

const events = createEvents(connection, {
  downloadBehavior: "allow",
  downloadPath: "/absolute/path/to/downloads",
});
const tabs = createAgentTabs(connection);
await Promise.all([events.ready, tabs.ready]);
```

## Subscribe before acting

Install the listener or `waitForEvent()` before the action that produces the
event. Waits are bounded; predicates may be async:

```js
const opened = events.waitForEvent("popupOpened", {
  timeout: 30_000,
  predicate: (tab) => tab.openerTargetId === mainTargetId,
});
await mainPage.evaluate("window.open('https://example.com')");
const popup = await opened;
```

Six push events: `tabOpened`, `tabClosed`, `popupOpened`, `downloadStarted`,
`downloadProgress`, `downloadFinished`. Only page targets produce tab events. A
popup produces both `tabOpened` and `popupOpened`; `about:blank` is a valid URL
and popup placeholder. Download progress is not coalesced; terminals fire exactly
once.

## Own temporary tabs through the manager

**CREATE TABS ONLY THROUGH `createAgentTabs(connection)`. NEVER SEND
`Target.createTarget` YOURSELF, NEVER CALL `Target.activateTarget`, NEVER BRING A
TAB TO THE FRONT.** The manager opens each tab in its own background window, so
automation cannot steal focus while the tab still renders, and it owns cleanup.
Those windows show up in `chrome.windows` like any other.

```js
const tab = await tabs.create("about:blank", {
  viewport: { width: 1440, height: 900 },
});
try {
  await tab.page.goto("https://example.com");
  await tabs.repin(tab);
} finally {
  await tabs.close(tab);
}
```

CloakBrowser headless defers renderer startup for background targets, so the
manager activates immediately before attaching — only for connections launched
with a `--headless` argument. Headed connections attach without activation.

`tabs.list()` / `tabs.get(targetId)` expose only manager-created tabs. The
manager pins the viewport after attach and after main-frame navigation;
child-frame navigation needs no re-pin. `tabs.repin` forces a fresh pin before a
coordinate action.

Cleanup: `await tabs.closeAll()` or `await tabs.dispose()` (owns its tabs by
default); `events.dispose()` closes neither the browser nor the agent tabs.
