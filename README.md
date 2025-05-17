# Website Scraper

ウェブサイトから記事コンテンツをスクレイピングし、Markdownファイルとして保存するPythonツールです。XMLサイトマップとHTMLサイトマップの両方に対応しており、WordPressサイトにも最適化されています。

## 特徴

- ウェブサイトの記事コンテンツを自動抽出
- XMLサイトマップとHTMLサイトマップの両方に対応
- WordPressサイト専用の最適化
- サイトマップインデックスにも対応（複数サイトマップの処理）
- HTMLをMarkdown形式に変換
- 記事のタイトル、URL、公開日などのメタデータを保存
- 重複記事の処理を回避
- 適切な待機時間でサーバー負荷に配慮

## インストール

```bash
# リポジトリをクローン
git clone https://github.com/hiirofish/website_scraper.git
cd website_scraper

# 依存パッケージをインストール
pip install -r requirements.txt
```

## 必要条件

- Python 3.6以上
- requests
- beautifulsoup4
- html2text

## 基本的な使用方法

### 標準的なサイト

```bash
python scraper.py --url https://example.com/
```

### WordPressサイト

```bash
python scraper.py --url https://example.com/ --wordpress
```

### 特定のサイトマップを指定

```bash
python scraper.py --url https://example.com/ --sitemap https://example.com/post-sitemap.xml
```

## オプション

```
--url URL           スクレイピング対象URL（必須）
--output-dir DIR    出力先ディレクトリ（デフォルト: scraped_articles）
--delay SECONDS     リクエスト間の遅延（デフォルト: 1）
--max-pages NUM     最大取得ページ数（デフォルト: 無制限）
--sitemap URL       サイトマップURL（省略可能）
--wordpress         WordPressサイトマップを試行（デフォルト: False）
```

## サポートするサイトマップ形式

- XMLサイトマップ（sitemap.xml）
- WordPressサイトマップ（post-sitemap.xml等）
- XMLサイトマップインデックス
- HTMLサイトマップページ

## カスタマイズ

サイト構造に合わせて以下の関数を調整できます：

- `extract_content()`: 記事本文の抽出
- `extract_date()`: 公開日付の抽出

```python
def extract_content(self, soup):
    """記事の本文コンテンツを抽出する（サイト構造に合わせてカスタマイズ）"""
    if soup is None:
        return None
        
    # サイト固有のセレクターを追加
    if 'example.com' in self.base_url:
        article = soup.select_one('.article-content, .post-body')
    else:
        article = soup.select_one('article, .entry-content, .post-content, main')
    
    # 以下省略...
```

## トラブルシューティング

### 記事が抽出されない場合

1. **サイトマップURLの確認**: `--sitemap`オプションで正確なURLを指定
2. **セレクターの調整**: サイト構造に合わせて`extract_content()`を修正
3. **遅延時間の増加**: `--delay`の値を大きくしてサーバー負荷を軽減

## 使用例

### 特定数の記事のみを取得
```bash
python scraper.py --url https://example.com/ --max-pages 10
```

### サーバー負荷に配慮
```bash
python scraper.py --url https://example.com/ --delay 3
```

## 高度な使用法

### 複数サイトの一括処理
```bash
#!/bin/bash
python scraper.py --url https://site1.com/ --wordpress --output-dir site1_articles
python scraper.py --url https://site2.com/ --output-dir site2_articles
```

### 定期的な更新
crontabに追加して定期実行：
```
# 毎日午前2時に実行
0 2 * * * /path/to/scraper_script.sh
```

## 注意事項

- ウェブサイトの利用規約に従ってください
- robots.txtファイルを尊重してください
- サーバーに過度な負荷をかけないようにリクエスト間に適切な待機時間を設定してください
- 著作権で保護されたコンテンツを不適切に使用しないでください

## ライセンス

MIT

## 貢献

プルリクエストや機能リクエストを歓迎します。大きな変更を加える前に、まず問題を開いて議論するようにしてください。