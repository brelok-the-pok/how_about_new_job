import json
from datetime import datetime

import scrapy
from scrapy import Request

from ..constants.hh_parser import *


class BaseParser(scrapy.Spider):

    @staticmethod
    def get_next_page(response):
        next_page = response.xpath(NEXT_PAGE).get('')
        if next_page:
            next_page = response.urljoin(next_page)
        return next_page

    @staticmethod
    def get_result_container(response):
        result = {
            'url': response.url,
            'rpc': '',
            'title': '',
            'posted_date': '',
            'through_date': '',
            'employment_type': '',
            'company_name': '',
            'min_salary': 0,
            'max_salary': 0,
            'per_time': '',
            'currency': '',
            'location': '',
            'description': '',
            'vac_type': '',
            'views': 0,
            'job_xp': '',
            'keywords': [],
        }
        return result

    def get_vac_jo(self, response):
        try:
            jo_1 = json.loads(response.xpath(VAC_JO_1).get())
            jo_2 = json.loads(response.xpath(VAC_JO_2).get())
            jo_1.update(jo_2)
        except:
            self.logger.warning(f'Ошибка при получении json со страницы вакансии: {response.url}')
            jo_1 = dict()
        finally:
            return jo_1

    @staticmethod
    def get_id(jo):
        id = jo['identifier']['value']
        return {'rpc': id}

    @staticmethod
    def get_title(jo):
        title = jo.get('title', '')
        return {'title': title}

    def get_date(self, response, jo, key):
        # Поскольку дата создания не является сильно критичной вешаем try except для сохранения остальных данных
        try:
            posted_date = jo[key]
            if posted_date:
                posted_date = posted_date.partition('T')[0]
                posted_date = datetime.strptime(posted_date, "%Y-%m-%d")
                posted_date = posted_date.timestamp()
        except:
            self.logger.warning(f'Ошибка при получении {key}: {response.url}')
            posted_date = 0
        finally:
            return posted_date

    def get_posted_date(self, response, jo):
        key = 'datePosted'
        posted_date = self.get_date(response, jo, key)
        return {'posted_date': posted_date}

    def get_through_date(self, response, jo):
        key = 'validThrough'
        posted_date = self.get_date(response, jo, key)
        return {'through_date': posted_date}

    def get_employment_type(self, response, jo):
        employment_type = jo.get('employmentType')
        translated_type = EMPLOYMENT_TYPE.get(jo.get('employmentType'), '')
        if not translated_type:
            self.logger.warning(f'Неизвестный тип занятости {employment_type}: {response.url}')
        return {'employment_type': translated_type}

    @staticmethod
    def get_company_name(jo):
        name = jo.get('hiringOrganization', {}).get('name', '')
        return {'company_name': name}

    @staticmethod
    def get_salary(jo):
        salary = jo.get('baseSalary', {})
        min_salary = salary.get('value', {}).get('minValue', 0.0)
        max_salary = salary.get('value', {}).get('maxValue', 0)
        per_time = salary.get('value', {}).get('unitText', '')
        currency = salary.get('currency', '')
        return {'min_salary': min_salary, 'max_salary': max_salary, 'per_time': per_time, 'currency': currency}

    @staticmethod
    def get_location(jo):
        location = jo.get('jobLocation', {}).get('address', {})
        location = f"{location.get('addressRegion', '')}, {location.get('streetAddress', '')}"
        return {'location': location}

    @staticmethod
    def get_description(jo):
        description = jo.get('description', '')
        return {'description': description}

    @staticmethod
    def get_vac_type(jo):
        vac_type = jo.get('vac_type', '')
        return {'vac_type': vac_type}

    def get_views(self, response, jo):
        try:
            views = int(jo['vac_views'])
        except:
            self.logger.warning(f'Ошибка при получении числа просмотров вакансии: {response.url}')
            views = 0
        finally:
            return {'views': views}

    def get_job_xp(self, response, jo):
        job_xp = jo.get('vac_exp')
        translated_job_xp = XP_TIME.get(job_xp, '')
        if not translated_job_xp:
            self.logger.warning(f'Неизвестный требуемый опыт {job_xp}: {response.url}')
        return {'job_xp': translated_job_xp}

    @staticmethod
    def get_keywords(jo):
        keywords = jo.get('vac_skills', [])
        return {'keywords': keywords}


class HhSpider(BaseParser):
    """
    Нужны мидлвары обработки результата, а также pydantic модель на сервеке

    Хочу на сайте график, который бы показывал число вакансий по моим запросам
    квантили по зпшке, среднюю зпшку, квантили по опыту работы и подобное

    """

    name = 'hh_parser'
    custom_settings = {
        'DOWNLOAD_TIMEOUT': 60,
        'DOWNLOAD_DELAY': 0.2,
        'CONCURRENT_REQUESTS': 50,
    }

    def __init__(self, update=True):
        self.start_urls = START_URLS
        self.update = update

    def start_requests(self):
        if self.update:
            for url in self.start_urls:
                yield Request(url=url, callback=self.parse)

    def parse(self, response):
        jo = response.xpath(SEARCH_JO).get()
        jo = json.loads(jo)
        vacancies = jo['vacancySearchResult']['vacancies']
        urls = [HH_VAC_URL.format(id=x['vacancyId']) for x in vacancies]
        for url in urls[:3]:
            yield Request(url=url, callback=self.parse_vac)

        next_page = self.get_next_page(response)
        # if next_page:
        #     yield Request(url=next_page, callback=self.parse, dont_filter=True)

    def parse_vac(self, response):
        result = self.get_result_container(response)
        jo = self.get_vac_jo(response)
        try:
            result.update(self.get_id(jo))
            result.update(self.get_title(jo))
            result.update(self.get_posted_date(response, jo))
            result.update(self.get_through_date(response, jo))
            result.update(self.get_employment_type(response, jo))
            result.update(self.get_company_name(jo))
            result.update(self.get_salary(jo))
            result.update(self.get_location(jo))
            result.update(self.get_description(jo))
            result.update(self.get_vac_type(jo))
            result.update(self.get_views(response, jo))
            result.update(self.get_job_xp(response, jo))
            result.update(self.get_keywords(jo))
        except Exception as e:
            self.logger.error(f"Возникла ошибка при сборе {response.url}\n Ошибка: {e}")
        else:
            yield result
