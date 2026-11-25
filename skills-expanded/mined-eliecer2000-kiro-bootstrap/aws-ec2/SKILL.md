---
name: aws-ec2
description: Amazon EC2 instance configuration. Use when setting up AMIs, instance types, security groups, IAM roles, Auto Scaling Groups, EBS volumes or Packer golden images.
---

# AWS EC2

Skill para configurar instancias EC2: AMIs, instance types, security groups, IAM roles, user data, Auto Scaling Groups, EBS volumes, Packer para golden images y mejores prácticas de seguridad y costos.

## Principios fundamentales

- Serverless-first: usar EC2 solo cuando Lambda/Fargate no cubren el caso de uso (procesos largos, GPU, software con licencia, cargas constantes).
- IAM roles en lugar de access keys. Nunca hardcodear credenciales en user data.
- Security groups con least privilege: solo puertos necesarios desde fuentes específicas.
- SSH restringido a IPs conocidas o usar SSM Session Manager (sin puerto 22 abierto).
- AMIs versionadas con Packer para deployments reproducibles.

## Security group seguro (CDK)

```typescript
const sg = new ec2.SecurityGroup(this, 'WebSG', {
  vpc,
  description: 'Web server security group',
  allowAllOutbound: true,
});

// Solo HTTPS desde internet
sg.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(443), 'HTTPS');

// SSH solo desde bastion o SSM (preferir SSM)
// sg.addIngressRule(ec2.Peer.ipv4('10.0.0.0/8'), ec2.Port.tcp(22), 'SSH from VPC');
```

## Instancia EC2 con SSM (CDK)

```typescript
const instance = new ec2.Instance(this, 'WebServer', {
  vpc,
  vpcSubnets: { subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS },
  instanceType: ec2.InstanceType.of(ec2.InstanceClass.T4G, ec2.InstanceSize.MICRO),
  machineImage: ec2.MachineImage.latestAmazonLinux2023({
    cpuType: ec2.AmazonLinuxCpuType.ARM_64,
  }),
  ssmSessionPermissions: true, // SSM Session Manager en lugar de SSH
  blockDevices: [{
    deviceName: '/dev/xvda',
    volume: ec2.BlockDeviceVolume.ebs(20, {
      encrypted: true,
      volumeType: ec2.EbsDeviceVolumeType.GP3,
    }),
  }],
});
```

## Auto Scaling Group (CDK)

```typescript
const asg = new autoscaling.AutoScalingGroup(this, 'ASG', {
  vpc,
  instanceType: ec2.InstanceType.of(ec2.InstanceClass.T4G, ec2.InstanceSize.SMALL),
  machineImage: ec2.MachineImage.latestAmazonLinux2023(),
  minCapacity: 2,
  maxCapacity: 10,
  healthCheck: autoscaling.HealthCheck.elb({ grace: cdk.Duration.minutes(5) }),
});

asg.scaleOnCpuUtilization('CpuScaling', {
  targetUtilizationPercent: 70,
  cooldown: cdk.Duration.minutes(5),
});
```

## Golden images con Packer

```hcl
packer {
  required_plugins {
    amazon = {
      source  = "github.com/hashicorp/amazon"
      version = "~> 1.3"
    }
  }
}

locals {
  timestamp = regex_replace(timestamp(), "[- TZ:]", "")
}

source "amazon-ebs" "app" {
  region        = var.region
  instance_type = "t3.micro"

  source_ami_filter {
    filters = {
      name                = "al2023-ami-*-x86_64"
      root-device-type    = "ebs"
      virtualization-type = "hvm"
    }
    most_recent = true
    owners      = ["amazon"]
  }

  ssh_username = "ec2-user"
  ami_name     = "my-app-${local.timestamp}"

  tags = {
    Name      = "my-app"
    BuildDate = local.timestamp
    ManagedBy = "Packer"
  }
}

build {
  sources = ["source.amazon-ebs.app"]

  provisioner "shell" {
    inline = [
      "sudo dnf update -y",
      "sudo dnf install -y nodejs20 nginx",
    ]
  }
}
```

### Comandos Packer
```bash
packer init .
packer validate .
packer build .
packer build -var "region=us-east-1" .
```

## Cuándo usar EC2 vs Lambda vs Fargate

| Criterio | Lambda | Fargate | EC2 |
|---|---|---|---|
| Duración | < 15 min | Ilimitada | Ilimitada |
| RAM máxima | 10 GB | 120 GB | Ilimitada |
| GPU | No | No | Sí |
| Cold start | Sí | Sí (menor) | No |
| Costo variable | Pay-per-invocation | Pay-per-vCPU/hora | Pay-per-hora |
| Caso ideal | Event-driven, APIs | Containers, microservices | Cargas constantes, GPU, licencias |

## Anti-patrones a evitar

- ❌ SSH abierto a `0.0.0.0/0`.
- ❌ Access keys hardcodeadas en user data.
- ❌ Instancias sin IAM role (usando access keys en su lugar).
- ❌ EBS volumes sin cifrado.
- ❌ AMIs desactualizadas sin parches de seguridad.
- ❌ Over-provisioning sin medir uso real.
- ❌ Instancias on-demand para cargas estables (usar Savings Plans).
- ❌ No usar Auto Scaling para cargas variables.
- ❌ Termination protection deshabilitada en producción.
- ❌ Usar EC2 cuando Lambda o Fargate cubren el caso de uso.

## Checklist de revisión EC2

- [ ] Security groups con least privilege (no `0.0.0.0/0` en SSH).
- [ ] IAM role asignado (no access keys).
- [ ] SSM Session Manager habilitado (preferir sobre SSH).
- [ ] EBS volumes cifrados.
- [ ] AMI versionada con Packer o similar.
- [ ] Auto Scaling configurado para cargas variables.
- [ ] CloudWatch monitoring habilitado.
- [ ] Termination protection en producción.
- [ ] Savings Plans evaluados para cargas estables.
- [ ] Subnet privada con NAT Gateway (no pública salvo ALB).
