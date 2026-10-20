---
description: Enforces guidelines for creating custom libraries and utility modules in the lib directory.
globs:
  - "lib/**/*.rb"
---

# Lib

<rule>
name: lib_standard
description: Ensures that custom libraries and utility modules in the lib directory are well-organized, documented, and adhere to Rails conventions.

filters:
  - type: path
    pattern: "^lib/.*\\.rb$"
    # Applies to all Ruby files in the lib directory

actions:
  - type: suggest
    message: |
      Library files should:
      1. Be organized into appropriate subdirectories.
      2. Include clear documentation and inline comments.
      3. Follow Ruby naming conventions and modular structure.
      4. Avoid duplicating functionality already provided by Rails or gems.
      5. Be tested to ensure reliability.

examples:
  - input: |
      # Bad example: Unstructured file with mixed responsibilities.
      module Utilities
        def self.perform
          # code
        end
      end
    output: "Custom libraries should be modular, well-documented, and organized into specific namespaces."
  - input: |
      # Good example.
      module DataProcessing
        module Formatter
          def self.format(data)
            # formatting logic
          end
        end
      end
    output: "Library is well-structured, follows naming conventions, and is properly namespaced."

metadata:
  priority: medium
  version: 1.0
  related_rules:
    - rails_project_standard
  responsibility: "Standardize the creation and organization of custom libraries and utilities"
</rule>
