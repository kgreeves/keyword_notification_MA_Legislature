# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from os import getenv
import re
import psycopg2
from itemadapter import ItemAdapter
from dotenv import load_dotenv


class KeywordMaLegislaturePipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        field_names = adapter.field_names()

        ## Remove 'Bill' from bill_no
        for field_name in field_names:
            if field_name == 'bill_no':

                value = adapter.get(field_name)
                value = value.strip().replace('\r\n', '').split(' ')[-1]
                adapter[field_name] = value
                value = value.split('.')
                adapter['leg_body'] = value[0]
                adapter['bill_no_int'] = int(value[1])

            ## Separate Filed by into first, middle and last names if person
            elif field_name == 'filed_by':
                value = adapter.get(field_name)
                value = value.strip().replace('\r\n', '').split(' ')

                if len(value) == 2:
                    adapter['filed_by_first'], adapter['filed_by_last'] = tuple(value)
                elif len(value) == 3:
                    adapter['filed_by_first'], adapter['filed_by_middle_init'], adapter['filed_by_last'] = tuple(value)
                else:
                    adapter[field_name] = ' '.join(value)

            ## Strip all whitespaces from strings
            elif field_name == 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value.strip()

            ## Get session number from string
            elif field_name == 'session_no':
                value = adapter.get(field_name)
                value = value.replace('\r\n', '').split('(')[0]
                session_no = re.findall(r'\d+', value)
                adapter[field_name] = int(session_no[0])

            else:
                pass
        return item

class SavingToPostgresPipeline(object):

    def __init__(self):
        self.create_connection()

    def create_connection(self):

        self.conn = psycopg2.connect(
            host=getenv('PG_HOST'),
            port=getenv('PG_PORT'),
            database=getenv('PG_DATABASE'),
            user=getenv('PG_USER'),
            password=getenv('PG_PASSWORD'))

        self.curr = self.conn.cursor()

    def process_item(self, item, spider):
        self.store_in_db(item)
        # we need to return the item below as scrapy expects us to!
        return item

    def store_in_db(self, item):
        self.curr.execute(""" insert into bill_table 

        (bill_no,
        leg_body,
        bill_no_int,
        filed_by,
        filed_by_last,
        filed_by_first,
        filed_by_middle,
        title,
        description,
        url,
        session_no)

        values( %s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s )

        """,
                          (item['bill_no'],
                           item['leg_body'],
                           item['bill_no_int'],
                           item['filed_by'],
                           item['filed_by_last'],
                           item['filed_by_first'],
                           item['filed_by_middle'],
                           item['title'],
                           item['description'],
                           item['url'],
                           item['session_no'])
                          )

        self.conn.commit()

    def close_spider(self, spider):

        ## Close cursor and conenction to database
        self.curr.close()
        self.conn.close()
