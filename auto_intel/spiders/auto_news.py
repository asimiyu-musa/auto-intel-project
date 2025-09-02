import scrapy
import dateparser
from datetime import datetime
from auto_intel.items import ArticleItem

class AutoNewsSpider(scrapy.Spider):
    name = "auto_news"
    allowed_domains = ["carmagazine.co.uk", "pistonheads.com", "autoexpress.co.uk"]

    # start_requests method remains the same...
    def start_requests(self):
        # Car Magazine - 20 pages
        for page in range(1, 21):
            url = "https://www.carmagazine.co.uk/car-news/" if page == 1 else f"https://www.carmagazine.co.uk/car-news/?page={page}"
            yield scrapy.Request(url=url, callback=self.parse)

        # PistonHeads - 15 pages (they are JS heavy, so only root + pages if applicable)
        yield scrapy.Request(url="https://www.pistonheads.com/news", callback=self.parse)

        # AutoExpress - 20 pages each for car-news and consumer-issues
        autoexpress_paths = [
            "https://www.autoexpress.co.uk/car-news",
            "https://www.autoexpress.co.uk/consumer-issues"
        ]
        for base in autoexpress_paths:
            for page in range(1, 5):
                url = base if page == 1 else f"{base}?page={page}"
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        domain = response.url.split('/')[2]
        if "carmagazine.co.uk" in domain:
            yield from self.parse_carmagazine(response)
        elif "pistonheads.com" in domain:
            yield from self.parse_pistonheads(response)
        elif "autoexpress.co.uk" in domain:
            yield from self.parse_autoexpress(response)

    def parse_carmagazine(self, response):
        articles = response.css("article.panel")
        for article in articles:
            link = response.urljoin(article.css("h3.title a::attr(href)").get())
            raw_date = article.css("span.date::text").get(default="").strip()
            parsed_date = dateparser.parse(raw_date)

            item = ArticleItem(
                title=article.css("h3.title a::text").get(),
                link=link,
                author=article.css("span.author::text").get(default="").strip(),
                publication_date=parsed_date.date() if parsed_date else None, # FIXED
                source="Car Magazine UK"
            )
            yield item

    def parse_pistonheads(self, response):
        articles = response.css("a[data-gtm-event-action='click-article']")
        for article in articles:
            url = article.attrib.get("href")
            if url:
                full_url = response.urljoin(url)
                yield scrapy.Request(url=full_url, callback=self.parse_pistonheads_article)

    def parse_pistonheads_article(self, response):
        date_text = response.xpath("//p/text()[contains(., '202')]").get()
        parsed_date = dateparser.parse(date_text.strip()) if date_text else None
        
        yield ArticleItem(
            title=response.css("h1::text").get(default="").strip(),
            link=response.url,
            source="PistonHeads",
            author=response.css("a[data-gtm-event-action='author name click']::text").get(default="PistonHeads Staff").strip(),
            publication_date=parsed_date.date() if parsed_date else None # FIXED
        )

    def parse_autoexpress(self, response):
        articles = response.css("a.polaris__link.polaris__article-card--link")
        for article in articles:
            title = article.css("::text").get()
            link = article.attrib.get("href")
            full_url = response.urljoin(link) if link else None
            
            # The full date and author are often on the article page itself
            yield response.follow(full_url, callback=self.parse_autoexpress_article, meta={'title': title})

    def parse_autoexpress_article(self, response):
        # Get the full date from the article page for better accuracy
        date_text = response.css("span.polaris__date::text").get()
        pub_date = None
        if date_text:
            try:
                pub_date = datetime.strptime(date_text.strip().title(), "%d %b %Y").date() # FIXED
            except ValueError:
                pass
        
        authors = response.css("span.polaris__post-meta--author-name a::text").getall()

        yield ArticleItem(
            title=response.meta.get('title', '').strip(),
            link=response.url,
            author=", ".join(a.strip() for a in authors) if authors else "AutoExpress Staff",
            publication_date=pub_date,
            source="Auto Express"
        )