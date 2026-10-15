---
name: map-creator
description: 根据用户给出的城市、地点列表、地址表或已有 POI JSON，生成 GIS/OSM 城市导览地图、打卡地图、街区指南、小酒馆/咖啡/餐饮点位地图，并可选用 GPT Image 做风格化。用户要求“出一张地图”“生成城市点位图”“检查点位对齐”“用高德解析地址”“做 OSM/GIS 底图”“风格化地图海报”时使用。
---

# map-creator

在仓库根目录执行命令。当前项目是扁平化 skill 工具包，主要代码在 `guide_maps/`。

## 主流程

1. 从用户请求中提取：
   - `city`：城市名。
   - `places`：地点名或地址，保持用户给出的顺序。
   - `title`：地图标题；如果用户没给，按主题补一个简短标题。
   - 可选 `road_labels`：用户特别关心的道路名，只作为自动道路名筛选的加权提示，不是白名单。

2. 从地点名生成 GIS 地图草稿：

```bash
python -m guide_maps.cli.create_gis_map --city <城市> --places "<地点1>" "<地点2>" --title "<标题>"
```

3. 从已有 POI JSON 生成 GIS 地图草稿：

```bash
python -m guide_maps.cli.create_gis_map --city <城市> --poi-json <poi.json> --title "<标题>"
```

4. 如需保存解析结果以便复查，加入：

```bash
--save-poi-json outputs/poi_sets/<name>.json
```

5. GIS 草稿输出到：

```text
outputs/posters/
```

## 配置

从 `config.local.json` 读取本地 key；该文件已被忽略，不要提交真实 key。

- 高德：`amap.api_key`，也可用环境变量 `AMAP_KEY`。
- GPT Image：`gpt_image.api_key`，也可用环境变量 `OPENAI_API_KEY` 或 `GPT_IMAGE_API_KEY`。

`config.example.json` 只保留字段结构，不要写真实 key。

## POI 解析规则

1. 优先尝试本地 AMap CLI；不可用时使用高德 Web API。
2. 高德返回 GCJ-02 坐标。
3. 渲染前转换为 WGS84，以匹配 OSMnx / OpenStreetMap 坐标系。
4. 保存可复查字段：输入名、解析名、地址、区县、候选结果、置信度、WGS84 坐标。
5. 左侧索引的小字优先使用高德候选中的 `formatted_address` 或 `address`，并去掉省市前缀。

相关代码：

- `guide_maps/cli/create_gis_map.py`
- `guide_maps/geocoding/workflow.py`
- `guide_maps/geocoding/poi_resolver.py`
- `guide_maps/geocoding/coordinate_transform.py`
- `guide_maps/geocoding/poi_io.py`

## 地图范围方法

1. 将 POI 投影到本地 UTM。
2. 计算点位包围盒。
3. 添加 padding。
4. 强制使用 16:10 或 16:9 的目标画幅。
5. 计算中心点和 OSM 抓取半径 `dist`。
6. `dist > 3200` 判定为大范围地图。

大范围地图：

- 路网使用 `drive` network type。
- 减少生活方式 POI。
- 道路名数量更少。

小范围地图：

- 路网使用 `walk` network type。
- 显示步行路、建筑、公园、水体和生活方式 POI。

## OSM 数据获取

Overpass API 在中国大陆可能很慢。当前实现会：

1. 单独请求一次 OSM 路网。
2. 把建筑、公园、水体、生活方式 POI、交通点等 features 合并成一次 Overpass 请求。
3. 在本地拆分图层。
4. 缓存到 `cache/`，后续同一区域会复用缓存。

相关代码：

- `guide_maps/rendering/osm_context_style.py`
- `guide_maps/rendering/osm_context_map_template.py`

## GIS 渲染要求

地图应至少包含：

- 底色。
- 水系。
- 公园绿地。
- 建筑轮廓。
- 道路网络。
- 目标点编号。
- 目标点旁边的地点名。
- 左侧索引：编号、地点名、地址。
- 公园名称。
- 自动道路名。
- 标题。

不要在左侧 legend 区渲染地图底图元素。不要显示 subtitle；如果用户提供 subtitle，当前版本先忽略。

## 道路名筛选

不要把 `--road-labels` 当作白名单。道路名采用自动筛选：

1. 从当前画面内可见路网中找候选道路。
2. 按道路等级、可见长度、用户提示道路加权排序。
3. 大范围地图最多显示约 5 个道路名，小范围地图最多约 7 个。
4. 排除快速路、隧道、立交、内环、铁路、地铁、城际、各种“线”等不适合导览图的道路名。
5. 道路名必须避让点位名和公园名；放不下就跳过。

如果用户明确不要道路名，使用：

```bash
--no-road-labels
```

## 标签避让

使用 `LabelPlacer` 做文本避让：

1. 先注册左侧索引、标题、点位圆点等已占用区域。
2. 再放 POI 名。
3. 再放公园名。
4. 最后放道路名。
5. 如果候选位置和已有文本重叠，尝试下一个位置。
6. 放不下时宁可跳过，也不要压住重要信息。

## GPT Image 风格化

当用户要求“风格化”“海报化”“AI 重绘”时，在 GIS 草稿完成后运行：

```bash
python -m guide_maps.cli.style_poster_with_gpt_image --input outputs/posters/<draft>.png
```

提示词模板在：

```text
prompts/map_style_templates/
```

没有 GPT Image key 时，不要阻塞 GIS 草稿生成；提示用户可先使用 `outputs/posters/` 中的草稿。

## 常用命令

从地点名生成：

```bash
python -m guide_maps.cli.create_gis_map --city 南京 --places "地点1" "地点2" --title "南京小酒馆地图"
```

从 POI JSON 生成：

```bash
python -m guide_maps.cli.create_gis_map --city 南京 --poi-json outputs/poi_sets/nanjing_bars_no_baijiahu.json --title "南京小酒馆地图"
```

提示重点道路名：

```bash
python -m guide_maps.cli.create_gis_map --city 南京 --poi-json <poi.json> --title "南京小酒馆地图" --road-labels 长江路 石鼓路 应天大街
```

关闭道路名：

```bash
python -m guide_maps.cli.create_gis_map --city 南京 --poi-json <poi.json> --title "南京小酒馆地图" --no-road-labels
```

## 测试

```bash
python -m compileall guide_maps tests
python -m pytest tests
```

地图输出后需要目视检查：

- 点位是否落在正确街区。
- 编号和左侧索引是否一一对应。
- 道路名、公园名和 POI 名是否互相遮挡。
- 大范围地图是否没有挤太多细节。
- 建筑层是否没有压住点位和道路。
