---
name: remove-duplication
description: Finds duplicated logic in one area and merges it only where the copies truly belong together, with tests proving behavior held.
disable-model-invocation: true
---

Find and remove duplication in: $ARGUMENTS

1. Search the area for repeated logic: similar function bodies, repeated conditionals, parallel switch statements, copied SQL or regexes. Use `jscpd` or a similar detector if installed, then verify by reading.
2. For each cluster, diff the copies and list what differs. Ask of each pair: if one needs to change tomorrow, must the other change too? If yes, they truly belong together. If not, it is coincidental.
3. Make sure tests cover each copy before merging. Add missing characterization tests first and run them green.
4. Merge only real duplicates: extract one function, pass the differences as parameters, name it for what it does. Keep it in the nearest shared module, not a new utils dump.
5. Never merge across package boundaries or change public signatures without asking.

Report clusters as merged, left alone (with the reason), or needs decision. Run all tests and show the net lines removed.
