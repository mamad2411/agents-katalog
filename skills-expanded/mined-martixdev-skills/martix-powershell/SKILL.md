---
name: martix-powershell
description: Standalone-first PowerShell cmdlet guidance for compiled C# cmdlets and advanced functions that declare [CmdletBinding()] and follow the cmdlet contract. Use when authoring or reviewing cmdlets, choosing approved verbs or parameter sets, wiring pipeline processing or ErrorRecord/ShouldProcess/Force/WhatIf behavior, packaging binary modules or .psd1 manifests, or selecting validators like ValidateSet and ValidateRange. Do not use for generic scripts without [CmdletBinding()], DSC resources, or runbook automation.
license: Complete terms in LICENSE.txt
---

# MartiX PowerShell cmdlet router

- Standalone-first skill package focused on compiled PowerShell cmdlet
  development decisions for C# authors targeting PowerShell 7+.
- Keep decisions grounded in the bundled rule files and reference maps.
- Use [AGENTS.md](./AGENTS.md) when the task crosses multiple workstreams or
  needs the long-form review routes, package inventory, or maintainer guidance.

## When to use this skill

- Author or review a compiled PowerShell cmdlet class, cmdlet noun/verb pair,
  or binary module manifest.
- Author or review a PowerShell advanced function that declares
  `[CmdletBinding()]` and follows the cmdlet contract.
- Fix parameter binding, pipeline streaming, `ErrorRecord`, `ShouldProcess`, or
  `Force` behavior.
- Choose validation attributes, help-block structure, output declarations, or
  script-style boundaries for cmdlet-style PowerShell code.

## Not for this skill

- Generic PowerShell scripts or functions **without** `[CmdletBinding()]`.
- Pipeline-only scripts that do not follow the cmdlet contract.
- Automation scripts, runbooks, or DSC resources.
- For broader C# or .NET guidance beyond the PowerShell SDK — general class
  design, LINQ, async/await, ASP.NET, or Entity Framework — use
  `martix-dotnet-csharp`.

## Quick-start routes

Use the closest row first, then open the linked workstream map or companion
guide only when the task widens.

| Task | Start with | Add when |
| --- | --- | --- |
| New cmdlet or module shape | [Foundation — base class and attribute](./rules/foundation-base-class-attribute.md) + [Naming — approved verbs and cmdlet name contract](./rules/naming-approved-verbs-cmdlet-contract.md) | [Foundation — project and module shape](./rules/foundation-project-module-shape.md) for `.psd1` manifests, DLL layout, or `Import-Module` wiring. |
| Parameter or pipeline bug | [Parameters — pipeline binding](./rules/parameters-pipeline-binding.md) + [Pipeline — input processing methods](./rules/pipeline-input-processing-methods.md) | [Parameters — sets and dynamic parameters](./rules/parameters-sets-dynamic.md) when multiple parameter sets or runtime parameters are involved. |
| Error or destructive-operation review | [Error handling — terminating and non-terminating](./rules/error-handling-terminating-nonterminating.md) + [Confirmation — ShouldProcess and ShouldContinue](./rules/confirmation-shouldprocess-shouldcontinue.md) | [Confirmation — Force parameter and non-interactive safety](./rules/confirmation-force-parameter.md) when `Force`, automation safety, or second-level confirmation is in scope. |
| Advanced function authoring | [Parameters — declaration and validation](./rules/parameters-declaration-validation.md) + [Documentation, help, and style](./rules/documentation-help-style.md) | [Pipeline — output and streaming](./rules/pipeline-output-streaming.md) when emitted object type, streaming, or `OutputType` alignment matters. |
| Dynamic parameters or transactions | [Advanced patterns — dynamic parameters and aliases](./rules/advanced-dynamic-parameters-alias.md) | [Advanced patterns — transactions and jobs](./rules/advanced-transactions-jobs.md) only when transaction or job integration is explicitly required. |

## Rule library by workstream

Open the section for your target domain and read only the rule files it lists.

## Foundation and base class selection

- Use for base class choice (`Cmdlet` vs `PSCmdlet`), `[Cmdlet]` attribute
  declaration (verb, noun, `SupportsShouldProcess`, `SupportsTransactions`),
  `OutputType`, assembly structure, project file shape, `.psd1` module
  manifest, and `Import-Module` wiring.
- Rules:
  - [PowerShell cmdlet foundation — base class and attribute](./rules/foundation-base-class-attribute.md)
  - [PowerShell cmdlet foundation — project and module shape](./rules/foundation-project-module-shape.md)
- Map: [Foundation map](./references/foundation-map.md)

## Naming and conventions

- Use for approved verb selection from `Verbs*` typed constants, verb group
  semantics, paired inverse verb patterns (`Add`/`Remove`, `Start`/`Stop`),
  vendor noun prefix conventions, the standard parameter name table (`Path`,
  `Name`, `Force`, `Credential`, `PassThru`, `InputObject`), common parameter
  injection rules, and the `[Credential]` attribute pattern.
- Rules:
  - [PowerShell naming — approved verbs and cmdlet name contract](./rules/naming-approved-verbs-cmdlet-contract.md)
  - [PowerShell naming — parameter and common names](./rules/naming-parameter-and-common-names.md)
- Map: [Naming and conventions map](./references/naming-map.md)

## Parameters, validation, and sets

- Use for `[Parameter]` attribute options (`Mandatory`, `Position`,
  `ParameterSetName`, `HelpMessage`), validation attribute stacking,
  standard parameter names, parameter set design, the default parameter set,
  uniqueness requirement per set, and `IDynamicParameters` for runtime-declared
  parameters.
- Rules:
  - [PowerShell parameters — declaration and validation](./rules/parameters-declaration-validation.md)
  - [PowerShell parameters — sets and dynamic parameters](./rules/parameters-sets-dynamic.md)
  - [PowerShell parameters — pipeline binding](./rules/parameters-pipeline-binding.md)
- Map: [Parameters and validation map](./references/parameters-validation-map.md)

## Input processing and output streaming

- Use for `BeginProcessing`, `ProcessRecord`, `EndProcessing`, and
  `StopProcessing` override patterns, correct sequencing of object streaming,
  `WriteObject` semantics, null handling, avoiding text output in pipeline
  cmdlets, and `OutputType` declarations.
- Rules:
  - [PowerShell pipeline — input processing methods](./rules/pipeline-input-processing-methods.md)
  - [PowerShell pipeline — output and streaming](./rules/pipeline-output-streaming.md)
- Map: [Pipeline map](./references/pipeline-map.md)

## Error handling

- Use for the terminating vs. non-terminating decision, `ErrorRecord`
  construction (exception, identifier, `ErrorCategory`, target object),
  `WriteError` vs. `ThrowTerminatingError`, error action preferences, and
  standard error categories.
- Rules:
  - [PowerShell error handling — terminating and non-terminating](./rules/error-handling-terminating-nonterminating.md)
  - [PowerShell error handling — ErrorRecord construction](./rules/error-handling-errorrecord-construction.md)
- Map: [Error handling and categories map](./references/error-handling-categories-map.md)

## Confirmation, safety, and transactions

- Use for `SupportsShouldProcess = true`, `ShouldProcess` call patterns,
  `ShouldContinue` for high-impact operations, `ConfirmImpact` level selection,
  `WhatIf` / `Confirm` automatic parameters, the `Force` parameter bypass
  semantics, and `SupportsTransactions` for transactional cmdlets.
- Rules:
  - [PowerShell confirmation — ShouldProcess and ShouldContinue](./rules/confirmation-shouldprocess-shouldcontinue.md)
  - [PowerShell confirmation — Force parameter and non-interactive safety](./rules/confirmation-force-parameter.md)
- Map: [Confirmation and safety map](./references/confirmation-safety-map.md)

## Advanced patterns and extensibility

- Use for `IDynamicParameters`, parameter aliases, `ScriptBlock` invocation
  from cmdlet context, `SessionState` access via `PSCmdlet`, credential
  parameters, and transaction support (`SupportsTransactions`,
  `CurrentPSTransaction`).
- Rules:
  - [PowerShell advanced patterns — dynamic parameters and aliases](./rules/advanced-dynamic-parameters-alias.md)
  - [PowerShell advanced patterns — transactions and jobs](./rules/advanced-transactions-jobs.md)
- Map: [Advanced patterns map](./references/advanced-patterns-map.md)

## Attributes and validators

- Use for `ValidateSet`, `ValidateRange`, `ValidatePattern`, `ValidateScript`,
  `ValidateLength`, `ValidateCount`, `ValidateNotNull`, `ValidateNotNullOrEmpty`,
  custom validation attributes, and `OutputType` declarations. For approved
  verb selection and naming conventions, see the Naming workstream above.
- Rule:
  - [PowerShell attributes and validators](./rules/attributes-validators-outputtype.md)
- Map: [Attributes and validators map](./references/attributes-validators-map.md)

## Documentation, help, and style

- Use for comment-based help block structure and required sections (`.SYNOPSIS`,
  `.DESCRIPTION`, `.PARAMETER`, `.EXAMPLE`, `.OUTPUTS`, `.NOTES`) for advanced
  functions, MAML/PlatyPS help for compiled cmdlets, `.OUTPUTS`/`[OutputType]`
  alignment, script-body alias avoidance, `Read-Host` prohibition, `Write-Host`
  stream semantics, and the Tier-5 repo style overlay for `.ps1`/`.psm1` files.
- Rule:
  - [PowerShell documentation, help, and style](./rules/documentation-help-style.md)
- Map: [Documentation and style map](./references/documentation-style-map.md)

## Advanced scenarios

- Use for cmdlet testing patterns, help authoring integration, formatting
  extensions, and integration examples. These are linked references, not rule
  files.
- Reference: [PowerShell cmdlet cookbook index](./references/cookbook-index.md)

## Package conventions

- Every rule follows the shared section contract in
  [rules/_sections.md](./rules/_sections.md): `Purpose`, `Default guidance`,
  `Avoid`, `Review checklist`, `Related files`, and `Source anchors`.
- Use [the rule template](./templates/rule-template.md) for new rules,
  [the research pack template](./templates/research-pack-template.md) for
  scoped source inventories, and
  [the comparison matrix template](./templates/comparison-matrix-template.md)
  for external comparisons.
- Use [metadata.json](./metadata.json) as the registration-ready inventory for
  entrypoints, workstream coverage, and distribution notes.
- The taxonomy and preferred ordering live in
  [assets/taxonomy.json](./assets/taxonomy.json) and
  [assets/section-order.json](./assets/section-order.json).

## Standalone-first note

- This skill is authored as a standalone package under `skills`.
- If you document or install the package directly, use
  `npx skills add <source>` rather than `npx skill add`.
- Keep PowerShell cmdlet-specific guidance here. Pull broader C# or .NET
  guidance from `martix-dotnet-csharp` only when the task clearly widens
  beyond compiled cmdlet development.
