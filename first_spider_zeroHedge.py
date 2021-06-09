import scrapy
import datetime

class firstSpider(scrapy.Spider):
   name = 'zeroHedge'
   start_urls = ['https://www.zerohedge.com/']

   def parse(self, response):

       for link in response.css('div.Article_nonStickyContainer__1wgF6 a::attr(href)'):
           yield response.follow(link.get(), callback = self.parse_article)

       next_page = response.css('a.SimplePaginator_next__15okP').attrib['href']

       if next_page is not None:
           yield response.follow(next_page, callback = self.parse)

   def parse_article(self, response):

       article = response.css('article.ArticleFull_container__2-yXg')

       for articles in article:
           yield{
               'Title': article.css('h1.ArticleFull_title__2cUI6::text').get(),
               'Author': article.css('div.ArticleFull_headerFooter__author__2Ch4r::text').get(), 
               'Date Creted': article.css('div.ArticleFull_headerFooter__date__3T7FN::text').get(), 
               'Body Text': response.xpath("//div[@class='NodeContent_body__2clki NodeBody_container__1M6aJ']/p/text()").getall()
           }

