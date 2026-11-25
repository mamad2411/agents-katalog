---
name: two-factor-custom-provider
description: Creating a custom authentication provider for the Two Factor plugin.
---

# Two Factor Custom Provider
To create a custom Two Factor provider:
1. Create a PHP class implementing the provider logic.
2. Hook into `two_factor_providers` filter.
3. Return your class name in the array of providers.
