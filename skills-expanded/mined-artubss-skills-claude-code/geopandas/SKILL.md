---
name: geopandas
description: Biblioteca Python para trabalhar com dados vetoriais geoespaciais, incluindo shapefiles, GeoJSON e arquivos GeoPackage. Use ao trabalhar com dados geográficos para análise espacial, operações geométricas, transformações de coordenadas, spatial joins, operações de overlay, mapeamento coroplético ou qualquer tarefa envolvendo leitura/escrita/análise de dados vetoriais geográficos. Suporta bancos de dados PostGIS, mapas interativos e integração com matplotlib/folium/cartopy. Use para tarefas como análise de buffer, spatial joins entre datasets, dissolução de limites, clipping de dados, cálculo de áreas/distâncias, reprojeção de sistemas de coordenadas, criação de mapas ou conversão entre formatos de arquivos espaciais.
---

# GeoPandas

GeoPandas estende pandas para habilitar operações espaciais em tipos geométricos. Combina as capacidades de pandas e shapely para análise de dados geoespaciais.

## Instalação

```bash
uv pip install geopandas
```

### Dependências Opcionais

```bash
# Para mapas interativos
uv pip install folium

# Para esquemas de classificação em mapeamento
uv pip install mapclassify

# Para operações de I/O mais rápidas (2-4x aceleração)
uv pip install pyarrow

# Para suporte a banco de dados PostGIS
uv pip install psycopg2
uv pip install geoalchemy2

# Para mapas base
uv pip install contextily

# Para projeções cartográficas
uv pip install cartopy
```

## Início Rápido

```python
import geopandas as gpd

# Ler dados espaciais
gdf = gpd.read_file("data.geojson")

# Exploração básica
print(gdf.head())
print(gdf.crs)
print(gdf.geometry.geom_type)

# Plot simples
gdf.plot()

# Reprojetar para CRS diferente
gdf_projected = gdf.to_crs("EPSG:3857")

# Calcular área (use CRS projetado para precisão)
gdf_projected['area'] = gdf_projected.geometry.area

# Salvar em arquivo
gdf.to_file("output.gpkg")
```

## Conceitos Principais

### Estruturas de Dados

- **GeoSeries**: Vetor de geometrias com operações espaciais
- **GeoDataFrame**: Estrutura de dados tabular com coluna de geometria

Veja [data-structures.md](references/data-structures.md) para detalhes.

### Leitura e Escrita de Dados

GeoPandas lê/escreve múltiplos formatos: Shapefile, GeoJSON, GeoPackage, PostGIS, Parquet.

```python
# Ler com filtragem
gdf = gpd.read_file("data.gpkg", bbox=(xmin, ymin, xmax, ymax))

# Escrever com aceleração Arrow
gdf.to_file("output.gpkg", use_arrow=True)
```

Veja [data-io.md](references/data-io.md) para operações de I/O abrangentes.

### Sistemas de Referência de Coordenadas

Sempre verifique e gerencie CRS para operações espaciais precisas:

```python
# Verificar CRS
print(gdf.crs)

# Reprojetar (transforma coordenadas)
gdf_projected = gdf.to_crs("EPSG:3857")

# Definir CRS (apenas quando metadados faltam)
gdf = gdf.set_crs("EPSG:4326")
```

Veja [crs-management.md](references/crs-management.md) para operações de CRS.

## Operações Comuns

### Operações Geométricas

Buffer, simplificação, centroide, convex hull, transformações afins:

```python
# Buffer de 10 unidades
buffered = gdf.geometry.buffer(10)

# Simplificar com tolerância
simplified = gdf.geometry.simplify(tolerance=5, preserve_topology=True)

# Obter centroides
centroids = gdf.geometry.centroid
```

Veja [geometric-operations.md](references/geometric-operations.md) para todas as operações.

### Análise Espacial

Spatial joins, operações de overlay, dissolve:

```python
# Spatial join (intersects)
joined = gpd.sjoin(gdf1, gdf2, predicate='intersects')

# Spatial join com vizinho mais próximo
nearest = gpd.sjoin_nearest(gdf1, gdf2, max_distance=1000)

# Overlay de interseção
intersection = gpd.overlay(gdf1, gdf2, how='intersection')

# Dissolve por atributo
dissolved = gdf.dissolve(by='region', aggfunc='sum')
```

Veja [spatial-analysis.md](references/spatial-analysis.md) para operações de análise.

### Visualização

Crie mapas estáticos e interativos:

```python
# Mapa coroplético
gdf.plot(column='population', cmap='YlOrRd', legend=True)

# Mapa interativo
gdf.explore(column='population', legend=True).save('map.html')

# Mapa multicamada
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
gdf1.plot(ax=ax, color='blue')
gdf2.plot(ax=ax, color='red')
```

Veja [visualization.md](references/visualization.md) para técnicas de mapeamento.

## Documentação Detalhada

- **[Data Structures](references/data-structures.md)** - Fundamentos de GeoSeries e GeoDataFrame
- **[Data I/O](references/data-io.md)** - Leitura/escrita de arquivos, PostGIS, Parquet
- **[Geometric Operations](references/geometric-operations.md)** - Buffer, simplificação, transformações afins
- **[Spatial Analysis](references/spatial-analysis.md)** - Joins, overlay, dissolve, clipping
- **[Visualization](references/visualization.md)** - Plotting, mapas coreoplético, mapas interativos
- **[CRS Management](references/crs-management.md)** - Sistemas de referência de coordenadas e projeções

## Workflows Comuns

### Carregar, Transformar, Analisar, Exportar

```python
# 1. Carregar dados
gdf = gpd.read_file("data.shp")

# 2. Verificar e transformar CRS
print(gdf.crs)
gdf = gdf.to_crs("EPSG:3857")

# 3. Realizar análise
gdf['area'] = gdf.geometry.area
buffered = gdf.copy()
buffered['geometry'] = gdf.geometry.buffer(100)

# 4. Exportar resultados
gdf.to_file("results.gpkg", layer='original')
buffered.to_file("results.gpkg", layer='buffered')
```

### Spatial Join e Agregação

```python
# Fazer join de pontos com polígonos
points_in_polygons = gpd.sjoin(points_gdf, polygons_gdf, predicate='within')

# Agregar por polígono
aggregated = points_in_polygons.groupby('index_right').agg({
    'value': 'sum',
    'count': 'size'
})

# Fazer merge de volta com polígonos
result = polygons_gdf.merge(aggregated, left_index=True, right_index=True)
```

### Integração de Dados de Múltiplas Fontes

```python
# Ler de diferentes fontes
roads = gpd.read_file("roads.shp")
buildings = gpd.read_file("buildings.geojson")
parcels = gpd.read_postgis("SELECT * FROM parcels", con=engine, geom_col='geom')

# Garantir CRS correspondentes
buildings = buildings.to_crs(roads.crs)
parcels = parcels.to_crs(roads.crs)

# Realizar operações espaciais
buildings_near_roads = buildings[buildings.geometry.distance(roads.union_all()) < 50]
```

## Dicas de Desempenho

1. **Use spatial indexing**: GeoPandas cria índices espaciais automaticamente para a maioria das operações
2. **Filtre durante leitura**: Use parâmetros `bbox`, `mask` ou `where` para carregar apenas dados necessários
3. **Use Arrow para I/O**: Adicione `use_arrow=True` para leitura/escrita 2-4x mais rápida
4. **Simplifique geometrias**: Use `.simplify()` para reduzir complexidade quando precisão não é crítica
5. **Operações em lote**: Operações vetorizadas são muito mais rápidas que iteração de linhas
6. **Use CRS apropriado**: CRS projetado para área/distância, geográfico para visualização

## Melhores Práticas

1. **Sempre verifique CRS** antes de operações espaciais
2. **Use CRS projetado** para cálculos de área e distância
3. **Combine CRS** antes de spatial joins ou overlays
4. **Valide geometrias** com `.is_valid` antes de operações
5. **Use `.copy()`** ao modificar colunas de geometria para evitar efeitos colaterais
6. **Preserve topologia** ao simplificar para análise
7. **Use formato GeoPackage** para workflows modernos (melhor que Shapefile)
8. **Defina max_distance** em sjoin_nearest para melhor desempenho