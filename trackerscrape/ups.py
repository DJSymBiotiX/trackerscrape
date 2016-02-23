import requests
import lxml.html

from .useragent import get_random_useragent


class UPSInterface(object):

    def __init__(self, tracking_number):
        self.tracking_number = tracking_number

    def track(self):
        url = self.url()
        headers = {
            'User-Agent': get_random_useragent()
        }
        result = requests.get(url, headers=headers)
        doc = lxml.html.fromstring(result.text)

        status = doc.get_element_by_id('tt_spStatus').text_content().strip()

        texts = {}
        # Compile all the text from every <dl> with a single <dt> and <dd> into
        # a dict
        for dl in doc.findall('.//dl'):
            dts = dl.findall('./dt')
            dds = dl.findall('./dd')

            if len(dts) == 1 and len (dds) == 1:
                dt = dts[0].text_content().strip()
                dd = dds[0].text_content().strip()
                texts[dt] = ' '.join(dd.split())

        scheduled_delivery = texts['Scheduled Delivery:']
        last_location = texts['Last Location:']

        return {
            'status': status,
            'scheduled_delivery': scheduled_delivery,
            'last_location': last_location
        }

    def url(self):
        base = (
            'http://wwwapps.ups.com/WebTracking/processInputRequest?'
            'TypeOfInquiryNumber=T&InquiryNumber1=%s'
        )
        return base % self.tracking_number
