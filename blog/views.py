# -*- coding: utf-8 -*-
from django.shortcuts import render
# from django.http import HttpResponse
from .models import Column, Article
from django.shortcuts import redirect  # 重定向（301）
# import time
from django.views.decorators.cache import cache_page  # 添加缓存
# Create your views here.

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
        page_obj = Pager(current_page, column_slug)
        all_columns = Column.objects.get(slug=column_slug)
        all_article = all_columns.article_set.all()
        all_item = all_article.count()
        all_article = all_article[page_obj.start:page_obj.end]
    else:
        page_obj = Pager(current_page, '/')
        all_article = Article.objects.all()[page_obj.start:page_obj.end]
        # 获取所有的分页
        all_item = Article.objects.all().count()

    pager_str = page_obj.page_str(all_item)

    for article in all_article:
        article.update_time = article.update_time.strftime("%Y-%m-%d %H:%M:%S")
        article.columns = article.column.all()

    home_display_columns = Column.objects.filter(home_display=True)
    nav_display_columns = Column.objects.filter(nav_display=True)
    # all = Column()
    # all.name = '全部'
    # all.slug = 1
    # home_display_columns.insert(0,all)
    # nav_display_columns.insert(0,all)
 
    return render(request, 'index.html', {
        'home_display_columns': home_display_columns,
        'nav_display_columns': nav_display_columns,
        'all_article': all_article,
        'all_column': all_columns,
        'pager_str': pager_str
    })

# 分页
class Pager(object):
    def __init__(self, current_page, column):
        self.current_page = int(current_page)
        self.column = column

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
            self.column = '&column='+self.column
        else:
            self.column = ''

        # 前一页
        if self.current_page == 1:
            pager_str += '<li class="disabled"><a href="" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'
        else:
            pager_str += '<li><a href="/?page=%d%s" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>' % (self.current_page-1, self.column)

        # 标签页
        for i in range(1, all_page+1):
            # 每次循环生成一个标签
            if self.current_page == i:
                temp = '<li class="active"><a href="/?page=%d%s">%d</a></li>' % (i, self.column, i,)
            else:
                temp = '<li><a href="/?page=%d%s">%d</a></li>' % (i, self.column, i,)
            # 把标签拼接然后返回给前端
            pager_str += temp

        # 后一页
        if self.current_page == all_page:
            pager_str += '<li class="disabled"><a href="#" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'
        else:
            pager_str += '<li><a href="/?page=%d%s" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>' % (self.current_page+1, self.column)
        return pager_str