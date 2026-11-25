---
name: zapier-workflows
description: Gerencie e acione fluxos de trabalho pré-construídos do Zapier e orquestração de ferramentas MCP. Use quando o usuário mencionar workflows, Zaps, automações, resumo diário, pesquisa, busca, rastreamento de leads, despesas, ou pedir para "executar" qualquer processo. Também trata pesquisa baseada em Perplexity e rastreamento de dados no Google Sheets.
---

# Skill de Workflows do Zapier

## O Problema Que Isto Resolve

**O Zapier MCP dá ao Claude acesso a 8.000+ ferramentas individuais** (cada ação do Zapier), mas existem limitações críticas:

❌ **Sem memória** - Claude não lembra quais ferramentas VOCÊ usa ou por quê
❌ **Sem contexto** - Não sabe quando usar ferramentas específicas para seus workflows
❌ **Apenas ações isoladas** - Não consegue acionar seus Zaps complexos e multi-etapas
❌ **Novo começo a cada sessão** - Todo contexto perdido entre conversas

### Os Dois Tipos de Automação do Zapier

**1. Ferramentas MCP (Ações Isoladas)**
- Ações individuais do Zapier (Adicionar linha à planilha, Enviar email, etc.)
- Disponíveis via Zapier MCP em https://mcp.zapier.com/mcp/servers
- Ótimo para automação flexível e improvisada
- **Problema:** 8.000+ opções sem orientação sobre qual usar ou quando

**2. Zaps Multi-Etapas (Acionados por Webhook)**
- Workflows complexos que você construiu no dashboard do Zapier
- Múltiplas ações encadeadas, pré-otimizadas
- Acionadas via URL de webhook (requisição POST)
- **Problema:** Claude não consegue acionar estas - não estão no MCP

## O Que Esta Skill Faz

**Esta skill resolve ambos os problemas** ao dar ao Claude memória persistente para seus workflows do Zapier:

✅ **Lembra suas preferências de ferramentas MCP** - "Use Google Sheets para despesas, Notion para tarefas"
✅ **Sabe quando/por que usar cada ferramenta** - "Pesquise com Perplexity ao pesquisar, não Google"
✅ **Aciona Zaps multi-etapas** - "Execute meu resumo diário" = POST de webhook para seu Zap complexo
✅ **Auto-aprendizado** - Claude atualiza a skill conforme você ensina, nunca esquece
✅ **Persistência entre sessões** - Funciona em todas as conversas (instalação global)

### O Que Você Consegue

**Para Zaps Multi-Etapas:**
- Armazene URLs de webhook e o que fazem
- Acione workflows complexos apenas pedindo
- Lembre quando/por que usar cada Zap
- Documente custos, timing, outputs

**Para Ferramentas MCP:**
- Documente quais ferramentas você prefere para quais tarefas
- Construa padrões de workflow reutilizáveis
- Armazene preferências específicas das ferramentas (nomes de planilhas, formatos, etc.)
- Crie sequências de orquestração multi-ferramenta

**Auto-Aprendizado:**
- Claude atualiza automaticamente os arquivos da skill quando você ensina
- Mudanças persistem para sempre (instalação global) ou por projeto (instalação local)
- Sem edição manual necessária - apenas converse com Claude

## Instalação e Configuração

### Local de Instalação

**Global (`~/.claude/skills/`) - RECOMENDADO:**
- Padrões aprendidos persistem em TODOS os projetos
- Uma biblioteca de Zap para tudo
- Preferências se transferem para todos os projetos

**Nível de projeto (`./.claude/skills/`):**
- Padrões aprendidos APENAS neste projeto
- Isolado de outros projetos
- Útil para workflows específicos do projeto

### ⚠️ Aviso de Segurança

**IMPORTANTE:** Esta skill armazena URLs de webhook e detalhes de workflow em arquivos de texto simples.

**URLs de webhook contêm tokens de autenticação.** Se alguém tiver sua URL de webhook, pode acionar seus Zaps.

**Melhores práticas:**
- ✅ Instale globalmente em `~/.claude/skills/` (não em repos de projeto)
- ✅ Adicione `.claude/` ao seu `.gitignore` se instalado em um projeto
- ✅ Nunca faça commit de arquivos de skill com URLs reais de webhook em repos públicos
- ✅ Regenere URLs de webhook se acidentalmente expostas
- ✅ Use recursos de autenticação de webhook do Zapier quando disponível

**Se você precisar compartilhar esta skill:**
- Remova URLs reais de webhook primeiro
- Substitua por exemplos de placeholder
- Ou use URLs de webhook separadas para compartilhamento/teste

### Pré-requisitos

**Obrigatório:**
- Claude Code
- Conta Zapier (para webhooks e ferramentas MCP)

**Opcional:**
- Ferramentas MCP adicionais baseadas em seus workflows (Perplexity Search, Google Sheets, etc.)

### Configurando Zapier MCP

Para conectar as ferramentas MCP do Zapier ao Claude Code:

1. **Vá para servidores Zapier MCP:**
   - Visite https://mcp.zapier.com/mcp/servers
   - Faça login em sua conta Zapier se solicitado

2. **Crie um novo servidor MCP:**
   - Clique no botão "New MCP Server" (canto superior esquerdo)
   - No dropdown "MCP Client (required)", selecione **Claude Code**
   - Dê um nome ao seu servidor (ex: "Minhas Ferramentas Zapier")

3. **Adicione ferramentas:**
   - Clique no botão "Add tools"
   - Selecione quantas ações do Zapier você quiser (cada uma vira uma ferramenta MCP)
   - Ferramentas comuns: Run Zap, Add Row to Google Sheets, Send Email, etc.

4. **Conecte ao Claude Code:**
   - Clique no botão "Connect"
   - Você verá um comando assim:
   ```bash
   claude mcp add zapier https://mcp.zapier.com/api/mcp/mcp -t http -H "Authorization: Bearer ZjFmZGJkN..................1NjBhYzc2MDRlYg=="
   ```
   - Copie e execute este comando no seu terminal

5. **Reinicie o Claude Code:**
   - Feche e reabra o Claude Code
   - Suas ferramentas Zapier MCP agora estão disponíveis

**Dica:** Você pode adicionar mais ferramentas depois editando seu servidor MCP no Zapier e executando o comando de conexão novamente.

### Criando Zaps Acionados por Webhook

Para workflows pré-construídos e otimizados que você quer acionar sob demanda:

1. **No dashboard do Zapier:**
   - Crie um novo Zap
   - Escolha "Webhooks by Zapier" como trigger
   - Selecione "Catch Hook"
   - Copie a URL de webhook fornecida

2. **Construa seu workflow:**
   - Adicione qualquer ação que desejar (chamadas API, processamento de dados, etc.)
   - Teste e otimize o Zap

3. **Documente nesta skill:**
   - Conte ao Claude sobre o novo Zap (URL de webhook, o que faz, frases de acionamento)
   - Claude adicionará automaticamente a `references/zaps.md`
   - Agora você pode acioná-lo apenas pedindo ao Claude!

**Webhook vs Ferramentas MCP:**
- **Webhooks:** Zaps multi-etapas pré-construídos que você aciona com uma requisição POST. Ótimo para workflows complexos e otimizados.
- **Ferramentas MCP:** Ações individuais do Zapier chamadas diretamente. Ótimo para automação flexível e improvisada.

## Protocolo de Auto-Melhoria

**CRÍTICO: Esta skill pode e deve se editar para aprender com o feedback do usuário.**

Quando o usuário ensina algo novo ou corrige sua abordagem:

1. **Identifique o que atualizar:**
   - Novo Zap para documentar → Edite `references/zaps.md`
   - Preferência de ferramenta MCP → Edite `references/mcp-patterns.md`
   - Novo padrão de workflow → Edite `references/mcp-patterns.md`

2. **Faça a edição usando ferramentas Claude Code:**
   - Leia o arquivo primeiro com a ferramenta **Read**
   - Atualize com a ferramenta **Edit** (especifique exato `old_string` e `new_string`)
   - Confirme a mudança ao usuário

3. **Formato de atualização:**
   ```markdown
   User: "Use Apollo em vez de Clearbit para dados da empresa"
   Claude: [usa ferramenta Read em references/mcp-patterns.md]
           [usa ferramenta Edit para atualizar a preferência]
           "Atualizado! Usarei Apollo para enriquecimento de empresa a partir de agora.
            Esta mudança agora é permanente na skill."
   ```

**O que capturar em atualizações de skill:**
- ✅ Preferências de ferramenta (qual ferramenta para qual tarefa)
- ✅ Sequências de workflow (padrões passo a passo)
- ✅ Abordagens de tratamento de erros
- ✅ Requisitos de formatação de dados
- ✅ Novos Zaps e seus detalhes
- ❌ Pedidos únicos (não entupa a skill)
- ❌ Contexto temporário (use memória em vez disso)

## Lógica de Decisão

### Quando Usar Zaps Acionados por Webhook

Use webhooks quando:
- A tarefa é complexa, multi-etapas e já foi refinada
- O usuário menciona um nome específico de Zap (verifique `references/zaps.md`)
- A execução determinística é crítica
- A tarefa envolve 5+ chamadas API ou orquestração complexa
- Eficiência de custo/tempo importa (Zaps pré-construídos são otimizados)

### Quando Usar Orquestração de Ferramentas MCP

Use ferramentas MCP quando:
- A tarefa é simples (1-3 ações)
- Flexibilidade é necessária (parâmetros mudam)
- Testando um novo padrão de workflow
- O usuário explicitamente pede para usar ferramentas MCP específicas

## Padrão de Execução

1. **Escute triggers:** Nomes de workflow, "executar", "acionar", "pesquisar", "pesquisa", etc.
2. **Verifique referências:** Use ferramenta Read no arquivo de referência apropriado para detalhes
3. **Verifique pré-requisitos:**
   - **Se ferramentas MCP são necessárias mas não disponíveis:** Forneça instruções de configuração Zapier MCP (veja abaixo)
   - **Se ferramentas MCP disponíveis mas não documentadas:** Acione protocolo de descoberta de ferramentas (veja abaixo)
   - **Se URL de webhook é necessária mas não está em referências:** Forneça instruções de extração de webhook (veja abaixo)
4. **Execute:**
   - **Para Zaps acionados por webhook:** Use ferramenta Bash com curl para fazer POST para URL de webhook (webhooks são criados no dashboard Zapier com trigger "Catch Hook")
   - **Para workflows de ferramentas MCP:** Chame a ferramenta Zapier MCP apropriada diretamente (configurada via https://mcp.zapier.com/mcp/servers)
5. **Confirme:** Conte ao usuário o que aconteceu em linguagem natural
6. **Aprenda:** Se o usuário o corrige, use ferramenta Edit para atualizar arquivos da skill
7. **Sugira salvamento de padrão:** Depois de usar ferramenta com sucesso, ofereça-se para salvar o padrão (veja abaixo)

## Detecção Proativa de Padrões e Aprendizado

**CRÍTICO:** Depois de ajudar com sucesso o usuário com ferramentas MCP ou workflows, sugira proativamente economizar padrões valiosos.

### Quando Sugerir Salvamento de Padrões

Depois de completar uma tarefa usando ferramentas MCP, verifique se isto é um padrão que vale a pena guardar:

**Procure por:**
- Sequências multi-ferramenta que funcionaram bem
- Combinações de parâmetros específicos que o usuário gostou
- Workflows repetidos ou casos de uso
- Preferências de ferramenta que o usuário expressou durante a tarefa
- Soluções bem-sucedidas para problemas do usuário

**Sugira guardar se:**
- Você usou 2+ ferramentas MCP em sequência
- O usuário expressou satisfação com o resultado
- Isto parece algo que o usuário poderia repetir
- O usuário deu preferências específicas durante a interação

### Como Sugerir Salvamento de Padrão

Depois de completar a tarefa com sucesso:

```
"Funcionou bem! Percebi que eu [descreva o que você fez, ex: 'usei Perplexity para pesquisar, depois salvei resultados no Google Sheets'].

Você gostaria que eu salvasse isto como um padrão? Se você me disser:
- Que palavras de acionamento devo escutar
- Quando/por que usar este workflow
- Qualquer preferência ou variação

Vou lembrar e faço isto automaticamente próxima vez!"
```

### Documente o Padrão

Se o usuário disser sim:
1. Use ferramenta Read em `references/mcp-patterns.md`
2. Use ferramenta Edit para adicionar novo padrão com:
   - Nome do padrão
   - Frases de acionamento
   - Quando/por que usá-lo
   - Workflow passo a passo
   - Parâmetros/preferências
   - Exemplo
3. Confirme: "Guardado! Próxima vez que você [acionamento], vou [workflow]."

**Exemplos de padrões que valem a pena guardar:**
- "Pesquisar e documentar" (Perplexity → resumir → Google Sheets)
- "Rastreamento de despesas" (Extrair valor/descrição → formatar → adicionar à planilha)
- "Análise competitiva" (Pesquisar competidor → analisar → guardar insights)
- "Briefing diário" (Múltiplas pesquisas → sintetizar → entregar)

**Não guarde:**
- Pedidos únicos
- Situações altamente específicas/únicas
- Usos simples de ferramenta única (a menos que o usuário peça)

## Detecção de Configuração e Instruções

### Se Zapier MCP Não For Detectado

Quando o usuário solicita funcionalidade de ferramentas MCP mas Zapier MCP não está conectado, diga:

```
"Não vejo as ferramentas Zapier MCP conectadas. Eis como configurar:

1. Vá para https://mcp.zapier.com/mcp/servers
2. Faça login em sua conta Zapier
3. Clique em 'New MCP Server' (canto superior esquerdo)
4. Selecione 'Claude Code' no dropdown MCP Client
5. Dê um nome (ex: 'Minhas Ferramentas Zapier')
6. Clique em 'Add tools' e selecione as ações Zapier que quer
7. Clique em 'Connect' e copie o comando mostrado
8. Execute esse comando no seu terminal (fica assim):
   claude mcp add zapier https://mcp.zapier.com/api/mcp/mcp -t http -H "Authorization: Bearer [seu-token]"
9. Reinicie o Claude Code

Uma vez configurado, vou conseguir usar essas ações Zapier diretamente!"
```

### Quando Zapier MCP Está Conectado - Descoberta de Ferramentas e Documentação

**IMPORTANTE:** Quando Zapier MCP está conectado (ferramentas começando com `mcp__zapier__` estão disponíveis), ajude proativamente o usuário a documentá-las com contexto rico:

1. **Liste ferramentas disponíveis:**
   - Verifique quais ferramentas Zapier MCP estão disponíveis
   - Liste-as para o usuário

2. **Solicite documentação detalhada:**
   ```
   "Vejo que você tem essas ferramentas Zapier MCP disponíveis:
   - mcp__zapier__google_sheets_create_spreadsheet_row
   - mcp__zapier__perplexity_chat_completion
   - [etc.]

   Para me ajudar a usá-las efetivamente, preciso entender:

   Para cada ferramenta que você quer que eu use, por favor me conte:

   1. QUANDO devo usar esta ferramenta?
      - Que palavras de acionamento ou frases?
      - Que situações ou contextos?
      - Que tipos de pedidos?

   2. POR QUE devo usar esta ferramenta vs alternativas?
      - Para o que é melhor?
      - Quando eu NÃO deveria usá-la?

   3. COMO devo usá-la?
      - Algum parâmetro ou preferência específica?
      - Valores padrão que devo usar?
      - Nomes de planilhas, formatos, ou outros específicos?

   4. Algum PADRÃO ou workflow envolvendo esta ferramenta?
      - Sequências multi-etapas?
      - Combinações comuns com outras ferramentas?

   Pode ser à vontade - quanto mais detalhe você me der, melhor consigo servir você!"
   ```

3. **Documente na skill:**
   - Use ferramenta Read em `references/mcp-patterns.md`
   - Use ferramenta Edit para adicionar documentação compreensiva:
     - Nome e propósito da ferramenta
     - Frases de acionamento (quando)
     - Casos de uso (por quê)
     - Parâmetros e preferências (como)
     - Padrões de workflow se mencionados
   - Confirme ao usuário o que foi documentado

**Quando acionar isto:**
- Primeira vez que usuário menciona Zapier ou workflows após configuração MCP
- Usuário explicitamente pergunta "que ferramentas tenho?" ou "o que consigo fazer com Zapier?"
- Quando você detecta novas ferramentas Zapier MCP que não estão documentadas em `references/mcp-patterns.md`

### Se Usuário Quer Adicionar um Zap Acionado por Webhook

Quando o usuário menciona criar ou adicionar um Zap multi-etapas para acionamento por webhook, forneça essas instruções:

```
"Para obter sua URL de webhook de um Zap existente:

1. Vá para seu Zap no dashboard do Zapier
2. Certifique-se de que o trigger é um node 'Webhooks by Zapier'
3. No dropdown 'Trigger Event', selecione 'Catch Hook'
4. Vá para a aba 'Test'
5. Copie a 'Webhook URL' mostrada
6. Me dê essa URL e conte:
   - O que o Zap faz (passo a passo)
   - Que frases de acionamento você quer usar
   - Qualquer outro detalhe (timing, custo, etc.)

Vou adicionar ao meu conhecimento para que você consiga acioná-lo qualquer hora apenas pedindo!"
```

## Referência Rápida

- **Todos os Zaps:** Veja `references/zaps.md`
- **Padrões MCP:** Veja `references/mcp-patterns.md`
- **Workflows comuns:** Ambos os arquivos contêm exemplos

## Exemplos de Uso

**Acionando um Zap:**
```
User: "Execute meu resumo diário"
Claude: [usa ferramenta Read em references/zaps.md para detalhes de webhook]
        [usa ferramenta Bash para acionar webhook com curl POST]
        "Iniciado seu Resumo AI Diário. Você receberá o relatório via email
         em ~3 minutos, com alertas SMS para qualquer item de alta prioridade."
```

**Usando orquestração MCP:**
```
User: "Pesquise o que há de novo em computação quântica"
Claude: [usa ferramenta Read em references/mcp-patterns.md]
        [chama ferramenta Perplexity Search MCP]
        [analisa resultados, identifica lacunas]
        [chama Perplexity Search novamente para mergulho mais profundo]
        "Eis o que encontrei... [resumo]"
```

**Aprendendo e atualizando:**
```
User: "Não, ao rastrear despesas use minha planilha 'Orçamento Pessoal', não 'Despesas'"
Claude: [usa ferramenta Read em references/mcp-patterns.md]
        [usa ferramenta Edit para atualizar a seção Google Sheets]
        "Entendi - atualizei a skill. Vou usar a planilha 'Orçamento Pessoal'
         para rastreamento de despesas a partir de agora."
```

## Perguntas Frequentes e Troubleshooting

### "Claude não está detectando minhas ferramentas Zapier MCP"

**Verifique se MCP está conectado:**
- Procure por ferramentas começando com `mcp__zapier__` em suas ferramentas disponíveis
- Tente perguntar: "Que ferramentas Zapier tenho?"

**Se não aparecer:**
1. Verifique que você executou o comando de conexão de https://mcp.zapier.com/mcp/servers
2. Reinicie Claude Code completamente (não apenas recarregue)
3. Verifique suas configurações de MCP do Claude Code
4. Verifique se o token de autorização no comando estava correto

### "Claude não está sugerindo guardar padrões"

**Detecção de padrão aciona quando:**
- Você usa 2+ ferramentas MCP em sequência
- A tarefa se completa com sucesso
- Parece repetível (não um pedido único)

**Tente pedir explicitamente:**
- "Pode guardar isto como um padrão?"
- "Lembre-se deste workflow para próxima vez"

### "URL de webhook não está acionando meu Zap"

**Problemas comuns:**
1. **URL incorreta** - Certifique-se de copiar a URL completa da aba Test
2. **Zap não ativado** - Ative o Zap no dashboard do Zapier
3. **Node de trigger incorreto** - Deve ser "Webhooks by Zapier" → "Catch Hook"
4. **Firewall/rede** - Verifique se comando curl funciona do terminal primeiro

**Teste manualmente:**
```bash
curl -X POST https://hooks.zapier.com/hooks/catch/[sua-url]
```

### "Claude continua pedindo para documentar ferramentas que já documentei"

**Causas prováveis:**
- Ferramentas documentadas mas arquivo não salvo corretamente
- Usando diferente instância/instalação do Claude Code
- Skill instalada em nível de projeto, não global

**Arrume:**
1. Verifique que `references/mcp-patterns.md` tem suas ferramentas
2. Verifique local da skill: `~/.claude/skills/` (global) vs `./.claude/skills/` (projeto)
3. Se nível de projeto, copie para global para persistência entre projetos

### "Como sou se a skill está funcionando?"

**Sinais de que está funcionando:**
1. Quando você menciona Zapier/workflows, Claude menciona verificar referências
2. Claude faz perguntas detalhadas (QUANDO/POR QUÊ/COMO) sobre ferramentas
3. Depois de usar ferramentas, Claude sugere guardar padrões
4. Claude aciona seus webhooks com sucesso

**Teste rápido:**
1. Pergunte: "Que ferramentas Zapier tenho?"
2. Adicione um webhook fake e conte ao Claude sobre ele
3. Verifique se foi adicionado a `references/zaps.md`

### "Arquivos da skill ficando muito grandes / lendo lentamente"

**Se arquivos de referência ficarem muito grandes:**
- Revise e remova padrões desatualizados/não usados
- Consolide workflows similares
- Mantenha apenas ferramentas usadas ativamente documentadas
- Considere dividir em múltiplas instâncias de skill para diferentes domínios

**Dicas de desempenho:**
- Mantenha frases de acionamento concisas e específicas
- Evite documentar workflows únicos
- Use categorias de padrão para organizar

### "Quero resetar a skill para estado de template"

**Para começar fresco:**
1. Faça backup de seus arquivos de skill atuais (se quiser manter algo)
2. Delete o diretório da skill
3. Re-clone do GitHub: https://github.com/AlexBoudreaux/claude-zapier-skill
4. Copie template fresco para `~/.claude/skills/`

### "Consigo usar esta skill sem Zapier MCP?"

**Sim!** A skill funciona com:
- **Apenas webhooks** - Acione Zaps multi-etapas sem MCP
- **Apenas ferramentas MCP** - Documente uso de ferramentas sem webhooks
- **Ambos** - Obtenha funcionalidade completa

Cada modo é independente e valioso por sua própria conta.

### "Segurança: acidentalmente fiz commit de URLs de webhook"

**Ações imediatas:**
1. Remova o commit do histórico git (git rebase, BFG Repo-Cleaner)
2. Regenere URLs de webhook no dashboard Zapier:
   - Edite o Zap
   - Delete e re-adicione o node webhook trigger
   - Obtenha nova URL de webhook
3. Atualize arquivos da skill com novas URLs
4. Adicione `.claude/` ao `.gitignore`

**Prevenção:**
- Instale skill globalmente (`~/.claude/skills/`)
- Nunca faça commit do diretório `.claude/` em projetos
- Use URLs de placeholder em exemplos compartilhados

## Notas Importantes

- **Webhooks não precisam de payloads** - Zaps obtêm seus dados de Tabelas Zapier
- **Sempre leia arquivos de referência** antes de executar - contêm detalhes críticos
- **Atualize arquivos de skill** ao aprender algo novo - não apenas lembre para essa conversa

## Ferramentas Claude Code Usadas

Esta skill usa as seguintes ferramentas Claude Code:

- **Read** - Para visualizar arquivos de referência (zaps.md, mcp-patterns.md)
- **Edit** - Para atualizar arquivos de skill com novos workflows, padrões ou preferências
- **Bash** - Para acionar webhooks Zapier usando requisições curl POST
- **MCP Tools** - Para chamar Perplexity Search, Google Sheets e outras integrações