# ERB Build Rules

Rules and patterns for translating Figma designs into view-layer ERB partials in Nitro. Read alongside [SKILL.md](../SKILL.md) (the process orchestrator), [REFERENCE.md](./REFERENCE.md) (shared lookups), and [component-intelligence.md](./component-intelligence.md) (playbook-builder behavior, MCP guide, component recognition).

---

## Component-specific rules

These supplement the universal translation rules in [SKILL.md](../SKILL.md) Step 6.

### 1. Prop names: camelCase → snake_case

Convert all multi-word props from the spec:

| Spec prop | ERB prop |
|-----------|----------|
| `paddingX` | `padding_x` |
| `paddingBottom` | `padding_bottom` |
| `maxWidth` | `max_width` |
| `requiredIndicator` | `required_indicator` |
| `textTransform` | `text_transform` |
| `borderRadius` | `border_radius` |

### 2. `html_options` — avoid; use Playbook props instead

**Always prefer Playbook props over `html_options`.** Use `background: "light"` not `html_options: { style: "background-color: ..." }`. Use spacing tokens, not pixel values. Use color props, not hex values.

If `html_options` is absolutely unavoidable (no Playbook prop exists), add a comment explaining why. When using it:

- `html_options` goes **inside** the `props:` hash — never as a separate keyword (raises `unknown keyword: :html_options`)
- **Always use a CSS string for `style:`** — never a Ruby hash with symbol keys

```erb
<%# CORRECT — Playbook props for styling %>
<%= pb_rails("flex", props: { orientation: "column", background: "light" }) %>

<%# ACCEPTABLE — html_options only when no Playbook prop exists, with justification %>
<%= pb_rails("flex", props: {
  orientation: "column",
  html_options: { data: { controller: "toggle" } },
}) %>

<%# WRONG — html_options as separate keyword (raises error) %>
<%= pb_rails("flex", props: { orientation: "column" }, html_options: { style: "..." }) %>

<%# WRONG — html_options for styling that Playbook props can handle %>
<%= pb_rails("flex", props: {
  html_options: { style: "background-color: white;" },
}) %>
```

### 3. Component name mapping

| Spec component | ERB `pb_rails` name |
|---------------|---------------------|
| `BreadCrumbs` | `bread_crumbs` |
| `BreadCrumbItem` | `bread_crumbs/bread_crumb_item` |
| `Select` | `select` |
| `SelectableCard` | `selectable_card` |
| `FormGroup` | `form_group` |
| `TextInput` | `text_input` |
| `SectionSeparator` | `section_separator` |
| `FlexItem` | `flex/flex_item` |
| `NavItem` | `nav/item` |
| `LoadingInline` | `loading_inline` |
| `Card.Header` | `card/card_header` |
| `Table.Head` | `table/table_head` |
| `Table.Row` | `table/table_row` |
| `Table.Header` | `table/table_header` |
| `Table.Cell` | `table/table_cell` |
| `Dialog.Header` | `dialog/dialog_header` |
| `Dialog.Body` | `dialog/dialog_body` |
| `Dialog.Footer` | `dialog/dialog_footer` |

All other components use lowercase: `Title` → `title`, `Body` → `body`, `Card` → `card`, `Flex` → `flex`, `Button` → `button`.

**Sub-component pattern:** ERB uses slash notation for sub-components, not underscores: `nav/item`, `table/table_row`, `flex/flex_item`. Never write `nav_item` or `table_row`.

### 4. Text content: `text:` prop or `do...end` block

Simple text uses the prop. Complex/nested content uses blocks.

```erb
<%# Simple text %>
<%= pb_rails("title", props: { text: "Page Title", size: 3, bold: true, color: "default" }) %>

<%# Block content %>
<%= pb_rails("card", props: { padding: "md" }) do %>
  <%= pb_rails("body", props: { text: "Content here" }) %>
<% end %>
```

### 5. Select — use `options:` prop with `blank_selection:`

**Never use raw `<option>` HTML in a `do...end` block.** It bypasses Playbook styling.

```erb
<%# CORRECT %>
<%= pb_rails("select", props: {
  blank_selection: "All Territories",
  label: "Territory",
  name: "record[territory]",
  options: @territory_options.map { |o| { value: o.id, value_text: o.name } },
}) %>

<%# WRONG — unstyled, no border %>
<%= pb_rails("select", props: { label: "Territory" }) do %>
  <option value="">All Territories</option>
  <option value="east">Eastern</option>
<% end %>
```

### 6. `textAlign` on containers — skip it

Same as React: Figma's `textAlign: center` on frames means "center children." CSS cascades `text-align` to all descendant text. Apply only to `Title`, `Body`, `Caption`, `Detail`.

### 7. Component `text` exceptions

| Component | Spec `text` | Use instead |
|-----------|------------|-------------|
| `Timestamp` | Display text — ignore | `timestamp: 30.minutes.ago` |
| `Avatar` | Layer name — ignore | `name: "Full Name"` |

### 8. Component prop gotchas

These are **Playbook component behaviors** documented in `.cursor/rules/playbook-components.mdc`. During Figma builds, watch for these spec-to-code translation mistakes:

- **Pill / Badge** — `text:` prop is **required**. Use `text: "Review"`, never a `do...end` block with plain text. See `playbook-components.mdc` → Pill, Badge.
- **`required_indicator` vs `required`** — The spec emits `requiredIndicator` (→ `required_indicator` in ERB). Use that for the visual `*`. `required` is HTML5 validation — a separate concern. See `playbook-components.mdc` → TextInput, Textarea.
- **SectionSeparator** — Renders at zero width by default. Always add `width: "100%"`. See `playbook-components.mdc` → SectionSeparator.

### 9. DatePicker requires `picker_id`

```erb
<%= pb_rails("date_picker", props: { picker_id: "purchase-date" }) %>
```

### 10. Content area `max_width`

**Every content column must be checked for max_width.** The spec now emits `dimensions` on all layout nodes (not just FIXED), so you always have width data.

**When the spec includes `maxWidth`:** Convert to `max_width` and use directly.

**When the spec omits `maxWidth`:** Check `dimensions.width` on the content column. If it exceeds ~1240px and the column contains form fields, add a manual constraint. See [component-intelligence.md](./component-intelligence.md) → "Form pages without maxWidth" for the heuristic table.

Tokens: `"sm"` (~480px), `"md"` (~720px), `"lg"` (~960px). Add `margin: "auto"` when present.

```erb
<%= pb_rails("flex", props: {
  margin: "auto",
  max_width: "md",
  orientation: "column",
  width: "100%",
}) do %>
  <%# form content %>
<% end %>
```

---

## Minimal rendering controller

**Inspect existing files first.** Most components already have routes and controllers. If they exist, add to them — never overwrite. If missing, create the minimum needed to display the page.

This is **not application architecture.** It is the minimum to render the view. Data loading, model queries, and form processing are the developer's responsibility.

| File | If exists | If missing |
|------|-----------|------------|
| `config/routes.rb` | **Add** route to existing routes block | Add `get` route |
| `app/controllers/<ns>/<page>_controller.rb` | Use it — do not modify | Create with empty `index` action |
| `app/views/<ns>/<page>/index.html.erb` | Unlikely to exist — create new | Create new |
| `app/views/<ns>/<page>/_header.html.erb` | Create new partial | Create new partial |

**Controller pattern (empty — no data loading):**

```ruby
module MyComponent
  class PagesController < ApplicationController
    # TODO: Add data loading (model queries, API calls) here
    def index; end
  end
end
```

### File structure: partials, not TSX

Each section is an ERB partial. Render with `<%= render "header" %>`.

---

## Code patterns

```erb
<%= pb_rails("card", props: { padding: "md", width: "100%" }) do %>
  <%= pb_rails("flex", props: { orientation: "column", gap: "sm" }) do %>
    <%= pb_rails("title", props: { text: "Page Title", size: 3, bold: true, color: "default" }) %>
  <% end %>
<% end %>

<%= pb_rails("text_input", props: {
  label: "GL Code",
  required: true,
  required_indicator: true,
  placeholder: "00-00-0000",
}) %>

<%= pb_rails("flex", props: { orientation: "row", gap: "md" }) do %>
  <%= pb_rails("card", props: { flex: "2", padding: "md" }) do %>
    <%# left column %>
  <% end %>
  <%= pb_rails("flex", props: { flex: "3", orientation: "column" }) do %>
    <%# right column %>
  <% end %>
<% end %>

<%= pb_rails("bread_crumbs", props: { padding_bottom: "md" }) do %>
  <%= pb_rails("bread_crumbs/bread_crumb_item") do %>
    <%= pb_rails("title", props: { text: "Parent", color: "link", size: 4, tag: "span" }) %>
  <% end %>
<% end %>
```

---

## Mock data for backend handoff

ERB builds need structured mock data so developers can replace it with real backend calls later. Define mock data at the top of the main view or in the controller action.

**In the view (demo/prototype pages):**

```erb
<%
records = [
  { name: "Tier 1", role: "Revenue Recruiter", status: "Active", pay: "$50,000/yr" },
  { name: "Tier 2", role: "Senior Recruiter", status: "Active", pay: "$65,000/yr" },
]

filter_options = [
  { value: "people", value_text: "People" },
  { value: "operations", value_text: "Operations" },
]
%>
```

**In the controller (when backed by models):**

```ruby
def index
  @records = Record.active.order(:name)
  @filter_options = Department.pluck(:id, :name).map { |id, name| { value: id, value_text: name } }
end
```

**Rules:**
- Use **realistic values from the Figma spec text** — not "test", "lorem ipsum", or placeholder strings
- Include **3-5 rows** for table/list data so layout is visually verified
- Select/dropdown options: **3-5 realistic entries** matching the design's domain
- Add a `# TODO: Replace with real data from controller` comment above mock data blocks so backend developers can find and replace them
- Structure mock data as an array of hashes matching the shape the view iterates over

---

## Client-side interactivity (Stimulus)

Use Stimulus for UI interactions that don't need a server round-trip: show/hide panels, toggle sections, switch tabs, client-side validation.

Form submission (`form_with`), Turbo Frames, and server-driven interactions are the developer's responsibility. Use TODO comments where these belong:

```erb
<%# TODO: Wrap in form_with when controller action is ready %>
<%# TODO: Wrap in turbo_frame_tag when controller action is ready %>
```

### Stimulus wiring

| File | Purpose |
|------|---------|
| `app/javascript/entrypoints/stimulus/<component>.js` | Loads Stimulus for this component |
| `app/javascript/stimulus.js` | Creates `Application.start()`, registers controllers |
| `app/javascript/controllers/<name>_controller.js` | Individual Stimulus controller |

**View:** `<%= vite_javascript_tag "entrypoints/stimulus/<component>" %>`

```javascript
// controllers/toggle_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["content"]
  toggle() { this.contentTarget.classList.toggle("hidden") }
}
```

---

## Format and lint

```bash
bin/rubocop app/views/your_controller/ app/controllers/your_controller.rb
bundle exec erb_lint app/views/your_controller/
```

Key rules:
- **Trailing commas** in multiline hashes (RuboCop `TrailingCommaInHashLiteral`)
- **snake_case** for all prop names
- **Playbook props only for styling** — no inline styles, no hex values, no pixel values
- **`html_options` inside `props:`** — if used at all, never as a separate keyword

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `unknown keyword: :html_options` | `html_options` outside `props:` | Move inside `props:` hash |
| `pb_rails` not found | Missing `Playbook::PbKitHelper` | Add to ApplicationController |
| No red asterisk | Missing `required_indicator` | Add `required_indicator: true` with `required: true` |
| Prop doesn't work | camelCase instead of snake_case | Convert: `paddingX` → `padding_x` |
| `justify: "spaceBetween"` fails | Wrong value | Use `"between"` |
| `in_time_zone` for nil | `timestamp` missing DateTime | Use `timestamp: 30.minutes.ago` |
| Select unstyled / options missing | Raw `<option>` HTML in block | Use `options:` with `blank_selection:` |
| Page outside Nitro shell | Missing layout | Add `layout "nitro_theme/application"` |
| 404 | Engine not mounted | Add to `config/routes.rb` |
