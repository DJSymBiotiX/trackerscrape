import requests
from bs4 import BeautifulSoup


class UPSInterface(object):

    def __init__(self, tracking_number):
        self.tracking_number = tracking_number

    def track(self):
        url = self.url()
        result = requests.get(url)
        soup = BeautifulSoup(result.content, 'html5lib')
        return soup.find(id='tt_spStatus').text.strip()

    def url(self):
        base = (
            'http://wwwapps.ups.com/WebTracking/processInputRequest?'
            'TypeOfInquiryNumber=T&InquiryNumber1=%s'
        )
        return base % self.tracking_number
