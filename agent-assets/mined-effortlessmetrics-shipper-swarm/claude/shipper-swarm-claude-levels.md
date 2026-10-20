# Module: `crate::plan::levels`

**Layer:** plan (layer 4)
**Single responsibility:** Group publishable crates into parallel-eligible "waves" — crates within a wave have no dependencies on each other and can publish concurrently.
**Was:** standalone crate `shipper-levels` (absorbed into the layered plan module layout during the decrating effort)

## Public-to-crate API

- `pub(crate) fn group_packages_by_levels<T, F>(ordered_packages, package_name, dependencies) -> Vec<PublishLevel<T>>`
- `pub(crate) struct PublishLevel<T> { level: usize, packages: Vec<T> }`
