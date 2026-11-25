---
name: "solidworks-macro-fallback"
description: "Use when a SolidWorks API call through the MCP bridge needs a COM object argument (limit mates, gear mates, ModifyDefinition), and only after the user has agreed to macros being used. Ref and out values come back beside the invoke result."
---

# Macro fallback for calls the bridge cannot make

The list of calls the bridge cannot make is in `solidworks-bridge-tool-selection`. This skill is the workaround: a text macro run through the legacy RunMacro.

## Ask first
Macros run code inside the user's SolidWorks, are hard to verify through the bridge, and have failed with type-mismatch errors in real runs. Before writing one:
- Tell the user which call needs a macro and what the alternative is (design around it, or leave it as an open item).
- Use a macro only if the user agrees. If the user has said not to use macros, don't; record the item as open. A user constraint applies to every remaining step, not just the current one.

## Workaround: text macro + legacy RunMacro
1. Write a SolidWorks Basic macro as plain text with extension `.swb` into the project (e.g. `05_CAD/Macros/NAME.swb`, using device_bash) so the user can re-run it. Use **CRLF line endings** for the macro and any data file it reads; LF files were read as one line and silently did nothing.
2. Template:
```
Dim swApp As Object
Dim Part As Object
Sub main()
    Set swApp = Application.SldWorks
    Set Part = swApp.ActiveDoc
    Dim ok As Boolean
    Dim errStat As Long
    Dim m As Object
    Part.ClearSelection2 True
    ok = Part.Extension.SelectByID2("Front Plane@Comp-1@AsmName", "PLANE", 0, 0, 0, False, 1, Nothing, 0)
    ok = Part.Extension.SelectByID2("Right Plane", "PLANE", 0, 0, 0, True, 1, Nothing, 0)
    Set m = Part.AddMate5(5, 0, False, nominal, maxAbs, minAbs, 1, 1, 0, 0, 0, False, False, 0, errStat)
    Part.ClearSelection2 True
    Part.EditRebuild3
End Sub
```
   AddMate5 with type 5 (distance) and different upper/lower limits creates a LimitDistance mate. Values in metres. Do one mate (or one small, closely related group) per macro, so a failure has one cause.
3. Make sure the target document is active (app ActivateDoc(title)), then run: app invoke RunMacro("full\\path\\NAME.swb", "", "main"). It returns true when the macro ran.
4. **Verify, never assume.** A RunMacro call that reported an error or "RPC server unavailable" may still have run: re-read the mate list before running it again, or you create duplicates. Then read the result: doc FeatureByName("LimitDistance1") → GetSpecificFeature2 → get_property MinimumVariation / MaximumVariation (offsets from nominal, metres), and check the mate's error code.

## Use the macro route for (with the user's agreement)
- Limit and gear mates that still need a COM object argument. AddMate5's ref error status comes back in `WrittenBack`; that call was not re-checked on a live session.
- COM object arguments the bridge still cannot pass. Not for ref or out values: `invoke` returns those beside the result, including `GetEquationParameters2`.

Not for routine work the bridge can already do: a macro saves round trips but hides failures, and its values are not linked to the design state.

Equations that need deleting cannot be fixed by macro either in practice; rebuild the document instead (see the bridge skill).

## Note in the deliverable
Values hard-coded in a macro are not linked to the design state or the global-variables file. Tell the user which macro to edit and re-run when a driving parameter changes.