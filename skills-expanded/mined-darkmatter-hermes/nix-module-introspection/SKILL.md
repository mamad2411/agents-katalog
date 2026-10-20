---
name: nix-module-introspection
description: Use when inspecting Nix module options from flake inputs.
---

# Nix module introspection

Inspect the evaluated Nix module option tree rather than guessing from examples or treating flake outputs as a schema.

## When to use

- A user asks what options an input's flake-parts, NixOS, nix-darwin, or Home Manager module accepts.
- You need an option's type, default, description, declaration source, or evaluated value.
- `nix flake show` reveals the input's outputs but not its module configuration surface.
- You need to distinguish top-level options from `perSystem` options or nested submodule options.

## Core principle

A flake input exposes module values such as `flakeModules.default` or `nixosModules.default`; it does not expose an option schema until a module system evaluates those modules. Inspect the evaluator's `options` result.

## Flake-parts: zero-edit REPL workflow

For a flake-parts input, evaluate only the input module with flake-parts' built-in debug output:

```console
$ nix repl
nix-repl> :lf .
nix-repl> m = inputs.flake-parts.lib.mkFlake { inherit inputs; } {
             imports = [ inputs.foo.flakeModules.default ];
             debug = true;
             systems = [ ];
           }
nix-repl> builtins.attrNames m.debug.options
```

Then inspect the input namespace and a leaf option:

```nix
builtins.attrNames m.debug.options.foo
m.debug.options.foo.enable.description
m.debug.options.foo.enable.type.description
m.debug.options.foo.enable.default
m.debug.options.foo.enable.declarations
```

This requires no repository edit and isolates the input's module from project-local overrides.

## Inspect the fully composed flake

When effective composition matters, temporarily set this in the actual flake-parts module body:

```nix
debug = true;
```

After `:lf .`, inspect:

```nix
debug.options                         # top-level schema
debug.config                          # effective top-level config
allSystems."aarch64-darwin".options  # perSystem schema
allSystems."aarch64-darwin".config   # effective perSystem config
```

`currentSystem` is only available when Nix permits `builtins.currentSystem`; prefer explicit `allSystems."<system>"` paths in reproducible examples.

## Other module families

Choose the evaluator that owns the module:

- `nixosModules.*` → `inputs.nixpkgs.lib.nixosSystem`, inspect the result's `options`.
- `darwinModules.*` → `inputs.nix-darwin.lib.darwinSystem`, inspect `options`.
- `homeManagerModules.*` → Home Manager's configuration/module evaluator, inspect `options`.
- Raw modules → `lib.evalModules { modules = [ ... ]; }`, adding required `specialArgs` and base modules.

Do not evaluate a platform module with plain `lib.evalModules` when it relies on option declarations and module arguments supplied by NixOS, nix-darwin, or Home Manager.

## Option object fields

Useful leaf fields commonly include:

```nix
option.description
option.type.description
option.default
option.example
option.declarations
option.value
```

If a module declares one option whose type is a submodule, nested declarations may live behind:

```nix
option.type.getSubOptions [ ]
```

rather than directly under the outer `options` attrset.

## Browse input source and generated docs

Resolve the locked source without manually reading `flake.lock`:

```sh
inputPath="$(nix flake archive --json . | jq -r '.inputs.foo.path')"
```

Then inspect generated option docs if the input ships them, or search its module declarations. Quote jq keys containing hyphens:

```sh
jq -r '.inputs["flake-parts"].path'
```

See `references/flake-parts-options-repl.md` for a validated worked example.

## Pitfalls

- `nix flake show` lists outputs; it does not show module option schemas.
- `builtins.attrNames inputs.foo.flakeModules.default` usually shows only module structure such as `_file` and `imports`, not evaluated options.
- `builtins.functionArgs` is not useful when an exported module is already an applied attrset.
- Do not add permanent debug outputs merely for a one-time query; prefer the zero-edit REPL evaluator.
- Quote system names and input keys containing hyphens.
- Use explicit subpaths and leaf fields to avoid forcing the entire option tree to JSON; option objects contain functions and cannot generally be serialized wholesale.

## Verification

A successful inspection should prove at least one real option's name, description, type, and default from the evaluated module. If evaluating a composed flake, also distinguish schema (`options`) from effective values (`config`).
