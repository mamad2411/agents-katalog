# Skill: Background Worker

## Quando carregar

Carregue esta Skill para `BackgroundService`, `IHostedService`, polling, jobs ou processamento assíncrono em background.

## Objetivo

Implementar processamento resiliente, cancelável, observável e sem duplicar regras de negócio.

## Regras

- Worker é adapter de entrada.
- Delegar lógica para Application.
- Respeitar `stoppingToken`.
- Criar scopes para dependências scoped.
- Não manter estado crítico somente em memória.
- Evitar loops agressivos.
- Preferir `PeriodicTimer` ou mecanismo equivalente quando houver polling.
- Não usar retry infinito.
- Retry somente para falhas transitórias.
- Aplicar backoff e jitter quando apropriado.
- Tornar processamento idempotente quando uma mensagem/trabalho puder ser repetido.

## Fluxo recomendado

```text
Worker
  -> obtém trabalho
  -> cria scope
  -> chama Application
  -> registra resultado
  -> confirma/atualiza estado
```

## Shutdown

O Worker deve permitir encerramento gracioso.

Operações longas devem observar cancelamento e evitar iniciar novo trabalho quando shutdown já foi solicitado.

## Falhas

Distinguir falha transitória, falha permanente, dado inválido e regra de negócio rejeitada.

Não retryar indiscriminadamente erros permanentes.

## Testes

Teste prioritariamente delegação correta, cancelamento, retry policy, idempotência, tratamento de falha e mecanismo de aquisição de trabalho.

Não testar regras de negócio novamente no Worker.
