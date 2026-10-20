# 🌌 Xenon Project - Foundation Mandates

Este documento serve como a base de conhecimento e diretrizes fundamentais para o projeto Xenon. Ele deve ser lido por qualquer agente de IA ou desenvolvedor antes de realizar modificações no sistema.

## 🏗️ Arquitetura do Sistema

O Xenon é uma plataforma de pedidos orientada a eventos, baseada em microserviços e seguindo os princípios da **Clean Architecture**.

### Componentes:
- **Xenon.Orders.Api:** Serviço central de gerenciamento de pedidos (Core).
- **Xenon.Inventory.Api:** Microserviço responsável pela reserva de estoque.
- **Xenon.Notification.Api:** Microserviço de saída para notificações de usuários.

### Tecnologias Core:
- **Linguagem:** C# (.NET 9).
- **Persistência:** PostgreSQL (Bancos independentes por serviço).
- **Mensageria:** RabbitMQ (Event-Driven).
- **Observabilidade:** OpenTelemetry + Jaeger.
- **Logs:** Serilog (Structured JSON Logging).
- **Resiliência:** Polly (Retry/Circuit Breaker).

## 📐 Padrões de Código e Convenções

1.  **Clean Architecture:**
    - O **Domínio** (`Domain`) nunca deve depender de camadas externas.
    - A **Aplicação** (`Application`) contém os casos de uso e contratos.
    - A **Infraestrutura** (`Infrastructure`) lida com banco de dados e mensageria.
2.  **Mensageria:**
    - Usar o padrão de eventos de domínio para comunicação entre serviços.
    - Sempre propagar o `traceparent` nos headers do RabbitMQ para manter o rastreamento distribuído.
3.  **Resiliência:**
    - Todas as conexões externas (DB, RabbitMQ) devem implementar políticas de retry via Polly ou estratégias nativas do EF Core.
4.  **Testes:**
    - **Unitários:** Devem cobrir regras de negócio no Domínio e coordenação na Aplicação.
    - **Integração:** Devem usar **Testcontainers** para validar o fluxo real com Postgres e RabbitMQ.

## 🚀 Infraestrutura (Docker)

A infraestrutura completa é orquestrada via `docker-compose.yml`:
- `xenon-postgres` (Porta 5433): DB de Pedidos.
- `inventory-postgres` (Porta 5434): DB de Estoque.
- `xenon-rabbitmq` (Portas 5672, 15672): Broker.
- `xenon-jaeger` (Porta 16686): UI de Tracing.

## 🛠️ Comandos Comuns

- **Subir tudo:** `docker compose up --build`
- **Rodar Testes:** `dotnet test -p:AllowMissingPrunePackageData=true`
- **Adicionar Migração:** `dotnet ef migrations add <Nome> --project src/Xenon.Orders.Infrastructure --startup-project src/Xenon.Orders.Api`

---
*Documento gerado em 02/06/2026 via Gemini CLI.*
