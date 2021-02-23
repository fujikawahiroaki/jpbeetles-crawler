import scrapy


class JpbeetlesItem(scrapy.Item):
    kingdom = scrapy.Field()
    phylum = scrapy.Field()
    class_name = scrapy.Field()
    order = scrapy.Field()
    suborder = scrapy.Field()
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
