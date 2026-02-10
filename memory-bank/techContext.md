# 技术背景 (Tech Context)

## 技术栈
- **语言**：Python 3.9+
- **LLM 提供商**：OpenAI API（兼容 gpt-4o / deepseek-chat）
- **模板引擎**：Jinja2
- **环境管理**：`python-dotenv` 用于管理 API 密钥
- **数据格式**：JSON

## 依赖项
- `openai`: API 客户端。
- `jinja2`: HTML 模板渲染。
- `python-dotenv`: 配置管理。
- `requests`: （潜在）用于网络搜索。
- `beautifulsoup4`: （潜在）用于网页抓取。
- `jieba`: （潜在）用于 NLP 任务。

## 项目结构
```
WeChat_Article_Generator/
├── generator.py           # 主要逻辑
├── render_all.py          # 批量渲染工具
├── requirements.txt       # 依赖列表
├── content.json           # 中间数据存储
├── .env                   # 密钥文件（已排除在 git 之外）
├── templates/
│   └── article_template.html # Jinja2 模板
├── output/                # 生成的 HTML 文件
└── memory-bank/           # 项目文档
```
