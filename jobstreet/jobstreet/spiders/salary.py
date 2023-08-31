# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule, Request


import datetime
import lxml.html
import re
import mysql.connector
import json

class JobstreetsearchSpider(scrapy.Spider):
    name                 = 'salary'
    allowed_domains      = ['jobstreet.co.id']
    # start_urls           = ['https://www.jobstreet.co.id/id/job/recruitment-staff-3901778?jobId=jobstreet-id-job-3901778&sectionRank=1&token=0~da10c04b-62dc-4eae-84c6-28d191b0b20a&fr=SRP%20View%20In%20New%20Tab']
    #start_urls           = ['https://www.jobstreet.co.id/id/job/multimedia-staff-3899880?jobId=jobstreet-id-job-3899880&sectionRank=2&token=0~da10c04b-62dc-4eae-84c6-28d191b0b20a&searchPath=%2Fid%2Fjob-search%2Fjob-vacancy.php%3Fpg%3D1&fr=SRP%20View%20In%20New%20Tab']

    start_urls           = ['https://www.jobstreet.co.id/en/job/3965446?JASRC=JCLHPLI&itemIndex=2&correlationName=recommended-jobs&fr=Start%2BState%2BRec&token=1~fc210638-ddc5-4e20-8c69-06ec5553bbb0']

    
    
    def parse(self, response):    
        # ---------------------------------------------------------------------------------- script
            scriptx = response.xpath('//script[2]/text()').extract_first() 

        # ---------------------------------------------------------------------------------- UR
            url = response.meta.get('url') 
            
        # ---------------------------------------------------------------------------------- SITE
            site = 'jobstreet.co.id'
        
             
        # -------------------------------------------------------------- salary_min  
            # minSalary":
            class1 = "sx2jih0 zcydq8p zcydq8v _1xiw5030"
            class2 = "sx2jih0 zcydq897 zcydq8a2 zcydq887 zcydq892"
            class3 = "sx2jih0 zcydq8bm _18qlyvc14 _18qlyvc17 zcydq832 zcydq835"
            class4 = "sx2jih0 zcydq84u zcydq858 zcydq8f6 zcydq8f0 _17fduda2a _17fduda2n"
            class5 = "sx2jih0 zcydq8r zcydq8p _16wtmva0 _16wtmva4"
            class6 = "ssx2jih0 zcydq8a2 zcydq89k zcydq86i zcydq874 zcydq8n zcydq84u zcydq8ei _16wtmva1"
            class7 = "sx2jih0 _17fduda0 _17fduda5"
            class8 = "sx2jih0 zcydq86i"

            path1 = "/div[@class='"+class1+"']"
            path2 = "/div[@class='"+class2+"']"
            path3 = "/div[@class='"+class3+"']"
            path4 = "/div[@class='"+class4+"']"
            path5 = "/div[@class='"+class5+"']"
            path6 = "/div[@class='"+class6+"']"
            path7 = "/div[@class='"+class7+"']"

            end_path = "/text()"

            total_path = "/" + path6 
            pre1 = response.xpath(total_path).get()
            salary_min = pre1  

        # -------------------------------------------------------------- salary_max 
            # maxSalary":
            pre1 = response.xpath("//span[@class='sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _18qlyvca']/text()")[1].extract()
            salary_max = pre1  
 



    # ---------------------------------------------------------------------------------- 
            yield {'salary_min' : salary_min, 'salary_max' : salary_max }
