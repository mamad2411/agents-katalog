---
name: aws-cloudfront
description: Amazon CloudFront CDN configuration. Use when setting up distributions, origins, cache behaviors, SSL/TLS, WAF integration, invalidations or Lambda@Edge functions.
---

# AWS CloudFront

Skill para configurar Amazon CloudFront como CDN: distribuciones, origins (S3, API Gateway, ALB), cache behaviors, SSL/TLS, WAF, invalidaciones, Lambda@Edge y mejores prácticas de rendimiento.

## Principios fundamentales

- HTTPS obligatorio: `ViewerProtocolPolicy: redirect-to-https` siempre.
- Origin Access Control (OAC) para S3 origins. Nunca hacer buckets públicos para servir contenido.
- Cache policies explícitas por path pattern. No depender de defaults.
- WAF habilitado en distribuciones de producción.
- Invalidaciones con moderación. Preferir versionado de assets (hash en filename).

## Distribución con S3 origin (CDK)

```typescript
const distribution = new cloudfront.Distribution(this, 'CDN', {
  defaultBehavior: {
    origin: origins.S3BucketOrigin.withOriginAccessControl(bucket),
    viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
    cachePolicy: cloudfront.CachePolicy.CACHING_OPTIMIZED,
    compress: true,
  },
  defaultRootObject: 'index.html',
  priceClass: cloudfront.PriceClass.PRICE_CLASS_100,
  minimumProtocolVersion: cloudfront.SecurityPolicyProtocol.TLS_V1_2_2021,
});
```

## Distribución con API Gateway origin (CDK)

```typescript
const apiOrigin = new origins.HttpOrigin(
  `${api.restApiId}.execute-api.${cdk.Aws.REGION}.amazonaws.com`,
  { originPath: '/prod' }
);

distribution.addBehavior('/api/*', apiOrigin, {
  viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.HTTPS_ONLY,
  cachePolicy: cloudfront.CachePolicy.CACHING_DISABLED,
  originRequestPolicy: cloudfront.OriginRequestPolicy.ALL_VIEWER_EXCEPT_HOST_HEADER,
  allowedMethods: cloudfront.AllowedMethods.ALLOW_ALL,
});
```

## Cache policies recomendadas

| Tipo de contenido | Cache Policy | TTL |
|---|---|---|
| Assets estáticos (JS, CSS, imágenes) | CACHING_OPTIMIZED | 1 año (versionado por hash) |
| HTML pages | Custom: 5 min | 300s |
| API responses | CACHING_DISABLED | 0 (pass-through) |
| Media (video, audio) | CACHING_OPTIMIZED | 1 año |
| Fonts | Custom: 1 año | 31536000s |

## Invalidaciones

```bash
# Invalidar archivos específicos
aws cloudfront create-invalidation \
  --distribution-id E1234567890 \
  --paths "/index.html" "/css/*"

# Invalidar todo (costoso, evitar)
aws cloudfront create-invalidation \
  --distribution-id E1234567890 \
  --paths "/*"
```

- Primeras 1000 invalidaciones/mes gratis. Después $0.005 por path.
- Preferir versionado de assets (`app.abc123.js`) sobre invalidaciones.
- Invalidaciones tardan 5-10 minutos en propagarse globalmente.

## WAF con CloudFront (CDK)

```typescript
const webAcl = new wafv2.CfnWebACL(this, 'WebACL', {
  scope: 'CLOUDFRONT',
  defaultAction: { allow: {} },
  rules: [
    {
      name: 'AWSManagedRulesCommonRuleSet',
      priority: 1,
      overrideAction: { none: {} },
      statement: {
        managedRuleGroupStatement: {
          vendorName: 'AWS',
          name: 'AWSManagedRulesCommonRuleSet',
        },
      },
      visibilityConfig: {
        sampledRequestsEnabled: true,
        cloudWatchMetricsEnabled: true,
        metricName: 'CommonRuleSet',
      },
    },
  ],
  visibilityConfig: {
    sampledRequestsEnabled: true,
    cloudWatchMetricsEnabled: true,
    metricName: 'WebACL',
  },
});
```

## Anti-patrones a evitar

- ❌ S3 buckets públicos como origin (usar OAC).
- ❌ HTTP sin redirect a HTTPS.
- ❌ Cache de contenido dinámico/personalizado sin cache key adecuada.
- ❌ Invalidaciones masivas frecuentes (usar versionado de assets).
- ❌ Sin WAF en producción.
- ❌ TTL demasiado largo en HTML (usuarios ven versiones viejas).
- ❌ Sin custom error pages (403, 404).
- ❌ Price class ALL cuando el tráfico es solo regional.

## Checklist de revisión CloudFront

- [ ] HTTPS obligatorio (redirect-to-https).
- [ ] OAC configurado para S3 origins.
- [ ] Cache policies explícitas por path pattern.
- [ ] WAF habilitado en producción.
- [ ] Custom error pages configuradas (403, 404, 500).
- [ ] Compresión habilitada (gzip/brotli).
- [ ] Price class adecuada al tráfico geográfico.
- [ ] Logging habilitado a S3 bucket.
- [ ] TLS 1.2+ como versión mínima.
- [ ] Assets versionados por hash (no depender de invalidaciones).
