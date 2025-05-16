# Website Scraper 使用ガイド

このツールはウェブサイトから記事コンテンツをスクレイピングし、Markdownファイルとして保存するPythonスクリプトです。XMLサイトマップとHTMLサイトマップの両方に対応しており、WordPressサイト（特にCocoonテーマやWP Sitemap Pageプラグイン）にも最適化されています。

## 基本的な使用方法

### WordPressサイト向けの使用例

```bash
python scraper_complete.py --url https://example.com/ --wordpress --output-dir wordpress_articles
```

これにより、WordPressサイトの記事が自動的にスクレイピングされ、`wordpress_articles`ディレクトリにMarkdownファイルとして保存されます。`--wordpress`オプションを指定すると、一般的なWordPressサイトマップパターン（post-sitemap.xml, page-sitemap.xmlなど）が確認されます。

### take1bit.com向けの使用例

```bash
python scraper_complete.py --url https://take1bit.com/ --output-dir take1bit_articles --delay 2
```

### XMLサイトマップを持つサイト向けの使用例

```bash
python scraper_complete.py --url https://example.com/ --output-dir example_articles
```

上記のコマンドでは、スクリプトは自動的に`https://example.com/sitemap.xml`を探してスクレイピングを行います。

### 特定のサイトマップを指定する場合

```bash
python scraper_complete.py --url https://example.com/ --sitemap https://example.com/post-sitemap.xml
```

### オプションの説明

```
--url URL           スクレイピング対象のベースURL（必須）
--output-dir DIR    出力先ディレクトリ（デフォルト: scraped_articles）
--delay SECONDS     リクエスト間の遅延秒数（デフォルト: 1）
--max-pages NUM     最大取得ページ数（デフォルト: 無制限）
--sitemap URL       サイトマップページのURL（省略可能）
--wordpress         WordPressサイトマップを試行する（デフォルト: False）
```

## サイトマップ形式のサポート

このツールは以下のサイトマップ形式をサポートしています：

1. **標準XMLサイトマップ**: `sitemap.xml`など
2. **WordPressサイトマップ**: `post-sitemap.xml`, `page-sitemap.xml`など
3. **XMLサイトマップインデックス**: 複数のサイトマップを含むインデックスファイル
4. **HTMLサイトマップ**: HTML形式のサイトマップページ（take1bit.comなど）

スクリプトは自動的にサイトマップの形式を判別し、適切に処理します。特にWordPressサイトの場合は、Cocoonテーマやプラグインによって生成される様々なサイトマップパターンを検出します。

## WordPressサイト向けの特別対応

WordPressサイト（Cocoonテーマ、WP Sitemap Pageプラグインなど）では、以下のサイトマップパターンが自動的にチェックされます：

- `sitemap.xml` - メインサイトマップまたはインデックス
- `sitemap_index.xml` - サイトマップインデックス
- `post-sitemap.xml` - 投稿記事のサイトマップ
- `page-sitemap.xml` - 固定ページのサイトマップ
- `category-sitemap.xml` - カテゴリーのサイトマップ
- `tag-sitemap.xml` - タグのサイトマップ

`--wordpress`オプションを使用すると、より積極的にこれらのパターンをチェックします。

## 制限と注意点

1. **take1bit.com固有の設定**：
   - このスクリプトは`take1bit.com`向けに特別な処理（サイトマップURLなど）を含んでいます
   - 他のサイトでは、それぞれのサイト構造に合わせた調整が必要な場合があります

2. **サイト構造依存性**：
   - 記事コンテンツの抽出はHTMLセレクターを使用しているため、サイト構造が変わると調整が必要です
   - 特に以下の関数は調整が必要な場合があります：
     - `extract_content()`：記事本文の抽出
     - `extract_date()`：公開日付の抽出

3. **稼働確認済みサイト**：
   - take1bit.com
   - 標準的なXMLサイトマップを持つサイト
   - WordPressサイト（Cocoonテーマ、WP Sitemap Pageプラグイン）

## トラブルシューティング

### 記事が抽出されない場合

1. **サイトマップURLの確認**：
   - 各サイトのサイトマップページURLが正しいか確認してください
   - WordPressサイトの場合は `--wordpress` オプションを使用してみてください
   - 特定のサイトマップが分かっている場合は `--sitemap` オプションで直接指定してください

2. **ネットワーク接続の確認**：
   - サイトにアクセスできるか確認してください
   - DNSエラーが発生する場合は、ドメイン名が正しいか確認してください

3. **セレクターの調整**：
   - スクレイピング対象のサイトが記事をどのようなHTML構造で提供しているか調査し、
     必要に応じて`extract_content()`メソッドのセレクターを調整してください

4. **XMLサイトマップの検証**：
   - 対象サイトのXMLサイトマップが標準形式に準拠しているか確認してください
   - 非標準の場合は`--sitemap`オプションで正確なURLを指定してください

## 使用例詳細

### WordPressサイトの記事を取得

```bash
python scraper_complete.py --url https://example.com/ --wordpress
```

### 特定数の記事のみを取得

```bash
python scraper_complete.py --url https://take1bit.com/ --max-pages 10
```

### 特定のディレクトリに保存

```bash
python scraper_complete.py --url https://take1bit.com/ --output-dir my_articles
```

### サーバー負荷に配慮した設定

```bash
python scraper_complete.py --url https://take1bit.com/ --delay 3
```

### 独自のサイトマップURLを指定

```bash
python scraper_complete.py --url https://example.com/ --sitemap https://example.com/post-sitemap.xml
```

## サイト別の推奨設定

### WordPressサイト（Cocoonテーマ、WP Sitemap Pageプラグイン）

```bash
python scraper_complete.py --url https://example.com/ --wordpress --delay 2
```

### 一般的なブログサイト

```bash
python scraper_complete.py --url https://example.com/ --delay 2
```

### 特定のサイトマップ構造を持つサイト

```bash
python scraper_complete.py --url https://example.com/ --sitemap https://example.com/specific-sitemap.xml
```

## カスタマイズ方法

### 異なるサイト構造への対応

サイトによってはHTMLの構造が異なるため、記事コンテンツの抽出方法をカスタマイズする必要がある場合があります。`extract_content()`メソッドを編集して、対象サイトに合わせたセレクターを設定してください。

```python
def extract_content(self, soup):
    """記事の本文コンテンツを抽出する（サイト構造に合わせてカスタマイズ）"""
    if soup is None:
        return None
        
    # サイト固有のセレクターを追加
    if 'example.com' in self.base_url:
        # example.comサイト向けのセレクター
        article = soup.select_one('.article-content, .post-body')
    else:
        # デフォルトのセレクター
        article = soup.select_one('article, .entry-content, .post-content, main')
    
    # 以下は共通処理...
```

### サイトマップ処理のカスタマイズ

特殊なサイトマップ構造を持つサイトの場合は、`get_sitemap_links()`メソッドをカスタマイズして、そのサイト特有のパターンを追加できます。

```python
def get_sitemap_links(self):
    # サイト固有の処理を追加
    if 'mysite.com' in self.base_url:
        # mysiteの特殊なサイトマップパターン
        sitemap_candidates = [
            urljoin(self.base_url, "custom-sitemap.xml"),
            urljoin(self.base_url, "articles/index.xml"),
        ]
        # 以下処理を続ける...
```

## パフォーマンスの最適化

### 処理速度の向上

1. **XMLサイトマップの直接指定**:
   - `--sitemap`オプションでXMLサイトマップを直接指定すると、HTMLページからのリンク抽出処理をスキップできるため、処理が高速化されます
   - 例: `python scraper_complete.py --url https://example.com/ --sitemap https://example.com/post-sitemap.xml`

2. **最大ページ数の制限**:
   - テスト目的や部分的な抽出の場合は、`--max-pages`オプションで取得するページ数を制限すると良いでしょう
   - 例: `python scraper_complete.py --url https://example.com/ --max-pages 10`

3. **遅延時間の調整**:
   - サイトによっては、短い遅延時間でも問題なく処理できる場合があります。安定性を確認しながら`--delay`の値を調整してください
   - 例: `python scraper_complete.py --url https://example.com/ --delay 0.5`

### メモリ使用量の最適化

多数の記事をスクレイピングする場合、メモリ使用量が増大する可能性があります。以下の対策が有効です：

1. **逐次処理**:
   - 大量の記事を処理する場合は、一度に少数の記事だけを処理する複数回の実行に分割することを検討してください
   - 例: `--max-pages 100`を指定して複数回実行

2. **既存ファイルのスキップ**:
   - スクリプトは既に保存されたファイルを自動的にスキップするため、途中で中断しても再開できます

## よくある質問

### Q: 特定のURLのみをスクレイピングするには？
A: `--sitemap`オプションで特定のサイトマップを指定し、`--max-pages`オプションで取得するページ数を制限してください。

### Q: スクレイピングが途中で止まる場合は？
A: `--delay`オプションの値を大きくして（例：3秒以上）、サーバーへの負荷を減らしてみてください。

### Q: 記事の本文が正しく抽出されない場合は？
A: サイトの構造に合わせて`extract_content()`メソッドのセレクターを調整する必要があります。サイトのHTMLを確認して、記事コンテンツを含む要素の適切なセレクターを特定してください。

### Q: WordPressサイトのXMLサイトマップが見つからない場合は？
A: WordPressサイトでもプラグインや設定によってはサイトマップのURLが異なる場合があります。サイトのフッターやrobots.txtを確認して、正確なサイトマップのURLを特定し、`--sitemap`オプションで指定してください。

### Q: 処理速度を上げるには？
A: XMLサイトマップが利用可能な場合は、それを直接指定することで、カテゴリページやページネーションをたどる必要がなくなり、処理速度が大幅に向上します。

### Q: robots.txtを尊重するようにスクリプトを変更するには？
A: スクリプトを拡張して`robotparser`モジュールを使用することで、robots.txtの規則に従ったスクレイピングを実装できます。

### Q: 画像も保存するには？
A: 現在のスクリプトはテキストコンテンツのみを保存していますが、`html2text`の設定を変更し（`ignore_images=False`）、画像のダウンロード処理を追加することで対応可能です。

## 高度な使用法

### 複数サイトの一括処理

複数のサイトを処理する場合は、シェルスクリプトやバッチファイルを使用して自動化できます：

```bash
#!/bin/bash
# sites.sh - 複数サイトの処理

# WordPressサイト
python scraper_complete.py --url https://site1.com/ --wordpress --output-dir site1_articles

# 通常サイト
python scraper_complete.py --url https://site2.com/ --output-dir site2_articles

# 特定のサイトマップを持つサイト
python scraper_complete.py --url https://site3.com/ --sitemap https://site3.com/custom-sitemap.xml --output-dir site3_articles
```

### 定期的な更新

crontabなどを使用して定期的にスクリプトを実行することで、サイトの新しい記事を自動的に取得できます：

```
# 毎日午前2時に実行
0 2 * * * /path/to/scraper_script.sh
```

これにより、既存の記事はスキップされ、新しい記事のみが追加されます。 サイトマップ処理のカスタマイズ

特殊なサイトマップ構造を持つサイトの場合は、`get_sitemap_links()`メソッドをカスタマイズして、そのサイト特有のパターンを追加できます。

## よくある質問

### Q: 特定のURLのみをスクレイピングするには？
A: `--sitemap`オプションで特定のサイトマップを指定し、`--max-pages`オプションで取得するページ数を制限してください。

### Q: スクレイピングが途中で止まる場合は？
A: `--delay`オプションの値を大きくして（例：3秒以上）、サーバーへの負荷を減らしてみてください。

### Q: 記事の本文が正しく抽出されない場合は？
A: サイトの構造に合わせて`extract_content()`メソッドのセレクターを調整する必要があります。サイトのHTMLを確認して、記事コンテンツを含む要素の適切なセレクターを特定してください。ページのURL（省略可能）
```

## サイトマップ形式のサポート

このツールは以下のサイトマップ形式をサポートしています：

1. **XMLサイトマップ**: 標準的なXML形式のサイトマップ（sitemap.xml）
2. **XMLサイトマップインデックス**: 複数のサイトマップを含むインデックスファイル
3. **HTMLサイトマップ**: HTML形式のサイトマップページ（take1bit.comなど）

スクリプトは自動的にサイトマップの形式を判別し、適切に処理します。

## 制限と注意点

1. **take1bit.com固有の設定**：
   - このスクリプトは`take1bit.com`向けに特別な処理（サイトマップURLなど）を含んでいます
   - 他のサイトでは、それぞれのサイト構造に合わせた調整が必要な場合があります

2. **サイト構造依存性**：
   - 記事コンテンツの抽出はHTMLセレクターを使用しているため、サイト構造が変わると調整が必要です
   - 特に以下の関数は調整が必要な場合があります：
     - `extract_content()`：記事本文の抽出
     - `extract_date()`：公開日付の抽出

3. **稼働確認済みサイト**：
   - take1bit.com
   - 標準的なXMLサイトマップを持つサイト

## トラブルシューティング

### 記事が抽出されない場合

1. **サイトマップURLの確認**：
   - 各サイトのサイトマップページURLが正しいか確認してください
   - take1bit.comの場合は自動的に `https://take1bit.com/page-448/` を使用します
   - 標準的なサイトでは `sitemap.xml` を使用します

2. **ネットワーク接続の確認**：
   - サイトにアクセスできるか確認してください
   - DNSエラーが発生する場合は、ドメイン名が正しいか確認してください

3. **セレクターの調整**：
   - スクレイピング対象のサイトが記事をどのようなHTML構造で提供しているか調査し、
     必要に応じて`extract_content()`メソッドのセレクターを調整してください

4. **XMLサイトマップの検証**：
   - 対象サイトのXMLサイトマップが標準形式に準拠しているか確認してください
   - 非標準の場合は`--sitemap`オプションで正確なURLを指定してください

## 使用例詳細

### 特定数の記事のみを取得

```bash
python scraper.py --url https://take1bit.com/ --max-pages 10
```

### 特定のディレクトリに保存

```bash
python scraper.py --url https://take1bit.com/ --output-dir my_articles
```

### サーバー負荷に配慮した設定

```bash
python scraper.py --url https://take1bit.com/ --delay 3
```

### 独自のサイトマップURLを指定

```bash
python scraper.py --url https://example.com/ --sitemap https://example.com/my-sitemap.xml
```
