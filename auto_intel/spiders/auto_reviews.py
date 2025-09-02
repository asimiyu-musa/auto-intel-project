import scrapy
import re
from auto_intel.items import CarReviewItem
from datetime import datetime
from w3lib.html import remove_tags


class AutoReviewsSpider(scrapy.Spider):
    name = "auto_reviews"
    allowed_domains = ["autoexpress.co.uk", "carbuyer.co.uk"]
    start_urls = [
        f"https://www.autoexpress.co.uk/car-reviews?page={i}" for i in range(1, 31)
    ] + [
        f"https://www.carbuyer.co.uk/reviews?page={i}" for i in range(1, 31)
    ]

    def parse(self, response):
        article_links = response.css("div.polaris__article-card > a.polaris__link::attr(href)").getall()
        for link in article_links:
            if link and (link.startswith("http") or link.startswith("/")):
                full_url = response.urljoin(link)
                yield response.follow(full_url, callback=self.parse_article)
            else:
                self.logger.info(f"Skipping invalid link: {link}")

    def parse_article(self, response):
        domain = response.url.split('/')[2]
        item = CarReviewItem()
        item['link'] = response.url

        if "autoexpress.co.uk" in domain:
            self.parse_autoexpress_review(response, item)
        elif "carbuyer.co.uk" in domain:
            self.parse_carbuyer_review(response, item)

        yield item

    def parse_autoexpress_review(self, response, item):
        item['title'] = response.css("h1.polaris__heading.-content-title::text, h1.polaris__heading--content-title::text").get()
        item['source'] = "Auto Express"
        item['publication_date'] = self.parse_date(response.css("span.polaris__date::text").get())
        
        authors = response.css("span.polaris__post-meta--author-name a::text").getall()
        item['author'] = ", ".join(a.strip() for a in authors) if authors else None

        verdict_node = response.xpath(
            "//div[contains(@class, 'polaris__simple-grid--main')]//p[preceding-sibling::h2[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'verdict') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'our opinion')]][1]"
        ).get()
        item['verdict'] = remove_tags(verdict_node).strip() if verdict_node else None

        rating_text = response.css("p.polaris__rating--text::text").get()
        rating = None
        if rating_text:
            try:
                rating = float(rating_text.strip())
            except (ValueError, TypeError):
                pass
        item['rating'] = rating
        item['price'] = self.extract_price(response)

        # Fallback logic for data in tables
        if not item.get('rating') or not item.get('price'):
            self.extract_from_table(response, item)

    def parse_carbuyer_review(self, response, item):
        item['title'] = response.css("h1.polaris__heading.-content-title::text").get()
        item['source'] = "Carbuyer"
        item['publication_date'] = self.parse_date(response.css("span.polaris__date::text").get())
        
        authors = response.css("span.polaris__post-meta--author-name a::text").getall()
        item['author'] = ", ".join(a.strip() for a in authors) if authors else None

        verdict_node = response.xpath("//p[strong[contains(text(), 'verdict') or contains(text(), 'Verdict')]]/strong/following-sibling::text()[1]").get()
        item['verdict'] = verdict_node.strip() if verdict_node else None

        rating_text = response.css("p.polaris__rating--text span::text").get()
        rating = None
        if rating_text:
            try:
                rating = float(rating_text.strip())
            except (ValueError, TypeError):
                pass
        item['rating'] = rating
        item['price'] = self.extract_price(response)

    def parse_date(self, text):
        if text:
            try:
                return datetime.strptime(text.strip().title(), "%d %b %Y").date()
            except ValueError:
                return None
        return None

    def extract_price(self, response):
        prices = response.css("span.polaris__price--price::text").getall()
        for price_text in prices:
            match = re.search(r'£([\d,]+)', price_text)
            if match:
                return int(match.group(1).replace(',', ''))
        return None

    # FIXED: The arguments 'response' and 'item' are now in the correct order.
    def extract_from_table(self, response, item):
        """Fallback to extract data from a spec table if primary methods fail."""
        rows = response.css("table.tablesaw tbody tr")
        for row in rows:
            header = (row.css("td:nth-child(1)::text").get() or "").strip().lower()
            value = (row.css("td:nth-child(2)::text").get() or "").strip()

            if not header or not value:
                continue
            
            if "rating" in header and not item.get('rating'):
                match = re.search(r"(\d+(\.\d+)?)", value)
                if match:
                    item['rating'] = float(match.group(1))

            if "price new" in header and not item.get('price'):
                match = re.search(r'£([\d,]+)', value)
                if match:
                    item['price'] = int(match.group(1).replace(',', ''))