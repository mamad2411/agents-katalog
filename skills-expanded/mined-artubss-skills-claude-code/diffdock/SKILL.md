---
name: diffdock
description: "Ancoragem molecular baseada em difusão. Prever poses de ligação proteína-ligando a partir de PDB/SMILES, scores de confiança, triagem virtual, para design de fármacos baseado em estrutura. Não para predição de afinidade."
---

# DiffDock: Ancoragem Molecular com Modelos de Difusão

## Visão Geral

DiffDock é uma ferramenta de aprendizado profundo baseada em difusão para ancoragem molecular que prediz poses de ligação 3D de pequenas moléculas ligantes a alvos proteicos. Representa o estado da arte em ancoragem computacional, crucial para descoberta de fármacos baseada em estrutura e biologia química.

**Capacidades Principais:**
- Prever poses de ligação de ligantes com alta precisão usando aprendizado profundo
- Suportar estruturas proteicas (arquivos PDB) ou sequências (via ESMFold)
- Processar complexos individuais ou campanhas de triagem virtual em lote
- Gerar scores de confiança para avaliar confiabilidade das predições
- Lidar com entradas de ligantes diversas (SMILES, SDF, MOL2)

**Distinção Chave:** DiffDock prediz **poses de ligação** (estrutura 3D) e **confiança** (certeza da predição), NÃO afinidade de ligação (ΔG, Kd). Sempre combine com funções de scoring (GNINA, MM/GBSA) para avaliação de afinidade.

## Quando Usar Esta Ferramenta

Esta ferramenta deve ser usada quando:

- "Faça ancoragem deste ligante a uma proteína" ou "prediga pose de ligação"
- "Execute ancoragem molecular" ou "realize ancoragem proteína-ligando"
- "Triagem virtual" ou "escaneie biblioteca de compostos"
- "Onde esta molécula se liga?" ou "prediga sítio de ligação"
- Tarefas de design de fármacos baseado em estrutura ou otimização de líderes
- Tarefas envolvendo arquivos PDB + strings SMILES ou estruturas de ligantes
- Ancoragem em lote de múltiplos pares proteína-ligando

## Instalação e Configuração do Ambiente

### Verificar Status do Ambiente

Antes de prosseguir com tarefas DiffDock, verifique a configuração do ambiente:

```bash
# Use o verificador de configuração fornecido
python scripts/setup_check.py
```

Este script valida versão Python, PyTorch com CUDA, PyTorch Geometric, RDKit, ESM e outras dependências.

### Opções de Instalação

**Opção 1: Conda (Recomendado)**
```bash
git clone https://github.com/gcorso/DiffDock.git
cd DiffDock
conda env create --file environment.yml
conda activate diffdock
```

**Opção 2: Docker**
```bash
docker pull rbgcsail/diffdock
docker run -it --gpus all --entrypoint /bin/bash rbgcsail/diffdock
micromamba activate diffdock
```

**Notas Importantes:**
- GPU fortemente recomendada (10-100x aceleração vs CPU)
- Primeira execução pré-computa tabelas de lookup SO(2)/SO(3) (~2-5 minutos)
- Checkpoints de modelo (~500MB) são baixados automaticamente se não estiverem presentes

## Workflows Principais

### Workflow 1: Ancoragem Proteína-Ligando Única

**Caso de Uso:** Fazer ancoragem de um ligante a um alvo proteico único

**Requisitos de Entrada:**
- Proteína: Arquivo PDB OU sequência de aminoácidos
- Ligante: String SMILES OU arquivo de estrutura (SDF/MOL2)

**Comando:**
```bash
python -m inference \
  --config default_inference_args.yaml \
  --protein_path protein.pdb \
  --ligand "CC(=O)Oc1ccccc1C(=O)O" \
  --out_dir results/single_docking/
```

**Alternativa (sequência proteica):**
```bash
python -m inference \
  --config default_inference_args.yaml \
  --protein_sequence "MSKGEELFTGVVPILVELDGDVNGHKF..." \
  --ligand ligand.sdf \
  --out_dir results/sequence_docking/
```

**Estrutura de Saída:**
```
results/single_docking/
├── rank_1.sdf          # Pose melhor classificada
├── rank_2.sdf          # Segunda melhor pose
├── ...
├── rank_10.sdf         # 10ª pose (padrão: 10 amostras)
└── confidence_scores.txt
```

### Workflow 2: Processamento em Lote de Múltiplos Complexos

**Caso de Uso:** Fazer ancoragem de múltiplos ligantes a proteínas, campanhas de triagem virtual

**Passo 1: Preparar CSV em Lote**

Use o script fornecido para criar ou validar entrada em lote:

```bash
# Criar template
python scripts/prepare_batch_csv.py --create --output batch_input.csv

# Validar CSV existente
python scripts/prepare_batch_csv.py my_input.csv --validate
```

**Formato CSV:**
```csv
complex_name,protein_path,ligand_description,protein_sequence
complex1,protein1.pdb,CC(=O)Oc1ccccc1C(=O)O,
complex2,,COc1ccc(C#N)cc1,MSKGEELFT...
complex3,protein3.pdb,ligand3.sdf,
```

**Colunas Obrigatórias:**
- `complex_name`: Identificador único
- `protein_path`: Caminho do arquivo PDB (deixe em branco se usar sequência)
- `ligand_description`: String SMILES ou caminho do arquivo de ligante
- `protein_sequence`: Sequência de aminoácidos (deixe em branco se usar PDB)

**Passo 2: Executar Ancoragem em Lote**

```bash
python -m inference \
  --config default_inference_args.yaml \
  --protein_ligand_csv batch_input.csv \
  --out_dir results/batch/ \
  --batch_size 10
```

**Para Triagem Virtual Grande (>100 compostos):**

Pré-computa embeddings de proteína para processamento mais rápido:
```bash
# Pré-computar embeddings
python datasets/esm_embedding_preparation.py \
  --protein_ligand_csv screening_input.csv \
  --out_file protein_embeddings.pt

# Executar com embeddings pré-computados
python -m inference \
  --config default_inference_args.yaml \
  --protein_ligand_csv screening_input.csv \
  --esm_embeddings_path protein_embeddings.pt \
  --out_dir results/screening/
```

### Workflow 3: Analisando Resultados

Após a conclusão da ancoragem, analise os scores de confiança e classifique as predições:

```bash
# Analisar todos os resultados
python scripts/analyze_results.py results/batch/

# Mostrar top 5 por complexo
python scripts/analyze_results.py results/batch/ --top 5

# Filtrar por threshold de confiança
python scripts/analyze_results.py results/batch/ --threshold 0.0

# Exportar para CSV
python scripts/analyze_results.py results/batch/ --export summary.csv

# Mostrar top 20 predições entre todos os complexos
python scripts/analyze_results.py results/batch/ --best 20
```

O script de análise:
- Analisa scores de confiança de todas as predições
- Classifica como Alta (>0), Moderada (-1.5 a 0) ou Baixa (<-1.5)
- Classifica predições dentro e entre complexos
- Gera resumos estatísticos
- Exporta resultados para CSV para análise posterior

## Interpretação do Score de Confiança

**Entendendo os Scores:**

| Intervalo de Score | Nível de Confiança | Interpretação |
|------------|------------------|----------------|
| **> 0** | Alta | Predição forte, provavelmente precisa |
| **-1.5 a 0** | Moderada | Predição razoável, valide cuidadosamente |
| **< -1.5** | Baixa | Predição incerta, requer validação |

**Notas Críticas:**
1. **Confiança ≠ Afinidade**: Alta confiança significa certeza do modelo sobre a estrutura, NÃO ligação forte
2. **Contexto Importa**: Ajuste expectativas para:
   - Ligantes grandes (>500 Da): Confiança menor esperada
   - Múltiplas cadeias proteicas: Pode diminuir confiança
   - Famílias proteicas novas: Pode ter desempenho inferior
3. **Múltiplas Amostras**: Revise top 3-5 predições, procure por consenso

**Para orientação detalhada:** Leia `references/confidence_and_limitations.md` usando a ferramenta Read

## Customização de Parâmetros

### Usando Configuração Personalizada

Crie configuração personalizada para casos de uso específicos:

```bash
# Copiar template
cp assets/custom_inference_config.yaml my_config.yaml

# Editar parâmetros (veja template para presets)
# Então executar com config personalizado
python -m inference \
  --config my_config.yaml \
  --protein_ligand_csv input.csv \
  --out_dir results/
```

### Parâmetros Chave para Ajustar

**Densidade de Amostragem:**
- `samples_per_complex: 10` → Aumente para 20-40 para casos difíceis
- Mais amostras = melhor cobertura, mas tempo de execução maior

**Passos de Inferência:**
- `inference_steps: 20` → Aumente para 25-30 para maior precisão
- Mais passos = qualidade potencialmente melhor, mas mais lento

**Parâmetros de Temperatura (controlam diversidade):**
- `temp_sampling_tor: 7.04` → Aumente para ligantes flexíveis (8-10)
- `temp_sampling_tor: 7.04` → Diminua para ligantes rígidos (5-6)
- Temperatura maior = poses mais diversas

**Presets Disponíveis no Template:**
1. Alta Precisão: Mais amostras + passos, temperatura menor
2. Triagem Rápida: Menos amostras, mais rápido
3. Ligantes Flexíveis: Temperatura de torção aumentada
4. Ligantes Rígidos: Temperatura de torção diminuída

**Para referência completa de parâmetros:** Leia `references/parameters_reference.md` usando a ferramenta Read

## Técnicas Avançadas

### Ancoragem em Ensemble (Flexibilidade Proteica)

Para proteínas com flexibilidade conhecida, faça ancoragem em múltiplas conformações:

```python
# Criar CSV de ensemble
import pandas as pd

conformations = ["conf1.pdb", "conf2.pdb", "conf3.pdb"]
ligand = "CC(=O)Oc1ccccc1C(=O)O"

data = {
    "complex_name": [f"ensemble_{i}" for i in range(len(conformations))],
    "protein_path": conformations,
    "ligand_description": [ligand] * len(conformations),
    "protein_sequence": [""] * len(conformations)
}

pd.DataFrame(data).to_csv("ensemble_input.csv", index=False)
```

Execute ancoragem com amostragem aumentada:
```bash
python -m inference \
  --config default_inference_args.yaml \
  --protein_ligand_csv ensemble_input.csv \
  --samples_per_complex 20 \
  --out_dir results/ensemble/
```

### Integração com Funções de Scoring

DiffDock gera poses; combine com outras ferramentas para afinidade:

**GNINA (Fast neural network scoring):**
```bash
for pose in results/*.sdf; do
    gnina -r protein.pdb -l "$pose" --score_only
done
```

**MM/GBSA (Mais preciso, mais lento):**
Use MMPBSA.py do AmberTools ou gmx_MMPBSA após minimização de energia

**Cálculos de Energia Livre (Mais preciso):**
Use OpenMM + OpenFE ou GROMACS para cálculos FEP/TI

**Workflow Recomendado:**
1. DiffDock → Gera poses com scores de confiança
2. Inspeção visual → Verifique plausibilidade estrutural
3. GNINA ou MM/GBSA → Reclassifique e ordene por afinidade
4. Validação experimental → Ensaios bioquímicos

## Limitações e Escopo

**DiffDock FOI Projetado Para:**
- Ligantes de pequenas moléculas (tipicamente 100-1000 Da)
- Compostos orgânicos tipo droga
- Pequenos peptídeos (<20 resíduos)
- Proteínas com cadeia única ou múltiplas cadeias

**DiffDock NÃO FOI Projetado Para:**
- Grandes biomoléculas (ancoragem proteína-proteína) → Use DiffDock-PP ou AlphaFold-Multimer
- Grandes peptídeos (>20 resíduos) → Use métodos alternativos
- Ancoragem covalente → Use ferramentas especializadas de ancoragem covalente
- Predição de afinidade de ligação → Combine com funções de scoring
- Proteínas de membrana → Não especificamente treinado, use com cuidado

**Para limitações completas:** Leia `references/confidence_and_limitations.md` usando a ferramenta Read

## Resolução de Problemas

### Problemas Comuns

**Problema: Scores de confiança baixos em todas as predições**
- Causa: Ligantes grandes/incomuns, sítio de ligação pouco claro, flexibilidade proteica
- Solução: Aumente `samples_per_complex` (20-40), tente ancoragem em ensemble, valide estrutura proteica

**Problema: Erros de falta de memória**
- Causa: Memória GPU insuficiente para tamanho de lote
- Solução: Reduza `--batch_size 2` ou processe menos complexos por vez

**Problema: Desempenho lento**
- Causa: Executando em CPU em vez de GPU
- Solução: Verifique CUDA com `python -c "import torch; print(torch.cuda.is_available())"`, use GPU

**Problema: Poses de ligação irrealistas**
- Causa: Preparação inadequada de proteína, ligante muito grande, sítio de ligação incorreto
- Solução: Verifique proteína quanto a resíduos ausentes, remova águas distantes, considere especificar sítio de ligação

**Problema: Erros "Module not found"**
- Causa: Dependências ausentes ou ambiente incorreto
- Solução: Execute `python scripts/setup_check.py` para diagnosticar

### Otimização de Desempenho

**Para Melhores Resultados:**
1. Use GPU (essencial para uso prático)
2. Pré-computa embeddings ESM para uso repetido de proteína
3. Processe múltiplos complexos em lote juntos
4. Comece com parâmetros padrão, depois ajuste se necessário
5. Valide estruturas proteicas (resolva resíduos ausentes)
6. Use SMILES canônicas para ligantes

## Interface Gráfica do Usuário

Para uso interativo, inicie a interface web:

```bash
python app/main.py
# Navegue para http://localhost:7860
```

Ou use a demonstração online sem instalação:
- https://huggingface.co/spaces/reginabarzilaygroup/DiffDock-Web

## Recursos

### Scripts Auxiliares (`scripts/`)

**`prepare_batch_csv.py`**: Cria e valida arquivos CSV de entrada em lote
- Cria templates com entradas de exemplo
- Valida caminhos de arquivo e strings SMILES
- Verifica colunas obrigatórias e problemas de formato

**`analyze_results.py`**: Analisa scores de confiança e classifica predições
- Analisa resultados de execuções únicas ou em lote
- Gera resumos estatísticos
- Exporta para CSV para análise posterior
- Identifica melhores predições entre complexos

**`setup_check.py`**: Verifica configuração do ambiente DiffDock
- Verifica versão Python e dependências
- Verifica disponibilidade de PyTorch e CUDA
- Testa instalação de RDKit e PyTorch Geometric
- Fornece instruções de instalação se necessário

### Documentação de Referência (`references/`)

**`parameters_reference.md`**: Documentação completa de parâmetros
- Todas as opções de linha de comando e parâmetros de configuração
- Valores padrão e intervalos aceitáveis
- Parâmetros de temperatura para controlar diversidade
- Locais de checkpoint de modelo e flags de versão

Leia este arquivo quando usuários precisarem:
- Explicações detalhadas de parâmetros
- Orientação de fine-tuning para sistemas específicos
- Estratégias alternativas de amostragem

**`confidence_and_limitations.md`**: Interpretação de score de confiança e limitações da ferramenta
- Interpretação detalhada de score de confiança
- Quando confiar em predições
- Escopo e limitações de DiffDock
- Integração com ferramentas complementares
- Estratégias de resolução de problemas

Leia este arquivo quando usuários precisarem:
- Ajuda para interpretar scores de confiança
- Entender quando NÃO usar DiffDock
- Orientação sobre combinação com outras ferramentas
- Estratégias de validação

**`workflows_examples.md`**: Exemplos abrangentes de workflows
- Instruções completas de instalação
- Exemplos passo a passo para todos os workflows
- Padrões avançados de integração
- Resolução de problemas comuns
- Melhores práticas e dicas de otimização

Leia este arquivo quando usuários precisarem:
- Exemplos completos de workflows com código
- Integração com GNINA, OpenMM ou outras ferramentas
- Workflows de triagem virtual
- Procedimentos de ancoragem em ensemble

### Assets (`assets/`)

**`batch_template.csv`**: Template para processamento em lote
- CSV pré-formatizado com colunas obrigatórias
- Entradas de exemplo mostrando diferentes tipos de entrada
- Pronto para personalizar com dados reais

**`custom_inference_config.yaml`**: Template de configuração
- YAML anotado com todos os parâmetros
- Quatro configurações preset para casos de uso comuns
- Comentários detalhados explicando cada parâmetro
- Pronto para personalizar e usar

## Melhores Práticas

1. **Sempre verifique o ambiente** com `setup_check.py` antes de iniciar trabalhos grandes
2. **Valide CSVs em lote** com `prepare_batch_csv.py` para capturar erros cedo
3. **Comece com padrões** depois ajuste parâmetros baseado em necessidades específicas do sistema
4. **Gere múltiplas amostras** (10-40) para predições robustas
5. **Inspeção visual** de melhores poses antes de análise posterior
6. **Combine com funções de scoring** para avaliação de afinidade
7. **Use scores de confiança** para classificação inicial, não decisões finais
8. **Pré-computa embeddings** para campanhas de triagem virtual
9. **Documente parâmetros** usados para reprodutibilidade
10. **Valide resultados** experimentalmente quando possível

## Citações

Ao usar DiffDock, cite os artigos apropriados:

**DiffDock-L (modelo padrão atual):**
```
Stärk et al. (2024) "DiffDock-L: Improving Molecular Docking with Diffusion Models"
arXiv:2402.18396
```

**DiffDock Original:**
```
Corso et al. (2023) "DiffDock: Diffusion Steps, Twists, and Turns for Molecular Docking"
ICLR 2023, arXiv:2210.01776
```

## Recursos Adicionais

- **Repositório GitHub**: https://github.com/gcorso/DiffDock
- **Demonstração Online**: https://huggingface.co/spaces/reginabarzilaygroup/DiffDock-Web
- **Artigo DiffDock-L**: https://arxiv.org/abs/2402.18396
- **Artigo Original**: https://arxiv.org/abs/2210.01776