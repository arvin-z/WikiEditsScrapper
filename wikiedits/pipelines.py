# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging

from itemadapter import ItemAdapter
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem
from wikiedits.models import Edit, Tag, db_connect, create_table


class WikieditsPipeline:
    def process_item(self, item, spider):
        return item


class SaveEditsPipeline(object):
    def __init__(self):
        """Connect to database and create tables.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save Item in database.
        """
        session = self.Session()
        edit = Edit()
        tag = Tag()
        edit.ip_addr = item['ip_addr']
        edit.change = item['change']
        edit.new_words = item['new_words']

        if "tags" in item:
            for tag_name in item["tags"]:
                tag = Tag(name=tag_name)
                # check whether the current tag already exists in the database
                exist_tag = session.query(Tag).filter_by(name=tag.name).first()
                if exist_tag is not None:  # the current tag exists
                    tag = exist_tag
                edit.tags.append(tag)

        try:
            session.add(edit)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return item


# class DuplicatesPipeline(object):
#     def __init__(self):
#         """Connect to database and create tables.
#         """
#         engine = db_connect()
#         create_table(engine)
#         self.Session = sessionmaker(bind=engine)
#         logging.info("****DuplicatesPipeline: database connected****")
#
#     def process_item(self, item, spider):
#         session = self.Session()
#         exist_quote = session.query(Edit).filter_by(quote_content=item["ip_addr"]).first()
#         if exist_quote is not None:
#             raise DropItem("Duplicate item found: %s" % item["ip_addr"])
#             session.close()
#         else:
#             return item
#             session.close()
