---
name: galactica
description: "Use before changing a JS/TS file: every importer, including package-name imports grep misses, which tests to run, and whether the edit closes an import cycle. Also use when asked what imports or depends on a file, why one file reaches another, which tests cover it, whether files form an import cycle, or where an exported symbol is defined, and run its overview when you don't know where to start. Covers Vue, Svelte, Astro, MDX and Marko files too."
---

# Galactica

Galactica answers from this repository's import graph. Run it from the repository root. It reads files and never runs the repository's code. Each answer gives `path:line` or a path, so open exactly that file at that line.

## Before you change a file

1. Run `npx --prefix / @cognitap/galactica uses <file>`. It lists every file that imports this one, with the names each takes, including imports through package names and path aliases that grep misses. Then it lists the tests, closest first. A test that imports the file through other modules says `via <module>`, the importer its path starts from. `N more tests reach it only through <module>` counts tests that pass through a module most of the repository imports; run them only for a broad change.
2. The test list holds only tests that import the file. End-to-end, playground and fixture-driven tests that load it through a dev server, a build or a config can be missing. Also grep the test folders for the feature's name, such as `sourcemap` for `server/sourcemap.ts`, and add those tests.
3. Make the edit, and update the dependents it affects.
4. Run the tests from steps 1 and 2 with the repository's test command.
5. If you added an import, run `npx --prefix / @cognitap/galactica deps <file>`. A line `in an import cycle` that `uses` did not print before means your import closed a loop. Import from a lower module instead, or pass a callback.

`uses` also takes a package name, a package directory or a folder. `--depth <n>` lists dependents more import steps away.

## Finding a definition

`npx --prefix / @cognitap/galactica where <name>` lists each definition of an exported function, class, component, type or constant, with its signature, followed through re-exports to the file that defines it. It finds only exported symbols, so use grep alongside it for local names, strings and call sites.

## When you don't know where to start

`npx --prefix / @cognitap/galactica overview` lists the packages, their areas in dependency order and the most imported modules. Skip it when you already know which file to open.

## Import cycles

Leave an existing import cycle alone unless the task asks you to break it or it causes a load-time bug, such as "Cannot access 'X' before initialization" or a value that is `undefined` at startup. Then run `npx --prefix / @cognitap/galactica cycles`. It marks the imports `used at load time` and `break here` on the imports to cut: move what both modules need into a third, lower module, pass a callback instead of importing, or merge modules that cannot be separated.

## Other commands

- `npx --prefix / @cognitap/galactica deps <file>` lists what a file imports, inside the repository and outside it.
- `npx --prefix / @cognitap/galactica outline <file>` lists a file's exported symbols with their lines and signatures, without reading the whole file.
- `npx --prefix / @cognitap/galactica path <from> <to>` shows the shortest chain of imports by which one file reaches another. `--all` lists every chain, up to 20.
- `npx --prefix / @cognitap/galactica health` lists import cycles, oversized areas, and imports that reach into another package's internals. When the repository has `galactica-health.json`, findings recorded there are left out and the count of them is printed. Run `npx --prefix / @cognitap/galactica accept` only when asked to update that file.
- When the repository has `galactica-map.json`, it is a committed map of packages and areas. If a command says it is stale, run `npx --prefix / @cognitap/galactica check` to see which areas changed. Run `npx --prefix / @cognitap/galactica snapshot` only when asked to update the file.
- `--json` on any of these prints structured output.
