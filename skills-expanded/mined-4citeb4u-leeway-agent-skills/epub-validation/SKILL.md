---
name: leeway-epub-validation
description: EPUB conformance validation capability using EPUBCheck or equivalent standards-aware validation plus reading-system and accessibility testing.
license: MIT
---
# LeeWay EPUB Validation
Run the official EPUBCheck when available and preserve its version/report. Conformance validation is necessary but not sufficient: test representative reading systems and accessibility behavior where required. ERROR/WARNING handling follows project policy; do not call a book validated if the checker was never executed.