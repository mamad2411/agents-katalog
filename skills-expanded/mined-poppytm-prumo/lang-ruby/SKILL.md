---
name: lang-ruby
description: Modern Ruby 3.3+, gradual typing with RBS/Sorbet, RuboCop strict, and defensive metaprogramming limits.
---

# Ruby Gradual Typing Contract

## 1. Typing & Code Quality
- Enforce `# frozen_string_literal: true` on all Ruby source files.
- Provide RBS typespecs or Sorbet signatures (`typed: strict`) on core service boundaries.
- Limit dynamic metaprogramming (`method_missing`, `define_method`) to well-isolated library modules.
