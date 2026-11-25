---
name: aws-s3
description: Amazon S3 bucket and object management. Use when configuring buckets, encryption, versioning, lifecycle policies, presigned URLs, replication or CloudFront CDN origins.
---

# AWS S3

Skill para gestión de Amazon S3: buckets, objetos, cifrado, versionado, lifecycle policies, presigned URLs, replicación, CloudFront como CDN origin y mejores prácticas de seguridad y costos.

## Principios fundamentales

- Buckets privados por defecto. `BlockPublicAccess.BLOCK_ALL` siempre habilitado.
- Cifrado en reposo obligatorio: SSE-S3 mínimo, SSE-KMS para compliance.
- Versionado habilitado en buckets con datos importantes.
- Lifecycle policies para mover datos a clases de almacenamiento más baratas y expirar objetos temporales.
- Nunca almacenar secretos, credenciales o PII sin cifrado adicional.

## Configuración segura de bucket (CDK)

```typescript
const bucket = new s3.Bucket(this, 'DataBucket', {
  encryption: s3.BucketEncryption.S3_MANAGED,
  blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
  versioned: true,
  enforceSSL: true,
  removalPolicy: cdk.RemovalPolicy.RETAIN,
  objectOwnership: s3.ObjectOwnership.BUCKET_OWNER_ENFORCED,
  lifecycleRules: [{
    id: 'transition-to-ia',
    transitions: [{
      storageClass: s3.StorageClass.INFREQUENT_ACCESS,
      transitionAfter: cdk.Duration.days(90),
    }, {
      storageClass: s3.StorageClass.GLACIER,
      transitionAfter: cdk.Duration.days(365),
    }],
    expiration: cdk.Duration.days(730),
  }],
});
```

## Presigned URLs para acceso temporal

```typescript
import { S3Client, GetObjectCommand, PutObjectCommand } from '@aws-sdk/client-s3';
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';

const s3 = new S3Client({});

// URL de descarga (15 minutos)
const downloadUrl = await getSignedUrl(s3, new GetObjectCommand({
  Bucket: process.env.BUCKET_NAME,
  Key: `uploads/${userId}/${fileId}`,
}), { expiresIn: 900 });

// URL de subida (5 minutos, máximo 10MB)
const uploadUrl = await getSignedUrl(s3, new PutObjectCommand({
  Bucket: process.env.BUCKET_NAME,
  Key: `uploads/${userId}/${fileId}`,
  ContentType: 'application/pdf',
}), { expiresIn: 300 });
```

## Clases de almacenamiento

| Clase | Costo/GB | Acceso | Caso de uso |
|---|---|---|---|
| Standard | $0.023 | Inmediato | Datos activos, assets de app |
| Intelligent-Tiering | $0.023 + monitoring | Inmediato | Patrones impredecibles |
| Standard-IA | $0.0125 | Inmediato (cargo por acceso) | Backups, datos infrecuentes |
| Glacier Instant | $0.004 | Inmediato | Archival con acceso rápido |
| Glacier Flexible | $0.0036 | Minutos a horas | Archival estándar |
| Deep Archive | $0.00099 | 12+ horas | Compliance, retención legal |

## Bucket policy: enforce HTTPS

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "EnforceHTTPS",
    "Effect": "Deny",
    "Principal": "*",
    "Action": "s3:*",
    "Resource": [
      "arn:aws:s3:::my-bucket",
      "arn:aws:s3:::my-bucket/*"
    ],
    "Condition": {
      "Bool": { "aws:SecureTransport": "false" }
    }
  }]
}
```

## Event notifications (CDK)

```typescript
// Trigger Lambda cuando se sube un archivo
bucket.addEventNotification(
  s3.EventType.OBJECT_CREATED,
  new s3n.LambdaDestination(processorFn),
  { prefix: 'uploads/', suffix: '.pdf' }
);

// Trigger SQS para procesamiento batch
bucket.addEventNotification(
  s3.EventType.OBJECT_CREATED,
  new s3n.SqsDestination(processingQueue),
  { prefix: 'data/' }
);
```

## Anti-patrones a evitar

- ❌ Buckets públicos (usar CloudFront + OAC).
- ❌ Sin cifrado en reposo.
- ❌ Sin versionado en datos importantes.
- ❌ Sin lifecycle policies (datos acumulándose sin control).
- ❌ Presigned URLs con expiración demasiado larga.
- ❌ Bucket names con información sensible.
- ❌ Sin enforce SSL (permitir HTTP).
- ❌ Usar S3 como base de datos (para eso está DynamoDB).
- ❌ Subir archivos grandes sin multipart upload.
- ❌ Sin logging de acceso habilitado en producción.

## Checklist de revisión S3

- [ ] BlockPublicAccess.BLOCK_ALL habilitado.
- [ ] Cifrado en reposo (SSE-S3 o SSE-KMS).
- [ ] Versionado habilitado para datos importantes.
- [ ] Lifecycle policies configuradas.
- [ ] Enforce SSL con bucket policy.
- [ ] CloudFront + OAC para servir contenido público.
- [ ] Event notifications configuradas donde aplica.
- [ ] Access logging habilitado en producción.
- [ ] CORS configurado solo con dominios específicos.
- [ ] Presigned URLs con expiración mínima necesaria.
