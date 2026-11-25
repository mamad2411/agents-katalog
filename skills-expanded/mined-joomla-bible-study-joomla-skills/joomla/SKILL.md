---
name: joomla
description: Joomla 5+ / 6 / 7 extension development for components, modules, plugins, libraries, and templates using modern MVC with PSR-4, DI, and service providers. Trigger on Joomla 5, 5.4, 6, 6.1, 6.2, 7, J5/J6/J7, Joomla CMS, provider.php, manifest XML, install script, scriptfile, cli/joomla.php, or any Joomla extension code. Covers scaffolding; MVC views/models/controllers; service providers; manifests; database migrations; language files; form fields; layout and template overrides; plugin event subscribers (SubscriberInterface, CMSPlugin); module dispatchers; Web Asset Manager; task / webservices / finder / schemaorg plugins; Web Services REST API (Joomla JSON:API, ApiController, JsonapiView, API tokens, consuming the API); console commands (CLI, console plugins, AbstractCommand); SEF routers. Use for prompts like "add a view", "register web assets", "override a layout", "add a CLI command", "expose this via the API" in any Joomla project.
---

# Joomla 5+ Extension Development

This skill guides you through building Joomla 5+ extensions (components, modules, plugins) using modern architecture patterns derived from the [joomla-cms](https://github.com/joomla/joomla-cms) core and real-world production components.

**Target:** Natively Joomla 6, backward compatible with Joomla 5 (no backward compatibility plugin required)
**PHP requirement (Joomla 6.x):** 8.3+ minimum and supported, 8.4 recommended ([source](https://manual.joomla.org/docs/get-started/technical-requirements/))
**Coding standard:** PSR-12 (PHP), Joomla ESLint config (JavaScript)

## Canonical sources

When a Joomla pattern is non-obvious, ambiguous, or might have drifted between versions, verify against upstream before answering. Prefer fetching directly with WebFetch; if the fetch is blocked, fails, or the user is offline, fall back in this order: (1) cite the canonical URL so the user can open it, (2) rely on the patterns documented in this skill and `references/*.md`, (3) ask the user to paste the relevant snippet rather than guess.

**Primary — source of truth for runtime behavior:**

- [`github.com/joomla/joomla-cms`](https://github.com/joomla/joomla-cms) — core CMS. **Active dev branches** (verified 2026-04-30, after J6.1 release):
  - `6.1-dev` — current released J6 line, in patch maintenance. **Default reference for new J6 code.**
  - `6.2-dev` — next J6 minor in development.
  - `5.4-dev` — current released J5 line.
  - `7.0-dev` — next major in development. Where deprecations land for removal (e.g., the `CMSPlugin::__construct(DispatcherInterface, …)` deprecation slated for removal here — see `references/plugin.md`).
  
  Pick the branch matching the target Joomla version for the code you're verifying. Re-check [`/branches`](https://github.com/joomla/joomla-cms/branches) periodically — Joomla cuts new minor branches frequently and the names above will drift.
  - Frontend component examples: [`components/`](https://github.com/joomla/joomla-cms/tree/6.1-dev/components)
  - Backend component examples: [`administrator/components/`](https://github.com/joomla/joomla-cms/tree/6.1-dev/administrator/components)
  - Core plugins: [`plugins/`](https://github.com/joomla/joomla-cms/tree/6.1-dev/plugins)
  - Core modules: [`modules/`](https://github.com/joomla/joomla-cms/tree/6.1-dev/modules) and [`administrator/modules/`](https://github.com/joomla/joomla-cms/tree/6.1-dev/administrator/modules)
  - Framework libraries shipped with the CMS: [`libraries/src/`](https://github.com/joomla/joomla-cms/tree/6.1-dev/libraries/src)
- [`github.com/joomla-framework`](https://github.com/joomla-framework) — standalone Framework packages (DI, Event, Filesystem, etc.) reused by the CMS.

**Documentation:**

- [manual.joomla.org](https://manual.joomla.org/) — current Developer Manual (Joomla 5+). Preferred prose reference.
  - Source repo: [`github.com/joomla/Manual`](https://github.com/joomla/Manual) (default branch `main`) — the Markdown backing the rendered site. Useful when you need to grep, fetch raw, or cite a permalink to a specific page; manual edits / corrections also go here as PRs.
- [api.joomla.org](https://api.joomla.org/) — generated API reference (classes, methods, signatures).
- [framework.joomla.org](https://framework.joomla.org/) — Joomla Framework package docs.
- [docs.joomla.org](https://docs.joomla.org/) — **legacy wiki**. Useful for historical context (J3/J4) but often stale for J5/J6; cross-check against `joomla-cms` HEAD before quoting.

**When citing in generated code or replies:** prefer a permalink to a specific file/line in `joomla-cms` (right-click → "Copy permalink" produces a commit-pinned URL) over a branch link, so the reference does not silently drift.

**Update cadence:** if a WebFetch reveals the upstream pattern differs from what this skill teaches, flag it to the user and recommend opening an issue on `Joomla-Bible-Study/joomla-skills` so the skill can be corrected.

## Coding Standards

**Standards:** PSR-12 for PHP, Joomla ESLint flat config for JavaScript, `joomla/coding-standards` PHPCS ruleset, C++ style (`//`) for inline comments. Every PHP file ships a `@package` / `@copyright` / `@license` header, every class/property/method gets a docblock with `@since`, `@param` blocks align to two-space minimum spacing, and `@return` is always required. For in-flight code where the next release version isn't fixed yet, use the literal `@since __DEPLOY_VERSION__` placeholder — the release build substitutes it with the actual version before the package is archived. JS sources live in `build/media_source/` and compile to `media/<extension>/js/`; the `Joomla` and `bootstrap` globals are pre-registered. For full docblock examples (file header, class, property, method, deprecated, `__DEPLOY_VERSION__` placeholder), JS conventions and JSDoc patterns, the PHPCS install / `phpcs.xml` template, and the inline-comment style rules, read [`references/coding-standards.md`](references/coding-standards.md).

## Quick Start: Which Extension Type?

Before writing code, identify the right extension type:

- **Component** — Full application with admin backend + frontend views, database tables, CRUD operations, menus. Use when you need a complete management interface (e.g., a booking system, directory, inventory tracker, content manager).
- **Module** — Small, self-contained display block (sidebar, footer, header widget). Has a dispatcher, optional helper, and template. No admin CRUD — gets data from components or its own parameters.
- **Plugin** — Event-driven code that hooks into Joomla's lifecycle. Types include: content, system, finder (search), task (scheduled), webservices (API), schemaorg, console (CLI commands), and more.
- **Library** — Shared PHP code used by multiple extensions. Installed to `libraries/` and autoloaded via PSR-4 namespace. Use when you have utility classes, API wrappers, or shared logic consumed by your components, plugins, and modules.
- **Template** — Controls the site's HTML shell and layout overrides.

For detailed patterns of each type, read the appropriate reference file:
- `references/component.md` — Full component architecture
- `references/module.md` — Module structure and dispatcher pattern
- `references/plugin.md` — Plugin event subscriber pattern
- `references/library.md` — Library structure and packaging

Cross-cutting references (loaded on demand):
- `references/admin-routing.md` — `task=` vs `view=` URL patterns and the checkout pattern that prevents concurrent overwrites
- `references/coding-standards.md` — PSR-12 / PHPDoc / ESLint / PHPCS conventions
- `references/component-advanced.md` — Toolbar API, batch, ordering, tags, versioning, workflow, webservices, mail templates, dashboards, custom rules
- `references/component-lifecycle.md` — Model save flow, `prepareTable()`, `Table::bind()`/`store()`, filter forms, install script, config.xml, site-side differences, HTMLHelper services, `showon` and fieldset tabs
- `references/console-commands.md` — CLI commands for `php cli/joomla.php`: console plugin, `AbstractCommand`, lazy container-loader registration, what differs under the console
- `references/database.md` — Install SQL / update SQL, `#__` prefix, DDL-vs-DML rule
- `references/editor-api.md` — WYSIWYG editor JS/PHP API + XTD buttons
- `references/form-fields.md` — Built-in field types + custom field authoring
- `references/layouts.md` — `LayoutHelper::render()`, override priority, sublayouts, key built-in layouts
- `references/menu-items.md` — Site-view menu item type XML (request fields, params, useglobal, multi-layout)
- `references/packaging.md` — Manual zip, build scripts, package extensions, include/exclude checklist, **changelog XML**
- `references/testing.md` — PHPUnit + Jest patterns with real Joomla CMS classes
- `references/update-server.md` — Update server XML, `<targetplatform>` regex, SHA hashes, per-type tweaks
- `references/web-assets.md` — `joomla.asset.json` schema, `useStyle`/`useScript`, dependencies
- `references/webservices-api.md` — Joomla JSON:API REST layer: webservices plugin routes, `ApiController` / `JsonapiView`, API tokens, errors, CORS, consuming the API from PHP / JS / curl
- `references/gotchas.md` — Hard-won J5/J6 pitfalls (controllers, routing, WAM, dark mode, etc.)

Shared cross-extension references (linked from the per-type files above):
- `references/manifest.md` — Universal manifest elements (`<extension>` root, metadata, `<files>`, `<media>`, `<languages>`, `<scriptfile>`, `<update>` / `<updateservers>`)
- `references/install-script.md` — Lifecycle hooks (`preflight`/`install`/`update`/`postflight`/`uninstall`) shared by component/module/plugin/library
- `references/language-files.md` — Filename conventions, key prefixes per type, plurals, `Text::script()` JS registration
- `references/service-provider.md` — `ServiceProviderInterface` pattern + per-type binding table (component/module/plugin)
- `references/component-router.md` — Router class + `RouterServiceInterface` + `RouterFactory` 3-part contract and SEF rules

## Core Architecture Principles

### 1. PSR-4 Namespaces (Everything Lives in src/)

All PHP classes go under `src/` and use PSR-4 autoloading. Joomla maps namespaces declared in the manifest XML.

**Component namespace declaration (manifest XML):**
```xml
<namespace path="src">Vendor\Component\MyComponent</namespace>
```

Joomla auto-expands this to:
- `Vendor\Component\MyComponent\Administrator\` → `admin/src/`
- `Vendor\Component\MyComponent\Site\` → `site/src/`
- `Vendor\Component\MyComponent\Api\` → `admin/src/Api/` (if present)

**Example:**
```xml
<namespace path="src">Acme\Component\Bookings</namespace>
```
- `Acme\Component\Bookings\Administrator\Model\BookingModel` → `admin/src/Model/BookingModel.php`
- `Acme\Component\Bookings\Site\View\Booking\HtmlView` → `site/src/View/Booking/HtmlView.php`

**Module namespace:**
```xml
<namespace path="src">Vendor\Module\MyModule</namespace>
```

**Plugin namespace:**
```xml
<namespace path="src">Vendor\Plugin\PluginGroup\MyPlugin</namespace>
```

Case sensitivity matters on Linux. Directory names and class names must match exactly.

> **Joomla 5/6 Compatibility Note:** `createQuery()` and `\Joomla\Input\Input` work on both Joomla 5 and 6. Writing code this way means it runs natively on J6 without the backward compatibility plugin, while also working fine on J5.

### 2. Service Provider (The Modern Entry Point)

Every extension has `services/provider.php` — this is how Joomla discovers and bootstraps the extension through its DI container. The wrapping pattern (`ServiceProviderInterface` + anonymous class + `register()`) is shared across components, modules, and plugins; for the universal pattern, the per-type binding table, and the common DI pitfalls see [`references/service-provider.md`](references/service-provider.md). The example below is the **component** flavor — it registers `MVCFactory`, `ComponentDispatcherFactory`, `RouterFactory`, and (when applicable) `CategoryFactory`, then binds `ComponentInterface`.

**Component service provider pattern:**
```php
<?php
\defined('_JEXEC') or die;

use Vendor\Component\MyComponent\Administrator\Extension\MyComponentComponent;
use Joomla\CMS\Component\Router\RouterFactoryInterface;
use Joomla\CMS\Dispatcher\ComponentDispatcherFactoryInterface;
use Joomla\CMS\Extension\ComponentInterface;
use Joomla\CMS\Extension\Service\Provider\CategoryFactory;
use Joomla\CMS\Extension\Service\Provider\ComponentDispatcherFactory;
use Joomla\CMS\Extension\Service\Provider\MVCFactory;
use Joomla\CMS\Extension\Service\Provider\RouterFactory;
use Joomla\CMS\HTML\Registry;
use Joomla\CMS\MVC\Factory\MVCFactoryInterface;
use Joomla\DI\Container;
use Joomla\DI\ServiceProviderInterface;

return new class () implements ServiceProviderInterface {
    public function register(Container $container): void
    {
        $container->registerServiceProvider(new CategoryFactory('\\Vendor\\Component\\MyComponent'));
        $container->registerServiceProvider(new MVCFactory('\\Vendor\\Component\\MyComponent'));
        $container->registerServiceProvider(new ComponentDispatcherFactory('\\Vendor\\Component\\MyComponent'));
        $container->registerServiceProvider(new RouterFactory('\\Vendor\\Component\\MyComponent'));

        $container->set(
            ComponentInterface::class,
            function (Container $container) {
                $component = new MyComponentComponent(
                    $container->get(ComponentDispatcherFactoryInterface::class)
                );
                $component->setRegistry($container->get(Registry::class));
                $component->setMVCFactory($container->get(MVCFactoryInterface::class));
                $component->setRouterFactory($container->get(RouterFactoryInterface::class));

                return $component;
            }
        );
    }
};
```

The namespace string passed to each factory (e.g., `'\\Vendor\\Component\\MyComponent'`) tells Joomla where to find your Controller, Model, View, and Table classes. Get this wrong and nothing loads.

### 3. Modern Joomla API — What to Use and What to Avoid

This is critical. Code must work natively on Joomla 6 WITHOUT the "Behaviour - Backward Compatibility 6" plugin, and also run on Joomla 5.

**Use these (Joomla 6 native):**
| Task | Modern API |
|------|-----------|
| Database access | `$this->getDatabase()` or inject `DatabaseInterface` |
| Build queries | `$db->createQuery()` (preferred over `$db->getQuery(true)`) |
| Current user | `$this->getCurrentUser()` in models, `$this->getIdentity()` in views/controllers |
| Input handling | `\Joomla\Input\Input` (NOT `\Joomla\CMS\Input`) — CMS\Input is removed in J6 |
| Create model/table | MVCFactory `$this->getMVCFactory()->createModel('Name')` |
| Input in controllers | `$this->input` (already available, uses `\Joomla\Input\Input`) |
| Error handling | Throw exceptions (`\RuntimeException`, `\InvalidArgumentException`) |
| Web assets | `WebAssetManager` via `$wa = $this->getDocument()->getWebAssetManager()` |
| File operations | PHP native functions or Symfony Filesystem (NOT `\Joomla\CMS\Filesystem`) |
| getItem() return | Treat as `stdClass` (NOT `CMSObject`) — no `->get()` or `->set()` magic |

**Never use these (removed or behind compat plugin in Joomla 6):**
| Deprecated | Why | Replacement |
|-----------|-----|-------------|
| `getDbo()` or `$this->_db` | Removed in Joomla 5 | `$this->getDatabase()` |
| `$db->getQuery(true)` | Still works but deprecated pattern | `$db->createQuery()` |
| `\Joomla\CMS\Input` | Removed in Joomla 6 | `\Joomla\Input\Input` |
| `\Joomla\CMS\Filesystem` | Moved to compat plugin in J6, removed J7 | PHP native / Symfony |
| `CMSObject` properties via `->get()` / `->set()` | `getItem()` returns `stdClass` in J6 | Direct property access: `$item->title` |
| `Factory::getUser()` | Deprecated | `$this->getCurrentUser()` or `$this->getIdentity()` |
| `getSession()->get('user')` | Use identity methods | `$this->getIdentity()` |
| `getError()` / `setError()` on **models** (`BaseDatabaseModel`) | Use exceptions | Throw `\RuntimeException` |
| `new ClassName()` for models | Hard-coded dependencies | `$this->getMVCFactory()->createModel()` |
| `jimport()` | Removed | PSR-4 autoloading |
| `CMSObject` class | Deprecated, removed in J7 | `stdClass` or custom classes |
| `getErrorMsg()` | Removed | Throw exceptions |

### 4. Directory Structure

**Component layout:**
```
com_mycomponent/
├── mycomponent.xml              # Manifest
├── mycomponent.script.php       # Install/update script (optional)
├── admin/
│   ├── services/
│   │   └── provider.php         # DI container registration
│   ├── src/
│   │   ├── Extension/
│   │   │   └── MyComponentComponent.php
│   │   ├── Controller/
│   │   │   ├── DisplayController.php
│   │   │   ├── ItemController.php      # FormController (single item)
│   │   │   └── ItemsController.php     # AdminController (list)
│   │   ├── Model/
│   │   │   ├── ItemModel.php           # FormModel (single)
│   │   │   └── ItemsModel.php          # ListModel (list)
│   │   ├── View/
│   │   │   ├── Item/
│   │   │   │   └── HtmlView.php
│   │   │   └── Items/
│   │   │       └── HtmlView.php
│   │   ├── Table/
│   │   │   └── ItemTable.php
│   │   ├── Field/                      # Custom form fields
│   │   ├── Helper/                     # Utility classes
│   │   ├── Dispatcher/
│   │   │   └── Dispatcher.php
│   │   └── Service/
│   │       └── HTML/                   # HTMLHelper services
│   ├── forms/                          # XML form definitions
│   ├── sql/
│   │   ├── install.mysql.utf8.sql
│   │   └── updates/
│   │       └── mysql/
│   │           └── 1.0.0.sql
│   ├── tmpl/                           # Admin templates
│   │   ├── item/
│   │   │   └── edit.php
│   │   └── items/
│   │       └── default.php
│   ├── language/
│   │   └── en-GB/
│   │       ├── com_mycomponent.ini
│   │       └── com_mycomponent.sys.ini
│   ├── access.xml                      # ACL definitions
│   └── config.xml                      # Component options
├── site/
│   ├── src/
│   │   ├── Controller/
│   │   ├── Model/
│   │   ├── View/
│   │   ├── Dispatcher/
│   │   ├── Helper/
│   │   └── Service/
│   │       └── Router.php              # SEF URL routing
│   ├── forms/
│   ├── tmpl/
│   └── layouts/
└── media/
    ├── joomla.asset.json               # Web asset definitions
    ├── css/
    ├── js/
    └── images/
```

### 5. MVC Request Flow

Understanding the request lifecycle helps you know what to create:

```
URL → Router → Dispatcher → Controller → Model → Table (DB) → View → Template → Response
```

1. **Router** parses the URL to determine component, view, and ID
2. **Dispatcher** (admin/src/Dispatcher/) checks access and creates the controller
3. **Controller** handles the action (display, save, delete, publish)
4. **Model** fetches or manipulates data using database queries
5. **Table** maps to a single database row (load, store, delete, check)
6. **View** (HtmlView.php) prepares data for rendering
7. **Template** (tmpl/) outputs the HTML

### Admin URL Routing (`task=` vs `view=`)

Admin URLs use two patterns: `task={controller}.{method}` triggers a controller action (and checks out the record), while `view={view}` just displays a view. Linking from list views to edit forms MUST use `task=` — using `view=item&layout=edit` skips checkout and lets two users overwrite each other. For the full pattern table (when to use which), the checked-out handling pattern in list templates, and the JOIN that surfaces the editor name, read [`references/admin-routing.md`](references/admin-routing.md).

### 6. Naming Conventions

Joomla has strict naming that connects everything automatically:

| What | Naming Pattern | Example |
|------|---------------|---------|
| Single-item controller | `{Entity}Controller` | `BookingController` |
| List controller | `{Entity}sController` (plural) | `BookingsController` |
| Single-item model | `{Entity}Model` | `BookingModel` |
| List model | `{Entity}sModel` (plural) | `BookingsModel` |
| Table class | `{Entity}Table` | `BookingTable` |
| Single-item view dir | `View/{Entity}/HtmlView.php` | `View/Booking/HtmlView.php` |
| List view dir | `View/{Entity}s/HtmlView.php` | `View/Bookings/HtmlView.php` |
| Edit template | `tmpl/{entity}/edit.php` | `tmpl/booking/edit.php` |
| List template | `tmpl/{entity}s/default.php` | `tmpl/bookings/default.php` |

Some projects use a vendor prefix on entity names (e.g., `AcmeBooking` instead of plain `Booking`). This is optional but helps avoid naming collisions with other extensions.

The view name in the URL (e.g., `&view=bookings`) must match the View directory name (case-insensitive on the URL side, but the directory must match the class namespace).

### 7. Data, distribution, and storage — pointer summary

The data + distribution layers that every extension type touches are documented in their own references so this skill stays focused on the architecture above. Read the one(s) you need:

- **Database schema** — install SQL (`admin/sql/install.mysql.utf8.sql`), update SQL files in `admin/sql/updates/mysql/`, the `#__` prefix Joomla replaces at runtime, and the DDL-vs-DML rule (SQL files do DDL only; data migrations go in the install script). [`references/database.md`](references/database.md).
- **Language files** — INI file conventions, key prefixes per extension type (`COM_`, `MOD_`, `PLG_<GROUP>_<ELEMENT>_`, `LIB_`), plurals, and `Text::script()` JS registration. [`references/language-files.md`](references/language-files.md).
- **Web Asset Manager** — `joomla.asset.json` schema, `$wa->useStyle()` / `$wa->useScript()`, dependencies, attributes. [`references/web-assets.md`](references/web-assets.md).
- **Manifest XML** — `<extension>` root attributes, `<files>`, `<media>`, `<languages>`, `<scriptfile>`, the `<administration>` block with `<menu>` / `<submenu>`, and the `<install>` / `<update>` blocks. Universal elements in [`references/manifest.md`](references/manifest.md); the full component-flavored manifest template in [`references/component.md`](references/component.md).
- **Install / update scripts** — `preflight` / `install` / `update` / `postflight` / `uninstall` hooks and DML migrations. [`references/install-script.md`](references/install-script.md).
- **Changelog XML** — what powers the in-admin "View changelog" link; categories (`<security>`, `<fix>`, etc.), required nodes, element/type values per extension type. [`references/packaging.md`](references/packaging.md) § Changelog XML.
- **Update server** — update XML, `<targetplatform>` regex, SHA hashes, per-extension-type tweaks (`folder` / `client` attributes). [`references/update-server.md`](references/update-server.md).

## Workflow: Adding a New Entity to a Component

When adding a new entity (e.g., "Location" to a component), create these files:

1. **Table** — `admin/src/Table/LocationTable.php`
2. **Model (single)** — `admin/src/Model/LocationModel.php` (extends FormModel)
3. **Model (list)** — `admin/src/Model/LocationsModel.php` (extends ListModel)
4. **Controller (single)** — `admin/src/Controller/LocationController.php` (extends FormController)
5. **Controller (list)** — `admin/src/Controller/LocationsController.php` (extends AdminController)
6. **View (edit)** — `admin/src/View/Location/HtmlView.php`
7. **View (list)** — `admin/src/View/Locations/HtmlView.php`
8. **Templates** — `admin/tmpl/location/edit.php` and `admin/tmpl/locations/default.php`
9. **Form XML** — `admin/forms/location.xml`
10. **SQL** — Add CREATE TABLE to install SQL, add update SQL file
11. **Language strings** — Add to `.ini` files
12. **Menu entry** — Add `<menu>` to manifest XML submenu

For detailed code templates of each file, read `references/component.md`.

## Component Lifecycle & Patterns

The internal mechanics of how components work — the model save flow (`Controller::save()` → `Model::prepareTable()` → `Table::bind()` → `Table::check()` → `Table::store()`), the `getItem()` / `save()` model overrides, `Table::bind()` JSON-encoding params, filter form XML for searchtools, the component install/update script class, `config.xml` component options, site-side differences (caching, access filtering, menu params, page metadata), the Extension class implementing `CategoryServiceInterface` / `TagServiceInterface`, custom controller tasks and AJAX, registering HTMLHelper services, and form XML conditional fields (`showon`) plus fieldset-to-tab rendering — all live in [`references/component-lifecycle.md`](references/component-lifecycle.md).

## Advanced Component Features

Component-level features beyond core MVC: the toolbar API (`getDocument()->getToolbar()`, dropdown groups, save dropdowns), batch processing (`AdminModel` batch methods, dialog template, controller `batch()` override), drag-drop ordering (the `ordering` column, `js-draggable` markup, AJAX save), tags integration (`TagServiceInterface`, `TaggableTableInterface`), content versioning (`VersionableModelInterface`, `#__content_types` registration, `save_history` config), workflow integration (`WorkflowServiceInterface`), the webservices API plugin (`onBeforeApiRoute`, `createCRUDRoutes`, JSON:API view), mail templates (`MailTemplate`, `#__mail_templates`), dashboard views (manifest `<dashboards>`, presets, `cpanel-*` positions), and custom form validation rules (`FormRule`, `addruleprefix`). For full code examples and the toolbar method list, read [`references/component-advanced.md`](references/component-advanced.md).

## Editor API

Joomla's Editor API provides a unified interface for WYSIWYG editors (TinyMCE, CodeMirror, None) and editor extension buttons. Coverage: the modern `JoomlaEditor` JS API (`get`, `getActive`, `getValue`, `setValue`, `getSelection`, `replaceSelection`, `disable`, `getRawInstance`, `getType`); the legacy `Joomla.editors.instances` proxy; the `JoomlaEditorDecorator` pattern for implementing a custom editor; XTD button plugins (`onEditorButtonsSetup`, `Button` class, `JoomlaEditorButton.registerAction`); the modal-button content-selection flow with `postMessage` and `joomla:content-select`; the `editor` form field type with all attributes (`buttons`, `hide`, `height`, `width`, `editor`, `filter`, `asset_field`, `created_by_field`, `syntax`); and editor plugin registration via `onEditorSetup` with `AbstractEditorProvider`.

For full code examples and the button-action behavior table, read [`references/editor-api.md`](references/editor-api.md).

## Layouts (LayoutHelper)

Joomla's layout system provides reusable, overridable PHP template fragments via `LayoutHelper::render()`. Layout IDs are dot-separated paths (`joomla.form.field.text` → `layouts/joomla/form/field/text.php`). Templates can override any layout by copying it to `templates/{template}/html/layouts/`. For the rendering API, layout-override priority table, sublayout pattern, and the list of key built-in layouts (searchtools, edit.title_alias, batch.*, content.info_block, form.renderfield, pagination.default, etc.), read [`references/layouts.md`](references/layouts.md).


## Form Fields

Joomla ships ~90 built-in form field types and a clean extension model for custom field classes. Coverage: built-in field reference (basic inputs, selection fields, file/media fields, special fields including `subform`, `rules`, `ordering`, `note`, `componentlayout`), the `subform` repeatable-group pattern with external/inline form sources, the `media` picker (`types`, `preview`, `directory` attributes), authoring custom fields by extending `ListField` / `GroupedlistField` / `FormField` / `TextField` / `PredefinedlistField`, the `addfieldprefix` form attribute, and modern layout-based field rendering with `getLayoutData()`.

For the full type reference, custom-field examples, and layout overrides, read [`references/form-fields.md`](references/form-fields.md).

## Menu Item Types (Site Views)

Menu item types define what appears in Joomla's Menu Manager. Joomla scans `components/{component}/tmpl/{view}/` for XML files: each `.xml` matching a layout name (`default.xml`, `blog.xml`, etc.) becomes a selectable menu item type. For the full XML structure (list and single-item variants), `<layout>` / `<fields name="request">` / `<fields name="params">` semantics, the `useglobal="true"` cascade rule, and the multi-layout-per-view convention, read [`references/menu-items.md`](references/menu-items.md).

## Libraries and Composer

Libraries are shared PHP packages installed under `libraries/` that any extension can consume; Composer is the package manager for any third-party PHP libs you bundle into your extension. The full reference — when to use a library vs. a helper, the `composer.json` template, the `vendor-dir: libraries/vendor` convention, runtime autoload-loading from `provider.php`, the common Joomla-ecosystem libraries to use vs. avoid duplicating, and npm front-end build tooling — lives in [`references/library.md`](references/library.md).

## Web Services API (JSON:API)

Joomla's REST layer at `/api/index.php/v1/...` speaks JSON:API and is extended in three pieces: a **webservices plugin** registering routes in `onBeforeApiRoute` (`createCRUDRoutes()` for the five CRUD routes, `Route` objects for anything custom, a per-route `public` flag that defaults to private), an **`ApiController`** in the component's `api/` tier that whitelists `filter[...]` / `list[...]` query vars into model state and reuses the **administrator** models through `ApiMVCFactory`, and a **`JsonapiView`** whose `fieldsToRenderItem` / `fieldsToRenderList` arrays are the output whitelist. Requests authenticate per call through the `api-authentication` plugin group — a Joomla API Token in `X-Joomla-Token` or `Authorization: Bearer`, HMAC-bound to the site secret — never the session cookie, so admin JS talks to a `JsonView` on the admin tier instead. Language strings load from `api/`, not `administrator/`. The reference also covers error statuses (401 vs 404 as the wiring diagnostic), CORS settings, and consuming the API with `HttpFactory`, `fetch()`, and curl. Read [`references/webservices-api.md`](references/webservices-api.md).

## Console Commands (CLI)

Extensions add commands to `php cli/joomla.php` through a plugin in the **`console`** group that subscribes to `ApplicationEvents::BEFORE_EXECUTE` and calls `$app->addCommand()` — or, like core, shares the command in the container and adds it to the writable command loader so it is only instantiated when invoked. Commands extend `Joomla\Console\Command\AbstractCommand` (`$defaultName`, `configure()`, `doExecute()` returning a Symfony `Command::SUCCESS` / `FAILURE` exit code). The console application has no document, no identity, and no HTTP host — the reference lists every web assumption that breaks under CLI and the guard for each. Standalone `cli/*.php` scripts on `CliApplication` are removed in Joomla 6. For the plugin scaffold, command template, model access via `bootComponent()`, cron / `scheduler:run` guidance, and testing, read [`references/console-commands.md`](references/console-commands.md).

## Extension Packaging (Building the Installable ZIP)

Joomla extensions ship as ZIP files installed through the admin installer (`System → Install → Extensions`). For manual packaging, the build-script pattern, package manifests (multiple extensions bundled), and the include/exclude checklist for what belongs in the ZIP, read [`references/packaging.md`](references/packaging.md).

## Real-World Reference: Production Components

When working on a Joomla project, check whether the project has its own `CLAUDE.md` or `CONTRIBUTING.md` at the repo root — these often define project-specific naming conventions, build commands, and coding standards that should take precedence over this skill's generic patterns.

Common patterns seen in production Joomla 5+ components:

- **Entity prefixes** — Some projects prefix entity names to avoid collisions (e.g., a `<Vendor>` prefix on every Model/View/Table class). Follow the project's existing convention.
- **Plugin groups** — Real components typically ship with several plugin types: content, finder (Smart Search), schemaorg (structured data), system, task (scheduled jobs), and webservices (REST API).
- **Module variants** — Both admin-side and site-side modules in `modules/admin/` and `modules/site/`.
- **Build tooling** — Composer for PHP dependencies + npm for JS/CSS asset compilation. Look for `composer.json` and `package.json` at the project root.
- **Testing** — PHPUnit for PHP (unit + integration tests in `tests/`), Jest for JavaScript. See the **Testing** section below for patterns.
- **Non-standard vendor paths** — Some projects place Composer's `vendor/` directory in a custom location (e.g., `libraries/vendor/`). Check `composer.json` for the `vendor-dir` config.
- **Media asset pipeline** — Source JS/CSS in a build directory (e.g., `build/media_source/`) compiled to `media/` via npm scripts. The `media/` directory may be gitignored.

## Testing

PHPUnit (PHP) and Jest (JavaScript) patterns for Joomla 5+ extensions, anchored on the principle Joomla core uses for its own tests: **load real CMS classes, don't stub them.** Topics covered: `tests/Unit/` + `tests/Integration/` directory layout, `phpunit.xml` configuration, the bootstrap that loads Joomla's vendor autoloader plus your component's PSR-4 autoloader, the `getQueryStub()` helper for a real `DatabaseQuery` with only 2 abstract methods stubbed, model/table/helper test patterns, Jest with jsdom for JavaScript with mocked `Joomla` globals, and four high-stakes testing gotchas (`DatabaseInterface` lacks `createQuery()`, `CMSApplicationInterface` lacks `getSession()`, the bootstrap-must-load-`libraries/vendor/autoload.php` rule, `createMock()` vs `createStub()` for expectations).

For full setup, code patterns, and gotcha details, read [`references/testing.md`](references/testing.md).

## Version Migration: Joomla 5 → 6 (and Beyond)

When migrating an extension from Joomla 5 to Joomla 6 (or writing code that supports both), apply these changes systematically:

### Step 1: Query Builder
Find all instances of `$db->getQuery(true)` and replace with `$db->createQuery()`. Both work on Joomla 5, but only `createQuery()` is guaranteed going forward.

### Step 2: Input Classes
Replace any `use Joomla\CMS\Input\Input` with `use Joomla\Input\Input`. The CMS wrapper is removed in Joomla 6. Note: `$this->input` in controllers already works correctly on both versions.

### Step 3: CMSObject → stdClass
If code uses `$item->get('property')` or `$item->set('property', $value)` on objects returned by `getItem()`, replace with direct property access: `$item->property` and `$item->property = $value`. In Joomla 6, `getItem()` returns `stdClass`, not `CMSObject`.

### Step 4: Filesystem Classes
Replace `use Joomla\CMS\Filesystem\File` / `Folder` / `Path` with PHP native functions (`file_put_contents`, `mkdir`, `is_dir`, etc.) or Symfony Filesystem. The CMS Filesystem classes move behind the compat plugin in J6 and are removed in J7.

### Step 5: Factory Methods
Search for and replace:
- `Factory::getUser()` → `$this->getCurrentUser()` (in models) or `$this->getIdentity()` (in controllers/views)
- `Factory::getApplication()` → Inject via constructor or use `$this->getApplication()`
- `Factory::getDbo()` → `$this->getDatabase()` or inject `DatabaseInterface`

### Step 6: Error Handling
Replace `$model->getError()` / `$model->setError()` patterns with try/catch and thrown exceptions (`\RuntimeException`, `\InvalidArgumentException`).

### Step 7: Test
After migration, test with the "Behaviour - Backward Compatibility 6" plugin **disabled** to confirm the extension runs natively on Joomla 6 without compatibility shims.

### Future Versions
This skill targets Joomla 6 native patterns that also work on Joomla 5. As Joomla 7+ introduces additional changes, this migration checklist will expand. The core principle remains: use the modern API from the framework layer (`Joomla\Database`, `Joomla\Input`) rather than the CMS convenience wrappers.

## Common Gotchas & Pitfalls

Hard-won lessons from real Joomla 5/6 extension development — easy to get wrong because IDE autocompletion, documentation gaps, or reasonable assumptions lead you astray. Topics covered: `BaseController` vs `FormController`, J5 controller API differences (`$this->input` not `getInput()`), event dispatching for J5 compatibility, plugin manifest naming, plugin language file conventions, task plugin language keys, **plugins loading under the console application (no `getDocument()`)**, **Web Services API language files loading from `api/` not `administrator/`**, **API 401 with a valid token (two login gates)**, **`Log::add()` to an unregistered category being silently dropped**, `AdminModel`/`Table` save workflow, `task=` routing, `form.validate` asset, `Table::check()`, HTTP client class, `Registry::get()` defaults, `Text::script()` registration, `Joomla.Text._()` truthy-key trap, batch routing, **the 3-part SEF router contract** (router class + `RouterServiceInterface` + `RouterFactory`), hidden menu items for SEF, router callback naming, **WAM URI auto-resolution / non-standard paths / inline assets**, Bootstrap 5.3 dark mode classes, dynamic modal cleanup, and `getStoreId()` in `ListModel`.

For full details and code examples, read [`references/gotchas.md`](references/gotchas.md).

