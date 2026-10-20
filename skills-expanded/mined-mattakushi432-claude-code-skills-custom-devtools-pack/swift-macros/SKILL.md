---
name: swift-macros
description: "When to activate: Swift Macros, @attached, freestanding macros, #stringify, macro expansion, SE-0382, SE-0389"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: swift
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Swift Macros

## Macro Types (Swift 5.9+)

| Type | Syntax | Use Case |
|------|--------|----------|
| Freestanding expression | `#expr(...)` | Transform an expression |
| Freestanding declaration | `#decl(...)` | Generate declarations |
| Attached member | `@Macro struct T {}` | Add members to a type |
| Attached peer | `@Macro func f()` | Add declarations alongside |
| Attached accessor | `@Macro var x` | Add getters/setters |
| Attached memberAttribute | `@Macro struct T {}` | Add attributes to members |
| Attached extension | `@Macro struct T {}` | Add extensions |

## Using Built-In Macros

```swift
// #stringify — returns both value and source text
let (value, code) = #stringify(2 + 2)
print(value, code)  // 4, "2 + 2"

// #file, #line, #column, #function
func log(_ message: String, file: String = #file, line: Int = #line) {
    print("[\(file):\(line)] \(message)")
}

// @Observable — replaces @Published ObservableObject boilerplate
import Observation

@Observable
class Counter {
    var count = 0
    var step = 1
    func increment() { count += step }
}

// SwiftUI auto-tracks any @Observable property accessed in body
struct CounterView: View {
    var counter: Counter  // no @ObservedObject needed
    var body: some View { Text("\(counter.count)") }
}
```

## Writing an Attached Member Macro

```swift
// Package.swift declaration
targets: [
    .macro(name: "MyMacros", dependencies: [
        .product(name: "SwiftSyntaxMacros", package: "swift-syntax"),
        .product(name: "SwiftCompilerPlugin", package: "swift-syntax"),
    ]),
]
```

```swift
// Implementation
import SwiftSyntax
import SwiftSyntaxMacros

public struct AutoInitMacro: MemberMacro {
    public static func expansion(
        of node: AttributeSyntax,
        providingMembersOf declaration: some DeclGroupSyntax,
        in context: some MacroExpansionContext
    ) throws -> [DeclSyntax] {
        guard let structDecl = declaration.as(StructDeclSyntax.self) else {
            throw MacroError.notAStruct
        }

        let storedProperties = structDecl.memberBlock.members
            .compactMap { $0.decl.as(VariableDeclSyntax.self) }
            .filter { $0.bindingSpecifier.tokenKind == .keyword(.var) }

        let params = storedProperties.compactMap { varDecl -> String? in
            guard let name = varDecl.bindings.first?.pattern.trimmedDescription,
                  let type = varDecl.bindings.first?.typeAnnotation?.type.trimmedDescription else { return nil }
            return "\(name): \(type)"
        }.joined(separator: ", ")

        let assignments = storedProperties.compactMap {
            $0.bindings.first?.pattern.trimmedDescription
        }.map { "self.\($0) = \($0)" }.joined(separator: "\n        ")

        return ["""
            init(\(raw: params)) {
                \(raw: assignments)
            }
            """]
    }
}

enum MacroError: Error { case notAStruct }
```

## Attached Accessor Macro Example

```swift
@Logged
var username: String = ""

// Expands to:
var username: String {
    get { _username }
    set {
        print("username changed from \(_username) to \(newValue)")
        _username = newValue
    }
}
```

## Testing Macros

```swift
import SwiftSyntaxMacrosTestSupport

final class AutoInitMacroTests: XCTestCase {
    func testExpansion() {
        assertMacroExpansion(
            """
            @AutoInit
            struct Point {
                var x: Double
                var y: Double
            }
            """,
            expandedSource: """
            struct Point {
                var x: Double
                var y: Double

                init(x: Double, y: Double) {
                    self.x = x
                    self.y = y
                }
            }
            """,
            macros: ["AutoInit": AutoInitMacro.self]
        )
    }
}
```

## Common Anti-Patterns

- **Overusing macros for simple code gen** — explicit code is often clearer and easier to debug
- **Macros without tests** — always test expansion with `assertMacroExpansion`
- **Side effects in macros** — macros must be pure; they may be called multiple times
- **Ignoring diagnostics** — emit `context.diagnose` for bad usage instead of silently failing
- **Not pinning `swift-syntax` version** — it must match the Swift toolchain exactly
