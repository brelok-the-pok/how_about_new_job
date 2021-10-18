import datetime
import json
import requests

POST_API = "http://127.0.0.1:8000/vacancy/create"


class SpiderPipeline(object):
    def __init__(self, unique_id, *args, **kwargs):
        self.unique_id = unique_id
        self.items = []

    @classmethod
    def from_crawler(cls, crawler):
        return cls(unique_id=crawler.settings.get('unique_id'), )

    def close_spider(self, spider):
        response = requests.post(url=POST_API, json=self.items)
        spider.log(response)

    def process_item(self, item, spider):
        item['keywords'] = json.dumps(item['keywords'])
        self.items.append(item)
        return item
