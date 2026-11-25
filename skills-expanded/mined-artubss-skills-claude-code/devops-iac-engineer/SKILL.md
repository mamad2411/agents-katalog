---
name: devops-iac-engineer
description: Implementa infraestrutura como código usando Terraform, Kubernetes e plataformas de nuvem. Projeta arquiteturas escaláveis, pipelines de CI/CD e soluções de observabilidade. Fornece práticas DevOps com segurança em primeiro lugar e orientação em engenharia de confiabilidade de sites.
---

# DevOps IaC Engineer

Este Skill ajuda equipes DevOps a projetar, implementar e manter infraestrutura de nuvem usando princípios de Infrastructure as Code. Use quando estiver construindo arquiteturas em nuvem, implantando aplicações containerizadas, configurando pipelines de CI/CD ou implementando práticas de observabilidade e segurança.

## Navegação Rápida

- **Terraform & IaC**: Veja [terraform.md](reference/terraform.md) para boas práticas e padrões de Terraform
- **Kubernetes & Containers**: Veja [kubernetes.md](reference/kubernetes.md) para orquestração de containers
- **Plataformas de Nuvem**: Veja [cloud_platforms.md](reference/cloud_platforms.md) para orientação em AWS, Azure, GCP
- **Pipelines de CI/CD**: Veja [cicd.md](reference/cicd.md) para design de pipelines e GitOps
- **Observabilidade**: Veja [observability.md](reference/observability.md) para monitoramento e logging
- **Segurança**: Veja [security.md](reference/security.md) para práticas DevSecOps
- **Templates & Ferramentas**: Veja [templates.md](reference/templates.md) para templates prontos para uso

## Princípios Fundamentais

### Terminologia-Chave em DevOps (Consistente em Todo o Documento)
- **Infrastructure as Code (IaC)**: Gerenciamento de infraestrutura através de arquivos de código declarativo
- **GitOps**: Uso do Git como fonte única da verdade para infraestrutura e aplicações
- **Immutable Infrastructure**: Componentes de infraestrutura que são substituídos em vez de modificados
- **Service Mesh**: Camada de infraestrutura para comunicação entre serviços
- **Observability**: Capacidade de entender o estado do sistema a partir de saídas externas (logs, métricas, traces)
- **SLI/SLO/SLA**: Service Level Indicators/Objectives/Agreements para confiabilidade
- **RTO/RPO**: Recovery Time Objective/Recovery Point Objective para recuperação de desastres

### Fluxo de Trabalho: Implementação de Infraestrutura

Ao implementar infraestrutura, siga esta abordagem estruturada:

1. **Entender os Requisitos**
   - Qual é a necessidade de negócio? (nova aplicação, migração, escalabilidade, conformidade)
   - Quais são os requisitos de escala? (tráfego, dados, distribuição geográfica)
   - Quais são as restrições? (orçamento, cronograma, regulamentação)
   - Quais são as dependências? (sistemas existentes, fontes de dados)

2. **Projetar Arquitetura**
   - Escolha plataforma(s) de nuvem apropriada(s) e serviços
   - Projete para alta disponibilidade e tolerância a falhas
   - Planeje topologia de rede e limites de segurança
   - Identifique fluxos de dados e requisitos de armazenamento
   - Documente a arquitetura com diagramas

3. **Selecionar Ferramentas de IaC**
   - Terraform para provisionamento de infraestrutura multi-cloud
   - Manifests Kubernetes/Helm para orquestração de containers
   - Seleção de ferramentas de CI/CD com base na equipe e requisitos
   - Ferramentas de gerenciamento de configuração, se necessário

4. **Implementar Infraestrutura**
   - Crie código IaC modular e reutilizável
   - Siga boas práticas de segurança (veja [security.md](reference/security.md))
   - Implemente gerenciamento de estado e versionamento apropriados
   - Use convenções de nomenclatura e tagging consistentes
   - Documente o código e crie arquivos README

5. **Configurar Observabilidade**
   - Defina SLIs e SLOs para serviços críticos
   - Implemente logging, métricas e tracing
   - Crie dashboards e alertas
   - Configure agregação e análise de logs
   - Planeje rotação de on-call e runbooks

6. **Implementar CI/CD**
   - Projete estágios de pipeline de implantação
   - Implemente testes automatizados (unitários, integração, e2e)
   - Configure fluxos de trabalho GitOps
   - Configure estratégias de implantação (blue/green, canary)
   - Implemente procedimentos de rollback

7. **Testar & Validar**
   - Execute testes de infraestrutura (segurança, conformidade, custo)
   - Execute simulações de recuperação de desastres
   - Teste de carga e validação de desempenho
   - Scanning de segurança e teste de penetração
   - Documente resultados de testes e melhorias

8. **Implantar & Monitorar**
   - Execute rollout em fases
   - Monitore métricas e logs de perto
   - Valide contra SLOs
   - Documente runbooks e guias de troubleshooting
   - Conduza revisão pós-implantação

### Framework de Decisão: Seleção de Ferramentas

**Requisitos Multi-Cloud** → Terraform ou Pulumi
**Apenas AWS** → Terraform, AWS CDK ou CloudFormation
**Orquestração de Containers** → Kubernetes (EKS, GKE, AKS)
**Implantação Simples de Containers** → ECS, Cloud Run ou App Service
**Gerenciamento de Configuração** → Ansible ou soluções nativas de nuvem
**Fluxos de Trabalho GitOps** → ArgoCD ou Flux
**Pipelines de CI/CD** → GitHub Actions, GitLab CI ou Jenkins

## Desafios Comuns & Soluções

**Problema**: Desvio de infraestrutura entre código e realidade
**Solução**: Implemente detecção automática de desvio, use `terraform plan` em CI/CD, habilite acesso somente leitura a produção, mantenha integridade do state file

**Problema**: Gerenciamento de secrets e exposição de credenciais
**Solução**: Use gerenciadores de secrets nativos de nuvem (AWS Secrets Manager, HashiCorp Vault), implemente SOPS para secrets criptografados no Git, use IRSA/workload identity

**Problema**: Custos altos de nuvem e contas inesperadas
**Solução**: Implemente estratégia de tagging, use cost allocation tags, configure alertas de orçamento, dimensione adequadamente recursos, use instâncias spot, implemente auto-scaling

**Problema**: Configurações complexas de Kubernetes
**Solução**: Use Helm charts para templating, implemente Kustomize para configs específicas por ambiente, siga padrões GitOps, use operators para workloads complexas

## Dicas de Colaboração

- **Com Equipes de Desenvolvimento**: Forneça plataformas self-service, documente APIs, compartilhe infraestrutura como módulos reutilizáveis
- **Com Equipes de Segurança**: Implemente policy as code, automatize verificações de conformidade, forneça trilhas de auditoria
- **Com Equipes de SRE**: Defina SLIs/SLOs em conjunto, compartilhe responsabilidades de on-call, colabore em resposta a incidentes
- **Com Equipes de Finanças**: Forneça visibilidade de custos, preveja despesas, implemente modelos de chargeback

---

## Próximos Passos

1. Comece com [terraform.md](reference/terraform.md) se estiver implementando infrastructure as code
2. Use [kubernetes.md](reference/kubernetes.md) para orquestração de containers
3. Consulte [templates.md](reference/templates.md) para configurações prontas para uso
4. Verifique [observability.md](reference/observability.md) para configurar monitoramento

**Nota**: Sempre verifique o estado atual da infraestrutura, requisitos de segurança e necessidades de conformidade antes de implementar mudanças. Este Skill fornece frameworks e boas práticas, mas deve ser adaptado aos requisitos específicos da sua organização.