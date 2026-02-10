# WeChat Article Generator (微信公众号文章生成器)

一个基于 AI 的微信公众号文章自动生成工具，支持多种风格（包括知乎高赞现实风），自动配图、排版并推送至公众号草稿箱。

## 功能特性 (Features)

*   **多风格支持**：
    *   `zhihu_real`：知乎高赞现实风（工业冷淡排版、人间清醒文案）。
    *   `hot_topic`：热点追踪风格。
    *   `life`：生活感悟风格。
*   **自动排版引擎**：
    *   支持多种 CSS 主题（Classic Red, Ocean Blue, Forest Green, Industrial Retro 等）。
    *   微信原生卡片式布局。
    *   自动生成并插入装饰性小标题和引用块。
*   **全自动工作流**：
    *   联网搜索 (DuckDuckGo) 获取真实素材 (RAG)。
    *   AI 内容生成 (OpenAI Compatible API)。
    *   AI 配图生成与处理 (Picsum/Volcengine)。
    *   自动上传图片素材至微信服务器。
    *   生成文末二维码。
    *   一键推送至公众号草稿箱。

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
