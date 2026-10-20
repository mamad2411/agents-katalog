## Instruções Específicas da Empresa para Product Owner

### Contexto Organizacional
- Nossa empresa é uma software house focada em soluções .NET para o mercado brasileiro
- Trabalhamos principalmente com sistemas web usando ASP.NET Core, Entity Framework e PostgreSQL
- Nossos clientes são principalmente PMEs do setor financeiro e de saúde
- Atuamos no modelo de desenvolvimento sob demanda e produtos próprios

### Metodologia de Trabalho
- **Sprints:** 2 semanas de duração
- **Planning:** Segundas-feiras às 9h
- **Review/Retro:** Sextas-feiras às 14h  
- **Standup:** Diário às 9h (15min máx)
- **Refinement:** Quartas-feiras às 14h

### Critérios de Aceitação Padrão
Toda funcionalidade deve atender:
- Testes unitários com cobertura mínima de 80%
- Code review obrigatório antes do merge
- Documentação técnica atualizada
- Compliance com LGPD quando há dados pessoais
- Performance testada (< 2s para telas de consulta)
- Responsivo para mobile e desktop

### Stakeholders Típicos por Projeto
- **Cliente final:** Usuários operacionais do sistema
- **Sponsor:** Diretor de TI ou Gerente de Projetos
- **Compliance:** Time jurídico (validação LGPD/GDPR)
- **Infraestrutura:** DevOps interno (deploy e monitoramento)
- **Segurança:** CISO para validação de segurança
- **UX/UI:** Designer para validação de experiência

### Frameworks e Padrões Técnicos Preferidos
- **Backend:** ASP.NET Core 8.0+, Entity Framework Core
- **Frontend:** React com TypeScript ou Blazor Server
- **Banco:** PostgreSQL ou SQL Server
- **Cache:** Redis para sessões e cache distribuído
- **Logs:** Serilog com Elasticsearch
- **Monitoramento:** Application Insights
- **Deploy:** Azure DevOps Pipelines

### Definição de Pronto (DoD)
Uma funcionalidade está pronta quando:
1. Código desenvolvido e testado
2. Testes unitários passando (>80% cobertura)
3. Code review aprovado
4. Testes de integração passando
5. Deploy em ambiente de homologação realizado
6. Validação funcional pelo PO
7. Documentação técnica atualizada
8. Validação de segurança (se aplicável)

### Métricas de Sucesso do Produto
- **Performance:** Tempo de resposta < 2s (90% das requests)
- **Disponibilidade:** SLA 99.9% mensal
- **Qualidade:** Bugs críticos < 1 por sprint
- **Satisfação:** NPS > 8 com usuários finais
- **Adoção:** Taxa de utilização > 75% dos usuários ativos

### Cenários de Risco Comum
- **Integração com sistemas legados:** Sempre mapear APIs e formatos de dados
- **Migração de dados:** Planejar estratégia de rollback e validação
- **Compliance LGPD:** Revisar fluxos de dados pessoais
- **Performance:** Testar com volume real de dados
- **Segurança:** Validar autenticação, autorização e auditoria

### Templates de User Story
**Funcional:**
```
Como [usuário/stakeholder]
Eu quero [funcionalidade]  
Para que [valor/benefício]

Critérios de Aceitação:
- [ ] Dado que [contexto], quando [ação], então [resultado]
- [ ] Performance: [métrica específica]
- [ ] Segurança: [validação necessária]
```

**Técnica:**  
```
Como desenvolvedor
Eu preciso [infraestrutura/ferramenta]
Para que [capacidade técnica/manutenibilidade]
```

### Priorização (Método MoSCoW adaptado)
- **Must:** Funcionalidades críticas para operação
- **Should:** Importantes para produtividade  
- **Could:** Melhorias de experiência
- **Won't:** Fora do escopo atual (backlog futuro)