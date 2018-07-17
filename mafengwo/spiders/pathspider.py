import scrapy
import re
import bs4
import json


class PathSpider(scrapy.Spider):
    name = "path"

    start_urls = [
        "http://www.mafengwo.cn/u/76342360.html",
    ]

    def parse_dest_html(self, response):
        html = bs4.BeautifulSoup(response, "html5lib")
        res = []
        mddid = 0
        for dest in html.find_all("div", class_="_j_cityitem"):
            mddid = dest['data-mddid']
            if "待完善" in dest.prettify():
                res.append({
                    "city":
                    dest.find(
                        "div",
                        class_="vertical").find("p").get_text(strip=True)[:-3],
                    "city_poi": []
                })
            else:
                city = dest.find("h3").find("span").get_text()
                dests = []
                for poi in dest.find_all("h4"):
                    dests = poi.get_text(strip=True)
                res.append({
                    "city": city,
                    "city_poi": dests,
                })
        return (res, mddid)

    def parse_dests(self, response):
        this = response.meta['partial_res']
        uid = response.meta['uid']
        response_html = json.loads(response.body_as_unicode())['data']['html']
        if response_html == "":
            yield {"uid": uid, "footpath": this}
        else:
            this_res, last_mddid = self.parse_dest_html(response_html)
            this = [*this, *this_res]
            yield scrapy.Request(
                "http://www.mafengwo.cn/path/ajax_userindex.php?act=getCountryCityList&mddid=0&sub_mddid=0&lastmddid={}&uid={}".
                format(last_mddid, uid),
                callback=self.parse_dests,
                meta={
                    "uid": uid,
                    "partial_res": this
                })

    def parse(self, response):
        follows = response.xpath(
            "//ul[@class='clearfix _j_followlist']/li/a/@href").extract()
        for follow in follows:
            uid = re.search(r"/u/(\d+).html", follow).group(1)
            yield scrapy.Request(
                "http://www.mafengwo.cn/path/ajax_userindex.php?act=getCountryCityList&mddid=0&sub_mddid=0&lastmddid=0&uid={}".
                format(uid),
                callback=self.parse_dests,
                meta={
                    "uid": uid,
                    "partial_res": []
                })
            yield response.follow(
                "http://www.mafengwo.cn/u/{}.html".format(uid))
