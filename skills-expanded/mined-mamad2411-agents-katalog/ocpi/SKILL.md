---
name: ocpi
description: >-
  OCPI: Open Charge Point Interface version 2.2.1. Covers OCPI 2.2.1. Use when exchanging charge-point roaming data. Triggers: OCPI, OCPI 2.2.1.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# OCPI

Open Charge Point Interface (OCPI) 2.2.1, from the 2.2.1 tag. This skill pins the locations, sessions, tokens, CDRs, commands and tariffs modules fetched from that tag.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text when exchanging OCPI roaming data for locations, sessions, tokens, tariffs, CDRs or commands.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: a CPO or an eMSP.
- Target version: OCPI 2.2.1 (current) — default. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **text.** "When the CPO wants to delete an EVSE from the list of active EVSEs, they MUST update the EVSE's `status` field to `REMOVED` and call the <<mod_locations_put_method,PUT>> or <<mod_locations_patch_method,PATCH>> on the eMSP system."
2. **2.2.** "In order for this to work properly, the following logic MUST be implemented accordingly: If an EVSE is updated, also the 'parent' Location's `last_updated` field needs to be updated."
3. **text.** "When the PUT only contains a <<mod_locations_evse_object,EVSE>> Object, the Receiver SHALL also set the new `last_updated` value on the parent <<mod_locations_location_object,Location>> Object."
4. **text.** "[[mod_sessions_reservation]] ==== Reservation When a EV driver makes a Reservation for a Charge Point/EVSE, the Sender SHALL create a new Session object with `status` = `RESERVED` When the Push model is used, the CPO SHALL push the new Session object to the Receiver."
5. **text.** "[[mod_sessions_msp_get_request_parameters]] ====== Request Parameters The following parameters shall be provided as URL segments."
6. **text.** "If the new <<mod_sessions_session_object,Session>> object does not contain `charging_periods` (field is omitted or contains any empty list), the `charging_periods` of the existing object SHALL be removed (replaced by the new empty list)."
7. **text.** "NOTE: If real-time authorization is asked for a location, the eMSP SHALL NOT validate that charging is possible based on information like opening hours or EVSE status etc."
8. **text.** "This SHALL be the same value as the `country_code` in the Token object being pushed."
9. **text.** "Examples: `+https://www.server.com/ocpi/emsp/2.2/tokens/012345678/authorize+` `+https://ocpi.server.com/2.2/tokens/012345678/authorize?type=RFID+` When the eMSP does not know the Token, the eMSP SHALL respond with an HTTP status code: 404 (Not Found)."
10. **text.** "This credit CDR SHALL have a different CDR.id which can be a completely different number, or it can be the id of the original CDR with something appended like for example: `-C` to make it unique again."
11. **text.** "The Credit CDR references the old CDR via the <<mod_cdrs_cdr_object,`credit_reference_id`>> field, which SHALL contain the <<mod_cdrs_cdr_object,`id`>> of the original CDR."
12. **2.2.** "The _CDR_ object shall always contain information like Location, EVSE, Tariffs and Token as they were _at the start_ of the charging session."
13. **text.** "|=== [[mod_commands_cpo_post_request_body]] ===== Request Body Depending on the `command` parameter the body SHALL contain the applicable object for that command."
14. **text.** "The Token provided by the eMSP for the `ReserveNow` SHALL be authorized by the eMSP before sending it to the CPO."
15. **text.** "If this is an OCPP Charge Point, the Charge Point decides if it needs to validate the given Token, in such case: - If this Token is of type `AD_HOC_USER` or `APP_USER` the CPO SHALL NOT do a <<mod_tokens.asciidoc#mod_tokens_real-time_authorization,realtime authorization>> at the eMSP for this."
16. **text.** "[[mod_tariffs_msp_get_request_parameters]] ====== Request Parameters The following parameters SHALL be provided as URL segments."
17. **text.** "|=== [[mod_tariffs_msp_put_request_parameters]] ====== Request Parameters The following parameters SHALL be provided as URL segments."
18. **text.** "This SHALL be the same value as the `country_code` in the Tariff object being pushed."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the heading it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [OCPI 2.2.1 locations](https://raw.githubusercontent.com/ocpi/ocpi/2.2.1/mod_locations.asciidoc): Specification, OCPI 2.2.1, checked 2026-10-06.
- [OCPI 2.2.1 sessions](https://raw.githubusercontent.com/ocpi/ocpi/2.2.1/mod_sessions.asciidoc): Specification, OCPI 2.2.1, checked 2026-10-06.
- [OCPI 2.2.1 tokens](https://raw.githubusercontent.com/ocpi/ocpi/2.2.1/mod_tokens.asciidoc): Specification, OCPI 2.2.1, checked 2026-10-06.
- [OCPI 2.2.1 CDRs](https://raw.githubusercontent.com/ocpi/ocpi/2.2.1/mod_cdrs.asciidoc): Specification, OCPI 2.2.1, checked 2026-10-06.
- [OCPI 2.2.1 commands](https://raw.githubusercontent.com/ocpi/ocpi/2.2.1/mod_commands.asciidoc): Specification, OCPI 2.2.1, checked 2026-10-06.
- [OCPI 2.2.1 tariffs](https://raw.githubusercontent.com/ocpi/ocpi/2.2.1/mod_tariffs.asciidoc): Specification, OCPI 2.2.1, checked 2026-10-06.
