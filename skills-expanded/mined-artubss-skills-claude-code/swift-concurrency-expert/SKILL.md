---
name: swift-concurrency-expert
description: Revise e corrija problemas de concorrência em Swift, como isolamento de actor e violações de Sendable.
risk: safe
source: "Dimillian/Skills (MIT)"
date_added: "2026-03-25"
---

# Swift Concurrency Expert

## Visão Geral

Revise e corrija problemas de Concorrência em Swift em bases de código Swift 6.2+ aplicando isolamento de actor, segurança de Sendable e padrões de concorrência modernos com mudanças mínimas de comportamento.

## Quando Usar

- Quando o usuário pede para revisar o uso de concorrência em Swift ou corrigir diagnósticos do compilador.
- Quando você precisa de orientação sobre isolamento de actor, `Sendable`, `@MainActor` ou migração para async.

## Fluxo de Trabalho

### 1. Triagem do problema

- Capture os diagnósticos exatos do compilador e o(s) símbolo(s) infrator(es).
- Verifique as configurações de concorrência do projeto: versão da linguagem Swift (6.2+), nível de concorrência estrita e se a concorrência acessível (isolamento de actor padrão / main-actor-by-default) está habilitada.
- Identifique o contexto de actor atual (`@MainActor`, `actor`, `nonisolated`) e se um modo de isolamento de actor padrão está habilitado.
- Confirme se o código é vinculado à interface ou se se destina a executar fora do main actor.

### 2. Aplique o menor corrigimento seguro

Prefira edições que preservem o comportamento existente enquanto satisfazem segurança contra data-race.

Correções comuns:
- **Tipos vinculados à interface**: anote o tipo ou membros relevantes com `@MainActor`.
- **Conformidade de protocolo em tipos do main actor**: torne a conformidade isolada (ex: `extension Foo: @MainActor SomeProtocol`).
- **Estado global/estático**: proteja com `@MainActor` ou mova para um `actor`.
- **Trabalho em background**: mova trabalho custoso para uma função async `@concurrent` em um tipo `nonisolated` ou use um `actor` para guardar estado mutável.
- **Erros Sendable**: prefira tipos imutáveis/valor; adicione conformidade `Sendable` apenas quando correto; evite `@unchecked Sendable` a menos que você possa provar thread safety.

### 3. Verifique o corrigimento

- Recompile e confirme que todos os diagnósticos de concorrência foram resolvidos sem nenhum novo aviso introduzido.
- Execute a suite de testes para verificar regressões — mudanças de concorrência podem introduzir problemas em tempo de execução sutis mesmo quando a compilação está limpa.
- Se o corrigimento revelar novos avisos, trate cada um como uma triagem nova (retorne à etapa 1) e resolva iterativamente até que a compilação esteja limpa e os testes passem.

### Exemplos

**Tipo vinculado à interface — adicionando `@MainActor`**

```swift
// Before: data-race warning because ViewModel is accessed from the main thread
// but has no actor isolation
class ViewModel: ObservableObject {
    @Published var title: String = ""
    func load() { title = "Loaded" }
}

// After: annotate the whole type so all stored state and methods are
// automatically isolated to the main actor
@MainActor
class ViewModel: ObservableObject {
    @Published var title: String = ""
    func load() { title = "Loaded" }
}
```

**Isolamento de conformidade de protocolo**

```swift
// Before: compiler error — SomeProtocol method is nonisolated but the
// conforming type is @MainActor
@MainActor
class Foo: SomeProtocol {
    func protocolMethod() { /* accesses main-actor state */ }
}

// After: scope the conformance to @MainActor so the requirement is
// satisfied inside the correct isolation context
@MainActor
extension Foo: SomeProtocol {
    func protocolMethod() { /* safely accesses main-actor state */ }
}
```

**Trabalho em background com `@concurrent`**

```swift
// Before: expensive computation blocks the main actor
@MainActor
func processData(_ input: [Int]) -> [Int] {
    input.map { heavyTransform($0) }   // runs on main thread
}

// After: hop off the main actor for the heavy work, then return the result
// The caller awaits the result and stays on its own actor
nonisolated func processData(_ input: [Int]) async -> [Int] {
    await Task.detached(priority: .userInitiated) {
        input.map { heavyTransform($0) }
    }.value
}

// Or, using a @concurrent async function (Swift 6.2+):
@concurrent
func processData(_ input: [Int]) async -> [Int] {
    input.map { heavyTransform($0) }
}
```

## Material de referência

- Consulte `references/swift-6-2-concurrency.md` para mudanças, padrões e exemplos do Swift 6.2.
- Consulte `references/approachable-concurrency.md` quando o projeto está optado para o modo de concorrência acessível.
- Consulte `references/swiftui-concurrency-tour-wwdc.md` para orientação sobre concorrência específica do SwiftUI.