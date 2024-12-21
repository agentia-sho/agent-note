# Note.com Search API

Note.comの記事を検索するためのRESTful APIです。FastAPIとPlaywrightを使用して実装されています。

## 機能

- Note.comの記事検索
- ソート機能（いいね数、人気順、新着順）
- スクロール数の指定による検索結果の調整

## API エンドポイント

### GET /search

記事を検索します。

**パラメータ:**
- `q` (必須): 検索キーワード
- `sort` (オプション): ソート方法（"like", "popular", "new"）
- `num_scrolls` (オプション): スクロール回数（1-10、デフォルト: 3）

**レスポンス例:**
```json
{
  "results": [
    {
      "title": "記事タイトル",
      "url": "記事URL",
      "author": {
        "name": "著者名",
        "url": "著者プロフィールURL"
      },
      "price": 0,
      "createdAt": "2023-12-21T00:00:00",
      "likeCount": 100,
      "thumbnailUrl": "サムネイルURL",
      "remainingCount": null
    }
  ]
}
```

## セットアップ

1. リポジトリのクローン:
```bash
git clone [your-repo-url]
cd note-search-api
```

2. 依存関係のインストール:
```bash
pip install -r requirements.txt
```

3. Playwrightのセットアップ:
```bash
playwright install
playwright install-deps
```

4. サーバーの起動:
```bash
uvicorn main:app --reload
```

## Docker での実行

```bash
docker build -t note-search-api .
docker run -p 8000:8000 note-search-api
```

## API ドキュメント

サーバー起動後、以下のURLでSwagger UIにアクセスできます：
- http://localhost:8000/docs
- http://localhost:8000/redoc

## デプロイ

このAPIはRenderでのデプロイを想定して作られています。
Dockerfileが含まれているため、Renderで直接デプロイすることができます。

## ライセンス

MIT 