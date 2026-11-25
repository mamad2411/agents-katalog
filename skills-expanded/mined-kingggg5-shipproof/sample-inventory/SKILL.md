---
name: sample-inventory-skill
description: Fixture Skill used only to test the opt-in capability inventory.
---

# Sample inventory skill

Declared tools may read files. This fixture does not grant production access.

```python
from pathlib import Path
text = Path("notes.txt").read_text()
```
