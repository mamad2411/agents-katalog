---
name: mapv-three-skills
description: 使用 MapV-Three 构建专业的 3D 地图和 GIS 应用 - 基于 Three.js 的 3D 地图渲染引擎，支持天空环境、底图加载、3DTiles、可视化组件、LBS服务、模型资产、GIS分析、编辑测量等完整地图开发能力。适用于创建 3D 数字孪生、城市可视化、GIS 分析等 Web 应用。
license: MIT
version: 1.0.0
---

# MapV-Three 3D 地图开发指南

MapV-Three 是基于 Three.js 的专业 3D 地图渲染引擎（@baidu/mapv-three），提供从底图加载、天空环境、3DTiles、可视化组件到 GIS 空间分析的完整 3D 地图开发能力。

## 何时适用

- 使用 MapV-Three 创建 3D 地图应用、数字孪生、城市可视化
- 加载和配置底图（百度、Bing、OSM、天地图、WMS/WMTS 等）
- 使用天空环境和天气系统（物理天空、动态天空、雨雪雷暴等）
- 加载 3DTiles 数据（建筑、高精地图、交通地图）
- 使用可视化组件（点、线、面、热力图、飞线等）
- 加载 3D 模型和设备资产（GLTF、实例化渲染、LOD）
- 使用 LBS 服务（地理编码、路线规划、POI 搜索）
- 进行 GIS 空间分析（通视、视域、淹没、坡度、体积等）
- 使用编辑和测量工具（绘制、编辑、长度/面积测量）
- 管理数据源和动画追踪系统

## 代码生成原则（必须在查阅参考文档前先读完本节）

生成 mapv-three 代码时必须遵守以下原则：

1. **最小改动**：只给用户请求的功能代码，不堆砌额外参数。例如用户说"添加动态天空"，只给 `engine.add(new mapvthree.DynamicSky())`，不要附带 `cloudsCoverage`、`affectWorld` 等高级参数。
2. **默认天空冲突**：Engine 自带默认天空。添加自定义天空（DynamicSky 等）时，必须在 Engine 配置中设置 `rendering: { sky: null }`，否则两个天空会叠加。
3. **交互确认**：涉及多种方案选择时（如安装环境、3DTiles 类型），如果用户已明确说明，直接执行不再询问。否则通过交互确认让用户选择，具体选项见各 reference 文档的「交互判断」章节。
4. **路况加载**：用户提到"路况"、"高精路况"、"百度路况"时，查阅 `vector-tile.md`（不是 3dtiles.md）。路况通过矢量瓦片提供者加载，不是 3DTiles。
5. **百度底图**：用户提到"百度底图"、"百度地图"时，需同时查阅 `mapview-bindmap.md`（百度栅格影像 Baidu09ImageryTileProvider）和 `vector-tile.md`（百度矢量 BaiduVectorTileProvider），两者都是百度底图，让用户选择栅格还是矢量。
6. **参数准确**：代码中的 API 名称、参数名、默认值必须与参考文档一致，不要凭记忆猜测。
7. **AK 不要猜测**：使用 LBS 服务（地理编码、搜索、路线规划等）需要 `BaiduMapConfig.ak`。如果代码中已有 `BaiduMapConfig.ak` 的设置，可以直接复用；如果没有，必须提示用户提供，**不要**从其他服务（如 AssetsScene、TileLightManager 等）的 ak 中复用，因为不同服务的 ak 权限可能不同。
8. **自定义瓦片排查**：用户反馈自定义 XYZ 瓦片加载不出来时，**不要直接修改代码**，而是查阅 `mapview-bindmap.md` 中 XYZImageryTileProvider 的「自定义瓦片服务常见问题排查」章节，将排查方案以清单形式列出引导用户确认。对于 startLevel 问题，如果用户不确定最小层级，可让用户提供一个可访问的瓦片地址，AI 通过 WebFetch 逐级访问父瓦片（z-1, x//2, y//2）自动探测出 startLevel。排查清单：(1) 瓦片地址是否可访问 (2) startLevel 是否匹配数据最小层级 (3) Y 坐标方向（{y} vs {reverseY}） (4) CORS 跨域。确认具体原因后再修改代码。
9. **版本确认**：当用户遇到 API 不存在、参数不生效等问题时，优先让用户确认 `@baidu/mapv-three` 的版本（`npm list @baidu/mapv-three`）。内网 npm 安装时必须加 `@latest`（`npm install -S @baidu/mapv-three@latest`），否则可能因 registry 缓存或 lock 文件安装到旧版本。详见 `project-setup.md` 的版本注意事项。

## 快速参考

### 0. 项目搭建
- [项目搭建指南](./references/project-setup.md) — npm安装、离线部署、环境配置、项目结构

### 1. 引擎核心
- [引擎初始化与地图绑定](./references/engine-bindmap.md) — Engine构造函数、配置项、视野控制、生命周期

### 2. 天空与天气
- [天空环境系统](./references/sky-environment.md) — EmptySky、DefaultSky、HazeSky、StaticSky、CustomStaticSky、VerticalGradientSky、DynamicSky、PhysicalSky
- [天气系统](./references/weather-system.md) — DynamicWeather 雨雪雾雷暴等9种天气效果

### 3. 底图加载
- [MapView底图系统](./references/mapview-bindmap.md) — MapView、QuadMap、影像瓦片提供者（Bing/OSM/XYZ/百度/天地图/WMS/WMTS）
- [矢量瓦片、路况与地形](./references/vector-tile.md) — Mapbox矢量、百度矢量、GeoJSON矢量、**百度路况（BaiduTrafficTileProvider）、高精路况（HDTrafficTileProvider）**、Cesium地形、材质管理器。用户要求加载路况时查阅此文档

### 4. 3DTiles
- [3DTiles加载与管理](./references/3dtiles.md) — Default3DTiles、3DTilesGroup、材质管理器、HDMap、TrafficMap、元素管理器

### 5. 可视化组件
- [SimplePoint 简单点](./references/simple-point.md) — 基础散点、数据驱动颜色/大小、自定义形状
- [Label 标签、IconPoint 图标点、Icon 图标与 Text 文字](./references/label-icon.md) — 文本标签、图标点、图文组合、Icon 贴地/跳动/旋转图标、Text 纯文字标注
- [EffectPoint 特效、Circle 圆形、Pillar 柱体](./references/effect-circle-pillar.md) — 波纹/雷达/气泡特效、圆形、柱状图
- [Polyline 折线与 Wall 墙体](./references/polyline-wall.md) — SimpleLine、Polyline（屏幕/贴地）、飞线效果、Wall 墙体动画
- [Polygon 多边形](./references/polygon.md) — 填充/拉伸/边框/贴地/纹理/动画多边形
- [Heatmap 热力图与 ClusterPoint 聚合点](./references/heatmap-cluster.md) — 2D/3D 热力图、点聚合
- [EffectModelPoint 效果模型点](./references/effect-model-point.md) — 自定义3D模型点、旋转/跳跃动画、PointGroup组合

### 6. 模型与资产
- [模型加载](./references/model-loading.md) — SimpleModel、AnimationModel、LODModel、GLTFScene、GeoInstancedMesh、InstancedModel、DynamicInstancedMesh
- [AssetsScene 资产场景](./references/assets-scene.md) — 资产平台对接、设备加载/添加/编辑/删除、巡游、设备查询与显隐控制
- [设备状态控制](./references/device-control.md) — 情报板文字、信号灯、路灯、风机、卷帘门、升降杆、防火门等 8 种设备操作

### 7. LBS 服务
- [Geocoder 地理编码](./references/geocoder.md) — 地址转坐标、坐标转地址、百度/天地图数据源
- [LocalSearch 搜索与 AutoComplete 自动完成](./references/search-autocomplete.md) — POI检索、范围搜索、周边搜索、输入提示
- [路线规划](./references/route-planning.md) — 驾车/步行/骑行/公交路线规划、策略配置、途经点
- [行政区划](./references/boundary-district.md) — Boundary边界查询、DistrictLayer聚合图层

### 8. GIS 分析
- [GIS空间分析](./references/gis-analysis.md) — 通视、天际线分析（SkylineAnalysis）、淹没、坡度、视域、体积、缓冲区、瓦片掩膜（TileMask）

### 9. 编辑与测量
- [编辑与测量工具](./references/editor-measure.md) — Editor（DrawerType: Spline/Point/Circle/Rect/Polygon）、Measure（MeasureType: Length/Area/Point）

### 10. 数字孪生与实时数据
- [Twin 数字孪生车流](./references/twin.md) — Twin车辆管理、MockTwin模拟车流、DataProvider数据映射、模型配置、车辆追踪
- [TileLightManager 实时信号灯](./references/tile-light-manager.md) — 实时信号灯加载、DefaultLampRequest/RegionLampRequest数据源、灯态编码、自定义数据源

### 11. 数据源
- [数据源](./references/datasource.md) — DataItem、DataSource、GeoJSONDataSource、CSVDataSource、JSONDataSource、属性映射、数据过滤

### 12. 动画追踪
- [动画追踪器](./references/tracker.md) — PathTracker 路径巡游、OrbitTracker 轨道环绕、ObjectTracker 对象跟随

### 13. 覆盖物
- [覆盖物与弹窗](./references/overlay-popup.md) — DOMOverlay、Popup、Marker、GroundOverlay、事件系统

## 如何使用

1. 根据你要实现的功能，在上面的「快速参考」中找到对应的章节
2. 阅读对应的参考文档，其中包含构造函数、参数表格、方法列表和完整代码示例
3. 将代码示例中的参数替换为你的实际数据即可
