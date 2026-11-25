---
name: kotlin-coroutines-expert
description: "Padrões avançados para Kotlin Coroutines e Flow, cobrindo structured concurrency, tratamento de erros e testes."
risk: safe
source: community
date_added: "2026-02-27"
---

# Kotlin Coroutines Expert

## Visão Geral

Um guia para dominar programação assíncrona com Kotlin Coroutines. Aborda tópicos avançados como structured concurrency, transformações de `Flow`, tratamento de exceções e estratégias de testes.

## Quando Usar Esta Skill

- Use ao implementar operações assíncronas em Kotlin.
- Use ao projetar fluxos de dados reativos com `Flow`.
- Use ao depurar cancelamentos de coroutines ou exceções.
- Use ao escrever testes unitários para funções suspensas ou Flows.

## Guia Passo a Passo

### 1. Structured Concurrency

Sempre lance coroutines dentro de um `CoroutineScope` definido. Use `coroutineScope` ou `supervisorScope` para agrupar tarefas concorrentes.

```kotlin
suspend fun loadDashboardData(): DashboardData = coroutineScope {
    val userDeferred = async { userRepo.getUser() }
    val settingsDeferred = async { settingsRepo.getSettings() }
    
    DashboardData(
        user = userDeferred.await(),
        settings = settingsDeferred.await()
    )
}
```

### 2. Tratamento de Exceções

Use `CoroutineExceptionHandler` para escopos de nível superior, mas conte com `try-catch` dentro de funções suspensas para controle granular.

```kotlin
val handler = CoroutineExceptionHandler { _, exception ->
    println("Caught $exception")
}

viewModelScope.launch(handler) {
    try {
        riskyOperation()
    } catch (e: IOException) {
        // Trate erro de rede especificamente
    }
}
```

### 3. Fluxos Reativos com Flow

Use `StateFlow` para estado que precisa ser retido, e `SharedFlow` para eventos.

```kotlin
// Cold Flow (Lazy)
val searchResults: Flow<List<Item>> = searchQuery
    .debounce(300)
    .flatMapLatest { query -> searchRepo.search(query) }
    .flowOn(Dispatchers.IO)

// Hot Flow (State)
val uiState: StateFlow<UiState> = _uiState.asStateFlow()
```

## Exemplos

### Exemplo 1: Execução Paralela com Tratamento de Erros

```kotlin
suspend fun fetchDataWithErrorHandling() = supervisorScope {
    val task1 = async { 
        try { api.fetchA() } catch (e: Exception) { null } 
    }
    val task2 = async { api.fetchB() }
    
    // Se task2 falhar, task1 NÃO é cancelada por causa do supervisorScope
    val result1 = task1.await()
    val result2 = task2.await() // Pode lançar exceção
}
```

## Melhores Práticas

- ✅ **Faça:** Use `Dispatchers.IO` para operações de I/O bloqueante.
- ✅ **Faça:** Cancele escopos quando não forem mais necessários (ex: `ViewModel.onCleared`).
- ✅ **Faça:** Use `TestScope` e `runTest` para testes unitários de coroutines.
- ❌ **Não faça:** Use `GlobalScope`. Quebra structured concurrency e pode causar vazamentos.
- ❌ **Não faça:** Capture `CancellationException` a menos que relance.

## Solução de Problemas

**Problema:** Teste de coroutine trava ou falha de forma imprevisível.
**Solução:** Certifique-se de usar `runTest` e injete `TestDispatcher` nas suas classes para que você possa controlar o tempo virtual.