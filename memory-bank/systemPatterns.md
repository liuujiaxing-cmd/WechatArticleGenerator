# 系统模式 (System Patterns)

## 架构
系统遵循流水线架构：
1.  **主题源**：`search_hot_topics()`（目前为模拟数据，可扩展为网络搜索）。
2.  **内容生成器**：使用 OpenAI API 的 `WeChatArticleGenerator` 类。
    -   使用提示词工程（Prompt Engineering）控制结构和语调。
    -   返回结构化的 JSON 数据。
3.  **渲染器**：Jinja2 模板引擎。
    -   将 JSON 转换为 HTML。
    -   使用 `templates/article_template.html` 进行布局。
    -   **关键模式**：使用嵌套的 HTML `<table>` 元素实现“卡片式”布局，以获得最大兼容性。
4.  **安全过滤器**：`safety_check()` 方法。
    -   简单的关键词匹配（可扩展为基于 LLM 的审核）。

## 关键决策
- **HTML 优于 Markdown**：微信需要特定的 HTML 样式（内联样式、表格），Markdown 无法完全满足。
- **Jinja2 模板**：将内容逻辑与展示分离，便于更改主题。
- **JSON 中间格式**：解耦 LLM 生成与 HTML 渲染，便于调试和重新渲染而无需重新生成文本。
- **Skill 封装**：创建 `wechat-article-writer` skill，以便 AI Agent 未来能轻松调用这些能力。
