import re
import json
import scrapy
from urllib.parse import urlencode
from indeed.items import IndeedItem

class IndeedSearchSpider(scrapy.Spider):
    name = "indeed_search"
    custom_settings = {
        'FEEDS': { 'data/%(name)s_%(time)s.csv': { 'format': 'csv',}}
        }

    def get_indeed_search_url(self, keyword, location, offset=0):
        parameters = {"q": keyword, "l": location, "filter": 0, "start": offset}
        return "https://www.indeed.com/jobs?" + urlencode(parameters)

    def start_requests(self):
        keyword_list = ['manufacturing']
        location_list = ['Tennessee']
        for keyword in keyword_list:
            for location in location_list:
                indeed_jobs_url = self.get_indeed_search_url(keyword, location)
                yield scrapy.Request(url=indeed_jobs_url, callback=self.parse_search_results, meta={'keyword': keyword, 'location': location, 'offset': 0})


    def parse_search_results(self, response):
        location = response.meta['location']
        keyword = response.meta['keyword'] 
        offset = response.meta['offset'] 
        script_tag  = re.findall(r'window.mosaic.providerData\["mosaic-provider-jobcards"\]=(\{.+?\});', response.text)
        if script_tag is not None:
            json_blob = json.loads(script_tag[0])

            ## Extract Jobs From Search Page
            jobs_list = json_blob['metaData']['mosaicProviderJobCardsModel']['results']
            for index, job in enumerate(jobs_list):
                item = IndeedItem()
                item['keyword'] = keyword
                item['location'] = location
                item['page'] = round(offset / 10) + 1 if offset > 0 else 1
                item['position'] = index
                item['company'] = job.get('company')
                item['companyRating'] = job.get('companyRating')
                item['companyReviewCount'] = job.get('companyReviewCount')
                item['companyRating'] = job.get('companyRating')
                item['highlyRatedEmployer'] = job.get('highlyRatedEmployer')
                item['jobkey'] = job.get('jobkey')
                item['jobTitle'] = job.get('title')
                item['jobLocationCity'] = job.get('jobLocationCity')
                item['jobLocationPostal'] = job.get('jobLocationPostal')
                item['jobLocationState'] = job.get('jobLocationState')
                item['maxSalary'] = job.get('estimatedSalary').get('max') if job.get('estimatedSalary') is not None else 0
                item['minSalary'] = job.get('estimatedSalary').get('min') if job.get('estimatedSalary') is not None else 0
                item['salaryType'] = job.get('estimatedSalary').get('max') if job.get('estimatedSalary') is not None else 'none'
                item['pubDate'] = job.get('pubDate')
                item['salaryText'] = job.get('salarySnippet').get('text') if job.get('salarySnippet') is not None else 'none'
                item['urgentlyHiring'] = job.get('urgentlyHiring')
                if job.get('jobkey') is not None:
                    job_url = 'https://www.indeed.com/m/basecamp/viewjob?viewtype=embedded&jk=' + job.get('jobkey')
                    item['jobUrl'] = job_url
                    yield scrapy.Request(url=job_url, 
                            callback=self.parse_job, 
                            meta={
                                'item': item,
                                'jobKey': job.get('jobkey'),
                            })
                else:
                    yield item
            
            ## Paginate Through Jobs Pages
            if offset == 0:
                meta_data = json_blob["metaData"]["mosaicProviderJobCardsModel"]["tierSummaries"]
                num_results = sum(category["jobCount"] for category in meta_data)
                #if num_results > 1000:
                #    num_results = 50
                
                for offset in range(10, num_results + 10, 10):
                    url = self.get_indeed_search_url(keyword, location, offset)
                    yield scrapy.Request(url=url, callback=self.parse_search_results, meta={'keyword': keyword, 'location': location, 'offset': offset})

    def parse_job(self, response):
        item = response.meta['item']
        script_tag  = re.findall(r"_initialData=(\{.+?\});", response.text)
        if script_tag is not None:
            json_blob = json.loads(script_tag[0])
            job = json_blob["jobInfoWrapperModel"]["jobInfoModel"]
            item['jobDescription'] = job.get('sanitizedJobDescription')
        
        yield item


