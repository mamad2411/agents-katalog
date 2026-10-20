# Module Factory

This directory owns the authoring tool schema, saved-manifest actions and module-log
queries. Shared manifest infrastructure owns validation and persistence; the normal
module loader owns runtime activation.

Creation authorizes the module directory because atomic manifest persistence
also creates temporary siblings. Removal preserves the shared module directory.
The persistence owner's path resolver supplies both authorization and execution.
Observation resolves to a read effect; removal retains destructive approval.
The static write effect keeps discovery annotations and the guardrail risk floor
conservative for this mixed-action tool.
