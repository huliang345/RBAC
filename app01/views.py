from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from . import models
import re


# class MenuHelper(object):
#     def __init__(self, username, current_url):
#         self.permission2action_list = None
#         self.result = None
#         self.username = username
#         self.current_url = current_url
#         self.init_data()
#
#     def init_data(self):
#         # 方式一：user2role_list
#         # user_obj = models.User.objects.get(username=username)
#         # user2role_list = models.User2Role.objects.filter(u=user_obj)
#         # 方式二：role_list
#         # user_obj = models.User.objects.get(username=username)
#         # role_list=models.Role.objects.filter(user2role__u=user_obj)
#         # 方式三：role_list
#         role_list = models.Role.objects.filter(user2role__u__username=self.username)
#         # print(role_list)  # <QuerySet [<Role: 搬砖者>, <Role: 按摩>, <Role: 技师>]>
#         # v = models.Permission2Action2Role.objects.filter(r__in=role_list)
#         # print(v)
#
#         # 获取用户的所有权限，放在session中，缺点：不能实时更新权限信息，需要重新登陆
#         permission2action_list = models.Permission2Action.objects.filter(
#             permission2action2role__r__in=role_list).values(
#             'p__url', 'a__code').distinct()
#         self.permission2action_list = permission2action_list
#         # 获取所有种的url：
#         # url_list = models.Permission2Action.objects.filter(permission2action2role__r__in=role_list).values(
#         #     'p__url', 'p__caption').distinct()
#
#         # 判断所有种url中有菜单的部分：
#         menu_leaf_list = models.Permission2Action.objects.filter(permission2action2role__r__in=role_list).exclude(
#             p__menu__isnull=True).values(
#             'p_id', 'p__url', 'p__caption', 'p__menu').distinct()
#         # for i in menu_leaf_list:
#         #     print(i)
#         # {'p_id': 3, 'p__url': '/report.html', 'p__caption': '报表管理', 'p__menu': 4}
#         # {'p_id': 4, 'p__url': '/girl.html', 'p__caption': '姑娘管理', 'p__menu': 6}
#         # {'p_id': 2, 'p__url': '/order.html', 'p__caption': '订单管理', 'p__menu': 6}
#         menu_leaf_dict = {}
#         open_leaf_parent_id = None
#         for item in menu_leaf_list:
#             item = {
#                 'id': item['p_id'],
#                 'url': item['p__url'],
#                 'caption': item['p__caption'],
#                 'parent_id': item['p__menu'],
#                 'child': [],
#                 'status': True,
#                 'open': False
#             }
#             if item['parent_id'] in menu_leaf_dict:
#                 menu_leaf_dict[item['parent_id']].append(item)
#             else:
#                 menu_leaf_dict[item['parent_id']] = [item, ]
#             import re
#             if re.match(item['url'], self.current_url):
#                 item['open'] = True
#                 open_leaf_parent_id = item['parent_id']
#
#         # 将菜单获取：
#         menu_list = models.Menu.objects.values('id', 'parent_id', 'caption')
#         menu_dict = {}
#         for item in menu_list:
#             item['child'] = []
#             item['status'] = False
#             item['open'] = False
#             menu_dict[item['id']] = item
#         for k, v in menu_leaf_dict.items():
#             menu_dict[k]['child'] = v
#             # menu_dict[k]['status'] = True
#             parent_id = k
#             while parent_id:
#                 menu_dict[parent_id]['status'] = True
#                 parent_id = menu_dict[parent_id]['parent_id']
#         while open_leaf_parent_id:
#             menu_dict[open_leaf_parent_id]['open'] = True
#             open_leaf_parent_id = menu_dict[open_leaf_parent_id]['parent_id']
#         result = []
#         for row in menu_dict.values():
#             if not row['parent_id']:
#                 result.append(row)
#             else:
#                 menu_dict[row['parent_id']]['child'].append(row)
#         # for i in result:
#         #     print(i)
#         self.result = result
#
#     def menu_content(self, child_list):  # 递归完成对子代的添加
#         active = ''
#         tpl = """
#                    <div class="item %s">
#                        <div class="title">%s</div>
#                        <div class="content">%s</div>
#                    </div>
#                """
#         response = ''
#         for row in child_list:
#             if not row['status']:
#                 continue
#             if row['open']:
#                 active = 'active'
#             if 'url' in row:
#                 response += '<a class="%s" href="%s">%s</a>' % (active, row['url'], row['caption'],)
#             else:
#                 title = row['caption']
#                 content = self.menu_content(row['child'])
#                 response += tpl % (active, title, content)
#         return response
#
#     def menu_tree(self):  # 生成菜单树函数
#         tpl = """
#                <div class="item %s">
#                    <div class="title">%s</div>
#                    <div class="content">%s</div>
#                </div>
#            """
#         response = ''
#         for row in self.result:
#             active = ''
#             if not row['status']:
#                 continue
#             if row['open']:
#                 active = 'active'
#             title = row['caption']
#             content = self.menu_content(row['child'])
#             response += tpl % (active, title, content,)
#         return response


# def login(request):
#     # 注意这里没有做登陆
#     user_request_url = '/order.html'
#     username = request.GET.get('u')
#     obj = MenuHelper(username, user_request_url)
#     # obj.permission2action_list  # 应放在session中的权限列表
#     # obj.result  # 树状菜单数据集合
#     string = obj.menu_tree()
#     return render(request, 'index.html', {'menu_string': string})

# 帮助生成相应权限菜单的类：
class MenuHelper(object):
    def __init__(self, request, username):
        # 获取请求对象request：
        self.request = request
        # 用户名：
        self.username = username
        # 用以判断的url，主要是判断是否折叠：
        self.current_url = request.path_info
        # 事先建立接收所有权限的变量:
        self.permission2action_dict = None
        # 事先建立接收所有leaf的变量：
        self.menu_leaf_list = None
        # 事先建立接收所有菜单的变量：
        self.menu_list = None
        # 初始化时需要做的事情：主要是登陆时把用户权限放入session中
        self.session_data()

    # 生成权限数据并将权限放入session，如果有就直接放
    def session_data(self):
        permission_dict = self.request.session.get('permission_info')
        if permission_dict:
            self.permission2action_dict = permission_dict['permission2action_dict']
            self.menu_leaf_list = permission_dict['menu_leaf_list']
            self.menu_list = permission_dict['menu_list']
        else:
            # 获取当前用户的角色列表：
            role_list = models.Role.objects.filter(user2role__u__username=self.username)  # 反向查询用表名
            # 获取对应角色的权限：
            permission2action_list = models.Permission2Action.objects.filter(
                permission2action2role__r__in=role_list).values('p__url', 'a__code').distinct()
            # print(permission2action_list)
            # < QuerySet[{'p__url': '/report.html', 'a__code': 'get'}, {'p__url': '/girl.html', 'a__code': 'post'}, {
            #     'p__url': '/girl.html', 'a__code': 'put'}, {'p__url': '/girl.html', 'a__code': 'get'}, {
            #                'p__url': '/order.html', 'a__code': 'get'}] >

            # 转化数据结构成{'/report.html': ['get'], '/girl.html': ['post', 'put', 'get'], '/order.html': ['get']}
            permission2action_dict = {}
            for item in permission2action_list:
                if item['p__url'] in permission2action_dict:
                    permission2action_dict[item['p__url']].append(item['a__code'])
                else:
                    permission2action_dict[item['p__url']] = [item['a__code'], ]
            # print(permission2action_dict)
            # {'/report.html': ['get'], '/girl.html': ['post', 'put', 'get'], '/order.html': ['get']}

            # 获取leaf列表：就是在menu中显示的权限
            menu_leaf_list = list(
                models.Permission2Action.objects.filter(permission2action2role__r__in=role_list).exclude(
                    p__menu__isnull=True).values('p_id', 'p__url', 'p__caption', 'p__menu').distinct())
            # print(menu_leaf_list)
            # menu_leaf_list1 = models.Permission.objects.filter(url__in=permission2action_dict).values('id', 'url',
            #                                                                                          'caption',
            #                                                                                          'menu').exclude(
            #     menu__isnull=True)
            # print(menu_leaf_list1)
            menu_list = list(models.Menu.objects.values('id', 'caption', 'parent_id'))
            # 放入session：
            self.request.session['permission_info'] = {
                'permission2action_dict': permission2action_dict,
                'menu_leaf_list': menu_leaf_list,
                'menu_list': menu_list,
            }

    # 构造理想的树形菜单数据：
    def menu_data_list(self):
        menu_leaf_dict = {}
        open_leaf_parent_id = None
        # 构建self.menu_leaf_list的新的好用的数据结构menu_leaf_dict
        for item in self.menu_leaf_list:
            # menu_leaf_list=[{'p_id': 3, 'p__url': '/report.html', 'p__caption': '报表管理', 'p__menu': 4}, {'p_id': 4, 'p__url': '/girl.html', 'p__caption': '姑娘管理', 'p__menu': 6}, {'p_id': 1, 'p__url': '/index.html', 'p__caption': '用户管理', 'p__menu': 7}]

            item = {
                'id': item['p_id'],
                'url': item['p__url'],
                'caption': item['p__caption'],
                'parent_id': item['p__menu'],
                'child': [],
                'status': True,  # 是否显示
                'open': False,  # 是否展开
            }
            if item['parent_id'] in menu_leaf_dict:
                menu_leaf_dict[item['parent_id']].append(item)
            else:
                menu_leaf_dict[item['parent_id']] = [item, ]
                # menu_leaf_dict=｛parent_id(12):[item1,item2...],parent_id(13):[item3,item4...]｝
            if re.match(item['url'], self.current_url):
                item['open'] = True
                open_leaf_parent_id = item['parent_id']
        # 用menu_list构建好用的menu_dict字典：
        menu_dict = {}
        for item in self.menu_list:
 # menu_list= [{'id': 1, 'caption': '菜单1', 'parent_id': None}, {'id': 2, 'caption': '菜单2', 'parent_id': None}, {'id': 3, 'caption': '菜单3', 'parent_id': None}, {'id': 4, 'caption': '菜单1.1', 'parent_id': 1}, {'id': 5, 'caption': '菜单1.2', 'parent_id': 1}, {'id': 6, 'caption': '菜单1.2.1', 'parent_id': 5}, {'id': 7, 'caption': '菜单1.2.2', 'parent_id': 5}]
            item['child'] = []
            item['status'] = False
            item['open'] = False
            menu_dict[item['id']] = item
            # menu_dict={1:{'id': 1, 'caption': '菜单1', 'parent_id': None,'child':[],'status':False,'open':False},...}
        # 将leaf节点挂在父节点的child里：
        for k, v in menu_leaf_dict.items():
            # menu_leaf_dict=｛parent_id(12):[item1,item2...],parent_id(13):[item3,item4...]｝
            menu_dict[k]['child'] = v
            parent_id = k
            # 遍历父代让其status=True,意为有权限的就显示，没的就不显示
            while parent_id:
                menu_dict[parent_id]['status'] = True
                parent_id = menu_dict[parent_id]['parent_id']
        # 将open_leaf_parent_id（存的是选中的leaf的父id）的menu的open置True，并遍历其父并置True
        while open_leaf_parent_id:
            menu_dict[open_leaf_parent_id]['open'] = True
            open_leaf_parent_id = menu_dict[open_leaf_parent_id]['parent_id']
        # 生成树形结构数据，放入变量result：
        result = []
        for row in menu_dict.values():
            # menu_dict={1:{'id': 1, 'caption': '菜单1', 'parent_id': None,'child':[],'status':False,'open':False},...}
            if not row['parent_id']:
                result.append(row)
                # [{'id': 1, 'caption': '菜单1', 'parent_id': None,'child':[],'status':False,'open':False},....]
            else:
                menu_dict[row['parent_id']]['child'].append(row)
        return result

    # 将子代都构造成字符串：
    def menu_content(self, child_list):
        response = ''
        tpl = """
                    <div class="item %s">
                        <div class="title">%s</div>
                        <div class="content">%s</div>
                    </div>
                """
        for row in child_list:
            if not row['status']:
                continue
            active = ""
            if row['open']:
                active = "active"
            if 'url' in row:
                response += "<a class='%s' href='%s'>%s</a>" % (active, row['url'], row['caption'],)
            else:
                title = row['caption']
                content = self.menu_content(row['child'])
                response += tpl % (active, title, content)
        return response

    # 生成菜单树，并能显示在页面，也就是字符串的html
    def menu_tree(self):
        response = ''
        tpl = """
            <div class="item %s">
                <div class="title">%s</div>
                <div class="content">%s</div>
            </div>
        """
        for row in self.menu_data_list():
            if not row['status']:
                continue
            active = ''
            if row['open']:
                active = 'active'
            title = row['caption']
            content = self.menu_content(row['child'])
            response += tpl % (active, title, content)
        return response

    # 获取当前url的具体权限：
    def actions(self):
        action_list = []
        for k, v in self.permission2action_dict.items():
            # print(permission2action_dict)
            # {'/report.html': ['get'], '/girl.html': ['post', 'put', 'get'], '/order.html': ['get']}
            if re.match(k, self.current_url):
                action_list = v
                break
        return action_list


# 登陆：
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        obj = models.User.objects.filter(username=username, password=pwd).first()
        if obj:
            # 登陆成功后在session中放置用户信息
            request.session['user_info'] = {'nid': obj.id, 'username': obj.username}
            # 获取用户所有权限
            # 获取用户所有菜单
            # 获取在菜单上的权限，也就是leaf
            # 把权限放在session中用以判断是否具有权限
            MenuHelper(request, obj.username)
            test_leaf(obj.username)
            return redirect('/index.html')
        else:
            return redirect('/login.html')


# 退出：
def logout(request):
    request.session.clear()
    return redirect('/login.html')


# 验证是否登陆：
def permission(func):
    def inner(request, *args, **kwargs):
        user_info = request.session.get('user_info')
        if not user_info:
            return redirect('/login.html')
        obj = MenuHelper(request, user_info['username'])
        action_list = obj.actions()
        # 当前url的动作列表
        if not action_list:
            return HttpResponse('无权限访问')
        kwargs['action_list'] = action_list
        kwargs['menu_string'] = obj.menu_tree()
        return func(request, *args, **kwargs)

    return inner


# 后台管理主页：
@permission
def index(request, *args, **kwargs):
    action_list = kwargs.get('action_list')
    menu_string = kwargs.get('menu_string')
    if 'GET' in action_list:
        result = models.User.objects.all()
    else:
        result = []
    return render(request, 'index.html', {
        'action_list': action_list,
        'menu_string': menu_string,
    })


def test_leaf(username):
    role_list = models.Role.objects.filter(user2role__u__username=username)
    menu_leaf_list = list(
        models.Permission2Action.objects.filter(permission2action2role__r__in=role_list).exclude(
            p__menu__isnull=True).values('p_id', 'p__url', 'p__caption', 'p__menu').distinct())
    print(menu_leaf_list)
    # [{'p_id': 3, 'p__url': '/report.html', 'p__caption': '报表管理', 'p__menu': 4}, {'p_id': 4, 'p__url': '/girl.html', 'p__caption': '姑娘管理', 'p__menu': 6}, {'p_id': 1, 'p__url': '/index.html', 'p__caption': '用户管理', 'p__menu': 7}]
    menu_list = list(models.Menu.objects.values('id', 'caption', 'parent_id'))
    print(menu_list)
    # menu_list= [{'id': 1, 'caption': '菜单1', 'parent_id': None}, {'id': 2, 'caption': '菜单2', 'parent_id': None}, {'id': 3, 'caption': '菜单3', 'parent_id': None}, {'id': 4, 'caption': '菜单1.1', 'parent_id': 1}, {'id': 5, 'caption': '菜单1.2', 'parent_id': 1}, {'id': 6, 'caption': '菜单1.2.1', 'parent_id': 5}, {'id': 7, 'caption': '菜单1.2.2', 'parent_id': 5}]