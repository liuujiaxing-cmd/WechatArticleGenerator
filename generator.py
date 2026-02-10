import os
import json
import time
import random
import requests
import markdown
from bs4 import BeautifulSoup
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import openai
from dotenv import load_dotenv
from wechat_publisher import WeChatPublisher
from duckduckgo_search import DDGS

# Load environment variables
load_dotenv()

# Configure OpenAI (if available)
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

# Color Themes
COLOR_THEMES = [
    {
        "name": "Classic Red",
        "primary": "#d9534f",
        "secondary": "#f9f9f9",
        "text": "#333333",
        "accent_bg": "rgba(217, 83, 79, 0.1)",
        "style_type": "classic"
    },
    {
        "name": "Ocean Blue",
        "primary": "#007bff",
        "secondary": "#f0f8ff",
        "text": "#2c3e50",
        "accent_bg": "rgba(0, 123, 255, 0.1)",
        "style_type": "modern"
    },
    {
        "name": "Forest Green",
        "primary": "#28a745",
        "secondary": "#f1fff3",
        "text": "#1e392a",
        "accent_bg": "rgba(40, 167, 69, 0.1)",
        "style_type": "bubble"
    },
    {
        "name": "Royal Purple",
        "primary": "#6f42c1",
        "secondary": "#f8f4ff",
        "text": "#3a2a52",
        "accent_bg": "rgba(111, 66, 193, 0.1)",
        "style_type": "classic"
    },
    {
        "name": "Sunset Orange",
        "primary": "#fd7e14",
        "secondary": "#fff5eb",
        "text": "#4d3a2a",
        "accent_bg": "rgba(253, 126, 20, 0.1)",
        "style_type": "modern"
    },
    {
        "name": "Teal Cyan",
        "primary": "#20c997",
        "secondary": "#e6fffa",
        "text": "#1a403a",
        "accent_bg": "rgba(32, 201, 151, 0.1)",
        "style_type": "bubble"
    },
    {
        "name": "Industrial Retro",
        "primary": "#2c2c2c",
        "secondary": "#f5f5f5",
        "text": "#1a1a1a",
        "accent_bg": "rgba(0, 0, 0, 0.05)",
        "style_type": "industrial"
    }
]

class WeChatArticleGenerator:
    def __init__(self, output_dir="output"):
        # Ensure paths are relative to the script location
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_dir = os.path.join(base_dir, output_dir)
        template_dir = os.path.join(base_dir, "templates")
        
        self.env = Environment(loader=FileSystemLoader(template_dir))
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Pick a random theme for this session
        # self.theme = random.choice(COLOR_THEMES)
        self.theme = next(t for t in COLOR_THEMES if t['name'] == "Industrial Retro")
        print(f"🎨 Using Theme: {self.theme['name']}")
        
        # Initialize WeChat Publisher
        try:
            self.publisher = WeChatPublisher()
            print("✅ WeChat Publisher initialized.")
        except Exception as e:
            print(f"⚠️ WeChat Publisher failed to init: {e}")
            self.publisher = None

    def fetch_real_info(self, topic):
        """
        Search the web for real-time information about the topic using DuckDuckGo.
        Returns a summarized context string.
        """
        print(f"🔍 Searching web for real info about: {topic}")
        try:
            results = DDGS().text(topic, max_results=5)
            if not results:
                return "No specific search results found."
            
            context = "Real-time Search Results:\n"
            for i, res in enumerate(results):
                context += f"{i+1}. {res['title']}: {res['body']}\n"
            
            print(f"✅ Found {len(results)} search results.")
            return context
        except Exception as e:
            print(f"⚠️ Search failed: {e}")
            return "Search failed, rely on internal knowledge."

    def search_hot_topics(self):
        """
        Simulate searching for hot topics. 
        In a real scenario, this would call a News API or scrape Weibo/Baidu.
        """
        print("Searching for hot topics...")
        # Mock data based on 2026-02-09 search
        return [
            "2026年亚冬会短道速滑接力摘铜 孙龙怒吼",
            "2026日本大选 高市早苗",
            "OpenClaw AI Agent 平台爆火",
            "2026全球AI安全报告发布"
        ]

    def _style_html_content(self, html_content):
        """
        Post-process HTML content to add WeChat-compatible inline styles.
        Uses self.theme for dynamic coloring.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        primary = self.theme['primary']
        secondary = self.theme['secondary']
        text_color = self.theme['text']
        accent_bg = self.theme['accent_bg']

        style_type = self.theme.get('style_type', 'classic')

        # 1. Blockquotes
        for quote in soup.find_all('blockquote'):
            if style_type == 'classic':
                # Left border + background
                quote['style'] = f"border-left: 4px solid {primary}; padding-left: 15px; color: #666666; margin: 20px 0; font-style: italic; background-color: {secondary}; padding: 10px 15px;"
            elif style_type == 'modern':
                # Top/Bottom border + centered
                quote['style'] = f"border-top: 2px solid {primary}; border-bottom: 2px solid {primary}; padding: 15px 10px; color: {text_color}; margin: 25px 0; font-style: italic; text-align: center; background-color: transparent;"
            elif style_type == 'bubble':
                # Rounded bubble
                quote['style'] = f"background-color: {secondary}; border-radius: 12px; padding: 15px 20px; color: {text_color}; margin: 20px 0; font-style: italic; border: 1px solid {accent_bg};"
            elif style_type == 'industrial':
                # Industrial Retro: Boxed, KaiTi font, minimalistic
                quote['style'] = f"border: 1px solid {text_color}; padding: 25px; color: {text_color}; margin: 40px 0; font-family: 'KaiTi', 'SimKai', serif; font-style: normal; background-color: transparent; font-size: 15px; letter-spacing: 1px;"
            else:
                # Default
                quote['style'] = f"border-left: 4px solid {primary}; padding-left: 15px; color: #666666; margin: 20px 0; font-style: italic; background-color: {secondary}; padding: 10px 15px;"
            
        # 2. Strong/Bold
        for strong in soup.find_all(['strong', 'b']):
            if style_type == 'industrial':
                # Industrial: No background, just bold and slightly larger or underlined
                strong['style'] = f"color: #000000; font-weight: 900; border-bottom: 2px solid {text_color}; padding-bottom: 1px;"
            else:
                # Use dynamic accent highlight
                strong['style'] = f"color: {primary}; font-weight: bold; background: {accent_bg}; padding: 0 4px; border-radius: 2px;"
            
        # 3. Emphasis/Italic
        for em in soup.find_all(['em', 'i']):
            if style_type == 'industrial':
                em['style'] = f"color: {text_color}; font-family: 'FangSong', serif; font-style: italic; text-decoration: underline;"
            else:
                em['style'] = f"color: {primary}; font-style: italic;"
            
        # 4. Lists (ul/ol)
        # Fix: Apply list-style-type to BOTH ol/ul and li to ensure visibility in WeChat
        for ul in soup.find_all('ul'):
            if style_type == 'industrial':
                ul['style'] = "padding-left: 20px; margin: 25px 0; list-style-type: square;"
            else:
                ul['style'] = "padding-left: 20px; margin: 15px 0; list-style-type: disc;"
        
        for ol in soup.find_all('ol'):
            ol['style'] = "padding-left: 20px; margin: 15px 0; list-style-type: decimal;"
            
        for li in soup.find_all('li'):
            # Determine list type based on parent
            parent = li.parent
            list_style = "inherit"
            if parent:
                if parent.name == 'ol':
                    list_style = "decimal"
                elif parent.name == 'ul':
                    list_style = "disc"
                    if style_type == 'industrial':
                        list_style = "square"
            
            li['style'] = f"margin-bottom: 8px; color: {text_color}; list-style-type: {list_style};"
            
        # 5. Headings (h3/h4 in content)
        for h3 in soup.find_all('h3'):
            if style_type == 'classic':
                # Gradient bottom border, slight background
                h3['style'] = (
                    f"font-size: 18px; color: {text_color}; margin-top: 35px; margin-bottom: 20px; "
                    f"font-weight: bold; padding: 5px 10px; border-left: 5px solid {primary}; "
                    f"background: linear-gradient(to right, {secondary}, transparent); "
                    f"border-radius: 0 4px 4px 0;"
                )
            elif style_type == 'modern':
                # Bottom border only, minimal
                h3['style'] = (
                    f"font-size: 20px; color: {primary}; margin-top: 40px; margin-bottom: 20px; "
                    f"font-weight: bold; padding-bottom: 8px; border-bottom: 2px solid {primary}; "
                    f"display: inline-block; padding-right: 20px;"
                )
            elif style_type == 'bubble':
                # Capsule style
                h3['style'] = (
                    f"font-size: 18px; color: #ffffff; margin-top: 35px; margin-bottom: 20px; "
                    f"font-weight: bold; padding: 8px 15px; background-color: {primary}; "
                    f"border-radius: 20px; display: inline-block; box-shadow: 0 2px 5px {accent_bg};"
                )
            elif style_type == 'industrial':
                # Industrial Retro: Monospace, spaced out, bottom border line
                h3['style'] = (
                    f"font-family: 'Courier New', 'Songti SC', monospace; "
                    f"font-size: 20px; color: {text_color}; "
                    f"margin-top: 60px; margin-bottom: 30px; "
                    f"font-weight: bold; "
                    f"padding-left: 0; "
                    f"border-bottom: 2px solid {text_color}; "
                    f"display: inline-block; "
                    f"letter-spacing: 4px; "
                    f"line-height: 1.4;"
                )
            else:
                h3['style'] = (
                    f"font-size: 18px; color: {text_color}; margin-top: 35px; margin-bottom: 20px; "
                    f"font-weight: bold; padding: 5px 10px; border-left: 5px solid {primary}; "
                    f"background: linear-gradient(to right, {secondary}, transparent); "
                    f"border-radius: 0 4px 4px 0;"
                )

        return str(soup)

    def generate_article(self, topic, article_type):
        """
        Generate article content using LLM with RAG (Search Context).
        """
        # 1. Fetch Real Info
        search_context = self.fetch_real_info(topic)
        
        print(f"Generating article for topic: {topic} ({article_type})")
        
        if article_type == "zhihu_real":
            prompt = f"""
            Write a 'Zhihu High-Vote Style (Realistic Edition)' article about '{topic}'.
            Type: {article_type}
            
            REAL-TIME CONTEXT (Use this to ensure TRUTHFULNESS):
            {search_context}
            
            STYLE GUIDELINES (Must Follow):
            1. **Persona**: Frustrated Middle-aged / Awake Youth. NOT Elite. You are a "Realistic Observer" who has seen the truth of society.
            2. **Opening Hook**: Start with a concrete, painful reality or a "Heart-piercing Truth" (扎心真相). 
               - Templates: "说个扎心的真相...", "35岁...", "别听专家瞎吹...".
            3. **Narrative**: Personal Misery -> Social Context -> Resignation/Acceptance.
               - Focus on: "Degradation" (消费降级), "Involution" (内卷), "Lying Flat" (躺平), "Survival" (苟住).
            4. **Keywords**: 巨大的草台班子, 降本增效, 祛魅, 牛马, 窒息感.
            5. **Tone**: Calm desperation. Don't sell hope. Share the pain. Give permission to "give up" or "live simply".
            
            STRUCTURE & FORMATTING:
            - **No Title/Author in Body**.
            - **Short Paragraphs**: 1-3 lines max.
            - **Subheadings**: Use "Industrial Retro" style headers (short, punchy).
            - **Images**: Insert exactly 3 [IMAGE: description] placeholders reflecting "Realistic/Grounded/Melancholy" scenes.
            - **Language**: Simplified Chinese (简体中文), Colloquial (大白话).
            
            Return JSON format: {{ "title": "...", "summary": "...", "sections": [ {{ "heading": "...", "content": "..." }} ] }}
            """
        else:
            prompt = f"""
            Write a High-Readability WeChat Official Account article about '{topic}'.
            Type: {article_type}
            
            REAL-TIME CONTEXT (Use this to ensure TRUTHFULNESS):
            {search_context}
            
            CRITICAL WRITING GUIDELINES (Must Follow):
            1. **Title Strategy (Life or Death)**: 
               - Spend 50% of effort here.
               - Techniques: Contrast (e.g., "Monthly income 100k, eating 10 yuan lunch"), Front-loaded Benefits, Specific Numbers ("4 actions", not "many ways"), Secrecy ("The Truth", "Hidden").
            
            2. **Golden 3 Seconds (Opening)**:
               - Hook curiosity immediately. NO long intros.
               - Techniques: Conclusion first, Empathy scene (e.g., "2 AM in the office"), Controversial quote.
            
            3. **The Slide Effect (Structure)**:
               - **Hooks**: End every paragraph with a cliffhanger to keep them scrolling.
               - **SCQA Model**: Situation -> Complication -> Question -> Answer.
               - **Visual Decompression**: Short sentences. Paragraphs MAX 3 lines.
               - **Navigation**: Catchy subheadings every 300 words.
               - **Continuous Numbering**: When using numbered lists (1. 2. 3.), ensure they are in a SINGLE Markdown block so numbering is continuous. Do NOT break lists with images or long text unless necessary.
            
            4. **Social Currency (Shareability)**:
               - Express what readers want to say but can't (Golden Quotes).
               - Provide scarcity/utility.
               - Value resonance (Identity shaping).
            
            5. **The Final Kick (Closing)**:
               - Guide interaction.
               - Techniques: A/B Voting question ("Do you support A or B?"), Surprise gift in comments, Author Persona (Human touch/碎碎念).

            6. **Visuals & Depth**:
               - Insert exactly 3 [IMAGE: description] placeholders.
               - Include 2 "Deep Dive" paragraphs (philosophical/contrarian).
            
            General Requirements:
            - Language: Simplified Chinese (简体中文).
            - **Truthfulness**: Integrate the provided 'REAL-TIME CONTEXT' naturally. Cite facts or numbers if available in the context.
            - **NO Metadata in Body**: Do NOT include the Title, Author, or Date in the content sections. Start directly with the hook.
            - **Image Format**: Strictly use `[IMAGE: description]` for placeholders.
            - Title: MUST use one of the strategies above.
            - **Format**: Use Markdown. 
              - **Bold** for key points.
              - *Italic* for emphasis.
              - > Blockquotes for Golden Quotes/Key Insights.
            - Length: ~1200 words.
            - Return JSON format: {{ "title": "...", "summary": "...", "sections": [ {{ "heading": "...", "content": "..." }} ] }}
            """

        try:
            if not openai.api_key:
                raise ValueError("No OpenAI API Key found")
                
            response = openai.chat.completions.create(
                model="deepseek-chat", # Updated model name for DeepSeek
                messages=[
                    {"role": "system", "content": "You are an expert WeChat Official Account writer."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            data = json.loads(response.choices[0].message.content)
            
            # Post-process Markdown to HTML for each section content
            if "sections" in data:
                for section in data["sections"]:
                    if "content" in section:
                        # Convert markdown to html
                        raw_html = markdown.markdown(section["content"])
                        # Apply inline styles
                        section["content"] = self._style_html_content(raw_html)
            
            return data
        except Exception as e:
            print(f"Error generating article: {e}")
            print("⚠️ Switching to Mock Content generation due to error.")
            return self._generate_mock_article(topic, article_type)

    def _generate_mock_article(self, topic, article_type):
        """Fallback mock content"""
        return {
            "title": f"【重磅】{topic}：深度解析与未来展望",
            "summary": f"本文深入探讨了{topic}的最新进展...",
            "sections": [
                {"heading": "背景介绍", "content": f"关于{topic}的背景是这样的...（此处为模拟生成的长文本，用于展示排版效果）..."},
                {"heading": "核心分析", "content": f"从专业的角度来看，{topic}的影响深远..."},
                {"heading": "未来展望", "content": "我们要保持关注..."},
            ]
        }

    def _get_tone(self, article_type):
        tones = {
            "hot_topic": "Urgent, exciting, informative",
            "ai_news": "Professional, visionary, authoritative",
            "life": "Emotional, reflective, warm",
            "culture": "Deep, historical, storytelling",
            "zhihu_real": "Disillusioned, Calm, Pragmatic, Grounded, 'Insider' (but Grounded)",
            "other": "Informative, objective"
        }
        return tones.get(article_type, "Neutral")

    def generate_image(self, prompt):
        """
        Generate image using DALL-E or Volcengine (if configured), fallback to placeholder.
        """
        print(f"Generating image for prompt: {prompt}")
        
        # Use a consistent seed based on prompt hash to get same image for same topic
        seed = hash(prompt) % 1000
        # WeChat content image recommended width: 900px
        # Use 'seed' instead of 'id' to avoid 404s on missing IDs
        url = f"https://picsum.photos/seed/{abs(seed)}/900/500"
        return url

    def process_content_images(self, content):
        """
        Parse content for [IMAGE: description] tags, generate images, upload to WeChat (if publisher active),
        and replace tags with HTML using WeChat URLs.
        """
        import re
        
        def replace_match(match):
            image_prompt = match.group(1)
            image_url = self.generate_image(image_prompt)
            
            # Download the image locally first
            filename = f"img_{abs(hash(image_prompt)) % 10000}.jpg"
            local_path = self.download_image(image_url, filename)
            
            final_url = ""
            if local_path:
                # 1. Try to upload to WeChat to get a permanent URL for the article content
                if self.publisher:
                    wechat_url = self.publisher.upload_article_image(local_path)
                    if wechat_url:
                        final_url = wechat_url
                
                # 2. Fallback to local relative path if upload failed or no publisher (for local preview)
                if not final_url:
                    final_url = os.path.basename(local_path)
            
            if final_url:
                # Removed figcaption to hide prompt words as requested
                return f'''
                <figure style="margin: 30px 0; text-align: center;">
                    <img src="{final_url}" style="width: 100%; border-radius: 4px; box-shadow: 0 4px 20px rgba(0,0,0,0.5);" />
                </figure>
                '''
            return ""

        # Regex to find [IMAGE: ...]
        # Match case-insensitive [IMAGE: ...]
        new_content = re.sub(r'\[IMAGE:\s*(.*?)\]', replace_match, content, flags=re.IGNORECASE)
        return new_content

    def download_image(self, url, filename):
        """Download image to local path"""
        try:
            path = os.path.join(self.output_dir, filename)
            # Add timeout to prevent hanging
            response = requests.get(url, stream=True, timeout=15)
            if response.status_code == 200:
                with open(path, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                return path
            else:
                print(f"❌ Failed to download image. Status: {response.status_code}, URL: {url}")
                return None
        except Exception as e:
            print(f"❌ Exception downloading image: {e}")
            return None

    def publish_to_wechat(self, article_data, html_content, image_path):
        """
        Publish article to WeChat Draft.
        """
        if not self.publisher:
            print("Skipping WeChat push (Publisher not initialized)")
            return

        print(f"🚀 Pushing '{article_data['title']}' to WeChat...")
        
        try:
            # 1. Upload Cover Image
            thumb_media_id = None
            if image_path and os.path.exists(image_path):
                thumb_media_id, _ = self.publisher.upload_image(image_path)
            
            if not thumb_media_id:
                print("⚠️ No thumb_media_id, cannot upload article.")
                return

            # 2. Prepare Article Data
            article_payload = {
                "title": article_data['title'],
                "thumb_media_id": thumb_media_id,
                "author": "伊扎里斯的索拉尔",
                "digest": article_data.get('summary', '')[:100],
                "show_cover_pic": 1,
                "content": html_content,
                "content_source_url": "https://github.com/trae-ai"
            }
            
            # 3. Upload Draft
            media_id = self.publisher.upload_article([article_payload])
            print(f"✅ Successfully pushed to WeChat! Draft Media ID: {media_id}")
            return media_id
            
        except Exception as e:
            print(f"❌ Failed to push to WeChat: {e}")

    def format_html(self, article_data):
        """
        Format article into HTML using Jinja2 template.
        """
        # Process images in sections
        for section in article_data.get("sections", []):
            if "content" in section:
                section["content"] = self.process_content_images(section["content"])

        # Process QR Code (Upload to WeChat if exists)
        qrcode_path = os.path.join(self.output_dir, "qrcode.jpg")
        if os.path.exists(qrcode_path) and self.publisher:
            print("📤 Uploading QR Code to WeChat...")
            qr_url = self.publisher.upload_article_image(qrcode_path)
            if qr_url:
                article_data["qrcode_url"] = qr_url
                print(f"✅ QR Code uploaded: {qr_url}")
        
        template = self.env.get_template("article_template.html")
        return template.render(article=article_data, date=datetime.now().strftime("%Y-%m-%d"), theme=self.theme)

    def save_article(self, html_content, filename):
        path = os.path.join(self.output_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Saved article to {path}")

    def safety_check(self, content):
        """
        Perform safety checks on the content.
        """
        print("Performing safety check...")
        # Simple keyword check mock
        forbidden_words = ["forbidden", "illegal"]
        for word in forbidden_words:
            if word in content:
                print(f"Warning: Found forbidden word '{word}'")
                return False
        return True

    def run(self):
        # Define the plan
        # Generating 3 articles in "Zhihu Realistic Style" as requested
        plan = [
            {"topic": "35岁失业，去开滴滴丢人吗？", "type": "zhihu_real"},
            {"topic": "月薪2万，为什么我只敢吃15块钱的盒饭？", "type": "zhihu_real"},
            {"topic": "为什么现在的年轻人开始“断亲”了？", "type": "zhihu_real"},
        ]

        for i, item in enumerate(plan):
            # Author name override for this run
            article_data = self.generate_article(item["topic"], item["type"])
            if article_data:
                # Add image placeholder
                article_data["image_url"] = self.generate_image(article_data["title"])
                
                # Format
                html = self.format_html(article_data)
                
                # Safety Check
                if self.safety_check(html):
                    filename = f"article_{i+1}_{item['type']}.html"
                    self.save_article(html, filename)
                    
                    # Download Image for Cover
                    image_path = self.download_image(article_data["image_url"], f"cover_{i+1}.jpg")
                    
                    # Push to WeChat
                    # Modify article_data author before push if needed, 
                    # but wechat_publisher currently hardcodes author to "AI Generator" in publish_to_wechat.
                    # Let's fix that.
                    self.publish_to_wechat(article_data, html, image_path)
                    
                    # Sleep to avoid rate limits
                    time.sleep(2)
                else:
                    print(f"Article {i+1} failed safety check.")

if __name__ == "__main__":
    generator = WeChatArticleGenerator()
    # To run this, you need to set OPENAI_API_KEY in .env
    generator.run()
    # print("Generator initialized. Configure .env and uncomment run() to execute.")
