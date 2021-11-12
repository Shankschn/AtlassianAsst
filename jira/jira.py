from atlassian import Jira
from tools import log
from .models import *


class JiraDo:

    def __init__(self):
        self.url = None
        self.account = None
        self.password = None
        self.obj = None

    def login(self, url, account, password):
        self.url = url
        self.account = account
        self.password = password
        obj = False
        try:
            obj = Jira(url=self.url, username=self.account, password=self.password)
        except Exception as e:
            log.i(e)
        else:
            self.obj = obj
            log.i(obj)
        return obj

    def group_add_user(self, group, user):
        has_error = False
        try:
            obj = self.obj.add_user_to_group(user, group)
        except Exception as e:
            log.i(e)
            has_error = e
        else:
            log.i(obj)
        finally:
            return has_error

    def group_add_users(self, group, users):
        errors = {}
        if not isinstance(users, list):
            has_error = self.group_add_user(group, users)
            if has_error:
                errors[users] = has_error
        else:
            for user in users:
                has_error = self.group_add_user(group, user)
                if has_error:
                    errors[user] = has_error
        if errors:
            log.i(errors)
            return False, errors
        else:
            log.i(True)
            return True, errors

    def group_remove_user(self, group, user):
        has_error = False
        try:
            obj = self.obj.remove_user_from_group(user, group)
        except Exception as e:
            log.i(e)
            has_error = e
        else:
            log.i(obj)
        finally:
            return has_error

    def group_remove_users(self, group, users):
        errors = {}
        if not isinstance(users, list):
            has_error = self.group_remove_user(group, users)
            if has_error:
                errors[users] = has_error
        else:
            for user in users:
                has_error = self.group_remove_user(group, user)
                if has_error:
                    errors[user] = has_error
        if errors:
            log.i(errors)
            return False, errors
        else:
            log.i(True)
            return True, errors


def group_admin_permission_check(user, ):
    pass


