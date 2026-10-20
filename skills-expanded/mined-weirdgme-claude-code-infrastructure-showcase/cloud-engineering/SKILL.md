---
description: Cloud engineering guide covering AWS, Azure, GCP, and Oracle Cloud (OCI) services, multi-cloud strategies, serverless architectures, cloud-native patterns, cost optimization, cloud networking, security, migration strategies, and Well-Architected frameworks. Use when designing cloud infrastructure, implementing cloud services, optimizing cloud costs, or planning cloud migrations. (project)
---
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 SKILL ACTIVATED: cloud-engineering
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


# Cloud Engineering

Comprehensive guide for designing, building, and managing cloud infrastructure across AWS, Azure, GCP, and Oracle Cloud Infrastructure (OCI). This skill provides production-tested patterns for cloud-native architectures, multi-cloud strategies, serverless computing, and cloud optimization.

## When to Use This Skill

Automatically activates when working on:
- AWS, Azure, GCP, or Oracle Cloud (OCI) service selection and implementation
- Cloud architecture design and cloud-native patterns
- Multi-cloud and hybrid cloud strategies
- Serverless application development (Lambda, Cloud Functions, Azure Functions, OCI Functions)
- Cloud networking (VPC, VNet, Cloud VPC, OCI VCN)
- Cloud cost optimization and FinOps practices
- Cloud security and IAM configuration
- Cloud migration planning and execution
- Well-Architected Framework implementation

## Overview

**Purpose:** Enable teams to build robust, scalable cloud infrastructure leveraging the best services from AWS, Azure, and GCP while maintaining portability, cost efficiency, and operational excellence.

**Scope:**
- Cloud service selection and architecture (AWS, Azure, GCP, OCI)
- Multi-cloud and hybrid cloud strategies
- Serverless and event-driven architectures
- Cloud cost optimization and FinOps
- Cloud networking (VPC, VNet, VCN, peering, transit gateway, DNS)
- Cloud security and compliance (IAM, encryption, audit)
- Migration strategies and modernization
- Well-Architected frameworks and best practices

**This skill is for:**
- Cloud engineers designing cloud-native solutions
- Architects choosing between cloud services
- Teams implementing multi-cloud strategies
- Organizations migrating to cloud
- Engineers optimizing cloud costs

## Quick Start Checklist

When starting a cloud engineering task:

- [ ] Define requirements (scale, performance, compliance, budget)
- [ ] Choose cloud provider(s) based on needs
- [ ] Design for Well-Architected principles
- [ ] Plan networking topology (VPC, subnets, routing)
- [ ] Implement identity and access management
- [ ] Enable encryption at rest and in transit
- [ ] Set up cost tracking and budgets
- [ ] Implement monitoring and logging
- [ ] Design for high availability and disaster recovery
- [ ] Document architecture and operational runbooks

## Core Concepts

### 1. Cloud Service Models

**IaaS (Infrastructure as a Service):**
```
Control:  ████████░░  High control, high responsibility
Examples: EC2, Azure VMs, Compute Engine
Use Case: Lift-and-shift, custom configurations
```

**PaaS (Platform as a Service):**
```
Control:  █████░░░░░  Balanced control and management
Examples: Elastic Beanstalk, App Service, App Engine
Use Case: Application deployment, reduced ops
```

**FaaS (Function as a Service):**
```
Control:  ██░░░░░░░░  Low control, minimal management
Examples: Lambda, Azure Functions, Cloud Functions
Use Case: Event-driven, serverless, pay-per-use
```

**Managed Services:**
```
Control:  ███░░░░░░░  Vendor-managed operations
Examples: RDS, Cosmos DB, Cloud SQL
Use Case: Databases, analytics, managed ops
```

### 2. Cloud Provider Comparison

```
┌─────────────────┬──────────────────┬──────────────────┬──────────────────┬──────────────────┐
│    Service      │       AWS        │      Azure       │       GCP        │       OCI        │
├─────────────────┼──────────────────┼──────────────────┼──────────────────┼──────────────────┤
│ Compute         │ EC2              │ Virtual Machines │ Compute Engine   │ Compute Instance │
│ Containers      │ ECS, EKS         │ ACI, AKS         │ GKE, Cloud Run   │ OKE, Instances   │
│ Serverless      │ Lambda           │ Functions        │ Cloud Functions  │ Functions        │
│ Storage         │ S3               │ Blob Storage     │ Cloud Storage    │ Object Storage   │
│ Database        │ RDS, DynamoDB    │ SQL, Cosmos DB   │ Cloud SQL, Spanner│ Autonomous DB   │
│ Networking      │ VPC              │ Virtual Network  │ VPC              │ VCN              │
│ DNS             │ Route 53         │ DNS              │ Cloud DNS        │ DNS              │
│ CDN             │ CloudFront       │ CDN              │ Cloud CDN        │ CDN              │
│ IAM             │ IAM              │ Active Directory │ IAM              │ IAM              │
│ Monitoring      │ CloudWatch       │ Monitor          │ Cloud Monitoring │ Monitoring       │
└─────────────────┴──────────────────┴──────────────────┴──────────────────┴──────────────────┘
```

### 3. Well-Architected Principles

**Five Pillars (AWS Framework):**

1. **Operational Excellence:**
   - Automate operations
   - Document and share knowledge
   - Make frequent, small changes
   - Anticipate failure and learn

2. **Security:**
   - Implement strong identity foundation
   - Enable traceability
   - Apply security at all layers
   - Protect data in transit and at rest

3. **Reliability:**
   - Test recovery procedures
   - Automatically recover from failure
   - Scale horizontally
   - Stop guessing capacity

4. **Performance Efficiency:**
   - Use serverless architectures
   - Experiment and innovate
   - Go global in minutes
   - Consider mechanical sympathy

5. **Cost Optimization:**
   - Adopt consumption model
   - Measure overall efficiency
   - Eliminate undifferentiated work
   - Analyze and attribute expenditure

### 4. Multi-Cloud Architecture

```
┌────────────────────────────────────────────────────┐
│          Application Layer (Multi-Cloud)           │
│     (Containers, Kubernetes, Serverless)          │
└────────────────────────────────────────────────────┘
                      │
┌────────────────────────────────────────────────────┐
│       Abstraction Layer (Terraform, Pulumi)       │
│        (Service Mesh, API Gateway, CDN)           │
└────────────────────────────────────────────────────┘
                      │
      ┌───────────────┼───────────────┐
      │               │               │
┌─────▼────┐    ┌─────▼────┐    ┌─────▼────┐
│   AWS    │    │  Azure   │    │   GCP    │
│ Services │    │ Services │    │ Services │
└──────────┘    └──────────┘    └──────────┘
```

### 5. Serverless Architecture

**Event-Driven Pattern:**
```
Event Source → Event Router → Lambda Function → Destination
    │              │               │                │
  S3/API      EventBridge      Process          Database
  Upload       Rules           Transform         SNS/SQS
```

**Benefits:**
- No server management
- Automatic scaling
- Pay per execution
- Built-in high availability

**Challenges:**
- Cold starts
- Vendor lock-in
- Debugging complexity
- Execution limits

## Common Patterns

### Pattern 1: Multi-Region Architecture

```yaml
# High availability across regions
Architecture:
  Primary Region (us-east-1):
    - Application tier (Auto Scaling)
    - Database (RDS Multi-AZ)
    - Cache (ElastiCache cluster)
    - Load balancer (ALB)

  Secondary Region (us-west-2):
    - Read replicas (RDS)
    - Standby infrastructure
    - S3 cross-region replication

  Global:
    - Route 53 (DNS failover)
    - CloudFront (CDN)
    - DynamoDB Global Tables
```

**Implementation (Terraform):**
```hcl
# Multi-region deployment
provider "aws" {
  alias  = "primary"
  region = "us-east-1"
}

provider "aws" {
  alias  = "secondary"
  region = "us-west-2"
}

# Primary region resources
module "primary_region" {
  source = "./modules/region"
  providers = {
    aws = aws.primary
  }

  environment     = "production"
  region_type     = "primary"
  enable_rds      = true
  enable_cache    = true
  multi_az        = true
}

# Secondary region (DR)
module "secondary_region" {
  source = "./modules/region"
  providers = {
    aws = aws.secondary
  }

  environment     = "production"
  region_type     = "secondary"
  enable_rds      = false  # Read replica
  enable_cache    = true
  multi_az        = false
}

# Global services
resource "aws_route53_health_check" "primary" {
  fqdn              = module.primary_region.load_balancer_dns
  port              = 443
  type              = "HTTPS"
  resource_path     = "/health"
  failure_threshold = 3
  request_interval  = 30
}

resource "aws_route53_record" "failover_primary" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "api.example.com"
  type    = "A"

  failover_routing_policy {
    type = "PRIMARY"
  }

  set_identifier = "primary"
  health_check_id = aws_route53_health_check.primary.id

  alias {
    name                   = module.primary_region.load_balancer_dns
    zone_id                = module.primary_region.load_balancer_zone_id
    evaluate_target_health = true
  }
}
```

### Pattern 2: Serverless API Architecture

```yaml
# API Gateway + Lambda + DynamoDB
apiVersion: v1
kind: ServerlessAPI
spec:
  components:
    apiGateway:
      type: REST
      authentication: Cognito
      throttling:
        rateLimit: 10000
        burstLimit: 5000

    functions:
      - name: getUser
        runtime: nodejs18.x
        memory: 256
        timeout: 10
        triggers:
          - http:
              path: /users/{id}
              method: GET

      - name: createUser
        runtime: nodejs18.x
        memory: 512
        timeout: 30
        triggers:
          - http:
              path: /users
              method: POST

    database:
      type: DynamoDB
      tables:
        - name: Users
          partitionKey: userId
          sortKey: timestamp
          globalSecondaryIndexes:
            - name: EmailIndex
              partitionKey: email
```

**Implementation (AWS SAM):**
```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    Runtime: nodejs18.x
    Timeout: 30
    MemorySize: 256
    Environment:
      Variables:
        TABLE_NAME: !Ref UsersTable
        REGION: !Ref AWS::Region

Resources:
  ApiGateway:
    Type: AWS::Serverless::Api
    Properties:
      StageName: prod
      Auth:
        DefaultAuthorizer: CognitoAuthorizer
        Authorizers:
          CognitoAuthorizer:
            UserPoolArn: !GetAtt UserPool.Arn

      Cors:
        AllowMethods: "'GET,POST,PUT,DELETE'"
        AllowHeaders: "'Content-Type,Authorization'"
        AllowOrigin: "'*'"

      MethodSettings:
        - ResourcePath: '/*'
          HttpMethod: '*'
          ThrottlingRateLimit: 10000
          ThrottlingBurstLimit: 5000

  GetUserFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: functions/getUser/
      Handler: index.handler
      Events:
        GetUser:
          Type: Api
          Properties:
            RestApiId: !Ref ApiGateway
            Path: /users/{id}
            Method: GET
      Policies:
        - DynamoDBReadPolicy:
            TableName: !Ref UsersTable

  CreateUserFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: functions/createUser/
      Handler: index.handler
      MemorySize: 512
      Events:
        CreateUser:
          Type: Api
          Properties:
            RestApiId: !Ref ApiGateway
            Path: /users
            Method: POST
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref UsersTable

  UsersTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: Users
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: userId
          AttributeType: S
        - AttributeName: email
          AttributeType: S
      KeySchema:
        - AttributeName: userId
          KeyType: HASH
      GlobalSecondaryIndexes:
        - IndexName: EmailIndex
          KeySchema:
            - AttributeName: email
              KeyType: HASH
          Projection:
            ProjectionType: ALL

Outputs:
  ApiEndpoint:
    Description: API Gateway endpoint
    Value: !Sub 'https://${ApiGateway}.execute-api.${AWS::Region}.amazonaws.com/prod'
```

### Pattern 3: Cloud-Native Networking

```hcl
# AWS VPC with best practices
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "production-vpc"
  cidr = "10.0.0.0/16"

  # Multi-AZ deployment
  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
  database_subnets = ["10.0.201.0/24", "10.0.202.0/24", "10.0.203.0/24"]

  # NAT Gateways for private subnets
  enable_nat_gateway = true
  single_nat_gateway = false  # Multi-AZ NAT for HA
  one_nat_gateway_per_az = true

  # DNS
  enable_dns_hostnames = true
  enable_dns_support   = true

  # VPC Flow Logs for security
  enable_flow_log                      = true
  create_flow_log_cloudwatch_iam_role  = true
  create_flow_log_cloudwatch_log_group = true

  # Tags for cost allocation
  tags = {
    Environment = "production"
    ManagedBy   = "terraform"
    Team        = "platform"
  }
}

# VPC Peering for cross-VPC communication
resource "aws_vpc_peering_connection" "main" {
  vpc_id      = module.vpc.vpc_id
  peer_vpc_id = var.peer_vpc_id
  auto_accept = true

  tags = {
    Name = "production-to-shared-services"
  }
}

# Transit Gateway for hub-and-spoke
resource "aws_ec2_transit_gateway" "main" {
  description = "Central transit gateway"

  default_route_table_association = "enable"
  default_route_table_propagation = "enable"
  dns_support                     = "enable"
  vpn_ecmp_support               = "enable"

  tags = {
    Name = "production-tgw"
  }
}

# Private Link for AWS services
resource "aws_vpc_endpoint" "s3" {
  vpc_id       = module.vpc.vpc_id
  service_name = "com.amazonaws.${var.region}.s3"

  route_table_ids = module.vpc.private_route_table_ids

  tags = {
    Name = "s3-endpoint"
  }
}
```

## Resource Files

For detailed guidance on specific topics, see:

### Cloud Platforms
- **[aws-patterns.md](resources/aws-patterns.md)** - Comprehensive AWS services guide (EC2, S3, RDS, Lambda, EKS), Well-Architected Framework, service selection
- **[azure-patterns.md](resources/azure-patterns.md)** - Azure services guide (VMs, Blob Storage, AKS, Functions), Azure best practices
- **[gcp-patterns.md](resources/gcp-patterns.md)** - GCP services guide (Compute Engine, Cloud Storage, GKE, Cloud Functions), Google Cloud best practices
- **[oci-patterns.md](resources/oci-patterns.md)** - Oracle Cloud Infrastructure guide (Compute Instances, Object Storage, Autonomous Database, OKE), OCI best practices

### Cloud Strategies
- **[multi-cloud-strategies.md](resources/multi-cloud-strategies.md)** - Multi-cloud vs single cloud, abstraction layers, service selection, trade-offs
- **[cloud-cost-optimization.md](resources/cloud-cost-optimization.md)** - Reserved instances, spot instances, right-sizing, tagging, FinOps principles
- **[migration-strategies.md](resources/migration-strategies.md)** - 6 R's of migration, migration patterns, modernization, assessment tools

### Networking & Security
- **[cloud-networking.md](resources/cloud-networking.md)** - VPC design, peering, transit gateway, private link, DNS, CDN configuration
- **[cloud-security.md](resources/cloud-security.md)** - IAM best practices, encryption (KMS), compliance (HIPAA, PCI-DSS), security controls
- **[cleared-cloud-environments.md](resources/cleared-cloud-environments.md)** - Government cloud regions (AWS GovCloud, Azure Government, GCP Gov, OCI Gov), air-gapped deployments, FedRAMP, CMMC, classified environments
- **[cloud-security-tools.md](resources/cloud-security-tools.md)** - CSPM tools (Trend Micro Cloud One, Prisma Cloud, Wiz, Aqua), native cloud security (Security Hub, Defender, SCC), tool comparison

### Architecture Patterns
- **[well-architected-frameworks.md](resources/well-architected-frameworks.md)** - AWS/Azure/GCP Well-Architected pillars, design principles, review process
- **[serverless-patterns.md](resources/serverless-patterns.md)** - Lambda/Cloud Functions, API Gateway, event-driven architecture, FaaS best practices

## Best Practices

### Cloud Architecture

1. **Design for Failure:**
   - Assume everything fails
   - Use multiple availability zones
   - Implement health checks and auto-recovery
   - Test failure scenarios regularly

2. **Security First:**
   - Implement least privilege access
   - Enable encryption everywhere
   - Use managed identity services
   - Regular security audits and updates

3. **Cost Management:**
   - Tag all resources for cost allocation
   - Use auto-scaling to match demand
   - Leverage reserved capacity for predictable workloads
   - Regular cost reviews and optimization

### Service Selection

1. **Managed Services First:**
   - Prefer managed services over self-managed
   - Reduces operational overhead
   - Built-in high availability and backup
   - Auto-patching and updates

2. **Right-Size Resources:**
   - Start small, scale as needed
   - Monitor and adjust based on metrics
   - Use burstable instances for variable workloads
   - Consider serverless for intermittent loads

3. **Regional Selection:**
   - Deploy close to users (latency)
   - Consider data residency requirements
   - Check service availability by region
   - Plan for disaster recovery region

### Multi-Cloud Strategy

1. **Avoid Lock-In:**
   - Use containers and Kubernetes
   - Abstract cloud-specific services
   - Infrastructure as Code (portable)
   - Standard protocols and APIs

2. **Choose Best-of-Breed:**
   - AWS for breadth of services
   - Azure for Microsoft integration
   - GCP for data analytics and ML
   - OCI for Oracle Database and cost efficiency
   - Hybrid for on-premises integration

3. **Operational Complexity:**
   - Balance benefits vs complexity
   - Unified monitoring and logging
   - Centralized identity management
   - Consistent security policies

## Anti-Patterns to Avoid

❌ **Single region deployment** - No disaster recovery capability
❌ **No auto-scaling** - Manual scaling is error-prone and slow
❌ **Ignoring costs** - Leads to cloud bill shock
❌ **Over-provisioning** - Wastes money on unused resources
❌ **No tagging strategy** - Impossible to track costs and ownership
❌ **Tight cloud coupling** - Creates vendor lock-in
❌ **Manual deployments** - Error-prone and not repeatable
❌ **No monitoring** - Can't detect or resolve issues
❌ **Weak IAM policies** - Security vulnerabilities
❌ **No backup strategy** - Risk of data loss

## Common Tasks

### Task: Deploy Serverless Application

1. Design API endpoints and data model
2. Create Lambda functions with proper IAM roles
3. Set up API Gateway with authentication
4. Configure DynamoDB tables with indexes
5. Implement CloudWatch monitoring and alarms
6. Set up CI/CD pipeline for deployments
7. Test with load testing tools
8. Document API and operational runbooks

### Task: Implement Multi-Region Architecture

1. Choose primary and secondary regions
2. Design global networking (Route 53, CDN)
3. Set up VPC in each region
4. Implement database replication
5. Configure load balancers and auto-scaling
6. Set up health checks and failover
7. Test failover scenarios
8. Document disaster recovery procedures

### Task: Optimize Cloud Costs

1. Enable cost allocation tags
2. Analyze current spending patterns
3. Identify unused or underutilized resources
4. Right-size instances based on metrics
5. Purchase reserved capacity for steady workloads
6. Implement auto-scaling for variable loads
7. Use spot instances for fault-tolerant workloads
8. Set up cost budgets and alerts

## Integration Points

This skill integrates with:
- **platform-engineering**: Kubernetes on cloud (EKS, AKS, GKE), infrastructure automation
- **devsecops**: Cloud security scanning, IAM policies, compliance
- **sre**: Cloud monitoring, incident response, reliability engineering
- **release-engineering**: Cloud CI/CD services, artifact storage
- **systems-engineering**: Cloud networking, performance tuning, troubleshooting

## Triggers and Activation

This skill activates when you:
- Work with cloud service providers (AWS, Azure, GCP, OCI)
- Design cloud-native architectures
- Implement serverless applications
- Optimize cloud costs
- Plan cloud migrations
- Configure cloud networking or security
- Use cloud-specific IaC (CloudFormation, ARM templates, Terraform)

## Next Steps

For your specific task:
1. Identify which cloud provider best fits your needs
2. Review the relevant patterns and Well-Architected principles
3. Choose appropriate services and architecture
4. Implement with Infrastructure as Code
5. Test in development environment first
6. Monitor costs and performance continuously

---

**Total Resources:** 11 detailed guides covering all aspects of cloud engineering
**Pattern Library:** 125+ production-tested cloud patterns across AWS, Azure, GCP, and OCI
**Maintained by:** Cloud Engineering team based on real-world production experience
