import scrapy
from Final.items import FinalItem
import re

class FinalSpider(scrapy.Spider):
    name = 'final'
    allowed_domains = ['finance.yahoo.com']
    start_urls = ['https://finance.yahoo.com/gainers?offset=0&count=100']

    def parse(self, response):

        # obtain the number of the stocks
        num_str = str(response.xpath("//span[@class='Mstart(15px) Fw(500) Fz(s)']/span/text()").extract_first())
        page = {}
        page["total_num"] = int(re.search(r"of (\d*) results", num_str).group(1))
        page["current_end_num"] = int(re.search(r"^(\d*)-(\d*)", num_str).group(2))

        # start to process the detailed information
        tr_list = response.xpath("//tr[contains(@class,'simpTblRow')]")

        for tr in tr_list:
            item = FinalItem()
            item["Code"] = tr.xpath(".//a[@data-test='quoteLink']/text()").extract_first()
            item["Name"] = tr.xpath(".//td[@aria-label='Name']/text()").extract_first()
            item["Price"] = float(tr.xpath(".//td[@aria-label='Price (Intraday)']/fin-streamer/@value").extract_first())
            item["Change"] = float(tr.xpath(".//td[@aria-label='Change']/fin-streamer/@value").extract_first())
            item["Percentage"] = float(tr.xpath("//td[@aria-label='% Change']/fin-streamer/@value").extract_first())
            item["Volume"] = float(tr.xpath(".//td[@aria-label='Volume']/fin-streamer/@value").extract_first())
            item["Avg_Vol"] = tr.xpath(".//td[@aria-label='Avg Vol (3 month)']/text()").extract_first()
            item["Market_Cap"] = float(tr.xpath(".//td[@aria-label='Market Cap']/fin-streamer/@value").extract_first())
            if tr.xpath(".//td[@aria-label='PE Ratio (TTM)']/text()").extract_first() is not None:
                item["PE"] = float(re.sub(r",", "",tr.xpath(".//td[@aria-label='PE Ratio (TTM)']/text()").extract_first()))
            else:
                item["PE"] = "N/A"

            yield item

        #next page
        if page["total_num"] != page["current_end_num"]:
            next_url = "https://finance.yahoo.com/gainers?offset={}&count=100".format(page["current_end_num"])
            yield scrapy.Request(
                next_url,
                callback=self.parse,
            )


