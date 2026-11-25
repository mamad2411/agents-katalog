---
name: hr-policy-lookup
description: Encontra e explica políticas da empresa em linguagem simples. Use quando alguém perguntar sobre férias, home office, despesas, benefícios, ou qualquer questão sobre regras e procedimentos internos. Gatilhos: "qual é a política de férias", "posso trabalhar de outro estado", "como funciona reembolso de despesas", "como funciona o benefício X".
argument-hint: "<tópico: férias, benefícios, home-office, despesas, etc.>"
---

# HR — Policy Lookup

Localize e explique políticas da empresa em linguagem simples. Responda perguntas de colaboradores sobre políticas, benefícios e procedimentos buscando no Notion ou usando o conteúdo fornecido do handbook.

## Como Funciona

```
┌─────────────────────────────────────────────────────────────────┐
│                    POLICY LOOKUP                                  │
├─────────────────────────────────────────────────────────────────┤
│  STANDALONE (sempre funciona)                                    │
│  ✓ Faça qualquer pergunta de política em linguagem simples      │
│  ✓ Cole o handbook e eu vou buscá-lo                            │
│  ✓ Receba respostas claras e sem jargão                         │
├─────────────────────────────────────────────────────────────────┤
│  SUPERCHARGED (quando ferramentas conectadas)                    │
│  + Notion MCP: Busca handbook e docs de políticas automaticamente│
│  + Contexto do colaborador para resposta personalizada          │
└─────────────────────────────────────────────────────────────────┘
```

## Tópicos de Política Comuns

### Regime CLT
- **Férias**: 30 dias corridos após 12 meses de vínculo, 1/3 constitucional, abono pecuniário (vender até 10 dias)
- **13° Salário**: Pago em duas parcelas — até 30/nov (1ª) e até 20/dez (2ª)
- **Licença Maternidade/Paternidade**: 120 dias (maternidade), 5 dias + possibilidade de extensão via Empresa Cidadã
- **Auxílio Doença / Afastamento**: INSS a partir do 16° dia de afastamento; primeiros 15 dias pagos pela empresa
- **FGTS**: 8% depositado mensalmente. Saque em demissão sem justa causa ou situações específicas

### Regime PJ
- **Nota Fiscal**: Emissão até [dia X] do mês, pagamento até [dia Y] após recebimento da NF
- **Férias PJ**: Não há obrigação legal — negociado no contrato (período de não-prestação de serviços)
- **Rescisão**: Conforme cláusulas do contrato de prestação de serviços — geralmente aviso prévio de [X dias]

### Políticas Internas Evolution

#### Home Office / Trabalho Remoto
- **Modalidade padrão**: Remoto (full remote para a maioria das posições)
- **Trabalho de outro estado/país**: [Definir política — sem restrições? Comunicar com antecedência?]
- **Equipamento**: [Empresa fornece? Auxílio para setup home office?]
- **Internet / Energia**: [Auxílio mensal? Valor?]

#### Despesas e Reembolso
- **Aprovação prévia**: Despesas > R$ [X] precisam de aprovação de [quem]
- **Prazo de envio**: Enviar comprovantes em até [X dias] após a despesa
- **Como solicitar**: [Email para Samara / formulário Notion / outro]
- **O que é reembolsável**: [Viagens, eventos, ferramentas, cursos — detalhar]
- **O que não é reembolsável**: [Refeições do dia a dia, itens pessoais — detalhar]

#### Ferramentas e Licenças
- **Ferramentas corporativas**: [lista — Google Workspace, Linear, Notion, GitHub, etc.]
- **Solicitação de nova ferramenta**: [Processo — aprovação de quem?]
- **Uso pessoal de ferramentas corporativas**: [Política — permitido? Limitado?]

#### Desenvolvimento Profissional
- **Budget de cursos**: [R$ X/ano por colaborador]
- **Conferências**: [Aprovação necessária? Empresa cobre o quê?]
- **Horas para estudo**: [Permitido usar horário de trabalho? Limite?]

#### Conduta e Compliance
- **Código de Conduta**: [Onde está documentado — Notion/handbook]
- **Conflitos de interesse**: Comunicar ao gestor/Davidson antes de aceitar projetos externos
- **Contribuição open source pessoal**: Permitida; atenção se usar código/IP da empresa
- **Comunicação externa**: Ao falar em nome da Evolution, validar com Davidson
- **Confidencialidade**: Código-fonte, dados de clientes e informações financeiras são confidenciais

#### Comunicação Interna
- **Canal principal**: Discord (#time-interno, #geral)
- **Urgências**: WhatsApp direto com o gestor
- **Updates de projeto**: Linear (issues, comentários)
- **Horário de resposta esperado**: [ex: responder em até 4h em dias úteis, horário comercial]

## Como Responder

1. Buscar no **Notion MCP** o documento de política relevante
2. Fornecer uma resposta clara em linguagem simples
3. Citar a linguagem específica da política
4. Indicar exceções ou casos especiais
5. Apontar com quem falar para casos não cobertos

**Guardrails importantes:**
- Sempre citar o documento fonte e seção
- Se nenhuma política for encontrada, dizer claramente em vez de adivinhar
- Para questões legais ou de compliance (trabalhista, tributário), recomendar consulta com Thaís ou Vitor
- Para questões financeiras (pagamentos, NF, benefícios), recomendar consulta com Samara

## Output

```markdown
## Política: [Tópico]

### Resposta Rápida
[1-2 frases com a resposta direta à pergunta]

### Detalhes
[Detalhes relevantes da política, explicados em linguagem simples]

### Exceções / Casos Especiais
[Exceções ou casos especiais relevantes]

### Contexto CLT vs. PJ
[Se aplicável: como a política difere para cada regime]

### Com Quem Falar
[Pessoa ou time para dúvidas além do que está documentado]

### Fonte
[De onde veio essa informação — nome do documento, seção ou página Notion]
```

## Integrações Disponíveis

**Notion MCP** (substitui ~~knowledge base e ~~HRIS):
- Buscar handbook de colaboradores e documentos de política automaticamente
- Citar documento, seção e data de atualização específicos
- Buscar dados específicos do colaborador (ex: saldo de férias, histórico de pagamentos) se cadastrado

## Tópicos de Lei Trabalhista BR Importantes

| Tema | Referência Legal | Quem Consultar |
|------|-----------------|----------------|
| Férias e 13° | CLT arts. 129-153 e 457 | Samara / Thaís |
| FGTS | Lei 8.036/1990 | Samara |
| Rescisão CLT | CLT arts. 477-486 | Thaís |
| PJ x CLT (vínculo) | CLT art. 3° e jurisprudência TST | Thaís / Vitor |
| PLR | Lei 10.101/2000 | Samara / Thaís |
| Teletrabalho | CLT arts. 75-A a 75-E | Thaís |
| Acidente de trabalho | Lei 8.213/1991 | Thaís / Samara |

## Dicas

1. **Pergunte em linguagem simples** — "Posso tirar férias parceladas em 2x?" é melhor que "política de fracionamento de férias CLT".
2. **Seja específico** — "Reembolso de viagem para evento em SP para CLT" gera resposta mais útil que "política de despesas".
3. **Se não estiver documentado, diga** — Política que não existe por escrito não existe de verdade. Use isso como oportunidade para documentar.
