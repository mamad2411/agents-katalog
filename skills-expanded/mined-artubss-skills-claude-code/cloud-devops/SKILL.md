---
name: cloud-devops
description: "Fluxo de trabalho de infraestrutura em nuvem e DevOps abrangendo AWS, Azure, GCP, Kubernetes, Terraform, CI/CD, monitoramento e desenvolvimento nativo em nuvem."
category: workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# Pacote de Fluxo de Trabalho Cloud/DevOps

## Visão Geral

Fluxo de trabalho abrangente de nuvem e DevOps para provisionamento de infraestrutura, orquestração de containers, pipelines CI/CD, monitoramento e desenvolvimento de aplicações nativas em nuvem.

## Quando Usar Este Fluxo de Trabalho

Use este fluxo de trabalho quando:
- Configurar infraestrutura em nuvem
- Implementar pipelines CI/CD
- Fazer deploy de aplicações Kubernetes
- Configurar monitoramento e observabilidade
- Gerenciar custos em nuvem
- Implementar práticas DevOps

## Fases do Fluxo de Trabalho

### Fase 1: Configuração de Infraestrutura em Nuvem

#### Skills a Invocar
- `cloud-architect` - Arquitetura de nuvem
- `aws-skills` - Desenvolvimento AWS
- `azure-functions` - Desenvolvimento Azure
- `gcp-cloud-run` - Desenvolvimento GCP
- `terraform-skill` - IaC com Terraform
- `terraform-specialist` - Terraform avançado

#### Ações
1. Projetar arquitetura em nuvem
2. Configurar contas e faturamento
3. Configurar rede
4. Provisionar recursos
5. Configurar IAM

#### Prompts para Copiar e Colar
```
Use @cloud-architect to design multi-cloud architecture
```

```
Use @terraform-skill to provision AWS infrastructure
```

### Fase 2: Orquestração de Containers

#### Skills a Invocar
- `kubernetes-architect` - Arquitetura Kubernetes
- `docker-expert` - Containerização Docker
- `helm-chart-scaffolding` - Gráficos Helm
- `k8s-manifest-generator` - Manifestos K8s
- `k8s-security-policies` - Segurança K8s

#### Ações
1. Projetar arquitetura de containers
2. Criar Dockerfiles
3. Compilar imagens de container
4. Escrever manifestos K8s
5. Fazer deploy para cluster
6. Configurar rede

#### Prompts para Copiar e Colar
```
Use @kubernetes-architect to design K8s architecture
```

```
Use @docker-expert to containerize application
```

```
Use @helm-chart-scaffolding to create Helm chart
```

### Fase 3: Implementação de CI/CD

#### Skills a Invocar
- `deployment-engineer` - Engenharia de deploy
- `cicd-automation-workflow-automate` - Automação CI/CD
- `github-actions-templates` - GitHub Actions
- `gitlab-ci-patterns` - GitLab CI
- `deployment-pipeline-design` - Design de pipeline

#### Ações
1. Projetar pipeline de deployment
2. Configurar automação de compilação
3. Configurar automação de testes
4. Configurar estágios de deployment
5. Implementar estratégias de rollback
6. Configurar notificações

#### Prompts para Copiar e Colar
```
Use @cicd-automation-workflow-automate to set up CI/CD pipeline
```

```
Use @github-actions-templates to create GitHub Actions workflow
```

### Fase 4: Monitoramento e Observabilidade

#### Skills a Invocar
- `observability-engineer` - Engenharia de observabilidade
- `grafana-dashboards` - Dashboards Grafana
- `prometheus-configuration` - Configuração Prometheus
- `datadog-automation` - Integração Datadog
- `sentry-automation` - Rastreamento de erros Sentry

#### Ações
1. Projetar estratégia de monitoramento
2. Configurar coleta de métricas
3. Configurar agregação de logs
4. Implementar rastreamento distribuído
5. Criar dashboards
6. Configurar alertas

#### Prompts para Copiar e Colar
```
Use @observability-engineer to set up observability stack
```

```
Use @grafana-dashboards to create monitoring dashboards
```

### Fase 5: Segurança em Nuvem

#### Skills a Invocar
- `cloud-penetration-testing` - Pentesting em nuvem
- `aws-penetration-testing` - Segurança AWS
- `k8s-security-policies` - Segurança K8s
- `secrets-management` - Gerenciamento de secrets
- `mtls-configuration` - Configuração mTLS

#### Ações
1. Avaliar segurança em nuvem
2. Configurar grupos de segurança
3. Configurar gerenciamento de secrets
4. Implementar políticas de rede
5. Configurar criptografia
6. Configurar log de auditoria

#### Prompts para Copiar e Colar
```
Use @cloud-penetration-testing to assess cloud security
```

```
Use @secrets-management to configure secrets
```

### Fase 6: Otimização de Custos

#### Skills a Invocar
- `cost-optimization` - Otimização de custos em nuvem
- `database-cloud-optimization-cost-optimize` - Otimização de custos de banco de dados

#### Ações
1. Analisar gastos em nuvem
2. Identificar oportunidades de otimização
3. Dimensionar corretamente recursos
4. Implementar auto-scaling
5. Usar instâncias reservadas
6. Configurar alertas de custos

#### Prompts para Copiar e Colar
```
Use @cost-optimization to reduce cloud costs
```

### Fase 7: Recuperação de Desastres

#### Skills a Invocar
- `incident-responder` - Resposta a incidentes
- `incident-runbook-templates` - Criação de runbooks
- `postmortem-writing` - Documentação de postmortem

#### Ações
1. Projetar estratégia de DR
2. Configurar backups
3. Criar runbooks
4. Testar failover
5. Documentar procedimentos
6. Treinar equipe

#### Prompts para Copiar e Colar
```
Use @incident-runbook-templates to create runbooks
```

## Fluxos de Trabalho por Provedor de Nuvem

### AWS
```
Skills: aws-skills, aws-serverless, aws-penetration-testing
Services: EC2, Lambda, S3, RDS, ECS, EKS
```

### Azure
```
Skills: azure-functions, azure-ai-projects-py, azure-monitor-opentelemetry-py
Services: Functions, App Service, AKS, Cosmos DB
```

### GCP
```
Skills: gcp-cloud-run
Services: Cloud Run, GKE, Cloud Functions, BigQuery
```

## Portas de Qualidade

- [ ] Infraestrutura provisionada
- [ ] Pipeline CI/CD funcionando
- [ ] Monitoramento configurado
- [ ] Medidas de segurança em lugar
- [ ] Otimização de custos aplicada
- [ ] Procedimentos de DR documentados

## Pacotes de Fluxo de Trabalho Relacionados

- `development` - Desenvolvimento de aplicações
- `security-audit` - Testes de segurança
- `database` - Operações de banco de dados
- `testing-qa` - Fluxos de trabalho de testes