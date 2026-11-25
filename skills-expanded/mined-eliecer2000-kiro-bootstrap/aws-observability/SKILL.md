---
name: aws-observability
description: Observability for AWS workloads. Use when implementing structured logging, CloudWatch metrics, alarms, dashboards, X-Ray distributed tracing or monitoring operations.
---

# AWS Observability

Skill para implementar observabilidad completa en workloads AWS: logs estructurados con CloudWatch, métricas custom, alarmas, dashboards, trazas distribuidas con X-Ray, y operaciones de monitoreo proactivo.

## Principios fundamentales

- Observabilidad desde día 1, no como afterthought. Cada recurso desplegado debe tener logging, métricas y trazas configurados.
- Logs estructurados en JSON siempre. Nunca `print()` o `console.log()` con texto plano en producción.
- Tres pilares: Logs (qué pasó), Métricas (cuánto/cuándo), Trazas (dónde en el flujo).
- Alarmas accionables: cada alarma debe tener un runbook asociado. Si no sabes qué hacer cuando suena, no la crees.
- Usar AWS Lambda Powertools como estándar para logging, tracing y metrics en Lambda.

## Logging estructurado

### Con Powertools (Python)
```python
from aws_lambda_powertools import Logger
logger = Logger(service="order-service")

logger.info("Order created", extra={
    "order_id": order.id,
    "customer_id": order.customer_id,
    "total": order.total,
    "items_count": len(order.items),
})
```

### Con Powertools (TypeScript)
```typescript
import { Logger } from '@aws-lambda-powertools/logger';
const logger = new Logger({ serviceName: 'order-service' });

logger.info('Order created', {
  orderId: order.id,
  customerId: order.customerId,
  total: order.total,
  itemsCount: order.items.length,
});
```

### Log retention por ambiente
| Ambiente | Retención |
|---|---|
| dev | 7 días |
| staging | 30 días |
| prod | 365 días |

## Métricas custom

### Con Powertools (CDK + Lambda)
```typescript
import { Metrics, MetricUnit } from '@aws-lambda-powertools/metrics';
const metrics = new Metrics({ namespace: 'MiApp', serviceName: 'order-service' });

metrics.addMetric('OrderCreated', MetricUnit.Count, 1);
metrics.addDimension('Environment', process.env.STAGE ?? 'dev');
```

## Alarmas

### Alarma de errores Lambda (CDK)
```typescript
const errorAlarm = new cloudwatch.Alarm(this, 'LambdaErrorAlarm', {
  metric: fn.metricErrors({ period: cdk.Duration.minutes(5) }),
  threshold: 5,
  evaluationPeriods: 2,
  treatMissingData: cloudwatch.TreatMissingData.NOT_BREACHING,
  alarmDescription: 'Lambda errors > 5 in 10 min. Runbook: https://wiki/runbooks/lambda-errors',
});

errorAlarm.addAlarmAction(new cw_actions.SnsAction(alertsTopic));
```

### Alarmas recomendadas por servicio

| Servicio | Alarma | Threshold sugerido |
|---|---|---|
| Lambda | Error rate | > 1% de invocaciones |
| Lambda | Duration p99 | > 80% del timeout |
| Lambda | Throttles | > 0 |
| API Gateway | 5XX rate | > 1% |
| API Gateway | Latency p99 | > 3s |
| DynamoDB | ThrottledRequests | > 0 |
| SQS | AgeOfOldestMessage | > 5 min (ajustar según SLA) |

## Trazas distribuidas con X-Ray

### Habilitar en Lambda (CDK)
```typescript
new lambda.Function(this, 'Handler', {
  // ...
  tracing: lambda.Tracing.ACTIVE,
});
```

### Instrumentar con Powertools
```python
from aws_lambda_powertools import Tracer
tracer = Tracer(service="order-service")

@tracer.capture_method
def process_order(order_id: str) -> dict:
    # X-Ray captura automáticamente llamadas a AWS SDK
    order = table.get_item(Key={"PK": f"ORDER#{order_id}"})
    tracer.put_annotation(key="order_id", value=order_id)
    tracer.put_metadata(key="order_details", value=order)
    return order
```

### Propagación de trace context
- API Gateway → Lambda: automático con X-Ray habilitado.
- Lambda → Lambda (async): propagar `X-Amzn-Trace-Id` header.
- Lambda → SQS → Lambda: habilitar X-Ray en SQS y event source mapping.
- Step Functions: habilitar tracing en la state machine.

## Dashboards

### Dashboard operacional mínimo (CDK)
```typescript
const dashboard = new cloudwatch.Dashboard(this, 'ServiceDashboard', {
  dashboardName: `${serviceName}-${stage}`,
});

dashboard.addWidgets(
  new cloudwatch.GraphWidget({
    title: 'Lambda Invocations & Errors',
    left: [fn.metricInvocations()],
    right: [fn.metricErrors()],
    period: cdk.Duration.minutes(5),
  }),
  new cloudwatch.GraphWidget({
    title: 'API Latency',
    left: [api.metricLatency({ statistic: 'p50' }), api.metricLatency({ statistic: 'p99' })],
  }),
  new cloudwatch.GraphWidget({
    title: 'DynamoDB Consumed Capacity',
    left: [table.metricConsumedReadCapacityUnits(), table.metricConsumedWriteCapacityUnits()],
  }),
);
```

## CloudWatch Logs Insights queries útiles

```sql
-- Errores en las últimas 24h agrupados por función
fields @timestamp, @message
| filter @message like /ERROR/
| stats count() as errorCount by bin(1h)

-- Latencia p99 por endpoint
fields @timestamp, @duration
| filter ispresent(@duration)
| stats pct(@duration, 99) as p99, avg(@duration) as avg_duration by bin(5m)

-- Cold starts
fields @timestamp, @initDuration
| filter ispresent(@initDuration)
| stats count() as coldStarts, avg(@initDuration) as avgInitDuration by bin(1h)

-- Requests lentos (> 3s)
fields @timestamp, @duration, @requestId
| filter @duration > 3000
| sort @duration desc
| limit 20
```

## Anti-patrones a evitar

- ❌ `print()` o `console.log()` con texto plano en producción.
- ❌ Alarmas sin runbook asociado (nadie sabe qué hacer cuando suena).
- ❌ Alarmas con threshold demasiado sensible (alert fatigue).
- ❌ No configurar log retention (logs infinitos = costos infinitos).
- ❌ Loguear PII, tokens o secretos.
- ❌ Métricas sin dimensiones (no puedes filtrar por ambiente/servicio).
- ❌ Dashboards con 50 widgets que nadie mira.
- ❌ X-Ray deshabilitado en producción.
- ❌ No propagar correlation_id entre servicios.
- ❌ Monitorear solo errores, ignorar latencia y throughput.

## Checklist de observabilidad

- [ ] Logging estructurado (JSON) con Powertools en todas las funciones.
- [ ] Campos obligatorios: service, level, timestamp, request_id.
- [ ] Log retention configurado por ambiente.
- [ ] Métricas custom para KPIs de negocio.
- [ ] Alarmas con thresholds basados en SLOs y runbooks asociados.
- [ ] X-Ray habilitado en Lambda, API Gateway y servicios downstream.
- [ ] Dashboard operacional con métricas clave.
- [ ] Logs Insights queries guardadas para troubleshooting común.
- [ ] No se loguea PII ni secretos.
- [ ] Correlation ID propagado entre servicios.
