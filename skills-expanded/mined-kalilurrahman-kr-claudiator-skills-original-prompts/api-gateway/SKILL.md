---
name: api-gateway
description: Design and configure API gateway architecture covering routing, authentication, rate limiting, request transformation, and observability. Outputs gateway configuration for Kong, AWS API Gateway, or Nginx, with traffic management and security policies.
argument-hint: [gateway technology, auth method, rate limiting requirements, upstream services]
allowed-tools: Read, Write, Bash
---

# API Gateway

An API gateway is the front door to your microservices. It centralizes cross-cutting concerns — auth, rate limiting, logging, routing — so each service doesn't have to implement them. A well-configured gateway dramatically simplifies service development while improving security and observability.

## When to Use an API Gateway

| Situation | Recommendation |
|-----------|---------------|
| Single service, simple needs | Skip — use Nginx reverse proxy |
| Multiple services, shared auth | API gateway is the right tool |
| Public API with third-party consumers | Essential |
| Internal service mesh | Consider service mesh instead |
| Multi-cloud, multi-region | Gateway + service mesh together |

## Process

1. **Map upstream services** — what services need to be exposed and to whom.
2. **Define authentication strategy** — JWT, API key, OAuth, mTLS, or combinations.
3. **Configure routing** — path-based, header-based, or hostname-based routing.
4. **Set rate limits** — per consumer, per endpoint, global limits.
5. **Add request/response transforms** — header injection, payload transformation.
6. **Configure observability** — access logs, metrics, distributed tracing.
7. **Test end-to-end** — including auth failures, rate limit behavior, and failover.

## Output Format

### Kong Gateway Configuration

```yaml
# kong/kong.yaml — Declarative (deck) configuration

_format_version: "3.0"

services:
  - name: order-service
    url: http://order-service.production.svc.cluster.local:8080
    connect_timeout: 5000
    write_timeout: 10000
    read_timeout: 10000
    retries: 2
    tags: [production, orders]
    
    routes:
      - name: orders-v1
        paths: ["/api/v1/orders"]
        methods: [GET, POST, PUT, PATCH, DELETE]
        strip_path: false
        preserve_host: false
        tags: [production]
    
    plugins:
      # JWT Authentication
      - name: jwt
        config:
          key_claim_name: sub
          claims_to_verify: [exp, nbf]
          maximum_expiration: 3600
          run_on_preflight: false   # Don't require JWT on OPTIONS
      
      # Rate limiting per consumer
      - name: rate-limiting
        config:
          minute: 100
          hour: 3000
          policy: redis
          redis_host: redis.production.svc.cluster.local
          redis_port: 6379
          fault_tolerant: true     # Don't block traffic if Redis is down
          hide_client_headers: false
      
      # Request size limit
      - name: request-size-limiting
        config:
          allowed_payload_size: 10   # MB
          size_unit: megabytes
      
      # CORS
      - name: cors
        config:
          origins: ["https://app.example.com", "https://admin.example.com"]
          methods: [GET, POST, PUT, PATCH, DELETE, OPTIONS]
          headers: [Authorization, Content-Type, X-Request-ID]
          exposed_headers: [X-RateLimit-Remaining, X-RateLimit-Reset]
          credentials: true
          max_age: 3600
      
      # Request transformer — inject upstream headers
      - name: request-transformer
        config:
          add:
            headers:
              - "X-Gateway-Request-ID:$(uuid)"
              - "X-Consumer-ID:$(consumer.id)"
              - "X-Consumer-Username:$(consumer.username)"
          remove:
            headers:
              - Authorization   # Don't forward raw JWT to upstream
      
      # Response transformer
      - name: response-transformer
        config:
          add:
            headers:
              - "X-Content-Type-Options:nosniff"
              - "Strict-Transport-Security:max-age=31536000; includeSubDomains"
          remove:
            headers:
              - X-Powered-By
              - Server

  - name: user-service
    url: http://user-service.production.svc.cluster.local:8080
    
    routes:
      - name: users-v1
        paths: ["/api/v1/users"]
        methods: [GET, PUT, PATCH]
      
      - name: auth-endpoints
        paths: ["/api/v1/auth"]
        methods: [POST]
        # No JWT plugin on auth endpoints
    
    plugins:
      - name: jwt
        config:
          key_claim_name: sub
      
      - name: rate-limiting
        config:
          minute: 60
          hour: 1000
          policy: redis
          redis_host: redis.production.svc.cluster.local

  - name: public-api
    url: http://public-api-service.production.svc.cluster.local:8080
    
    routes:
      - name: public-v1
        paths: ["/api/v1/public"]
        methods: [GET]
    
    plugins:
      # API Key auth for public API
      - name: key-auth
        config:
          key_names: [X-API-Key, apikey]
          key_in_body: false
          hide_credentials: true   # Don't forward key to upstream
      
      # Stricter rate limit for public API
      - name: rate-limiting
        config:
          minute: 30
          hour: 500
          policy: redis
          redis_host: redis.production.svc.cluster.local

# Global plugins (apply to all routes)
plugins:
  - name: prometheus
    config:
      per_consumer: true
      status_code_metrics: true
      latency_metrics: true
      bandwidth_metrics: true
  
  - name: request-id
    config:
      header_name: X-Request-ID
      generator: uuid
      echo_downstream: true
  
  - name: file-log
    config:
      path: /dev/stdout    # Log to stdout for container log aggregation
      reopen: false

# Consumers (API key holders and JWT issuers)
consumers:
  - username: mobile-app-ios
    keyauth_credentials:
      - key: "{{ env.MOBILE_IOS_API_KEY }}"
    tags: [mobile, ios]
  
  - username: mobile-app-android
    keyauth_credentials:
      - key: "{{ env.MOBILE_ANDROID_API_KEY }}"
    tags: [mobile, android]
  
  - username: internal-dashboard
    jwt_secrets:
      - algorithm: RS256
        rsa_public_key: "{{ file '/secrets/dashboard-public.pem' }}"
    tags: [internal]

# Upstreams (load balancing)
upstreams:
  - name: order-service.production.svc.cluster.local
    algorithm: round-robin
    healthchecks:
      active:
        healthy:
          interval: 10
          successes: 2
        unhealthy:
          interval: 5
          http_failures: 3
          timeouts: 2
        http_path: /health
        https_verify_certificate: false
      passive:
        healthy:
          successes: 5
        unhealthy:
          http_failures: 5
          timeouts: 3
    targets:
      - target: "10.0.1.10:8080"
        weight: 100
      - target: "10.0.1.11:8080"
        weight: 100
      - target: "10.0.1.12:8080"
        weight: 100
```

### AWS API Gateway (CDK)

```typescript
// lib/api-gateway-stack.ts
import * as cdk from 'aws-cdk-lib';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as cognito from 'aws-cdk-lib/aws-cognito';
import * as wafv2 from 'aws-cdk-lib/aws-wafv2';
import { Construct } from 'constructs';

export class ApiGatewayStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Cognito User Pool for JWT auth
    const userPool = cognito.UserPool.fromUserPoolId(
      this, 'UserPool', process.env.USER_POOL_ID!
    );

    // WAF for the API (SQL injection, XSS, rate limiting)
    const webAcl = new wafv2.CfnWebACL(this, 'ApiWAF', {
      name: 'api-gateway-waf',
      scope: 'REGIONAL',
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
            metricName: 'CommonRuleSetMetric',
          },
        },
        {
          name: 'RateLimit',
          priority: 2,
          action: { block: {} },
          statement: {
            rateBasedStatement: {
              limit: 2000,             // 2000 requests per 5 minutes per IP
              aggregateKeyType: 'IP',
            },
          },
          visibilityConfig: {
            sampledRequestsEnabled: true,
            cloudWatchMetricsEnabled: true,
            metricName: 'RateLimitMetric',
          },
        },
      ],
      visibilityConfig: {
        sampledRequestsEnabled: true,
        cloudWatchMetricsEnabled: true,
        metricName: 'ApiWAFMetric',
      },
    });

    // REST API
    const api = new apigateway.RestApi(this, 'Api', {
      restApiName: 'example-api',
      description: 'Main API gateway',
      
      deployOptions: {
        stageName: 'v1',
        throttlingRateLimit: 1000,    // Requests per second
        throttlingBurstLimit: 2000,
        metricsEnabled: true,
        loggingLevel: apigateway.MethodLoggingLevel.INFO,
        dataTraceEnabled: false,      // Don't log request bodies (PII risk)
        accessLogDestination: new apigateway.LogGroupLogDestination(
          new cdk.aws_logs.LogGroup(this, 'ApiAccessLogs', {
            retention: cdk.aws_logs.RetentionDays.THIRTY_DAYS,
          })
        ),
        accessLogFormat: apigateway.AccessLogFormat.jsonWithStandardFields({
          caller: true,
          httpMethod: true,
          ip: true,
          protocol: true,
          requestTime: true,
          resourcePath: true,
          responseLength: true,
          status: true,
          user: true,
        }),
      },
      
      defaultCorsPreflightOptions: {
        allowOrigins: ['https://app.example.com'],
        allowMethods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
        allowHeaders: ['Authorization', 'Content-Type', 'X-Request-ID'],
        maxAge: cdk.Duration.hours(1),
      },
    });

    // Cognito Authorizer
    const authorizer = new apigateway.CognitoUserPoolsAuthorizer(this, 'Authorizer', {
      cognitoUserPools: [userPool],
      authorizerName: 'jwt-authorizer',
      identitySource: 'method.request.header.Authorization',
    });

    // Lambda backend
    const orderHandler = lambda.Function.fromFunctionArn(
      this, 'OrderHandler', process.env.ORDER_LAMBDA_ARN!
    );

    // Usage plans and API keys for external consumers
    const usagePlan = api.addUsagePlan('DefaultUsagePlan', {
      name: 'Standard',
      throttle: {
        rateLimit: 100,
        burstLimit: 200,
      },
      quota: {
        limit: 10000,
        period: apigateway.Period.DAY,
      },
    });

    const apiKey = api.addApiKey('PartnerApiKey', {
      apiKeyName: 'partner-key',
      description: 'API key for partner integrations',
    });

    usagePlan.addApiKey(apiKey);
    usagePlan.addApiStage({ stage: api.deploymentStage });

    // Routes
    const ordersResource = api.root.addResource('orders');
    
    ordersResource.addMethod('GET', new apigateway.LambdaIntegration(orderHandler), {
      authorizer,
      authorizationType: apigateway.AuthorizationType.COGNITO,
      requestValidator: new apigateway.RequestValidator(this, 'OrdersGetValidator', {
        restApi: api,
        validateRequestParameters: true,
      }),
      requestParameters: {
        'method.request.querystring.status': false,
        'method.request.querystring.page': false,
      },
    });

    ordersResource.addMethod('POST', new apigateway.LambdaIntegration(orderHandler), {
      authorizer,
      authorizationType: apigateway.AuthorizationType.COGNITO,
      requestValidator: new apigateway.RequestValidator(this, 'OrdersPostValidator', {
        restApi: api,
        validateRequestBody: true,
      }),
      requestModels: {
        'application/json': new apigateway.Model(this, 'CreateOrderModel', {
          restApi: api,
          contentType: 'application/json',
          schema: {
            type: apigateway.JsonSchemaType.OBJECT,
            required: ['items'],
            properties: {
              items: {
                type: apigateway.JsonSchemaType.ARRAY,
                items: {
                  type: apigateway.JsonSchemaType.OBJECT,
                  required: ['product_id', 'quantity'],
                  properties: {
                    product_id: { type: apigateway.JsonSchemaType.STRING },
                    quantity: { type: apigateway.JsonSchemaType.INTEGER, minimum: 1 },
                  },
                },
              },
            },
          },
        }),
      },
    });

    // WAF association
    new wafv2.CfnWebACLAssociation(this, 'WafAssociation', {
      resourceArn: api.deploymentStage.stageArn,
      webAclArn: webAcl.attrArn,
    });

    // Outputs
    new cdk.CfnOutput(this, 'ApiUrl', { value: api.url });
    new cdk.CfnOutput(this, 'ApiKey', { value: apiKey.keyId });
  }
}
```

### Nginx Gateway (Simpler Alternative)

```nginx
# /etc/nginx/conf.d/api-gateway.conf

upstream order_service {
    least_conn;
    server order-service-1:8080 weight=1 max_fails=3 fail_timeout=30s;
    server order-service-2:8080 weight=1 max_fails=3 fail_timeout=30s;
    server order-service-3:8080 weight=1 max_fails=3 fail_timeout=30s;
    keepalive 32;
}

upstream user_service {
    least_conn;
    server user-service-1:8080;
    server user-service-2:8080;
    keepalive 16;
}

# Rate limit zones
limit_req_zone $binary_remote_addr zone=api_global:10m rate=100r/m;
limit_req_zone $http_x_api_key zone=api_key:10m rate=60r/m;
limit_req_zone $binary_remote_addr zone=auth:10m rate=10r/m;

server {
    listen 443 ssl http2;
    server_name api.example.com;

    ssl_certificate     /etc/ssl/certs/api.example.com.crt;
    ssl_certificate_key /etc/ssl/private/api.example.com.key;
    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_ciphers         HIGH:!aNULL:!MD5;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;

    # Remove server version
    server_tokens off;

    # Request ID for tracing
    add_header X-Request-ID $request_id always;

    # Global rate limit
    limit_req zone=api_global burst=20 nodelay;
    limit_req_status 429;

    # JWT validation via auth_request
    location = /auth/validate {
        internal;
        proxy_pass http://auth-service:8080/validate;
        proxy_pass_request_body off;
        proxy_set_header Content-Length "";
        proxy_set_header X-Original-URI $request_uri;
        proxy_set_header X-Original-Method $request_method;
        proxy_set_header Authorization $http_authorization;
    }

    # Orders API
    location /api/v1/orders {
        # JWT validation
        auth_request /auth/validate;
        auth_request_set $auth_user_id $upstream_http_x_user_id;
        
        # Rate limiting
        limit_req zone=api_global burst=10 nodelay;
        
        # Upstream proxy
        proxy_pass http://order_service;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-User-ID $auth_user_id;
        proxy_set_header X-Request-ID $request_id;
        
        # Don't forward auth header to upstream
        proxy_set_header Authorization "";
        
        # Timeouts
        proxy_connect_timeout 5s;
        proxy_read_timeout 30s;
        proxy_send_timeout 10s;
    }

    # Auth endpoints — stricter rate limit, no JWT
    location /api/v1/auth {
        limit_req zone=auth burst=5 nodelay;
        
        proxy_pass http://user_service;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Request-ID $request_id;
    }

    # Health check endpoint (no auth, no rate limit)
    location /health {
        access_log off;
        return 200 '{"status":"ok"}';
        add_header Content-Type application/json;
    }

    # Default: 404
    location / {
        return 404 '{"error":"Not Found"}';
        add_header Content-Type application/json;
    }

    # Access log with timing
    log_format api_json escape=json
        '{'
            '"time":"$time_iso8601",'
            '"method":"$request_method",'
            '"uri":"$uri",'
            '"status":$status,'
            '"bytes_sent":$bytes_sent,'
            '"request_time":$request_time,'
            '"upstream_time":"$upstream_response_time",'
            '"request_id":"$request_id",'
            '"remote_addr":"$remote_addr",'
            '"user_agent":"$http_user_agent"'
        '}';
    
    access_log /var/log/nginx/api-access.log api_json;
    error_log  /var/log/nginx/api-error.log warn;
}

# HTTP → HTTPS redirect
server {
    listen 80;
    server_name api.example.com;
    return 301 https://$server_name$request_uri;
}
```

### Gateway Observability

```python
# monitoring/gateway_metrics.py
"""Parse gateway access logs and push metrics to Prometheus."""

import json
import time
from prometheus_client import Counter, Histogram, start_http_server

request_count = Counter(
    'gateway_requests_total',
    'Total requests through gateway',
    ['method', 'endpoint', 'status', 'upstream']
)

request_duration = Histogram(
    'gateway_request_duration_seconds',
    'Request duration through gateway',
    ['method', 'endpoint', 'upstream'],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10]
)

def process_log_line(line: str):
    try:
        entry = json.loads(line)
        
        endpoint = entry.get('uri', 'unknown').split('?')[0]   # Strip query params
        endpoint = normalize_endpoint(endpoint)   # /orders/123 → /orders/{id}
        
        request_count.labels(
            method=entry.get('method', 'unknown'),
            endpoint=endpoint,
            status=str(entry.get('status', 0)),
            upstream=entry.get('upstream', 'unknown'),
        ).inc()
        
        duration = float(entry.get('request_time', 0))
        request_duration.labels(
            method=entry.get('method', 'unknown'),
            endpoint=endpoint,
            upstream=entry.get('upstream', 'unknown'),
        ).observe(duration)
    
    except (json.JSONDecodeError, ValueError):
        pass

def normalize_endpoint(path: str) -> str:
    """Normalize dynamic path segments for metric cardinality control."""
    import re
    # Replace UUIDs and numeric IDs
    path = re.sub(r'/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', '/{uuid}', path)
    path = re.sub(r'/\d+', '/{id}', path)
    return path
```

## Rules

- **Centralize auth at the gateway** — don't implement JWT validation in every service.
- **Don't pass raw credentials upstream** — gateway validates auth, then injects user context via headers.
- **Rate limit at the gateway, not in services** — centralized enforcement is consistent and observable.
- **Request IDs are mandatory** — every request needs a traceable ID injected at the gateway.
- **Timeout at every layer** — gateway timeout, upstream timeout, and circuit breaker must all be configured.
- **Log structured access logs** — JSON format enables analytics; include method, path, status, duration, user.
- **Validate request schemas** — reject malformed requests at the gateway before they hit services.
- **WAF for public APIs** — OWASP managed rule sets block common attack patterns with minimal configuration.
- **Health check endpoints bypass auth** — monitoring must reach health checks without credentials.
- **Never log request bodies by default** — they contain PII and credentials; enable only for specific debugging.
