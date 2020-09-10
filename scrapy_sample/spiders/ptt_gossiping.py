import scrapy
from ..items import PostItem
from datetime import datetime


class PttGossipingSpider(scrapy.Spider):
    name = 'ptt_gossiping'
    allowed_domains = ['www.ptt.cc/bbs/Gossiping']
    start_urls = ['http://www.ptt.cc/bbs/Gossiping']

    max_page = 10
    page_count = 0

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'yes': 'yes'},
            callback=self.after_ask,
            dont_filter=True
        )

    def after_ask(self, response):
        for href in response.css('div.r-ent div.title a::attr(href)').getall():
            url = response.urljoin(href)
            yield scrapy.Request(url=url, callback=self.parse_post, dont_filter=True)

        if self.page_count < self.max_page:
            next = response.xpath(
                '//div[@id="action-bar-container"]//a[contains(text(), "上頁")]/@href').get(default=None)
            if next:
                self.page_count += 1
                url = response.urljoin(next)
                yield scrapy.Request(url=url, callback=self.after_ask, dont_filter=True)

    def parse_post(self, response):
        item = PostItem()
        item['title'] = response.css('meta[property="og:title"]::attr(content)').get()
        item['author'] = response.xpath(
            '//div[@class="article-metaline"]/span[text()="作者"]/following-sibling::span[1]/text()').get().split(' ')[0]

        datetime_str = response.xpath(
            '//div[@class="article-metaline"]/span[text()="時間"]/following-sibling::span[1]/text()').get()
        item['date'] = datetime.strptime(datetime_str, '%a %b %d %H:%M:%S %Y')
        item['content'] = response.css('div#main-content::text').get()
        comments = []
        score_total = 0

        for comment in response.css('div.push'):
            tag = comment.css('span.push-tag::text').get()
            user = comment.css('span.push-userid::text').get()
            content = comment.css('span.push-content::text').get()

            if '推' in tag:
                score = 1
            elif '噓' in tag:
                score = -1
            else:
                score = 0

            score_total += score

            comments.append({
                'user': user,
                'score': score,
                'content': content
            })

        item['comments'] = comments
        item['score'] = score_total
        item['url'] = response.url

        yield item