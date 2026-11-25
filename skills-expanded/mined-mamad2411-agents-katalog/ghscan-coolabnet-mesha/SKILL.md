# SKILL: server-services

## Purpose

The `server-services` skill installs and manages approved local services on community servers. It uses reviewed installation recipes, verifies prerequisites, configures local domain access through the reverse proxy, writes simple user onboarding notes, and supports backup and restore hooks. All actions require an approved plan before execution.

Only services listed in the approved service catalog may be installed through this skill.

---

## Responsibilities

### Must do

- Accept a service request and check whether the requested service is in the approved catalog at `desired-state/server/service-catalog.yaml`.
- Refuse to install any service not present in the approved catalog.
- Produce a written installation plan before executing: which recipe will be used, what prerequisites are needed, what local domain will be assigned, what ports will be used, what storage will be required, and what the rollback path is.
- Present the plan to the requesting maintainer and wait for explicit approval before executing.
- Verify prerequisites before starting installation: available disk space, required software dependencies, network access, and resource availability.
- Execute the installation using only the approved recipe for that service (from `skills/server-services/scripts/` or equivalent).
- Configure local domain access per `desired-state/server/domains.yaml` and the reverse proxy configuration.
- Validate service health after installation: reachability, health-check endpoint, correct domain resolution.
- Validate offline behavior: confirm the service is reachable without internet access.
- Write simple user onboarding notes: how to access the service, what it is for, basic usage instructions in plain language.
- Register the installed service in `inventories/local-services.yaml` with status, URL, and maintainer contact.
- Connect backup hooks per `desired-state/server/backup-policy.yaml` when the service has data that should be backed up.
- Validate that backup hooks are working after installation.
- Execute service updates using the same recipe-based approach: plan, approve, execute, validate.
- Support controlled service removal: plan, approve, remove, clean up local domain and proxy config, update inventory.
- Restore from backup when instructed and approved: plan, approve, validate pre-restore state, execute, verify.
- Write a maintenance log entry for every install, update, removal, or restore action.

### Must not do

- Install any service that is not in the approved catalog at `desired-state/server/service-catalog.yaml`.
- Execute any installation, update, or removal without a confirmed written plan and explicit maintainer approval.
- Invent installation procedures — use only reviewed recipes.
- Expose services directly on public interfaces without explicit configuration in the approved reverse proxy setup.
- Store credentials or secrets in any log, doc, or inventory file.
- Proceed if prerequisites are not met — halt and report what is missing.
- Skip post-install validation.
- Skip backup hook setup for services with persistent data.
- Perform mass service changes (multiple services in one operation) without a plan that covers each service individually.

---

## Inputs

- Service request: which service to install, update, remove, or restore; from which host.
- Approved service catalog: `desired-state/server/service-catalog.yaml`
- Server desired state: `desired-state/server/hosts.yaml`, `desired-state/server/domains.yaml`, `desired-state/server/reverse-proxy.yaml`, `desired-state/server/backup-policy.yaml`
- Installation recipes in `skills/server-services/scripts/`
- Server inventory: `inventories/local-services.yaml`
- Pre-action snapshot from `server-readonly` (required before any change execution)
- Approval record from an authorized maintainer via the trusted channel
- Optional: restore source (backup location, snapshot reference) for restore operations

---

## Outputs

- **Installation plan** (before execution): written plan with recipe, prerequisites, domain assignment, storage requirement, rollback path, and success criteria.
- **Post-install validation report**: service health, domain resolution result, offline behavior confirmation.
- **User onboarding notes**: plain-language document explaining how to access and use the service.
- **Updated local service inventory entry**: `inventories/local-services.yaml` updated with service status, URL, and maintainer.
- **Maintenance log entry**: appended to `logs/` — timestamp, service name, action taken, approval reference, outcome. Handed to `knowledge-curator`.
- **Backup hook confirmation** (when applicable): confirmation that backup is configured and tested.
- **Rollback report** (when applicable): what was removed or reverted and current state.

---

## Risk Class

**Class C — Medium-risk infrastructure change**

Installing, updating, or removing a service changes the server's running state. Requires a written plan and explicit maintainer approval before execution. Rollback required: each recipe must define a removal or rollback procedure.

Restore operations involving live data replacement are **Class D** and require an explicit additional confirmation acknowledging that existing data may be overwritten.

---

## Activation Examples

- "Install the local media archive on the server." (requires plan + approval)
- "Set up the community wiki." (requires plan + approval)
- "Update the Nextcloud instance to the latest approved version." (requires plan + approval)
- "Add a local domain for the media server." (requires plan + approval)
- "Remove the test service from the server." (requires plan + approval)
- "Restore the wiki from last week's backup." (requires plan + explicit approval for data overwrite)
- "Check that backup is running for the media archive." (read-only check — routes to server-readonly)
- "Add the new service to the service catalog." (documentation only — routes to knowledge-curator)
- "What services are approved for installation?" (read-only — routes to server-readonly or knowledge-curator)

---

## Constraints and Guardrails

1. **Catalog enforcement**: if a requested service is not in `desired-state/server/service-catalog.yaml`, the skill must refuse the request and explain that the service needs to be added to the approved catalog first. It must not attempt to install it anyway.
2. **No approval, no execution**: explicit written approval from an authorized maintainer is required for every install, update, removal, or restore. This is non-negotiable.
3. **Recipe discipline**: only use approved, reviewed recipes from `skills/server-services/scripts/`. Do not improvise installation steps with arbitrary shell commands.
4. **Prerequisites must be verified before proceeding**: if prerequisites are not met, stop and report what is needed. Do not proceed with an incomplete environment.
5. **No public exposure without explicit proxy config**: a newly installed service must not be reachable outside the local network unless the reverse proxy and domain config are explicitly set up and confirmed.
6. **No secrets in output**: installation logs, onboarding notes, and inventory entries must never contain passwords, API tokens, or private keys. Reference `secrets/README.md` for how to handle credentials.
7. **Post-install validation is mandatory**: the skill must not report success until reachability, domain resolution, and offline behavior have been confirmed.
8. **Backup hooks for persistent data**: any service that stores user data must have backup hooks configured before the install is considered complete. Services with no backup path for persistent data must be flagged to the maintainer.
9. **Restore is Class D**: any restore operation that overwrites live data requires an explicit additional confirmation from the maintainer acknowledging the data impact. Treat it as a separate approval step.
10. **Log every action**: every install, update, removal, and restore must be logged. An undocumented change to the server is a failure condition.
11. **Rollback path required**: every install plan must define a removal/rollback procedure before execution is approved. If a clean rollback path cannot be defined for a service, this must be disclosed in the plan.
