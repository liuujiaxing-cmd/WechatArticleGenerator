# WeChat Article Generator (微信公众号文章生成器) v1.0

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg) ![Status](https://img.shields.io/badge/status-stable-green.svg)

一个基于 AI 的微信公众号文章全自动生成工具。不仅能写，还能自动排版、配图，并直接推送到公众号草稿箱。

**v1.0 版本核心亮点**：
*   🚀 **全自动工作流**：从选题 -> 搜索(RAG) -> 写作 -> 配图 -> 排版 -> 推送，一气呵成。
*   🎭 **多重人格/风格**：支持“知乎高赞现实风”、“热点追踪风”、“生活感悟风”。
*   🎨 **自适应美学排版**：内置“工业冷淡风(Industrial)”、“气泡风(Bubble)”、“极简风(Modern)”等多套 CSS 主题，每次生成都有新视觉。
*   🧠 **RAG 事实增强**：集成 DuckDuckGo 搜索，确保文章内容基于真实信息，拒绝 AI 幻觉。

## 功能特性 (Features)

*   **多风格支持**：
    *   `zhihu_real`：**知乎高赞现实风**（新增）。主打“人间清醒”、“扎心真相”，配合工业冷淡风排版。
    *   `hot_topic`：热点追踪风格。紧跟时事，快速输出。
    *   `life`：生活感悟风格。温暖治愈，适合情感类账号。
*   **智能排版引擎**：
    *   **随机/指定主题**：支持 Industrial Retro (工业复古), Classic Red, Ocean Blue 等 6+ 种配色方案。
    *   **组件化设计**：自动为小标题、引用块、列表适配不同的 CSS 样式（如胶囊型、下划线型、方框型）。
    *   **微信原生兼容**：生成的 HTML 代码完美兼容微信公众号编辑器。
*   **全自动工作流**：
    *   **RAG (检索增强生成)**：自动搜索 DuckDuckGo 获取最新事实/新闻，作为写作上下文。
    *   **AI 写作**：基于 OpenAI 接口（兼容 DeepSeek 等模型），遵循“黄金3秒”、“滑梯效应”等新媒体写作法则。
    *   **AI 配图**：自动生成 Prompt 并获取高质量配图（支持 Picsum Seed 稳定图源，可扩展 Volcengine）。
    *   **一键推送**：集成 `wechatpy`，自动上传素材并创建草稿，文末自动附带二维码。

## v1.0 更新日志 (Changelog)

*   ✅ **新增**：`zhihu_real` 文章类型，模拟知乎高赞回答的“现实主义”文风。
*   ✅ **新增**：`Industrial Retro` (工业冷淡风) 排版主题，包含等宽字体标题和方框引用样式。
*   ✅ **新增**：RAG 联网搜索功能，基于 `ddgs` 实现真实信息注入。
*   ✅ **优化**：修复了数字列表断裂问题，确保序号连续。
*   ✅ **优化**：文章去除正文标题和作者（由微信原生接管），体验更原生。
*   ✅ **优化**：图片生成切换为 `picsum.photos/seed` 模式，确保稳定性；支持文末自动附加二维码。
*   ✅ **发布**：正式封版为 v1.0。

## 快速开始 (Quick Start)

### 1. 安装依赖

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` (需自行创建) 为 `.env` 并填入配置：

```ini
# OpenAI / DeepSeek API
OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=https://api.openai.com/v1

# WeChat Official Account
WECHAT_APP_ID=your_app_id
WECHAT_APP_SECRET=your_app_secret

# (Optional) Volcengine for Images
VOLC_ACCESS_KEY=...
VOLC_SECRET_KEY=...
```

### 3. 运行生成器

```bash
python generator.py
```

## 项目结构

*   `generator.py`: 核心逻辑，负责调度 LLM、图片处理和 HTML 生成。
*   `wechat_publisher.py`: 负责与微信公众号接口交互（上传素材、创建草稿）。
*   `templates/`: HTML 模板文件。
*   `output/`: 生成的中间文件（图片、HTML、二维码）。

## 风格指南

本项目包含一个 `learn_zhihu_style.py` 脚本，用于分析和提取知乎高赞文风。

## License

MIT
