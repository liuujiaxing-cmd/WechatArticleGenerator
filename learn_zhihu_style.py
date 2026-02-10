import os
import json
import time
from duckduckgo_search import DDGS
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

# Synthetic data as fallback (Grounded, Realistic Zhihu Style samples - Recent 2 Years)
MOCK_ZHIHU_DATA = """
1. 35岁被裁，投了500份简历，面试0。这才是2024年真实的就业市场，别听专家瞎吹什么“灵活就业”。每天早上醒来，看着房贷扣款短信，那种窒息感，没经历过的人不懂。
2. 坐标三线城市，月薪3000，没有房贷，每天下班去夜市摆摊卖淀粉肠。虽然赚得不多，但不用看老板脸色，不用回钉钉消息，我觉得这才是生活。
3. 别卷了，身体是自己的。上周我同事在工位上晕倒，ICU住一晚，你那点加班费不够塞牙缝的。公司转头就招了个更年轻更便宜的。
4. 说个扎心的真相：普通人翻身的机会，真的不多了。以前靠买房、靠互联网红利，现在呢？消费降级才是主旋律，拼多多的财报说明了一切。
5. 没什么大道理，就是穷。以前喝星巴克，现在喝瑞幸还要等9块9的券。这不是抠，这是认清现实。
"""

def fetch_zhihu_content():
    """
    Search for Zhihu high-vote style content using DuckDuckGo (Focus on Realistic/Grounded topics).
    """
    print("🔍 Searching for Zhihu high-vote content (Realistic/Grounded)...")
    queries = [
        'site:zhihu.com "2024" "真实经历" 高赞',
        'site:zhihu.com "2025" "普通人" 现状',
        'site:zhihu.com "失业" "送外卖" 经历',
        'site:zhihu.com "消费降级" "房贷" 压力',
        'site:zhihu.com "35岁" "裁员" 出路'
    ]
    
    collected_texts = []
    
    # Try Search first
    try:
        with DDGS() as ddgs:
            for query in queries:
                print(f"  - Querying: {query}")
                results = list(ddgs.text(query, max_results=2))
                for r in results:
                    collected_texts.append(f"Title: {r['title']}\nSnippet: {r['body']}")
                time.sleep(1) # Be nice
    except Exception as e:
        print(f"    ⚠️ Search Warning: {e}")

    # Combine with Mock Data if search yields little
    if len(collected_texts) < 2:
        print("⚠️ Search yielded insufficient data. Integrating internal knowledge base samples...")
        collected_texts.append(MOCK_ZHIHU_DATA)

    return "\n\n".join(collected_texts)

def analyze_style(content):
    """
    Ask LLM to analyze the collected content and generate a style guide.
    """
    print("\n🧠 Analyzing style patterns...")
    
    prompt = f"""
    Here are text samples representing the "Zhihu High-Vote Style (Recent 2 Years - Realistic/Grounded)":

    {content}

    Please analyze these texts and generate a **"Zhihu High-Vote Style Guide (Realistic Edition)"**.
    
    Output structured Markdown in **Simplified Chinese**:
    
    ## 1. 核心人设 (Persona)
    - Describe the typical persona (e.g., Frustrated Middle-aged, Lay-flat Youth, Realistic Observer).
    - **Avoid**: "Elite", "Insider", "Show-off". **Focus on**: "Ordinary", "Struggling", "Awake".
    
    ## 2. 黄金开头 (The Hook)
    - List 3-4 specific opening templates (e.g., "说个扎心的真相", "刚办完离职手续").
    
    ## 3. 叙事逻辑 (Structure)
    - How to organize the content (Personal Misery -> Social Context -> Resignation/Acceptance).
    
    ## 4. 关键词与梗 (Keywords)
    - List buzzwords (e.g., 降本增效, 消费降级, 巨大的草台班子, 祛魅).
    
    ## 5. 情绪调动 (Tone)
    - How to trigger resonance through shared pain or "giving up".
    - **Tone**: Disillusioned, Calm, Pragmatic, Anti-anxiety (by accepting the worst).
    """

    try:
        response = openai.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a literary analyst."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Analysis failed: {e}"

if __name__ == "__main__":
    content = fetch_zhihu_content()
    if content:
        print(f"✅ Ready for analysis.")
        style_guide = analyze_style(content)
        print("\n" + "="*20 + " ZHIHU STYLE GUIDE " + "="*20)
        print(style_guide)
        print("="*60)
        
        # Save to file
        with open("zhihu_style_guide.md", "w", encoding="utf-8") as f:
            f.write(style_guide)
        print("✅ Style guide saved to 'zhihu_style_guide.md'")
    else:
        print("❌ Failed to collect content.")
