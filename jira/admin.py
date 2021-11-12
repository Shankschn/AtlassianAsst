from django.contrib import admin, messages

# Register your models here.
from .jira import JiraDo
from .models import *
from tools import log

admin.site.site_title = 'Atlassian 助手'
admin.site.site_header = 'Atlassian 助手'
admin.site.index_title = 'Atlassian 助手'


def is_super_admin(request):
    if request.user.is_superuser:
        log.i('{} is superuser.'.format(request.user))
        return True
    else:
        log.i('{} is not superuser.'.format(request.user))
        return False


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    search_fields = ['name']
    exclude = ['password']
    pass

    def save_model(self, request, obj, form, change):
        if obj.password_tips != '请输入密码':
            obj.password = obj.password_tips
            obj.password_tips = '请输入密码'
        obj.save()


@admin.register(SettingsToUsers)
class SettingsToUsersAdmin(admin.ModelAdmin):
    search_fields = ['name']

    autocomplete_fields = ['group_admin', 'setting']

    pass


@admin.register(UserGroupOp)
class UserGroupOpAdmin(admin.ModelAdmin):
    list_display = ['id', 'group', 'users', 'status', 'msg', 'operator']
    readonly_fields = ['status', 'msg']
    # exclude = ['operator']
    # autocomplete_fields = ['settings_to_user']
    actions = [
        'action_group_add_users',
        'action_group_remove_users',
    ]

    def save_model(self, request, obj, form, change):
        msg = ''

        if not change:
            obj.operator = '{},'.format(request.user)

        if change:
            if not is_super_admin(request):
                old = UserGroupOp.objects.get(pk=obj.pk)
                if obj.operator != old.operator:
                    obj.operator = old.operator
                    msg = '无权修改 operator。'
                    messages.info(request, msg)

        obj.msg = msg
        obj.save()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        log.i('in UserGroupOpAdmin get_queryset')
        if is_super_admin(request):
            return qs
        else:
            return qs.filter(operator__contains='{},'.format(request.user))

    def action_group_add_users(self, request, queryset):
        log.i('in UserGroupOpAdmin action_group_add_users')
        for q in queryset:
            status = False
            msg = ''
            configs = SettingsToUsers.objects.filter(group_admin=request.user)
            if configs:
                for config in configs:
                    if '{},'.format(q.group) not in config.group_mark:
                        msg = '{} 不在 {} 中'.format(q.group, config.group_mark)
                        log.i(msg)
                    else:
                        msg = '{} 在 {} 中'.format(q.group, config.group_mark)
                        log.i(msg)
                        jira = JiraDo()
                        setting = config.setting
                        if not jira.login(setting.url, setting.account, setting.password):
                            msg = '{} 登录失败。'.format(setting.url)
                            log.i(msg)
                            messages.error(request, msg)
                        else:
                            users = q.users.split(',')
                            if '' in users:
                                users.remove('')
                            st, errors = jira.group_add_users(q.group, users)
                            if st:
                                status = True
                                msg = '群组 {} 添加用户 {}，成功。'.format(q.group, q.users)
                                log.i(msg)
                                messages.success(request, msg)
                            else:
                                status = False
                                msg = '群组 {} 添加用户 {}，失败。'.format(q.group, q.users)
                                log.i(msg)
                                log.i(str(errors))
                                messages.error(request, msg)
                                msg = errors
                        break
            else:
                msg = '{} 不是群组管理员，无权限进行此操作。'.format(request.user)
                log.i(msg)
                messages.error(request, '你不是群组管理员，无权限进行此操作。')
            messages.info(request, '执行完成。若有错误，请查看消息。')
            q.status = status
            q.msg = msg
            q.save()

    action_group_add_users.short_description = '群组添加用户'

    def action_group_remove_users(self, request, queryset):
        log.i('in UserGroupOpAdmin action_group_remove_users')
        for q in queryset:
            status = False
            msg = ''
            configs = SettingsToUsers.objects.filter(group_admin=request.user)
            if configs:
                for config in configs:
                    if '{},'.format(q.group) not in config.group_mark:
                        msg = '{} 不在 {} 中'.format(q.group, config.group_mark)
                        log.i(msg)
                    else:
                        msg = '{} 在 {} 中'.format(q.group, config.group_mark)
                        log.i(msg)
                        jira = JiraDo()
                        setting = config.setting
                        if not jira.login(setting.url, setting.account, setting.password):
                            msg = '{} 登录失败。'.format(setting.url)
                            log.i(msg)
                            messages.error(request, msg)
                        else:
                            users = q.users.split(',')
                            if '' in users:
                                users.remove('')
                            st, errors = jira.group_remove_users(q.group, users)
                            if st:
                                status = True
                                msg = '群组 {} 移除用户 {}，成功。'.format(q.group, q.users)
                                log.i(msg)
                                messages.success(request, msg)
                            else:
                                status = False
                                msg = '群组 {} 移除用户 {}，失败。'.format(q.group, q.users)
                                log.i(msg)
                                log.i(str(errors))
                                messages.error(request, msg)
                                msg = errors
                        break
            else:
                msg = '{} 不是群组管理员，无权限进行此操作。'.format(request.user)
                log.i(msg)
                messages.error(request, '你不是群组管理员，无权限进行此操作。')
            messages.info(request, '执行完成。若有错误，请查看消息。')
            q.status = status
            q.msg = msg
            q.save()

    action_group_remove_users.short_description = '群组移除用户'


