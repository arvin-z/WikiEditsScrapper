import scrapy
from scrapy.loader import ItemLoader
from wikiedits.items import WikiEditItem
import itemadapter


class WikiEditsSpider(scrapy.Spider):
    name = "edits"

    start_urls = ['https://en.wikipedia.org/wiki/Special:RecentChanges?goodfaith=verylikelybad&userExpLevel'
                  '=unregistered&hidebots=1&hidecategorization=1&hideWikibase=1&limit=50&days=7&urlversion=2']

    def parse(self, response, **kwargs):
        self.logger.info('spider started...')
        edits = response.css('li.mw-changeslist-line')
        for edit in edits:
            loader = ItemLoader(item=WikiEditItem(), selector=edit)
            loader.add_css('ip_addr', '.mw-userlink>bdi::text')
            loader.add_css('tags', '.mw-tag-marker::text')
            loader.add_css('change', '.mw-diff-bytes::text')
            edit_item = loader.load_item()

            edit_url = edit.css('.mw-changeslist-diff::attr(href)').get()
            yield response.follow(edit_url, callback=self.parse_edit, meta={'edit_item': edit_item})

            # TODO: scrape multiple pages

    def parse_edit(self, response):
        edit_item = response.meta['edit_item']
        loader = ItemLoader(item=edit_item, response=response)
        loader.add_value('new_words', '')
        loader.add_css('new_words', '.diffchange::text')
        yield loader.load_item()
