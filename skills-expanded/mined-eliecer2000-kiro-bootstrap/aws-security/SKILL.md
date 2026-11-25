---
name: aws-security
description: AWS security implementation. Use when configuring IAM policies, managing secrets, setting up encryption, securing networking, hardening services or auditing configurations.
---

# AWS Security

Skill para implementar seguridad en workloads AWS: IAM least privilege, gestión de secretos, cifrado en tránsito y reposo, networking seguro, endurecimiento de servicios y auditoría de configuraciones.

## Principios fundamentales

- Least privilege siempre: cada componente tiene solo los permisos mínimos necesarios para funcionar.
- Defense in depth: múltiples capas de seguridad. No depender de un solo control.
- Cifrado por defecto: en tránsito (TLS 1.2+) y en reposo (KMS) para todo recurso que lo soporte.
- Secretos nunca en código: usar SSM Parameter Store (SecureString) o Secrets Manager.
- Auditoría continua: CloudTrail habilitado, Config rules activas, GuardDuty encendido.

## IAM: Políticas de mínimo privilegio

### Estructura de política IAM
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowDynamoDBReadWrite",
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:UpdateItem",
        "dynamodb:DeleteItem",
        "dynamodb:Query"
      ],
      "Resource": [
        "arn:aws:dynamodb:us-east-1:123456789012:table/orders",
        "arn:aws:dynamodb:us-east-1:123456789012:table/orders/index/*"
      ]
    }
  ]
}
```

### Reglas de IAM

- Nunca usar `"Resource": "*"` salvo para acciones que lo requieran (ej: `sts:GetCallerIdentity`, `logs:CreateLogGroup`).
- Nunca usar `"Action": "*"`. Listar acciones específicas.
- Usar conditions cuando sea posible: `aws:SourceArn`, `aws:PrincipalOrgID`, `aws:RequestedRegion`.
- Un rol IAM por Lambda. No compartir roles entre funciones con responsabilidades diferentes.
- Preferir políticas inline en CDK/Terraform sobre políticas managed custom (más fácil de auditar).
- Usar `aws:PrincipalTag` y ABAC para control de acceso basado en atributos en escenarios multi-tenant.

### Ejemplo CDK: permisos mínimos
```typescript
// ✅ Correcto: permisos específicos
table.grantReadWriteData(fn);
bucket.grantRead(fn);
queue.grantSendMessages(fn);

// ❌ Incorrecto: permisos excesivos
fn.addToRolePolicy(new iam.PolicyStatement({
  actions: ['dynamodb:*'],
  resources: ['*'],
}));
```

## Gestión de secretos

### SSM Parameter Store (preferido para configuración)
```typescript
// Almacenar
const param = new ssm.StringParameter(this, 'ApiKey', {
  parameterName: '/myapp/prod/api-key',
  stringValue: 'valor-secreto',
  type: ssm.ParameterType.SECURE_STRING,
  tier: ssm.ParameterTier.STANDARD,
});

// Leer en Lambda con Powertools
import { getParameter } from '@aws-lambda-powertools/parameters/ssm';
const apiKey = await getParameter('/myapp/prod/api-key', { decrypt: true });
```

### Secrets Manager (para rotación automática)
```typescript
const secret = new secretsmanager.Secret(this, 'DbPassword', {
  secretName: '/myapp/prod/db-password',
  generateSecretString: {
    excludePunctuation: true,
    passwordLength: 32,
  },
});

// Rotación automática cada 30 días
secret.addRotationSchedule('Rotation', {
  automaticallyAfter: cdk.Duration.days(30),
  rotationLambda: rotationFn,
});
```

### Cuándo usar cada uno
| Caso | Servicio |
|---|---|
| API keys, config strings | SSM Parameter Store (SecureString) |
| Passwords de DB con rotación | Secrets Manager |
| Tokens OAuth con refresh | Secrets Manager |
| Feature flags, URLs | SSM Parameter Store (String) |

## Cifrado

### En reposo (por servicio)
| Servicio | Cifrado | Configuración |
|---|---|---|
| DynamoDB | SSE con KMS | Habilitado por defecto (AWS managed key). Usar CMK para control total. |
| S3 | SSE-S3 o SSE-KMS | `BucketEncryption: S3_MANAGED` mínimo. KMS para compliance. |
| SQS | SSE-KMS | Habilitar explícitamente con CMK. |
| SNS | SSE-KMS | Habilitar explícitamente. |
| Lambda env vars | KMS | Cifradas por defecto con AWS managed key. |
| CloudWatch Logs | KMS | Opcional, recomendado para datos sensibles. |

### En tránsito
- TLS 1.2+ obligatorio en todas las comunicaciones.
- API Gateway: TLS habilitado por defecto.
- Endpoints de VPC: usar `PrivateDnsEnabled: true`.
- Enforce HTTPS en S3: bucket policy con `aws:SecureTransport` condition.

```json
{
  "Condition": {
    "Bool": { "aws:SecureTransport": "false" }
  },
  "Effect": "Deny",
  "Action": "s3:*",
  "Resource": "arn:aws:s3:::my-bucket/*"
}
```

## Networking seguro

### VPC solo cuando es necesario
- Lambda SIN VPC por defecto (menor cold start, menor complejidad).
- Lambda CON VPC solo si necesita acceso a: RDS, ElastiCache, recursos en subnets privadas.
- Si Lambda necesita VPC + internet: NAT Gateway en subnet pública, Lambda en subnet privada.

### Security Groups
- Principio: deny all, allow specific.
- Ingress: solo puertos necesarios desde fuentes específicas.
- Egress: restringir a destinos conocidos cuando sea posible.
- Nunca `0.0.0.0/0` en ingress para puertos de administración (SSH, RDP).

### VPC Endpoints (PrivateLink)
- Usar VPC endpoints para servicios AWS cuando Lambda está en VPC.
- Evita tráfico por internet y NAT Gateway.
- Servicios comunes: DynamoDB (Gateway), S3 (Gateway), SQS (Interface), SSM (Interface), Secrets Manager (Interface).

## S3: endurecimiento

```typescript
const bucket = new s3.Bucket(this, 'DataBucket', {
  encryption: s3.BucketEncryption.S3_MANAGED,
  blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
  versioned: true,
  enforceSSL: true,
  removalPolicy: cdk.RemovalPolicy.RETAIN,
  objectOwnership: s3.ObjectOwnership.BUCKET_OWNER_ENFORCED,
  lifecycleRules: [{
    id: 'archive-old-objects',
    transitions: [{
      storageClass: s3.StorageClass.INFREQUENT_ACCESS,
      transitionAfter: cdk.Duration.days(90),
    }],
  }],
});
```

## Auditoría y compliance

### CloudTrail
- Habilitado en todas las cuentas y regiones.
- Logs a S3 bucket centralizado con lifecycle policies.
- Integrar con CloudWatch Logs para alarmas en tiempo real.

### AWS Config
- Rules activas para detectar configuraciones no conformes:
  - `s3-bucket-public-read-prohibited`
  - `iam-policy-no-statements-with-admin-access`
  - `encrypted-volumes`
  - `lambda-function-public-access-prohibited`
  - `dynamodb-pitr-enabled`

### GuardDuty
- Habilitado en todas las cuentas.
- Findings enviados a EventBridge → SNS → equipo de seguridad.

## Anti-patrones a evitar

- ❌ `"Action": "*"` o `"Resource": "*"` en políticas IAM.
- ❌ Secretos en variables de entorno planas o en código.
- ❌ S3 buckets sin `BlockPublicAccess.BLOCK_ALL`.
- ❌ Lambda en VPC sin necesidad real.
- ❌ Security groups con `0.0.0.0/0` en ingress.
- ❌ Compartir un rol IAM entre múltiples Lambdas con responsabilidades diferentes.
- ❌ No habilitar cifrado en SQS, SNS o CloudWatch Logs con datos sensibles.
- ❌ CloudTrail deshabilitado.
- ❌ No rotar secretos periódicamente.
- ❌ Confiar solo en seguridad perimetral (VPC) sin IAM granular.

## Checklist de seguridad

- [ ] IAM roles con least privilege (acciones y recursos específicos).
- [ ] Un rol por Lambda, no roles compartidos.
- [ ] Secretos en SSM SecureString o Secrets Manager, nunca en código.
- [ ] Cifrado en reposo habilitado en todos los servicios.
- [ ] TLS 1.2+ en todas las comunicaciones.
- [ ] S3 con BlockPublicAccess, versioning y enforceSSL.
- [ ] Security groups con reglas mínimas y específicas.
- [ ] CloudTrail habilitado en todas las cuentas.
- [ ] AWS Config rules activas para compliance.
- [ ] GuardDuty habilitado.
- [ ] Rotación de secretos configurada donde aplica.
- [ ] VPC endpoints para servicios AWS cuando Lambda está en VPC.
