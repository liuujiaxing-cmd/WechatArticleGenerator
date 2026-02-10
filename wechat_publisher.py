# coding:utf-8
import os
import time
from dotenv import load_dotenv
from wechatpy import WeChatClient
from wechatpy.exceptions import WeChatClientException
import requests

# Load environment variables
load_dotenv()

APP_ID = os.getenv("WECHAT_APP_ID")
APP_SECRET = os.getenv("WECHAT_APP_SECRET")

class WeChatPublisher:
    def __init__(self):
        if not APP_ID or not APP_SECRET:
            raise ValueError("Please set WECHAT_APP_ID and WECHAT_APP_SECRET in .env")
        
        self.client = WeChatClient(APP_ID, APP_SECRET)
        self.access_token = self.client.access_token
        print(f"✅ WeChatClient initialized. Token: {self.access_token[:10]}...")

    def upload_image(self, image_path):
        """
        Upload an image to WeChat material library (for Cover Image).
        Returns the media_id and url.
        """
        print(f"📤 Uploading cover image: {image_path}")
        try:
            with open(image_path, 'rb') as f:
                # Upload as permanent material (image)
                # WeChat requires 'media' parameter
                res = self.client.material.add('image', f)
                print(f"✅ Cover Image uploaded. Media ID: {res['media_id']}")
                return res['media_id'], res['url']
        except WeChatClientException as e:
            print(f"❌ Failed to upload cover image: {e}")
            raise e

    def upload_article_image(self, image_path):
        """
        Upload an image for use INSIDE the article content.
        This uses the 'media.upload_image' (or upload_mass_image) API which returns a URL, not a media_id.
        """
        print(f"📤 Uploading content image: {image_path}")
        try:
            with open(image_path, 'rb') as f:
                # Correct method name for content image is upload_image (or upload_mass_image)
                # It returns the URL directly (processed by result_processor in wechatpy)
                url = self.client.media.upload_image(f)
                print(f"✅ Content Image uploaded. URL: {url}")
                return url
        except WeChatClientException as e:
            print(f"❌ Failed to upload content image: {e}")
            return None

    def upload_article(self, articles):
        """
        Upload articles (drafts) using the new Draft API.
        articles: list of dicts.
        """
        print(f"📝 Uploading {len(articles)} articles to Draft Box...")
        # The old material/add_news API is deprecated (Error 45106).
        # We must use the new draft/add API.
        # https://api.weixin.qq.com/cgi-bin/draft/add?access_token=ACCESS_TOKEN
        
        try:
            # construct payload
            data = {"articles": articles}
            # Use client.post to handle access_token automatically
            # Note: client.post expects a relative URL or full URL.
            # Base URL is usually https://api.weixin.qq.com/cgi-bin/
            res = self.client.post('draft/add', data=data)
            print(f"✅ Draft created. Media ID: {res['media_id']}")
            return res['media_id']
        except WeChatClientException as e:
            print(f"❌ Failed to upload draft: {e}")
            raise e

    def get_user_list(self):
        """Test connection by getting user list"""
        try:
            users = self.client.user.get()
            print(f"👥 User list: {users}")
            return users
        except WeChatClientException as e:
            print(f"❌ Failed to get user list: {e}")
            raise e

if __name__ == "__main__":
    # Test connection
    try:
        publisher = WeChatPublisher()
        # Test basic API call
        publisher.get_user_list()
        
        # Test Image Upload (if file exists)
        # dummy_image = "test_image.jpg"
        # if os.path.exists(dummy_image):
        #     media_id, url = publisher.upload_image(dummy_image)
            
        # Test Article Upload (Draft)
        # article = {
        #     "title": "Test Article from Code",
        #     "thumb_media_id": media_id if 'media_id' in locals() else "MEDIA_ID_HERE",
        #     "author": "AI Generator",
        #     "digest": "This is a test digest",
        #     "show_cover_pic": 1,
        #     "content": "<p>Hello WeChat!</p>",
        #     "content_source_url": "https://example.com"
        # }
        # publisher.upload_article([article])
        
    except Exception as e:
        print(f"Test failed: {e}")
