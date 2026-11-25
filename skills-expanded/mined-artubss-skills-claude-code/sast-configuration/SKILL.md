---
name: sast-configuration
description: "Configuração de ferramentas de Teste Estático de Segurança de Aplicações (SAST), customização e criação de regras personalizadas para varredura de segurança abrangente em múltiplas linguagens de programação."
risk: unknown
source: community
date_added: "2026-02-27"
---

# Configuração de SAST

Configuração de ferramentas de Teste Estático de Segurança de Aplicações (SAST), customização e criação de regras personalizadas para varredura de segurança abrangente em múltiplas linguagens de programação.

## Use essa habilidade quando

- Configurar varredura SAST em pipelines CI/CD
- Criar regras de segurança personalizadas para sua base de código
- Configurar quality gates e políticas de conformidade
- Otimizar desempenho de varredura e reduzir falsos positivos
- Integrar múltiplas ferramentas SAST para defesa em profundidade

## Não use essa habilidade quando

- Você precisa apenas de orientação em DAST ou teste de penetração manual
- Você não tem acesso ao código-fonte ou pipelines CI/CD
- Você precisa de decisões de política organizacional em vez de configuração de ferramentas

## Instruções

1. Identifique linguagens, repositórios e requisitos de conformidade.
2. Escolha ferramentas e defina uma política baseline.
3. Integre varreduras em CI/CD com thresholds de gating.
4. Ajuste regras e suppressões com base em falsos positivos.
5. Acompanhe remediação e verifique correções.

## Segurança

- Evite varreduras de repositórios sensíveis com serviços de terceiros sem aprovação.
- Previna vazamentos de secrets em artefatos de varredura e logs.

## Visão Geral

Essa habilidade fornece orientação abrangente para configuração de ferramentas SAST, incluindo Semgrep, SonarQube e CodeQL.

## Capacidades Principais

### 1. Configuração Semgrep
- Criação de regras personalizadas com pattern matching
- Regras de segurança específicas por linguagem (Python, JavaScript, Go, Java, etc.)
- Integração CI/CD (GitHub Actions, GitLab CI, Jenkins)
- Ajuste de falsos positivos e otimização de regras
- Imposição de política organizacional

### 2. Configuração SonarQube
- Configuração de quality gates
- Análise de hotspots de segurança
- Rastreamento de cobertura de código e débito técnico
- Perfis de qualidade personalizados por linguagem
- Integração empresarial com LDAP/SAML

### 3. Análise CodeQL
- Integração com GitHub Advanced Security
- Desenvolvimento de queries personalizadas
- Análise de variantes de vulnerabilidade
- Workflows de pesquisa de segurança
- Processamento de resultado SARIF

## Início Rápido

### Avaliação Inicial
1. Identifique as linguagens de programação primárias em sua base de código
2. Determine requisitos de conformidade (PCI-DSS, SOC 2, etc.)
3. Escolha ferramenta SAST baseado em suporte de linguagem e necessidades de integração
4. Revise varredura baseline para entender a postura de segurança atual

### Configuração Básica
```bash
# Início rápido com Semgrep
pip install semgrep
semgrep --config=auto --error

# SonarQube com Docker
docker run -d --name sonarqube -p 9000:9000 sonarqube:latest

# Configuração CLI do CodeQL
gh extension install github/gh-codeql
codeql database create mydb --language=python
```

## Documentação de Referência

- Semgrep Rule Creation - Desenvolvimento de regras de segurança baseadas em pattern
- SonarQube Configuration - Quality gates e perfis
- CodeQL Setup Guide - Desenvolvimento de queries e workflows

## Templates & Assets

- semgrep-config.yml - Configuração Semgrep pronta para produção
- sonarqube-settings.xml - Template de perfil de qualidade SonarQube
- run-sast.sh - Script de execução automática de SAST

## Padrões de Integração

### Integração com Pipeline CI/CD
```yaml
# Exemplo GitHub Actions
- name: Run Semgrep
  uses: returntocorp/semgrep-action@v1
  with:
    config: >-
      p/security-audit
      p/owasp-top-ten
```

### Pre-commit Hook
```bash
# .pre-commit-config.yaml
- repo: https://github.com/returntocorp/semgrep
  rev: v1.45.0
  hooks:
    - id: semgrep
      args: ['--config=auto', '--error']
```

## Melhores Práticas

1. **Comece com Baseline**
   - Execute varredura inicial para estabelecer baseline de segurança
   - Priorize achados críticos e de alta severidade
   - Crie roadmap de remediação

2. **Adoção Incremental**
   - Comece com regras focadas em segurança
   - Adicione gradualmente regras de qualidade de código
   - Implemente bloqueio apenas para problemas críticos

3. **Gerenciamento de Falsos Positivos**
   - Documente suppressões legítimas
   - Crie listas de permissão para patterns conhecidos seguros
   - Revise regularmente achados suprimidos

4. **Otimização de Desempenho**
   - Exclude arquivos de teste e código gerado
   - Use varredura incremental para bases de código grandes
   - Armazene em cache resultados de varredura em CI/CD

5. **Capacitação do Time**
   - Forneça treinamento de segurança para desenvolvedores
   - Crie documentação interna para patterns comuns
   - Estabeleça programa de security champions

## Casos de Uso Comum

### Configuração de Novo Projeto
```bash
./scripts/run-sast.sh --setup --language python --tools semgrep,sonarqube
```

### Desenvolvimento de Regra Personalizada
```yaml
# Veja references/semgrep-rules.md para exemplos detalhados
rules:
  - id: hardcoded-jwt-secret
    pattern: jwt.encode($DATA, "...", ...)
    message: JWT secret não deve ser hardcoded
    severity: ERROR
```

### Varredura de Conformidade
```bash
# Varredura focada em PCI-DSS
semgrep --config p/pci-dss --json -o pci-scan-results.json
```

## Troubleshooting

### Taxa Alta de Falsos Positivos
- Revise e ajuste sensibilidade de regra
- Adicione filtros de path para excluir arquivos de teste
- Use metadados nostmt para patterns barulhentos
- Crie exceções de regra específicas da organização

### Problemas de Desempenho
- Ative varredura incremental
- Paralelizar varreduras entre módulos
- Otimize patterns de regra para eficiência
- Armazene em cache dependências e resultados de varredura

### Falhas de Integração
- Verifique tokens de API e credenciais
- Valide conectividade de rede e configurações de proxy
- Revise compatibilidade de formato de saída SARIF
- Valide permissões do runner de CI/CD

## Habilidades Relacionadas

- OWASP Top 10 Checklist
- Container Security
- Dependency Scanning

## Comparação de Ferramentas

| Ferramenta | Melhor para | Suporte de Linguagem | Custo | Integração |
|------|----------|------------------|------|-------------|
| Semgrep | Regras personalizadas, varreduras rápidas | 30+ linguagens | Grátis/Enterprise | Excelente |
| SonarQube | Qualidade de código + segurança | 25+ linguagens | Grátis/Comercial | Bom |
| CodeQL | Análise profunda, pesquisa | 10+ linguagens | Grátis (OSS) | GitHub nativo |

## Próximos Passos

1. Conclua configuração inicial de ferramenta SAST
2. Execute varredura de segurança baseline
3. Crie regras personalizadas para patterns específicos da organização
4. Integre ao pipeline CI/CD
5. Estabeleça políticas de security gate
6. Treine time de desenvolvimento em achados e remediação