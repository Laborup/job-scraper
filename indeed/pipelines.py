# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class IndeedPipeline:
    
    def __init__(self):
        ## Create/Connect to database
        self.con = sqlite3.connect('jobs.db')

        ## Create cursor, used to execute commands
        self.cur = self.con.cursor()
        
        ## Create jobs table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS jobs(
            keyword TEXT,
            location TEXT,
            page INTEGER,
            position INTEGER,
            company TEXT,
            companyRating REAL,
            companyReviewCount INTEGER,
            highlyRatedEmployer INTEGER,
            jobkey TEXT,
            jobTitle TEXT,
            jobLocationCity TEXT,
            jobLocationPostal TEXT,
            jobLocationState TEXT,
            maxSalary INTEGER,
            minSalary INTEGER,
            salaryType TEXT,
            pubDate TEXT, 
            salaryText TEXT,
            urgentlyHiring INTEGER,
            jobDescription TEXT,
            jobUrl TEXT
        )
        """)

    def process_item(self, item, spider):
        ## Check to see if text is already in database 
        self.cur.execute("select * from jobs where jobkey = ?", (item['jobkey'],))
        result = self.cur.fetchone()
        
        ## If it is in DB, create log message
        if result:
            spider.logger.warn("Item already in database: %s" % item['text'])
        ## If text isn't in the DB, insert data
        else:
            ## Define insert statement
            self.cur.execute("""
                INSERT INTO jobs (keyword, location, page, position, company, companyRating, companyReviewCount, 
                highlyRatedEmployer, jobKey, jobTitle, jobLocationCity, jobLocationPostal, jobLocationState, maxSalary, minSalary, salaryType, pubDate, salaryText, urgentlyHiring, jobDescription, jobUrl ) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item['keyword'],
                item['location'],
                item['page'],
                item['position'],
                item['company'],
                item['companyRating'],
                item['companyReviewCount'],
                item['highlyRatedEmployer'],
                item['jobkey'],
                item['jobTitle'],
                item['jobLocationCity'],
                item['jobLocationPostal'],
                item['jobLocationState'],
                item['maxSalary'],
                item['minSalary'],
                item['salaryType'],
                item['pubDate'],
                item['salaryText'],
                item['urgentlyHiring'],
                item['jobDescription'], 
                item['jobUrl']
            ))

            ## Execute insert of data into database
            self.con.commit()
            
        return item
