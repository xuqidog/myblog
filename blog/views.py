# -*- coding: utf-8 -*-
from django.shortcuts import render
# from django.http import HttpResponse
from .models import Column, Article, YouDao
from django.shortcuts import redirect  # 重定向（301）
# import time
from django.views.decorators.cache import cache_page  # 添加缓存


# 列表详情
@cache_page(60 * 15)  # 缓存时间 秒数
def column_detail(request, column_slug):
    column = Column.objects.get(slug=column_slug)
    return render(request, 'column.html', {'column': column})
 
# 文章详情
@cache_page(60 * 15)  # 缓存时间 秒数
def article_detail(request, pk, article_slug):
    article = Article.objects.get(pk=pk)

    # 修改时间格式
    article.update_time = article.update_time.strftime("%Y-%m-%d %H:%M:%S")

    if article_slug != article.slug:
        return redirect(article, permanent=True)

    return render(request, 'article.html', {'article': article})

# 首页
@cache_page(60 * 15)  # 缓存时间 秒数
def index(request):
    current_page = int(request.GET.get('page', 1))
    column_slug = request.GET.get('column', 1)
    all_columns = []
    if column_slug != 1:
        page_obj = Pager(current_page, column_slug, 'column')
        all_columns = Column.objects.get(slug=column_slug)
        all_article = all_columns.article_set.all()
        all_item = all_article.count()
        all_article = all_article[page_obj.start:page_obj.end]
    else:
        page_obj = Pager(current_page, '/', 'column')
        all_article = Article.objects.all()[page_obj.start:page_obj.end]
        # 获取所有的分页
        all_item = Article.objects.all().count()

    pager_str = page_obj.page_str(all_item)

    for article in all_article:
        article.update_time = article.update_time.strftime("%Y-%m-%d %H:%M:%S")
        article.columns = article.column.all()

    home_display_columns = Column.objects.filter(home_display=True)
    nav_display_columns = Column.objects.filter(nav_display=True)
 
    return render(request, 'index.html', {
        'home_display_columns': home_display_columns,
        'nav_display_columns': nav_display_columns,
        'all_article': all_article,
        'all_column': all_columns,
        'pager_str': pager_str,
    })

# 分页
class Pager(object):
    def __init__(self, current_page, column, type):
        self.current_page = int(current_page)
        self.column = column
        self.type = type

    @property
    def start(self):
        return (self.current_page-1)*10

    @property
    def end(self):
        return self.current_page*10

    def page_str(self, all_item):
        all_page, div = divmod(all_item, 10)

        if div > 0:
            all_page += 1

        pager_str = ""
        if self.column != '/':
            self.column = '&'+self.type+'='+self.column
        else:
            self.column = ''

        # 前一页
        if self.current_page == 1:
            pager_str += '<li class="disabled"><a href="" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'
        else:
            pager_str += '<li><a href="?page=%d%s" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>' % (self.current_page-1, self.column)

        # 标签页
        for i in range(1, all_page+1):
            if all_page <= 9:  # 只显示一行的页码
                # 每次循环生成一个标签
                if self.current_page == i:
                    temp = '<li class="active"><a href="?page=%d%s">%d</a></li>' % (i, self.column, i,)
                else:
                    temp = '<li><a href="?page=%d%s">%d</a></li>' % (i, self.column, i,)
                pager_str += temp
            else:
                if self.current_page-5 > 0:  # 第一页
                    temp = '<li><a href="?page=%d%s">%s</a></li>' % (1, self.column, '...',)
                    pager_str += temp
                last_page = 0
                for page in range(self.current_page-4, self.current_page):
                    if page <= 0:
                        last_page += 1
                    else:
                        temp = '<li><a href="?page=%d%s">%d</a></li>' % (page, self.column, page,)
                        pager_str += temp
                temp = '<li class="active"><a href="?page=%d%s">%d</a></li>' % (self.current_page, self.column, self.current_page,)
                pager_str += temp
                for page in range(self.current_page+1, self.current_page+4+1+last_page):
                    if page <= all_page:
                        temp = '<li><a href="?page=%d%s">%d</a></li>' % (page, self.column, page,)
                        pager_str += temp
                if self.current_page+4+last_page < all_page:  # 最后一页
                    temp = '<li><a href="?page=%d%s">%s</a></li>' % (all_page, self.column, '...',)
                    pager_str += temp
                break
            # 把标签拼接然后返回给前端
            # pager_str += temp

        # 后一页
        if self.current_page == all_page:
            pager_str += '<li class="disabled"><a href="#" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'
        else:
            pager_str += '<li><a href="?page=%d%s" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>' % (self.current_page+1, self.column)
        return pager_str

# 有道
@cache_page(60 * 15)  # 缓存时间 秒数
def youDao(request):
    current_page = int(request.GET.get('page', 1))
    list_type = request.GET.get('type', 1)
    all_article = YouDao.objects.order_by("time").reverse()
    all_all = all_article.count()
    types = [x.type for x in all_article]  # 获取所有type 并且去重
    all_type = []
    for one in set(types):
        all_type.append({'type': one, 'count': types.count(one)})

    if list_type != 1:
        all_article = YouDao.objects.filter(type=list_type).order_by("time").reverse()
        all_item = all_article.count()
        page_obj = Pager(current_page, list_type, 'type')
        all_article = all_article[page_obj.start:page_obj.end]
    else:
        page_obj = Pager(current_page, '/', 'type')
        all_item = all_all
        all_article = all_article[page_obj.start:page_obj.end]

    pager_str = page_obj.page_str(all_item)
    return render(request, 'youDao.html', {
        'all_article': all_article,
        'pager_str': pager_str,
        'all_type': all_type,
        'all_all': all_all
    })
