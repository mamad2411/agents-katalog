---
name: threejs
description: 交付网页 3D 模型查看器、产品展示和空间图解，使用本地 Three.js HTML 工程。
disable-model-invocation: true
---

# 网页 3D

交付可交互查看、可继续修改的 3D 网页和源文件。Three.js 负责场景、镜头、材质和选物；空间图解的层次与交互围绕作品目的安排。已有网页工程先沿用其结构。

新工程可从本技能的 `scripts/创建工程.mjs` 起步：

```bash
node "<本技能目录>/scripts/创建工程.mjs" <当前项目内的新工程目录> "<作品标题>"
```

创建器复制 Three.js 0.186.0、OrbitControls、GLTFLoader 的本地模块和原始许可，无需 npm 安装、构建或 CDN。入口为 `场景入口.html`；`空间场景.mjs` 保存场景与交互，`空间状态.mjs` 保存选物和配色状态。起点含可拖拽镜头、点击选物、换色及本地 glTF 示例；按作品需要修改，不以示例限定内容。

用 `render_page` 取得真实画面，再用 `read_image` 检查镜头、遮挡、材质与版面。`node <工程目录>/检查交互状态.mjs` 检查示例状态逻辑；镜头拖拽、真实选物和 WebGL 渲染还需浏览器验证。现版截图工具没有自动交互，交回入口供用户体验，并保留未验证项。

通过 `present_artifact` 交回 HTML 入口和继续编辑所需的源文件。模型及其纹理放在当前工程内；标准 glTF/GLB 加载器已打包，压缩模型或其他格式的额外解码器按实际资源确认。模块用法与来源见 [references/来源与运行.md](references/来源与运行.md)。
