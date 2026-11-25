# Commands and evidence

Resolve actual paths and SDK from the checkout; do not infer from bin/obj. The supplied archive has `RoadGuardSystem.slnx`, SDK 10.0.401, net8.0 targets. Use the project's installed runner and package versions.

Example in CMD/PowerShell from repository root, replacing Feature with an observed test class/method:

```cmd
dotnet build RoadGuardSystem.API/RoadGuardSystem.eAPI.csproj -nologo -v q -clp:ErrorsOnly
dotnet build tests/RoadGuardSystem.ApiTests/RoadGuardSystem.ApiTests.csproj -nologo -v q -clp:ErrorsOnly
dotnet test tests/RoadGuardSystem.ApiTests/RoadGuardSystem.ApiTests.csproj --no-build --nologo -v q --filter "FullyQualifiedName~Feature"
```

The first build satisfies the current repository production gate; the second compiles tests and refreshes their copied dependencies. Do not remove the second merely because the first passed. Reuse either only while its inputs/output remain valid. If the owner updates the repo gate, building the selected test project and references once can avoid duplicate production traversal.

Use exact sibling csproj paths for UnitTests and IntegrationTests. Add the same `-c Release` or `-f net8.0` to build and test if required by the scope; never build Debug and then test stale Release. Do not assume `--no-restore` until assets are valid.

For affected-project breadth, omit the filter on selected test projects. For an authorized full-solution gate:

```cmd
dotnet build RoadGuardSystem.slnx -nologo -v q -clp:ErrorsOnly
dotnet test RoadGuardSystem.slnx --no-build --nologo -v q
```

Select actual test names with scoped rg before execution. If discovery is ambiguous, `dotnet test <csproj> --no-build --list-tests` is a read-only diagnostic after a valid build. Check that the filter really executed the intended tests.

Read only the setup relevant to the fixture: local SQL vs existing Testcontainers. Do not disable security, skip SQL or alter host configuration to hide a missing dependency. Build unavailable because the pinned SDK is missing is a blocked check, not permission to edit global.json.

Minimal evidence record follows `planning/V2/TASK_LIFECYCLE.md`: task/source checkpoint; changed source/config and dependency scope; command/config/filter; executed/pass/fail/required-skip counts; SQL/runtime environment; smoke/effect result; valid reused/invalidated evidence and unverified risk. A new commit alone does not invalidate a passing test; changed relevant inputs do.
