---
name: recording-studio-new-recordable
description: Add or register a Recording Studio recordable type with hierarchy declarations, product labels, and tests. Use when creating a new recordable class, root, or nested model — not for webhook deliveries, audit exhaust, or other logs.
---

# New recordable

Follow Recording Studio's public API. Do not invent private registrar internals.

First decide whether this belongs in the tree at all (`recording-studio-data-shape`). Facts, exhaust, derived data, and high-volume rows are logs or separate tables — not a new recordable type. Mixins are opt-in later (`recording-studio-capabilities`).

## When to use

- Adding a new recordable type to a host app or addon gem
- Declaring root vs nested hierarchy rules
- Wiring labels, table names, and tests for a new type

## Steps

1. Create a lean recordable model. Snapshot tables should not need `updated_at`. Prefix tables with `recording_studio_` when the model lives in an engine.

2. Declare hierarchy on the model. The `label` is **product language** people may see — never “Recordable” or “Recording”:

```ruby
class Workspace < ApplicationRecord
  recording_studio_recordable label: "Workspace", root: true
end

class Page < ApplicationRecord
  recording_studio_recordable label: "Page",
                              root: false,
                              allowed_parent_types: ["Workspace", "Page"]
end
```

3. Register the type in the host initializer:

```ruby
RecordingStudio.configure do |config|
  config.recordable_types = ["Workspace", "Page"]
end
```

4. Validate declarations:

```ruby
RecordingStudio.validate_recordable_declarations!
```

5. Write with the `Recording` helpers `recording.record` / `#revise` / `#log_event!`; they wrap the low-level `RecordingStudio.record!`, which you use directly only when you need the returned event or lower-level control. Do not insert recordings by hand.

```ruby
root = RecordingStudio.root_recording_for(workspace)
root.record(Page) { |page| page.title = "Getting started" }
```

6. Enable only the mixins this type needs (`recording-studio-capabilities`).

## Guardrails

- Writes: `recording-studio-saving`.
- Prefer public helpers such as `RecordingStudio.root_allowed?` and `RecordingStudio.parent_allowed?`.
- Cover declaration, root rejection, and parent rejection in Minitest.
- `label` is product language (`recording-studio-text`) — never “Recordable.”
