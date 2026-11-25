---
name: fails
description: A fixture for scripts/test-check-contract-sections.sh, not a skill. Every line below the heading must fail, and the test expects exactly these.
---

# Lines that must FAIL

- A section the contract does not have: `get_app_contract` with `sections: ["9"]`.
- One bad id among good ones: `sections: ["2", "2.9", "4.1"]`.
- Two literals on one line, the second bad: `sections: ["2"]`, then `sections: ["0"]`.
- An id that is not a quoted string: `sections: [2]`.
- The JSON key form: `{ "app": "demo", "sections": ["1.9"] }`.
- A literal that does not close on its line: `sections: ["2",
  "3"]`.
- A literal glued to the one before it, the second bad: `sections: ["2"]sections: ["9"]`.
- An id that is not numbers joined by dots, though each part is a section: `sections: ["1.3 2"]`.
