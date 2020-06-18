import scrapy
from scrapy.crawler import CrawlerProcess
import json,csv

class Pharmeasy(scrapy.Spider):

    name = 'pharmeasy'
    url= 'https://pharmeasy.in/api/otc/getCategoryProducts?categoryId=89&page='
    headers ={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    }
    
     def __init__(self): # Python constructor
         with open('pharmeasy.csv','w') as f:
             f.write('Name,Manufacturer,Availability,Quantity,Price,Images_link\n')
        
        #request pages

    def start_requests(self):
        for page in range(0,24):
           
          
            yield scrapy.Request(url = self.url + str(page), headers=self.headers, callback=self.parse)

      #extraction logic
    def parse(self,response):
        data =response.text   #Loading response from API
        data =json.loads(data)
        for product in data['data']['products']:
            items = {
                'Name'        : product['name'],
                'Manufacturer': product['manufacturer'],
                'Availability': product['productAvailabilityFlags']['isAvailable'],
                'Quantity'    : product['maxQuantity'],
                'Price'       : product['mrpDecimal'],
                'Images_link' : product['images']
                }
            with open('pharmeasy.csv','a') as f:
                writer=csv.DictWriter(f , fieldnames=items.keys())
                writer.writerow(items)
            
       
process = CrawlerProcess()
process.crawl(Pharmeasy)
process.start()

