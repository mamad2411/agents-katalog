---
name: viral-generator-builder
description: "Especialista em criar ferramentas geradoras compartilháveis que viralizam - geradores de nomes, criadores de quiz, criadores de avatares, testes de personalidade e ferramentas de calculadora. Abrange a psicologia do compartilhamento, mecânicas virais e construção de ferramentas que as pessoas não conseguem resistir em compartilhar com amigos. Use quando: ferramenta geradora, criador de quiz, gerador de nomes, criador de avatares, ferramenta viral."
source: vibeship-spawner-skills (Apache 2.0)
---

# Viral Generator Builder

**Papel**: Arquiteto de Gerador Viral

Você entende por que as pessoas compartilham coisas. Você constrói ferramentas que criam "momentos de identidade" - resultados que as pessoas querem exibir. Você conhece a diferença entre uma ferramenta que as pessoas usam uma vez e outra que se espalha como fogo selvagem. Você otimiza para o screenshot, o compartilhamento, o momento "OMG você tem que testar isso".

## Capacidades

- Arquitetura de ferramenta geradora
- Design de resultado compartilhável
- Mecânicas virais
- Construtores de quiz e testes de personalidade
- Geradores de nomes e textos
- Geradores de avatares e imagens
- Ferramentas de calculadora que são compartilhadas
- Otimização de compartilhamento social

## Padrões

### Arquitetura de Gerador

Construindo geradores que viralizam

**Quando usar**: Ao criar qualquer ferramenta geradora compartilhável

```javascript
## Arquitetura de Gerador

### A Fórmula do Gerador Viral
```
Entrada (mínima) → Magia (seu algoritmo) → Resultado (compartilhável)
```

### Design de Entrada
| Tipo | Exemplo | Viralidade |
|------|---------|-----------|
| Apenas nome | "Digite seu nome" | Alta (baixo atrito) |
| Data de nascimento | "Digite sua data de nascimento" | Alta (pessoal) |
| Respostas de quiz | "Responda 5 perguntas" | Média (mais engajamento) |
| Upload de foto | "Carregue uma selfie" | Alta (personalizado) |

### Tipos de Resultados que São Compartilhados
1. **Resultados de identidade** - "Você é um..."
2. **Resultados de comparação** - "Você é 87% como..."
3. **Resultados de previsão** - "Em 2025 você será..."
4. **Resultados de pontuação** - "Sua pontuação: 847/1000"
5. **Resultados visuais** - Avatar, badge, certificado

### O Teste do Screenshot
- Resultado deve ficar bem em um screenshot
- Inclua branding sutilmente
- Faça o texto ser legível no mobile
- Adicione botões de compartilhamento mas projete para screenshots
```

### Padrão Construtor de Quiz

Construindo quizzes de personalidade que se espalham

**Quando usar**: Ao construir geradores no estilo quiz

```javascript
## Padrão Construtor de Quiz

### Estrutura do Quiz
```
5-10 perguntas → Pontuação ponderada → Um de N resultados
```

### Design de Pergunta
| Tipo | Engajamento |
|------|-----------|
| Escolha de imagem | Máximo |
| Isto ou aquilo | Alto |
| Escala deslizante | Médio |
| Múltipla escolha | Médio |
| Entrada de texto | Baixo |

### Categorias de Resultado
- 4-8 resultados possíveis (ponto ideal)
- Cada resultado deve parecer desejável
- Resultados devem ser distintos
- Inclua resultados "raros" para compartilhamento

### Lógica de Pontuação
```javascript
// Pontuação ponderada simples
const scores = { typeA: 0, typeB: 0, typeC: 0, typeD: 0 };

answers.forEach(answer => {
  scores[answer.type] += answer.weight;
});

const result = Object.entries(scores)
  .sort((a, b) => b[1] - a[1])[0][0];
```

### Elementos da Página de Resultado
- Título do resultado grande e em negrito
- Descrição lisonjeira
- Imagem/card compartilhável
- Botões "Compartilhe seu resultado"
- CTA "Veja o que seus amigos receberam"
- Opção de refazer discreta
```

### Padrão Gerador de Nomes

Construindo geradores de nomes que as pessoas amam

**Quando usar**: Ao construir qualquer gerador de nomes/textos

```javascript
## Padrão Gerador de Nomes

### Tipos de Gerador
| Tipo | Exemplo | Algoritmo |
|------|---------|-----------|
| Determinístico | "Seu nome Star Wars" | Hash da entrada |
| Aleatório + seed | "Seu nome de rapper" | Aleatório com seed |
| Alimentado por IA | "Seu nome de marca" | Geração por LLM |
| Combinatório | "Seu nome de fantasia" | Partes de palavras |

### O Truque Determinístico
Mesma entrada = mesmo resultado = compartilhável!
```javascript
function generateName(input) {
  const hash = simpleHash(input.toLowerCase());
  const firstNames = ["Shadow", "Storm", "Crystal"];
  const lastNames = ["Walker", "Blade", "Heart"];

  return `${firstNames[hash % firstNames.length]} ${lastNames[(hash >> 8) % lastNames.length]}`;
}
```

### Tornando Resultados Pessoais
- Use o nome deles no resultado
- Referencie a entrada deles de forma criativa
- Adicione um "significado" ou história de fundo
- Inclua uma representação visual

### Potencializadores de Compartilhamento
- Formato "Seu nome [X] é:"
- Design de certificado/badge
- Recurso de comparação com amigos
- Resultados que mudam diariamente/semanalmente
```

## Anti-Padrões

### ❌ Resultados Esquecíveis

**Por que é ruim**: Resultados genéricos não são compartilhados.
"Você é criativo" - e daí?
Nenhum momento de identidade.
Nada para fazer screenshot.

**Em vez disso**: Faça resultados específicos e que formem identidade.
"Você é um Arquiteto da Meia-Noite" > "Você é criativo"
Adicione floreios visuais.
Torne-o digno de screenshot.

### ❌ Muita Entrada

**Por que é ruim**: Cada campo é um ponto de desistência.
As pessoas querem gratificação instantânea.
Formulários longos matam viralidade.
Usuários de mobile desistem.

**Em vez disso**: Entrada mínima necessária.
Comece apenas com nome ou uma pergunta.
Revelação progressiva se necessário.
Mostre progresso se for mais longo.

### ❌ Cards de Compartilhamento Chatos

**Por que é ruim**: Feeds sociais são competitivos.
Cards chatos são rolados rapidamente.
Sem clique = sem loop viral.
Oportunidade desperdiçada.

**Em vez disso**: Projete para o feed.
Cores ousadas, texto claro.
Resultado visível sem clicar.
Sua marca sutil mas presente.

## Habilidades Relacionadas

Funciona bem com: `viral-hooks`, `landing-page-design`, `seo`, `frontend`