# AIニュースダイジェストの設定ファイル

# RSSフィードの一覧
AI_FEEDS = [
    # Google/Gemini関連
    "https://blog.google/technology/ai/rss/",
    "https://ai.googleblog.com/feeds/posts/default",
    
    # Microsoft関連
    "https://blogs.microsoft.com/ai/feed/",
    "https://techcommunity.microsoft.com/t5/microsoft-ai-blog/bg-p/ArtificialIntelligence/rss",
    
    # Anthropic/Claude関連
    "https://www.anthropic.com/blog/rss",
    
    # arXiv AI論文フィード
    "http://export.arxiv.org/rss/cs.AI"
]

# フィルタリングに使用するキーワード
KEYWORDS = ["生成AI", "大規模言語モデル", "LLM", "Claude", "Gemini", "GPT", "Copilot", 
            "Anthropic", "OpenAI", "transformers"]

# その他の設定
HOURS_BACK = 24  # 何時間前までの記事を収集するか
MAX_ENTRIES = 10  # ダイジェストに含める最大記事数