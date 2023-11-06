# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class IndeedItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    keyword = Field()
    location = Field()
    page = Field()
    position = Field()
    company = Field()
    companyRating = Field()
    companyReviewCount = Field()
    highlyRatedEmployer = Field()
    jobkey = Field()
    jobTitle = Field()
    jobLocationCity = Field()
    jobLocationPostal = Field()
    jobLocationState = Field()
    maxSalary = Field()
    minSalary = Field()
    salaryType = Field()
    pubDate = Field()
    salaryText = Field()
    urgentlyHiring = Field()
    jobDescription = Field()
    jobUrl = Field()
    
    pass
