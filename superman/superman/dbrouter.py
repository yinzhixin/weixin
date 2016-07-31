#coding: utf-8


class BlogRouter(object):
    """指定blog应用操作某个数据库的路由"""

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'blog':
            return 'test'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'blog':
            return 'test'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'blog' or obj2._meta.app_label == 'blog':
            return True
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        if app_label == 'blog':
            return db == 'blog'
        return None

class WechatRouter(object):
    """指定wechat应用操作某个数据库的路由"""

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'wechat':
            return 'test'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'wechat':
            return 'test'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'wechat' or obj2._meta.app_label == 'wechat':
            return True
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        if app_label == 'wechat':
            return db == 'wechat'
        return None
