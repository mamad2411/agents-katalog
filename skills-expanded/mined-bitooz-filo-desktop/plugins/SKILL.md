---
name: plugins
description: "Make or change a Filo plugin: a small JavaScript program that gives the user a page of its own in Filo's sidebar (a habit tracker, a reading list, a dashboard of their servers, a tool over their files), drawn natively from building blocks (list, text, button, input, picker, toggle, chart), keeping its own data, with full access to files, the shell, the internet and Filo's data. Use when the user wants something that lives in Filo and they come back to, rather than a chat answer or a one-off page (that's an artifact)."
---

# Plugins: pages of the user's own in Filo's sidebar

A plugin is a folder with two files, `plugin.json` and `index.js`. Filo runs `index.js` on macOS's own JavaScriptCore (no Node, no browser, no npm packages) and draws the page it describes with Filo's own native list rows, buttons, fields and charts, in the sidebar under the plugin's name. It keeps its data in `filo.store`, which survives restarts, edits and reinstalls. Once installed it reloads by itself whenever you save one of its files.

A plugin you write runs at once, with no permission to ask for: it's the user's own code on their Mac. It can read and change any file, run any command, reach the internet and call Filo's own functions. So be as careful as you'd be with the shell: never delete or overwrite the user's things unless they asked.

## 1. New, or a change?

- **A change to one that exists:** `list_plugins` gives each plugin's id and folder. Edit its files there; it reloads within a second. Then check `plugin_status`.
- **A plugin the user got from someone else** (a file, a link): don't install it as your own. Use `import_plugin`, which marks it as from elsewhere; it waits until the user installs it from its page, which shows what it will reach. It stays marked after you edit it.
- **New:** step 2.

## 2. Write it

Make `plugins/<short-name>/` in your working folder, like `plugins/habits/` (`plugins/` itself may not be there yet: `mkdir -p` it), and keep that folder for as long as it's this plugin. Start from the example in this skill's folder, a complete habit tracker: copy `example-plugin.json` to `plugin.json` and `example-index.js` to `index.js` in the new folder, then change them.

`plugin.json`:

```json
{ "name": "Habits", "icon": "list-todo", "description": "Tick off today's habits and watch your streaks." }
```

- `name`: the sidebar's label, one or two short words (it's cut at about 10 characters there).
- `icon`: one of the names below; anything else shows a plug.
- `description`: one sentence, shown under the title until the page sets its own subtitle.

`index.js` is a plain script (not a module: no `import`, `export` or `require`, and no top-level `await`). It reads its data, then calls `filo.render` with a function that returns the page. That function runs again after everything that happens: a tap, each key typed, a timer, a finished command or download. So keep the state in variables and rebuild the page from them; there's no state hook to call.

```js
const ui = filo.ui;
let items = filo.store.get("items", []);
let draft = "";

filo.render(() =>
  ui.page({
    children: [
      ui.input({ id: "new", placeholder: "Add an item", value: draft, onChange: (t) => (draft = t),
        onSubmit: (t) => { items.push({ title: t }); draft = ""; filo.store.set("items", items); } }),
      ui.list({ items, empty: "Nothing yet." }),
    ],
  }),
);
```

## 3. Install and check it

Call `install_plugin` with the folder (`plugins/habits`). Filo runs it and tells you within a few seconds: running with the page's outline ("text · input "Add an item" · list (0 items)"), or the error with its line and the plugin's log. Fix what it says by editing the files, wait a second, and read `plugin_status`. Installing the same folder again restarts it. Tell the user it's in their sidebar under its name once the status says running with no error.

## The page: `filo.ui`

Every block is a plain object; the helpers below just make them. Children can be nested arrays, and `null`, `false` and `undefined` are left out, so `cond && ui.text("…")` works. A string or number among children is text. Every handler (`onPress`, `onChange`, `onSubmit`, `onToggle`) may be an `async` function.

- `ui.page({ title, subtitle, actions, children })`: the whole page, what render returns (an array of blocks is fine too). `title` defaults to the plugin's name; `actions` are buttons at the top right.
- `ui.text(text, { style, color })`: `style` is `title`, `heading`, `body` (default), `secondary`, `caption` or `mono`.
- `ui.button(title, onPress, { style, icon, disabled })` or `ui.button({ title, onPress, … })`: `style` is `primary`, `secondary` (default), `ghost` or `danger`. With an `icon` and no `title` it's a small icon button (give it a `tooltip`).
- `ui.input({ id, label, placeholder, value, onChange, onSubmit, multiline, secure })`: `onChange(text)` on each key, `onSubmit(text)` on Return (⌘Return in a `multiline` one). Give it an `id`. With a `value`, the field shows that value (set your variable to `""` in onSubmit to empty it); without one, it keeps what's typed and empties after onSubmit.
- `ui.picker({ label, options, value, onChange, placeholder, style })`: `options` are strings or `{ value, label }`; `onChange(value)` gets the value as a string. `style: "segmented"` shows them side by side (for two to four short ones).
- `ui.toggle(label, value, onChange)` or `ui.toggle({ label, value, onChange })`: a switch; `onChange(on)`.
- `ui.list({ title, items, empty, footer })` or `ui.list(items)`: rows on a card. Each item: `{ title, subtitle, icon, accessory, accessoryColor, checked, onToggle, onPress, actions }`. `checked` (true or false) puts a checkbox first, which calls `onToggle(on)`; `accessory` is short text at the end (a count, a date); `actions` are buttons at the end; `onPress` makes the row open something.
- `ui.section(title, children, { footer })`: blocks grouped on a card under a heading.
- `ui.row(children, { fill })`: blocks side by side, wrapping when narrow (`fill: true` shares the width).
- `ui.stat(label, value, { detail, color })`: a number to see at a glance; put two to four in a `ui.row`.
- `ui.progress(fraction, { label, color })`: a bar from 0 to 1. It shows the percentage itself at its end, so `label` says what it measures ("Today's goal"), not the number.
- `ui.chart({ kind, title, data, height, color })`: `kind` is `bar` (default), `line`, `area` or `pie`; `data` is `[{ label, value }]` or `[[label, value]]`; `height` in points (180 by default).
- `ui.divider()`.

Colours (`color`, `accessoryColor`) are names, so the page fits light and dark mode: `accent`, `success`, `warning`, `danger`, `info`, `secondary`, `tertiary` (or a `#hex`, rarely).

Icons, for `plugin.json`, buttons and rows. Pick the one that names the plugin's subject; anything not listed shows a plug.

- Everyday life: `droplet`, `glass-water`, `coffee`, `utensils`, `apple`, `carrot`, `dumbbell`, `footprints`, `bike`, `activity`, `heart-pulse`, `heart`, `bed`, `pill`, `scale`, `weight`, `baby`, `dog`, `cat`, `paw-print`, `sprout`, `leaf`, `mountain`, `sun`, `moon`, `cloud-sun`, `thermometer`, `house`, `car`, `plane`, `gift`, `gamepad-2`, `camera`, `music`, `smile`.
- Money and work: `wallet`, `piggy-bank`, `dollar-sign`, `receipt`, `shopping-cart`, `briefcase`, `graduation-cap`, `book`, `book-open`, `notebook-pen`, `file-text`, `folder`, `inbox`, `user`, `building-2`, `lightbulb`, `brain`, `palette`.
- Time and goals: `list-todo`, `list`, `calendar`, `calendar-clock`, `clock-3`, `alarm-clock`, `timer`, `hourglass`, `target`, `flame`, `circle-check`, `check`, `star`, `bookmark`, `flag`, `pin`, `bell`, `repeat`.
- Data and tech: `chart-column-stacked`, `chart-line`, `chart-pie`, `trending-up`, `table`, `layout-dashboard`, `layout-grid`, `search`, `globe`, `link`, `map`, `compass`, `image`, `video`, `mic`, `square-terminal`, `code-xml`, `git-branch`, `workflow`, `monitor`, `laptop`, `smartphone`, `key-round`, `plug`, `puzzle`.
- Actions (buttons): `plus`, `minus`, `pencil`, `trash-2`, `refresh-cw`, `play`, `pause`, `send`, `share-2`, `download`, `external-link`, `settings`, `sliders-horizontal`, `x`.

## What it reaches: `filo`

- `filo.store.get(key, fallback)`, `.set(key, value)`, `.remove(key)`, `.keys()`, `.all()`: the plugin's own data, any JSON. It's saved after each event and kept in Filo's folder, not the plugin's, so editing or reinstalling the plugin keeps it. Keep everything the user enters here.
- `filo.fs.read(path)`, `.readJSON(path)`, `.write(path, text)`, `.writeJSON(path, value)`, `.append(path, text)`, `.list(path)` (`[{ name, path, dir, size, modified }]`), `.exists(path)`, `.stat(path)`, `.mkdir(path)`, `.remove(path)`: files, at once. `~/` is the home folder; a relative path is in the plugin's data folder (`filo.plugin.dataFolder`). Never write into the plugin's own folder: that reloads it.
- `await filo.shell(command, { cwd, timeout, input })`: runs a command in the user's login shell and gives `{ code, stdout, stderr }` (it doesn't throw when the command fails: check `code`). `timeout` in seconds, 120 by default. `filo.shellSync(…)` waits for it right there; prefer the async one so the page keeps answering.
- `await filo.fetch(url, { method, headers, body, timeout })`: `{ status, ok, url, headers, text, json() }`. A `body` that isn't a string is sent as JSON. `filo.fetchSync(…)` waits right there.
- `await filo.call(name, args)`: one of Filo's own functions, as Filo's pages call them: `notes:mine` (the notes), `notes:getMine` (`{ id }`), `notes:createMine` (`{ title, body }`), `agents:list`, `memories:list` and the like. It throws with Filo's message when the call fails. `filo.callSync(…)` waits right there.
- `filo.open(target)`: opens a link in the browser, or a file or folder (`~/` and relative paths as for files) in its app.
- `filo.toast(text)`: a short message in Filo's window.
- `filo.update()`: draws the page again (after work you started outside a handler; handlers, timers and finished jobs redraw by themselves).
- `setTimeout`, `setInterval`, `clearTimeout`, `clearInterval`, `Promise`, `async`/`await`, `JSON`, `Date`, `Intl` and the rest of the language are there. There's no DOM, `window`, `document`, `localStorage` or global `fetch`: use `filo.*`.
- `console.log`, `console.warn`, `console.error` and `filo.log` write to the plugin's log, which `plugin_status` shows with every error and where it was thrown.
- `filo.plugin` (`{ id, name, folder, dataFolder }`) and `filo.home`.

## Make it good

- **The page answers first.** The top says the state of things (a subtitle, a stat row, today's progress); the list and the controls come after. No welcome text or instructions the user doesn't need.
- **Plain words**, sentence case, short labels. Empty lists say what's missing (`empty: "No habits yet."`).
- **Quick to use.** A field submits on Return; a row's checkbox or a button does the common thing in one tap. Destructive actions are small (`trash-2` icon buttons).
- **Never lose what the user entered:** save to `filo.store` in the same handler that changes it, and keep older data readable when you change its shape (read missing fields with defaults).
- **Slow work off the page:** fetch and shell with `await`, show a "Loading…" text or the last known values meanwhile, and keep a refresh button in `actions`. Poll with `setInterval` only as often as the data changes (a minute or more for the web).
- **A script that runs more than 10 seconds at once is stopped**, so don't loop on work; use timers.
