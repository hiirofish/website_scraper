#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import time
import os
import json
import argparse
import xml.etree.ElementTree as ET
from urllib.parse import urljoin, urlparse
from pathlib import Path
import html2text

class WebsiteScraper:
    def __init__(self, base_url, output_dir="scraped_articles", delay=1, sitemap_url=None, try_wordpress_sitemaps=False):
        self.base_url = base_url
        self.visited_urls = set()
        self.all_pages = []
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}
        self.output_dir = Path(output_dir)
        self.delay = delay
        self.sitemap_url = sitemap_url
        self.try_wordpress_sitemaps = try_wordpress_sitemaps
        
        # html2textコンバーターの設定
        self.h2t = html2text.HTML2Text()
        self.h2t.ignore_links = False
        self.h2t.ignore_images = True
        self.h2t.body_width = 0  # 自動折り返しなし
        self.h2t.unicode_snob = True  # Unicode文字を保持
        self.h2t.bypass_tables = False  # テーブルを保持
        self.h2t.mark_code = True  # コードブロックをマークダウン形式で保持
        
    def get_soup(self, url):
        """URLからHTMLを取得してBeautifulSoupオブジェクトを返す"""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # エラーチェック
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def extract_content(self, soup):
        """記事の本文コンテンツを抽出する"""
        if soup is None:
            return None
            
        # ヘッダー、フッター、サイドバー、広告などの不要要素を削除
        for elem in soup.select('header, footer, nav, aside, .sidebar, .advertisement, script, style, .widget, .wp-block-social-links'):
            if elem:
                elem.decompose()
        
        # 記事の本文を取得（サイトの構造によって調整が必要）
        article = soup.select_one('article, .entry-content, .post-content, main')
        
        if not article:
            # 記事要素が見つからない場合はmain要素を探す
            article = soup.select_one('main, .main, #main, #content')
            
        if not article:
            # それでも見つからない場合はbody要素を使用
            article = soup.body
            
        return article
    
    def html_to_markdown(self, html_content):
        """HTMLコンテンツをMarkdownに変換する"""
        if html_content is None:
            return ""
        
        # BeautifulSoupオブジェクトをHTML文字列に変換
        if isinstance(html_content, BeautifulSoup) or hasattr(html_content, 'prettify'):
            html_string = str(html_content)
        else:
            html_string = str(html_content)
            
        # html2textを使ってMarkdownに変換
        return self.h2t.handle(html_string)
    
    def extract_links(self, soup, current_url):
        """ページ内のリンクを抽出する"""
        if soup is None:
            return []
            
        links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            # 相対URLを絶対URLに変換
            absolute_url = urljoin(current_url, href)
            
            # 同じドメイン内のURLのみを収集
            if self.base_url in absolute_url and '#' not in absolute_url:
                links.append(absolute_url)
                
        return links
    
    def sanitize_filename(self, title):
        """ファイル名に使用できない文字を置換する"""
        # 無効な文字を削除または置換
        filename = re.sub(r'[\\/*?:"<>|]', "", title)
        # スペースをアンダースコアに置換
        filename = filename.replace(' ', '_')
        # 長すぎる場合は切り詰める
        if len(filename) > 100:
            filename = filename[:100]
        return filename
    
    def save_to_markdown(self, page):
        """ページ情報をMarkdownファイルとして保存する"""
        # 出力ディレクトリが存在しない場合は作成
        if not self.output_dir.exists():
            self.output_dir.mkdir(parents=True)
            
        title = page.get('title', 'No Title')
        url = page.get('url', '')
        content = page.get('content', '')
        date = page.get('date', '')
        
        # URLからスラッグを抽出してファイル名に使用
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.strip('/').split('/')
        slug = path_parts[-1] if path_parts else 'index'
        
        # ファイル名を生成（スラッグがない場合はタイトルを使用）
        if slug == 'index' or not slug:
            filename = self.sanitize_filename(title)
        else:
            filename = self.sanitize_filename(slug)
            
        filepath = self.output_dir / f"{filename}.md"
        
        # ファイルに書き込む
        with open(filepath, 'w', encoding='utf-8') as f:
            # メタデータ部分を書き込み
            f.write(f"---\n")
            f.write(f"title: {title}\n")
            f.write(f"url: {url}\n")
            if date:
                f.write(f"date: {date}\n")
            f.write(f"---\n\n")
            
            # 本文を書き込み
            f.write(content)
            
        return filepath
    
    def extract_date(self, soup):
        """記事の公開日を抽出する"""
        if soup is None:
            return ""
            
        # まずmetaタグから日付を探す
        meta_date = soup.select_one('meta[property="article:published_time"]')
        if meta_date and meta_date.get('content'):
            return meta_date['content'].split('T')[0]  # ISOフォーマットの日付部分のみ
            
        # time要素から日付を探す
        time_elem = soup.select_one('time')
        if time_elem and time_elem.get('datetime'):
            return time_elem['datetime'].split('T')[0]
            
        # 日付らしきクラス名を持つ要素を探す
        date_classes = ['date', 'published', 'post-date', 'entry-date']
        for cls in date_classes:
            date_elem = soup.select_one(f'.{cls}')
            if date_elem:
                return date_elem.text.strip()
                
        return ""
    
    def process_page(self, url):
        """指定されたURLのページを処理する"""
        if url in self.visited_urls:
            return
            
        print(f"Processing: {url}")
        self.visited_urls.add(url)
        
        soup = self.get_soup(url)
        if soup:
            # タイトルを取得
            title = soup.title.string if soup.title else "No Title"
            # 日付を抽出
            date = self.extract_date(soup)
            # 本文コンテンツを抽出
            article_content = self.extract_content(soup)
            # HTMLをMarkdownに変換
            markdown_content = self.html_to_markdown(article_content)
            
            page_info = {
                'url': url,
                'title': title,
                'date': date,
                'content': markdown_content
            }
            
            self.all_pages.append(page_info)
            return page_info
        
        return None
        
    def parse_xml_sitemap(self, sitemap_url, xml_content):
        """XMLサイトマップを解析してURLのリストを返す"""
        all_urls = []
        
        try:
            # XMLをパース
            root = ET.fromstring(xml_content)
            
            # 名前空間を取得
            ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            
            # サイトマップインデックスかどうかを確認
            if root.tag.endswith('sitemapindex'):
                print("サイトマップインデックスを検出しました。含まれるサイトマップを処理します。")
                # サイトマップインデックスの場合、各サイトマップを処理
                for sitemap in root.findall('.//sm:sitemap', ns):
                    loc = sitemap.find('sm:loc', ns)
                    if loc is not None and loc.text:
                        print(f"サブサイトマップを処理: {loc.text}")
                        try:
                            sub_response = requests.get(loc.text, headers=self.headers)
                            sub_urls = self.parse_xml_sitemap(loc.text, sub_response.content)
                            all_urls.extend(sub_urls)
                            time.sleep(self.delay)  # サーバー負荷軽減
                        except Exception as e:
                            print(f"サブサイトマップの処理中にエラー: {e}")
            else:
                # 通常のサイトマップの場合、各URLを処理
                for url in root.findall('.//sm:url', ns):
                    loc = url.find('sm:loc', ns)
                    if loc is not None and loc.text:
                        if self.base_url in loc.text:
                            all_urls.append(loc.text)
                
                print(f"XMLサイトマップから {len(all_urls)} 個のURLを抽出しました")
        
        except ET.ParseError as e:
            print(f"XMLの解析エラー: {e}、HTMLサイトマップとして処理を試みます")
            soup = self.get_soup(sitemap_url)
            if soup:
                # HTMLサイトマップとして処理
                html_urls = self.parse_html_sitemap(soup, sitemap_url)
                return html_urls
        
        return all_urls
        
    def parse_html_sitemap(self, soup, current_url):
        """HTMLサイトマップを解析してリンクを抽出する"""
        # サイトマップから直接リンクを取得
        links = self.extract_links(soup, current_url)
        
        # カテゴリーページのリンクを分離
        category_links = [link for link in links if 'category' in link]
        # 記事ページのリンクを分離（カテゴリではなく、ページネーションでもない）
        article_links = [link for link in links if 'category' not in link and '/page-' not in link and '/page/' not in link]
        
        # 各カテゴリーページから記事リンクを取得
        all_article_links = set(article_links)
        for cat_link in category_links:
            print(f"カテゴリーページから記事リンクを取得中: {cat_link}")
            cat_soup = self.get_soup(cat_link)
            if cat_soup:
                # カテゴリページ内の全リンクを取得
                cat_links = self.extract_links(cat_soup, cat_link)
                # カテゴリページ内のページネーションリンクを取得
                pagination_links = [link for link in cat_links if '/page/' in link]
                
                # 現在のカテゴリページから記事リンクを抽出
                cat_article_links = [link for link in cat_links 
                                    if 'category' not in link 
                                    and '/page/' not in link 
                                    and link not in all_article_links
                                    and self.base_url in link]
                all_article_links.update(cat_article_links)
                
                # ページネーションをたどって記事を取得
                for page_link in pagination_links:
                    print(f"ページネーションをたどっています: {page_link}")
                    page_soup = self.get_soup(page_link)
                    if page_soup:
                        page_links = self.extract_links(page_soup, page_link)
                        page_article_links = [link for link in page_links 
                                            if 'category' not in link 
                                            and '/page/' not in link 
                                            and link not in all_article_links
                                            and self.base_url in link]
                        all_article_links.update(page_article_links)
                        time.sleep(self.delay)
                
                time.sleep(self.delay)
        
        # メインページから記事が抽出できなかった場合
        if not all_article_links:
            # 別のアプローチを試す（記事を含む要素を特定）
            # たとえばaタグで特定のCSSクラスを持つものなど
            if soup:
                # 記事リンクのパターンを持つaタグを探す
                article_pattern = rf'{self.base_url}[^/]+/[^/]+/'
                article_a_tags = soup.find_all('a', href=re.compile(article_pattern))
                for a_tag in article_a_tags:
                    if a_tag.get('href'):
                        all_article_links.add(a_tag['href'])
        
        return list(all_article_links)
    
    def get_sitemap_links(self):
        """サイトマップからリンクを取得する"""
        # take1bit.comの場合は特定のページをサイトマップとして扱う
        if 'take1bit.com' in self.base_url and not self.sitemap_url:
            # WordPressのサイトマップパターンを試す
            sitemap_candidates = [
                urljoin(self.base_url, "sitemap.xml"),
                urljoin(self.base_url, "sitemap_index.xml"),
                urljoin(self.base_url, "post-sitemap.xml"),
                urljoin(self.base_url, "page-sitemap.xml"),
                "https://take1bit.com/page-448/"  # 最後にフォールバックとして特定ページを試す
            ]
            
            # 候補となるサイトマップを順番に試す
            for candidate in sitemap_candidates:
                print(f"サイトマップ候補を確認中: {candidate}")
                try:
                    response = requests.get(candidate, headers=self.headers)
                    if response.status_code == 200:
                        sitemap_url = candidate
                        print(f"有効なサイトマップが見つかりました: {sitemap_url}")
                        content_type = response.headers.get('Content-Type', '')
                        if 'xml' in content_type.lower() or sitemap_url.endswith('.xml'):
                            print("XMLサイトマップとして処理します")
                            return self.parse_xml_sitemap(sitemap_url, response.content)
                        else:
                            print("HTMLサイトマップとして処理します")
                            soup = self.get_soup(sitemap_url)
                            if soup:
                                return self.parse_html_sitemap(soup, sitemap_url)
                except Exception as e:
                    print(f"サイトマップ候補の確認中にエラー: {e}")
            
            # フォールバック: 特定ページをHTMLサイトマップとして処理
            print(f"XMLサイトマップが見つからないため、HTMLページをサイトマップとして使用します: {sitemap_candidates[-1]}")
            sitemap_url = sitemap_candidates[-1]
            soup = self.get_soup(sitemap_url)
            if soup:
                return self.parse_html_sitemap(soup, sitemap_url)
            return []
        else:
            # 他のサイトの場合
            sitemap_url = self.sitemap_url
            
            # サイトマップURLが指定されていない場合はWordPressの一般的なパターンを試す
            if not sitemap_url:
                sitemap_candidates = [
                    urljoin(self.base_url, "sitemap.xml"),
                    urljoin(self.base_url, "sitemap_index.xml"),
                    urljoin(self.base_url, "post-sitemap.xml"),
                ]
                
                for candidate in sitemap_candidates:
                    print(f"サイトマップ候補を確認中: {candidate}")
                    try:
                        response = requests.get(candidate, headers=self.headers)
                        if response.status_code == 200:
                            sitemap_url = candidate
                            print(f"有効なサイトマップが見つかりました: {sitemap_url}")
                            break
                    except Exception as e:
                        print(f"サイトマップ候補の確認中にエラー: {e}")
            
            # サイトマップが見つからなかった場合
            if not sitemap_url:
                print("有効なサイトマップが見つかりませんでした。デフォルトのURLを使用します。")
                sitemap_url = urljoin(self.base_url, "sitemap.xml")
            
            print(f"サイトマップから取得中: {sitemap_url}")
            
            try:
                response = requests.get(sitemap_url, headers=self.headers)
                content_type = response.headers.get('Content-Type', '')
                
                # XMLサイトマップの場合（content-typeにxmlが含まれている場合）
                if 'xml' in content_type.lower() or sitemap_url.endswith('.xml'):
                    print("XMLサイトマップを検出しました。XMLとして処理します。")
                    return self.parse_xml_sitemap(sitemap_url, response.content)
            except Exception as e:
                print(f"XMLサイトマップの確認中にエラーが発生しました: {e}")
            
            # HTMLサイトマップとして処理（XMLではない場合）
            soup = self.get_soup(sitemap_url)
            if soup:
                return self.parse_html_sitemap(soup, sitemap_url)
            
            return []

    def run(self, max_pages=None):
        """スクレイピングを実行する"""
        # まずはサイトマップからリンクを取得
        print("サイトマップからリンクを取得中...")
        article_links = self.get_sitemap_links()
        
        # 記事リンクが見つからなかった場合、WordPressの他のサイトマップも試す
        if len(article_links) == 0 and ('wordpress' in self.base_url.lower() or self.try_wordpress_sitemaps):
            print("WordPressサイトマップを確認します...")
            wordpress_sitemaps = [
                urljoin(self.base_url, "post-sitemap.xml"),
                urljoin(self.base_url, "page-sitemap.xml"),
                urljoin(self.base_url, "category-sitemap.xml"),
                urljoin(self.base_url, "tag-sitemap.xml")
            ]
            
            for wp_sitemap in wordpress_sitemaps:
                try:
                    print(f"WordPressサイトマップを確認中: {wp_sitemap}")
                    response = requests.get(wp_sitemap, headers=self.headers)
                    if response.status_code == 200 and ('xml' in response.headers.get('Content-Type', '').lower() or wp_sitemap.endswith('.xml')):
                        wp_links = self.parse_xml_sitemap(wp_sitemap, response.content)
                        if wp_links:
                            print(f"{wp_sitemap}から{len(wp_links)}個のリンクを取得しました")
                            article_links.extend(wp_links)
                except Exception as e:
                    print(f"WordPressサイトマップの確認中にエラー: {e}")
        
        # 重複を除去
        article_links = list(set(article_links))        
        print(f"サイトマップから {len(article_links)} 個の記事リンクを取得しました")
        
        # 取得したリンクを表示（最大10件）
        print("\n取得した記事リンク一覧（一部）:")
        for i, link in enumerate(article_links[:10], 1):
            print(f"{i}. {link}")
        
        # 処理対象のファイルを決定（既に存在するファイルは除外）
        existing_files = set()
        if self.output_dir.exists():
            # 既存のmdファイルからURLを抽出
            for md_file in self.output_dir.glob('*.md'):
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        url_match = re.search(r'url: (https?://[^\n]+)', content)
                        if url_match:
                            existing_files.add(url_match.group(1))
                except Exception as e:
                    print(f"既存ファイル {md_file} の読み込みエラー: {e}")
        
        # 未処理のリンクのみを抽出
        links_to_process = [link for link in article_links if link not in existing_files]
        
        # 最大ページ数の制限がある場合
        if max_pages is not None and max_pages > 0:
            links_to_process = links_to_process[:max_pages]
            
        print(f"\n処理対象: {len(links_to_process)}個の記事（既存の{len(existing_files)}個は除外）")
        
        processed_count = 0
        
        for link in links_to_process:
            page_info = self.process_page(link)
            if page_info:
                # Markdownファイルとして保存
                filepath = self.save_to_markdown(page_info)
                print(f"保存完了: {filepath}")
                processed_count += 1
                
            time.sleep(self.delay)  # サーバー負荷軽減
        
        print(f"\nスクレイピング完了! {processed_count}個の記事を保存しました。")
        print(f"記事ファイルは '{self.output_dir}' ディレクトリに保存されています。")


def main():
    parser = argparse.ArgumentParser(description='ウェブサイトの記事をスクレイピングしてMarkdownに変換')
    parser.add_argument('--url', required=True, help='スクレイピング対象のベースURL')
    parser.add_argument('--output-dir', default='scraped_articles', help='出力先ディレクトリ（デフォルト: scraped_articles）')
    parser.add_argument('--delay', type=float, default=1, help='リクエスト間の遅延秒数（デフォルト: 1）')
    parser.add_argument('--max-pages', type=int, help='最大取得ページ数（デフォルト: 無制限）')
    parser.add_argument('--sitemap', help='サイトマップページのURL（省略可能）')
    parser.add_argument('--wordpress', action='store_true', help='WordPressサイトマップを試行する（デフォルト: False）')
    
    args = parser.parse_args()
    
    scraper = WebsiteScraper(
        base_url=args.url,
        output_dir=args.output_dir, 
        delay=args.delay,
        sitemap_url=args.sitemap,
        try_wordpress_sitemaps=args.wordpress
    )
    
    scraper.run(max_pages=args.max_pages)


if __name__ == "__main__":
    main()