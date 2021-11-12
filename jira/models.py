from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Settings(models.Model):
    name = models.CharField('配置文件名称', max_length=40, null=True, unique=True,
                            help_text='40字符内。')
    url = models.URLField('Url', null=True, help_text='200字符内。')
    account = models.CharField('用户账号', max_length=40, null=True,
                               help_text='40字符内。')
    password_tips = models.CharField('用户密码', max_length=40, null=True, default='请输入密码',
                                     help_text='40字符内。该字段一直为"请输入密码"。若输入，则更改。')
    password = models.CharField('用户密码', max_length=40, null=True)
    mark = models.TextField('备注', null=True, blank=True)

    class Meta:
        # 数据库中表名称 默认app_表名
        # db_table = ''
        # Django Admin 中显示名名称
        verbose_name = '1 配置文件'  # 单数
        verbose_name_plural = '1 配置文件'  # 复数

    def __str__(self):
        return self.name


class SettingsToUsers(models.Model):
    name = models.CharField('授权规则名称', max_length=40, null=True, unique=True,
                            help_text='40字符内。')
    group_admin = models.ForeignKey(User, verbose_name='群组管理员', on_delete=models.CASCADE, null=True)
    group_mark = models.TextField('可管理群组列表', null=True,
                                  help_text='分隔符“,”，末尾必须有“,”')
    setting = models.ForeignKey(Settings, verbose_name='配置文件', on_delete=models.CASCADE, null=True)
    mark = models.TextField('备注', null=True, blank=True)

    class Meta:
        # 数据库中表名称 默认app_表名
        # db_table = ''
        # Django Admin 中显示名名称
        verbose_name = '2 配置文件授权'  # 单数
        verbose_name_plural = '2 配置文件授权'  # 复数

    def __str__(self):
        return self.name


class UserGroupOp(models.Model):
    group = models.CharField('群组', max_length=100, null=True)
    users = models.TextField('用户', null=True,
                             help_text='分隔符","。')
    operator = models.TextField('可查看人', null=True, blank=True,
                                help_text='仅超级管理员可更改，其他人不可更改。')
    status = models.BooleanField('操作状态', default=False)
    msg = models.TextField('操作消息', null=True)
    # settings_to_user = models.ForeignKey(SettingsToUsers, verbose_name='授权规则', on_delete=models.CASCADE, null=True)

    class Meta:
        # 数据库中表名称 默认app_表名
        # db_table = ''
        # Django Admin 中显示名名称
        verbose_name = '3 用户与群组操作'  # 单数
        verbose_name_plural = '3 用户与群组操作'  # 复数
