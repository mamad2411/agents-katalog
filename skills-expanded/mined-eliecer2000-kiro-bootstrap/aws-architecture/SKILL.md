---
name: aws-architecture
description: AWS architecture decisions, serverless patterns, event-driven design, service boundaries and Well-Architected Framework. Use when designing system architecture or making infrastructure tradeoffs.
---

# AWS Architecture

Skill para decisiones de arquitectura AWS-first, patrones serverless, event-driven, límites de servicios, segmentación por perfil, Well-Architected Framework y diseño de sistemas escalables.

## Principios fundamentales

- Serverless-first: preferir servicios gestionados (Lambda, DynamoDB, SQS, EventBridge, Step Functions) sobre infraestructura auto-gestionada (EC2, ECS) salvo justificación técnica clara.
- Event-driven por defecto: desacoplar componentes con eventos asíncronos. Comunicación síncrona solo cuando el cliente necesita respuesta inmediata.
- Diseñar para fallos: todo componente puede fallar. Implementar retries con exponential backoff, circuit breakers, dead-letter queues y timeouts explícitos.
- Least privilege: cada componente tiene solo los permisos mínimos necesarios.
- Infraestructura como código: toda infraestructura se define en CDK o Terraform. Cero recursos creados manualmente en consola.

## Pilares del Well-Architected Framework aplicados

### Excelencia operacional
- Automatizar deployments con CI/CD (CodePipeline, GitHub Actions).
- Runbooks documentados para incidentes comunes.
- Feature flags para rollouts graduales.
- Observabilidad desde día 1: logs estructurados, métricas custom, trazas distribuidas.

### Seguridad
- Cifrado en tránsito (TLS 1.2+) y en reposo (KMS) por defecto.
- IAM roles con políticas inline mínimas, nunca `*` en Resource salvo excepciones documentadas.
- Secrets en SSM Parameter Store (SecureString) o Secrets Manager, nunca en variables de entorno planas.
- VPC solo cuando se necesita acceso a recursos privados (RDS, ElastiCache). Lambdas sin VPC por defecto.

### Fiabilidad
- Multi-AZ por defecto en servicios que lo soporten.
- DLQ en toda cola SQS y suscripción SNS.
- Retry policies configuradas en Step Functions, EventBridge rules y Lambda event source mappings.
- Idempotencia en todos los handlers que procesan eventos (usar Powertools idempotency).

### Eficiencia de rendimiento
- Right-sizing de Lambda: empezar con 256MB, medir con Powertools y ajustar.
- Provisioned concurrency solo para endpoints con requisitos de latencia p99 < 100ms.
- DynamoDB on-demand para cargas impredecibles, provisioned para cargas estables y predecibles.
- Caching con DAX (DynamoDB), CloudFront (APIs públicas) o ElastiCache (datos compartidos).

### Optimización de costos
- Usar servicios pay-per-use (Lambda, DynamoDB on-demand, S3) para cargas variables.
- Savings Plans para cargas estables y predecibles.
- Monitorear costos con Cost Explorer y alertas de Budget.
- Evitar over-provisioning: medir antes de escalar.

## Patrones de arquitectura serverless

### API sincrónica
```
Cliente → API Gateway → Lambda → DynamoDB
                                → S3
```
- Para CRUD simple con respuesta inmediata.
- Timeout de API Gateway: 29s máximo. Si la operación puede tardar más, usar patrón asíncrono.

### Procesamiento asíncrono
```
Cliente → API Gateway → SQS → Lambda → DynamoDB
                    (202 Accepted)
```
- Para operaciones que no necesitan respuesta inmediata.
- SQS como buffer absorbe picos de tráfico.
- DLQ para mensajes que fallan después de N reintentos.

### Event-driven con EventBridge
```
Servicio A → EventBridge → Rule 1 → Lambda → DynamoDB
                         → Rule 2 → Step Functions → ...
                         → Rule 3 → SQS → Lambda → ...
```
- Para desacoplar dominios de negocio.
- Schema registry para contratos de eventos.
- Archive + Replay para reprocessing.

### Orquestación con Step Functions
```
API Gateway → Step Functions → Lambda A → Lambda B → DynamoDB
                             → SNS (notificación)
                             → Error handler
```
- Para workflows con múltiples pasos, branching, retries y error handling.
- Preferir Express Workflows para alta frecuencia (< 5 min).
- Standard Workflows para procesos largos (hasta 1 año).

### Streaming y procesamiento en tiempo real
```
DynamoDB Streams → Lambda → EventBridge → Consumers
Kinesis Data Streams → Lambda → S3 / DynamoDB / OpenSearch
```
- DynamoDB Streams para CDC (Change Data Capture) y sincronización.
- Kinesis para alto volumen de eventos en tiempo real.

## Límites de servicios críticos

| Servicio | Límite | Default | Ajustable |
|----------|--------|---------|-----------|
| Lambda | Concurrencia por cuenta/región | 1,000 | Sí |
| Lambda | Timeout máximo | 15 min | No |
| Lambda | Payload síncrono | 6 MB | No |
| Lambda | Payload asíncrono | 256 KB | No |
| API Gateway HTTP | Timeout | 30s | No |
| API Gateway REST | Timeout | 29s | No |
| DynamoDB | Tamaño de item | 400 KB | No |
| DynamoDB | Tamaño de transacción | 25 items | No |
| SQS | Tamaño de mensaje | 256 KB | No (usar S3 para payloads grandes) |
| EventBridge | Tamaño de evento | 256 KB | No |
| Step Functions | Tamaño de input/output | 256 KB | No |
| S3 | Tamaño de objeto | 5 TB | No |

## Decisiones de diseño por caso de uso

### ¿Cuándo usar Lambda vs Fargate/ECS?
- Lambda: operaciones cortas (< 15 min), cargas variables, event-driven.
- Fargate: procesos largos, cargas constantes, necesidad de más de 10GB RAM, containers existentes.

### ¿Cuándo usar DynamoDB vs RDS/Aurora?
- DynamoDB: access patterns conocidos, key-value o document, escala masiva, serverless.
- RDS/Aurora: queries ad-hoc complejas, JOINs frecuentes, transacciones ACID multi-tabla, reporting.

### ¿Cuándo usar SQS vs EventBridge vs SNS?
- SQS: buffering, procesamiento ordenado (FIFO), un solo consumidor por mensaje.
- EventBridge: routing basado en contenido, múltiples consumidores, schema evolution.
- SNS: fan-out simple a múltiples suscriptores, push notifications.

### ¿Cuándo usar Step Functions vs SQS chains?
- Step Functions: workflows con branching, parallel execution, error handling complejo, visibilidad.
- SQS chains: pipelines lineales simples, alto throughput, bajo costo.

## Segmentación por perfil de proyecto

### Backend API (Lambda + API Gateway + DynamoDB)
- Perfil más común para APIs serverless.
- Stack: API Gateway HTTP → Lambda → DynamoDB.
- IaC: CDK o Terraform.

### Full-stack con Amplify (React/Vue/Nuxt + Backend)
- Frontend en Amplify Hosting, backend con Amplify Gen 2 o CDK.
- Auth con Cognito, storage con S3, API con AppSync o API Gateway.

### Infraestructura pura (CDK o Terraform)
- Para equipos de plataforma que proveen recursos compartidos.
- Módulos reutilizables, state management, multi-account.

## Anti-patrones a evitar

- ❌ Lambda monolítico que hace todo (API + procesamiento + notificaciones).
- ❌ Comunicación síncrona en cadena (Lambda → Lambda → Lambda). Usar Step Functions o eventos.
- ❌ DynamoDB scan como patrón principal de lectura.
- ❌ Ignorar límites de servicios hasta que fallan en producción.
- ❌ VPC en Lambdas sin necesidad real (añade cold start y complejidad).
- ❌ Crear recursos manualmente en consola AWS.
- ❌ Usar el mismo rol IAM para todos los Lambdas.
- ❌ No tener DLQ en colas y event source mappings.
- ❌ Hardcodear ARNs, account IDs o nombres de recursos.
- ❌ Diseñar sin considerar idempotencia desde el inicio.

## Checklist de revisión de arquitectura

- [ ] Diagrama de arquitectura actualizado (C4 model o similar).
- [ ] Todos los servicios usan cifrado en tránsito y reposo.
- [ ] IAM roles con least privilege documentado.
- [ ] DLQ configurada en todas las colas y event sources.
- [ ] Retry policies y timeouts explícitos en cada integración.
- [ ] Límites de servicios revisados y requests de aumento enviados si necesario.
- [ ] Observabilidad configurada (logs, métricas, trazas).
- [ ] Costos estimados y alertas de budget configuradas.
- [ ] Disaster recovery plan documentado (RPO/RTO).
- [ ] Infraestructura 100% en código (CDK o Terraform).
