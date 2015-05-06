from models import *
from django.shortcuts import *
from django.db.models import *
from salaries.models import *
from django.http import HttpResponse

list_of_govs = Govt.objects.filter(viewable=1).order_by('type').annotate(Count('salary'))
emptotal = Salary.objects.filter(govt__viewable=1).count()

#Main page for either state or local salaries
def Main(request, bigtype):
    list_of_govs = Govt.objects.filter(bigtype=bigtype).filter(viewable=1).order_by('type').annotate(Count('salary'))
    govcount = list_of_govs.count()
    top10 = Salary.objects.filter(govt__viewable=1, bigtype=bigtype).order_by("-total_gross")[:10]
    #elected = Salary.objects.filter(govt__viewable=1).filter(status="Elected").order_by('-total_gross')
    types = Govt.objects.filter(viewable=1).filter(bigtype=bigtype).values('type').distinct()
    top_by_gov = {}
    for thing in list_of_govs:
        top_by_gov[thing.name] = Salary.objects.filter(govt=thing.name).order_by("-total_gross")[:10]        
    dictionaries = { 'govcount': govcount, 'top10':top10, 'types': types, 'emptotal':emptotal, 'list_of_govs': list_of_govs, 'top_by_gov': top_by_gov  }
    return render_to_response('salaries/index.html', dictionaries)

def GovtPage(request, bigtype, govtname):
    people = Salary.objects.filter(govt__viewable=1).filter(govslug=govtname).order_by('-total_gross')
    under25 = people.filter(total_gross__lte=25000)
    under50 = people.filter(total_gross__gt=25000).filter(total_gross__lte=50000)
    under75 = people.filter(total_gross__gt=50000).filter(total_gross__lte=75000)
    under100 = people.filter(total_gross__gt=75000).filter(total_gross__lte=100000)
    under125 = people.filter(total_gross__gt=100000).filter(total_gross__lte=125000)
    under150 = people.filter(total_gross__gt=125000).filter(total_gross__lte=150000)
    over150 = people.filter(total_gross__gt=150000)
    first = people[0]
    govt = first.govt
    hire = first.hiredate
    total = Salary.objects.filter(govt__viewable=1, govslug=govtname).aggregate(Sum('total_gross'))['total_gross__sum']
    base = Salary.objects.filter(govt__viewable=1, govslug=govtname).aggregate(Sum('display_sal'))['display_sal__sum']
    other = Salary.objects.filter(govt__viewable=1, govslug=govtname).aggregate(Sum('nonsalary'))['nonsalary__sum']
    departments = people.values('dept').distinct().annotate(dtotal=Sum('total_gross')).order_by('dept')
    topearns = people[:10]
    bigwigs = people.exclude(bigwig='')
    dictionaries = { 'govt': govt, 'people': people, 'departments': departments, 'topearns':topearns, 'list_of_govs': list_of_govs, 'hire':hire, 'other':other, 'total':total, 'base':base, 'under25':under25, 'under50':under50, 'under75':under75, 'under100':under100, 'under125':under125, 'under150':under150, 'over150':over150, 'bigwigs':bigwigs, }
    return render_to_response('salaries/government.html', dictionaries)

def DeptPage(request, bigtype, govtname, deptname):
    people = Salary.objects.filter(govt__viewable=1).filter(govslug=govtname, deptslug=deptname).order_by('-total_gross')
    dept_total = people.values('dept').distinct().annotate(total=Sum('total_gross'))[0]
    first = people[0]
    govt = first.govt
    dept = first.dept
    total = Salary.objects.filter(govt__viewable=1, govslug=govtname, deptslug=deptname).aggregate(Sum('total_gross'))['total_gross__sum']
    base = Salary.objects.filter(govt__viewable=1, govslug=govtname, deptslug=deptname).aggregate(Sum('display_sal'))['display_sal__sum']
    other = Salary.objects.filter(govt__viewable=1, govslug=govtname, deptslug=deptname).aggregate(Sum('nonsalary'))['nonsalary__sum']

    departments = Salary.objects.filter(govt__viewable=1).filter(govslug=govtname).values('dept').distinct().annotate(dtotal=Sum('total_gross')).order_by('-dtotal')
    dictionaries = { 'govt': govt, 'dept': dept, 'dept_total': dept_total, 'people': people, 'departments': departments, 'list_of_govs': list_of_govs, 'base':base, 'other':other, 'total':total, }
    return render_to_response('salaries/department.html', dictionaries)

def NamelessIndividualPage(request, govtname, deptname, id):
    govt = govtname
    person = Salary.objects.get(pk=id)
    more_employees = Salary.objects.filter(govslug=govtname, deptslug=deptname, total_gross__gt=50000).order_by('-total_gross')
    this_govt = Salary.objects.filter(govslug=govtname).order_by('-total_gross')
    this_dept = this_govt.filter(deptslug=deptname).order_by('-total_gross')
    departments = Salary.objects.filter(govslug=govtname).values('dept').distinct().annotate(dtotal=Sum('total_gross')).order_by('-dtotal')

    dictionaries = {'govt': govt, 'person': person, 'more_employees': more_employees, 'list_of_govs': list_of_govs, 'departments': departments, 
'this_govt': this_govt, 'this_dept': this_dept, }
    return render_to_response('salaries/individual.html', dictionaries)


def IndividualPage(request, bigtype, govtname, deptname, nameslug):
    govt = govtname
    person = Salary.objects.get(govslug=govtname, deptslug=deptname, nameslug=nameslug)
    more_employees = Salary.objects.filter(govslug=govtname, deptslug=deptname, total_gross__gt=50000).order_by('-total_gross')[:30]
    this_govt = Salary.objects.filter(govslug=govtname).order_by('-total_gross')
    this_dept = this_govt.filter(deptslug=deptname).order_by('-total_gross')
    departments = Salary.objects.filter(govslug=govtname).values('dept').distinct().annotate(dtotal=Sum('total_gross')).order_by('-dtotal')

    dictionaries = { 'govt': govt, 'person': person, 'more_employees': more_employees, 'list_of_govs': list_of_govs, 'departments': departments, 
'this_govt': this_govt, 'this_dept': this_dept, }
    return render_to_response('salaries/individual.html', dictionaries)


def Search(request):
    query = request.GET.get('q', '')
    exploded = query.split(" ")
    q_objects = Q()
    for term in exploded:
        q_objects &= Q(fullname__icontains=term)

    if query:
        qset = (
            q_objects
        )
        results = Salary.objects.filter(govt__viewable=1).filter(total_gross__gt=50000).filter(qset)
    else:
        results = []

    dictionaries = { 'results': results, 'query': query, 'list_of_govs': list_of_govs, 'emptotal': emptotal, }
    return render_to_response('salaries/search.html', dictionaries)

def CatePage(request):
    people = Salary.objects.filter(govt__viewable=1).exclude(bigwig='').order_by('bigwig')
    dictionaries = { 'people': people, 'list_of_govs': list_of_govs, }
    return render_to_response('salaries/catepage.html', dictionaries)

def JeffPage(request):
    people = Salary.objects.filter(govt__viewable=1).order_by('-total_gross')
    dictionaries = { 'people': people, 'list_of_govs': list_of_govs, 'emptotal':emptotal, }
    return render_to_response('salaries/jeffpage.html', dictionaries)

def ArticlePage(request):
    dictionaries = { 'list_of_govs': list_of_govs, }
    return render_to_response('salaries/articlepage.html', dictionaries)
