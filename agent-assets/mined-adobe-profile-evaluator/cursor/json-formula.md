---
description: writing json-formula based expressions
alwaysApply: false
---
rule: |
  # Rule: Use json-formula for profile expressions

  When writing expressions in a profile, use the [json-formula](https://opensource.adobe.com/json-formula/doc/output/json-formula-specification-1.1.2.html) syntax. This allows for powerful, concise, and standards-based evaluation of JSON data.

  ## Requirements

  - Expressions must be valid according to the json-formula specification (v1.1.2).
  - Use json-formula operators for property access, logical operations, comparisons, and functions.
  - Prefer concise expressions that directly evaluate the required condition or value.
  - Use `@` to refer to the root object, and dot notation for property access (e.g., `@.metadata.name`).
  - Use logical operators (`&&`, `||`, `!`) and comparison operators (`==`, `!=`, `<`, `>`, `<=`, `>=`) as needed.
  - Use built-in functions (e.g., `hasProperty`, `toDate`, `now`) where appropriate.
  - Expressions should not use non-standard extensions or syntax outside the json-formula specification.

  ## Examples

  - Check if a property exists:
    ```
    hasProperty(@, "manifest")
    ```
  - Compare a date property to the current time:
    ```
    toDate(manifests[0].claim_signature.validity.not_before) < now()
    ```
  - Logical combination:
    ```
    @.profile.not_before && @.profile.not_after && !@.profile.test_cert && @.profile.issuer
    ```
  - Access a nested property:
    ```
    manifests[0].claim_signature.issuer.CN == "Alice's Trust Services"
    ```

  For more details, see the [json-formula specification](https://opensource.adobe.com/json-formula/doc/output/json-formula-specification-1.1.2.html).
