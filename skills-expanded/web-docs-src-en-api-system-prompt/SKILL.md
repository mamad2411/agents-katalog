# Popup

## Importing Modules

``` js
import prompt from '@system.prompt'
```

## API Definitions

#### `showToast`
<decl method><pre>
(options: {
  message: string,
  duration?: number,
  important?: boolean
}): void
</pre></decl>

Displays a toast popup. A toast is a text popup placed at the top level of the interface. Only one instance of a toast is displayed in the interface at a time; if there are multiple toast contents, they will be displayed in a queue.

Description of `options` parameter fields:
- `message`: The text to be displayed.
- `duration`: The display duration of the toast in ms. The toast will automatically hide after the timeout duration is reached.
- `important`: Whether it is an important toast, defaults to `false`. If set to `true`, the toast is allowed to pop up even when the application is in the background.

The display style of the toast (font, color, etc.) is determined by the firmware and cannot be modified within the application. The display duration of the toast is also limited, ranging from $200$ to $5000$ milliseconds.

#### `showPopup` <decl type="(options: { uri: string, params?: Object }): Promise<any>" method />

Displays a floating page popup. Description of `options` parameter fields:
- `uri`: The name of the target page, which needs to be registered in the `router` section of `manifest.json`.
- `params`: Data to be passed during navigation. The properties of the `params` parameter will replace the `data` property values of the target page.

A floating page is a system-level popup (similar to a toast or dialog), but it is a full-featured page with the highest level of customizability. Unlike regular pages, floating pages are displayed in the system's floating page stack rather than the application's own page stack. Therefore, APIs such as `router.back()` in the [page routing](api/system-router) mechanism cannot operate on floating pages. To close a floating page, you can use the [`router.close()`](system-router.md#close) method.

The display hierarchy of popups is higher than that of the application, so floating pages will be displayed above all application pages. All applications use the same floating page stack. The display hierarchy of floating pages is determined by the order in which they pop up, meaning the page that pops up earlier is at the top. The display hierarchy of floating pages is the same as dialogs and lower than toasts.

Like `router.push()`, `showPopup()` also returns a Promise object, which resolves and returns a custom result after the floating page exits. For details, please refer to [`router.push()`](system-router.md#push) and [`router.close()`](system-router.md#close).
