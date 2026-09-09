# Discord Event Bot

クイズ、くじなどの機能を備えたDiscord イベント bot です。

## 機能

### イベント管理
- `/event_create` - イベントを作成
- `/event_list` - イベント一覧を表示
- `/event_join` - イベントに参加
- `/event_leave` - イベントから退出

### クイズ
- `/quiz_create` - クイズを作成 (4肢問題)
- `/quiz_start` - クイズを開始
- `/quiz_answer` - クイズの答えを表示

### くじ
- `/lottery_create` - くじを作成
- `/lottery_draw` - くじに参加
- `/lottery_winner` - くじの当選者を抽選
- `/lottery_list` - くじ一覧を表示

## セットアップ

### 1. リポジトリをクローン
```bash
git clone https://github.com/haru515515-droid/discord-event-bot.git
cd discord-event-bot
```

### 2. 依存パッケージのインストール
```bash
pip install -r requirements.txt
```

### 3. Discord Bot Token の設定

**方法1: .env ファイルを使う**
```bash
cp .env.example .env
```
`.env` ファイルを編集して、`YOUR_BOT_TOKEN_HERE` をあなたの bot token に置き換えます。

**方法2: コードで直接設定**
`main.py` の最後の行を編集：
```python
bot.run('YOUR_BOT_TOKEN_HERE')
```

### 4. Bot を実行
```bash
python main.py
```

## Discord Bot Token の取得方法

1. [Discord Developer Portal](https://discord.com/developers/applications) にアクセス
2. 「New Application」をクリック
3. アプリケーション名を入力
4. 左のメニューから「Bot」を選択
5. 「Add Bot」をクリック
6. 「TOKEN」セクションの「Copy」をクリック
7. トークンを `.env` ファイルに貼り付け

## 使い方

### イベント作成例
```
/event_create
event_name: サマーパーティー
description: 皆で楽しむイベントです
date: 2024-08-15 19:00
```

### クイズ作成例
```
/quiz_create
quiz_name: 地理クイズ
question: 日本の首都はどこですか？
option_a: 大阪
option_b: 京都
option_c: 東京
option_d: 広島
answer: C
```

### くじ作成例
```
/lottery_create
lottery_name: 夏祭りくじ
description: 楽しい景品がいっぱい
prizes: 花火セット, アイスクリーム, うちわ
quantity: 1
```

## ファイル構成

```
discord-event-bot/
├── main.py              # メインプログラム
├── requirements.txt     # 依存パッケージ
├── .env.example         # 環境変数のテンプレート
├── events.json          # イベントデータ（自動生成）
├── quizzes.json         # クイズデータ（自動生成）
├── lotteries.json       # くじデータ（自動生成）
└── README.md            # このファイル
```

## データ保存形式

すべてのデータは JSON 形式でローカルに保存されます。

### events.json
```json
{
  "1": {
    "name": "イベント名",
    "description": "説明",
    "date": "2024-08-15 19:00",
    "creator": "123456789",
    "participants": ["987654321"],
    "created_at": "2024-08-01T10:00:00"
  }
}
```

### quizzes.json
```json
{
  "1": {
    "name": "クイズ名",
    "question": "問題文",
    "options": {
      "A": "選択肢A",
      "B": "選択肢B",
      "C": "選択肢C",
      "D": "選択肢D"
    },
    "answer": "C",
    "creator": "123456789",
    "created_at": "2024-08-01T10:00:00"
  }
}
```

### lotteries.json
```json
{
  "1": {
    "name": "くじ名",
    "description": "説明",
    "prizes": ["景品1", "景品2"],
    "quantity_per_prize": 1,
    "tickets": ["123456789"],
    "winners": [["123456789", "景品1"]],
    "creator": "123456789",
    "created_at": "2024-08-01T10:00:00"
  }
}
```

## トラブルシューティング

### Bot がオンラインにならない
- Bot token が正しいか確認
- Intents が有効になっているか確認
- Discord Developer Portal で Bot の権限を確認

### コマンドが表示されない
- Bot を再起動
- スラッシュコマンド同期を待つ（最大1分）
- Bot にアプリケーションコマンド権限があるか確認

## ライセンス

MIT License

## 開発者

haru515515-droid
