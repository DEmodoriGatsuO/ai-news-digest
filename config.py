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
KEYWORDS = [
    "生成AI", "大規模言語モデル", "LLM", "Claude", "Gemini", "GPT", "人工知能", 
    "機械学習", "深層学習", "AI倫理", "AIガバナンス", "マルチモーダル", "音声認識",
    "画像認識", "自然言語処理", "NLP", "強化学習", "Anthropic", "Microsoft AI",
    "Google AI", "OpenAI", "transformers", "RLHF", "ニューラルネットワーク"
]

# その他の設定
HOURS_BACK = 24  # 何時間前までの記事を収集するか
MAX_ENTRIES = 10  # ダイジェストに含める最大記事数