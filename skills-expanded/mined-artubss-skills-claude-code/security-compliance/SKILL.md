---
name: security-compliance
description: Guia para profissionais de segurança na implementação de arquiteturas de segurança em defesa em profundidade, alcance de conformidade com frameworks da indústria (SOC2, ISO27001, GDPR, HIPAA), realização de modelagem de ameaças e avaliações de risco, gestão de operações de segurança e resposta a incidentes, e integração de segurança em todo o SDLC.
---

# Especialista em Segurança & Conformidade

## Princípios Fundamentais

### 1. Defesa em Profundidade
Aplique múltiplas camadas de controles de segurança para que, se uma falhar, outras forneçam proteção. Nunca dependa de um único mecanismo de segurança.

### 2. Arquitetura Zero Trust
Nunca confie, sempre verifique. Assuma a possibilidade de violação e verifique cada solicitação de acesso independentemente da localização ou rede.

### 3. Menor Privilégio
Conceda o acesso mínimo necessário para que usuários e sistemas desempenhem suas funções. Revise e revogue regularmente permissões não utilizadas.

### 4. Segurança por Design
Integre requisitos de segurança desde os estágios iniciais do design do sistema, não como uma reflexão tardia.

### 5. Monitoramento Contínuo
Implemente monitoramento e alertas contínuos para detectar anomalias e eventos de segurança em tempo real.

### 6. Abordagem Baseada em Risco
Priorize esforços de segurança com base em avaliação de risco, concentrando recursos nos ativos mais críticos e ameaças prováveis.

### 7. Conformidade como Fundação
Use frameworks de conformidade como baseline, mas vá além dos requisitos mínimos para alcançar segurança real.

### 8. Preparação para Incidentes
Prepare-se para incidentes de segurança através de planejamento, testes e exercícios regulares de simulação. Assuma que compromissos ocorrerão.

---

## Ciclo de Vida de Segurança & Conformidade

### Fase 1: Avaliar & Planejar
**Objetivo**: Compreender a postura de segurança atual e os requisitos de conformidade

**Atividades**:
- Conduzir avaliações de segurança e análise de lacunas
- Identificar requisitos de conformidade (SOC2, ISO27001, GDPR, HIPAA, PCI-DSS)
- Realizar avaliações de risco e modelagem de ameaças
- Definir políticas e padrões de segurança
- Estabelecer estrutura de governança de segurança
- Criar roadmap de segurança com iniciativas priorizadas

**Entregáveis**:
- Registro de risco com riscos priorizados
- Relatório de análise de lacuna de conformidade
- Documentação de arquitetura de segurança
- Políticas e procedimentos de segurança
- Roadmap de segurança e orçamento

### Fase 2: Design & Arquitetura
**Objetivo**: Projetar sistemas e arquiteturas seguras

**Atividades**:
- Projetar arquiteturas de defesa em profundidade
- Implementar arquitetura de rede Zero Trust
- Projetar sistemas de gerenciamento de identidade e acesso (IAM)
- Arquitetar soluções de proteção e criptografia de dados
- Projetar pipelines de CI/CD seguros
- Criar modelos de ameaça para aplicações e sistemas
- Definir controles de segurança e controles compensatórios

**Entregáveis**:
- Diagramas de arquitetura de segurança
- Modelos de ameaça (STRIDE, PASTA ou árvores de ataque)
- Diagramas de fluxo de dados com limites de segurança
- Design de criptografia e gerenciamento de chaves
- Design de IAM com modelos RBAC/ABAC
- Matriz de controles de segurança

### Fase 3: Implementar & Fortalecer
**Objetivo**: Implantar controles de segurança e fortalecer sistemas

**Atividades**:
- Implementar controles de segurança (preventivos, detetivos, corretivos)
- Configurar ferramentas de segurança (SIEM, EDR, CASB, WAF, IDS/IPS)
- Fortalecer sistemas operacionais e aplicações
- Implementar criptografia em repouso e em trânsito
- Implantar autenticação multifatorial (MFA)
- Configurar logging e monitoramento
- Implementar prevenção de perda de dados (DLP)
- Estabelecer programa de gerenciamento de vulnerabilidades

**Entregáveis**:
- Baselines de hardening e padrões de configuração
- Ferramentas e controles de segurança implantados
- Implementação de criptografia
- Implantação de MFA
- Dashboards de monitoramento de segurança
- Procedimentos de gerenciamento de vulnerabilidades

### Fase 4: Monitorar & Detectar
**Objetivo**: Monitorar continuamente ameaças e anomalias

**Atividades**:
- Monitorar logs e eventos de segurança (SIEM)
- Analisar alertas e anomalias de segurança
- Conduzir threat hunting
- Realizar varreduras de vulnerabilidade e testes de penetração
- Monitorar controles de conformidade
- Rastrear métricas e KPIs de segurança
- Revisar logs de acesso e atividade de contas privilegiadas
- Analisar feeds de inteligência de ameaças

**Entregáveis**:
- Runbooks do centro de operações de segurança (SOC)
- Procedimentos de triagem de alertas e escalação
- Playbooks de threat hunting
- Relatórios de varredura de vulnerabilidade
- Relatórios de testes de penetração
- Dashboard de métricas de segurança
- Relatórios de monitoramento de conformidade

### Fase 5: Responder & Recuperar
**Objetivo**: Responder a incidentes de segurança e recuperar operações

**Atividades**:
- Executar plano de resposta a incidentes
- Conter e erradicar ameaças
- Realizar análise forense
- Recuperar sistemas afetados
- Conduzir análises pós-incidente
- Atualizar controles de segurança com base em lições aprendidas
- Relatar incidentes a stakeholders e reguladores
- Melhorar regras de detecção e procedimentos de resposta

**Entregáveis**:
- Relatórios de resposta a incidentes
- Descobertas de análise forense
- Análise de causa raiz
- Planos de remediação
- Playbooks de resposta a incidentes atualizados
- Notificações de violação regulatória (se necessário)
- Análise pós-incidente e recomendações

### Fase 6: Auditar & Melhorar
**Objetivo**: Validar conformidade e melhorar continuamente a segurança

**Atividades**:
- Conduzir auditorias internas
- Preparar-se para auditorias externas (SOC2, ISO27001)
- Realizar avaliações de conformidade
- Revisar e atualizar políticas de segurança
- Conduzir programas de treinamento e conscientização de segurança
- Realizar exercícios de simulação e testes de recuperação de desastres
- Atualizar avaliações de risco
- Implementar melhorias de segurança

**Entregáveis**:
- Relatórios de auditoria (interna e externa)
- Relatório SOC2 Type II
- Certificação ISO27001
- Atestados de conformidade
- Políticas e procedimentos atualizados
- Métricas de conclusão de treinamento
- Resultados de exercícios de simulação
- Plano de melhoria contínua

---

## Frameworks de Decisão

### 1. Framework de Avaliação de Risco

**Quando usar**: Avaliando riscos de segurança e priorizando esforços de mitigação

**Processo**:

```
1. Identificar Ativos
   - Quais sistemas, dados e serviços precisam de proteção?
   - Qual é o valor comercial de cada ativo?
   - Quem são os proprietários dos ativos?

2. Identificar Ameaças
   - Que atores de ameaça podem mirar nesses ativos? (estado-nação, cibercriminosos, insiders)
   - Quais são suas motivações? (ganho financeiro, espionagem, interrupção)
   - Quais são as tendências atuais de ameaças?

3. Identificar Vulnerabilidades
   - Quais fraquezas existem em sistemas ou processos?
   - Quais controles de segurança estão faltando ou ineficazes?
   - Quais CVEs conhecidas afetam seus sistemas?

4. Calcular Risco
   Risco = Probabilidade × Impacto

   Escala de Probabilidade (1-5):
   1 = Raro (< 5% de chance em 1 ano)
   2 = Improvável (5-25%)
   3 = Possível (25-50%)
   4 = Provável (50-75%)
   5 = Quase Certo (> 75%)

   Escala de Impacto (1-5):
   1 = Mínimo (< R$ 50K de perda, sem violação de dados)
   2 = Menor (R$ 50K-R$ 500K, exposição limitada de dados)
   3 = Moderado (R$ 500K-R$ 5M, violação significativa de dados)
   4 = Major (R$ 5M-R$ 50M, violação extensa de dados, multas regulatórias)
   5 = Catastrófico (> R$ 50M, ameaça à existência do negócio)

   Pontuação de Risco = Probabilidade × Impacto (máx. 25)

5. Priorizar Riscos
   - Crítico: Pontuação de risco 15-25 (ação imediata)
   - Alto: Pontuação de risco 10-14 (ação em 30 dias)
   - Médio: Pontuação de risco 5-9 (ação em 90 dias)
   - Baixo: Pontuação de risco 1-4 (monitorar e aceitar)

6. Determinar Resposta ao Risco
   - Mitigar: Implementar controles para reduzir risco
   - Aceitar: Documentar aceitação se o risco estiver dentro da tolerância
   - Transferir: Usar seguro ou serviços de terceiros
   - Evitar: Eliminar a atividade que cria o risco
```

**Resultado**: Registro de risco com riscos priorizados e planos de mitigação

### 2. Seleção de Controles de Segurança

**Quando usar**: Escolhendo controles de segurança apropriados para riscos identificados

**Framework**: Use categorias de NIST CSF ou CIS Controls

```
Funções de NIST CSF:
1. Identificar (ID)
   - Gerenciamento de Ativos
   - Avaliação de Risco
   - Governança

2. Proteger (PR)
   - Controle de Acesso
   - Segurança de Dados
   - Tecnologia de Proteção

3. Detectar (DE)
   - Anomalias e Eventos
   - Monitoramento de Segurança
   - Processos de Detecção

4. Responder (RS)
   - Planejamento de Resposta
   - Comunicações
   - Análise e Mitigação

5. Recuperar (RC)
   - Planejamento de Recuperação
   - Melhorias
   - Comunicações

Tipos de Controles:
- Preventivo: Impedir incidentes antes que ocorram (MFA, firewalls, criptografia)
- Detetivo: Identificar incidentes quando ocorrem (SIEM, IDS, monitoramento de logs)
- Corretivo: Corrigir problemas após a detecção (patching, resposta a incidentes)
- Dissuasor: Desencorajar atacantes (políticas de segurança, avisos)
- Compensatório: Controles alternativos quando os controles primários não são viáveis

Critérios de Seleção:
1. Ele aborda o risco identificado?
2. É custo-efetivo? (Custo do controle < Valor do risco)
3. É tecnicamente viável?
4. Ele atende aos requisitos de conformidade?
5. Podemos mantê-lo e monitorá-lo?
```

### 3. Seleção de Framework de Conformidade

**Quando usar**: Determinando quais frameworks de conformidade implementar

**Árvore de Decisão**:

```
Que tipo de organização você é?

├─ SaaS/Provedor de Serviço em Nuvem
│  ├─ Vendendo para empresas? → SOC2 Type II (obrigatório)
│  ├─ Clientes internacionais? → ISO27001 (altamente recomendado)
│  ├─ Processando dados de saúde? → HIPAA + HITRUST
│  └─ Processando cartões de pagamento? → PCI-DSS

├─ Provedor de Saúde/Pagador
│  ├─ Baseado nos EUA → HIPAA (obrigatório)
│  ├─ Clientes internacionais → HIPAA + GDPR
│  └─ Além disso: HITRUST para framework abrangente

├─ Serviços Financeiros
│  ├─ Bancos dos EUA → GLBA, SOX (se público)
│  ├─ Processamento de pagamentos → PCI-DSS (obrigatório)
│  ├─ Internacional → ISO27001, regulações locais
│  └─ Além disso: NIST CSF para framework

├─ E-commerce/Varejo
│  ├─ Aceita cartões de crédito → PCI-DSS (obrigatório)
│  ├─ Clientes na UE → GDPR (obrigatório)
│  ├─ Clientes na Califórnia → CCPA
│  └─ Vendas B2B → SOC2 Type II

└─ Empresa Geral
   ├─ Vendendo para empresas → SOC2 Type II
   ├─ Quer reconhecimento amplo → ISO27001
   ├─ Contratos governamentais → FedRAMP, NIST 800-53
   └─ Específico do setor → Verifique regulações do setor

Estratégia Multi-Framework:
- Comece com: SOC2 ou ISO27001 (escolha um como fundação)
- Adicione: Regulações de privacidade de dados (GDPR, CCPA) conforme necessário
- Camada: Requisitos específicos da indústria
```

### 4. Classificação de Severidade de Incidentes

**Quando usar**: Triagem e resposta a incidentes de segurança

**Níveis de Severidade**:

```
P0 - Crítico (Resposta Imediata)
- Violação ativa com exfiltração de dados ocorrendo
- Criptografia de ransomware em andamento
- Indisponibilidade completa de serviços críticos
- Acesso não autorizado a bancos de dados de produção
- Resposta: Ativar CIRT imediatamente, notificar executivos, esforço 24/7

P1 - Alto (Resposta em 1 hora)
- Malware confirmado em sistemas críticos
- Tentativa de acesso não autorizado a dados sensíveis
- Ataque DDoS afetando disponibilidade
- Vulnerabilidade significativa com exploits ativos
- Resposta: Ativar CIRT, notificar gerentes, trabalhar até conter

P2 - Médio (Resposta em 4 horas)
- Malware em sistemas não-críticos
- Atividade suspeita de conta
- Violações de política com impacto de segurança
- Vulnerabilidade que requer patching
- Resposta: Investigação da equipe de segurança, horário comercial

P3 - Baixo (Resposta em 24 horas)
- Tentativas de login falhadas (abaixo do threshold)
- Violações menores de política
- Eventos de segurança informativos
- Resposta: Fila padrão, documentar descobertas

Fatores de Classificação:
1. Impacto na confidencialidade de dados (PHI, PII, financeiro, PI)
2. Impacto na disponibilidade do sistema (receita, operações)
3. Impacto na integridade de dados (corrupção, mudanças não autorizadas)
4. Número de sistemas/usuários afetados
5. Requisitos de relatório regulatório
```

### 5. Priorização de Vulnerabilidades

**Quando usar**: Priorizando remediação de vulnerabilidades

**Framework**: CVSS aprimorado com contexto comercial

```
Pontuação Base de CVSS × Multiplicador de Contexto Comercial = Pontuação de Prioridade

Intervalos de Severidade de CVSS:
- Crítica: 9.0-10.0
- Alta: 7.0-8.9
- Média: 4.0-6.9
- Baixa: 0.1-3.9

Multiplicadores de Contexto Comercial:
- Sistema de produção voltado para a internet: 2.0×
- Sistema de produção interno: 1.5×
- Sistemas com dados sensíveis: 1.5×
- Ambiente de desenvolvimento/teste: 0.5×
- Exploit ativo em circulação: 2.0×
- Controles compensatórios em vigor: 0.7×

Níveis de Prioridade:
- P0 (Crítica): Pontuação ≥ 14 → Patchar em 24-48 horas
- P1 (Alta): Pontuação 10-13.9 → Patchar em 7 dias
- P2 (Média): Pontuação 6-9.9 → Patchar em 30 dias
- P3 (Baixa): Pontuação < 6 → Patchar em 90 dias ou aceitar risco

Considerações Adicionais:
- O sistema pode ser isolado/segmentado?
- Existem controles detetivos eficazes?
- Qual é a complexidade/risco do patching?
- Existe um patch do vendor disponível?
```

### 6. Avaliação de Risco de Terceiros

**Quando usar**: Avaliando riscos de segurança de vendors e parceiros

**Framework de Avaliação**:

```
1. Categorizar Nível de Risco do Vendor

Risco Baixo (Avaliação Mínima):
- Sem acesso a sistemas ou dados
- Integração limitada
- Serviço não-crítico
→ Questionário simples

Risco Médio (Avaliação Padrão):
- Acesso limitado a sistemas
- Acesso a dados não-sensíveis
- Serviço importante mas não crítico
→ Questionário de segurança + revisão de evidências

Risco Alto (Avaliação Abrangente):
- Acesso a sistema de produção
- Processamento de dados sensíveis
- Dependência de serviço crítico
→ Avaliação completa + relatórios de auditoria + teste de pen

Risco Crítico (Avaliação Extensa):
- Acesso total de produção
- Processamento de PHI/PII
- Dependência crítica do negócio
→ Auditoria presencial + monitoramento contínuo + SLA

2. Componentes de Avaliação

Para vendors Médio/Alto/Crítico:
□ Questionário de segurança (SIG, CAIQ, ou customizado)
□ Certificações de conformidade (SOC2, ISO27001)
□ Certificados de seguro (cyber liability)
□ Políticas e procedimentos de segurança
□ Plano de resposta a incidentes
□ Plano de recuperação/continuidade de negócios
□ Acordo de processamento de dados (DPA)
□ Resultados de testes de penetração (para risco alto/crítico)
□ Cláusula de direito de auditoria no contrato

3. Monitoramento Contínuo

- Reavaliação anual
- Monitorar violações/incidentes
- Revisar atualizações e patches de segurança
- Rastrear renovações de certificação de conformidade
- Conduzir auditorias periódicas (para vendors críticos)

4. Pontuação de Risco do Vendor

Calcule pontuação (0-100):
- Maturidade de segurança: 40 pontos
- Certificações de conformidade: 20 pontos
- Histórico de incidentes: 15 pontos
- Estabilidade financeira: 15 pontos
- Referências e reputação: 10 pontos

Ação baseada em pontuação:
- 80-100: Aprovado
- 60-79: Aprovado com condições
- 40-59: Requer plano de remediação
- < 40: Não participar
```

---

## Principais Frameworks & Padrões de Segurança

### NIST Cybersecurity Framework (CSF)
- **Propósito**: Framework baseado em risco para melhorar cibersegurança
- **Estrutura**: 5 Funções, 23 Categorias, 108 Subcategorias
- **Melhor para**: Organizações gerais, contratados do governo
- **Modelo de maturidade**: Tier 1 (Parcial) a Tier 4 (Adaptativo)

### CIS Critical Security Controls
- **Propósito**: Conjunto priorizado de ações para defesa cibernética
- **Estrutura**: 18 Controles com Grupos de Implementação (IG1, IG2, IG3)
- **Melhor para**: Orientação de implementação prática
- **Foco**: Defesa contra padrões comuns de ataque

### ISO/IEC 27001
- **Propósito**: Padrão internacional para gerenciamento de segurança da informação
- **Estrutura**: 14 domínios, 114 controles (Anexo A)
- **Melhor para**: Reconhecimento internacional, certificação formal
- **Requisitos**: ISMS (Sistema de Gerenciamento de Segurança da Informação)

### SOC 2 Type II
- **Propósito**: Controles de organização de serviço para segurança e disponibilidade
- **Estrutura**: Critérios de Confiança (Segurança, Disponibilidade, Confidencialidade, Integridade de Processamento, Privacidade)
- **Melhor para**: Empresas SaaS, provedores de serviço em nuvem
- **Auditoria**: Período de observação de 3-12 meses

### NIST 800-53
- **Propósito**: Controles de segurança para sistemas federais
- **Estrutura**: 20 famílias, 1000+ controles
- **Melhor para**: Contratados do governo, FedRAMP
- **Baselines**: Impacto baixo, moderado, alto

### GDPR (Regulamento Geral sobre Proteção de Dados)
- **Propósito**: Regulação de privacidade de dados da UE
- **Escopo**: Qualquer organização processando dados de residentes da UE
- **Requisitos**: Base legal, consentimento, direitos do titular de dados, notificação de violação
- **Penalidades**: Até 4% da receita global ou €20M

### HIPAA (Lei de Portabilidade e Responsabilidade de Seguros Saúde)
- **Propósito**: Proteger informações de saúde (PHI)
- **Escopo**: Provedores de saúde, pagadores, parceiros comerciais
- **Requisitos**: Salvaguardas administrativas, físicas, técnicas
- **Penalidades**: R$ 500-R$ 250K+ por violação, acusações criminais possíveis

### PCI-DSS (Padrão de Segurança de Dados da Indústria de Cartões de Pagamento)
- **Propósito**: Proteger dados de titulares de cartão
- **Estrutura**: 12 requisitos, 6 objetivos de controle
- **Escopo**: Qualquer organização armazenando, processando ou transmitindo dados de cartão
- **Níveis**: Baseado em volume de transações (Nível 1-4)

---

## Domínios Principais de Segurança

### 1. Gerenciamento de Identidade e Acesso (IAM)
- Mecanismos de autenticação (MFA, SSO, passwordless)
- Modelos de autorização (RBAC, ABAC, ReBAC)
- Gerenciamento de acesso privilegiado (PAM)
- Governança e administração de identidade (IGA)
- Serviços de diretório (Active Directory, LDAP, Okta, Auth0)

### 2. Segurança de Rede
- Segmentação de rede e micro-segmentação
- Firewalls (próxima geração, WAF, camada de aplicação)
- Detecção/prevenção de intrusão (IDS/IPS)
- VPN e acesso remoto seguro
- Arquitetura de rede Zero Trust (ZTNA)
- Proteção contra DDoS

### 3. Segurança de Dados
- Criptografia em repouso e em trânsito (AES-256, TLS 1.3)
- Gerenciamento de chaves (KMS, HSM)
- Classificação e rotulagem de dados
- Prevenção de perda de dados (DLP)
- Segurança de banco de dados (criptografia, masking, tokenização)
- Gerenciamento de segredos (Vault, AWS Secrets Manager)

### 4. Segurança de Aplicação
- SDLC seguro e DevSecOps
- SAST (Teste Estático de Segurança de Aplicação)
- DAST (Teste Dinâmico de Segurança de Aplicação)
- SCA (Análise de Composição de Software)
- Análise de código seguro
- Mitigação OWASP Top 10

### 5. Segurança em Nuvem
- Gerenciamento de postura de segurança em nuvem (CSPM)
- Cloud Access Security Broker (CASB)
- Segurança de container (varredura de imagem, proteção de runtime)
- Segurança sem servidor
- Varredura de segurança de Infrastructure as Code (IaC)
- Arquitetura de segurança multi-nuvem

### 6. Segurança de Endpoint
- Detecção e Resposta de Endpoint (EDR)
- Antivírus e anti-malware
- Firewalls baseados em host
- Criptografia de dispositivo (BitLocker, FileVault)
- Gerenciamento de dispositivo móvel (MDM)
- Gerenciamento de patches

### 7. Operações de Segurança
- Gerenciamento de Informações e Eventos de Segurança (SIEM)
- Orquestração, Automação e Resposta de Segurança (SOAR)
- Plataformas de Inteligência de Ameaças (TIP)
- Threat hunting
- Gerenciamento de vulnerabilidades
- Testes de penetração e red teaming

### 8. Resposta a Incidentes
- Plano e playbooks de resposta a incidentes
- Perícia computacional e investigação
- Análise de malware
- Contenção e erradicação de ameaças
- Revisão pós-incidente e lições aprendidas
- Notificação de violação regulatória

### 9. Governança, Risco & Conformidade (GRC)
- Políticas e procedimentos de segurança
- Avaliação e gerenciamento de risco
- Gerenciamento e auditoria de conformidade
- Treinamento de conscientização de segurança
- Gerenciamento de risco de vendors
- Continuidade de negócios e recuperação de desastres

---

## Métricas & KPIs de Segurança

### Métricas de Risco & Conformidade
- Número de riscos críticos/altos abertos
- Tempo de remediação de risco (tempo médio para remediar)
- Descobertas de auditoria de conformidade (abertas/fechadas)
- Taxa de efetividade de controle de conformidade
- Taxa de conclusão de reconhecimento de política
- Taxa de conclusão de treinamento

### Métricas de Gerenciamento de Vulnerabilidades
- Tempo médio para detectar (MTTD) vulnerabilidades
- Tempo médio para patchar (MTTP)
- Backlog de vulnerabilidades (total aberto, por severidade)
- Taxa de conformidade de patch (% de sistemas patchados dentro de SLA)
- Taxa de recorrência de vulnerabilidades

### Métricas de Resposta a Incidentes
- Tempo médio para detectar (MTTD) incidentes
- Tempo médio para responder (MTTR)
- Tempo médio para conter (MTTC)
- Tempo médio para recuperar (MTTR)
- Número de incidentes por severidade
- Taxa de recorrência de incidentes
- Taxa de falsos positivos

### Métricas de Operações de Segurança
- Volume de alerta de SIEM (total, por severidade)
- Tempo de triagem de alerta
- Taxa de falso positivo de alerta
- Cober