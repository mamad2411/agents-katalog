# Anchored Filesystem I/O

This boundary owns shared root-scoped UTF-8 and bounded exact-byte file access, snapshot checks, and
physical mutation rollback. Callers own authorization, allowed directories,
filename selection, content formats, and domain transitions.

- Keep filesystem safety independent of task queues and editor tools. Markdown
  selection belongs to callers, not the filesystem helper.
- Directory traversal and leaf operations stay in the isolated helper process.
  Preserve no-follow opens, directory identity checks, and working-directory
  anchoring together; pathname validation alone is not a replacement.
- An anchored directory can be renamed during an operation. Leaf operations
  remain attached to that directory, not a replacement at its former pathname.
  This is not an atomic beneath-root guarantee against relocation of that inode.
- Files must be regular and single-link. Reads carry verified metadata snapshots;
  conditional writes and removals compare those snapshots before mutation.
  These are optimistic checks, not atomic compare-and-swap against other writers.
  Text decoding rejects malformed UTF-8 bytes and preserves valid Unicode and BOMs.
  Existing entries require their exact stored spelling, including on filesystems
  that otherwise alias case or Unicode normalization variants.
- Bounded line reads stream one opening snapshot and limit selected output, not
  total file size. Exact selections fail visibly when they exceed the byte budget;
  recent context omits oversized lines. Callers own record attribution and expiry.
- Cross-directory moves install then remove, with snapshot-checked compensation.
  They are not atomic transactions; failed cleanup may retain a temporary or
  quarantined entry rather than remove an entry whose identity is uncertain.
- Retain the source-embedded subprocess while Node lacks the required relative
  directory-descriptor operations. Unsupported no-follow platforms fail closed.
- Daemon record and configuration stores retain their own stricter ownership,
  permissions, and lifecycle contracts; do not merge them by weakening those rules.
- Safety tests belong here for shared mechanics and beside domain callers for
  distinct semantic entry points. Do not duplicate the helper in callers.

## Private publication

`publishPrivateFile` is the stricter credential-writing boundary. It does not
reuse relocatable anchored mutations. The Linux helper walks from `/` without
following symlinks and requires administrator-owned, non-writable ancestors above
the destination directory. This prevents unprivileged writers from moving that
directory or its root; privileged host administrators remain trusted.

All byte writes and permission changes occur on an anonymous `O_TMPFILE` inode.
Only completed bytes gain a name; publication replaces an entry relative to the
protected directory without following leaf links. No named staging directory or
subsequent credential write can follow a relocated inode. Changed-target snapshot
checks catch intervening edits but are not atomic compare-and-swap: a final racing
leaf replacement is replaced as an entry, never dereferenced. Callers requiring
conditional updates must not treat this API as a transaction or optimistic lock.
Unsupported platforms, identities, layouts or filesystem primitives fail closed.
The helper receives content over stdin and returns only redacted status.
