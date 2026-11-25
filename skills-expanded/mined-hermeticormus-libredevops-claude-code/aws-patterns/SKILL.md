---
name: aws-patterns
description: "Production AWS patterns in CDK TypeScript, IAM JSON, and CloudFormation: three-tier VPC, ECS Fargate behind an ALB, CloudFront and S3 SPA hosting, Aurora PostgreSQL, IAM permission boundaries, AWS Config drift rules, multi-region CloudTrail, and tagging with CDK Aspects. Use when building or reviewing AWS infrastructure code."
---

# AWS Patterns

Production AWS architecture patterns with CDK TypeScript, IAM JSON, and CloudFormation YAML examples.

## VPC Three-Tier Pattern

```typescript
// lib/network-stack.ts
import * as cdk from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';

export class NetworkStack extends cdk.Stack {
  public readonly vpc: ec2.Vpc;

  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    this.vpc = new ec2.Vpc(this, 'Vpc', {
      ipAddresses: ec2.IpAddresses.cidr('10.0.0.0/16'),
      maxAzs: 3,
      natGateways: 1,  // Increase to 3 for prod HA; each costs ~$32/mo
      subnetConfiguration: [
        {
          cidrMask: 24,
          name: 'public',
          subnetType: ec2.SubnetType.PUBLIC,
        },
        {
          cidrMask: 24,
          name: 'app',
          subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
        },
        {
          cidrMask: 28,
          name: 'data',
          subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
        },
      ],
      // VPC Flow Logs to S3 for cost-effective storage
      flowLogs: {
        's3': {
          destination: ec2.FlowLogDestination.toS3(flowLogBucket),
          trafficType: ec2.FlowLogTrafficType.REJECT,  // Only rejected traffic
        },
      },
    });

    // VPC Endpoints to avoid NAT Gateway charges for AWS services
    this.vpc.addGatewayEndpoint('S3Endpoint', {
      service: ec2.GatewayVpcEndpointAwsService.S3,
    });
    this.vpc.addInterfaceEndpoint('EcrEndpoint', {
      service: ec2.InterfaceVpcEndpointAwsService.ECR,
    });
    this.vpc.addInterfaceEndpoint('SecretsManagerEndpoint', {
      service: ec2.InterfaceVpcEndpointAwsService.SECRETS_MANAGER,
    });
  }
}
```

## ECS Fargate Service with ALB

```typescript
// lib/compute-stack.ts
const cluster = new ecs.Cluster(this, 'Cluster', {
  vpc,
  containerInsights: true,  // CloudWatch Container Insights metrics
});

const service = new ecs_patterns.ApplicationLoadBalancedFargateService(this, 'Service', {
  cluster,
  taskDefinition: taskDef,
  desiredCount: 2,
  publicLoadBalancer: true,
  certificate: acm.Certificate.fromCertificateArn(this, 'Cert', certArn),
  redirectHTTP: true,  // 80 -> 443
  healthCheckGracePeriod: Duration.seconds(60),
});

// Auto Scaling based on CPU and request count
const scaling = service.service.autoScaleTaskCount({ minCapacity: 2, maxCapacity: 20 });
scaling.scaleOnCpuUtilization('CpuScaling', {
  targetUtilizationPercent: 70,
  scaleInCooldown: Duration.seconds(300),
  scaleOutCooldown: Duration.seconds(60),
});
scaling.scaleOnRequestCount('RequestScaling', {
  requestsPerTarget: 1000,
  targetGroup: service.targetGroup,
});
```

## CloudFront + S3 SPA Hosting

```typescript
const bucket = new s3.Bucket(this, 'WebBucket', {
  blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
  encryption: s3.BucketEncryption.S3_MANAGED,
  enforceSSL: true,
  removalPolicy: cdk.RemovalPolicy.RETAIN,
});

const oac = new cloudfront.CfnOriginAccessControl(this, 'OAC', {
  originAccessControlConfig: {
    name: 'S3OAC',
    originAccessControlOriginType: 's3',
    signingBehavior: 'always',
    signingProtocol: 'sigv4',
  },
});

const distribution = new cloudfront.Distribution(this, 'Distribution', {
  defaultRootObject: 'index.html',
  defaultBehavior: {
    origin: new origins.S3Origin(bucket),
    viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
    cachePolicy: cloudfront.CachePolicy.CACHING_OPTIMIZED,
  },
  additionalBehaviors: {
    '/api/*': {
      origin: new origins.LoadBalancerV2Origin(alb),
      cachePolicy: cloudfront.CachePolicy.CACHING_DISABLED,
      originRequestPolicy: cloudfront.OriginRequestPolicy.ALL_VIEWER,
    },
  },
  errorResponses: [
    { httpStatus: 403, responseHttpStatus: 200, responsePagePath: '/index.html' },
    { httpStatus: 404, responseHttpStatus: 200, responsePagePath: '/index.html' },
  ],
  geoRestriction: cloudfront.GeoRestriction.allowlist('US', 'CA', 'GB'),
  webAclId: wafAclArn,  // WAF for rate limiting and managed rules
});
```

## RDS Aurora PostgreSQL

```typescript
const dbCluster = new rds.DatabaseCluster(this, 'Database', {
  engine: rds.DatabaseClusterEngine.auroraPostgres({
    version: rds.AuroraPostgresEngineVersion.VER_15_4,
  }),
  credentials: rds.Credentials.fromGeneratedSecret('postgres', {
    secretName: '/myapp/prod/db-credentials',
  }),
  writer: rds.ClusterInstance.serverlessV2('writer', {
    scaleWithWriter: true,
  }),
  readers: [
    rds.ClusterInstance.serverlessV2('reader1', { scaleWithWriter: true }),
  ],
  serverlessV2MinCapacity: 0.5,   // 0.5 ACU minimum (saves cost at idle)
  serverlessV2MaxCapacity: 64,    // 64 ACU maximum
  vpc,
  vpcSubnets: { subnetType: ec2.SubnetType.PRIVATE_ISOLATED },
  securityGroups: [dbSecurityGroup],
  backup: { retention: Duration.days(14), preferredWindow: '03:00-04:00' },
  parameterGroup: new rds.ParameterGroup(this, 'DbParams', {
    engine: rds.DatabaseClusterEngine.auroraPostgres({ version: ... }),
    parameters: {
      'rds.force_ssl': '1',
      'log_min_duration_statement': '1000',
      'shared_preload_libraries': 'pg_stat_statements',
    },
  }),
  storageEncrypted: true,
  deletionProtection: true,
});
```

## IAM Role with Permission Boundary

```typescript
// Permission boundary limits max permissions a developer role can grant
const permissionBoundary = new iam.ManagedPolicy(this, 'DevBoundary', {
  statements: [
    new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      actions: ['s3:*', 'lambda:*', 'dynamodb:*', 'logs:*'],
      resources: ['*'],
      conditions: {
        StringEquals: { 'aws:RequestedRegion': ['us-east-1', 'us-west-2'] },
      },
    }),
    new iam.PolicyStatement({
      effect: iam.Effect.DENY,
      actions: ['iam:CreateUser', 'iam:DeleteUser', 'organizations:*'],
      resources: ['*'],
    }),
  ],
});

const developerRole = new iam.Role(this, 'DeveloperRole', {
  assumedBy: new iam.FederatedPrincipal('arn:aws:iam::ACCOUNT:saml-provider/IdP', {}, 'sts:AssumeRoleWithSAML'),
  permissionsBoundary: permissionBoundary,
  maxSessionDuration: Duration.hours(8),
});
```

## AWS Config Rules for Drift Detection

```typescript
// Enforce encryption on all EBS volumes
new config.ManagedRule(this, 'EbsEncrypted', {
  identifier: config.ManagedRuleIdentifiers.EC2_EBS_ENCRYPTION_BY_DEFAULT,
  configRuleName: 'ebs-encryption-by-default',
});

// Ensure S3 buckets block public access
new config.ManagedRule(this, 'S3PublicAccess', {
  identifier: config.ManagedRuleIdentifiers.S3_BUCKET_LEVEL_PUBLIC_ACCESS_PROHIBITED,
});

// Remediation: auto-remediate non-compliant resources
const remediation = new config.CfnRemediationConfiguration(this, 'EbsRemediation', {
  configRuleName: 'ebs-encryption-by-default',
  targetType: 'SSM_DOCUMENT',
  targetId: 'AWSConfigRemediation-EnableEbsEncryptionByDefault',
  automatic: true,
  maximumAutomaticAttempts: 3,
  retryAttemptSeconds: 60,
});
```

## CloudTrail Multi-Region Setup

```typescript
const trail = new cloudtrail.Trail(this, 'OrgTrail', {
  isMultiRegionTrail: true,
  includeGlobalServiceEvents: true,
  enableFileValidation: true,  // Log file integrity validation
  bucket: trailBucket,
  encryptionKey: trailKey,
  sendToCloudWatchLogs: true,
  cloudWatchLogsRetention: logs.RetentionDays.ONE_YEAR,
  // Insight events detect unusual API activity
  insightTypes: [cloudtrail.InsightType.API_CALL_RATE, cloudtrail.InsightType.API_ERROR_RATE],
});

// Data events for S3 (important buckets only, not all)
trail.addS3EventSelector([{ bucket: sensitiveDataBucket }], {
  includeManagementEvents: false,
  readWriteType: cloudtrail.ReadWriteType.ALL,
});
```

## Tagging Strategy (CDK Aspects)

```typescript
// Apply mandatory tags to all resources in a stack
class RequiredTagsAspect implements cdk.IAspect {
  constructor(private readonly tags: Record<string, string>) {}

  public visit(node: IConstruct): void {
    if (node instanceof cdk.CfnResource) {
      Object.entries(this.tags).forEach(([key, value]) => {
        cdk.Tags.of(node).add(key, value);
      });
    }
  }
}

// Apply in stack
cdk.Aspects.of(app).add(new RequiredTagsAspect({
  'Environment': 'production',
  'Team':        'platform',
  'CostCenter':  'engineering',
  'ManagedBy':   'cdk',
}));
```
