---
name: deployment-procedures
description: Princípios de deploy em produção e tomada de decisão. Workflows seguros de deployment, estratégias de rollback e verificação. Ensina raciocínio, não scripts.
allowed-tools: Read, Glob, Grep, Bash
---

# Procedimentos de Deployment

> Princípios de deployment e tomada de decisão para releases seguros em produção.
> **Aprenda a PENSAR, não decore scripts.**

---

## ⚠️ Como Usar Esta Habilidade

Esta habilidade ensina **princípios de deployment**, não bash scripts para copiar.

- Cada deployment é único
- Entenda o POR QUE por trás de cada passo
- Adapte os procedimentos à sua plataforma

---

## 1. Seleção de Plataforma

### Árvore de Decisão

```
O que você está fazendo deploy?
│
├── Site estático / JAMstack
│   └── Vercel, Netlify, Cloudflare Pages
│
├── App web simples
│   ├── Gerenciado → Railway, Render, Fly.io
│   └── Controle → VPS + PM2/Docker
│
├── Microserviços
│   └── Orquestração de containers
│
└── Serverless
    └── Edge functions, Lambda
```

### Cada Plataforma Tem Procedimentos Diferentes

| Plataforma | Método de Deployment |
|----------|------------------|
| **Vercel/Netlify** | Git push, deploy automático |
| **Railway/Render** | Git push ou CLI |
| **VPS + PM2** | SSH + passos manuais |
| **Docker** | Push de imagem + orquestração |
| **Kubernetes** | kubectl apply |

---

## 2. Princípios Pré-Deployment

### As 4 Categorias de Verificação

| Categoria | O que Verificar |
|----------|--------------|
| **Qualidade de Código** | Testes passando, linting limpo, revisado |
| **Build** | Build de produção funciona, sem avisos |
| **Ambiente** | Variáveis de ambiente definidas, secrets atualizados |
| **Segurança** | Backup feito, plano de rollback pronto |

### Checklist Pré-Deployment

- [ ] Todos os testes passando
- [ ] Código revisado e aprovado
- [ ] Build de produção bem-sucedido
- [ ] Variáveis de ambiente verificadas
- [ ] Migrações de banco de dados prontas (se houver)
- [ ] Plano de rollback documentado
- [ ] Time notificado
- [ ] Monitoramento ativo

---

## 3. Princípios de Workflow de Deployment

### O Processo de 5 Fases

```
1. PREPARAR
   └── Verificar código, build, variáveis de ambiente

2. BACKUP
   └── Salvar estado atual antes de mudar

3. DEPLOY
   └── Executar com monitoramento aberto

4. VERIFICAR
   └── Health check, logs, fluxos-chave

5. CONFIRMAR ou ROLLBACK
   └── Tudo bem? Confirmar. Problemas? Rollback.
```

### Princípios das Fases

| Fase | Princípio |
|-------|-----------|
| **Preparar** | Nunca faça deploy de código não testado |
| **Backup** | Não é possível fazer rollback sem backup |
| **Deploy** | Acompanhe, não se afaste |
| **Verificar** | Confie, mas verifique |
| **Confirmar** | Tenha o gatilho de rollback pronto |

---

## 4. Verificação Pós-Deployment

### O que Verificar

| Verificação | Por Quê |
|-------|-----|
| **Endpoint de health** | Serviço está rodando |
| **Logs de erro** | Sem novos erros |
| **Fluxos de usuário-chave** | Funcionalidades críticas funcionam |
| **Performance** | Tempos de resposta aceitáveis |

### Janela de Verificação

- **Primeiros 5 minutos**: Monitoramento ativo
- **15 minutos**: Confirmar estabilidade
- **1 hora**: Verificação final
- **Próximo dia**: Revisar métricas

---

## 5. Princípios de Rollback

### Quando Fazer Rollback

| Sintoma | Ação |
|---------|--------|
| Serviço fora | Rollback imediato |
| Erros críticos | Rollback |
| Performance >50% degradada | Considere rollback |
| Problemas menores | Corrija adiante se rápido |

### Estratégia de Rollback por Plataforma

| Plataforma | Método de Rollback |
|----------|----------------|
| **Vercel/Netlify** | Redeploy do commit anterior |
| **Railway/Render** | Rollback no dashboard |
| **VPS + PM2** | Restaurar backup, reiniciar |
| **Docker** | Tag de imagem anterior |
| **K8s** | kubectl rollout undo |

### Princípios de Rollback

1. **Velocidade sobre perfeição**: Rollback primeiro, debugue depois
2. **Não compunha erros**: Um rollback, não múltiplas mudanças
3. **Comunique**: Diga ao time o que aconteceu
4. **Post-mortem**: Entenda por que depois de estável

---

## 6. Deployment com Zero Downtime

### Estratégias

| Estratégia | Como Funciona |
|----------|--------------|
| **Rolling** | Substituir instâncias uma por uma |
| **Blue-Green** | Mudar tráfego entre ambientes |
| **Canary** | Mudança gradual de tráfego |

### Princípios de Seleção

| Cenário | Estratégia |
|----------|----------|
| Release padrão | Rolling |
| Mudança de alto risco | Blue-green (rollback fácil) |
| Precisa validação | Canary (teste com tráfego real) |

---

## 7. Procedimentos de Emergência

### Prioridade Serviço Fora

1. **Avalie**: Qual é o sintoma?
2. **Correção rápida**: Reinicie se unclear
3. **Rollback**: Se reinício não ajudar
4. **Investigue**: Depois de estável

### Ordem de Investigação

| Verificação | Problemas Comuns |
|-------|--------------|
| **Logs** | Erros, exceções |
| **Recursos** | Disco cheio, memória |
| **Rede** | DNS, firewall |
| **Dependências** | Banco de dados, APIs |

---

## 8. Anti-Padrões

| ❌ Não Faça | ✅ Faça |
|----------|-------|
| Deploy na sexta | Deploy no início da semana |
| Acelere deployment | Siga o processo |
| Pule staging | Sempre teste primeiro |
| Deploy sem backup | Backup antes de deploy |
| Saia após deploy | Monitore por 15+ min |
| Múltiplas mudanças por vez | Uma mudança por vez |

---

## 9. Checklist de Decisão

Antes de fazer deploy:

- [ ] **Procedimento apropriado para a plataforma?**
- [ ] **Estratégia de backup pronta?**
- [ ] **Plano de rollback documentado?**
- [ ] **Monitoramento configurado?**
- [ ] **Time notificado?**
- [ ] **Tempo para monitorar depois?**

---

## 10. Melhores Práticas

1. **Deploys pequenos e frequentes** sobre releases grandes
2. **Feature flags** para mudanças arriscadas
3. **Automatize** passos repetitivos
4. **Documente** cada deployment
5. **Revise** o que deu errado após problemas
6. **Teste rollback** antes de precisar

---

> **Lembre-se:** Cada deployment é um risco. Minimize risco através da preparação, não da velocidade.