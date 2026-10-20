---
name: dart-models
description: Dart model standards — freezed + json_serializable code generation, JSON key mapping, closed-set enums with an unknown fallback, DTO vs domain model split, nullability, UTC date handling, and derived getters. Load when defining or changing a Dart domain model or an API DTO.
user-invocable: false
stack: language/dart-models
paths:
  - "**/domain/models/*.dart"
  - "**/domain/**/*.dart"
  - "**/data/dto/*.dart"
---

Full standards in [dart-models.md](dart-models.md). Always-on summary.

**Scope:** model shape and serialization only. Fetching, `Dio`, interceptors and error mapping are `api-style/dio`. Provider wiring and caching are `state/riverpod`. Field and file naming is `naming-conventions`.

**Generation:**
- Every model is `@freezed` with `part '<file>.freezed.dart';` and `part '<file>.g.dart';`, and a `fromJson` factory delegating to `_$<Model>FromJson(json)`. Never hand-write `fromJson`/`toJson`.
- Freezed gives value equality for free. Without it Riverpod rebuilds the widget tree on every identical refetch.
- Regenerate with `dart run build_runner build --delete-conflicting-outputs`.

**No unchecked casts:**
- `strict-casts: true` in `analysis_options.yaml`, alongside `errors: invalid_annotation_target: ignore` (freezed puts `@JsonKey` on factory params). `json['name'] as String` is the symptom `strict-casts` exists to make impossible.

**Closed sets are enums:**
- `enum` with `@JsonValue('...')` per member, an `unknown` member, and `@JsonKey(unknownEnumValue: X.unknown)` on the field. A new server value must not crash the parse.
- Compare enum members; never compare strings (`status == 'active'`) at a call site.

**DTO vs domain:**
- Put a DTO in `data/dto/` when the wire shape is awkward — `_id`, snake_case, nullable-on-wire-but-required-in-domain — with a `toDomain()` method on the DTO. `@JsonKey(name: '_id')` for a simple rename; a DTO when the shape genuinely differs. `domain/` never imports `data/`.
- Nullable means the UI has a state for it. Never nullable to dodge a parse error.

**Dates:** parsed to UTC through a `JsonConverter`, stored UTC, `.toLocal()` only at the display edge, formatted with `intl` `DateFormat`.

**Derived values are getters** on the model (`const Model._();` unlocks them). Never stored fields that can disagree with their inputs.

**Never:** import `package:flutter/...` inside `domain/` · commit a generated `*.g.dart`/`*.freezed.dart` conflict · use `dynamic` as a model field type.

**Related:** `api-style/dio`, `state/riverpod`, `naming-conventions`, `type-safety`.
