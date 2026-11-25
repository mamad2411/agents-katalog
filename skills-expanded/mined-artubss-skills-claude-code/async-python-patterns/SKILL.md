---
name: async-python-patterns
description: "Orientação abrangente para implementar aplicações Python assincronous usando asyncio, padrões de programação concorrente e async/await para construir sistemas de alto desempenho e não bloqueantes."
risk: safe
source: community
date_added: "2026-02-27"
---

# Padrões Async Python

Orientação abrangente para implementar aplicações Python assincronous usando asyncio, padrões de programação concorrente e async/await para construir sistemas de alto desempenho e não bloqueantes.

## Use essa skill quando

- Construindo APIs web assincronous (FastAPI, aiohttp, Sanic)
- Implementando operações I/O concorrentes (banco de dados, arquivo, rede)
- Criando web scrapers com requisições concorrentes
- Desenvolvendo aplicações em tempo real (servidores WebSocket, sistemas de chat)
- Processando múltiplas tarefas independentes simultaneamente
- Construindo microservices com comunicação assincronous
- Otimizando workloads vinculados a I/O
- Implementando tarefas assincronous em background e filas

## Não use essa skill quando

- O workload é vinculado a CPU com I/O mínimo.
- Um script sincronous simples é suficiente.
- O ambiente de runtime não consegue suportar uso de asyncio/event loop.

## Instruções

- Esclareça características do workload (I/O vs CPU), targets e restrições de runtime.
- Escolha padrões de concorrência (tasks, gather, queues, pools) com regras de cancelamento.
- Adicione timeouts, backpressure e tratamento de erros estruturado.
- Inclua orientação de testes e debugging para caminhos de código assincronous.
- Se exemplos detalhados forem necessários, abra `resources/implementation-playbook.md`.

Consulte `resources/implementation-playbook.md` para padrões detalhados e exemplos.

## Recursos

- `resources/implementation-playbook.md` para padrões detalhados e exemplos.