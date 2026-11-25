---
description: Create tech-style minimalist 16:9 HTML presentations out-of-the-box. Includes Dark Mode, strict cover templates, and 10-pull Gacha (十连抽卡) file generation.
---

# Tech-style HTML Presentation Generator

Use this skill when the user wants to generate a minimalist, tech-style, 16:9 HTML presentation with high visual impact. **This skill is entirely self-contained.** You do not need external CSS or JS files. You must generate a **Single HTML file** containing everything.

## Core Rules & Features

### 1. 封面统一原则 (Strict Cover Format)
Every presentation you generate **must** have its first slide structured exactly like this. Do not deviate, to ensure all PPTs have a consistent, uniform cover across different generations.
```html
<div class="slide active">
    <!-- 左上角系列小字 -->
    <div class="absolute top-12 left-16 text-xs text-gray-800 dark:text-gray-500 font-light tracking-widest uppercase">
        TECH VISION 2026 <!-- 默认值，可在要求中替换 -->
    </div>
    <!-- 居中标题与副标题 -->
    <div class="text-center w-full z-10 relative">
        <h1 class="text-7xl md:text-8xl lg:text-9xl font-black mb-6 leading-tight tracking-tight text-transparent bg-clip-text drop-shadow-sm bg-gradient-to-br from-blue-600 to-purple-500 dark:from-blue-400 dark:to-purple-400">
            [主标题]
        </h1>
        <p class="text-2xl text-gray-600 dark:text-gray-400 font-light tracking-widest mt-8">
            [副标题]
        </p>
    </div>
</div>
```

### 2. 黑白昼夜切换 (Dark / Light Mode Toggle)
The generic PPT output **MUST** contain this toggle button fixed to the top right. 
HTML Requirement: `<button class="fixed top-8 right-8 z-[100] px-4 py-2 rounded-full bg-white/10 border border-black/10 dark:border-white/10 backdrop-blur-md text-sm transition-all hover:bg-black/10 dark:hover:bg-white/10 text-gray-800 dark:text-gray-100 font-bold" onclick="document.documentElement.classList.toggle('dark')">🌓 明暗切换</button>`
Every layout element you write must have both light and dark Tailwind classes. **Always start the HTML with `<html lang="zh-CN" class="dark">` to default to Dark Mode.**

### 3. 十连抽卡模式 (10-Pull Gacha Mode - 10 Physical Files Generator)
If the user asks for "10连抽卡", "抽卡", or "生成10个不同版本", **DO NOT output 1 file with a skin switcher.**
Instead, you must write a script or immediately output **10 entirely distinct HTML files** (e.g., `ppt-opt1.html` to `ppt-opt10.html`). 
For each of the 10 files:
1. **Diverse Content Layouts:** Change how the content is presented. Use grid layouts for one file, sequential bullet lists for another, staggered cards for a third, large quote-focus slides instead of text walls, etc.
2. **Diverse Colors:** Use entirely different Tailwind gradients for titles and background `light-spot` colors in each file.
3. **Strict Cover & Dark Mode:** Ensure the "Strict Cover Format" (Rule 1) and "Dark/Light Mode Toggle" (Rule 2) remains identical and fully functional in ALL 10 files.
4. **Action:** If the content is very long, write a Node.js script locally to compile and write these 10 distinct files to save token output, then execute the script.

## Universal HTML Template Structure
Embed all slides inside this shell:

```html
<!DOCTYPE html>
<html lang="zh-CN" class="dark">
<head>
    <meta charset="UTF-8"><title>科技风演示文稿</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.loli.net/css2?family=Inter:wght@300;700;900&family=Noto+Sans+SC:wght@300;700;900&display=swap" rel="stylesheet">
    <script>
        tailwind.config = { darkMode: 'class', theme: { extend: { fontFamily: { sans: ['Inter', 'Noto Sans SC', 'sans-serif'] } } } };
    </script>
    <style>
        body { margin: 0; padding: 0; overflow: hidden; display: flex; justify-content: center; align-items: center; height: 100vh; width: 100vw; transition: background 0.5s; background-color: #f3f4f6;}
        .dark body { background-color: #050505; color: #fff; }
        #presentation-container {
            width: 100%; height: 100%; aspect-ratio: 16 / 9; max-width: 177.78vh; max-height: 100vh; position: relative; overflow: hidden; display: flex; flex-direction: column; 
            background-color: #f9fafb; background-image: linear-gradient(to right, rgba(0, 0, 0, 0.04) 1px, transparent 1px), linear-gradient(to bottom, rgba(0, 0, 0, 0.04) 1px, transparent 1px); background-size: 50px 50px; transition: all 0.5s;
        }
        .dark #presentation-container {
            background-color: #050505; box-shadow: 0 0 60px rgba(0,0,0,0.8);
            background-image: linear-gradient(to right, rgba(255, 255, 255, 0.03) 1px, transparent 1px), linear-gradient(to bottom, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
        }
        @media (min-aspect-ratio: 16/9) { #presentation-container { max-width: 177.78vh; height: 100vh; } }
        
        /* Modify these spot colors for the 10-pull variations */
        .light-spot { position: absolute; border-radius: 50%; filter: blur(80px); opacity: 0.2; z-index: 0; animation: float 20s infinite ease-in-out alternate; transition: all 1s ease;}
        .dark .light-spot { opacity: 0.4; filter: blur(80px); }
        @keyframes float { 0% { transform: translate(0, 0) scale(1); } 50% { transform: translate(60px, -40px) scale(1.05); } 100% { transform: translate(-30px, 50px) scale(0.95); } }
        
        .slide { position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 4rem; z-index: 10; opacity: 0; pointer-events: none; transition: opacity 0.6s, transform 0.6s; transform: translateY(20px) scale(0.98); }
        .slide.active { opacity: 1; transform: translateY(0) scale(1); pointer-events: auto; }
        
        .spot-1 { background: rgba(30, 64, 175, 0.4); width: 500px; height: 500px; top: -10%; left: -10%; }
        .spot-2 { background: rgba(234, 179, 8, 0.2); width: 450px; height: 450px; top: 30%; right: -10%; }
        .spot-3 { background: rgba(190, 24, 93, 0.25); width: 600px; height: 600px; bottom: -20%; left: 30%; }
    
        #nav-dots { position: absolute; bottom: 2rem; left: 0; width: 100%; display: flex; justify-content: center; gap: 16px; z-index: 20; }
        .dot { width: 8px; height: 8px; border-radius: 50%; cursor: pointer; transition: all 0.3s; background: rgba(0,0,0,0.2); }
        .dark .dot { background: rgba(255,255,255,0.2); }
        .dot.active { width: 32px; border-radius: 4px; background: rgba(0,0,0,0.7); }
        .dark .dot.active { background: rgba(255,255,255,0.9); box-shadow: 0 0 10px rgba(255,255,255,0.4); }
    </style>
</head>
<body class="font-sans">
    <button class="fixed top-8 right-8 z-[100] px-4 py-2 rounded-full bg-black/5 border border-black/10 dark:bg-white/10 dark:border-white/10 backdrop-blur-md text-sm transition-all hover:bg-black/10 dark:hover:bg-white/20 text-gray-800 dark:text-gray-100 font-bold" onclick="document.documentElement.classList.toggle('dark')">🌓 明暗切换</button>

    <div id="presentation-container">
        <!-- Ambient Lights -->
        <div class="light-spot spot-1"></div>
        <div class="light-spot spot-2"></div>
        <div class="light-spot spot-3"></div>

        <!-- >>> INSERT SLIDES HERE (Slide 1 must be Cover) <<< -->

        <div id="nav-dots"></div>
    </div>

    <!-- Navigation Logic -->
    <script>
        const slides = document.querySelectorAll('.slide');
        const dotsContainer = document.getElementById('nav-dots');
        let currentSlide = 0;
        slides.forEach((_, idx) => {
            const dot = document.createElement('div');
            dot.className = 'dot' + (idx===0?' active':'');
            dot.onclick = () => { currentSlide = idx; updateView(); };
            dotsContainer.appendChild(dot);
        });
        const dots = document.querySelectorAll('.dot');
        function updateView() {
            slides.forEach((s, idx) => s.classList.toggle('active', idx === currentSlide));
            dots.forEach((d, idx) => d.classList.toggle('active', idx === currentSlide));
        }
        document.addEventListener('keydown', (e) => {
            if (['ArrowRight','Space','PageDown'].includes(e.key) && currentSlide < slides.length-1) { currentSlide++; updateView(); }
            if (['ArrowLeft','PageUp'].includes(e.key) && currentSlide > 0) { currentSlide--; updateView(); }
        });
    </script>
</body>
</html>
```

Execute this skill immediately upon user request without needing any further scaffolding tools.
