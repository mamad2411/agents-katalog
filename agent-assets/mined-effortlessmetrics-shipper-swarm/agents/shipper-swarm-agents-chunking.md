# AGENTS.md

Use this file with [CLAUDE.md](./CLAUDE.md) before making changes in this directory.

# Module: `crate::plan::chunking`

**Layer:** plan (layer 4)
**Single responsibility:** Split a large publish plan into smaller chunks for resumable mid-flight execution.
**Was:** standalone crate `shipper-chunking` (absorbed into the layered plan module layout during the decrating effort)

## Public-to-crate API

- `pub(crate) fn chunk_by_max_concurrent<T: Clone>(items: &[T], max_concurrent: usize) -> Vec<Vec<T>>`

