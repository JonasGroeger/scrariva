import arrow
import scrapy

from scrariva.items import ScrarivaItem


class Ariva(scrapy.Spider):
    name = "Ariva"

    def __init__(self, *args, **kwargs):
        super(Ariva, self).__init__(*args, **kwargs)
        self.url_base = 'http://www.ariva.de'
        self.url_overview = self.url_base + '/{}'
        self.url_hist = self.url_base + '/{}/historische_kurse'
        self.url_download = self.url_base + '/quote/historic/historic.csv?secu={}&boerse_id=12&min_time={}&max_time={}&trenner=%3B&go=Download'
        self.date_format = "DD.MM.YYYY"

    def start_requests(self):
        min_time = getattr(self, "from", None)
        max_time = getattr(self, "to", arrow.now().format(self.date_format))
        isin = getattr(self, 'isin', None)

        if isin is not None:
            self.url_overview = self.url_overview.format(isin)
            self.url_hist = self.url_hist.format(isin)
        else:
            raise TypeError("Please specify an ISIN.")

        item = ScrarivaItem(
            isin=isin,
            min_time=min_time,
            max_time=max_time,
            secu=None,
            csv=None,
        )

        # Get Auflagedatum only if min_time is not specified by user
        if min_time is None:
            request = scrapy.Request(url=self.url_overview, callback=self.parse_auflagedatum)
        else:
            request = scrapy.Request(url=self.url_hist, callback=self.parse_secu)

        request.meta['item'] = item
        return [request]

    def parse_secu(self, response):
        secu = response.xpath("//input[@name = 'secu']/@value").extract_first()

        item = response.meta['item']
        item['secu'] = secu

        self.url_download = self.url_download.format(secu, item['min_time'], item['max_time'])

        return [scrapy.Request(url=self.url_download, callback=self.parse_csv, meta={'item': item})]

    def parse_auflagedatum(self, response):
        auflagedatum_xpath = "//text()[contains(.,'Auflagedatum')]/../../td[2]/text()"
        auflagedatum = arrow.get(response.xpath(auflagedatum_xpath).extract_first(), self.date_format)
        auflagedatum_first = auflagedatum.floor('month').format(self.date_format)

        item = response.meta['item']
        item['min_time'] = auflagedatum_first
        return [scrapy.Request(url=self.url_hist, callback=self.parse_secu, meta={'item': item})]

    def parse_csv(self, response):
        item = response.meta['item']
        csv = response.text

        # Fix CSV
        csv = csv.replace("\\n", "\n")
        csv = "\n".join([l.rstrip() for l in csv.splitlines() if l.strip()])

        item['csv'] = csv
        yield item
