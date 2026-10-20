# Home Assistant

## Instructions

- After each meaningful change to the configuration, run `pnpm reload`, then check runtime logs via `pnpm home-assistant raw request GET /api/hassio/core/logs --text` (Supervisor) to confirm there are no warnings or errors related to the changes.
- If `/api/hassio/core/logs` is unavailable or returns an upstream error, fall back to `pnpm home-assistant error-log` and continue the runtime validation there.
- If you add brand-new `input_*` helpers, be prepared to restart Home Assistant core before first-time seeding or runtime verification; `pnpm reload` does not always register new helper entities on its own.
- When changing helper `initial` values, do not assume `pnpm reload` will update existing live helper states. Verify the runtime state explicitly, and use a service call or one-time migration if existing installs must adopt the new values immediately.
- For user-editable helper migrations, prefer explicit one-time post-reload seeding plus state verification over startup or `automation_reloaded` reseeding; recurring reseed automations will overwrite later user changes.
- For runtime-only settings that cannot be templated in static package config, use a helper-backed script or automation and trigger it on `automation_reloaded` in addition to startup so `pnpm reload` reapplies the live settings without a full restart.
- `pnpm home-assistant` requires Node.js `>= 22.6.0` (see `bin/cli/README.md`).
- Do not use `mode: single` in automations since it is the default
- Do not use empty conditions
- Do not add erronenous keys where the value is the same as the default value
- Comments should be at the beginning of a code block, and not at the end.
- All package names, ids, unique_ids, entity_ids, etc. should use snake_case.
- When a package needs `input_*` helpers, keep those helper definitions in a separate standalone package file instead of mixing them into the package's `automation`, `script`, or integration logic. When one feature spans multiple input domains, prefer a feature-scoped `_input` package key such as `shared_background_music_input`.
- User-configurable values should be helper-backed instead of hard-coded inside automation, script, or integration logic. When migrating existing values into helpers, avoid YAML `initial` for user-editable defaults and preserve current live behavior with one-time post-reload seeding plus explicit state verification. Newly added helper entities may still require a core restart before that first seed or verification step. Keep any legacy defaults confined to that one-time/manual seed path; runtime scripts and automations should fail closed when required helper state is blank or unavailable.
- For area automations that share a trigger across multiple concerns, prefer nested trigger directories with one automation per concern, for example `tv/on/lights.yaml` and `tv/on/blinds.yaml`, instead of a single mixed `on.yaml` or `off.yaml` package.
- For sunset window automation, prefer helper-backed positions instead of hard-coded ones. The living room pattern (`packages/areas/living_room/blinds/sunset.yaml` with `packages/areas/living_room/blinds/sunset_position.yaml`) turns off `input_boolean.living_room_blinds_automatic` and then sets `cover.living_room_blinds` position from `input_number.living_room_blinds_sunset_position`; newer blinds features should follow this helper-backed pattern over the older hard-coded `bedroom/blinds/sunset.yaml`.
- Room-specific Configuration views in the Rooms dashboard should live at `includes/lovelace/views/<area>/configuration.yaml` with `subview: true`, use `type: sections` or omit `type` when relying on the default, declare their content under a top-level `sections:` list instead of a top-level `cards:` list, group surfaced entities into concern-based section blocks, use multiple sections when multiple concerns are surfaced, and allow a single named section when only one concern is present. Use built-in card types, place one built-in `entities` card in each concern section, preserve the entity ordering within that section, omit the area name from labels, include only entities created or configured by YAML packages under `packages/`, be included from `includes/lovelace/dashboards/dashboard_room.yaml`, and be opened from a dedicated Configuration tile in the area view with `navigation_path: /dashboard-room/<area>-configuration`. Keep that Configuration tile as the last item on its row in the area view.
- The unified helper dashboard lives at `includes/lovelace/dashboards/configuration.yaml` with detail views under `includes/lovelace/views/configuration/`. Surface every YAML-defined `input_*` helper under `packages/` there exactly once, grouped by shared concerns and each helper-owning area or scope, while keeping the Rooms dashboard Configuration subviews intact.
- Use the `notify.mobile_app_pixel_6_pro` service for all mobile notifications.

Use the `flex-card` and `grid-card` to create a responsive layout.

Avoid using `grep` in the root directory. Instead, use it within specific subdirectories to limit the scope of the search and improve performance.

Use the `pnpm home-assistant` command to run Home Assistant CLI commands. The documentation is located in the `bin/cli` directory.

- Bedroom AC presence-off: `packages/areas/bedroom/presence/off/thermostat.yaml` now turns both thermostats fully off (`climate.turn_off`) after a 15 s presence-off hold — the old `for: {minutes: 1}` hold plus setpoint-only actions was the defect (it never fired); the `script.bedroom_air_conditioner_off` debounce is bounded to 30 s via `timeout: '00:00:30'`.
- Expose the combined `climate.bedroom_thermostat` climate group to Google Assistant, not its separate heat and cool implementation entities, so whole-home thermostat commands use the group's `off` mode and propagate to both members.
- Keep helper-only packages separate even when the related behavior package contains only integration metadata such as `google_assistant.entity_config`; preserve the helper entity ID and move its definition into a sibling `_input` package.
- For local runtime validation from the Home Assistant host, pass `-H http://localhost:8123` to `pnpm home-assistant` when the configured external URL is slow or unavailable.
- The bedroom sunset and TV-idle blind position intentionally share `input_number.bedroom_blinds_sunset_position`; the live migration default was seeded once to 75 after the helper was registered.
- Background music uses Music Assistant library URIs such as `library://radio/2`; opaque numeric media IDs can become unresolvable. Keep the play and stop target helpers pointed at the Music Assistant player entity, trim text-helper values when consuming them, and gate scheduled play/stop actions with the per-day enable helpers.

## Commands

- Use `ha core logs` to view Home Assistant core logs.
- Use `ha core restart` to restart Home Assistant core.
