---
name: server-management
description: Princípios de gerenciamento de servidores e tomada de decisão. Gestão de processos, estratégia de monitoramento e decisões de escalabilidade. Ensina raciocínio, não comandos.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Gerenciamento de Servidores

> Princípios de gerenciamento de servidores para operações em produção.
> **Aprenda a PENSAR, não decore comandos.**

---

## 1. Princípios de Gestão de Processos

### Seleção de Ferramentas

| Cenário | Ferramenta |
|----------|-------------|
| **App Node.js** | PM2 (clustering, reload) |
| **Qualquer app** | systemd (nativo Linux) |
| **Containers** | Docker/Podman |
| **Orquestração** | Kubernetes, Docker Swarm |

### Objetivos da Gestão de Processos

| Objetivo | O Que Significa |
|----------|-----------------|
| **Reiniciar em falha** | Auto-recuperação |
| **Reload sem tempo de inatividade** | Sem interrupção de serviço |
| **Clustering** | Usar todos os núcleos da CPU |
| **Persistência** | Sobreviver a reinicializações do servidor |

---

## 2. Princípios de Monitoramento

### O Que Monitorar

| Categoria | Métricas-Chave |
|----------|-----------------|
| **Disponibilidade** | Uptime, health checks |
| **Performance** | Tempo de resposta, throughput |
| **Erros** | Taxa de erro, tipos |
| **Recursos** | CPU, memória, disco |

### Estratégia de Severidade de Alertas

| Nível | Resposta |
|-------|----------|
| **Crítico** | Ação imediata |
| **Aviso** | Investigar em breve |
| **Info** | Revisar diariamente |

### Seleção de Ferramentas de Monitoramento

| Necessidade | Opções |
|----------|---------|
| Simples/Gratuito | PM2 metrics, htop |
| Observabilidade completa | Grafana, Datadog |
| Rastreamento de erros | Sentry |
| Uptime | UptimeRobot, Pingdom |

---

## 3. Princípios de Gestão de Logs

### Estratégia de Logs

| Tipo de Log | Propósito |
|----------|----------|
| **Logs de aplicação** | Debug, auditoria |
| **Logs de acesso** | Análise de tráfego |
| **Logs de erro** | Detecção de problemas |

### Princípios de Log

1. **Rotacione logs** para evitar preenchimento de disco
2. **Logging estruturado** (JSON) para parsing
3. **Níveis apropriados** (error/warn/info/debug)
4. **Sem dados sensíveis** nos logs

---

## 4. Decisões de Escalabilidade

### Quando Escalar

| Sintoma | Solução |
|---------|---------|
| CPU alta | Adicionar instâncias (horizontal) |
| Memória alta | Aumentar RAM ou corrigir vazamento |
| Resposta lenta | Profile primeiro, depois escale |
| Picos de tráfego | Auto-scaling |

### Estratégia de Escalabilidade

| Tipo | Quando Usar |
|------|-------------|
| **Vertical** | Correção rápida, instância única |
| **Horizontal** | Sustentável, distribuído |
| **Auto** | Tráfego variável |

---

## 5. Princípios de Health Check

### O Que Constitui um Serviço Saudável

| Check | Significado |
|-------|-------------|
| **HTTP 200** | Serviço respondendo |
| **Banco de dados conectado** | Dados acessíveis |
| **Dependências OK** | Serviços externos acessíveis |
| **Recursos OK** | CPU/memória não esgotados |

### Implementação de Health Check

- Simples: Apenas retorne 200
- Profundo: Verifique todas as dependências
- Escolha com base nas necessidades do load balancer

---

## 6. Princípios de Segurança

| Área | Princípio |
|------|-----------|
| **Acesso** | Apenas chaves SSH, sem senhas |
| **Firewall** | Apenas portas necessárias abertas |
| **Atualizações** | Patches de segurança regulares |
| **Secrets** | Variáveis de ambiente, não arquivos |
| **Auditoria** | Registre acesso e alterações |

---

## 7. Prioridade de Troubleshooting

Quando algo não está funcionando:

1. **Verificar se está rodando** (status do processo)
2. **Verificar logs** (mensagens de erro)
3. **Verificar recursos** (disco, memória, CPU)
4. **Verificar rede** (portas, DNS)
5. **Verificar dependências** (banco de dados, APIs)

---

## 8. Anti-padrões

| ❌ Não Faça | ✅ Faça |
|----------|-------|
| Executar como root | Use usuário não-root |
| Ignorar logs | Configure rotação de logs |
| Pular monitoramento | Monitore desde o início |
| Reinicializações manuais | Configure auto-restart |
| Sem backups | Cronograma de backup regular |

---

> **Lembre-se:** Um servidor bem gerenciado é entediante. Esse é o objetivo.