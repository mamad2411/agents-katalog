# Owner-Decisions Module

Surfaces persisted owner decisions through the `kota owner-decision` CLI,
public HTTP routes, daemon-control routes, and the `KotaClient.ownerDecisions`
namespace.

The file-backed decision store lives in `src/core/daemon/` because workflows,
daemon runtime scope bundles, and provider action adapters share it. This
module owns only operator projection and mutation surfaces. New answer or
cancel surfaces should resolve the linked owner question through the same
operation helpers so waiting workflows resume through the existing
`owner.question.resolved` await-event path.

Route registrations resolve the daemon scope provider through their
`ModuleContext`; the runtime loader's provider registry is the authority for
multi-scope reads and mutations.
