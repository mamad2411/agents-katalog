---
name: plugin-creator
description: Create or update a Tomcat plugin, give it only the permissions it needs, validate the package, and install it through package_install at a user-approved scope.
---

# Plugin Creator

Use this skill for a new plugin, a change to an existing plugin, or a package containing plugins and skills.

## Start small

A plugin is a directory with `plugin.json` and the JavaScript file named by its `main` field. Its public bridge object is `tomcat`. Do not import a runtime bridge file. Existing plugins that use the legacy alias continue to run, but new source, examples, and documentation must use `tomcat`.

```text
my-plugin/
|-- plugin.json
`-- main.js
```

Use `scripts/init_plugin.mjs <plugin-id> --out <directory>` to make a valid source skeleton. It creates source files only; it does not install anything. Replace its example tool before packaging.

## Design and validate

1. Give the plugin a lowercase hyphen-case `id`. It is a directory name: never use slashes, `..`, or an absolute path.
2. Start with the smallest event handler, command, or tool that proves the requested behavior.
3. Declare only the permissions and network hosts the plugin actually needs. A network permission needs an explicit host list.
4. Keep arguments and return values JSON values. A tool may accept the host’s string input, but it must parse and return JSON-compatible data rather than relying on hidden state.
5. Validate `plugin.json`, run the smallest focused test, and confirm the generated source calls `tomcat.registerTool`, `tomcat.registerCommand`, or another documented Tomcat bridge method.

The type declarations are in `assets/types/tomcat-plugin.d.ts`. Include them in a JavaScript or TypeScript project only for editor checking; the Tomcat host supplies the runtime bridge.

## Package and install

- **Plugin only:** package a directory containing `plugin.json`.
- **Skill only:** package a directory containing `SKILL.md`.
- **Combined package:** use `package.json`; `tomcat.plugins` and `tomcat.skills` must point to directories below the package root.

Ask which scope is intended. Use `package_install`; do not copy files into a managed resource directory or edit a registry. `scope` needs an explicit project root. `agent` and `global` require a separate user confirmation and audit record. A new installation is found on the next user turn; it does not replace a plugin currently running in the session.

Do not allow a resource path to leave its package root or cross a symbolic link.
