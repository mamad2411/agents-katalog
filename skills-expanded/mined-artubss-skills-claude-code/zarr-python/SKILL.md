---
name: zarr-python
description: "Arrays N-D em chunks para armazenamento em nuvem. Arrays comprimidos, I/O paralelo, integração S3/GCS, compatível com NumPy/Dask/Xarray, para pipelines de computação científica em larga escala."
---

# Zarr Python

## Visão Geral

Zarr é uma biblioteca Python para armazenar arrays N-dimensionais grandes com chunking e compressão. Use essa habilidade para I/O paralelo eficiente, workflows nativos em nuvem e integração perfeita com NumPy, Dask e Xarray.

## Início Rápido

### Instalação

```bash
uv pip install zarr
```

Requer Python 3.11+. Para suporte a armazenamento em nuvem, instale pacotes adicionais:
```python
uv pip install s3fs  # Para S3
uv pip install gcsfs  # Para Google Cloud Storage
```

### Criação Básica de Array

```python
import zarr
import numpy as np

# Crie um array 2D com chunking e compressão
z = zarr.create_array(
    store="data/my_array.zarr",
    shape=(10000, 10000),
    chunks=(1000, 1000),
    dtype="f4"
)

# Escreva dados usando indexação estilo NumPy
z[:, :] = np.random.random((10000, 10000))

# Leia dados
data = z[0:100, 0:100]  # Retorna array NumPy
```

## Operações Principais

### Criando Arrays

Zarr oferece múltiplas funções convenientes para criação de arrays:

```python
# Crie array vazio
z = zarr.zeros(shape=(10000, 10000), chunks=(1000, 1000), dtype='f4',
               store='data.zarr')

# Crie arrays preenchidos
z = zarr.ones((5000, 5000), chunks=(500, 500))
z = zarr.full((1000, 1000), fill_value=42, chunks=(100, 100))

# Crie a partir de dados existentes
data = np.arange(10000).reshape(100, 100)
z = zarr.array(data, chunks=(10, 10), store='data.zarr')

# Crie similar a outro array
z2 = zarr.zeros_like(z)  # Corresponde shape, chunks, dtype de z
```

### Abrindo Arrays Existentes

```python
# Abra array (modo leitura/escrita por padrão)
z = zarr.open_array('data.zarr', mode='r+')

# Modo somente leitura
z = zarr.open_array('data.zarr', mode='r')

# A função open() detecta automaticamente arrays vs grupos
z = zarr.open('data.zarr')  # Retorna Array ou Group
```

### Leitura e Escrita de Dados

Arrays Zarr suportam indexação estilo NumPy:

```python
# Escreva array inteiro
z[:] = 42

# Escreva slices
z[0, :] = np.arange(100)
z[10:20, 50:60] = np.random.random((10, 10))

# Leia dados (retorna array NumPy)
data = z[0:100, 0:100]
row = z[5, :]

# Indexação avançada
z.vindex[[0, 5, 10], [2, 8, 15]]  # Indexação por coordenadas
z.oindex[0:10, [5, 10, 15]]       # Indexação ortogonal
z.blocks[0, 0]                     # Indexação por bloco/chunk
```

### Redimensionamento e Append

```python
# Redimensione array
z.resize(15000, 15000)  # Expande ou encolhe dimensões

# Adicione dados ao longo de um eixo
z.append(np.random.random((1000, 10000)), axis=0)  # Adiciona linhas
```

## Estratégias de Chunking

Chunking é crítico para desempenho. Escolha tamanhos e formas de chunk baseado em padrões de acesso.

### Diretrizes de Tamanho de Chunk

- **Tamanho mínimo de chunk**: 1 MB recomendado para desempenho ideal
- **Balanço**: Chunks maiores = menos operações de metadados; chunks menores = melhor acesso paralelo
- **Consideração de memória**: Chunks inteiros devem caber em memória durante compressão

```python
# Configure tamanho de chunk (alme por ~1MB por chunk)
# Para dados float32: 1MB = 262.144 elementos = array 512×512
z = zarr.zeros(
    shape=(10000, 10000),
    chunks=(512, 512),  # ~1MB chunks
    dtype='f4'
)
```

### Alinhando Chunks com Padrões de Acesso

**Crítico**: A forma do chunk afeta dramaticamente o desempenho baseado em como os dados são acessados.

```python
# Se acessar linhas frequentemente (primeira dimensão)
z = zarr.zeros((10000, 10000), chunks=(10, 10000))  # Chunk abrange colunas

# Se acessar colunas frequentemente (segunda dimensão)
z = zarr.zeros((10000, 10000), chunks=(10000, 10))  # Chunk abrange linhas

# Para padrões de acesso misto (abordagem balanceada)
z = zarr.zeros((10000, 10000), chunks=(1000, 1000))  # Chunks quadrados
```

**Exemplo de desempenho**: Para um array (200, 200, 200), lendo ao longo da primeira dimensão:
- Usando chunks (1, 200, 200): ~107ms
- Usando chunks (200, 200, 1): ~1.65ms (65× mais rápido!)

### Sharding para Armazenamento em Larga Escala

Quando arrays têm milhões de chunks pequenos, use sharding para agrupar chunks em objetos de armazenamento maiores:

```python
from zarr.codecs import ShardingCodec, BytesCodec
from zarr.codecs.blosc import BloscCodec

# Crie array com sharding
z = zarr.create_array(
    store='data.zarr',
    shape=(100000, 100000),
    chunks=(100, 100),  # Chunks pequenos para acesso
    shards=(1000, 1000),  # Agrupa 100 chunks por shard
    dtype='f4'
)
```

**Benefícios**:
- Reduz overhead do sistema de arquivos de milhões de pequenos arquivos
- Melhora desempenho de armazenamento em nuvem (menos requisições de objetos)
- Previne desperdício de tamanho de bloco do filesystem

**Importante**: Shards inteiros devem caber em memória antes de escrever.

## Compressão

Zarr aplica compressão por chunk para reduzir armazenamento mantendo acesso rápido.

### Configurando Compressão

```python
from zarr.codecs.blosc import BloscCodec
from zarr.codecs import GzipCodec, ZstdCodec

# Padrão: Blosc com Zstandard
z = zarr.zeros((1000, 1000), chunks=(100, 100))  # Usa compressão padrão

# Configure codec Blosc
z = zarr.create_array(
    store='data.zarr',
    shape=(1000, 1000),
    chunks=(100, 100),
    dtype='f4',
    codecs=[BloscCodec(cname='zstd', clevel=5, shuffle='shuffle')]
)

# Compressores Blosc disponíveis: 'blosclz', 'lz4', 'lz4hc', 'snappy', 'zlib', 'zstd'

# Use compressão Gzip
z = zarr.create_array(
    store='data.zarr',
    shape=(1000, 1000),
    chunks=(100, 100),
    dtype='f4',
    codecs=[GzipCodec(level=6)]
)

# Desabilite compressão
z = zarr.create_array(
    store='data.zarr',
    shape=(1000, 1000),
    chunks=(100, 100),
    dtype='f4',
    codecs=[BytesCodec()]  # Sem compressão
)
```

### Dicas de Desempenho de Compressão

- **Blosc** (padrão): Compressão/descompressão rápida, bom para workloads interativos
- **Zstandard**: Melhores taxas de compressão, ligeiramente mais lento que LZ4
- **Gzip**: Compressão máxima, desempenho mais lento
- **LZ4**: Compressão mais rápida, taxas menores
- **Shuffle**: Habilite filtro shuffle para melhor compressão em dados numéricos

```python
# Ótimo para dados científicos numéricos
codecs=[BloscCodec(cname='zstd', clevel=5, shuffle='shuffle')]

# Ótimo para velocidade
codecs=[BloscCodec(cname='lz4', clevel=1)]

# Ótimo para taxa de compressão
codecs=[GzipCodec(level=9)]
```

## Backends de Armazenamento

Zarr suporta múltiplos backends de armazenamento através de uma interface de armazenamento flexível.

### Sistema de Arquivos Local (Padrão)

```python
from zarr.storage import LocalStore

# Criação explícita de store
store = LocalStore('data/my_array.zarr')
z = zarr.open_array(store=store, mode='w', shape=(1000, 1000), chunks=(100, 100))

# Ou use caminho string (cria LocalStore automaticamente)
z = zarr.open_array('data/my_array.zarr', mode='w', shape=(1000, 1000),
                    chunks=(100, 100))
```

### Armazenamento Em Memória

```python
from zarr.storage import MemoryStore

# Crie store em memória
store = MemoryStore()
z = zarr.open_array(store=store, mode='w', shape=(1000, 1000), chunks=(100, 100))

# Dados existem apenas em memória, não persistem
```

### Armazenamento em Arquivo ZIP

```python
from zarr.storage import ZipStore

# Escreva em arquivo ZIP
store = ZipStore('data.zip', mode='w')
z = zarr.open_array(store=store, mode='w', shape=(1000, 1000), chunks=(100, 100))
z[:] = np.random.random((1000, 1000))
store.close()  # IMPORTANTE: Deve fechar ZipStore

# Leia de arquivo ZIP
store = ZipStore('data.zip', mode='r')
z = zarr.open_array(store=store)
data = z[:]
store.close()
```

### Armazenamento em Nuvem (S3, GCS)

```python
import s3fs
import zarr

# Armazenamento S3
s3 = s3fs.S3FileSystem(anon=False)  # Use credenciais
store = s3fs.S3Map(root='my-bucket/path/to/array.zarr', s3=s3)
z = zarr.open_array(store=store, mode='w', shape=(1000, 1000), chunks=(100, 100))
z[:] = data

# Google Cloud Storage
import gcsfs
gcs = gcsfs.GCSFileSystem(project='my-project')
store = gcsfs.GCSMap(root='my-bucket/path/to/array.zarr', gcs=gcs)
z = zarr.open_array(store=store, mode='w', shape=(1000, 1000), chunks=(100, 100))
```

**Melhores Práticas para Armazenamento em Nuvem**:
- Use metadados consolidados para reduzir latência: `zarr.consolidate_metadata(store)`
- Alinhe tamanhos de chunk com dimensionamento de objetos em nuvem (tipicamente 5-100 MB ótimo)
- Habilite escritas paralelas usando Dask para dados em larga escala
- Considere sharding para reduzir número de objetos

## Grupos e Hierarquias

Grupos organizam múltiplos arrays hierarquicamente, similares a diretórios ou grupos HDF5.

### Criando e Usando Grupos

```python
# Crie grupo raiz
root = zarr.group(store='data/hierarchy.zarr')

# Crie sub-grupos
temperature = root.create_group('temperature')
precipitation = root.create_group('precipitation')

# Crie arrays dentro de grupos
temp_array = temperature.create_array(
    name='t2m',
    shape=(365, 720, 1440),
    chunks=(1, 720, 1440),
    dtype='f4'
)

precip_array = precipitation.create_array(
    name='prcp',
    shape=(365, 720, 1440),
    chunks=(1, 720, 1440),
    dtype='f4'
)

# Acesse usando caminhos
array = root['temperature/t2m']

# Visualize hierarquia
print(root.tree())
# Saída:
# /
#  ├── temperature
#  │   └── t2m (365, 720, 1440) f4
#  └── precipitation
#      └── prcp (365, 720, 1440) f4
```

### API Compatível com H5py

Zarr oferece uma interface compatível com h5py para usuários familiarizados com HDF5:

```python
# Crie grupo com métodos estilo h5py
root = zarr.group('data.zarr')
dataset = root.create_dataset('my_data', shape=(1000, 1000), chunks=(100, 100),
                              dtype='f4')

# Acesse como h5py
grp = root.require_group('subgroup')
arr = grp.require_dataset('array', shape=(500, 500), chunks=(50, 50), dtype='i4')
```

## Atributos e Metadados

Anexe metadados customizados a arrays e grupos usando atributos:

```python
# Adicione atributos a array
z = zarr.zeros((1000, 1000), chunks=(100, 100))
z.attrs['description'] = 'Dados de temperatura em Kelvin'
z.attrs['units'] = 'K'
z.attrs['created'] = '2024-01-15'
z.attrs['processing_version'] = 2.1

# Atributos são armazenados como JSON
print(z.attrs['units'])  # Saída: K

# Adicione atributos a grupos
root = zarr.group('data.zarr')
root.attrs['project'] = 'Análise Climática'
root.attrs['institution'] = 'Instituto de Pesquisa'

# Atributos persistem com o array/grupo
z2 = zarr.open('data.zarr')
print(z2.attrs['description'])
```

**Importante**: Atributos devem ser serializáveis em JSON (strings, números, listas, dicts, booleanos, null).

## Integração com NumPy, Dask e Xarray

### Integração NumPy

Arrays Zarr implementam a interface de array NumPy:

```python
import numpy as np
import zarr

z = zarr.zeros((1000, 1000), chunks=(100, 100))

# Use funções NumPy diretamente
result = np.sum(z, axis=0)  # NumPy opera em array Zarr
mean = np.mean(z[:100, :100])

# Converta para array NumPy
numpy_array = z[:]  # Carrega array inteiro em memória
```

### Integração Dask

Dask oferece computação lazy e paralela em arrays Zarr:

```python
import dask.array as da
import zarr

# Crie array Zarr grande
z = zarr.open('data.zarr', mode='w', shape=(100000, 100000),
              chunks=(1000, 1000), dtype='f4')

# Carregue como array Dask (lazy, nenhum dado carregado)
dask_array = da.from_zarr('data.zarr')

# Realize computações (paralelo, fora da memória)
result = dask_array.mean(axis=0).compute()  # Computação paralela

# Escreva array Dask em Zarr
large_array = da.random.random((100000, 100000), chunks=(1000, 1000))
da.to_zarr(large_array, 'output.zarr')
```

**Benefícios**:
- Processe datasets maiores que a memória
- Computação paralela automática através de chunks
- I/O eficiente com armazenamento chunked

### Integração Xarray

Xarray oferece arrays multidimensionais rotulados com backend Zarr:

```python
import xarray as xr
import zarr

# Abra store Zarr como Dataset Xarray (carregamento lazy)
ds = xr.open_zarr('data.zarr')

# Dataset inclui coordenadas e metadados
print(ds)

# Acesse variáveis
temperature = ds['temperature']

# Realize operações rotuladas
subset = ds.sel(time='2024-01', lat=slice(30, 60))

# Escreva Dataset Xarray em Zarr
ds.to_zarr('output.zarr')

# Crie do zero com coordenadas
ds = xr.Dataset(
    {
        'temperature': (['time', 'lat', 'lon'], data),
        'precipitation': (['time', 'lat', 'lon'], data2)
    },
    coords={
        'time': pd.date_range('2024-01-01', periods=365),
        'lat': np.arange(-90, 91, 1),
        'lon': np.arange(-180, 180, 1)
    }
)
ds.to_zarr('climate_data.zarr')
```

**Benefícios**:
- Dimensões e coordenadas nomeadas
- Indexação e seleção baseada em rótulos
- Integração com pandas para séries temporais
- Interface similar a NetCDF familiar a cientistas de clima/geoespacial

## Computação Paralela e Sincronização

### Operações Thread-Safe

```python
from zarr import ThreadSynchronizer
import zarr

# Para escritas multi-thread
synchronizer = ThreadSynchronizer()
z = zarr.open_array('data.zarr', mode='r+', shape=(10000, 10000),
                    chunks=(1000, 1000), synchronizer=synchronizer)

# Seguro para escritas concorrentes de múltiplas threads
# (quando escritas não abrangem limites de chunk)
```

### Operações Process-Safe

```python
from zarr import ProcessSynchronizer
import zarr

# Para escritas multi-processo
synchronizer = ProcessSynchronizer('sync_data.sync')
z = zarr.open_array('data.zarr', mode='r+', shape=(10000, 10000),
                    chunks=(1000, 1000), synchronizer=synchronizer)

# Seguro para escritas concorrentes de múltiplos processos
```

**Nota**:
- Leituras concorrentes não requerem sincronização
- Sincronização necessária apenas para escritas que podem abranger limites de chunk
- Cada processo/thread escrevendo em chunks separados não precisa sincronização

## Metadados Consolidados

Para stores hierárquicos com muitos arrays, consolide metadados em um único arquivo para reduzir operações de I/O:

```python
import zarr

# Após criar arrays/grupos
root = zarr.group('data.zarr')
# ... crie múltiplos arrays/grupos ...

# Consolide metadados
zarr.consolidate_metadata('data.zarr')

# Abra com metadados consolidados (mais rápido, especialmente em armazenamento em nuvem)
root = zarr.open_consolidated('data.zarr')
```

**Benefícios**:
- Reduz operações de leitura de metadados de N (um por array) para 1
- Crítico para armazenamento em nuvem (reduz latência)
- Acelera operações `tree()` e traversal de grupos

**Cuidados**:
- Metadados podem ficar obsoletos se arrays atualizam sem re-consolidação
- Não adequado para datasets frequentemente atualizados
- Cenários multi-writer podem ter leituras inconsistentes

## Otimização de Desempenho

### Checklist para Desempenho Ótimo

1. **Tamanho de Chunk**: Alme por 1-10 MB por chunk
   ```python
   # Para float32: 1MB = 262.144 elementos
   chunks = (512, 512)  # 512×512×4 bytes = ~1MB
   ```

2. **Forma de Chunk**: Alinhe com padrões de acesso
   ```python
   # Acesso linha-wise → chunk abrange colunas: (pequeno, grande)
   # Acesso coluna-wise → chunk abrange linhas: (grande, pequeno)
   # Acesso aleatório → balanceado: (médio, médio)
   ```

3. **Compressão**: Escolha baseado em workload
   ```python
   # Interativo/rápido: BloscCodec(cname='lz4')
   # Balanceado: BloscCodec(cname='zstd', clevel=5)
   # Compressão máxima: GzipCodec(level=9)
   ```

4. **Backend de Armazenamento**: Corresponda ao ambiente
   ```python
   # Local: LocalStore (padrão)
   # Nuvem: S3Map/GCSMap com metadados consolidados
   # Temporário: MemoryStore
   ```

5. **Sharding**: Use para datasets em larga escala
   ```python
   # Quando você tem milhões de chunks pequenos
   shards=(10*chunk_size, 10*chunk_size)
   ```

6. **I/O Paralelo**: Use Dask para operações grandes
   ```python
   import dask.array as da
   dask_array = da.from_zarr('data.zarr')
   result = dask_array.compute(scheduler='threads', num_workers=8)
   ```

### Profiling e Debug

```python
# Imprima informações detalhadas de array
print(z.info)

# Saída inclui:
# - Tipo, shape, chunks, dtype
# - Codec de compressão e nível
# - Tamanho de armazenamento (comprimido vs descomprimido)
# - Local de armazenamento

# Verifique tamanho de armazenamento
print(f"Tamanho comprimido: {z.nbytes_stored / 1e6:.2f} MB")
print(f"Tamanho descomprimido: {z.nbytes / 1e6:.2f} MB")
print(f"Taxa de compressão: {z.nbytes / z.nbytes_stored:.2f}x")
```

## Padrões Comuns e Melhores Práticas

### Padrão: Dados de Série Temporal

```python
# Armazene série temporal com tempo como primeira dimensão
# Isso permite append eficiente de novos passos de tempo
z = zarr.open('timeseries.zarr', mode='a',
              shape=(0, 720, 1440),  # Comece com 0 passos de tempo
              chunks=(1, 720, 1440),  # Um passo de tempo por chunk
              dtype='f4')

# Adicione novos passos de tempo
new_data = np.random.random((1, 720, 1440))
z.append(new_data, axis=0)
```

### Padrão: Operações de Matriz Grande

```python
import dask.array as da

# Crie matriz grande em Zarr
z = zarr.open('matrix.zarr', mode='w',
              shape=(100000, 100000),
              chunks=(1000, 1000),
              dtype='f8')

# Use Dask para computação paralela
dask_z = da.from_zarr('matrix.zarr')
result = (dask_z @ dask_z.T).compute()  # Multiplicação de matriz paralela
```

### Padrão: Workflow Nativo em Nuvem

```python
import s3fs
import zarr

# Escreva em S3
s3 = s3fs.S3FileSystem()
store = s3fs.S3Map(root='s3://my-bucket/data.zarr', s3=s3)

# Crie array com chunking apropriado para nuvem
z = zarr.open_array(store=store, mode='w',
                    shape=(10000, 10000),
                    chunks=(500, 500),  # ~1MB chunks
                    dtype='f4')
z[:] = data

# Consolide metadados para leituras mais rápidas
zarr.consolidate_metadata(store)

# Leia de S3 (de qualquer lugar, qualquer hora)
store_read = s3fs.S3Map(root='s3://my-bucket/data.zarr', s3=s3)
z_read = zarr.open_consolidated(store_read)
subset = z_read[0:100, 0:100]
```

### Padrão: Conversão de Formato

```python
# HDF5 para Zarr
import h5py
import zarr

with h5py.File('data.h5', 'r') as h5:
    dataset = h5['dataset_name']
    z = zarr.array(dataset[:],
                   chunks=(1000, 1000),
                   store='data.zarr')

# NumPy para Zarr
import numpy as np
data = np.load('data.npy')
z = zarr.array(data, chunks='auto', store='data.zarr')

# Zarr para NetCDF (via Xarray)
import xarray as xr
ds = xr.open_zarr('data.zarr')
ds.to_netcdf('data.nc')
```

## Problemas Comuns e Soluções

### Problema: Desempenho Lento

**Diagnóstico**: Verifique tamanho de chunk e alinhamento
```python
print(z.chunks)  # Chunks são tamanho apropriado?
print(z.info)    # Verifique taxa de compressão
```

**Soluções**:
- Aumente tamanho de chunk para 1-10 MB
- Alinhe chunks com padrão de acesso
- Teste diferentes codecs de compressão
- Use Dask para operações paralelas

### Problema: Alto Uso de Memória

**Causa**: Carregando array inteiro ou chunks grandes em memória

**Soluções**:
```python
# Não carregue array inteiro
# Ruim: data = z[:]
# Bom: Processe em chunks
for i in range(0, z.shape[0], 1000):
    chunk = z[i:i+1000, :]
    process(chunk)

# Ou use Dask para chunking automático
import dask.array as da
dask_z = da.from_zarr('data.zarr')
result = dask_z.mean().compute()  # Processa em chunks
```

### Problema: Latência de Armazenamento em Nuvem

**Soluções**:
```python
# 1. Consolide metadados
zarr.consolidate_metadata(store)
z = zarr.open_consolidated(store)

# 2. Use tamanhos de chunk apropriados (5-100 MB para nuvem)
chunks = (2000, 2000)  # Chunks maiores para nuvem

# 3. Habilite sharding
shards = (10000, 10000)  # Agrupa muitos chunks
```

### Problema: Conflitos de Escrita Concorrente

**Solução**: Use sincronizadores ou garanta escritas não-sobrepostas
```python
from zarr import ProcessSynchronizer

sync = ProcessSynchronizer('sync.sync')
z = zarr.open_array('data.zarr', mode='r+', synchronizer=sync)

# Ou projete workflow para que cada processo escreva em chunks separados
```

## Recursos Adicionais

Para documentação de API detalhada, uso avançado e últimas atualizações:

- **Documentação Oficial**: https://zarr.readthedocs.io/
- **Especificações Zarr**: https://zarr-specs.readthedocs.io/
- **Repositório GitHub**: https://github.com/zarr-developers/zarr-python
- **Chat Comunitário**: https://gitter.im/zarr-developers/community

**Bibliotecas Relacionadas**:
- **Xarray**: https://docs.xarray.dev/ (arrays rotulados)
- **Dask**: https://docs.dask.org/ (computação paralela)
- **NumCodecs**: https://numcodecs.readthedocs.io/ (codecs de compressão)