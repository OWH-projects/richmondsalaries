from django.db import models
from django.db.models import *
from django.template.defaultfilters import slugify
import datetime

def CheckNull(x):
    if x:
	    return x
    else:
        return 0	

class Govt(models.Model):
    name = models.CharField(max_length=60, null=False, blank=False, primary_key=True)
    full_name = models.CharField(max_length=60, null=False, blank=False)
    bigtype = models.CharField(max_length=60, null=False, blank=False)
    type = models.CharField(max_length=60, null=False, blank=False)
    population = models.IntegerField(null=True, blank=True)
    viewable = models.NullBooleanField()
    payroll_count = models.IntegerField(null=True, blank=True)
    payroll_sum = models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)
    ft_median = models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)
    ft_avg = models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)
    ft_max = models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)
    text = models.TextField(null=True, blank=True)
    url = models.CharField(max_length=200, null=True, blank=True)
    pic = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = u'salaries_govts'

    def __unicode__(self):
        return self.name

    def save(self):
        self.payroll_sum = Govt.objects.get(name__iexact = self.name).salary_set.aggregate(Sum('total_gross'))['total_gross__sum']
        self.ft_avg = Govt.objects.get(name__iexact = self.name).salary_set.filter(status="FT").aggregate(Avg('total_gross'))['total_gross__avg']
        self.ft_max = Govt.objects.get(name__iexact = self.name).salary_set.filter(status="FT").aggregate(Max('total_gross'))['total_gross__max']
        self.payroll_count = Govt.objects.get(name__iexact = self.name).salary_set.count()
        self.ft_median = Govt.objects.get(name__iexact = self.name).salary_set.filter(status="FT").order_by('total_gross')[int(round(Govt.objects.get(name__iexact = self.name).salary_set.filter(status="FT").count() / 2))].total_gross
        super(Govt, self).save()

class Salary(models.Model):
    bigtype = models.CharField(max_length=20, null=False, blank=False)
    govt = models.ForeignKey(Govt)
    last = models.CharField(max_length=60, null=False, blank=False)
    rest = models.CharField(max_length=60, null=False, blank=False)
    fullname = models.CharField(max_length=100, null=False, blank=False)
    dob = models.CharField(max_length=10, null=True, blank=True)
    dept = models.CharField(max_length=60, null=False, blank=False)
    job = models.CharField(max_length=60, null=False, blank=False)
    status = models.CharField(max_length=30, null=True, blank=True)
    hiredate = models.CharField(max_length=10, null=True, blank=True)
    salary = models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=False)
    display_sal = models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=False)
    deferred = models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)
    total_gross = models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=False)
    extra = models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)
    bonus_allowances = models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)
    additional = models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)
    masters = models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)
    nameslug = models.CharField(max_length=60)
    deptslug = models.CharField(max_length=60)
    govslug = models.CharField(max_length=60)
    year = models.IntegerField(max_length=4, null=False, blank=False)
    comments = models.TextField(blank=True)
    length = models.IntegerField(max_length=3, null=True, blank=True)
    bigwig = models.CharField(max_length=50, null=True, blank=True)
    photo = models.URLField(null=True, blank=True)
    nonsalary = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=2)
    
    class Meta:
        db_table = u'salaries'

    def __unicode__(self):
        return self.rest + " " + self.last

    def save(self):
#        curr = datetime.date(2013,12,31)
#        if self.hiredate:
#            then = self.hiredate
#            diff = curr - then
#            self.length = int(diff.days / 365.25)
        self.nameslug = '%s' % slugify(self.fullname)
        self.deptslug = '%s' % slugify(self.dept)
        self.govslug = '%s' % slugify(self.govt)
        nonsals = [CheckNull(self.deferred), CheckNull(self.extra), CheckNull(self.bonus_allowances), CheckNull(self.additional), CheckNull(self.masters)]

        self.nonsalary = sum(nonsals)

        if self.nonsalary == 0 or self.salary == 0:
            self.salary = self.total_gross

        if self.salary > self.total_gross:
            self.display_sal = self.total_gross
        else:
            self.display_sal = self.salary
        print self.nameslug
        super(Salary, self).save()
