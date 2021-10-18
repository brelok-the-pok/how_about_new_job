import datetime
import json

from django.db import models


class Vacancy(models.Model):
    rpc = models.CharField(max_length=512)
    url = models.CharField(max_length=512)
    title = models.CharField(max_length=512)
    employment_type = models.CharField(max_length=64, default='', blank=True)
    company_name = models.CharField(max_length=128, default='')
    location = models.CharField(max_length=512, default='', blank=True)
    vac_type = models.CharField(max_length=512, default='', blank=True)
    job_xp = models.CharField(max_length=512, default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    posted_date = models.DateField(blank=True)
    through_date = models.DateField(blank=True)
    views = models.PositiveSmallIntegerField(default=0, blank=True)
    min_salary = models.PositiveIntegerField(default=0, blank=True)
    max_salary = models.PositiveIntegerField(default=0, blank=True)
    per_time = models.CharField(max_length=64, default='Месяц')
    currency = models.CharField(max_length=64, default='Руб')
    description = models.CharField(max_length=1024, default='', blank=True)
    keywords = models.TextField(default='', blank=True)

    def __str__(self):
        return self.rpc

    def get_keywords(self):
        return json.loads(self.keywords)

    def set_keywords(self, keywords):
        self.keywords = json.dumps(keywords)
