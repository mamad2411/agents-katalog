---
name: aws-rds
description: Amazon RDS and Aurora database configuration. Use when setting up PostgreSQL/MySQL engines, Multi-AZ, read replicas, backups, encryption, IAM auth or parameter groups.
---

# AWS RDS

Skill para configurar Amazon RDS y Aurora: engines (PostgreSQL, MySQL), Multi-AZ, read replicas, backups, cifrado, IAM auth, parameter groups, Secrets Manager y mejores prácticas de seguridad y rendimiento.

## Principios fundamentales

- Multi-AZ habilitado en producción. Sin excepciones.
- Cifrado en reposo (KMS) y en tránsito (SSL/TLS) obligatorio.
- Credenciales en Secrets Manager con rotación automática. Nunca en código o variables de entorno planas.
- Backups automáticos habilitados con retención mínima de 7 días (35 en producción).
- Subnet groups privados. RDS nunca accesible desde internet.

## Instancia RDS segura (CDK)

```typescript
const db = new rds.DatabaseInstance(this, 'Database', {
  engine: rds.DatabaseInstanceEngine.postgres({
    version: rds.PostgresEngineVersion.VER_16,
  }),
  instanceType: ec2.InstanceType.of(ec2.InstanceClass.T4G, ec2.InstanceSize.MEDIUM),
  vpc,
  vpcSubnets: { subnetType: ec2.SubnetType.PRIVATE_ISOLATED },
  multiAz: true,
  storageEncrypted: true,
  credentials: rds.Credentials.fromGeneratedSecret('dbadmin'),
  backupRetention: cdk.Duration.days(35),
  deletionProtection: true,
  removalPolicy: cdk.RemovalPolicy.RETAIN,
  monitoringInterval: cdk.Duration.seconds(60),
});
```

## Aurora Serverless v2 (CDK)

```typescript
const cluster = new rds.DatabaseCluster(this, 'AuroraCluster', {
  engine: rds.DatabaseClusterEngine.auroraPostgres({
    version: rds.AuroraPostgresEngineVersion.VER_16_1,
  }),
  serverlessV2MinCapacity: 0.5,
  serverlessV2MaxCapacity: 8,
  writer: rds.ClusterInstance.serverlessV2('writer'),
  readers: [
    rds.ClusterInstance.serverlessV2('reader', { scaleWithWriter: true }),
  ],
  vpc,
  vpcSubnets: { subnetType: ec2.SubnetType.PRIVATE_ISOLATED },
  credentials: rds.Credentials.fromGeneratedSecret('dbadmin'),
  storageEncrypted: true,
  backupRetention: cdk.Duration.days(35),
  deletionProtection: true,
  removalPolicy: cdk.RemovalPolicy.RETAIN,
});
```

## Conexión desde Lambda

```typescript
// Usar RDS Proxy para connection pooling
const proxy = new rds.DatabaseProxy(this, 'Proxy', {
  proxyTarget: rds.ProxyTarget.fromInstance(db),
  secrets: [db.secret!],
  vpc,
  requireTLS: true,
});

// En el Lambda handler
import { RDSDataClient, ExecuteStatementCommand } from '@aws-sdk/client-rds-data';

const rdsData = new RDSDataClient({});

const result = await rdsData.send(new ExecuteStatementCommand({
  resourceArn: process.env.DB_CLUSTER_ARN,
  secretArn: process.env.DB_SECRET_ARN,
  database: 'mydb',
  sql: 'SELECT * FROM orders WHERE user_id = :userId',
  parameters: [{ name: 'userId', value: { stringValue: userId } }],
}));
```

## Parameter groups recomendados (PostgreSQL)

| Parámetro | Valor recomendado | Razón |
|---|---|---|
| `shared_preload_libraries` | `pg_stat_statements` | Monitoreo de queries |
| `log_min_duration_statement` | `1000` (ms) | Loguear queries lentas |
| `max_connections` | Según instance class | Evitar connection exhaustion |
| `work_mem` | `64MB` | Mejorar sorts y joins |
| `maintenance_work_mem` | `256MB` | Mejorar VACUUM y CREATE INDEX |

## Cuándo usar RDS vs DynamoDB vs Aurora

| Criterio | DynamoDB | RDS PostgreSQL | Aurora Serverless v2 |
|---|---|---|---|
| Access patterns | Conocidos, key-value | Ad-hoc, JOINs, SQL | Ad-hoc, JOINs, SQL |
| Escala | Masiva, automática | Vertical (instance class) | Auto-scaling (0.5-128 ACU) |
| Costo variable | Pay-per-request | Pay-per-hora (fijo) | Pay-per-ACU (variable) |
| Transacciones | Limitadas (25 items) | ACID completo | ACID completo |
| Serverless | Nativo | No | Sí |
| Caso ideal | APIs de alta escala | Apps tradicionales SQL | Cargas variables con SQL |

## Anti-patrones a evitar

- ❌ RDS accesible desde internet (public accessibility).
- ❌ Credenciales en código o variables de entorno planas.
- ❌ Sin Multi-AZ en producción.
- ❌ Sin backups automáticos.
- ❌ Sin cifrado en reposo.
- ❌ Conexiones directas desde Lambda sin RDS Proxy.
- ❌ Over-provisioning de instance class sin medir.
- ❌ Sin monitoring (Enhanced Monitoring, Performance Insights).
- ❌ Sin parameter group customizado.
- ❌ Usar RDS cuando DynamoDB cubre el caso de uso.

## Checklist de revisión RDS

- [ ] Multi-AZ habilitado en producción.
- [ ] Cifrado en reposo (KMS) y en tránsito (SSL).
- [ ] Credenciales en Secrets Manager con rotación.
- [ ] Subnet group privado (no accesible desde internet).
- [ ] Backups automáticos con retención adecuada.
- [ ] Enhanced Monitoring y Performance Insights habilitados.
- [ ] RDS Proxy para conexiones desde Lambda.
- [ ] Parameter group customizado con logging de queries lentas.
- [ ] Deletion protection habilitada.
- [ ] Read replicas configuradas si hay carga de lectura alta.
