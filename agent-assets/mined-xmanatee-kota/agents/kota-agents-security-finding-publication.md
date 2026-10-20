# Security Finding Publication

Materializes confirmed security families from the security-review runtime outbox.
The review owns evidence and coverage; this writer owns only task publication.
Use the shared task resource and revisioned state transaction so active or retained
builders keep their admitted contracts. Unavailable ownership parks publication;
pending findings remain in runtime state for dispatcher reconciliation.

Resolve outbox entries independently. Unresolvable task identities stay pending
with their provenance and reason while valid evidence publishes independently,
including for the same task when older evidence still requires lineage.
Recheck each entry against the task after preceding writes; newly unresolved
evidence parks without aborting independently publishable entries in the batch.
The publication invariant still rejects a target with no resolvable evidence.
