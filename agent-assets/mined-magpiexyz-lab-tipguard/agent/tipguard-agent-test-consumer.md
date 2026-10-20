# Test Consumer

This consumer references `golden_path` directly without using the canonical
function. The field_role_map rule should flag this.

```
for step in experiment["golden_path"]:
    print(step)
```
