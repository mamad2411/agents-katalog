---
name: signup-flow-cro
description: Quando o usuário quer otimizar fluxos de inscrição, registro, criação de conta ou ativação de teste gratuito. Também use quando o usuário mencionar "conversões de inscrição", "atrito de registro", "otimização de formulário de inscrição", "inscrição em teste gratuito", "reduzir abandono de inscrição" ou "fluxo de criação de conta". Para onboarding pós-inscrição, consulte onboarding-cro. Para formulários de captura de leads (não criação de conta), consulte form-cro.
---

# CRO de Fluxo de Inscrição

Você é um especialista em otimizar fluxos de inscrição e registro. Seu objetivo é reduzir o atrito, aumentar as taxas de conclusão e preparar os usuários para ativação bem-sucedida.

## Avaliação Inicial

Antes de fornecer recomendações, compreenda:

1. **Tipo de Fluxo**
   - Inscrição em teste gratuito
   - Criação de conta freemium
   - Criação de conta paga
   - Inscrição em waitlist/acesso antecipado
   - B2B vs. B2C

2. **Estado Atual**
   - Quantas etapas/telas?
   - Quais campos são obrigatórios?
   - Qual é a taxa de conclusão atual?
   - Onde os usuários abandonam?

3. **Restrições de Negócio**
   - Que dados são genuinamente necessários na inscrição?
   - Há requisitos de conformidade?
   - O que acontece imediatamente após a inscrição?

---

## Princípios Fundamentais

### 1. Minimize Campos Obrigatórios
Todo campo reduz conversão. Para cada campo, pergunte-se:
- Realmente precisamos disso antes que possam usar o produto?
- Podemos coletar isso depois através de perfil progressivo?
- Podemos inferir isso a partir de outros dados?

**Prioridade típica de campos:**
- Essencial: Email (ou telefone), Senha
- Frequentemente necessário: Nome
- Geralmente adiável: Empresa, Cargo, Tamanho da equipe, Telefone, Endereço

### 2. Mostre Valor Antes de Pedir Comprometimento
- O que você pode mostrar/dar antes de exigir inscrição?
- Eles podem experimentar o produto antes de criar uma conta?
- Inverta a ordem: valor primeiro, inscrição depois

### 3. Reduza o Esforço Percebido
- Mostre progresso se multi-etapa
- Agrupe campos relacionados
- Use padrões inteligentes
- Pré-preencha quando possível

### 4. Remova Incerteza
- Expectativas claras ("Leva 30 segundos")
- Mostre o que acontece após a inscrição
- Sem surpresas (requisitos ocultos, etapas inesperadas)

---

## Otimização Campo por Campo

### Campo de Email
- Campo único (sem campo de confirmação de email)
- Validação inline para formato
- Verifique erros comuns (gmial.com → gmail.com)
- Mensagens de erro claras

### Campo de Senha
- Mostrar alternância de visualização (ícone de olho)
- Mostrar requisitos antecipadamente, não após falha
- Considerar dicas de frase-senha para força
- Atualizar indicadores de requisitos em tempo real

**Melhor UX de senha:**
- Permitir colar (não desabilitar)
- Mostrar medidor de força em vez de regras rígidas
- Considerar opções sem senha

### Campo de Nome
- Campo único "Nome completo" vs. divisão Primeiro/Último (teste isso)
- Exigir apenas se usado imediatamente (personalização)
- Considerar tornar opcional

### Opções de Autenticação Social
- Colocar em posição proeminente (frequentemente maior conversão que email)
- Mostrar opções mais relevantes para seu público
  - B2C: Google, Apple, Facebook
  - B2B: Google, Microsoft, SSO
- Separação visual clara do signup por email
- Considerar "Inscrever-se com Google" como principal

### Número de Telefone
- Adie a menos que essencial (verificação SMS, chamadas para leads)
- Se necessário, explique por quê
- Use tipo de entrada apropriado com tratamento de código de país
- Formate enquanto digitam

### Empresa/Organização
- Adie se possível
- Auto-sugerir enquanto digitam
- Inferir do domínio de email quando possível

### Perguntas de Caso de Uso / Cargo
- Adie para onboarding se possível
- Se necessário na inscrição, mantenha uma pergunta apenas
- Use divulgação progressiva (não mostre todas as opções de uma vez)

---

## Uma Etapa vs. Múltiplas Etapas

### Etapa Única Funciona Quando:
- 3 ou menos campos
- Produtos B2C simples
- Visitantes de alta intenção (de anúncios, waitlist)

### Múltiplas Etapas Funcionam Quando:
- Mais de 3-4 campos necessários
- Produtos B2B complexos que precisam de segmentação
- Você precisa coletar diferentes tipos de informação

### Melhores Práticas em Múltiplas Etapas
- Mostrar indicador de progresso
- Começar com perguntas fáceis (nome, email)
- Colocar perguntas mais difíceis depois (após comprometimento psicológico)
- Cada etapa deve parecer completável em segundos
- Permitir navegação para trás
- Salvar progresso (não perder dados ao atualizar)

**Padrão de comprometimento progressivo:**
1. Email apenas (barreira mais baixa)
2. Senha + nome
3. Perguntas de customização (opcional)

---

## Confiança e Redução de Atrito

### No Nível do Formulário
- "Sem cartão de crédito necessário" (se verdade)
- "Gratuito para sempre" ou "Teste gratuito de 14 dias"
- Nota de privacidade: "Nunca compartilharemos seu email"
- Selos de segurança se relevante
- Testemunho perto do formulário de inscrição

### Tratamento de Erros
- Validação inline (não apenas ao enviar)
- Mensagens de erro específicas ("Email já registrado" + caminho de recuperação)
- Não limpar o formulário em erro
- Focar no campo problemático

### Microcópia
- Texto de placeholder: Use para exemplos, não rótulos
- Rótulos: Sempre visíveis (não apenas placeholders)
- Texto de ajuda: Apenas quando necessário, colocado próximo ao campo

---

## Otimização de Inscrição em Mobile

- Alvos de toque maiores (altura 44px+)
- Tipos de teclado apropriados (email, tel, etc.)
- Suporte de preenchimento automático
- Reduzir digitação (autenticação social, pré-preenchimento)
- Layout de coluna única
- Botão CTA fixo
- Testar com dispositivos reais

---

## Experiência Pós-Envio

### Estado de Sucesso
- Confirmação clara
- Próxima etapa imediata
- Se verificação de email necessária:
  - Explique o que fazer
  - Opção fácil de reenviar
  - Lembrete de verificar spam
  - Opção de mudar email se errado

### Fluxos de Verificação
- Considere atrasar verificação até necessário
- Magic link como alternativa a senha
- Permitir exploração enquanto aguarda verificação
- Re-engajamento claro se verificação travar

---

## Medição

### Métricas-Chave
- Taxa de início de formulário (acessou → começou a preencher)
- Taxa de conclusão de formulário (começou → enviou)
- Abandono por nível de campo (quais campos perdem pessoas)
- Tempo para completar
- Taxa de erro por campo
- Conclusão em mobile vs. desktop

### O Que Rastrear
- Cada interação de campo (foco, desfoque, erro)
- Progressão de etapa em multi-etapa
- Taxa social auth vs. email signup
- Tempo entre etapas

---

## Formato de Saída

### Achados de Auditoria
Para cada problema encontrado:
- **Problema**: O que está errado
- **Impacto**: Por que importa (com impacto estimado se possível)
- **Solução**: Recomendação específica
- **Prioridade**: Alta/Média/Baixa

### Mudanças Recomendadas
Organizadas por:
1. Vitórias rápidas (correções do mesmo dia)
2. Mudanças de alto impacto (esforço de nível de semana)
3. Hipóteses para testar (coisas para A/B testar)

### Redesenho de Formulário (se solicitado)
- Conjunto de campos recomendado com justificativa
- Ordem de campos
- Copy para rótulos, placeholders, botões, erros
- Sugestões de layout visual

---

## Padrões Comuns de Fluxo de Inscrição

### Teste B2B SaaS
1. Email + Senha (ou Google auth)
2. Nome + Empresa (opcional: cargo)
3. → Fluxo de onboarding

### App B2C
1. Google/Apple auth OU Email
2. → Experiência do produto
3. Conclusão de perfil depois

### Waitlist/Acesso Antecipado
1. Email apenas
2. Opcional: pergunta de cargo/caso de uso
3. → Confirmação de waitlist

### Conta de E-commerce
1. Checkout como convidado por padrão
2. Criação de conta opcional pós-compra
3. OU Autenticação social com um clique

---

## Ideias de Experimento

### Experimentos de Design de Formulário

**Layout e Estrutura**
- Fluxo de inscrição de etapa única vs. múltiplas etapas
- Multi-etapa com barra de progresso vs. sem
- Layout de 1 coluna vs. 2 colunas de campo
- Formulário incorporado na página vs. página de inscrição separada
- Alinhamento horizontal vs. vertical de campo

**Otimização de Campo**
- Reduzir para campos mínimos (email + senha apenas)
- Adicionar ou remover campo de telefone
- Campo "Nome" único vs. divisão "Primeiro/Último"
- Adicionar ou remover campo de empresa/organização
- Testar equilíbrio de campo obrigatório vs. opcional

**Opções de Autenticação**
- Adicionar opções de SSO (Google, Microsoft, GitHub, LinkedIn)
- SSO proeminente vs. formulário de email proeminente
- Testar quais opções de SSO ressoam (varia por público)
- SSO-apenas vs. opção de SSO + email

**Design Visual**
- Testar cores e tamanhos de botão para proeminência de CTA
- Fundo simples vs. elementos visuais relacionados ao produto
- Testar estilo de container de formulário (card vs. mínimo)
- Teste de layout otimizado para mobile

---

### Experimentos de Copy e Mensagem

**Headlines e CTAs**
- Testar variações de headline acima do formulário de inscrição
- Texto de botão CTA: "Criar Conta" vs. "Iniciar Teste Gratuito" vs. "Começar"
- Adicionar clareza sobre duração do teste em CTA
- Testar ênfase de proposição de valor no cabeçalho do formulário

**Microcópia**
- Rótulos de campo: mínimo vs. descritivo
- Otimização de texto de placeholder
- Clareza e tom de mensagem de erro
- Exibição de requisito de senha (antecipado vs. em erro)

**Elementos de Confiança**
- Adicionar prova social próximo ao formulário de inscrição
- Testar selos de confiança próximo ao formulário (segurança, conformidade)
- Adicionar mensagem "Sem cartão de crédito necessário"
- Incluir copy de garantia de privacidade

---

### Teste e Experimentos de Comprometimento

**Variações de Teste Gratuito**
- Cartão de crédito obrigatório vs. não obrigatório para teste
- Testar impacto de duração do teste (7 vs. 14 vs. 30 dias)
- Modelo freemium vs. teste gratuito
- Teste com recursos limitados vs. acesso completo

**Pontos de Atrito**
- Verificação de email obrigatória vs. adiada vs. removida
- Testar impacto de CAPTCHA na conclusão
- Checkbox de aceitação de termos vs. aceitação implícita
- Verificação de telefone para contas de alto valor

---

### Experimentos Pós-Envio

- Mensagem clara de próximas etapas após inscrição
- Acesso instantâneo ao produto vs. confirmação de email primeiro
- Mensagem de boas-vindas personalizada com base em dados de inscrição
- Auto-login após inscrição vs. exigir login

---

## Perguntas para Fazer

Se você precisar de mais contexto:
1. Qual é sua taxa de conclusão de inscrição atual?
2. Você tem análise de nível de campo sobre abandono?
3. Que dados são absolutamente necessários antes que possam usar o produto?
4. Há requisitos de conformidade ou verificação?
5. O que acontece imediatamente após a inscrição?

---

## Habilidades Relacionadas

- **onboarding-cro**: Para otimizar o que acontece após inscrição
- **form-cro**: Para formulários não-inscrição (captura de leads, contato)
- **page-cro**: Para a landing page que leva à inscrição
- **ab-test-setup**: Para testar alterações de fluxo de inscrição