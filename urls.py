from django.conf.urls import *
from django.views.generic import TemplateView

urlpatterns = patterns('',
    (r'^/about$', 'salaries.views.JeffPage'),
    (r'^/positions$', 'salaries.views.CatePage'),
    (r'^/read$', 'salaries.views.ArticlePage'),
    (r'^/search$', 'salaries.views.Search'),
    (r'^/(?P<bigtype>[a-zA-Z0-9_.-]+)/(?P<govtname>[a-zA-Z0-9_.-]+)/(?P<deptname>[a-zA-Z0-9_.-]+)/(?P<id>[0-9_.-]+)$', 'salaries.views.NamelessIndividualPage'),
    (r'^/(?P<bigtype>[a-zA-Z0-9_.-]+)/(?P<govtname>[a-zA-Z0-9_.-]+)/(?P<deptname>[a-zA-Z0-9_.-]+)/(?P<nameslug>[a-zA-Z0-9_.-]+)$', 'salaries.views.IndividualPage'),
    (r'^/(?P<bigtype>[a-zA-Z0-9_.-]+)/(?P<govtname>[a-zA-Z0-9_.-]+)/(?P<deptname>[a-zA-Z0-9_.-]+)$', 'salaries.views.DeptPage'),
    (r'^/(?P<bigtype>[a-zA-Z0-9_.-]+)/(?P<govtname>[a-zA-Z0-9_.-]+)$', 'salaries.views.GovtPage'),
    (r'^/(?P<bigtype>[a-zA-Z0-9_.-]+)$', 'salaries.views.Main'),
    (r'^', TemplateView.as_view(template_name="salaries/landingpage.html")),    
    )
