---
name: burp-extension-development
description: Design, implement, package, and test Burp Suite extensions using Java and the Montoya API, including Community edition UI integrations, request processing, and manual installation.
---

# Burp extension development

## Establish the extension contract

Determine the supported Burp editions and minimum version, entry points, user-visible actions, data lifetime, and required artifact. Distinguish a loadable extension JAR from a BApp submission. A request to build an extension does not imply installing it into a running session or sending requests.

Check the installed Burp/JVM and build tools at runtime when available. Keep machine paths, captured traffic, credentials, and workstation details out of this skill and distributable examples. Use synthetic fixtures.

## Choose and verify the API

Prefer Java with the maintained Montoya API for new extensions. Use the legacy Extender API only for an existing integration or a concrete compatibility requirement. Python extensions using that API require a compatible standalone Jython runtime; system Python is not a substitute.

Read the official documentation and verify exact signatures against the pinned API artifact. Do not assume the API artifact has the same version number as Burp. Select a Java compilation target supported by the intended Burp runtime. Keep the Montoya dependency compile-only/provided; Burp supplies it at runtime.

For Community compatibility, identify edition-dependent services before implementation. Context menus, Swing UI, and ordinary HTTP message access need no Scanner dependency. Do not infer Community support for Scanner, Collaborator, or AI features from an interface merely being present.

Useful primary sources:

- [Creating extensions](https://portswigger.net/burp/documentation/desktop/extend-burp/extensions/creating)
- [Montoya API documentation](https://portswigger.github.io/burp-extensions-montoya-api/javadoc/)
- [Montoya example extensions](https://github.com/PortSwigger/burp-extensions-montoya-api-examples)
- [Extension starter project](https://github.com/PortSwigger/ExtensionTemplateProject)
- [Release notes](https://portswigger.net/burp/releases)
- [Manual installation](https://portswigger.net/burp/documentation/desktop/extend-burp/extensions/installing/manual-install)

## Implement the smallest useful integration

Implement `BurpExtension.initialize(MontoyaApi)`, name the extension, and register the appropriate handlers. Keep parsing and transformation logic independent from Burp and UI code so behavior can be tested without a live project.

For context menus, handle both the message editor's current request/response and table selections. Prefer the current editor object when present; table selections may be empty or stale. Make multiple-selection behavior explicit. Capture the selected message when the user invokes the action. Never replace the user's original request merely to populate a tool dialog.

Build and update Swing components on the event dispatch thread. Apply Burp's theme and fonts. Move filesystem indexing and slow work into cancellable workers. Close dialogs and cancel workers when unloading. Show validation next to the action and disable actions that cannot produce a valid result.

Treat HTTP service destination, request target, Host header, body bytes, and displayed text as separate concepts. Preserve scheme, port, method, and supported content deliberately. Describe conversion limitations instead of silently altering unsupported requests.

Persist preferences only when needed. Keep request bodies, responses, cookies, authorization values, and generated commands in memory by default. Avoid writing them to logs or shipping them as fixtures.

For integrations with command-line tools, build an argument vector first and render it for an explicitly named shell. Never interpolate untrusted request data into executable shell fragments. Validate the target tool's option semantics using its own documentation and locally installed help.

For editable request dialogs, selection mapping, filesystem pickers, clipboard export, or shell-command generation, read [UI and export engineering](references/ui-and-export.md). It captures conversion and lifecycle pitfalls that are easy to miss in small context-menu extensions.

## Package and verify

Deliver source, a reproducible build, a ready-to-load JAR when the environment permits, and a README with the exact installation flow. Pin downloaded build dependencies and verify their integrity. Exclude build caches and API classes from the extension JAR.

Test the behavior that can fail: context source selection, request preservation, parser boundaries, empty selections, unavailable files, Unicode, shell quoting, and unload cleanup. Use an isolated GUI harness when practical. API-adapter tests can run against the target Burp JAR and bundled JVM without opening or changing the user's project. Separate a successful build, a synthetic UI test, API compatibility tests, and a real Burp load in the final report; none implies the others.

Document known unsupported cases and a short manual acceptance checklist for the requested Burp version. Never claim a live load or network test without having performed it.

When a live Burp configuration must be changed, consider its in-memory settings and shutdown writes before editing a settings file. Prefer a supported UI/API operation, or apply file changes after a clean shutdown within the user's authorized scope. A valid JSON file alone does not prove that the running application has adopted it.
