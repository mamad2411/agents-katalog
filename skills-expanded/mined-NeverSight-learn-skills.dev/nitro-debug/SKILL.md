---
name: nitro-debug
description: For projects using nitro-web only. Debugging a nitro-web app. Use when something returns no data, a filter or save silently fails, types break, or you need to trace a request end to end.
---

  Most failures sit between two adjacent hops in the request flow, see the nitro-overview skill for the flow. Find the hop first and read both sides, rather than reading the whole feature.

# Common issues and their causes

  - **List is empty but the data exists.** Either the tenant scope matches nothing, or the query key is not in the `parseFilters` whitelist. Log the built `query` object in the controller.
  - **A field disappears on save.** It is missing from `fields` in the model, monastery strips unknown keys.
  - **A filter in the UI does nothing.** The page's filter array and the server whitelist are out of sync.
  - **Type error on an enum value.** The constants chain was only half updated, see the nitro-model skill.
  - **Dropdown shows stale options.** A shared collection is cached on the store and needs invalidating.
  - **Validation error with no visible message.** `setState` was not passed to `request`, or the field path is missing from the `<FormError fields={[...]}>` list.
  - **Table cell renders nothing.** `generateTd` has no case for that column, check the console.
  - **Deleted rows still listed.** The model soft deletes but a read query is missing the filter.
