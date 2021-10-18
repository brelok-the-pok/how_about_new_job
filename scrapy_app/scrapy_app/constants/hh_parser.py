

START_URLS = [
    'https://spb.hh.ru/search/vacancy?area=2&fromSearchLine=true&st=searchVacancy&text=python'
]

HH_VAC_URL = "https://spb.hh.ru/vacancy/{id}"

NEXT_PAGE = "//a[@data-qa='pager-next']/@href"

VACANCY_HREF = "//span[@class='g-user-content']/a/@href"
SEARCH_JO = "//template[@id='HH-Lux-InitialState']/text()"

VAC_JO_1 = "//script[@type='application/ld+json']/text()"
VAC_JO_2 = "//script[@data-name='HH/GoogleDfpService']/@data-params"

EMPLOYMENT_TYPE = {
    'FULL_TIME': 'Полная занятость, полный день'
}

XP_TIME = {
    'between1And3': '1-3 года'
}
