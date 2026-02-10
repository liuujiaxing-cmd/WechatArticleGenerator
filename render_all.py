import json
import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

def render_all():
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("article_template.html")

    with open("content.json", "r", encoding="utf-8") as f:
        articles = json.load(f)

    for i, article in enumerate(articles):
        html_content = template.render(article=article, date=datetime.now().strftime("%Y-%m-%d"))
        filename = f"article_{i+1}_{article['type']}.html"
        path = os.path.join(output_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Generated: {path}")

if __name__ == "__main__":
    render_all()
