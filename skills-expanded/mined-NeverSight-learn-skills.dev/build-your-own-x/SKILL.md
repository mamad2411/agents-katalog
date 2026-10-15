---
name: build-your-own-x
description: "Master programming by recreating your favorite technologies from scratch. Based on the 529K+ star GitHub repo codecrafters-io/build-your-own-x, this skill indexes 200+ step-by-step tutorials across 30+ tech domains — 3D renderer, AI model, blockchain, database, Docker, emulator, game engine, Git, OS, programming language, neural network, Shell, web server, and more. Triggers on: build your own, from scratch, byox, learn by building, recreate, 从零实现, 手写, 造轮子."
---

# Build Your Own X — 从零构建一切

> "What I cannot create, I do not understand." — Richard Feynman

基于 [codecrafters-io/build-your-own-x](https://github.com/codecrafters-io/build-your-own-x)（529K+ ⭐），精心整理的 200+ 篇「从零重建技术」教程合集。

## Use this guide when someone asks

- "我想从零实现一个 XXX" / "I want to build a XXX from scratch"
- "怎么手写/手搓一个 XXX" / "How to recreate XXX"
- "想理解 XXX 底层原理" / "How does XXX work under the hood?"
- "build your own XXX" / "from scratch" / "byox"
- "不用框架/库，纯手写 XXX" / "No frameworks, just raw code"

## When NOT to use

- Simple how-to-use guides for existing frameworks/libraries
- Pure theory discussions without coding
- Already-known standalone tutorials (this is an index, not a replacement)

---

## How to Use

### Step 1: Clarify what to build

Ask:
- What technology? (database, game, OS, language…)
- What language? (Python, Go, Rust, C, JS…)
- Time budget? (one afternoon vs. multi-week deep dive)
- Minimal (< 500 lines) or full-featured?

### Step 2: Match a tutorial

Find the best match from the index below. Prioritize **language + difficulty + domain**.

### Step 3: Guide through the tutorial

- Open the tutorial link, extract key steps and code snippets
- Plan the coding flow, guide the user step by step
- If there's a companion code repo, point them to clone it
- Verify compilation/execution at each step

---

## 教程索引 / Tutorial Index

### 🎮 3D 渲染器 (3D Renderer)

| 语言 | 教程 | 特点 |
|------|------|------|
| C++ | [Ray Tracing in One Weekend](https://raytracing.github.io/books/RayTracingInOneWeekend.html) | 经典入门，周末搞定 |
| C++ | [TinyRenderer](https://github.com/ssloy/tinyrenderer/wiki) | 500 行 OpenGL |
| C++ | [Physically Based Rendering](http://www.pbr-book.org/) | 教科书级 |
| C# / JS | [3D soft engine from scratch](https://www.davrous.com/2013/06/13/tutorial-series-learning-how-to-write-a-3d-soft-engine-from-scratch-in-c-typescript-or-javascript/) | 从 C# 到 JS 多语言 |
| Java / JS | [Build your own 3D renderer](https://avik-das.github.io/build-your-own-raytracer/) | 从零光线追踪 |
| Python | [A 3D Modeller](http://aosabook.org/en/500L/a-3d-modeller.html) | 500 Lines or Less |
| C++ | [Rasterization: Practical Implementation](https://www.scratchapixel.com/lessons/3d-basic-rendering/rasterization-practical-implementation/overview-rasterization-algorithm) | 光栅化实战 |

### 🤖 AI 模型 (AI Model)

| 语言 | 教程 | 特点 |
|------|------|------|
| Python | [LLMs from scratch](https://github.com/rasbt/LLMs-from-scratch) | 从零实现大语言模型 |
| Python | [Diffusion Models for Image Generation](https://huggingface.co/learn/diffusion-course/en/unit1/3) | HuggingFace 官方 |
| Python | [RAG from Scratch](https://github.com/langchain-ai/rag-from-scratch) | LangChain 出品 |

### ⛓️ 区块链 / 加密货币 (Blockchain)

| 语言 | 教程 | 特点 |
|------|------|------|
| Go | [Building Blockchain in Go](https://jeiwan.net/posts/building-blockchain-in-go-part-1/) | 系列教程 |
| Python | [Learn Blockchains by Building One](https://hackernoon.com/learn-blockchains-by-building-one-117428612f46) | 经典入门 |
| JavaScript | [Naivecoin](https://github.com/conradoqg/naivecoin) | <1500 行 |
| TypeScript | [NaivecoinStake](https://naivecoinstake.learn.uno/) | PoS 版本 |
| JavaScript | [Build your own Blockchain in JS](https://github.com/nambrot/blockchain-in-js) | 纯 JS |

### 🗄️ 数据库 (Database)

| 语言 | 教程 | 特点 |
|------|------|------|
| Go | [Build Your Own Database from Scratch](https://build-your-own.org/database/) | B+Tree → SQL，3000 行 |
| Go | [Build Your Own Redis from Scratch](https://www.build-redis-from-scratch.dev/) | Redis 协议 |
| C | [Let's Build a Simple Database](https://cstack.github.io/db_tutorial/) | C 语言经典 |
| C++ | [Build Your Own Redis from Scratch](https://build-your-own.org/redis/) | Redis 实现 |
| JavaScript | [Dagoba: in-memory graph database](http://aosabook.org/en/500L/dagoba-an-in-memory-graph-database.html) | 500L 系列 |
| Python | [DBDB: Dog Bed Database](http://aosabook.org/en/500L/dbdb-dog-bed-database.html) | 500L 系列 |
| Python | [Miniature Redis with Python](http://charlesleifer.com/blog/building-a-simple-redis-server-with-python/) | 迷你 Redis |
| Rust | [Build your own Redis client and server](https://tokio.rs/tokio/tutorial/setup) | Tokio 官方 |

### 🐳 Docker

| 语言 | 教程 | 特点 |
|------|------|------|
| C | [Linux containers in 500 lines](https://blog.lizzie.io/linux-containers-in-500-loc.html) | 纯 C |
| Go | [Build Your Own Container Using <100 Lines of Go](https://www.infoq.com/articles/build-a-container-golang) | 100 行 Go |
| Python | [A workshop on Linux containers](https://github.com/Fewbytes/rubber-docker) | 重写 Docker |
| Shell | [Docker in ~100 lines of bash](https://github.com/p8952/bocker) | 最简容器 |

### 🕹️ 模拟器 / 虚拟机 (Emulator / VM)

| 语言 | 教程 | 特点 |
|------|------|------|
| C | [Write your Own Virtual Machine](https://justinmeiners.github.io/lc3-vm/) | LC-3 VM |
| C | [Writing a Game Boy emulator, Cinoop](https://cturt.github.io/cinoop.html) | GameBoy |
| JavaScript | [GameBoy Emulation in JavaScript](http://imrannazar.com/GameBoy-Emulation-in-JavaScript) | GameBoy in JS |
| Python | [Chip 8 Emulator/Interpreter](http://omokute.blogspot.com.br/2012/06/emulation-basics-write-your-own-chip-8.html) | Chip-8 |
| Rust | [0dmg: Learning Rust by building a Game Boy emulator](https://jeremybanks.github.io/0dmg/) | GameBoy in Rust |
| C++ | [NES Emulator From Scratch](https://www.youtube.com/playlist?list=PLrOv9FMX8xJHqMvSGB_9G9nZZ_4IgteYf) | NES 视频系列 |

### 🎮 游戏 (Game)

| 语言 | 教程 | 特点 |
|------|------|------|
| C | [Handmade Hero](https://handmadehero.org/) | 传奇级，从零写游戏 |
| C | [How to Program an NES game in C](https://nesdoug.com/) | NES 游戏 |
| C | [On Tetris and Reimplementation](https://brennan.io/2015/06/12/tetris-reimplementation/) | 俄罗斯方块 |
| JavaScript | [2D breakout game using Phaser](https://developer.mozilla.org/en-US/docs/Games/Tutorials/2D_breakout_game_Phaser) | MDN 官方 |
| JavaScript | [How to Make Your First Roguelike](https://gamedevelopment.tutsplus.com/tutorials/how-to-make-your-first-roguelike--gamedev-13677) | Roguelike |
| Python | [Pygame Tutorial](https://pythonprogramming.net/pygame-python-3-part-1-intro/) | Pygame 入门 |
| Python | [Roguelike Tutorial Revised](http://rogueliketutorials.com/) | Roguelike 经典 |
| Rust | [Roguelike Tutorial in Rust + tcod](https://tomassedovic.github.io/roguelike-tutorial/) | Rust + tcod |

### 🔧 Git

| 语言 | 教程 | 特点 |
|------|------|------|
| JavaScript | [Gitlet](http://gitlet.maryrosecook.com/docs/gitlet.html) | Git in JS |
| JavaScript | [Build GIT - Learn GIT](https://kushagra.dev/blog/build-git-learn-git/) | 学习 Git 内部 |
| Python | [Write yourself a Git!](https://wyag.thb.lt/) | 最完整 |
| Python | [ugit: Learn Git Internals by Building Git Yourself](https://www.leshenko.net/p/ugit/) | 精简易懂 |
| Python | [Just enough of a Git client](https://benhoyt.com/writings/pygit/) | 最小 Git |

### 🧠 神经网络 (Neural Network)

| 语言 | 教程 | 特点 |
|------|------|------|
| Python | [A Neural Network in 11 lines of Python](https://iamtrask.github.io/2015/07/12/basic-python-network/) | 11 行入门 |
| Python | [Build Deep Learning From Scratch](https://github.com/roiaimiel1/Build-Deep-Learning-From-Scratch) | 34 阶段重写 PyTorch |
| Python | [Neural Networks: Zero to Hero](https://www.youtube.com/playlist?list=PLAqhIrjkxbWUI23v9cTHsA9GvCAUhRvKZ) | Karpathy 视频 |
| Python | [SlowTorch](https://github.com/xames3/slowtorch) | 纯 Python 实现 PyTorch |
| Go | [Build a multilayer perceptron with Golang](https://made2591.github.io/posts/neuralnetwork) | Go 写 MLP |
| JavaScript | [Neural networks from scratch for JS linguists](https://hackernoon.com/neural-networks-from-scratch-for-javascript-linguists-part1-the-perceptron-632a4d1fbad2) | JS 党入门 |

### 💻 操作系统 (Operating System)

| 语言 | 教程 | 特点 |
|------|------|------|
| C | [OS: From 0 to 1](https://tuhdo.github.io/os01/) | 电子书 |
| C | [The little book about OS development](https://littleosbook.github.io/) | 经典小书 |
| C | [Roll your own toy UNIX-clone OS](http://jamesmolloy.co.uk/tutorial_html/) | 类 UNIX |
| C | [Kernel 101 – Let's write a Kernel](https://arjunsreedharan.org/post/82710718100/kernel-101-lets-write-a-kernel) | 入门内核 |
| C | [Kernel 201 – Keyboard and screen support](https://arjunsreedharan.org/post/99370248137/kernel-201-lets-write-a-kernel-with-keyboard) | 进阶内核 |
| Rust | [Writing an OS in Rust](https://os.phil-opp.com/) | Rust OS 圣经 |
| Rust | [Add RISC-V Rust Operating System Tutorial](https://osblog.stephenmarz.com/) | RISC-V |
| Assembly | [Writing a Tiny x86 Bootloader](http://joebergeron.io/posts/post_two.html) | Bootloader |
| C++ | [Write your own Operating System](https://www.youtube.com/playlist?list=PLHh55M_Kq4OApWScZyPl5HhgsTJS9MZ6M) | 视频系列 |
| (any) | [Linux from Scratch](https://linuxfromscratch.org/lfs) | 终极挑战 |

### 📝 编程语言 (Programming Language)

| 语言 | 教程 | 特点 |
|------|------|------|
| (any) | [mal - Make a Lisp](https://github.com/kanaka/mal#mal---make-a-lisp) | 68 种语言实现 Lisp |
| C | [Build Your Own Lisp](http://www.buildyourownlisp.com/) | 1000 行 C |
| Go | [The Super Tiny Compiler](https://github.com/hazbo/the-super-tiny-compiler) | 最小编译器 |
| JavaScript | [The Super Tiny Compiler](https://github.com/jamiebuilds/the-super-tiny-compiler) | JS 版 |
| JavaScript | [How to implement a programming language in JS](http://lisperator.net/pltut/) | PL 入门 |
| Python | [Let's Build A Simple Interpreter](https://ruslanspivak.com/lsbasi-part1/) | 解释器系列 |
| Python | [From Source Code To Machine Code](https://build-your-own.org/compiler/) | 编译器 |
| Python | [A Python Interpreter Written in Python](http://aosabook.org/en/500L/a-python-interpreter-written-in-python.html) | PyPy 式 |
| Haskell | [Write Yourself a Scheme in 48 Hours](https://en.wikibooks.org/wiki/Write_Yourself_a_Scheme_in_48_Hours) | Scheme 48h |
| Java | [Crafting Interpreters](http://www.craftinginterpreters.com/) | 神书 |
| Rust | [Learning Parser Combinators With Rust](https://bodil.lol/parser-combinators/) | Parser Combinators |
| TypeScript | [Build your own WebAssembly Compiler](https://blog.scottlogic.com/2019/05/17/webassembly-compiler.html) | WASM |

### 🔍 正则表达式引擎 (Regex Engine)

| 语言 | 教程 | 特点 |
|------|------|------|
| C | [A Regular Expression Matcher](https://www.cs.princeton.edu/courses/archive/spr09/cos333/beautiful.html) | Rob Pike 经典 |
| JavaScript | [Build a Regex Engine in <40 Lines of Code](https://nickdrane.com/build-your-own-regex/) | <40 行 |
| Python | [Build Your Own Regex Engines](https://build-your-own.org/b2a/r0_intro) | NFA/DFA/回溯 |

### 🔎 搜索引擎 (Search Engine)

| 语言 | 教程 | 特点 |
|------|------|------|
| Python | [Building a search engine using Redis](http://www.dr-josiah.com/2010/07/building-search-engine-using-redis-and.html) | Redis 搜索 |
| Python | [Building A Python-Based Search Engine](https://www.youtube.com/watch?v=cY7pE7vX6MU) | 视频 |

### 🐚 Shell

| 语言 | 教程 | 特点 |
|------|------|------|
| C | [Tutorial - Write a Shell in C](https://brennan.io/2015/01/16/write-a-shell-in-c/) | C Shell 经典 |
| C | [Writing a UNIX Shell](https://indradhanush.github.io/blog/writing-a-unix-shell-part-1/) | UNIX Shell |
| Go | [Writing a simple shell in Go](https://sj14.gitlab.io/post/2018-07-01-go-unix-shell/) | Go Shell |
| Rust | [Build Your Own Shell using Rust](https://www.joshmcguigan.com/blog/build-your-own-shell-rust/) | Rust Shell |

### 🌐 Web 服务器 (Web Server)

| 语言 | 教程 | 特点 |
|------|------|------|
| Node.js | [Build Your Own Web Server From Scratch In JavaScript](https://build-your-own.org/webserver/) | 分步指南 |
| Node.js | [lets-build-express](https://github.com/antoaravinth/lets-build-express) | 从零写 Express |
| Python | [Let's Build A Web Server.](https://ruslanspivak.com/lsbaws-part1/) | 经典系列 |
| Python | [Web application from scratch](https://defn.io/2018/02/25/web-app-from-scratch-01/) | 从头开始 |
| Ruby | [Building a simple websockets server from scratch in Ruby](http://blog.honeybadger.io/building-a-simple-websockets-server-from-scratch-in-ruby/) | WebSocket |

### 🖥️ 前端框架 / 库 (Front-end Framework)

| 语言 | 教程 | 特点 |
|------|------|------|
| JavaScript | [WTF is JSX (Let's Build a JSX Renderer)](https://jasonformat.com/wtf-is-jsx/) | 理解 JSX |
| JavaScript | [Build your own React](https://pomb.us/build-your-own-react/) | 手写 React |
| JavaScript | [Gooact: React in 160 lines of JavaScript](https://medium.com/@sweetpalma/gooact-react-in-160-lines-of-javascript-44e0742ad60f) | 160 行 React |
| JavaScript | [Build Yourself a Redux](https://zapier.com/engineering/how-to-build-redux/) | 手写 Redux |
| JavaScript | [Building a frontend framework](https://mfrachet.github.io/create-frontend-framework/) | 完整框架 |
| JavaScript | [How to write your own Virtual DOM](https://medium.com/@deathmood/how-to-write-your-own-virtual-dom-ee74acc13060) | 虚拟 DOM |

### 📡 网络栈 (Network Stack)

| 语言 | 教程 | 特点 |
|------|------|------|
| C | [Beej's Guide to Network Programming](http://beej.us/guide/bgnet/) | 网络编程圣经 |
| C | [Let's code a TCP/IP stack](http://www.saminiir.com/lets-code-tcp-ip-stack-1-ethernet-arp/) | TCP/IP |
| Ruby | [How to build a network stack in Ruby](https://medium.com/geckoboard-under-the-hood/how-to-build-a-network-stack-in-ruby-f73aeb1b661b) | Ruby 网络 |

### 🖊️ 文本编辑器 (Text Editor)

| 语言 | 教程 | 特点 |
|------|------|------|
| C | [Build Your Own Text Editor (Kilo)](https://viewsourcecode.org/snaptoken/kilo/) | 经典 kilo |
| Rust | [Hecto: Build your own text editor in Rust](https://www.flenker.blog/hecto/) | Rust 编辑器 |

### 🧩 模板引擎 (Template Engine)

| 语言 | 教程 | 特点 |
|------|------|------|
| JavaScript | [JS template engine in just 20 lines](http://krasimirtsonev.com/blog/article/Javascript-template-engine-in-just-20-line) | 20 行 |
| Python | [A Template Engine](http://aosabook.org/en/500L/a-template-engine.html) | 500L 系列 |

### 🧰 命令行工具 (Command-Line Tool)

| 语言 | 教程 | 特点 |
|------|------|------|
| Go | [Build a CLI app with Go: lolcat](https://flaviocopes.com/go-tutorial-lolcat/) | Go CLI |
| Rust | [Command line apps in Rust](https://rust-cli.github.io/book/index.html) | Rust CLI 书 |
| Node.js | [Create a CLI tool in JavaScript](https://citw.dev/tutorial/create-your-own-cli-tool) | JS CLI |

### 🔩 其他 (Uncategorized)

| 主题 | 语言 | 教程 |
|------|------|------|
| BitTorrent Client | C# | [Building a BitTorrent client from scratch in C#](https://www.seanjoflynn.com/research/bittorrent.html) |
| BitTorrent Client | Go | [Building a BitTorrent client in Go](https://blog.jse.li/posts/torrent/) |
| BitTorrent Client | Python | [A BitTorrent client in Python 3.5](http://markuseliasson.se/article/bittorrent-in-python/) |
| Augmented Reality | C# | [How To Unity ARCore](https://www.youtube.com/playlist?list=PLKIKuXdn4ZMjuUAtdQfK1vwTZPQn_rgSv) |
| Bot (各种) | Python | [Build a Reddit Bot](https://pythonforengineers.com/blog/build-a-reddit-bot-part-1/) |
| Bot | Node.js | [Create a Discord bot](https://discordjs.guide/) |
| Physics Engine | JavaScript | [How Physics Engines Work](http://buildnewgames.com/gamephysics/) |
| Physics Engine | C++ | [Game physics series by Allen Chou](http://allenchou.net/game-physics-series/) |
| Visual Recognition | Python | [Facial Recognition Pipeline with Deep Learning](https://hackernoon.com/building-a-facial-recognition-pipeline-with-deep-learning-in-tensorflow-66e7645015b8) |
| Voxel Engine | C++ | [Let's Make a Voxel Engine](https://sites.google.com/site/letsmakeavoxelengine/home) |
| Web Browser | Rust | [Let's build a browser engine](https://limpet.net/mbrubeck/2014/08/08/toy-layout-engine-1.html) |
| Memory Allocator | C | [Malloc is not magic - Implementing your own](https://medium.com/p/e0354e914402) |
| Hash Table | C | [Learn how to write a hash table in C](https://github.com/jamesroutley/write-a-hash-table) |
| Video Player | C | [How to Write a Video Player in <1000 Lines](http://dranger.com/ffmpeg/ffmpeg.html) |
| DNS Server | Node.js | [Build a DNS Server in Node.js](https://engineerhead.github.io/dns-server/) |
| Load Balancer | Go | [Let's Create a Simple Load Balancer](https://kasvith.me/posts/lets-create-a-simple-lb-go/) |
| CDN | Lua | [Building a CDN from Scratch to Learn about CDN](https://github.com/leandromoreira/cdn-up-and-running) |
| From NAND to Tetris | (any) | [NAND to Tetris](http://nand2tetris.org/) |
| Build System | Nim | [Writing a Build system](https://xmonader.github.io/nimdays/day11_buildsystem.html) |
| JSON Decoding | Python | [JSON Decoding Algorithm](https://github.com/cheery/json-algorithm) |
| Promise | JavaScript | [Implementing promises from scratch (TDD)](https://www.mauriciopoppe.com/notes/computer-science/computation/promises/) |
| Module Bundler | JavaScript | [Minipack - Build Your Own Module Bundler](https://github.com/ronami/minipack) |
| Static Site Generator | Node.js | [Build a static site generator in 40 lines](https://www.webdevdrops.com/en/build-static-site-generator-nodejs-8969ebe34b22/) |
| Continuous Integration | Python | [A Continuous Integration System](http://aosabook.org/en/500L/a-continuous-integration-system.html) |

---

## 学习路线 / Learning Pathways

### 🟢 入门 (Beginner) — 周末速成 (Weekend projects)

适合刚入门、想快速有成就感 / Quick wins:


1. **Shell** (C) — 一个下午
2. **Regex Engine** (JS, <40 行) — 一小时
3. **Neural Network** (Python, 11 行) — 一小时
4. **Blockchain** (Python) — 一个下午
5. **Web Server** (Python/Node.js) — 一个下午

### 🟡 进阶 (Intermediate) — 深入理解 (Deep understanding)

有基础、想深入系统 / Solid foundations, deeper systems:

1. **Git** (Python) — 1 天
2. **Database** (Go/C) — 2-3 天
3. **Container/Docker** (Go) — 1 天
4. **3D Renderer** (C++, Ray Tracing) — 周末
5. **Emulator** (C, Chip-8) — 周末
6. **Programming Language** (mal Lisp) — 3-5 天

### 🔴 专家 (Expert) — 终极挑战 (The deep end)

推自己到极限 / Push your limits:

1. **Operating System** (C/Rust) — 数周到数月
2. **Compiler** (Crafting Interpreters) — 2-4 周
3. **Game Engine** (C, Handmade Hero) — 数月
4. **Browser Engine** (Rust) — 数周
5. **Linux from Scratch** — 数天到数周

---

## 小贴士 / Tips

- 从入门路线开始建立信心，再迈入进阶领域
- 每个项目建一个 Git 仓库记录进展
- 卡住时直接看教程评论区/Issues
- 有多个语言版本时先选你最熟悉的那门
