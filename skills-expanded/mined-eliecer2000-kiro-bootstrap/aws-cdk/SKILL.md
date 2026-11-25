---
name: aws-cdk
description: AWS CDK infrastructure development in TypeScript. Use when creating stacks, constructs, L2/L3 patterns, CDK testing, synth/deploy pipelines or organizing IaC code.
---

# AWS CDK

Skill para desarrollo de infraestructura con AWS CDK en TypeScript: stacks, constructs, patrones L2/L3, testing, synth, deploy, pipelines CI/CD y mejores prácticas de organización de código IaC.

## Principios fundamentales

- CDK es código, trátalo como tal: tests, code review, linting, CI/CD.
- Preferir constructs L2 (aws-xxx) sobre L1 (CfnXxx). L1 solo cuando L2 no expone la propiedad necesaria.
- Un stack = una unidad de deployment. No meter toda la infra en un solo stack.
- Nombres lógicos estables: evitar cambios que fuercen replacement de recursos stateful.
- Nunca hardcodear account IDs, regiones o ARNs. Usar `Aws.ACCOUNT_ID`, `Aws.REGION`, SSM lookups o context.

## Estructura de proyecto recomendada

```
infra/
├── bin/
│   └── app.ts              # Entry point, instancia stacks
├── lib/
│   ├── stacks/
│   │   ├── api-stack.ts     # Stack de API Gateway + Lambda
│   │   ├── data-stack.ts    # Stack de DynamoDB, S3
│   │   └── auth-stack.ts    # Stack de Cognito
│   ├── constructs/
│   │   ├── api-lambda.ts    # Construct reutilizable
│   │   └── monitored-table.ts
│   └── config/
│       └── environments.ts  # Configuración por ambiente
├── test/
│   ├── stacks/
│   │   └── api-stack.test.ts
│   └── constructs/
│       └── api-lambda.test.ts
├── cdk.json
├── tsconfig.json
└── package.json
```

## Configuración por ambiente

```typescript
interface EnvironmentConfig {
  readonly account: string;
  readonly region: string;
  readonly stageName: string;
  readonly domainName?: string;
  readonly logRetentionDays: number;
  readonly removalPolicy: cdk.RemovalPolicy;
}

const environments: Record<string, EnvironmentConfig> = {
  dev: {
    account: process.env.CDK_DEFAULT_ACCOUNT!,
    region: 'us-east-1',
    stageName: 'dev',
    logRetentionDays: 7,
    removalPolicy: cdk.RemovalPolicy.DESTROY,
  },
  prod: {
    account: '123456789012',
    region: 'us-east-1',
    stageName: 'prod',
    logRetentionDays: 365,
    removalPolicy: cdk.RemovalPolicy.RETAIN,
  },
};
```

## Patrones de constructs

### Construct L3 reutilizable (ejemplo)

```typescript
export interface MonitoredLambdaProps {
  readonly entry: string;
  readonly handler?: string;
  readonly runtime?: lambda.Runtime;
  readonly memorySize?: number;
  readonly timeout?: cdk.Duration;
  readonly environment?: Record<string, string>;
  readonly alarmThreshold?: number;
}

export class MonitoredLambda extends Construct {
  public readonly function: lambda.Function;
  public readonly errorAlarm: cloudwatch.Alarm;

  constructor(scope: Construct, id: string, props: MonitoredLambdaProps) {
    super(scope, id);

    this.function = new nodejs.NodejsFunction(this, 'Handler', {
      entry: props.entry,
      handler: props.handler ?? 'handler',
      runtime: props.runtime ?? lambda.Runtime.NODEJS_20_X,
      memorySize: props.memorySize ?? 256,
      timeout: props.timeout ?? cdk.Duration.seconds(30),
      environment: props.environment,
      tracing: lambda.Tracing.ACTIVE,
      insightsVersion: lambda.LambdaInsightsVersion.VERSION_1_0_229_0,
    });

    this.errorAlarm = new cloudwatch.Alarm(this, 'ErrorAlarm', {
      metric: this.function.metricErrors({ period: cdk.Duration.minutes(5) }),
      threshold: props.alarmThreshold ?? 5,
      evaluationPeriods: 2,
      treatMissingData: cloudwatch.TreatMissingData.NOT_BREACHING,
    });
  }
}
```

## Testing de CDK

### Snapshot tests
```typescript
test('stack matches snapshot', () => {
  const app = new cdk.App();
  const stack = new ApiStack(app, 'TestStack', { /* props */ });
  const template = Template.fromStack(stack);
  expect(template.toJSON()).toMatchSnapshot();
});
```

### Fine-grained assertions
```typescript
test('creates DynamoDB table with correct config', () => {
  const template = Template.fromStack(stack);

  template.hasResourceProperties('AWS::DynamoDB::Table', {
    BillingMode: 'PAY_PER_REQUEST',
    SSESpecification: { SSEEnabled: true },
    PointInTimeRecoverySpecification: { PointInTimeRecoveryEnabled: true },
  });
});

test('Lambda has correct environment variables', () => {
  const template = Template.fromStack(stack);

  template.hasResourceProperties('AWS::Lambda::Function', {
    Environment: {
      Variables: Match.objectLike({
        TABLE_NAME: Match.anyValue(),
        LOG_LEVEL: 'INFO',
      }),
    },
  });
});
```

### Validation tests
```typescript
test('stack does not create public S3 buckets', () => {
  const template = Template.fromStack(stack);

  template.allResourcesProperties('AWS::S3::Bucket', {
    PublicAccessBlockConfiguration: {
      BlockPublicAcls: true,
      BlockPublicPolicy: true,
      IgnorePublicAcls: true,
      RestrictPublicBuckets: true,
    },
  });
});
```

## Comandos esenciales

```bash
# Sintetizar CloudFormation
npx cdk synth

# Diff contra lo desplegado
npx cdk diff

# Deploy de un stack específico
npx cdk deploy ApiStack --require-approval broadening

# Deploy de todos los stacks
npx cdk deploy --all

# Destruir stack (solo dev)
npx cdk destroy ApiStack

# Listar stacks
npx cdk list

# Bootstrap de cuenta/región (una vez)
npx cdk bootstrap aws://ACCOUNT/REGION
```

## Mejores prácticas

### Naming de recursos

CRÍTICO: NO especificar nombres explícitos de recursos cuando son opcionales en CDK constructs.

```typescript
// ❌ MAL - Naming explícito impide reusabilidad y deploys paralelos
new lambda.Function(this, 'MyFunction', {
  functionName: 'my-lambda',  // Evitar esto
});

// ✅ BIEN - CDK genera nombres únicos automáticamente
new lambda.Function(this, 'MyFunction', {
  // Sin functionName - CDK genera: StackName-MyFunctionXXXXXX
});
```

CDK-generated names permiten:
- Patrones reutilizables: deploy del mismo construct múltiples veces sin conflictos.
- Deploys paralelos: múltiples stacks en la misma región simultáneamente.
- Lógica compartida: patterns y código compartido sin colisión de nombres.
- Aislamiento de stacks: cada stack obtiene recursos identificados automáticamente.

Para diferentes ambientes (dev, staging, prod), usar cuentas AWS separadas en lugar de naming dentro de una sola cuenta (AWS Security Pillar best practice).

### Validación pre-deployment con cdk-nag

#### Capa 1: Feedback en tiempo real (IDE)

Instalar [cdk-nag](https://github.com/cdklabs/cdk-nag) para validación en synthesis-time:

```bash
npm install --save-dev cdk-nag
```

Agregar al CDK app:

```typescript
import { Aspects } from 'aws-cdk-lib';
import { AwsSolutionsChecks } from 'cdk-nag';

const app = new App();
Aspects.of(app).add(new AwsSolutionsChecks());
```

#### Capa 2: Validación en synthesis (obligatoria)

```bash
# cdk-nag se ejecuta automáticamente via Aspects
cdk synth
```

Suprimir excepciones legítimas con razón documentada:

```typescript
import { NagSuppressions } from 'cdk-nag';

NagSuppressions.addResourceSuppressions(resource, [{
  id: 'AwsSolutions-L1',
  reason: 'Lambda@Edge requiere runtime específico para compatibilidad con CloudFront'
}]);
```

#### Capa 3: Safety net pre-commit

```bash
npm run build     # Compilación exitosa
npm test          # Tests unitarios + integración
cdk synth         # Synthesis con cdk-nag
cdk diff          # Diff contra lo desplegado
```

### Organización de stacks
- Separar por dominio: `ApiStack`, `DataStack`, `AuthStack`, `MonitoringStack`.
- Usar cross-stack references con `CfnOutput` + `Fn.importValue` o pasar props entre stacks.
- Stacks stateful (DynamoDB, S3, Cognito) separados de stacks stateless (Lambda, API Gateway).

### Lambda Functions en CDK

Usar el construct apropiado según runtime:

TypeScript/JavaScript: `NodejsFunction` (bundling automático con esbuild)
```typescript
import { NodejsFunction } from 'aws-cdk-lib/aws-lambda-nodejs';

new NodejsFunction(this, 'MyFunction', {
  entry: 'lambda/handler.ts',
  handler: 'handler',
  // Bundling, dependencias y transpilación automáticos
});
```

Python: `PythonFunction` (empaquetado automático)
```typescript
import { PythonFunction } from '@aws-cdk/aws-lambda-python-alpha';

new PythonFunction(this, 'MyFunction', {
  entry: 'lambda',
  index: 'handler.py',
  handler: 'handler',
  // Dependencias y packaging automáticos
});
```

### Seguridad
- `RemovalPolicy.RETAIN` en recursos stateful en producción.
- `PointInTimeRecovery: true` en DynamoDB.
- `SSE: true` (cifrado) en DynamoDB, S3, SQS, SNS.
- `BlockPublicAccess.BLOCK_ALL` en S3.
- `autoDeleteObjects: true` solo en dev.

### Performance
- Usar `NodejsFunction` con esbuild para bundling automático de Lambda TS/JS.
- `PythonFunction` de `@aws-cdk/aws-lambda-python-alpha` para Lambda Python.
- Excluir `aws-sdk` del bundle (ya está en el runtime de Lambda).

### CI/CD con CDK Pipelines
```typescript
const pipeline = new pipelines.CodePipeline(this, 'Pipeline', {
  synth: new pipelines.ShellStep('Synth', {
    input: pipelines.CodePipelineSource.gitHub('org/repo', 'main'),
    commands: ['npm ci', 'npx cdk synth'],
  }),
});

pipeline.addStage(new MyAppStage(this, 'Dev', { env: devEnv }));
pipeline.addStage(new MyAppStage(this, 'Prod', { env: prodEnv }), {
  pre: [new pipelines.ManualApprovalStep('PromoteToProd')],
});
```

## Aspectos y tags

```typescript
// Aplicar tags a todos los recursos
cdk.Tags.of(app).add('Project', 'MiProyecto');
cdk.Tags.of(app).add('Environment', stageName);
cdk.Tags.of(app).add('ManagedBy', 'CDK');

// Aspect para validar que todos los buckets tienen cifrado
class BucketEncryptionChecker implements cdk.IAspect {
  visit(node: IConstruct) {
    if (node instanceof s3.Bucket) {
      if (!node.encryptionKey) {
        Annotations.of(node).addWarning('Bucket sin cifrado KMS explícito');
      }
    }
  }
}
```

## Anti-patrones a evitar

- ❌ Un solo stack gigante con toda la infraestructura.
- ❌ Usar `CfnResource` (L1) cuando existe un construct L2.
- ❌ Hardcodear account IDs, ARNs o nombres de recursos.
- ❌ `RemovalPolicy.DESTROY` en recursos stateful en producción.
- ❌ No tener tests de infraestructura.
- ❌ Ignorar `cdk diff` antes de deploy.
- ❌ Usar `cdk deploy` sin `--require-approval` en CI/CD.
- ❌ Constructs con side effects en el constructor (llamadas a APIs, I/O).
- ❌ Circular dependencies entre stacks.
- ❌ No usar `cdk.context.json` para cachear lookups.

## Checklist de revisión CDK

- [ ] Stacks separados por dominio y stateful/stateless.
- [ ] Constructs reutilizables para patrones repetidos.
- [ ] Tests: snapshot + fine-grained assertions + validaciones de seguridad.
- [ ] Configuración por ambiente externalizada.
- [ ] Tags aplicados a todos los recursos.
- [ ] RemovalPolicy correcto según ambiente.
- [ ] Cifrado habilitado en todos los recursos que lo soporten.
- [ ] `cdk diff` ejecutado antes de cada deploy.
- [ ] Pipeline CI/CD con approval manual para producción.
- [ ] Sin hardcoded values (accounts, regions, ARNs).
