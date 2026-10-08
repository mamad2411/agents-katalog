# AGENTS.md

`swift-tui-terminal-view` owns terminal-program embedding for SwiftTUI.
Use `swiftly run swift` with the pinned toolchain. Run `Scripts/native_gate.sh`
after code changes; update `docs/.public-api-baseline.txt` with
`Scripts/generate_public_api_baseline.sh` after reviewed public API changes.

`SwiftTUITerminalView` composes the public `SwiftTUIRuntime` view surface and
consumes `SwiftTUIPTYPrimitives`. `SwiftTUITerminalEmulation` is the only target
that imports SwiftTerm. Do not use package-internal framework APIs or add an SPI
for this package. Public manifests use exact tagged HTTPS sibling dependencies;
localization belongs to the coordination overlay.

Keep two-space indentation and the checked-in Swift formatting and strict
memory-safety settings. Tests use Swift Testing. `docs/` describes HEAD only;
plans and work tracking belong to the organization coordination repository.
`CLAUDE.md` is a symlink to this file.
