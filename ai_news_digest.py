import feedparser
import datetime
import time
import os
import json
import google.generativeai as genai
import logging
from pathlib import Path

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ai_news_digest')

# 設定ファイルのインポート
try:
    from config import AI_FEEDS, KEYWORDS
except ImportError:
    # デフォルト設定
    logger.info("config.pyが見つかりません。デフォルト設定を使用します。")
    AI_FEEDS = [
        # Google/Gemini関連
        "https://blog.google/technology/ai/rss/",
        "https://ai.googleblog.com/feeds/posts/default",
        
        # Microsoft関連
        "https://blogs.microsoft.com/ai/feed/",
        "https://techcommunity.microsoft.com/t5/microsoft-ai-blog/bg-p/ArtificialIntelligence/rss",
        
        # Anthropic/Claude関連
        "https://www.anthropic.com/blog/rss"
    ]
    
    KEYWORDS = ["生成AI", "大規模言語モデル", "LLM", "Claude", "Gemini", "GPT", "人工知能", 
               "機械学習", "深層学習", "AI倫理", "AIガバナンス", "マルチモーダル", "音声認識",
               "画像認識", "自然言語処理", "NLP", "強化学習", "Anthropic", "Microsoft AI",
               "Google AI", "OpenAI", "transformers", "RLHF", "ニューラルネットワーク"]

# APIキー設定
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    logger.error("GEMINI_API_KEYが設定されていません。")
    raise ValueError("GEMINI_API_KEYが必要です。GitHub Secretsで設定してください。")

def get_feed_entries(feed_url, hours_back=24):
    """指定時間内の記事を取得"""
    entries = []
    current_time = datetime.datetime.now()
    
    try:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            # 公開日を解析（フィールド名が異なる場合に対応）
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published = datetime.datetime.fromtimestamp(time.mktime(entry.published_parsed))
            elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                published = datetime.datetime.fromtimestamp(time.mktime(entry.updated_parsed))
            else:
                # 日付情報がない場合は現在時刻を使用
                published = current_time
            
            time_diff = current_time - published
            
            # 指定時間内の記事のみ抽出
            if time_diff.total_seconds() < hours_back * 3600:
                entries.append({
                    "title": entry.title,
                    "link": entry.link,
                    "published": published,
                    "summary": entry.summary if hasattr(entry, "summary") else "",
                    "source": feed.feed.title if hasattr(feed.feed, "title") else feed_url
                })
        logger.info(f"フィード {feed_url} から {len(entries)} 件の記事を取得しました")
    except Exception as e:
        logger.error(f"フィード {feed_url} の解析中にエラーが発生しました: {e}")
    
    return entries

def summarize_with_gemini(text, max_tokens=100):
    """Gemini公式ライブラリを使用して要約を生成"""
    try:
        # Geminiモデルの設定
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # 要約の生成
        prompt = f"以下のAI関連記事を3-4文で要約してください。重要なポイントと影響を含めてください。\n\n{text}"
        
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=max_tokens,
                temperature=0.2
            )
        )
        
        return response.text
    except Exception as e:
        logger.error(f"要約の生成に失敗しました: {str(e)}")
        return f"要約生成エラー: {str(e)[:100]}..."

def filter_by_keywords(entry, keywords=KEYWORDS):
    """重要なキーワードによるフィルタリング"""
    # タイトルと要約からキーワードを検索
    text = (entry["title"] + " " + entry["summary"]).lower()
    for keyword in keywords:
        if keyword.lower() in text:
            return True
    
    return False

def format_text_digest(entries, max_entries=10):
    """テキスト形式でダイジェストを出力"""
    digest = f"🤖 AI最新ニュースダイジェスト 🤖\n{datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M')}\n\n"
    
    for i, entry in enumerate(entries[:max_entries], 1):
        digest += f"【{i}】{entry['title']} ({entry['source']})\n"
        digest += f"🔗 {entry['link']}\n"
        digest += f"📅 {entry['published'].strftime('%Y年%m月%d日')}\n"
        digest += f"💡 {entry['ai_summary']}\n\n"
    
    digest += f"---\n合計 {len(entries)} 件のAI関連ニュースが見つかりました。"
    return digest

def format_markdown_digest(entries, max_entries=10):
    """GitHub Pages用のMarkdown形式でダイジェストを出力"""
    today = datetime.datetime.now().strftime('%Y年%m月%d日')
    
    digest = f"""---
layout: default
title: AI最新ニュースダイジェスト {today}
---

# AI最新ニュースダイジェスト
**更新日時: {datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M')}**

"""
    
    for i, entry in enumerate(entries[:max_entries], 1):
        digest += f"## {i}. {entry['title']}\n\n"
        digest += f"**ソース**: {entry['source']}  \n"
        digest += f"**日付**: {entry['published'].strftime('%Y年%m月%d日')}  \n"
        digest += f"**リンク**: [{entry['link']}]({entry['link']})  \n\n"
        digest += f"{entry['ai_summary']}  \n\n"
        digest += "---\n\n"
    
    digest += f"*合計 {len(entries)} 件のAI関連ニュースが見つかりました。*\n"
    return digest

def update_index_page(latest_file_path):
    """GitHub Pages用のインデックスページを更新"""
    index_path = Path('docs/index.md')
    archives_path = Path('docs/archives')
    
    # アーカイブ一覧を取得
    archives = []
    if archives_path.exists():
        archives = sorted([f for f in archives_path.glob('*.md')], reverse=True)
    
    # インデックスページの内容を生成
    index_content = """---
layout: default
title: AI News Digest
---

# AI News Digest

最新のAI関連ニュースを自動で収集・要約したダイジェストです。

## 最新のダイジェスト

"""
    
    # 最新のダイジェストへのリンク
    latest_filename = latest_file_path.name
    latest_date = latest_filename.replace('digest_', '').replace('.md', '')
    index_content += f"- [{latest_date}のダイジェスト](./archives/{latest_filename})\n\n"
    
    # アーカイブリスト
    index_content += "## アーカイブ\n\n"
    for archive in archives[:10]:  # 最新10件のみ表示
        archive_date = archive.name.replace('digest_', '').replace('.md', '')
        index_content += f"- [{archive_date}](./archives/{archive.name})\n"
    
    # インデックスページを保存
    if not index_path.parent.exists():
        index_path.parent.mkdir(parents=True)
    
    index_path.write_text(index_content, encoding='utf-8')
    logger.info(f"インデックスページを更新しました: {index_path}")

def send_to_slack(digest, webhook_url):
    """Slackにダイジェストを送信"""
    if not webhook_url:
        logger.warning("SLACK_WEBHOOK_URLが設定されていないため、Slack通知はスキップします。")
        return False
    
    try:
        import requests
        
        # 文字数制限に対応するため要約
        short_digest = digest.split("\n\n")[0] + "\n\n"  # タイトル部分のみ
        short_digest += "新しいAIニュースダイジェストが生成されました。詳細はGitHub Pagesをご覧ください。"
        
        payload = {
            "text": short_digest,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": short_digest
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "詳細を見る"
                            },
                            "url": "https://[username].github.io/ai-news-digest/"  # GitHubユーザー名とリポジトリ名に応じて変更
                        }
                    ]
                }
            ]
        }
        
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 200:
            logger.info("Slackへの通知に成功しました")
            return True
        else:
            logger.error(f"Slackへの通知に失敗しました: ステータスコード {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"Slack通知中にエラーが発生しました: {e}")
        return False

def main():
    today_str = datetime.datetime.now().strftime('%Y%m%d')
    all_entries = []
    
    # ディレクトリの準備
    docs_path = Path('docs')
    archives_path = Path('docs/archives')
    
    if not docs_path.exists():
        docs_path.mkdir(parents=True)
    
    if not archives_path.exists():
        archives_path.mkdir(parents=True)
    
    # 全フィードから記事を収集
    for feed_url in AI_FEEDS:
        logger.info(f"フィードを解析中: {feed_url}")
        entries = get_feed_entries(feed_url)
        all_entries.extend(entries)
    
    # キーワードでフィルタリング
    filtered_entries = [entry for entry in all_entries if filter_by_keywords(entry)]
    logger.info(f"合計 {len(filtered_entries)} 件の関連記事が見つかりました")
    
    # 公開日で並べ替え
    filtered_entries.sort(key=lambda x: x["published"], reverse=True)
    
    # 記事がない場合の処理
    if not filtered_entries:
        logger.warning("関連記事が見つかりませんでした")
        return
    
    # 要約を生成
    for entry in filtered_entries:
        content = f"タイトル: {entry['title']}\n本文: {entry['summary']}"
        entry["ai_summary"] = summarize_with_gemini(content)
        time.sleep(1)
    
    # テキスト形式のダイジェストを生成
    text_digest = format_text_digest(filtered_entries)
    
    # Markdown形式のダイジェストを生成
    md_digest = format_markdown_digest(filtered_entries)
    
    # テキストファイルに保存
    txt_path = Path(f"ai_digest_{today_str}.txt")
    txt_path.write_text(text_digest, encoding='utf-8')
    logger.info(f"テキストダイジェストを保存しました: {txt_path}")
    
    # Markdownファイルに保存 (GitHub Pages用)
    md_filename = f"digest_{today_str}.md"
    md_path = archives_path / md_filename
    md_path.write_text(md_digest, encoding='utf-8')
    logger.info(f"Markdownダイジェストを保存しました: {md_path}")
    
    # インデックスページを更新
    update_index_page(md_path)

if __name__ == "__main__":
    main()