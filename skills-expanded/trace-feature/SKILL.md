---
name: trace-feature
description: Follow one feature through a program, from the button or command that starts it to the code that does the work.
---

# Trace a feature

The user names a feature ("export to PDF", "the login screen", "the save button"). Find its path through the code.

1. Find the feature's text in `list_strings`: its button label, menu title, error or success message, or a format string it prints.
2. Follow `xrefs` from that string to the code, and `resolve_containing_procedure` to name the function. That is your way in.
3. Walk forward with `procedure_callees`, reading each function's pseudocode, until you reach the code that does the real work rather than setting up UI.
4. Walk backward with `procedure_callers` when you need to know what triggers it.

As you go, `rename_function` each step and `add_note` its role, and `open_function` the function you are explaining so the user follows along.

Report the path as a short chain: trigger → … → the work, naming each function and what it does. End with where the feature actually happens and anything worth a closer look.
