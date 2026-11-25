---
name: ship-learn-next
description: Transforme conteúdo educacional (como transcrições do YouTube, artigos, tutoriais) em planos de implementação acionáveis usando o framework Ship-Learn-Next. Use quando o usuário quer converter conselhos, lições ou conteúdo educacional em passos concretos, repetições ou uma jornada de aprendizado.
allowed-tools:
  - Read
  - Write
---

# Planejador de Ações Ship-Learn-Next

Esta habilidade ajuda a transformar aprendizado passivo em ciclos **Ship-Learn-Next** acionáveis — convertendo conselhos e lições em iterações concretas e shippáveis.

## Quando Usar Esta Habilidade

Ative quando o usuário:
- Tem uma transcrição/artigo/tutorial e quer "implementar o conselho"
- Pede para "transformar isso em um plano" ou "tornar isso acionável"
- Quer extrair passos de implementação de conteúdo educacional
- Precisa quebrar ideias grandes em pequenas repetições shippáveis
- Diz coisas como "Assisti/li X, e agora?"

## Framework Central: Ship-Learn-Next

Toda jornada de aprendizado segue três fases repetidas:

1. **SHIP** - Crie algo real (código, conteúdo, produto, demonstração)
2. **LEARN** - Reflexão honesta sobre o que aconteceu
3. **NEXT** - Planeje a próxima iteração baseado no que aprendeu

**Princípio-chave**: 100 repetições vencem 100 horas de estudo. Aprender = fazer melhor, não saber mais.

## Como Esta Habilidade Funciona

### Passo 1: Ler o Conteúdo

Leia o arquivo que o usuário fornece (transcrição, artigo, notas):

```bash
# Usuário fornece o caminho do arquivo
FILE_PATH="/path/to/content.txt"
```

Use a ferramenta Read para analisar o conteúdo.

### Passo 2: Extrair Lições Principais

Identifique no conteúdo:
- **Conselhos/lições principais**: Quais são os aprendizados-chave?
- **Princípios acionáveis**: O que pode realmente ser praticado?
- **Habilidades sendo ensinadas**: O que alguém aprenderia fazendo isso?
- **Exemplos/estudos de caso**: Implementações reais mencionadas

**NÃO faça**:
- Resuma tudo (foque nas partes acionáveis)
- Liste teoria sem aplicação
- Inclua "legal saber" vs "precisa praticar"

### Passo 3: Definir a Jornada

Ajude o usuário a enquadrar seu objetivo de aprendizado:

Pergunte:
1. "Baseado neste conteúdo, o que você quer alcançar em 4-8 semanas?"
2. "Como seria o sucesso? (Seja específico)"
3. "Qual é algo concreto que você poderia construir/criar/enviar?"

**Exemplo de jornada boa**: "Enviar 10 mensagens de contato frio e obter 2 respostas"
**Exemplo de jornada ruim**: "Aprender sobre vendas" (muito vago)

### Passo 4: Desenhar Repetição 1 (A Primeira Iteração)

Quebre a jornada na **versão shippável mais simples**:

Pergunte:
- "Qual é a versão mais simples que você poderia enviar ESTA SEMANA?"
- "O que você precisa aprender APENAS para fazer isso?" (não tudo)
- "Como seria 'pronto' para repetição 1?"

**Torne-a**:
- Concreta e específica
- Completável em 1-7 dias
- Produz evidência/artefato real
- Pequena o suficiente para não ser intimidadora
- Grande o suficiente para aprender algo significativo

### Passo 5: Criar o Plano de Repetição

Estruture cada repetição com:

```markdown
## Repetição 1: [Objetivo Específico]

**Objetivo ao Enviar**: [O que você vai criar/fazer]
**Critérios de Sucesso**: [Como você saberá que terminou]
**O Que Você Aprenderá**: [Habilidades/insights específicos]
**Recursos Necessários**: [Mínimo - apenas o necessário para ESTA repetição]
**Prazo**: [Deadline específico]

**Passos de Ação**:
1. [Passo concreto 1]
2. [Passo concreto 2]
3. [Passo concreto 3]
...

**Após Enviar - Perguntas de Reflexão**:
- O que realmente aconteceu? (Seja específico)
- O que funcionou? O que não funcionou?
- O que o surpreendeu?
- Em escala de 1-10, como foi esta repetição?
- O que você faria diferente próxima vez?
```

### Passo 6: Mapear Repetições Futuras (2-5)

Baseado no conteúdo, sugira uma progressão:

```markdown
## Repetição 2: [Próximo nível]
**Baseado em**: O que você aprendeu na Repetição 1
**Novo desafio**: Uma coisa nova para tentar/melhorar
**Dificuldade esperada**: [Mais fácil/Igual/Mais difícil - e por quê]

## Repetição 3: [Continuar progressão]
...
```

**Princípios de progressão**:
- Cada repetição adiciona UM novo elemento
- Aumente a dificuldade baseado no sucesso
- Referencie lições específicas do conteúdo
- Mantenha repetições shippáveis (não teóricas)

### Passo 7: Conectar ao Conteúdo

Para cada repetição, referencie o material-fonte:

- "Isso implementa o [conceito] do minuto X"
- "Você está praticando a [técnica] mencionada no vídeo"
- "Isso testa o conselho sobre [tópico]"

**Mas**: Sempre enfatize FAZER sobre estudar. Aponte para recursos apenas quando necessário para a repetição específica.

## Estilo de Conversa

**Direto mas solidário**:
- Sem floreios, mas encorajador
- "Envie, depois melhoramos"
- "Qual é a versão mais simples que você poderia fazer esta semana?"

**Orientado por perguntas**:
- Faça-os pensar, não apenas diga
- "O que exatamente você quer alcançar?" não "Aqui está o que você deveria fazer"

**Específico, não genérico**:
- "Até sexta, enviar uma landing page" não "Aprender desenvolvimento web"
- Pressione por compromissos concretos

**Orientado para ação**:
- Sempre termine com "qual é o próximo passo?"
- Foque na próxima repetição, não na jornada inteira

## O Que NÃO Fazer

- ❌ Não crie um plano de estudo (crie um plano de ENVIO)
- ❌ Não liste todos os recursos para ler/assistir (escolha recursos mínimos para repetição atual)
- ❌ Não deixe a perfeição ser inimiga do enviado
- ❌ Não deixe-os planejar para sempre sem começar
- ❌ Não aceite objetivos vagos ("aprender X" → "enviar Y até Z data")
- ❌ Não os sobrecarregue com a jornada completa (foque na repetição 1)

## Frases-Chave para Usar

- "Qual é a versão mais simples que você poderia enviar esta semana?"
- "O que você precisa aprender APENAS para fazer isso?"
- "Isso não é sobre perfeição - é repetição 1 de 100"
- "Envie algo real, depois melhoramos"
- "Baseado em [conteúdo], o que você realmente FARIA diferente?"
- "Aprender = fazer melhor, não saber mais"

## Estrutura de Exemplo de Saída

```markdown
# Sua Jornada Ship-Learn-Next: [Título]

## Visão Geral da Jornada
**Objetivo**: [O que eles querem alcançar em 4-8 semanas]
**Fonte**: [O conteúdo que inspirou isso]
**Lições Principais**: [3-5 aprendizados acionáveis do conteúdo]

---

## Repetição 1: [Objetivo Específico e Shippável]

**Objetivo ao Enviar**: [Entregável concreto]
**Prazo**: [Esta semana / Até [data]]
**Critérios de Sucesso**:
- [ ] [Coisa específica 1]
- [ ] [Coisa específica 2]
- [ ] [Coisa específica 3]

**O Que Você Vai Praticar** (do conteúdo):
- [Habilidade/conceito 1 do material-fonte]
- [Habilidade/conceito 2 do material-fonte]

**Passos de Ação**:
1. [Passo concreto]
2. [Passo concreto]
3. [Passo concreto]
4. Envie (publique/implante/compartilhe/demonstre)

**Recursos Mínimos** (apenas para esta repetição):
- [Link ou referência - se realmente necessário]

**Após Enviar - Reflexão**:
Responda estas perguntas:
- O que realmente aconteceu?
- O que funcionou? O que não funcionou?
- O que o surpreendeu?
- Avalie esta repetição: _/10
- Qual é uma coisa para tentar diferente próxima vez?

---

## Repetição 2: [Próxima Iteração]

**Baseado em**: Repetição 1 + [o que você aprendeu]
**Novo elemento**: [Um novo desafio/habilidade]
**Objetivo ao enviar**: [Próximo entregável concreto]

[Estrutura similar...]

---

## Repetições 3-5: Caminho Futuro

**Repetição 3**: [Descrição breve]
**Repetição 4**: [Descrição breve]
**Repetição 5**: [Descrição breve]

*(Detalhes evoluirão baseado no que você aprender nas Repetições 1-2)*

---

## Lembre-se

- Isso é sobre FAZER, não estudar
- Vise 100 repetições ao longo do tempo (não perfeição na repetição 1)
- Cada repetição = Planejar → Fazer → Refletir → Próximo
- Você aprende enviando, não consumindo

**Pronto para enviar a Repetição 1?**
```

## Processando Diferentes Tipos de Conteúdo

### Transcrições do YouTube
- Foque em conselhos, não histórias
- Extraia técnicas concretas mencionadas
- Identifique estudos de caso/exemplos para replicar
- Anote timestamps para referência depois (mas não exija assistir novamente)

### Artigos/Tutoriais
- Identifique as partes "agora faça isso" vs teoria
- Extraia o workflow/processo específico
- Encontre o exemplo mínimo para começar

### Notas de Curso
- Qual é o menor projeto do curso?
- Quais módulos são necessários para repetição 1? (ignore o resto por enquanto)
- O que pode ser praticado imediatamente?

## Métricas de Sucesso

Um bom plano Ship-Learn-Next tem:
- ✅ Repetição 1 específica e shippável (completável em 1-7 dias)
- ✅ Critérios de sucesso claros (usuário sabe quando terminou)
- ✅ Artefatos concretos (algo real para mostrar)
- ✅ Conexão direta com conteúdo-fonte
- ✅ Caminho de progressão para repetições 2-5
- ✅ Ênfase em ação sobre consumo
- ✅ Reflexão honesta incorporada
- ✅ Pequena o suficiente para começar hoje, grande o suficiente para aprender

## Salvando o Plano

**IMPORTANTE**: Sempre salve o plano em um arquivo para o usuário.

### Convenção de Nome

Sempre use o formato:
- `Ship-Learn-Next Plan - [Título Breve da Jornada].md`

Exemplos:
- `Ship-Learn-Next Plan - Construir em Mercados Provados.md`
- `Ship-Learn-Next Plan - Aprender React.md`
- `Ship-Learn-Next Plan - Prospecção por Email Frio.md`

**O título da jornada deve ser**:
- Breve (3-6 palavras)
- Descritivo do objetivo principal
- Baseado na lição central/tema do conteúdo

### O Que Salvar

**Plano completo incluindo**:
- Visão geral da jornada com objetivo e fonte
- Todas as repetições (1-5) com detalhes completos
- Passos de ação e perguntas de reflexão
- Compromissos de prazo
- Referência ao material-fonte

**Formato**: Sempre salve como Markdown (`.md`) para legibilidade

## Após Criar o Plano

**Exiba para o usuário**:
1. Mostre que você salvou o plano: "✓ Salvo em: [nome do arquivo]"
2. Dê uma visão geral breve da jornada
3. Destaque a Repetição 1 (o que está vencido esta semana)

**Depois pergunte**:
1. "Quando você vai enviar a Repetição 1?"
2. "Qual é a única coisa que pode impedir você? Como vai lidar com isso?"
3. "Volte após enviar e vamos refletir + planejar a Repetição 2"

**Lembre-se**: Você não está criando um currículo. Você está ajudando-o a enviar algo real, aprender com isso, e enviar a próxima coisa.

Vamos ajudá-lo a enviar.