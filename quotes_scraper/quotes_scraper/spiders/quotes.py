import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('span small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

            author_link = quote.css('span a[href*="/author/"]::attr(href)').get()
            if author_link:
                yield response.follow(author_link, callback=self.parse_author)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_author(self, response):
        description = response.css('div.author-description::text').get()
        if description:
            description = description.replace('\n', ' ').strip()

        yield {
            'author_name': response.css('h3.author-title::text').get(),
            'born': response.css('span.author-born-date::text').get(),
            'born_location': response.css('span.author-born-location::text').get(),
            'description': description
        }