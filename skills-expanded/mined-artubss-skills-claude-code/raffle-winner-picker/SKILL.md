---
name: raffle-winner-picker
description: Seleciona vencedores aleatórios de listas, planilhas ou Google Sheets para sorteios, rifas e concursos. Garante seleção justa e imparcial com transparência.
---

# Raffle Winner Picker

Esta skill seleciona aleatoriamente vencedores de listas, planilhas ou Google Sheets para sorteios e concursos.

## Quando Usar Esta Skill

- Executar sorteios em redes sociais
- Selecionar vencedores de rifas em eventos
- Escolher aleatoriamente participantes para pesquisas ou testes
- Selecionar vencedores de submissões de concursos
- Distribuição justa de vagas ou recursos limitados
- Atribuições aleatórias de equipes

## O Que Esta Skill Faz

1. **Seleção Aleatória**: Usa seleção aleatória criptograficamente segura
2. **Múltiplas Fontes**: Funciona com CSV, Excel, Google Sheets ou listas simples
3. **Múltiplos Vencedores**: Pode selecionar um ou vários vencedores
4. **Prevenção de Duplicatas**: Garante que a mesma pessoa não vença duas vezes
5. **Resultados Transparentes**: Mostra o processo de seleção claramente
6. **Detalhes do Vencedor**: Exibe todas as informações relevantes sobre os vencedores

## Como Usar

### A Partir do Google Sheets

```
Pick a random row from this Google Sheet to select a winner 
for a giveaway: [Sheet URL]
```

### A Partir de Arquivo Local

```
Pick 3 random winners from entries.csv
```

### A Partir de Uma Lista

```
Pick a random winner from this list:
- Alice (alice@email.com)
- Bob (bob@email.com)
- Carol (carol@email.com)
...
```

### Múltiplos Vencedores

```
Pick 5 random winners from contest-entries.xlsx, 
make sure no duplicates
```

## Exemplo

**Usuário**: "Selecione uma linha aleatória desta Google Sheet para escolher um vencedor para um sorteio."

**Saída**:
```
Accessing Google Sheet...
Total entries found: 247

Randomly selecting winner...

🎉 WINNER SELECTED! 🎉

Row #142
Name: Sarah Johnson
Email: sarah.j@email.com
Entry Date: March 10, 2024
Comment: "Love your newsletter!"

Selection method: Cryptographically random
Timestamp: 2024-03-15 14:32:18 UTC

Would you like to:
- Pick another winner (excluding Sarah)?
- Export winner details?
- Pick runner-ups?
```

**Inspirado em**: Uso de Lenny - selecionar um vencedor do sorteio Sora 2 da sua comunidade Slack de assinantes

## Recursos

### Seleção Justa
- Usa geração de números aleatórios seguros
- Sem viés ou padrões
- Processo transparente
- Repetível com seed (para verificação)

### Exclusões
```
Pick a random winner excluding previous winners: 
Alice, Bob, Carol
```

### Seleção Ponderada
```
Pick a winner with weighted probability based on 
the "entries" column (1 entry = 1 ticket)
```

### Suplentes
```
Pick 1 winner and 3 runner-ups from the list
```

## Fluxos de Trabalho Exemplo

### Sorteio em Redes Sociais
1. Exporte submissões do Google Form para Sheets
2. "Selecione um vencedor aleatório de [Sheet URL]"
3. Verifique detalhes do vencedor
4. Anuncie publicamente com timestamp

### Rifa em Evento
1. Crie CSV com nomes e emails dos participantes
2. "Selecione 10 vencedores aleatórios de attendees.csv"
3. Exporte lista de vencedores
4. Envie email diretamente aos vencedores

### Atribuição de Equipes
1. Tenha lista de participantes
2. "Divida aleatoriamente esta lista em 4 equipes iguais"
3. Revise as atribuições
4. Compartilhe os rosters das equipes

## Dicas

- **Documente o processo**: Salve o timestamp e o método
- **Anúncio Público**: Compartilhe detalhes da seleção para transparência
- **Verifique elegibilidade**: Confirme que o vencedor atende às regras do concurso
- **Tenha suplentes**: Selecione suplentes caso o vencedor seja inelegível
- **Exporte resultados**: Salve lista de vencedores para registros

## Privacidade e Justiça

✓ Usa aleatoriedade criptograficamente segura
✓ Nenhuma manipulação possível
✓ Timestamp registrado para verificação
✓ Pode fornecer seed para verificação de terceiros
✓ Respeita privacidade de dados

## Casos de Uso Comuns

- Sorteios de assinantes de newsletter
- Rifas de lançamento de produtos
- Sorteios de ingressos para conferências
- Seleção de testadores beta
- Seleção de participantes de grupos de foco
- Distribuição aleatória de prêmios em eventos