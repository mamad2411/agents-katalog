---
name: blender
description: 用 Blender 后台建模、整理和转换 3D 模型，渲染画面、多角度预览与模型体检。
disable-model-invocation: true
---

# Blender

目标是交付看过实际画面、能继续修改的 3D 产物：模型文件、渲染图，以及能再打开编辑的 `.blend`。网页里的交互展示交给 Three.js，游戏运行交给 Godot；Blender 做出、整理和检查它们要用的模型与画面。产物放在当前项目内，用 `present_artifact` 交回。

需已安装 Blender，命令是 `blender`；用 `blender --version` 确认版本。下文标注 5.1.2 的实测经验按当前版本核对。

## 后台运行

```bash
blender -b --factory-startup --python-exit-code 1 --python <脚本.py> -- <脚本自己的参数>
```

- 一律带 `-b`。不带会打开 Blender 界面，占用户的桌面。
- `--python-exit-code 1` 要写在 `--python` 前面。不写或写在后面，脚本报错、脚本找不到时退出码仍是 0，看不出失败。
- `--factory-startup` 不读用户自己的偏好和插件，每次结果一致。
- 报错在 stderr；`--` 之后的参数用 `sys.argv[sys.argv.index("--") + 1:]` 取。
- 脚本里打开已有文件用 `bpy.ops.wm.open_mainfile(filepath=...)`；保存给用户继续改用 `bpy.ops.wm.save_as_mainfile(filepath=...)`；覆盖已有文件会多出 `.blend1` 备份，先设 `bpy.context.preferences.filepaths.save_version = 0`。

## 看画面

做完、改完、导出后都渲染出图，用 `read_image` 看形状、比例、朝向和材质。顶点数和尺寸对上，不等于看起来对。

检查模型文件用本技能的预览脚本：

```bash
blender -b --factory-startup --python-exit-code 1 --python "<本技能目录>/scripts/渲染预览.py" -- <模型文件> <模型名-预览.png> [--角度 4] [--边长 512]
```

它读 .blend、glTF／GLB、FBX、OBJ、STL、PLY、USD、Alembic，自动取景，绕竖轴拍几个角度拼成一张图，并打印一行「模型概况」：网格、顶点、面、尺寸（米）、材质、贴图读没读到、骨架和动作。第一张从 -Y 看向 +Y，素材朝向不同，正面可能在别的格子里。贴图没读到，多半是贴图文件没跟模型放在一起。5.1.2 在 Apple M1 上一个模型 2～5 秒。

## 体检：一个模型看一次

验一个交来的模型，或者交出之前自查，用体检脚本。它不调任何模型，只用 Blender 渲染和计算：

```bash
blender -b --factory-startup --python-exit-code 1 --python "<本技能目录>/scripts/模型体检.py" -- <模型文件> "$TMPDIR/模型体检" [--身高 24] [--边长 384]
```

它出两样东西，文件名带着模型文件的指纹：

- **一张联系表**：正、侧、背、顶四个正交视角，旁边站一个 1.75 米的人，脚下一条 0 米的地面线；一个 3/4 视角；正面、侧面纯黑剪影，外加一张缩到小尺寸的剪影，看远处、缩略图里还认不认得出；每个动作取 5 个时刻的侧面剪影排一行，五格同一个取景，动没动、往哪动、陷没陷进地面线，一眼比得出来。
- **一份读数**：尺寸、最低点、原点离脚底中心多远、三角面数和面数最多的部件、网格破损（非流形边、孤立点、零面积面）、缺 UV、缺材质、缩放没应用、镜像、贴图读没读到、骨骼和没有权重的顶点、每个动作的时长、最大位移、动没动、最低点范围、水平漂移。`--身高` 给了约定高度的，差得多会写出来。

先看读数里的「要看的」：机器量得出的毛病都在那里，会出错的排前面，常见又多半无害的（拼出来的模型没有 UV、管子两头开口）合成一句放最后。形和比例好不好、像不像，看联系表；这一半只能靠眼睛。

为什么这样用：以前验一个模型要一张张出图、一张张读，剪影、尺度、动作各验一遍，同一个模型几个节点各验一遍。体检把这些压成一张图和一份数，一次读完。同一份文件再跑，直接给上次的结果，不到一秒；所以输出放在项目公共的 `$TMPDIR/模型体检`，别的节点拿同一个文件来查，读到的就是同一份，不用重渲。改了模型，指纹变了，自然重新体检；贴图放在模型外面、只改了贴图的，加 `--重做`。

管不到的：只认 Blender 读得了的文件（同上面预览脚本那几种）；在 Godot 场景里用代码拼出来、或者写在 Godot 动画里的东西，GLB 里没有，体检看不到，要先导出成 GLB。读数说的是量得出的事实，不判断好不好看。5.1.2 在 Apple M1 上一个模型 2～6 秒。

自己搭的场景先用 EEVEE、小分辨率、低采样确认构图，再出正式图。Cycles 更准但慢；第一次用 GPU（Metal）渲染实测要等约一分半，之后几秒。

## 版本差异（5.1.2 实测）

记忆里的 bpy 写法多来自旧版，下面这些已经失效：

- 渲染引擎只有 `BLENDER_EEVEE`、`BLENDER_WORKBENCH`、`CYCLES`；写 `BLENDER_EEVEE_NEXT` 报错。
- OBJ、STL 用 `bpy.ops.wm.obj_import`／`obj_export`、`wm.stl_import`／`stl_export`；`import_scene.obj`、`import_mesh.stl` 已不存在。glTF、FBX 仍是 `import_scene.gltf`／`fbx` 与 `export_scene.gltf`／`fbx`。
- 新建材质自带节点树，直接取 `material.node_tree.nodes["Principled BSDF"]`；`use_nodes` 已标为弃用，不用再设。
- 自带 Python 3.13 和 numpy。
- 名字或参数报错时，在同一版本里用 `dir()` 或 `--python-expr` 查当前写法，不按记忆换着试。

## 格式与单位

- 只读二进制 FBX；ASCII FBX 报 `ASCII FBX files are not supported`。同一素材包里有 GLB 或 OBJ 时换用它们。
- glTF 按 1 单位＝1 米导入。尺寸离谱（一只动物几十米长）说明原件单位不同，缩放后再导出。
- 给 Godot、Three.js 用的模型导出 GLB：`bpy.ops.export_scene.gltf(filepath=..., export_format="GLB")`，导出后再用预览脚本看一遍。Blender 里朝 -Y 的面，导出后朝 +Z，也就是 glTF 约定的正面。
