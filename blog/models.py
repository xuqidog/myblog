# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from DjangoUeditor.models import UEditorField


@python_2_unicode_compatible
class Column(models.Model):
    name = models.CharField('栏目名称', max_length=256)
    slug = models.CharField('栏目网址', max_length=256, db_index=True)
    intro = models.TextField('栏目简介',default='')

    nav_display = models.BooleanField('导航显示', default=False)
    home_display = models.BooleanField('首页显示', default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('column', args=(self.slug, ))

    class Meta:
        verbose_name = '栏目'
        verbose_name_plural = '栏目'
        ordering = ['name']  # 按照哪个栏目排序


@python_2_unicode_compatible
class Article(models.Model):
    column = models.ManyToManyField(Column, verbose_name='归属栏目')
 
    title = models.CharField('标题', max_length=256)
    slug = models.CharField('网址', max_length=256, db_index=True)
 
    author = models.ForeignKey('auth.User', blank=True, null=True, verbose_name='作者')
    content = UEditorField('内容', height=300, width=1000,
        default=u'', blank=True, imagePath="uploads/images/",
        toolbars='besttome', filePath='uploads/files/')
 
    published = models.BooleanField('正式发布', default=True)

    pub_date = models.DateTimeField('发表时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField('更新时间', auto_now=True, null=True)
 
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article', args=(self.pk, self.slug))
 
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'


@python_2_unicode_compatible
class YouDao(models.Model):
    title = models.CharField('标题', max_length=256)
    channelName = models.CharField('分类', max_length=256)
    type = models.CharField('标签', max_length=256)
    url = models.CharField('内容链接', max_length=256)
    image_desk = models.CharField('图片链接', max_length=256)
    audiourl = models.CharField('音频链接', max_length=256)
    videourl = models.CharField('视频链接', max_length=256)
    time = models.CharField('创建时间', max_length=256)
    slug = models.CharField('slug', max_length=256, db_index=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('youDao')

    class Meta:
        verbose_name = '有道精选'
        verbose_name_plural = '有道精选'