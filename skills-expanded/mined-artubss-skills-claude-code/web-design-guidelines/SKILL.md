---
name: web-design-guidelines
description: Analise código da interface para conformidade com as Diretrizes de Interface Web. Use quando solicitado para "revisar minha UI", "verificar acessibilidade", "auditar design", "revisar UX" ou "verificar meu site em relação às melhores práticas".
argument-hint: <file-or-pattern>
---

# Diretrizes de Interface Web

Analise arquivos para conformidade com as Diretrizes de Interface Web.

## Como Funciona

1. Busque as últimas diretrizes da URL de origem abaixo
2. Leia os arquivos especificados (ou solicite ao usuário arquivos/padrão)
3. Verifique em relação a todas as regras nas diretrizes buscadas
4. Apresente os resultados no formato conciso `arquivo:linha`

## Fonte das Diretrizes

Busque diretrizes atualizadas antes de cada análise:

```
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

Use WebFetch para recuperar as últimas regras. O conteúdo buscado contém todas as regras e instruções de formato de saída.

## Uso

Quando um usuário fornece um argumento de arquivo ou padrão:
1. Busque diretrizes da URL de origem acima
2. Leia os arquivos especificados
3. Aplique todas as regras das diretrizes buscadas
4. Apresente os resultados usando o formato especificado nas diretrizes

Se nenhum arquivo for especificado, solicite ao usuário quais arquivos revisar.