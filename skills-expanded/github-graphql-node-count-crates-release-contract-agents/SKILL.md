# The release contract

Reconciles `release-targets.toml` against what the release configuration actually
publishes, in both directions, so a name this repository starts or stops
publishing fails here rather than going undeclared.

It also holds the project graph to `SCOPE_POLICY` — the module-boundary rule in
the form a Cargo workspace can enforce, since Nx's own is an ESLint rule and there
is no JavaScript here. A new project declares its scope in that table, and what
that scope may depend on, or the suite fails.

It depends on **nothing** in this workspace, deliberately: a change to the library
must not reach this suite, and this suite must not reach back into what depends on
it. Its own tests are what keep that true.
