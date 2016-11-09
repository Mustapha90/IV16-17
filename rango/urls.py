from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),  # New!
    url(r'^category/(?P<category_name_slug>\w+)/add_page/$', views.add_page, name='add_page'),
    url(r'^reclama_datos/', views.reclama_datos, name='reclama_datos'),
    url(r'^like_category/$', views.like_category, name='like_category'),
    
)
	
