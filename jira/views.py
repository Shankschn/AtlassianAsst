import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from jira.jira import JiraDo
from jira.models import Settings
from tools import log


@csrf_exempt
def group_users_op(request):
    """
    群组用户操作（字符串） op： 1 群组添加用户 0 群组移除用户

    :param request:
    :return:
    """
    d = {'status': '0', 'msg': 'Please use POST method.', 'data': ''}
    if request.method == 'POST':
        log.i('API do POST')
        op = request.POST.get('op', None)
        group = request.POST.get('group', None)
        users = str(request.POST.get('users', None)).split(',')
        if '' in users:
            users.remove('')

        jira_url = request.POST.get('jira_url', None)
        jira_account = request.POST.get('jira_account', None)
        jira_password = request.POST.get('jira_password', None)
        log.i('{}, {}, {}, {}, {}, {}'.format(op, group, users, jira_url, jira_account, jira_password))
        jira_do = JiraDo()
        try:
            setting = Settings.objects.get(url=jira_url, account=jira_account, password=jira_password)
        except Exception as e:
            d['msg'] = '账号信息错误！'
            d['data'] = str(e)
        else:
            if op == '0':
                if not jira_do.login(setting.url, setting.account, setting.password):
                    msg = '{} 登录失败。'.format(setting.url)
                    log.i(msg)
                    d['msg'] = msg
                else:
                    st, errors = jira_do.group_remove_users(group, users)
                    if st:
                        d['status'] = True
                        msg = '群组 {} 移除用户 {}，成功。'.format(group, users)
                        log.i(msg)
                        d['msg'] = msg
                        d['data'] = st
                    else:
                        msg = '群组 {} 移除用户 {}，失败。'.format(group, users)
                        log.i(msg)
                        d['msg'] = msg
                        d['data'] = str(errors)
            elif op == '1':
                if not jira_do.login(setting.url, setting.account, setting.password):
                    msg = '{} 登录失败。'.format(setting.url)
                    log.i(msg)
                    d['msg'] = msg
                else:
                    st, errors = jira_do.group_add_users(group, users)
                    if st:
                        d['status'] = True
                        msg = '群组 {} 添加用户 {}，成功。'.format(group, users)
                        log.i(msg)
                        d['msg'] = msg
                        d['data'] = st
                    else:
                        msg = '群组 {} 添加用户 {}，失败。'.format(group, users)
                        log.i(msg)
                        d['msg'] = msg
                        d['data'] = str(errors)
            else:
                msg = '未知的操作 op: {}'.format(op)
                log.i(msg)
                d['msg'] = msg
        d = json.dumps(d)
        return HttpResponse(d, content_type="application/json,charset=utf-8")
