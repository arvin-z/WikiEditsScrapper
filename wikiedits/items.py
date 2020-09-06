# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import re

import scrapy
from scrapy.item import Item, Field
from itemloaders.processors import MapCompose, TakeFirst


def str_to_int(text):
    try:
        return int(float(text))
    except ValueError:
        return text


def str_to_tup(text):
    return tuple(text.split(' '))


def punctuation_strip(text):
    regex = re.compile('[,.!?]')
    return regex.sub('', text).strip()




class WikiEditItem(Item):
    ip_addr = Field(
        output_processor=TakeFirst()
    )
    tags = Field()
    change = Field(
        input_processor=MapCompose(str_to_int),
        output_processor=TakeFirst()
    )
    new_words = Field(
        input_processor=MapCompose(punctuation_strip, str_to_tup),
        output_processor=TakeFirst()
    )


class WikieditsItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass
