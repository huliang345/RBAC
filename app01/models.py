from django.db import models


class User(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = '用户表'  # 在admin里显示表名

    def __str__(self):
        return self.username


class Role(models.Model):
    caption = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = '角色表'  # 在admin里显示表名

    def __str__(self):
        return self.caption


class User2Role(models.Model):
    u = models.ForeignKey(User, on_delete=models.CASCADE)
    r = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '用户分配角色'  # 在admin里显示表名

    def __str__(self):
        return '%s-%s' % (self.u.username, self.r.caption,)


class Menu(models.Model):
    caption = models.CharField(max_length=32)
    parent = models.ForeignKey('self', related_name='p', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '菜单'

    def __str__(self):
        return self.caption


class Permission(models.Model):
    caption = models.CharField(max_length=32)
    url = models.CharField(max_length=64)
    menu = models.ForeignKey(Menu, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'URL表'  # 在admin里显示表名

    def __str__(self):
        return '%s-%s' % (self.caption, self.url,)


class Action(models.Model):
    caption = models.CharField(max_length=32)
    code = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = '操作表'  # 在admin里显示表名

    def __str__(self):
        return self.caption


class Permission2Action(models.Model):
    p = models.ForeignKey(Permission, on_delete=models.CASCADE)
    a = models.ForeignKey(Action, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '权限表'  # 在admin里显示表名

    def __str__(self):
        return '%s-%s:-%s?t=%s' % (self.p.caption, self.a.caption, self.p.url, self.a.code,)


class Permission2Action2Role(models.Model):
    p2a = models.ForeignKey(Permission2Action, on_delete=models.CASCADE)
    r = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '角色分配权限'  # 在admin里显示表名

    def __str__(self):
        return '%s==>%s' % (self.r.caption, self.p2a,)
