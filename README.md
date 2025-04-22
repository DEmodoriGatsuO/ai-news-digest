# AI News Digest

AIニュース集約ツールは、AIに関する最新情報を自動で収集し、要約するシステムです。GitHub Actionsによって定期実行され、最新のAI動向を常に把握することができます。

## 特徴

- 主要なAIニュースソースから最新情報を自動収集
- Google Gemini AIを利用した記事内容の自動要約
- Microsoft、Claude、Gemini関連の情報に特化したフィルタリング
- GitHub Pagesによる自動更新されるWebサイト
- Slack通知機能（オプション）

## セットアップ方法

### 1. リポジトリのフォーク

このリポジトリをフォークして、自分のGitHubアカウントにコピーします。

### 2. シークレットの設定

フォークしたリポジトリで以下のシークレットを設定します:

1. リポジトリの「Settings」→「Secrets and variables」→「Actions」を開く
2. 「New repository secret」をクリック
3. 以下のシークレットを追加:
   - `GEMINI_API_KEY`: Google Gemini APIキー（必須）
   - `SLACK_WEBHOOK_URL`: Slack通知用のWebhook URL（オプション）

### 3. GitHub Pagesの有効化

1. リポジトリの「Settings」→「Pages」を開く
2. Source を「Deploy from a branch」に設定
3. Branch を「main」、フォルダを「/docs」に設定
4. 「Save」ボタンをクリック

### 4. 設定のカスタマイズ（オプション）

`config.py` ファイルを編集して、以下をカスタマイズできます:

- RSSフィードの追加/削除
- フィルタリングキーワードの調整
- 収集期間や表示件数の変更

## 手動実行方法

GitHub Actionsの「Actions」タブから、「AI News Digest Generator」ワークフローを選択し、「Run workflow」ボタンをクリックすると、手動で実行できます。

## 定期実行について

デフォルトでは、6時間ごと（0時、6時、12時、18時）に自動実行されます。
この設定は `.github/workflows/ai-digest.yml` ファイルの `cron` 設定で変更できます。

## ローカルでの実行方法

```bash
# リポジトリのクローン
git clone https://github.com/[username]/ai-news-digest.git
cd ai-news-digest

# 依存関係のインストール
pip install -r requirements.txt

# 環境変数の設定
export GEMINI_API_KEY="your-api-key"
export SLACK_WEBHOOK_URL="your-webhook-url"  # オプション

# スクリプトの実行
python ai_news_digest.py