# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Express(models.Model):
    number = models.BigIntegerField(unique=True, verbose_name='运单号')
    orig = models.CharField(max_length=200, blank=True, null=True, verbose_name='发件网点')
    start_time = models.DateTimeField(auto_now_add=True, verbose_name='开单时间')
    status = models.CharField(max_length=50, blank=True, null=True, verbose_name='运单状态')
    # follower = models.CharField(max_length=200, blank=True, null=True, verbose_name='跟进人')
    follower = models.ForeignKey(
        User, related_name='express_set',
        limit_choices_to={'is_superuser': False},
        verbose_name='跟进人'
    )
    detail = models.TextField(max_length=1000, blank=True, null=True, verbose_name='客户诉求')
    error_type = models.CharField(max_length=20, blank=True, null=True, verbose_name='异常类型')
    progess = models.TextField(max_length=500, blank=True, null=True, verbose_name='解决进展')
    resaon = models.TextField(max_length=500, blank=True, null=True, verbose_name='未解决原因')
    end_time = models.DateTimeField(blank=True, null=True,  verbose_name='完结时间')
    priority = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return '{0}'.format(self.number)

    class Meta:
        verbose_name = '运单管理'
        verbose_name_plural = '运单管理'
        ordering = ['-priority', 'start_time']
        permissions = (
            ('change_detail', '只允许修改需求,用于客户帐号'),
            ('change_follower', '只允许修改跟进相关，用于跟单帐号'),
        )


class ExpressArchive(models.Model):
    number = models.BigIntegerField(unique=True, verbose_name='运单号')
    orig = models.CharField(max_length=200, verbose_name='发件网点')
    start_time = models.DateTimeField(auto_now_add=True, verbose_name='开单时间')
    status = models.CharField(max_length=50, verbose_name='运单状态')
    follower = models.CharField(max_length=200, verbose_name='跟进人')
    detail = models.TextField(max_length=1000, verbose_name='客户诉求')
    end_time = models.DateTimeField(blank=True, null=True,  verbose_name='完结时间')

    def __str__(self):
        return '{0}'.format(self.number)

    class Meta:
        verbose_name = '历史运单'
        verbose_name_plural = '历史运单'
        ordering = ['-end_time']
        permissions = (
            ('view', '查看'),
        )
        default_permissions = ('add', 'change', 'delete')