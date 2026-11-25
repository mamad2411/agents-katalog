# AGENTS.md

## Best Practices

- **frozen_string_literal** — Every `.rb` file must start with `# frozen_string_literal: true`.
- **Require what you use** — Explicitly `require` standard library modules (e.g., `require 'set'`, `require 'tsort'`). Do not rely on transitive requires.
- **No side effects in domain classes** — Classes like `S3Bucket`, `Route53HostedZone`, and `Stack` must not call `puts`, `warn`, or `abort`. Return values or raise exceptions; let the caller handle output.
- **Keyword arguments for dependencies** — Use keyword args with defaults for injecting clients: `def initialize(name, client: Aws::S3::Client.new)`. The domain value comes first.
- **`class << self` for class methods** — Prefer `class << self` blocks over `def self.method_name`.
- **One class per file** — Each class or module gets its own file under `lib/cdk_plus/`.
- **Commands are classes** — CLI commands live in `lib/cdk_plus/commands/` and expose a `#run` method.
- **Top-level entry point** — `lib/cdk_plus.rb` requires all library components. CLI-specific code lives in `lib/cdk_plus/cli.rb`.
- **Gemspec metadata** — Always include `spec.license`, `spec.homepage`, and `spec.summary`.
- **Pin dependencies** — Use pessimistic version constraints (`~>`) in the gemspec.
- **Separation of concerns** — Keep orchestration (commands) separate from domain logic (models) and generic utilities (e.g., `DependencyTree`).
