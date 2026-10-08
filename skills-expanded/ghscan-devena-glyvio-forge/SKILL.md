---
name: create-list-page
description: "Generates a standard entity list page with search, sidebar filtering, routing, and menu registration for a Glyvio plugin."
---
<!-- Generated from src/skills/create-list-page/SKILL.md by tools/generate.py. Edit the source, not this file. -->
# Agent Skill: Create Custom List Page View in Glyvio

This document defines a structured AI agent skill. Other AI coding agents or developers can load and execute this skill to generate a fully functional list page view (extending `SimpleListPage`) within a Glyvio plugin project.

---

## 🎯 Skill Metadata

```json
{
  "name": "create_list_page",
  "description": "Generates a standard entity list page with search, sidebar filtering, routing, and menu registration for a Glyvio plugin.",
  "Audience": "AI agents or developers with write access to a Glyvio plugin codebase.",
  "parameters": {
    "type": "object",
    "properties": {
      "entityName":       { "type": "string", "description": "Entity model name in glyvio_entity.* (e.g., Product, Customer)" },
      "pluginNamespace":  { "type": "string", "description": "Plugin namespace string (e.g., my_plugin)" },
      "routePath":        { "type": "string", "description": "URL path starting with / (e.g., /products)" },
      "titleField":       { "type": "string", "description": "Primary field displayed on each list card (e.g., name)" },
      "subtitleField":    { "type": "string", "description": "Secondary field displayed below the title (e.g., code)" },
      "sidebarFilters":   { "type": "array", "items": { "type": "string" }, "description": "Field names to expose as sidebar filter controls" },
      "mainSearchFields": { "type": "array", "items": { "type": "string" }, "description": "Fields matched when typing in the top search bar" },
      "menuGroup":        { "type": "string", "description": "Menu group key and display name where the page item will appear" }
    },
    "required": ["entityName", "pluginNamespace", "routePath", "titleField", "mainSearchFields", "menuGroup"]
  }
}
```

---

## 📥 Required Input Parameters

To run this skill, the agent must obtain or ask for the following inputs:

1. **Entity Name** (e.g., `Product`, `Customer`): The name of the model in `glyvio_entity.*` to list.
2. **Plugin Namespace** (e.g., `my_plugin`): The namespace registered for the plugin.
3. **Route Path** (e.g., `/products`): The URL path (must start with `/` and be a single word/slug).
4. **Display Fields**:
   - **Title field** (e.g., `name`): The field to display as the primary text of each list card.
   - **Subtitle field** (e.g., `code`, `description`): The field to display as secondary text.
5. **Sidebar Filters** (e.g., `status`, `category`): Fields to build filter controls for.
6. **Main Search Fields** (e.g., `name`, `code`): Fields matched when typing in the top search bar.
7. **Menu Group** (e.g., `Administration` group key: `main-admin`): Where to place the menu item.

---

## 🚫 Environment Constraints & Rules

The executing agent MUST strictly adhere to these rules:

1. **No External Imports for Glyvio Globals**: Glyvio classes, decorators, services, and entities are injected globally at runtime. Do NOT import them from core packages.
   - _Example:_ Use `new glyvio_core.CellDesign(...)`, NOT `import { CellDesign } ...`
2. **Routing Rules**: `getRoutePath()` must return a path starting with `/` followed by alphanumeric characters or underscores (no trailing slashes, no multiple segments unless URL-encoded).
3. **Data Types & Models**: All referenced model fields must exist under the namespace `glyvio_entity.<EntityName>`.
4. **No any or force cast**: Do not use `any` or force cast to `any` to resolve type errors. Find another way to solve the problem.
5. **Interpolation syntax — use the correct prefix for each type**:
   - `$S{...}` → String/text values.
   - `$D{...}` → **DateTime only**. NEVER use for Decimal or numeric fields.
   - `$N{...}` → Decimal/Number (counts, amounts, any `Decimal` type).
   - `$T{...}` → Translation/i18n key.

---

## 📋 Execution Steps

The agent must perform the following actions:

### Step 1: Create the Page View and Route File

Create a new file `src/views/pages/<entity_snake_case>_list_page.ts` inside the target plugin's codebase and write the implementation using the blueprint below.

### Step 2: Register the Route

Add the route class to the routing configuration array (typically inside `src/index.ts` where other routes are loaded):

```typescript
glyvio_core.routerService.loadRoutes([
  // ... other routes
  YourEntityListPageRoute,
]);
```

### Step 3: Register the Main Navigation Menu Item

Register the view in the main app menu sidebar:

```typescript
glyvio_core.FullMenuPage.fullMenuGroupAdd({
  key: 'group_key',
  name: 'Group Name',
  position: 100, // Customize positioning
  items: [
    {
      key: 'menu-item-your-entity',
      title: 'Your Entity Title',
      iconName: 'fa_list', // FontAwesome icon
      colorTheme: 'BLUE', // Theme color
      route: new YourEntityListPageRoute(),
    },
  ],
});
```

---

## 📄 Code Blueprint (Template)

Replace all placeholder values wrapped in `<...>` with the corresponding input parameters:

```typescript
// Define state filters for the sidebar
export interface <EntityName>ListFilter extends glyvio_core.SimpleListPageStateFilter {
  // Add sidebar filters here (e.g., status?: string;)
  <filterField1>?: string;
  <filterField2>?: boolean;
}

// Define route params
export interface <EntityName>ListRouteParams extends glyvio_core.SimpleListPageRouteParams<<EntityName>ListFilter> {}

// Define page state
export interface <EntityName>ListPageState
  extends glyvio_core.SimpleListPageState<<EntityName>ListRouteParams, <EntityName>ListFilter> {}

/**
 * Route definition for the <EntityName> List Page.
 */
export class <EntityName>ListPageRoute extends glyvio_core.SimpleListPageRoute<<EntityName>ListRouteParams> {
  getRoutePath() {
    return '<RoutePath>'; // e.g., '/products'
  }

  getRouteNameSpace() {
    return '<PluginNamespace>';
  }

  getRouteNameObject() {
    return '<EntityName>ListPage';
  }
}

/**
 * Custom List Page component for displaying <EntityName> entities.
 */
export class <EntityName>ListPage extends glyvio_core.SimpleListPage<<EntityName>ListPageState, glyvio_entity.<EntityName>> {
  constructor() {
    super(<EntityName>ListPageRoute);
    this.extensionsManager.registerReport(this);
  }

  async initState(state: <EntityName>ListPageState): Promise<void> {
    await super.initState(state);
    state.userConfigKey = '<ENTITY_NAME_UPPER>_LIST_PAGE';
    await this.loadUserConfig(state);
  }

  /**
   * Configures the title and sidebar filter UI elements.
   */
  getDesign(state: <EntityName>ListPageState, design: glyvio_core.SimpleListPageDesign): void {
    const appBar = design.appBarDesign as glyvio_core.SimpleAppBarDesign;
    appBar.title = '<EntityName> List';
    appBar.putButtonOn(this.extensionsManager.report!.getButton());

    // Build sidebar filter components
    design.filterSectionsDesign?.push(
      new glyvio_core.FormSectionDesign({
        childDesign: new glyvio_core.FormLayoutDesign({
          columnSize: 280,
          children: [
            new glyvio_core.FormLayoutFieldDesign({
              key: '<filterField1>.formField',
              child: new glyvio_core.StringTextfieldDesign({
                name: 'state.filtersSidebar.<filterField1>',
                label: 'Filter Label 1',
              }),
            }),
          ],
        }),
      }),
    );
  }

  /**
   * Formats how each entity card is displayed in the list view.
   */
  getDesignForCell(state: <EntityName>ListPageState, item: glyvio_entity.<EntityName>): glyvio_core.LineCellDesign {
     return new glyvio_core.LineCellDesign({
      colorTheme: item.deleted ? 'RED' : null,
      padding: '16',
      child: new glyvio_core.RowLayoutDesign({
        crossAlignment: 'CENTER',
        children: [
          new glyvio_core.RowLayoutFieldDesign({
            isExpanded: true,
            child: new glyvio_core.ColumnLayoutDesign({
              key: 'nameField',
              children: [
                new glyvio_core.StringTextDesign({
                  value: item.<TitleField> ?? 'Unnamed Item',
                  padding: '0 4',
                }),
                new glyvio_core.StringTextDesign({
                  value: item.<SubtitleField> ?? '',
                  style: 'BODY_SMALL',
                }),
              ],
            }),
          }),
          new glyvio_core.ChipDesign({
            key: 'statusField',
            label: item.<StatusField> ?? '',
            colorTheme: `GREEN`,
          }),
        ],
      }),
    });
  }

  /**
   * Builds the database select query and applies sidebar filters.
   */
  populateQueryBuilder(
    state: <EntityName>ListPageState,
    queryBuilder: glyvio_core.QueryBuilder<glyvio_entity.<EntityName>>,
  ): void {
    queryBuilder.setFromEntity(glyvio_structure.AllEntities.<entityNameCamelCase>);
    queryBuilder.addOrderByEntity(glyvio_structure.AllEntities.<entityNameCamelCase>.<TitleField>, 'ASC');

    // Apply active sidebar filters to query
    // e.g.: if (state.filtersSidebar?.<filterField1>) {
    //   queryBuilder.addFilterOperator(glyvio_structure.AllEntities.<entityNameCamelCase>.<filterField1>, state.filtersSidebar.<filterField1>);
    // }
  }

  /**
   * Formats query filter matching the main top search bar input.
   */
  populateMainFilter(_state: <EntityName>ListPageState, text?: string): glyvio_core.QueryBuilderFilter {
     return new glyvio_core.QueryBuilderFilter({
      ors: [
        new glyvio_core.QueryBuilderFilterILike({
          field: glyvio_structure.AllEntities.<entityNameCamelCase>.<TitleField>,
          value: text,
        }),
      ],
    });
  }

  /**
   * Defines navigation action when a cell is clicked/tapped.
   */
  async onCellTap(state: <EntityName>ListPageState, item: glyvio_entity.<EntityName>): Promise<void> {
    // Implement navigation or callback here
    // e.g., await this.pushRoute(new <EntityName>EditPageRoute({ id: item.id }));
  }

  /**
   * Hooks into activity/telemetry tracking.
   * structureName must be glyvio_structure.AllEntities.<entityNameCamelCase>.getStructureName()
   * ex: glyvio_structure.AllEntities.appUser.getStructureName()
   */
  getEntitiesListenning(_state: <EntityName>ListPageState): glyvio_core.EntityListenning[] {
    return [
      new glyvio_core.EntityListenning({
        objectId: '*',
        structureName: glyvio_structure.AllEntities.<entityNameCamelCase>.getStructureName(),
      }),
    ];
  }

  /**
   * Hooks into activity/telemetry tracking.
   */
  getEntityToTracking(item: glyvio_entity.<EntityName>): { structureName: string; objectId: string } | undefined {
    return {
      structureName: glyvio_structure.AllEntities.<entityNameCamelCase>.getStructureName(),
      objectId: item.id,
    };
  }
}
```

> **Sobre o botão de report acima** — `registerReport(this)` + `getButton()` expõem o seletor
> **nativo de Report Records** (`glyvio_entity.Report`, o modelo configurado pelo app), não um
> controller que você tenha escrito. O seletor só lista registros cujo `screenPaths` contenha
> `{ path: '<o path desta rota>', type: '<o tipo desta rota>' }` — ou seja, **vincular um relatório
> a esta tela é cadastro, não código**. A tela não precisa implementar nada: `openExternalUrl` já
> vem de `CoreView`.
>
> Para abrir uma **Custom Page** (HTML/Plotly gerada pelo `glyvio-custom-page-agent`), não use
> este botão — adicione um `ActionButtonDesign` comum e, na action, chame
> `await this.openCustomPage(name, isPublic?, parameters?)`, retornando `'STATE_FREEZED'`.
> **Não monte a URL à mão**: o cliente Flutter resolve BASE_URL, company id e token sozinho, e
> converte `parameters` em query string. Do lado do controller eles chegam em
> `WebRequest.requestParams` sempre como **string** e são **entrada não confiável** — valide e
> reautorize no servidor. Ver a skill `create-custom-page`.
