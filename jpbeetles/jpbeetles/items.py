# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JpbeetlesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    family = scrapy.Field()
    subfamily = scrapy.Field()
    tribe = scrapy.Field()
    subtribe = scrapy.Field()
    genus = scrapy.Field()
    subgenus = scrapy.Field()
    species = scrapy.Field()
    subspecies = scrapy.Field()
    scientific_name_author = scrapy.Field()
    name_publishedin_year = scrapy.Field()
    japanese_name = scrapy.Field()
    distribution = scrapy.Field()
    note = scrapy.Field()
