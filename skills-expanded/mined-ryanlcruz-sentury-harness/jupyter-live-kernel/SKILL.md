---
name: jupyter-live-kernel
description: "Execução interativa Python via REPL persistente no sandbox."
version: 1.0.0
category: data-science
tags: [jupyter, repl, python, persistência, dataframe, analítico]
tools_used: [executar_python]
platforms: [linux, macos, windows]
---

# Jupyter Live Kernel (Interactive REPL)

Esta rotina fornece persistência de estado nas execuções Python no sandbox analítico. Ela permite carregar DataFrames na memória do Kernel e trabalhar de forma iterativa sem ler os arquivos a cada turno.

## Quando Usar

- Análise de dados incremental (exploração de tabelas gigantes).
- Modelagem de correlação de múltiplas variáveis temporais que exigem várias etapas de refinamento.
- Criação e depuração de visualizações e gráficos interativos passo a passo.

## Procedimento

1. **Iniciar Conexão**: Verificar se o servidor Jupyter local ou ambiente do sandbox está disponível para conexões.
2. **Carregar as Coleções**:
   ```python
   import pandas as pd
   # Carrega os arquivos que a pessoa indicou, uma vez
   pedidos = pd.read_csv("pedidos.csv")
   clientes = pd.read_csv("clientes.csv")
   ```
3. **Execução Stateful**:
   - A cada nova instrução de cálculo do usuário, execute o bloco na mesma sessão do kernel para reutilizar as variáveis `pedidos` e `clientes` modificadas.
4. **Inspecionar Variáveis**:
   - Chamar inspeção nos DataFrames (`df.head()` ou `df.info()`) e retornar apenas resumos tabulares concisos para o usuário.

## Pitfalls

- Evite reiniciar o kernel a menos que ocorra estouro de memória ou seja solicitado explicitamente.
- O tempo limite padrão das chamadas é de 30 segundos.
