---
name: oitc-config-change
description: Safely change an existing host, service, contact or contact group in openITCOCKPIT. Use before any update_* call - the edit endpoints are read-modify-write, so a naive partial payload silently blanks fields. Requires write tools to be enabled.
---

# Changing an existing object

Requires `OITC_ENABLE_WRITE_TOOLS=true`.

openITCOCKPIT's edit endpoints expect the **complete** object on every save. The
`update_*` tools handle that for you - they fetch the current effective values,
apply your `fields` on top, and resend everything. What you still have to get
right is what `fields` means.

## The three states of a field

| In `fields` | Effect |
|---|---|
| Absent | Keeps its current effective value. Safe. |
| Set to a value | Becomes this object's explicit override. |
| Set to `null` | **Resets to inherited** from the template. |

`null` is not "empty" - it means "go back to what the template says". Use it
deliberately. On `update_contact` / `update_contactgroup` there is no template
to inherit from, so `null` is rejected outright on required fields.

## Traps

**Contacts and contact groups are coupled.** `contact_names` and
`contactgroup_names` can only be reset together - a naemon-core limitation, not
an MCP choice. Pass both as `null`, or set both explicitly. Nulling one while
giving the other a real value is rejected.

**Array fields replace, never append.** `hostgroup_names`, `servicegroup_names`,
`contact_names`, `container_names` overwrite the whole set. To add one entry you
must send the existing entries plus the new one - so read the current value
first.

**Moving a host re-validates everything.** `update_host(..., container_name=...)`
re-checks every reference the host already has against the *new* container's
scope, including ones you did not touch. If the host's current template is not
visible there, the call is rejected and you must set a valid one in the same
call. This is deliberate: openITCOCKPIT itself would leave a dangling reference.

**Renaming a service.** `update_service` rejects a name already used by another
service on the same host.

## Procedure

1. **Read the current state.**
   ```
   get_host_health(hostname)            # the host and its services
   get_service_config(hostname, servicename)   # what a service sets itself
   list_catalog(kind="contact", name="...")    # contacts, groups, templates
   ```
   Array fields replace rather than append, so the current value *is* the input
   for your change. If a listing comes back with `truncated: true` you do not
   have the full set - narrow it with `name` before building the new list, or
   you will silently drop the entries you never saw.

2. **Check scope, if a reference is involved.**
   ```
   get_allowed_elements_for_container(object_type="host", container_name="<target>")
   ```
   Needed whenever you set a template, timeperiod, contact, contact group or
   group name - and always when passing `container_name` to `update_host`.

3. **Tell the operator what will change.** Name the object, the fields, the
   current value and the new value. Wait for agreement.

4. **Send the minimal `fields`.**
   ```
   update_service(hostname="web01", servicename="HTTP",
                  fields={"check_interval": 60})
   ```
   Only what actually changes. Everything else is carried forward for you -
   listing unchanged fields adds risk without adding anything.

5. **Verify.**
   ```
   get_host_health("web01")
   ```

## When a write is rejected

The error names the field, every invalid value in one go, and either the closest
matching names in scope or the count of valid ones. Read it and correct all of
them at once - do not retry a single field at a time, and do not guess a name
that was just rejected.

Full semantics:
<https://github.com/openITCOCKPIT/openITCOCKPIT-MCP-Server/blob/main/docs/using-the-tools.md>
(an absolute link, because this folder is meant to be copied out of the repo).
