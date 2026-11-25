---
name: Data Privacy Compliance
description: Especialista em privacidade de dados e conformidade regulatória para GDPR, CCPA, HIPAA e leis internacionais de proteção de dados. Use ao implementar controles de privacidade, conduzir avaliações de impacto de proteção de dados, garantir conformidade regulatória ou gerenciar direitos de titulares de dados. Especialista em gestão de consentimento, minimização de dados e princípios de privacidade por design.
---

# Conformidade com Privacidade de Dados

Orientação abrangente para implementar conformidade com privacidade de dados em GDPR, CCPA, HIPAA e outras regulamentações globais de proteção de dados.

## Quando Usar Esta Habilidade

Use esta habilidade quando:
- Implementar conformidade com GDPR, CCPA ou HIPAA
- Conduzir Avaliações de Impacto de Proteção de Dados (DPIA)
- Gerenciar direitos de titulares de dados (acesso, exclusão, portabilidade)
- Implementar sistemas de gestão de consentimento
- Redigir políticas de privacidade e avisos
- Lidar com violações de dados e resposta a incidentes
- Projetar sistemas com privacidade por design
- Conduzir auditorias e avaliações de privacidade

## Visão Geral das Principais Regulamentações

### GDPR (Regulamento Geral de Proteção de Dados)
**Escopo:** Dados de residentes da UE, independentemente de onde a empresa está localizada
**Requisitos Principais:**
- Base legal para processamento (consentimento, contrato, interesse legítimo, etc.)
- Direitos de titulares de dados (acesso, exclusão, portabilidade, objeção)
- Avaliações de Impacto de Proteção de Dados para processamento de alto risco
- Requisito de notificação de violação em 72 horas
- Registros de atividades de processamento
- Privacidade por design e por padrão

**Multas:** Até €20M ou 4% da receita anual global

### CCPA/CPRA (Lei de Privacidade do Consumidor da Califórnia)
**Escopo:** Dados de residentes da Califórnia
**Requisitos Principais:**
- Direito de saber que dados são coletados
- Direito de excluir informações pessoais
- Direito de recusar venda/compartilhamento
- Direito de corrigir informações imprecisas
- Direito de limitar o uso de informações sensíveis

**Multas:** Até $7.500 por violação intencional

### HIPAA (Lei de Portabilidade e Responsabilidade de Seguros de Saúde)
**Escopo:** Informações de Saúde Protegidas (PHI) nos EUA
**Requisitos Principais:**
- Regra de Privacidade (direitos do paciente e usos de informações)
- Regra de Segurança (salvaguardas para ePHI)
- Regra de Notificação de Violação (notificação em 60 dias)
- Contratos de Associado Comercial (BAAs)

**Multas:** Até $1.5M por categoria de violação por ano

## Implementação de Direitos de Titulares de Dados

### 1. Direito de Acesso (GDPR Art. 15 / CCPA § 1798.100)

**Manipulador de Solicitação:**
```javascript
async function handleAccessRequest(userId, email) {
  // Verificar identidade
  const verified = await verifyIdentity(email);
  if (!verified) throw new Error('Identity verification failed');

  // Coletar todos os dados pessoais
  const userData = await collectUserData(userId);

  // Formatar para legibilidade
  const report = {
    personalInfo: userData.profile,
    activityLogs: userData.activities,
    preferences: userData.settings,
    thirdPartySharing: userData.dataSharing,
    retentionPeriod: '2 years from last activity',
    dataProtectionOfficer: 'dpo@company.com'
  };

  // Gerar relatório em PDF para download
  const pdf = await generatePDFReport(report);

  // Registrar solicitação para conformidade
  await logAccessRequest(userId, 'completed');

  return pdf;
}
```

**Linha do Tempo de Resposta:**
- GDPR: 1 mês (extensível para 3 meses)
- CCPA: 45 dias (extensível para 90 dias)

### 2. Direito de Exclusão (GDPR Art. 17 / CCPA § 1798.105)

**Manipulador de Exclusão:**
```javascript
async function handleDeletionRequest(userId, email) {
  // Verificar identidade
  const verified = await verifyIdentity(email);
  if (!verified) throw new Error('Identity verification failed');

  // Verificar obrigações legais de retenção
  const mustRetain = await checkRetentionRequirements(userId);
  if (mustRetain.required) {
    return {
      status: 'partial_deletion',
      retained: mustRetain.data,
      reason: mustRetain.legalBasis,
      retentionPeriod: mustRetain.period
    };
  }

  // Excluir de todos os sistemas
  await Promise.all([
    deleteFromDatabase(userId),
    deleteFromBackups(userId), // Marcar para exclusão no próximo ciclo de backup
    deleteFromAnalytics(userId),
    deleteFromThirdPartyServices(userId),
    revokeAPIKeys(userId),
    anonymizeHistoricalRecords(userId)
  ]);

  // Confirmar exclusão
  await sendDeletionConfirmation(email);
  await logDeletionRequest(userId, 'completed');

  return { status: 'deleted', timestamp: new Date() };
}
```

**Exceções (quando a exclusão pode ser recusada):**
- Obrigações legais (registros fiscais, contratos)
- Interesse público/pesquisa científica
- Defesa de ações legais
- Exercício da liberdade de expressão

### 3. Direito de Portabilidade de Dados (GDPR Art. 20)

**Manipulador de Exportação:**
```javascript
async function handlePortabilityRequest(userId, format = 'json') {
  const userData = await collectUserData(userId);

  // Estruturar em formato legível por máquina
  const portableData = {
    exportDate: new Date().toISOString(),
    userId: userId,
    data: {
      profile: userData.profile,
      content: userData.userGeneratedContent,
      settings: userData.preferences,
      history: userData.activityHistory
    }
  };

  // Suportar múltiplos formatos
  if (format === 'csv') {
    return convertToCSV(portableData);
  } else if (format === 'xml') {
    return convertToXML(portableData);
  }

  return portableData; // JSON por padrão
}
```

**Requisitos:**
- Formato estruturado, comumente utilizado, legível por máquina
- Capacidade de transmitir diretamente a outro controlador
- Aplica-se apenas aos dados fornecidos pelo titular de dados
- Apenas para processamento automatizado baseado em consentimento ou contrato

### 4. Direito de Objeção (GDPR Art. 21)

**Manipulador de Objeção:**
```javascript
async function handleObjectionRequest(userId, processingType) {
  switch (processingType) {
    case 'direct_marketing':
      // Deve parar imediatamente
      await disableMarketing(userId);
      await updateConsent(userId, 'marketing', false);
      break;

    case 'legitimate_interest':
      // Avaliar se temos razões imperativas
      const assessment = await assessLegitimateInterest(userId);
      if (!assessment.compelling) {
        await stopProcessing(userId, processingType);
      }
      return assessment;

    case 'profiling':
      await disableProfiling(userId);
      await updateConsent(userId, 'profiling', false);
      break;

    default:
      throw new Error('Invalid processing type');
  }

  await logObjectionRequest(userId, processingType, 'granted');
}
```

## Gestão de Consentimento

### Requisitos de Consentimento (GDPR)

**Consentimento Válido Deve Ser:**
1. Livremente dado (sem coerção)
2. Específico (para cada finalidade)
3. Informado (linguagem clara)
4. Inequívoco (ação afirmativa clara)
5. Revogável (tão fácil de retirar quanto de dar)

**Implementação de Consentimento:**
```html
<!-- Bom: consentimento granular -->
<form>
  <h3>Preferências de Privacidade</h3>

  <label>
    <input type="checkbox" name="essential" checked disabled>
    <strong>Cookies essenciais (Obrigatório)</strong>
    <p>Necessários para a funcionalidade do website</p>
  </label>

  <label>
    <input type="checkbox" name="analytics" value="analytics">
    <strong>Cookies de análise</strong>
    <p>Ajudam-nos a melhorar nosso website coletando dados de uso</p>
  </label>

  <label>
    <input type="checkbox" name="marketing" value="marketing">
    <strong>Cookies de marketing</strong>
    <p>Mostram-lhe anúncios personalizados com base em seus interesses</p>
  </label>

  <button type="submit">Salvar Preferências</button>
  <a href="/privacy-policy">Saiba Mais</a>
</form>
```

**Armazenamento de Registro de Consentimento:**
```javascript
const consentRecord = {
  userId: 'user123',
  timestamp: new Date().toISOString(),
  consentVersion: '2.0',
  purposes: {
    essential: { granted: true, required: true },
    analytics: { granted: true, purpose: 'Website improvement' },
    marketing: { granted: false, purpose: 'Personalized advertising' }
  },
  ipAddress: '192.168.1.1', // Para prova
  userAgent: 'Mozilla/5.0...', // Para contexto
  method: 'explicit_opt_in' // ou 'implicit', 'presumed'
};

await saveConsentRecord(consentRecord);
```

### Banner de Cookies (Em Conformidade com GDPR)

```html
<div id="cookie-banner" role="dialog" aria-labelledby="cookie-title">
  <h2 id="cookie-title">Preferências de Cookie</h2>
  <p>
    Usamos cookies para melhorar sua experiência. Escolha quais cookies
    você permite que usemos. Você pode alterar suas preferências a qualquer momento.
  </p>

  <button onclick="acceptAll()">Aceitar Tudo</button>
  <button onclick="rejectNonEssential()">Rejeitar Não-Essenciais</button>
  <button onclick="showPreferences()">Gerenciar Preferências</button>
</div>

<script>
// Não deve carregar cookies não-essenciais até que o consentimento seja dado
function acceptAll() {
  setConsent({ analytics: true, marketing: true });
  loadAnalyticsCookies();
  loadMarketingCookies();
  hideBanner();
}

function rejectNonEssential() {
  setConsent({ analytics: false, marketing: false });
  hideBanner();
}
</script>
```

## Princípios de Privacidade por Design

### 1. Minimização de Dados

**Princípio:** Coletar apenas dados necessários para a finalidade especificada

**Implementação:**
```javascript
// ❌ Ruim: Coletando dados desnecessários
const userRegistration = {
  email: req.body.email,
  password: req.body.password,
  fullName: req.body.fullName,
  phoneNumber: req.body.phoneNumber, // Não é necessário
  dateOfBirth: req.body.dateOfBirth, // Não é necessário
  address: req.body.address, // Não é necessário
  socialSecurityNumber: req.body.ssn // Definitivamente não é necessário!
};

// ✅ Bom: Apenas dados essenciais
const userRegistration = {
  email: req.body.email,
  password: hashPassword(req.body.password),
  displayName: req.body.displayName // Opcional
};
```

### 2. Limitação de Finalidade

**Princípio:** Usar dados apenas para finalidades especificadas e explícitas

**Implementação:**
```javascript
// Documentar e aplicar finalidade
const dataProcessingPurpose = {
  email: [
    'account_authentication',
    'order_confirmations',
    'password_reset'
  ],
  phoneNumber: [
    'order_delivery_notifications'
    // NÃO: 'marketing_calls' (requer consentimento separado)
  ],
  purchaseHistory: [
    'order_fulfillment',
    'customer_support'
    // NÃO: 'targeted_advertising' (requer consentimento separado)
  ]
};

async function processData(data, purpose) {
  if (!isAllowedPurpose(data.type, purpose)) {
    throw new Error('Purpose not authorized for this data');
  }
  // Proceder com o processamento
}
```

### 3. Limitação de Armazenamento

**Princípio:** Reter dados apenas pelo tempo necessário

**Implementação:**
```javascript
const retentionPolicy = {
  userAccounts: {
    active: 'indefinite',
    inactive: '2 years',
    deleted: '30 days grace period'
  },
  orderRecords: '7 years', // Requisito legal
  supportTickets: '3 years',
  analytics: '26 months',
  marketingData: '1 year or until consent withdrawn'
};

// Exclusão de dados automatizada
async function enforceRetentionPolicy() {
  const now = new Date();

  // Excluir contas inativas
  await User.deleteMany({
    lastActive: { $lt: subYears(now, 2) },
    status: 'inactive'
  });

  // Anonimizar análises antigas
  await Analytics.updateMany(
    { createdAt: { $lt: subMonths(now, 26) } },
    { $unset: { userId: 1, ipAddress: 1 } }
  );

  // Excluir consentimento de marketing expirado
  await MarketingConsent.deleteMany({
    $or: [
      { expiresAt: { $lt: now } },
      { withdrawnAt: { $lt: subDays(now, 30) } }
    ]
  });
}

// Agendar diariamente
cron.schedule('0 2 * * *', enforceRetentionPolicy);
```

## Avaliação de Impacto de Proteção de Dados (DPIA)

**Quando Obrigatória (GDPR Art. 35):**
- Criação de perfil sistemática e extensa
- Processamento em larga escala de dados sensíveis
- Monitoramento sistemático de áreas publicamente acessíveis
- Novas tecnologias com altos riscos de privacidade

**Modelo de DPIA:**
```markdown
# Avaliação de Impacto de Proteção de Dados

## Visão Geral do Processamento
- **Finalidade**: [Descrever a atividade de processamento]
- **Tipos de Dados**: [Categorias de dados pessoais]
- **Titulares de Dados**: [Quem é afetado]
- **Destinatários**: [Quem recebe os dados]

## Avaliação de Necessidade
- [ ] O processamento é necessário para a finalidade declarada?
- [ ] A finalidade poderia ser alcançada com menos dados?
- [ ] O período de retenção é justificado?

## Avaliação de Risco
| Risco | Probabilidade | Severidade | Mitigação |
|-------|---------------|-----------|---------| 
| Violação de dados | Média | Alta | Criptografia, controles de acesso |
| Acesso não autorizado | Baixa | Alta | 2FA, registros de auditoria |
| Mudança de finalidade | Média | Média | Documentação de finalidade, treinamento |

## Salvaguardas
- [ ] Criptografia em repouso e em trânsito
- [ ] Controles de acesso e autenticação
- [ ] Auditorias de segurança regulares
- [ ] Minimização de dados aplicada
- [ ] Políticas de retenção aplicadas
- [ ] DPO consultado
- [ ] Mecanismo de direitos de titulares de dados em vigor

## Conclusão
O processamento é/não é aceitável com as salvaguardas propostas.

Assinado: [Encarregado de Proteção de Dados]
Data: [Data da Avaliação]
```

## Requisitos de Política de Privacidade

**Elementos Essenciais:**
```markdown
# Política de Privacidade

## 1. Identidade do Controlador
Nome da Empresa, Endereço, Informações de Contato
Encarregado de Proteção de Dados: dpo@company.com

## 2. Dados que Coletamos
- Dados de conta: email, nome
- Dados de uso: páginas visitadas, recursos usados
- Dados técnicos: endereço IP, tipo de navegador

## 3. Base Legal para Processamento
- **Consentimento**: Comunicações de marketing
- **Contrato**: Cumprimento de pedidos
- **Interesse Legítimo**: Prevenção de fraude
- **Obrigação Legal**: Registros fiscais

## 4. Como Usamos Seus Dados
- Fornecer serviços solicitados
- Melhorar nossos produtos
- Enviar atualizações importantes
- [Seja específico, evite declarações vagas]

## 5. Compartilhamento de Dados
- Processadores de pagamento (Stripe, PayPal)
- Provedores de envio (FedEx, UPS)
- Análise (Google Analytics)

NÃO vendemos seus dados pessoais.

## 6. Seus Direitos
- Direito de acessar seus dados
- Direito de corrigir imprecisões
- Direito de excluir seus dados
- Direito de se opor ao processamento
- Direito de portabilidade de dados
- Direito de retirar consentimento

Contato: privacy@company.com

## 7. Retenção de Dados
- Dados de conta: Até exclusão da conta + 30 dias
- Histórico de pedidos: 7 anos (requisito legal)
- Dados de marketing: 1 ano ou até opt-out

## 8. Segurança
Usamos medidas de segurança padrão da indústria incluindo
criptografia, servidores seguros e auditorias de segurança regulares.

## 9. Transferências Internacionais
Os dados podem ser transferidos para servidores nos EUA. Usamos
Cláusulas Contratuais Padrão aprovadas pela Comissão da UE.

## 10. Alterações na Política
Última atualização: [Data]
Notificaremos você sobre alterações materiais por email.

## 11. Contato
Dúvidas? Entre em contato com nosso Encarregado de Proteção de Dados em dpo@company.com
```

## Resposta a Incidentes

### Plano de Resposta a Violação de Dados

**Dentro de 72 Horas (GDPR):**
```markdown
1. **Detectar e Contêm** (0-4 horas)
   - Identificar escopo da violação
   - Isolar sistemas afetados
   - Prevenir perda adicional de dados

2. **Avaliar** (4-24 horas)
   - Determinar tipos de dados afetados
   - Identificar número de indivíduos
   - Avaliar risco para direitos e liberdades
   - Documentar tudo

3. **Notificar Autoridade** (24-72 horas)
   - Informar à autoridade supervisora
   - Incluir: natureza, categorias, números aproximados,
     prováveis consequências, medidas tomadas

4. **Notificar Titulares de Dados** (O MAIS RÁPIDO POSSÍVEL se alto risco)
   - Comunicação direta obrigatória
   - Descrever violação em linguagem clara
   - Fornecer recomendações de proteção
```

**Modelo de Notificação de Violação:**
```
Assunto: Aviso Importante de Segurança

Caro [Nome],

Estamos lhe informando sobre um incidente de segurança de dados que
pode ter afetado suas informações pessoais.

O QUE ACONTECEU:
Em [data], descobrimos que [breve descrição].

QUE INFORMAÇÕES FORAM ENVOLVIDAS:
[Listar tipos de dados específicos: nome, email, etc.]
[Listar o que NÃO foi envolvido]

O QUE ESTAMOS FAZENDO:
- [Ações imediatas tomadas]
- [Melhorias de segurança contínuas]
- [Recursos fornecidos aos indivíduos afetados]

O QUE VOCÊ PODE FAZER:
- Altere sua senha imediatamente
- Monitore suas contas para atividades suspeitas
- [Recomendações específicas]

PARA MAIS INFORMAÇÕES:
Entre em contato com nossa linha de atendimento dedicada: [telefone]
Email: security@company.com

Pedimos desculpas sinceras por este incidente e pelo incômodo
que possa causar.

Atenciosamente,
[Nome, Cargo]
```

## Lista de Verificação de Conformidade

### Conformidade com GDPR
- [ ] Base legal documentada para todo processamento
- [ ] Política de privacidade publicada e acessível
- [ ] Mecanismo de consentimento implementa controles granulares
- [ ] Processo de solicitação de direitos de titulares de dados estabelecido
- [ ] Registros de atividades de processamento mantidos
- [ ] Encarregado de Proteção de Dados designado (se obrigatório)
- [ ] DPIA conduzida para processamento de alto risco
- [ ] Procedimento de notificação de violação de dados em vigor
- [ ] Contratos de fornecedores incluem acordos de processamento de dados
- [ ] Salvaguardas de transferência de dados internacional implementadas
- [ ] Treinamento de equipe sobre proteção de dados concluído

### Conformidade com CCPA
- [ ] Link "Não Vender Meus Dados Pessoais" na página inicial
- [ ] Política de privacidade divulga coleta e venda de dados
- [ ] Mecanismos para solicitações verificáveis de consumidor
- [ ] Processo para solicitações de opt-out (resposta em 48 horas)
- [ ] Relatório anual sobre solicitações e conformidade
- [ ] Acordos de prestador de serviço atualizados
- [ ] Aviso de coleta fornecido

### Conformidade com HIPAA
- [ ] Avaliação de risco concluída
- [ ] Políticas e procedimentos de segurança documentados
- [ ] Equipe treinada em requisitos de HIPAA
- [ ] Contratos de Associado Comercial assinados
- [ ] Controles de acesso e registros de auditoria implementados
- [ ] Criptografia para ePHI
- [ ] Procedimentos de notificação de violação estabelecidos
- [ ] Plano de contingência e recuperação de desastre

A conformidade com privacidade é um processo contínuo, não uma lista de verificação única. Revise e atualize regularmente as práticas conforme as regulamentações evoluem e seu processamento de dados muda.