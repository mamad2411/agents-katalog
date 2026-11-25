---
name: neurokit2
description: Kit de ferramentas abrangente de processamento de biossinais para análise de dados fisiológicos incluindo sinais de ECG, EEG, EDA, RSP, PPG, EMG e EOG. Use esta skill ao processar sinais cardiovasculares, atividade cerebral, respostas eletrodérmicas, padrões respiratórios, atividade muscular ou movimentos oculares. Aplicável para análise de variabilidade da frequência cardíaca, potenciais relacionados a eventos, medidas de complexidade, avaliação do sistema nervoso autônomo, pesquisa psicofisiológica e integração multimodal de sinais fisiológicos.
---

# NeuroKit2

## Visão Geral

NeuroKit2 é um kit de ferramentas Python abrangente para processamento e análise de sinais fisiológicos (biossinais). Use esta skill para processar sinais cardiovasculares, neurais, autonômicos, respiratórios e musculares em pesquisas psicofisiológicas, aplicações clínicas e estudos de interação humano-computador.

## Quando Usar Esta Skill

Aplique esta skill ao trabalhar com:
- **Sinais cardíacos**: ECG, PPG, variabilidade da frequência cardíaca (HRV), análise de pulso
- **Sinais cerebrais**: Bandas de frequência de EEG, microstados, complexidade, localização de fonte
- **Sinais autonômicos**: Atividade eletrodérmica (EDA/GSR), respostas de condutância de pele (SCR)
- **Sinais respiratórios**: Frequência respiratória, variabilidade respiratória (RRV), volume por tempo
- **Sinais musculares**: Amplitude EMG, detecção de ativação muscular
- **Rastreamento ocular**: EOG, detecção e análise de piscadas
- **Integração multimodal**: Processamento de múltiplos sinais fisiológicos simultaneamente
- **Análise de complexidade**: Medidas de entropia, dimensões fractais, dinâmica não-linear

## Capacidades Principais

### 1. Processamento de Sinais Cardíacos (ECG/PPG)

Processe sinais de eletrocardiograma e fotopletismografia para análise cardiovascular. Consulte `references/ecg_cardiac.md` para workflows detalhados.

**Workflows principais:**
- Pipeline de processamento ECG: limpeza → detecção de onda R → delineação → avaliação de qualidade
- Análise HRV em domínios temporal, frequencial e não-linear
- Análise de pulso PPG e avaliação de qualidade
- Extração de respiração derivada de ECG

**Funções principais:**
```python
import neurokit2 as nk

# Pipeline completo de processamento ECG
signals, info = nk.ecg_process(ecg_signal, sampling_rate=1000)

# Analisar dados de ECG (relacionados a eventos ou intervalos)
analysis = nk.ecg_analyze(signals, sampling_rate=1000)

# Análise abrangente de HRV
hrv = nk.hrv(peaks, sampling_rate=1000)  # Domínios temporal, frequencial e não-linear
```

### 2. Análise de Variabilidade da Frequência Cardíaca

Calcule métricas abrangentes de HRV a partir de sinais cardíacos. Consulte `references/hrv.md` para todos os índices e análise específica por domínio.

**Domínios suportados:**
- **Domínio temporal**: SDNN, RMSSD, pNN50, SDSD e métricas derivadas
- **Domínio frequencial**: Potência ULF, VLF, LF, HF, VHF e razões
- **Domínio não-linear**: Gráfico de Poincaré (SD1/SD2), medidas de entropia, dimensões fractais
- **Especializado**: Arritmia sinusal respiratória (RSA), análise de quantificação de recorrência (RQA)

**Funções principais:**
```python
# Todos os índices HRV de uma vez
hrv_indices = nk.hrv(peaks, sampling_rate=1000)

# Análise específica por domínio
hrv_time = nk.hrv_time(peaks)
hrv_freq = nk.hrv_frequency(peaks, sampling_rate=1000)
hrv_nonlinear = nk.hrv_nonlinear(peaks, sampling_rate=1000)
hrv_rsa = nk.hrv_rsa(peaks, rsp_signal, sampling_rate=1000)
```

### 3. Análise de Sinais Cerebrais (EEG)

Analise sinais de eletroencefalograma para potência de frequência, complexidade e padrões de microstados. Consulte `references/eeg.md` para workflows detalhados e integração com MNE.

**Capacidades principais:**
- Análise de potência de banda de frequência (Delta, Theta, Alpha, Beta, Gamma)
- Avaliação de qualidade de canal e re-referência
- Localização de fonte (sLORETA, MNE)
- Segmentação de microstados e dinâmica de transição
- Potência de campo global e medidas de dissimilaridade

**Funções principais:**
```python
# Análise de potência em bandas de frequência
power = nk.eeg_power(eeg_data, sampling_rate=250, channels=['Fz', 'Cz', 'Pz'])

# Análise de microstados
microstates = nk.microstates_segment(eeg_data, n_microstates=4, method='kmod')
static = nk.microstates_static(microstates)
dynamic = nk.microstates_dynamic(microstates)
```

### 4. Atividade Eletrodérmica (EDA)

Processe sinais de condutância de pele para avaliação do sistema nervoso autônomo. Consulte `references/eda.md` para workflows detalhados.

**Workflows principais:**
- Decomposição de sinais em componentes tônico e fásico
- Detecção e análise de resposta de condutância de pele (SCR)
- Cálculo de índice do sistema nervoso simpático
- Detecção de autocorrelação e ponto de mudança

**Funções principais:**
```python
# Processamento completo de EDA
signals, info = nk.eda_process(eda_signal, sampling_rate=100)

# Analisar dados de EDA
analysis = nk.eda_analyze(signals, sampling_rate=100)

# Atividade do sistema nervoso simpático
sympathetic = nk.eda_sympathetic(signals, sampling_rate=100)
```

### 5. Processamento de Sinais Respiratórios (RSP)

Analise padrões de respiração e variabilidade respiratória. Consulte `references/rsp.md` para workflows detalhados.

**Capacidades principais:**
- Cálculo de frequência respiratória e análise de variabilidade
- Avaliação de amplitude e simetria da respiração
- Volume respiratório por tempo (aplicações em fMRI)
- Variabilidade de amplitude respiratória (RAV)

**Funções principais:**
```python
# Processamento completo de RSP
signals, info = nk.rsp_process(rsp_signal, sampling_rate=100)

# Variabilidade da frequência respiratória
rrv = nk.rsp_rrv(signals, sampling_rate=100)

# Volume respiratório por tempo
rvt = nk.rsp_rvt(signals, sampling_rate=100)
```

### 6. Eletromiografia (EMG)

Processe sinais de atividade muscular para detecção de ativação e análise de amplitude. Consulte `references/emg.md` para workflows.

**Funções principais:**
```python
# Processamento completo de EMG
signals, info = nk.emg_process(emg_signal, sampling_rate=1000)

# Detecção de ativação muscular
activation = nk.emg_activation(signals, sampling_rate=1000, method='threshold')
```

### 7. Eletro-oculografia (EOG)

Analise padrões de movimento ocular e piscadas. Consulte `references/eog.md` para workflows.

**Funções principais:**
```python
# Processamento completo de EOG
signals, info = nk.eog_process(eog_signal, sampling_rate=500)

# Extrair características de piscadas
features = nk.eog_features(signals, sampling_rate=500)
```

### 8. Processamento Geral de Sinais

Aplique operações de filtragem, decomposição e transformação a qualquer sinal. Consulte `references/signal_processing.md` para utilitários abrangentes.

**Operações principais:**
- Filtragem (passa-baixas, passa-altas, passa-banda, rejeita-banda)
- Decomposição (EMD, SSA, wavelet)
- Detecção e correção de picos
- Estimativa de densidade espectral de potência
- Interpolação e reamostragem de sinais
- Análise de autocorrelação e sincronização

**Funções principais:**
```python
# Filtragem
filtered = nk.signal_filter(signal, sampling_rate=1000, lowcut=0.5, highcut=40)

# Detecção de picos
peaks = nk.signal_findpeaks(signal)

# Densidade espectral de potência
psd = nk.signal_psd(signal, sampling_rate=1000)
```

### 9. Análise de Complexidade e Entropia

Calcule dinâmica não-linear, dimensões fractais e medidas de teoria da informação. Consulte `references/complexity.md` para todas as métricas disponíveis.

**Medidas disponíveis:**
- **Entropia**: Shannon, aproximada, amostra, permutação, espectral, fuzzy, multiscala
- **Dimensões fractais**: Katz, Higuchi, Petrosian, Sevcik, dimensão de correlação
- **Dinâmica não-linear**: Expoentes de Lyapunov, complexidade de Lempel-Ziv, quantificação de recorrência
- **DFA**: Análise de flutuação destendenciada, DFA multifractal
- **Teoria da informação**: Informação de Fisher, informação mútua

**Funções principais:**
```python
# Múltiplas métricas de complexidade de uma vez
complexity_indices = nk.complexity(signal, sampling_rate=1000)

# Medidas específicas
apen = nk.entropy_approximate(signal)
dfa = nk.fractal_dfa(signal)
lyap = nk.complexity_lyapunov(signal, sampling_rate=1000)
```

### 10. Análise Relacionada a Eventos

Crie épocas em torno de eventos de estímulo e analise respostas fisiológicas. Consulte `references/epochs_events.md` para workflows.

**Capacidades principais:**
- Criação de épocas a partir de marcadores de evento
- Média relacionada a evento e visualização
- Opções de correção de linha de base
- Computação de grande média com intervalos de confiança

**Funções principais:**
```python
# Encontrar eventos no sinal
events = nk.events_find(trigger_signal, threshold=0.5)

# Criar épocas em torno de eventos
epochs = nk.epochs_create(signals, events, sampling_rate=1000,
                          epochs_start=-0.5, epochs_end=2.0)

# Média em épocas
grand_average = nk.epochs_average(epochs)
```

### 11. Integração de Múltiplos Sinais

Processe múltiplos sinais fisiológicos simultaneamente com saída unificada. Consulte `references/bio_module.md` para workflows de integração.

**Funções principais:**
```python
# Processar múltiplos sinais de uma vez
bio_signals, bio_info = nk.bio_process(
    ecg=ecg_signal,
    rsp=rsp_signal,
    eda=eda_signal,
    emg=emg_signal,
    sampling_rate=1000
)

# Analisar todos os sinais processados
bio_analysis = nk.bio_analyze(bio_signals, sampling_rate=1000)
```

## Modos de Análise

NeuroKit2 seleciona automaticamente entre dois modos de análise baseado na duração dos dados:

**Análise relacionada a eventos** (< 10 segundos):
- Analisa respostas fixadas a estímulos
- Segmentação baseada em épocas
- Adequado para paradigmas experimentais com tentativas discretas

**Análise relacionada a intervalos** (≥ 10 segundos):
- Caracteriza padrões fisiológicos ao longo de períodos estendidos
- Estado de repouso ou atividades contínuas
- Adequado para medições de linha de base e monitoramento de longo prazo

A maioria das funções `*_analyze()` escolhe automaticamente o modo apropriado.

## Instalação

```bash
uv pip install neurokit2
```

Para versão de desenvolvimento:
```bash
uv pip install https://github.com/neuropsychology/NeuroKit/zipball/dev
```

## Workflows Comuns

### Início Rápido: Análise de ECG
```python
import neurokit2 as nk

# Carregar dados de exemplo
ecg = nk.ecg_simulate(duration=60, sampling_rate=1000)

# Processar ECG
signals, info = nk.ecg_process(ecg, sampling_rate=1000)

# Analisar HRV
hrv = nk.hrv(info['ECG_R_Peaks'], sampling_rate=1000)

# Visualizar
nk.ecg_plot(signals, info)
```

### Análise Multimodal
```python
# Processar múltiplos sinais
bio_signals, bio_info = nk.bio_process(
    ecg=ecg_signal,
    rsp=rsp_signal,
    eda=eda_signal,
    sampling_rate=1000
)

# Analisar todos os sinais
results = nk.bio_analyze(bio_signals, sampling_rate=1000)
```

### Potencial Relacionado a Evento
```python
# Encontrar eventos
events = nk.events_find(trigger_channel, threshold=0.5)

# Criar épocas
epochs = nk.epochs_create(processed_signals, events,
                          sampling_rate=1000,
                          epochs_start=-0.5, epochs_end=2.0)

# Análise relacionada a evento para cada tipo de sinal
ecg_epochs = nk.ecg_eventrelated(epochs)
eda_epochs = nk.eda_eventrelated(epochs)
```

## Referências

Esta skill inclui documentação abrangente de referência organizada por tipo de sinal e método de análise:

- **ecg_cardiac.md**: Processamento ECG/PPG, detecção de onda R, delineação, avaliação de qualidade
- **hrv.md**: Índices de variabilidade da frequência cardíaca em todos os domínios
- **eeg.md**: Análise de EEG, bandas de frequência, microstados, localização de fonte
- **eda.md**: Processamento de atividade eletrodérmica e análise de SCR
- **rsp.md**: Processamento de sinais respiratórios e variabilidade
- **ppg.md**: Análise de sinais de fotopletismografia
- **emg.md**: Processamento de eletromiografia e detecção de ativação
- **eog.md**: Eletro-oculografia e análise de piscadas
- **signal_processing.md**: Utilitários gerais de sinal e transformações
- **complexity.md**: Medidas de entropia, fractal e não-linear
- **epochs_events.md**: Análise relacionada a evento e criação de épocas
- **bio_module.md**: Workflows de integração multimodal de sinais

Carregue arquivos de referência específicos conforme necessário usando a ferramenta de leitura para acessar documentação detalhada de funções e parâmetros.

## Recursos Adicionais

- Documentação Oficial: https://neuropsychology.github.io/NeuroKit/
- Repositório GitHub: https://github.com/neuropsychology/NeuroKit
- Publicação: Makowski et al. (2021). NeuroKit2: A Python toolbox for neurophysiological signal processing. Behavior Research Methods. https://doi.org/10.3758/s13428-020-01516-y