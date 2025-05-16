# Website Scraper

ウェブサイトから記事コンテンツをスクレイピングし、Markdownファイルとして保存するPythonツールです。XMLサイトマップとHTMLサイトマップの両方に対応しており、WordPress（Cocoonテーマ、WP Sitemap Pageプラグイン）サイトにも最適化されています。

## 特徴

- ウェブサイトの記事コンテンツを自動抽出
- XMLサイトマップとHTMLサイトマップの両方に対応
- WordPressサイト（Cocoonテーマ、WP Sitemap Pageプラグインなど）専用の最適化
- サイトマップインデックスにも対応（複数サイトマップの処理）
- HTMLをMarkdown形式に変換
- 記事のタイトル、URL、公開日などのメタデータを保存
- 重複記事の処理を回避
- 適切な待機時間でサーバー負荷に配慮

## インストール

```bash
# リポジトリをクローン
git clone https://github.com/yourusername/website-scraper.git
cd website-scraper

# 依存パッケージをインストール
pip install -r requirements.txt
```

## 必要条件

- Python 3.6以上
- 以下のパッケージが必要です:
  - requests
  - beautifulsoup4
  - html2text

## 使い方

### 基本的な使い方

```bash
python scraper_complete.py --url https://example.com
```

### WordPressサイト向け

```bash
python scraper_complete.py --url https://example.com --wordpress
```

### XMLサイトマップ対応サイトの場合

```bash
# 自動的にsitemap.xmlを検出
python scraper_complete.py --url https://example.com
```

### 特定のサイトマップを指定する場合

```bash
python scraper_complete.py --url https://example.com --sitemap https://example.com/post-sitemap.xml
```

### オプション

```
--url URL           スクレイピング対象のベースURL（必須）
--output-dir DIR    出力先ディレクトリ（デフォルト: scraped_articles）
--delay SECONDS     リクエスト間の遅延秒数（デフォルト: 1）
--max-pages NUM     最大取得ページ数（デフォルト: 無制限）
--sitemap URL       サイトマップページのURL（省略可能）
--wordpress         WordPressサイトマップを試行する（デフォルト: False）
```

## サポートするサイトマップ形式

- XMLサイトマップ（標準的なsitemap.xml）
- WordPressサイトマップ（post-sitemap.xml, page-sitemap.xmlなど）
- XMLサイトマップインデックス（複数のサイトマップを含むファイル）
- HTMLサイトマップページ（リンク一覧ページなど）

## カスタマイズ

他のウェブサイトでこのスクレイパーを使用する場合は、サイト構造に合わせて以下の関数を調整する必要があるかもしれません:

- `extract_content`: 記事の本文を抽出するセレクターを調整
- `extract_date`: 公開日付を抽出するセレクターを調整

## 注意事項

- ウェブサイトの利用規約に従ってください
- robots.txtファイルを尊重してください
- サーバーに過度な負荷をかけないようにリクエスト間に適切な待機時間を設定してください
- 著作権で保護されたコンテンツを不適切に使用しないでください

## 詳細ドキュメント

詳細な使用方法とカスタマイズガイドについては、[使用ガイド.md](使用ガイド.md)を参照してください。

## ライセンス

MIT

## 貢献

プルリクエストや機能リクエストを歓迎します。大きな変更を加える前に、まず問題を開いて議論するようにしてください。
