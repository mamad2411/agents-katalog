---
name: pyopenms
description: Interface Python para OpenMS para análise de dados de espectrometria de massa. Use para workflows de proteômica e metabolômica LC-MS/MS, incluindo manipulação de arquivos (mzML, mzXML, mzTab, FASTA, pepXML, protXML, mzIdentML), processamento de sinais, detecção de features, identificação de peptídeos e análise quantitativa. Aplique ao trabalhar com dados de espectrometria de massa, analisar experimentos de proteômica ou processar datasets de metabolômica.
---

# PyOpenMS

## Visão Geral

PyOpenMS fornece bindings Python para a biblioteca OpenMS de espectrometria de massa computacional, permitindo análise de dados de proteômica e metabolômica. Use para manipular formatos de arquivo de espectrometria de massa, processar dados espectrais, detectar features, identificar peptídeos/proteínas e realizar análise quantitativa.

## Instalação

Instale usando uv:

```bash
uv uv pip install pyopenms
```

Verifique a instalação:

```python
import pyopenms
print(pyopenms.__version__)
```

## Capacidades Principais

PyOpenMS organiza funcionalidades nestos domínios:

### 1. I/O de Arquivos e Formatos de Dados

Manipule formatos de arquivo de espectrometria de massa e converta entre representações.

**Formatos suportados**: mzML, mzXML, TraML, mzTab, FASTA, pepXML, protXML, mzIdentML, featureXML, consensusXML, idXML

Leitura básica de arquivo:

```python
import pyopenms as ms

# Ler arquivo mzML
exp = ms.MSExperiment()
ms.MzMLFile().load("data.mzML", exp)

# Acessar espectros
for spectrum in exp:
    mz, intensity = spectrum.get_peaks()
    print(f"Spectrum: {len(mz)} peaks")
```

**Para manipulação detalhada de arquivos**: Veja `references/file_io.md`

### 2. Processamento de Sinais

Processe dados espectrais brutos com suavização, filtragem, centroiding e normalização.

Processamento básico de espectro:

```python
# Suavizar espectro com filtro Gaussiano
gaussian = ms.GaussFilter()
params = gaussian.getParameters()
params.setValue("gaussian_width", 0.1)
gaussian.setParameters(params)
gaussian.filterExperiment(exp)
```

**Para detalhes de algoritmos**: Veja `references/signal_processing.md`

### 3. Detecção de Features

Detecte e vincule features entre espectros e amostras para análise quantitativa.

```python
# Detectar features
ff = ms.FeatureFinder()
ff.run("centroided", exp, features, params, ms.FeatureMap())
```

**Para workflows completos**: Veja `references/feature_detection.md`

### 4. Identificação de Peptídeos e Proteínas

Integre com search engines e processe resultados de identificação.

**Engines suportados**: Comet, Mascot, MSGFPlus, XTandem, OMSSA, Myrimatch

Workflow básico de identificação:

```python
# Carregar dados de identificação
protein_ids = []
peptide_ids = []
ms.IdXMLFile().load("identifications.idXML", protein_ids, peptide_ids)

# Aplicar filtragem por FDR
fdr = ms.FalseDiscoveryRate()
fdr.apply(peptide_ids)
```

**Para workflows detalhados**: Veja `references/identification.md`

### 5. Análise de Metabolômica

Realize pré-processamento e análise de metabolômica não-direcionada.

Workflow típico:
1. Carregar e processar dados brutos
2. Detectar features
3. Alinhar tempos de retenção entre amostras
4. Vincular features ao mapa de consenso
5. Anotar com bancos de dados de compostos

**Para workflows completos de metabolômica**: Veja `references/metabolomics.md`

## Estruturas de Dados

PyOpenMS usa estes objetos principais:

- **MSExperiment**: Coleção de espectros e cromatogramas
- **MSSpectrum**: Espectro de massa único com pares m/z e intensidade
- **MSChromatogram**: Traço cromatográfico
- **Feature**: Pico cromatográfico detectado com métricas de qualidade
- **FeatureMap**: Coleção de features
- **PeptideIdentification**: Resultados de busca para peptídeos
- **ProteinIdentification**: Resultados de busca para proteínas

**Para documentação detalhada**: Veja `references/data_structures.md`

## Workflows Comuns

### Início Rápido: Carregar e Explorar Dados

```python
import pyopenms as ms

# Carregar arquivo mzML
exp = ms.MSExperiment()
ms.MzMLFile().load("sample.mzML", exp)

# Obter estatísticas básicas
print(f"Number of spectra: {exp.getNrSpectra()}")
print(f"Number of chromatograms: {exp.getNrChromatograms()}")

# Examinar primeiro espectro
spec = exp.getSpectrum(0)
print(f"MS level: {spec.getMSLevel()}")
print(f"Retention time: {spec.getRT()}")
mz, intensity = spec.get_peaks()
print(f"Peaks: {len(mz)}")
```

### Gerenciamento de Parâmetros

A maioria dos algoritmos usa um sistema de parâmetros:

```python
# Obter parâmetros do algoritmo
algo = ms.GaussFilter()
params = algo.getParameters()

# Visualizar parâmetros disponíveis
for param in params.keys():
    print(f"{param}: {params.getValue(param)}")

# Modificar parâmetros
params.setValue("gaussian_width", 0.2)
algo.setParameters(params)
```

### Exportar para Pandas

Converta dados em DataFrames pandas para análise:

```python
import pyopenms as ms
import pandas as pd

# Carregar mapa de features
fm = ms.FeatureMap()
ms.FeatureXMLFile().load("features.featureXML", fm)

# Converter em DataFrame
df = fm.get_df()
print(df.head())
```

## Integração com Outras Ferramentas

PyOpenMS integra-se com:
- **Pandas**: Exportar dados para DataFrames
- **NumPy**: Trabalhar com arrays de picos
- **Scikit-learn**: Machine learning em dados de MS
- **Matplotlib/Seaborn**: Visualização
- **R**: Via bridge rpy2

## Recursos

- **Documentação oficial**: https://pyopenms.readthedocs.io
- **Documentação OpenMS**: https://www.openms.org
- **GitHub**: https://github.com/OpenMS/OpenMS

## Referências

- `references/file_io.md` - Manipulação abrangente de formatos de arquivo
- `references/signal_processing.md` - Algoritmos de processamento de sinais
- `references/feature_detection.md` - Detecção e vinculação de features
- `references/identification.md` - Identificação de peptídeos e proteínas
- `references/metabolomics.md` - Workflows específicos de metabolômica
- `references/data_structures.md` - Objetos principais e estruturas de dados