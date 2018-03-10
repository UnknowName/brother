# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required

from express.forms import FileForm
from express.models import Express
from express.paginator import split_page
from express.utils import read_excel, to_datetime, to_unicode

import time
from xpinyin import Pinyin

@login_required(login_url='/accounts/login/')
def data_import(request):
    time.clock()
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['filename']
            if not excel_file.name.endswith(('xls', 'xlsx')):
                return HttpResponse(u'请上传EXCEL文件!')
            gener = read_excel(excel_file.read())
            next(gener)
            for datas in gener:
                unicode_datas = [ to_unicode(data) for data in datas ]
                num, start_time, orig, follower_firstname, status = unicode_datas
                # Get the User Object,If not have the user,Create user and set
                # default Password
                try:
                    follower = User.objects.get(first_name=follower_firstname)
                except User.DoesNotExist:
                    pinyin = Pinyin()
                    username = pinyin.get_pinyin(follower_firstname.decode('utf8'), '')
                    follower = User.objects.create(
                        username=username, is_staff=True, is_active=True,
                        first_name=follower_firstname
                    )
                    follower.set_password(username)
                    perm = Group.objects.get(name=u'跟单权限')
                    follower.groups = [perm]
                    follower.save()
                try:
                    number = Express(
                        number=num,orig=orig, follower=follower, status=status
                    )
                    number.save()
                    number.start_time = to_datetime(start_time)
                    number.save()
                except Exception as e:
                    _, err_info = e
                    print err_info
                    return HttpResponse('%s %s' %('Import Failed:', err_info))
        process_time = str(time.clock()).encode('utf8')
        return HttpResponse(u'导入数据成功，共花费时间' + process_time + u'秒')
    else:
        form = FileForm()
    return render(request, 'import.html', locals())


@login_required(login_url='/accounts/login/')
def change_follower(request):
    if request.method == 'POST':
        numbers = request.POST.getlist('numbers')
        users = request.POST.getlist('user')
        if numbers and users:
            query = Express.objects
            try:
                user = User.objects.get(first_name=users[0])
            except User.DoesNotExist:
                user = User.objects.get(username=users[0])
            for number in numbers:
                express = query.get(number=number)
                express.follower = user
                express.save()
            return HttpResponse('Change Suceess!')
        return HttpResponse('Please select number and user!')
    else:
        users = User.objects.filter(is_superuser=0)
        expresses = Express.objects.all()
        numbers = split_page(request, expresses)
        return render(request, 'change.html', locals())
