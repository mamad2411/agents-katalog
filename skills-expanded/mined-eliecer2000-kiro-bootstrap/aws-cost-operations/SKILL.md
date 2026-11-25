---
name: aws-cost-operations
description: AWS cost optimization and operations. Use when analyzing costs with Cost Explorer, setting budgets, right-sizing resources, evaluating Savings Plans or reducing per-service costs.
---

# AWS Cost & Operations

Skill para optimización de costos AWS, monitoreo de gastos, presupuestos, right-sizing, Savings Plans, análisis con Cost Explorer y estrategias de reducción de costos por servicio.

## Principios fundamentales

- Cost awareness desde día 1. Estimar costos antes de desplegar.
- Tag everything: tags de `Project`, `Environment`, `Team`, `ManagedBy` en todos los recursos.
- Right-size primero, reservar después. Medir uso real antes de comprar Savings Plans.
- Alertas de presupuesto configuradas. Nunca operar sin Budget alerts.
- Revisar costos semanalmente. Cost Explorer como herramienta principal.

## Estrategias de optimización por servicio

| Servicio | Estrategia | Ahorro estimado |
|---|---|---|
| Lambda | Right-size memory (Powertools Tracer), ARM64 (Graviton) | 20-40% |
| DynamoDB | On-demand → Provisioned con auto-scaling para cargas estables | 30-50% |
| S3 | Lifecycle policies (IA → Glacier), Intelligent-Tiering | 40-70% |
| EC2 | Savings Plans, Spot para batch, right-sizing | 30-60% |
| RDS | Reserved Instances, Aurora Serverless v2 para cargas variables | 30-50% |
| NAT Gateway | VPC endpoints para tráfico a servicios AWS | 50-80% |
| CloudWatch | Ajustar log retention, filtrar métricas innecesarias | 20-40% |

## Presupuestos y alertas (CDK)

```typescript
new budgets.CfnBudget(this, 'MonthlyBudget', {
  budget: {
    budgetName: `${projectName}-monthly`,
    budgetType: 'COST',
    timeUnit: 'MONTHLY',
    budgetLimit: { amount: 500, unit: 'USD' },
  },
  notificationsWithSubscribers: [
    {
      notification: {
        notificationType: 'ACTUAL',
        comparisonOperator: 'GREATER_THAN',
        threshold: 80,
        thresholdType: 'PERCENTAGE',
      },
      subscribers: [{ subscriptionType: 'EMAIL', address: 'team@example.com' }],
    },
    {
      notification: {
        notificationType: 'FORECASTED',
        comparisonOperator: 'GREATER_THAN',
        threshold: 100,
        thresholdType: 'PERCENTAGE',
      },
      subscribers: [{ subscriptionType: 'EMAIL', address: 'team@example.com' }],
    },
  ],
});
```

## Tags de cost allocation obligatorios

```typescript
cdk.Tags.of(app).add('Project', projectName);
cdk.Tags.of(app).add('Environment', stage);
cdk.Tags.of(app).add('Team', teamName);
cdk.Tags.of(app).add('ManagedBy', 'CDK');
cdk.Tags.of(app).add('CostCenter', costCenter);
```

## Lambda: optimización de costos

```typescript
// ARM64 (Graviton2) es ~20% más barato y ~34% mejor rendimiento
new lambda.Function(this, 'Handler', {
  architecture: lambda.Architecture.ARM_64,
  memorySize: 256, // Medir con Powertools y ajustar
  timeout: cdk.Duration.seconds(30),
  // ...
});
```

- Usar `Powertools Tracer` para medir duración real y ajustar memory.
- ARM64 (Graviton2): 20% más barato que x86_64.
- Reducir bundle size con tree-shaking y minification.
- Excluir `@aws-sdk/*` del bundle (ya incluido en runtime).

## S3: lifecycle policies para reducir costos

| Clase | Costo (us-east-1) | Caso de uso |
|---|---|---|
| Standard | $0.023/GB | Acceso frecuente |
| Intelligent-Tiering | $0.023/GB + monitoring | Patrones de acceso impredecibles |
| Standard-IA | $0.0125/GB | Acceso infrecuente (>30 días) |
| Glacier Instant | $0.004/GB | Archival con acceso inmediato |
| Glacier Flexible | $0.0036/GB | Archival (minutos a horas) |
| Glacier Deep Archive | $0.00099/GB | Archival largo plazo (12+ horas) |

## Herramientas de análisis de costos

```bash
# Cost Explorer CLI
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-01-31 \
  --granularity MONTHLY \
  --metrics "BlendedCost" \
  --group-by Type=DIMENSION,Key=SERVICE

# Infracost para estimación pre-deploy (Terraform)
infracost breakdown --path .
infracost diff --path . --compare-to infracost-base.json
```

## Anti-patrones a evitar

- ❌ Desplegar sin estimar costos primero.
- ❌ Recursos sin tags de cost allocation.
- ❌ No tener Budget alerts configurados.
- ❌ Over-provisioning "por si acaso" sin medir.
- ❌ NAT Gateway para tráfico a servicios AWS (usar VPC endpoints).
- ❌ Logs sin retention policy (costos infinitos).
- ❌ DynamoDB provisioned sin auto-scaling.
- ❌ EBS snapshots huérfanos acumulándose.
- ❌ Elastic IPs no asociadas (cobran $0.005/hora).
- ❌ Ignorar Savings Plans para cargas estables.

## Checklist de costos

- [ ] Budget alerts configurados (80% actual, 100% forecasted).
- [ ] Tags de cost allocation en todos los recursos.
- [ ] Cost Explorer revisado semanalmente.
- [ ] Lambda en ARM64 (Graviton2) donde sea posible.
- [ ] S3 lifecycle policies configuradas.
- [ ] DynamoDB: modo de capacidad elegido conscientemente.
- [ ] VPC endpoints para servicios AWS frecuentes.
- [ ] Log retention configurado por ambiente.
- [ ] Savings Plans evaluados para cargas estables.
- [ ] Infracost o similar en CI para estimación pre-deploy.
