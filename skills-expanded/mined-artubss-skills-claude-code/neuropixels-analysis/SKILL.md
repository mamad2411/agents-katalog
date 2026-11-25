---
name: neuropixels-analysis
description: "Análise de registros neurais Neuropixels. Carregamento de dados SpikeGLX/OpenEphys, pré-processamento, correção de movimento, spike sorting com Kilosort4, métricas de qualidade, curação Allen/IBL, análise visual assistida por IA, para eletrofisiologia extracelular Neuropixels 1.0/2.0. Use ao trabalhar com registros neurais, spike sorting, eletrofisiologia extracelular, ou quando o usuário mencionar Neuropixels, SpikeGLX, Open Ephys, Kilosort, métricas de qualidade, ou curação de unidades."
---

# Análise de Dados Neuropixels

## Visão geral

Toolkit abrangente para análise de registros neurais de alta densidade Neuropixels utilizando as melhores práticas atuais de SpikeInterface, Allen Institute e International Brain Laboratory (IBL). Suporta o fluxo de trabalho completo de dados brutos para unidades curadas prontas para publicação.

## Quando usar esta skill

Esta skill deve ser usada quando:
- Trabalhando com registros Neuropixels (.ap.bin, .lf.bin, arquivos .meta)
- Carregando dados de formatos SpikeGLX, Open Ephys ou NWB
- Pré-processando registros neurais (filtragem, CAR, detecção de canais ruins)
- Detectando e corrigindo movimento/deriva em registros
- Executando spike sorting (Kilosort4, SpykingCircus2, Mountainsort5)
- Computando métricas de qualidade (SNR, violações de ISI, razão de presença)
- Curando unidades utilizando critérios Allen/IBL
- Criando visualizações de dados neurais
- Exportando resultados para Phy ou NWB

## Hardware e formatos suportados

| Sonda | Eletrodos | Canais | Notas |
|-------|-----------|--------|-------|
| Neuropixels 1.0 | 960 | 384 | Requer correção phase_shift |
| Neuropixels 2.0 (único) | 1280 | 384 | Geometria mais densa |
| Neuropixels 2.0 (4-shank) | 5120 | 384 | Registro multi-região |

| Formato | Extensão | Leitor |
|--------|----------|--------|
| SpikeGLX | `.ap.bin`, `.lf.bin`, `.meta` | `si.read_spikeglx()` |
| Open Ephys | `.continuous`, `.oebin` | `si.read_openephys()` |
| NWB | `.nwb` | `si.read_nwb()` |

## Início rápido

### Importação e configuração básicas

```python
import spikeinterface.full as si
import neuropixels_analysis as npa

# Configurar processamento paralelo
job_kwargs = dict(n_jobs=-1, chunk_duration='1s', progress_bar=True)
```

### Carregando dados

```python
# SpikeGLX (mais comum)
recording = si.read_spikeglx('/path/to/data', stream_id='imec0.ap')

# Open Ephys (comum para muitos laboratórios)
recording = si.read_openephys('/path/to/Record_Node_101/')

# Verificar streams disponíveis
streams, ids = si.get_neo_streams('spikeglx', '/path/to/data')
print(streams)  # ['imec0.ap', 'imec0.lf', 'nidq']

# Para teste com subconjunto de dados
recording = recording.frame_slice(0, int(60 * recording.get_sampling_frequency()))
```

### Pipeline completo (Um comando)

```python
# Executar pipeline de análise completo
results = npa.run_pipeline(
    recording,
    output_dir='output/',
    sorter='kilosort4',
    curation_method='allen',
)

# Acessar resultados
sorting = results['sorting']
metrics = results['metrics']
labels = results['labels']
```

## Fluxo de trabalho de análise padrão

### 1. Pré-processamento

```python
# Cadeia de pré-processamento recomendada
rec = si.highpass_filter(recording, freq_min=400)
rec = si.phase_shift(rec)  # Necessário para Neuropixels 1.0
bad_ids, _ = si.detect_bad_channels(rec)
rec = rec.remove_channels(bad_ids)
rec = si.common_reference(rec, operator='median')

# Ou use nosso wrapper
rec = npa.preprocess(recording)
```

### 2. Verificar e corrigir deriva

```python
# Verificar deriva (sempre faça isso!)
motion_info = npa.estimate_motion(rec, preset='kilosort_like')
npa.plot_drift(rec, motion_info, output='drift_map.png')

# Aplicar correção se necessário
if motion_info['motion'].max() > 10:  # microns
    rec = npa.correct_motion(rec, preset='nonrigid_accurate')
```

### 3. Spike sorting

```python
# Kilosort4 (recomendado, requer GPU)
sorting = si.run_sorter('kilosort4', rec, folder='ks4_output')

# Alternativas CPU
sorting = si.run_sorter('tridesclous2', rec, folder='tdc2_output')
sorting = si.run_sorter('spykingcircus2', rec, folder='sc2_output')
sorting = si.run_sorter('mountainsort5', rec, folder='ms5_output')

# Verificar sorters disponíveis
print(si.installed_sorters())
```

### 4. Pós-processamento

```python
# Criar analyzer e computar todas as extensões
analyzer = si.create_sorting_analyzer(sorting, rec, sparse=True)

analyzer.compute('random_spikes', max_spikes_per_unit=500)
analyzer.compute('waveforms', ms_before=1.0, ms_after=2.0)
analyzer.compute('templates', operators=['average', 'std'])
analyzer.compute('spike_amplitudes')
analyzer.compute('correlograms', window_ms=50.0, bin_ms=1.0)
analyzer.compute('unit_locations', method='monopolar_triangulation')
analyzer.compute('quality_metrics')

metrics = analyzer.get_extension('quality_metrics').get_data()
```

### 5. Curação

```python
# Critérios Allen Institute (conservadores)
good_units = metrics.query("""
    presence_ratio > 0.9 and
    isi_violations_ratio < 0.5 and
    amplitude_cutoff < 0.1
""").index.tolist()

# Ou use curação automatizada
labels = npa.curate(metrics, method='allen')  # 'allen', 'ibl', 'strict'
```

### 6. Curação assistida por IA (Para unidades incertas)

Ao usar esta skill com Claude Code, Claude pode analisar diretamente plots de waveform e fornecer decisões de curação especializadas. Para acesso programático via API:

```python
from anthropic import Anthropic

# Configurar cliente da API
client = Anthropic()

# Analisar unidades incertas visualmente
uncertain = metrics.query('snr > 3 and snr < 8').index.tolist()

for unit_id in uncertain:
    result = npa.analyze_unit_visually(analyzer, unit_id, api_client=client)
    print(f"Unidade {unit_id}: {result['classification']}")
    print(f"  Raciocínio: {result['reasoning'][:100]}...")
```

**Integração Claude Code**: Ao executar dentro do Claude Code, peça a Claude para examinar diretamente plots de waveform/correlogram — não é necessária configuração de API.

### 7. Gerar relatório de análise

```python
# Gerar relatório HTML abrangente com visualizações
report_dir = npa.generate_analysis_report(results, 'output/')
# Abre report.html com estatísticas de resumo, figuras e tabela de unidades

# Imprimir resumo formatado no console
npa.print_analysis_summary(results)
```

### 8. Exportar resultados

```python
# Exportar para Phy para revisão manual
si.export_to_phy(analyzer, output_folder='phy_export/',
                 compute_pc_features=True, compute_amplitudes=True)

# Exportar para NWB
from spikeinterface.exporters import export_to_nwb
export_to_nwb(rec, sorting, 'output.nwb')

# Salvar métricas de qualidade
metrics.to_csv('quality_metrics.csv')
```

## Armadilhas comuns e melhores práticas

1. **Sempre verificar deriva** antes de spike sorting — deriva > 10μm impacta significativamente a qualidade
2. **Usar phase_shift** para sondas Neuropixels 1.0 (não necessário para 2.0)
3. **Salvar dados pré-processados** para evitar recomputação — use `rec.save(folder='preprocessed/')`
4. **Usar GPU** para Kilosort4 — é 10-50x mais rápido que alternativas CPU
5. **Revisar unidades incertas manualmente** — curação automatizada é um ponto de partida
6. **Combinar métricas com IA** — usar métricas para casos claros, IA para unidades borderline
7. **Documentar seus limites** — diferentes análises podem precisar de critérios diferentes
8. **Exportar para Phy** para experimentos críticos — supervisão humana é valiosa

## Parâmetros-chave para ajustar

### Pré-processamento
- `freq_min`: Cutoff highpass (300-400 Hz típico)
- `detect_threshold`: Sensibilidade de detecção de canal ruim

### Correção de movimento
- `preset`: 'kilosort_like' (rápido) ou 'nonrigid_accurate' (melhor para deriva severa)

### Spike sorting (Kilosort4)
- `batch_size`: Amostras por batch (padrão 30000)
- `nblocks`: Número de blocos de deriva (aumentar para registros longos)
- `Th_learned`: Limiar de detecção (menor = mais spikes)

### Métricas de qualidade
- `snr_threshold`: Cutoff sinal-ruído (3-5 típico)
- `isi_violations_ratio`: Violações refratárias (0.01-0.5)
- `presence_ratio`: Cobertura de gravação (0.5-0.95)

## Recursos agrupados

### scripts/preprocess_recording.py
Script de pré-processamento automatizado:
```bash
python scripts/preprocess_recording.py /path/to/data --output preprocessed/
```

### scripts/run_sorting.py
Executar spike sorting:
```bash
python scripts/run_sorting.py preprocessed/ --sorter kilosort4 --output sorting/
```

### scripts/compute_metrics.py
Computar métricas de qualidade e aplicar curação:
```bash
python scripts/compute_metrics.py sorting/ preprocessed/ --output metrics/ --curation allen
```

### scripts/export_to_phy.py
Exportar para Phy para curação manual:
```bash
python scripts/export_to_phy.py metrics/analyzer --output phy_export/
```

### assets/analysis_template.py
Template de análise completo. Copie e customize:
```bash
cp assets/analysis_template.py my_analysis.py
# Edite parâmetros e execute
python my_analysis.py
```

### reference/standard_workflow.md
Fluxo de trabalho passo a passo detalhado com explicações para cada etapa.

### reference/api_reference.md
Referência rápida de funções organizada por módulo.

### reference/plotting_guide.md
Guia abrangente de visualização para figuras em qualidade de publicação.

## Guias de referência detalhados

| Tópico | Referência |
|--------|-----------|
| Fluxo de trabalho completo | [reference/standard_workflow.md](reference/standard_workflow.md) |
| Referência de API | [reference/api_reference.md](reference/api_reference.md) |
| Guia de plotting | [reference/plotting_guide.md](reference/plotting_guide.md) |
| Pré-processamento | [PREPROCESSING.md](PREPROCESSING.md) |
| Spike sorting | [SPIKE_SORTING.md](SPIKE_SORTING.md) |
| Correção de movimento | [MOTION_CORRECTION.md](MOTION_CORRECTION.md) |
| Métricas de qualidade | [QUALITY_METRICS.md](QUALITY_METRICS.md) |
| Curação automatizada | [AUTOMATED_CURATION.md](AUTOMATED_CURATION.md) |
| Curação assistida por IA | [AI_CURATION.md](AI_CURATION.md) |
| Análise de waveform | [ANALYSIS.md](ANALYSIS.md) |

## Instalação

```bash
# Pacotes core
pip install spikeinterface[full] probeinterface neo

# Spike sorters
pip install kilosort          # Kilosort4 (GPU requerida)
pip install spykingcircus     # SpykingCircus2 (CPU)
pip install mountainsort5     # Mountainsort5 (CPU)

# Nossa toolkit
pip install neuropixels-analysis

# Opcional: Curação com IA
pip install anthropic

# Opcional: Ferramentas IBL
pip install ibl-neuropixel ibllib
```

## Estrutura de projeto

```
project/
├── raw_data/
│   └── recording_g0/
│       └── recording_g0_imec0/
│           ├── recording_g0_t0.imec0.ap.bin
│           └── recording_g0_t0.imec0.ap.meta
├── preprocessed/           # Gravação pré-processada salva
├── motion/                 # Resultados estimação de movimento
├── sorting_output/         # Saída spike sorter
├── analyzer/               # SortingAnalyzer (waveforms, métricas)
├── phy_export/             # Para curação manual
├── ai_curation/            # Relatórios análise IA
└── results/
    ├── quality_metrics.csv
    ├── curation_labels.json
    └── output.nwb
```

## Recursos adicionais

- **SpikeInterface Docs**: https://spikeinterface.readthedocs.io/
- **Neuropixels Tutorial**: https://spikeinterface.readthedocs.io/en/stable/how_to/analyze_neuropixels.html
- **Kilosort4 GitHub**: https://github.com/MouseLand/Kilosort
- **IBL Neuropixel Tools**: https://github.com/int-brain-lab/ibl-neuropixel
- **Allen Institute ecephys**: https://github.com/AllenInstitute/ecephys_spike_sorting
- **Bombcell (Automated QC)**: https://github.com/Julie-Fabre/bombcell
- **SpikeAgent (AI Curation)**: https://github.com/SpikeAgent/SpikeAgent