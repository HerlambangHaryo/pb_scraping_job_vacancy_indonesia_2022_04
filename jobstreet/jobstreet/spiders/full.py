# -*- coding: utf-8 -*-
from calendar import c
import scrapy
from scrapy.spiders import CrawlSpider, Rule, Request


import datetime
import lxml.html
import re
import mysql.connector
import json 

class JobstreetsearchSpider(scrapy.Spider):
    name                 = 'jobstreet'
    allowed_domains      = ['jobstreet.co.id'] 
    start_urls           = ['https://www.jobstreet.co.id/id/job-search/job-vacancy.php?ojs=1&pg=1']

    def parse(self, response):    
        page_number = response.meta.get('page_number') or 1         
        
        bodyx = response.xpath('//script[2]').extract_first()  
        bodysplit = bodyx.split('"jobUrl":"')
        stringcount = len(bodysplit)         
        counter = 1
        
        for row in bodysplit:   
            if(counter < stringcount):
                prelink = bodysplit[counter]
                prelink2 = prelink.split('","jobTitleSlug":"')[0]
                url = prelink2.replace('\\u002F', '/')   
                yield {'url': url}
                yield Request(url, callback=self.parse_page,meta={'url': url,'page_number': page_number}) 
                counter+=1
            else:
                break

        if int(page_number) == 1480 :
            page_number = 1480
        elif int(page_number) >= 1 :
            page_number = int(page_number) + 1
            next_page     = "https://www.jobstreet.co.id/id/job-search/job-vacancy.php?ojs=1&pg=" + str(page_number)
            yield Request(next_page, callback=self.parse,meta={'page_number': page_number})
            
    
    def parse_page(self, response):    
        
        # ---------------------------------------------------------------------------------- COL
            datenow = datetime.datetime.now()
            datenow_onlydate = datenow.strftime("%Y_%m") 
            
        # ---------------------------------------------------------------------------------- script
            scriptx = response.xpath('//script[2]/text()').extract_first() 

        # ---------------------------------------------------------------------------------- UR
            url = response.meta.get('url') 
            
        # ---------------------------------------------------------------------------------- SITE
            site = 'jobstreet.co.id'
       
        # ---------------------------------------------------------------------------------- COMPANY  
            # -------------------------------------------------------------- company  
            # company":{"name":"
            pre1 = scriptx.split('company":{"name":"')[1] 
            company = pre1.split('",')[0]  

            # -------------------------------------------------------------- company_size  
            # size":"
            pre1 = scriptx.split('size":"')[1] 
            company_size = pre1.split('",')[0]
            
            # -------------------------------------------------------------- address  
            # nearbyLocations":"
            pre1 = scriptx.split('nearbyLocations":"')[1] 
            address = pre1.split('"},"')[0]

            # -------------------------------------------------------------- city  
            # [{"location":"
            pre1 = scriptx.split('[{"location":"')[1] 
            city = pre1.split('",')[0]  

            # -------------------------------------------------------------- phone
            # telephoneNumber":
            pre1 = scriptx.split('telephoneNumber":')[1] 
            phone = pre1.split(',')[0] 
                
            # -------------------------------------------------------------- website  
            # Website":" 
            pre1 = scriptx.split('Website":')[1] 
            website = pre1.split(',')[0]  
                
            # -------------------------------------------------------------- industry  
            # industryValue":{"value":"
            # ","label":"
            # \u002F
            pre1 = scriptx.split('industryValue":{"value":"')[1] 
            pre2 = pre1.split('","label":"')[1] 
            pre3 = pre2.split('"},"')[0]
            industry = pre3.replace('\\u002F', ' / ')
                
        # ---------------------------------------------------------------------------------- JOB  
            # -------------------------------------------------------------- domain  
            # jobFunctionValue":
            pre1 = scriptx.split('jobFunctionValue":[{"code":')[1] 
            pre2 = pre1.split('}],')[0]  
            pre3 = pre2.replace('\\u002F', ' / ')
            pre4 = pre3.replace(',"name":"', ' ')
            pre5 = pre4.replace('","children":null', ' ')
            domain = pre5.replace('},{"code":', ', ') 

            # -------------------------------------------------------------- title 
            # jobTitle: "
            pre1 = scriptx.split('jobTitle":"')[1] 
            title = pre1.split('",')[0]
                
            # -------------------------------------------------------------- career_level  
            # careerLevel":"
            pre1 = scriptx.split('careerLevel":"')[1] 
            career_level = pre1.split('",')[0] 

            # -------------------------------------------------------------- salary_type
            # SALARY_TYPE":[{"label":"
            pre1 = scriptx.split('SALARY_TYPE":[{"label":"')[1] 
            salary_type = pre1.split('",')[0]  

            # -------------------------------------------------------------- salary_currency  
            # currency":"
            pre1 = scriptx.split('currency":"')[1] 
            salary_currency = pre1.split('",')[0]  

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
                
            # -------------------------------------------------------------- placement  
            pre1 = scriptx.split('[{"location":"')[1] 
            placement = pre1.split('",')[0]  
                
            # -------------------------------------------------------------- employment_type  
            # employmentType":"
            pre1 = scriptx.split('employmentType":"')[1] 
            employment_type = pre1.split('",')[0]   

            # -------------------------------------------------------------- working_hours  
            # employmentType":"
            pre1 = scriptx.split('workingHours":')[1] 
            working_hours = pre1.split(',')[0]   

            # -------------------------------------------------------------- dresscode  
            # dressCode":
            pre1 = scriptx.split('dressCode":')[1] 
            dresscode = pre1.split(',')[0]  

        # ---------------------------------------------------------------------------------- REQUIREMENT 
            # -------------------------------------------------------------- requirement  
            # jobDescription":{"html":"
            pre1 = scriptx.split('jobDescription":{"html":"')[1] 
            pre2 = pre1.split('},')[0]  
            pre3 = pre2.replace('\\u003E', ' ')
            pre4 = pre3.replace('\\u003Cli', ' ')
            pre5 = pre4.replace('\\u003C\\u002Fli ', ', ')
            pre6 = pre5.replace('\\u003Cul', ' ')
            requirement = pre6.replace('\\u003C\\u002Ful', ' ') 

            # -------------------------------------------------------------- qualification 
            # qualification":" 
            pre1 = scriptx.split('qualification":"')[1] 
            qualification = pre1.split('",')[0]  

            # -------------------------------------------------------------- field_of_study  
            # fieldOfStudy
            pre1 = scriptx.split('fieldOfStudy":')[1] 
            field_of_study = pre1.split(',')[0]     

            # -------------------------------------------------------------- gpa_min  
            gpa_min = '' 

            # -------------------------------------------------------------- experience 
            # yearsOfExperience":"
            pre1 = scriptx.split('yearsOfExperience":"')[1] 
            experience = pre1.split('",')[0]  
                
            # -------------------------------------------------------------- generalskill  
            # skills":
            pre1 = scriptx.split('skills":')[1] 
            generalskill = pre1.split(',')[0]   

            # -------------------------------------------------------------- hardskill  
            # skills":
            pre1 = scriptx.split('skills":')[1] 
            hardskill = pre1.split(',')[0]   
                
            # -------------------------------------------------------------- softskill   
            # skills":
            pre1 = scriptx.split('skills":')[1] 
            softskill = pre1.split(',')[0]    
                
            # -------------------------------------------------------------- max_age  
            max_age = '' 
                
            # -------------------------------------------------------------- gender  
            gender = '' 
                
        # ---------------------------------------------------------------------------------- DESCRIPTION 
            # -------------------------------------------------------------- description  
            # companyOverview":{"html":"             
            pre1 = scriptx.split('companyOverview":{"html":"')[1] 
            pre2 = pre1.split('},')[0]  
            pre3 = pre2.replace('\\u003E', ' ')
            pre4 = pre3.replace('\\u003Cli', ' ')
            pre5 = pre4.replace('\\u003Cdiv', ' ') 
            pre6 = pre5.replace('\\u002Fli', ' ') 
            pre7 = pre6.replace('\\n', ' ') 
            pre8 = pre7.replace('\\t', ' ') 
            pre9 = pre8.replace('\\u003Cstrong', ' ') 
            pre10 = pre9.replace('\\u003C\\u002Fdiv', ', ') 
            pre11 = pre10.replace('\u003C\\u002Fstrong', ' ') 
            pre12 = pre11.replace('style=\\"text-align:justify\\" ', ' ') 
            pre13 = pre12.replace('\\u003C', ' ') 
            pre14 = pre13.replace('\\u002F', '/') 
            pre15 = pre14.replace('/strong', ' ') 
            pre16 = pre15.replace('/ul', ' ') 
            description = pre16.replace('&lt;/div&gt;', ' ')  
            # -------------------------------------------------------------- jobdesk  
            jobdesk = '' 

            # -------------------------------------------------------------- benefit  
            # benefits":["
            pre1 = scriptx.split('benefits":["')[1] 
            benefit = pre1.split('"]}')[0]   

        # ---------------------------------------------------------------------------------- why_join 
            # -------------------------------------------------------------- why_join  
            # whyJoinUs":
            pre1 = scriptx.split('whyJoinUs":')[1] 
            why_join = pre1.split('},')[0]   
                
            # -------------------------------------------------------------- apply_url   
            # applyUrl":{"url":"
            pre1 = scriptx.split('applyUrl":{"url":"')[1] 
            pre2  = pre1.split('",')[0]   
            apply_url = pre2.replace('\\u002F', '/') 

        # ---------------------------------------------------------------------------------- DATE 
            # -------------------------------------------------------------- open  
            # postedDate":" 
            pre1 = scriptx.split('postedDate":"')[1] 
            open = pre1.split('",')[0]  

            # -------------------------------------------------------------- closed  
            # closingDate":"
            pre1 = scriptx.split('closingDate":"')[1] 
            closed = pre1.split('",')[0]  

        # ---------------------------------------------------------------------------------- MY SQL Connection
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="pr_scraping_job_vacancy_indonesia_2022_04"
            )            
            mycursor = mydb.cursor()       
                    
        # -------------------------------------------------------------------------------------------- INSERT INTO WEB
            sql = "INSERT INTO `jobstreet_raws_"+datenow_onlydate+"`(`site`, `scriptx`, `url`, `company`, `company_size`, `address`, `city`, `phone`, `website`, `industry`, `domain`, `title`, `career_level`, `salary_type`, `salary_currency`, `salary_min`, `salary_max`, `placement`, `employment_type`, `working_hours`, `dresscode`, `requirement`, `qualification`, `field_of_study`, `gpa_min`, `experience`, `generalskill`, `hardskill`, `softskill`, `max_age`, `gender`, `description`, `jobdesk`, `benefit`, `why_join`, `apply_url`, `open`, `closed` ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (site, scriptx, url, company, company_size, address, city, phone, website, industry, domain, title, career_level, salary_type, salary_currency, salary_min, salary_max, placement, employment_type, working_hours, dresscode, requirement, qualification, field_of_study, gpa_min, experience, generalskill, hardskill, softskill, max_age, gender, description, jobdesk, benefit, why_join, apply_url, open, closed)
            mycursor.execute(sql, val)
            mydb.commit()

        # ---------------------------------------------------------------------------------- 
            yield {'site': site, 
                   'url': url,  

                   'company' : company,
                   'company_size' : company_size,
                   'address' : address,
                   'city' : city,
                   'phone' : phone,
                   'website' : website,
                   'industry' : industry,
                   
                   'domain' : domain,
                   'title' : title,
                   'career_level' : career_level,
                   'salary_type' : salary_type,
                   'salary_currency' : salary_currency,
                   'salary_min' : salary_min,
                   'salary_max' : salary_max,
                   'placement' : placement,
                   'employment_type' : employment_type,
                   'working_hours' : working_hours,
                   'dresscode' : dresscode,

                   'requirement' : requirement,
                   'qualification' : qualification,
                   'field_of_study' : field_of_study,
                   'gpa_min' : gpa_min,
                   'experience' : experience,
                   'generalskill' : generalskill,
                   'hardskill' : hardskill,
                   'softskill' : softskill,
                   'max_age' : max_age,
                   'gender' : gender,

                   'description' : description,
                   'jobdesk' : jobdesk,
                   'benefit' : benefit,

                   'why_join' : why_join,
                   'apply_url' : apply_url,

                   'open' : open,
                   'closed' : closed,
  

                  }

                
    