---
name: aws-patterns
description: AWS patterns — Lambda, S3, RDS, DynamoDB, API Gateway, CloudFront, IAM, and serverless architectures
globs: ["**/*.ts", "**/*.js", "**/*.py", "**/*.yaml", "**/*.yml", "**/*.json", "**/*.tf"]
alwaysApply: false
---

# AWS Patterns & Best Practices

AWS provides scalable, reliable infrastructure. Master Lambda, databases, API Gateway, CDN, and IAM for production deployments.

---

## Lambda Functions

**ALWAYS**:
- Keep Lambda cold start fast (< 1s): optimize dependencies, use Lambda layers
- Configure timeout and memory appropriately (128MB–10GB)
- Use environment variables for config (not hardcoded)
- Enable VPC only when needed (adds cold start time)
- Implement graceful shutdown (complete in-flight requests before timeout)
- Log structured JSON (CloudWatch Logs, X-Ray tracing)
- Use async invocation with Dead Letter Queues for reliability

**NEVER**:
- Store secrets in environment variables (use Secrets Manager)
- Assume Lambda instance persists across invocations
- Create connections in handler (pool in global scope)
- Ignore timeout/memory settings (tune for cost + performance)

### ✅ GOOD Lambda Pattern

```typescript
// handler.ts — Optimized Lambda function
import { APIGatewayProxyHandler } from 'aws-lambda';
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { GetCommand } from '@aws-sdk/lib-dynamodb';
import { SecretsManagerClient, GetSecretValueCommand } from '@aws-sdk/client-secrets-manager';

// Global scope — reused across invocations
const dynamoDB = new DynamoDBClient({ region: process.env.AWS_REGION });
const secretsManager = new SecretsManagerClient({ region: process.env.AWS_REGION });

let apiKey: string;

// Get secret once (cached across warm invocations)
async function getApiKey(): Promise<string> {
  if (apiKey) return apiKey;
  
  const response = await secretsManager.send(
    new GetSecretValueCommand({ SecretId: process.env.SECRET_ID })
  );
  apiKey = JSON.parse(response.SecretString || '{}').apiKey;
  return apiKey;
}

export const handler: APIGatewayProxyHandler = async (event) => {
  try {
    console.log(JSON.stringify({
      requestId: event.requestContext.requestId,
      path: event.path,
      method: event.httpMethod,
    }));

    // Example: Query DynamoDB
    const userId = event.pathParameters?.id;
    const response = await dynamoDB.send(
      new GetCommand({
        TableName: process.env.TABLE_NAME,
        Key: { id: userId },
      })
    );

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(response.Item || {}),
    };
  } catch (error) {
    console.error(JSON.stringify({
      error: error instanceof Error ? error.message : 'Unknown error',
      stack: error instanceof Error ? error.stack : undefined,
    }));

    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Internal server error' }),
    };
  }
};
```

### ❌ BAD Lambda Pattern

```typescript
// ❌ Hardcoded secret
const apiKey = 'sk-1234567890';

// ❌ Creating DynamoDB client in handler (cold start penalty)
export const handler = async (event) => {
  const dynamoDB = new DynamoDBClient(); // Every invocation!
  // ...
};

// ❌ No timeout handling
export const handler = async (event) => {
  const result = await veryLongOperation(); // Might timeout
  return result;
};
```

---

## RDS (Relational Database)

**ALWAYS**:
- Use Aurora PostgreSQL/MySQL (managed, auto-scaling, multi-AZ failover)
- Enable Multi-AZ for production (automatic failover)
- Use connection pooling (RDS Proxy for Lambda)
- Set appropriate backup retention (7-30 days minimum)
- Enable automated backups + point-in-time recovery
- Use IAM database authentication (no password management)
- Monitor: CPU, connections, replication lag via CloudWatch

**NEVER**:
- Store DB password in Lambda environment variables
- Use Single-AZ for production (no failover)
- Disable automated backups
- Skip security groups (restrict to application only)

### ✅ GOOD RDS Setup

```yaml
# Terraform: RDS Aurora PostgreSQL
resource "aws_rds_cluster" "postgres" {
  cluster_identifier      = "production-db"
  engine                  = "aurora-postgresql"
  engine_version          = "15.2"
  database_name           = "appdb"
  master_username         = "postgres"
  master_password         = random_password.db_password.result
  
  # Multi-AZ failover
  availability_zones      = ["us-east-1a", "us-east-1b", "us-east-1c"]
  
  # Backups
  backup_retention_period = 30
  preferred_backup_window = "03:00-04:00"
  
  # Performance
  db_subnet_group_name    = aws_db_subnet_group.postgres.name
  vpc_security_group_ids  = [aws_security_group.postgres.id]
  
  # Monitoring
  enabled_cloudwatch_logs_exports = ["postgresql"]
  monitoring_interval             = 60
  monitoring_role_arn             = aws_iam_role.rds_monitoring.arn
  
  tags = {
    Environment = "production"
  }
}

resource "aws_rds_cluster_instance" "postgres" {
  count              = 3  # Multi-AZ instances
  cluster_identifier = aws_rds_cluster.postgres.id
  instance_class     = "db.r6g.xlarge"
  engine              = aws_rds_cluster.postgres.engine
  engine_version      = aws_rds_cluster.postgres.engine_version
  
  publicly_accessible = false
}

# RDS Proxy for connection pooling (Lambda compatibility)
resource "aws_db_proxy" "postgres" {
  name                   = "production-proxy"
  engine_family          = "POSTGRESQL"
  auth {
    auth_scheme = "SECRETS"
    secret_arn  = aws_secretsmanager_secret.db_password.arn
  }
  role_arn               = aws_iam_role.proxy.arn
  vpc_subnet_ids         = aws_db_subnet_group.postgres.subnet_ids
  
  max_idle_connections_percent = 50
  max_connections              = 100
  connection_borrow_timeout    = 120
}
```

---

## DynamoDB (NoSQL)

**ALWAYS**:
- Use on-demand billing for unpredictable workloads
- Use provisioned with auto-scaling for predictable workloads
- Design for single-digit millisecond latency
- Use Global Secondary Indexes (GSI) for queries on non-key attributes
- Enable Point-in-Time Recovery (PITR) for production
- Set TTL for temporary data (auto-delete after expiration)
- Monitor: consumed capacity, throttling, hot partitions

**NEVER**:
- Use as relational database (denormalize instead)
- Create one-to-many relationships (denormalize data)
- Scan entire table frequently (use Query + Index)
- Ignore partition key design (causes hot partitions)

### ✅ GOOD DynamoDB Schema

```typescript
// DynamoDB table design
interface User {
  pk: string; // Partition key: USER#<userId>
  sk: string; // Sort key: PROFILE#<timestamp>
  id: string;
  email: string;
  createdAt: number;
  updatedAt: number;
  ttl?: number; // Time to live (seconds since epoch)
}

interface Order {
  pk: string; // USER#<userId>
  sk: string; // ORDER#<orderId>#<timestamp>
  orderId: string;
  total: number;
  items: OrderItem[];
  status: 'pending' | 'completed' | 'cancelled';
}

// Terraform: DynamoDB table
resource "aws_dynamodb_table" "app" {
  name           = "app-table"
  billing_mode   = "PAY_PER_REQUEST" // On-demand
  hash_key       = "pk"
  range_key      = "sk"
  
  attribute {
    name = "pk"
    type = "S"
  }
  
  attribute {
    name = "sk"
    type = "S"
  }
  
  # GSI for email lookup
  global_secondary_index {
    name            = "EmailIndex"
    hash_key        = "email"
    projection_type = "ALL"
  }
  
  attribute {
    name = "email"
    type = "S"
  }
  
  # Point-in-time recovery
  point_in_time_recovery {
    enabled = true
  }
  
  # TTL for auto-cleanup
  ttl {
    attribute_name = "ttl"
    enabled        = true
  }
  
  tags = {
    Environment = "production"
  }
}
```

---

## API Gateway

**ALWAYS**:
- Use REST API or HTTP API (HTTP is faster, cheaper for simple cases)
- Enable request/response logging to CloudWatch
- Implement throttling (rate limiting to prevent abuse)
- Use API keys + usage plans for per-client quotas
- Enable CORS only for specific origins (not *)
- Use WAF (Web Application Firewall) for production
- Validate request schemas before Lambda invocation (saves cost)

**NEVER**:
- Allow CORS from * (opens to any origin)
- Skip authentication (expose endpoints publicly)
- Ignore error handling (return meaningful error codes)
- Log sensitive data (passwords, tokens)

### ✅ GOOD API Gateway Setup

```yaml
# Terraform: API Gateway
resource "aws_api_gateway_rest_api" "api" {
  name        = "production-api"
  description = "Production API"
  
  endpoint_configuration {
    types = ["REGIONAL"] // Regional endpoint (lower latency)
  }
}

# Lambda integration
resource "aws_api_gateway_integration" "lambda" {
  rest_api_id      = aws_api_gateway_rest_api.api.id
  resource_id      = aws_api_gateway_resource.users.id
  http_method      = "GET"
  type             = "AWS_PROXY"
  integration_http_method = "POST"
  uri              = aws_lambda_function.handler.invoke_arn
}

# Request validation
resource "aws_api_gateway_request_validator" "validator" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  name                    = "RequestValidator"
  validate_request_body   = true
  validate_request_parameters = true
}

# Usage plan for rate limiting
resource "aws_api_gateway_usage_plan" "basic" {
  name = "BasicPlan"
  
  api_stages {
    api_id = aws_api_gateway_rest_api.api.id
    stage  = aws_api_gateway_stage.prod.stage_name
  }
  
  quota_settings {
    limit  = 10000  # Requests per month
    period = "MONTH"
  }
  
  throttle_settings {
    burst_limit = 100  // Concurrent requests
    rate_limit  = 50   // Requests per second
  }
}

# WAF for DDoS protection
resource "aws_wafv2_web_acl" "api" {
  name  = "api-waf"
  scope = "REGIONAL"
  
  default_action {
    allow {} // Default: allow
  }
  
  rule {
    name     = "RateLimitRule"
    priority = 1
    
    action {
      block {} // Block if over threshold
    }
    
    statement {
      rate_based_statement {
        limit              = 2000  // Requests per 5 minutes
        aggregate_key_type = "IP"
      }
    }
    
    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name               = "RateLimitRule"
      sampled_requests_enabled  = true
    }
  }
}
```

---

## CloudFront (CDN)

**ALWAYS**:
- Cache static assets (images, CSS, JS, fonts)
- Set appropriate cache-control headers (1 year for versioned assets)
- Use Origin Access Identity (OAI) to restrict S3 direct access
- Enable compression (gzip, brotli)
- Enable access logging for debugging
- Use security headers (CSP, X-Frame-Options, X-Content-Type-Options)
- Monitor: cache hit ratio (target > 80%), error rates

**NEVER**:
- Cache HTML pages (set max-age=0, no-cache)
- Cache sensitive data
- Allow direct S3 access (use OAI)
- Skip HTTPS (use TLS 1.2+)

### ✅ GOOD CloudFront Setup

```yaml
# Terraform: CloudFront distribution
resource "aws_cloudfront_distribution" "cdn" {
  enabled = true
  
  origin {
    domain_name = aws_s3_bucket.website.bucket_regional_domain_name
    origin_id   = "S3Origin"
    
    # Restrict S3 access via OAI
    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.oai.cloudfront_access_identity_path
    }
  }
  
  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3Origin"
    
    # Cache policy for assets
    cache_policy_id = aws_cloudfront_cache_policy.assets.id
    
    # Security headers
    response_headers_policy_id = aws_cloudfront_response_headers_policy.security.id
    
    # Compression
    compress = true
    
    # HTTP/3, HTTP/2
    viewer_protocol_policy = "redirect-to-https"
  }
  
  # Cache policy for versioned assets (1 year)
  cache_policy {
    name = "AssetsPolicy"
    
    default_ttl = 31536000  // 1 year
    max_ttl     = 31536000
    min_ttl     = 0
    
    parameters_in_cache_key_and_forwarded_to_origin {
      query_strings {
        query_string_behavior = "none"
      }
      
      headers {
        header_behavior = "none"
      }
    }
  }
  
  # Security headers
  response_headers_policy {
    name = "SecurityHeaders"
    
    security_headers_config {
      strict_transport_security {
        access_control_max_age_sec = 63072000  // 2 years
        include_subdomains         = true
        override                   = true
      }
      
      content_security_policy {
        content_security_policy = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
        override                = true
      }
      
      x_content_type_options {
        override = true
      }
      
      x_frame_options {
        frame_option = "DENY"
        override     = true
      }
    }
  }
  
  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
  
  viewer_certificate {
    cloudfront_default_certificate = true
  }
  
  # Access logging
  logging_config {
    include_cookies = false
    bucket          = aws_s3_bucket.logs.bucket_domain_name
    prefix          = "cloudfront/"
  }
}

# OAI for S3 access restriction
resource "aws_cloudfront_origin_access_identity" "oai" {
  comment = "OAI for S3 website"
}

# S3 bucket policy — only CloudFront can access
resource "aws_s3_bucket_policy" "website" {
  bucket = aws_s3_bucket.website.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          AWS = aws_cloudfront_origin_access_identity.oai.iam_arn
        }
        Action   = "s3:GetObject"
        Resource = "${aws_s3_bucket.website.arn}/*"
      }
    ]
  })
}
```

---

## IAM (Identity & Access Management)

**ALWAYS**:
- Use principle of least privilege (only required permissions)
- Create specific IAM roles per Lambda function, not shared roles
- Use managed policies when available (AWS-maintained)
- Enable MFA for console access
- Rotate access keys every 90 days
- Use temporary credentials (STS AssumeRole)
- Audit with CloudTrail (track all API calls)
- Review permissions quarterly

**NEVER**:
- Use root account for operations
- Grant * (all) permissions
- Hardcode access keys in code
- Share IAM roles across unrelated functions

### ✅ GOOD IAM Setup

```yaml
# Terraform: Least privilege Lambda role
resource "aws_iam_role" "lambda" {
  name = "GetUserLambdaRole"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

# CloudWatch Logs permission (basic Lambda requirement)
resource "aws_iam_role_policy" "logs" {
  name = "LambdaLogsPolicy"
  role = aws_iam_role.lambda.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

# DynamoDB read-only access
resource "aws_iam_role_policy" "dynamodb" {
  name = "DynamoDBReadPolicy"
  role = aws_iam_role.lambda.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:Query"
        ]
        Resource = aws_dynamodb_table.users.arn
      }
    ]
  })
}

# Secrets Manager access
resource "aws_iam_role_policy" "secrets" {
  name = "SecretsManagerPolicy"
  role = aws_iam_role.lambda.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = aws_secretsmanager_secret.api_key.arn
      }
    ]
  })
}
```

---

## AWS Security Checklist

- [ ] Lambda: Connection pooling, no hardcoded secrets, structured logging
- [ ] RDS: Multi-AZ, automated backups, IAM auth, no password in code
- [ ] DynamoDB: TTL configured, PITR enabled, on-demand or auto-scaling
- [ ] S3: Versioning enabled, public access blocked, encryption at rest
- [ ] API Gateway: Authentication, rate limiting, WAF, CORS restricted
- [ ] CloudFront: OAI for S3, cache headers, security headers, access logging
- [ ] IAM: Least privilege roles, no root access, MFA enabled, keys rotated
- [ ] CloudTrail: Enabled for audit trail, alerts for sensitive actions
- [ ] Secrets Manager: All secrets stored, rotated regularly
- [ ] VPC: Security groups, NACLs, private subnets for databases

---

## Summary

Good AWS architecture:
1. **Serverless first** — Lambda + managed services
2. **Resilient** — Multi-AZ, automated failover, backups
3. **Secure** — Least privilege IAM, secrets managed, encrypted
4. **Performant** — CDN for static content, caching, connection pooling
5. **Observable** — Logging, metrics, tracing, CloudTrail audit
6. **Cost-optimized** — Right-sized instances, on-demand pricing, resource cleanup

Master these patterns for production AWS deployments.
