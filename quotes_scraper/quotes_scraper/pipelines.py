# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


import json

class QuotesPipeline:
    def open_spider(self, spider):
        self.file = open('quotes.json', 'w', encoding='utf-8')
        self.quotes = []

    def close_spider(self, spider):
        self.file.write(json.dumps(self.quotes, ensure_ascii=False, indent=4))
        self.file.close()

    def process_item(self, item, spider):
        if 'text' in item:
            quotes_data = {
                'tags': item['tags'],
                'author': item['author'],
                'quote': item['text'],
            }
            self.quotes.append(quotes_data)
        return item


class AuthorsPipeline:
    def open_spider(self, spider):
        self.file = open('authors.json', 'w', encoding='utf-8')
        self.authors = []

    def close_spider(self, spider):
        self.file.write(json.dumps(self.authors, ensure_ascii=False, indent=4))
        self.file.close()

    def process_item(self, item, spider):
        if 'author_name' in item:
            author_data = {
                'fullname': item['author_name'],
                'born_date': item['born'],
                'born_location': item['born_location'],
                'description': item['description']
            }
            self.authors.append(author_data)
        return item
