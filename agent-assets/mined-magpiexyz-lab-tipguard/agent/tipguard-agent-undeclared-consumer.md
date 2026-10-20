# Undeclared Consumer

This file is NOT in the consumers list but matches the consumption pattern
`test_field[`. discover_consumers should emit a WARN finding asking the
template author to either add this file to consumers or audit the access.

```python
first = test_field[0]
```
