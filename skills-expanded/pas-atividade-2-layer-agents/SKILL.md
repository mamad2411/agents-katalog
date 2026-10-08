# Orientações do projeto

Este é um projeto didático e deve continuar pequeno. O escopo é cadastrar e
excluir salas, consultar disponibilidade e criar reservas. Não adicione login,
usuários, perfis, pagamentos, notificações ou integrações sem pedido explícito.

## Camadas

```text
presentation -> application -> domain
infrastructure -------------> domain
```

Mantenha um arquivo principal por camada enquanto o tamanho permitir. Só crie
uma nova abstração quando houver um segundo uso real.

## Regras

- Capacidade e quantidade de pessoas são inteiros positivos.
- O intervalo é `[startTime, endTime)` e o início deve ser anterior ao fim.
- Existe conflito quando a data é igual, o início existente é menor que o fim
  pedido e o fim existente é maior que o início pedido.
- Verificação de conflito e inserção usam a mesma transação `IMMEDIATE`.
- Dados do solicitante pertencem à reserva; não crie uma entidade de usuário.
- Datas usam `YYYY-MM-DD` e horários usam `HH:mm`.

Use TypeScript estrito no backend, SQLite com Drizzle e JavaScript nativo no
frontend. Antes de concluir uma alteração, execute `npm run check`.
