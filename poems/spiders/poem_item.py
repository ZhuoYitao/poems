from scrapy import Item, Field

class PoemItem(Item):
    name = Field()
    author = Field()
    content = Field()
    tag = Field()