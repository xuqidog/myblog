"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from DjangoUeditor import urls as DjangoUeditor_urls
from blog.views import article_detail, column_detail, index
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_URL}),
    # url(r'^column/(?P<column_slug>[^/]+)/$', column_detail, name='column'),
    # url(r'^news/(?P<article_slug>[^/]+)/$', article_detail, name='article'),
    url(r'^news/(?P<pk>\d+)/(?P<article_slug>[^/]+)/$', article_detail, name='article'),
    # url(r'^news/(?P<pk>\d+)/(?P<article_slug>[^/]+)/$', column_detail, name='column'),
    url(r'^ueditor/', include(DjangoUeditor_urls)),
    url(r'^admin/', admin.site.urls),
]