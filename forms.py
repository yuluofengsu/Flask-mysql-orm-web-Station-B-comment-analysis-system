from flask_admin.contrib.sqla import ModelView



# 自定义模型视图
class userModelView(ModelView):
    column_list = ('id','email', 'password','role')
    # 【搜索框】---过滤的字段名
    column_searchable_list = ('email',)
    # 设置分页大小
    page_size = 10
class upinfoModelView(ModelView):
    column_list = ('id','mid', 'upName','fensi','avatar','level', 'upVideoLen','sign')
    # 【搜索框】---过滤的字段名
    column_searchable_list = ('upName',)
    # 设置分页大小
    page_size = 10
class videolistModelView(ModelView):
    column_list = ('id','title','bvid','videoLen', 'videoId','avatar','seeNum','mid', 'created')
    # 【搜索框】---过滤的字段名
    column_searchable_list = ('title',)
    # 设置分页大小
    page_size = 10
class videocommentsModelView(ModelView):
    column_list = ('id','videoId', 'uname','avatar','content','sex', 'likes','created','vipLen')
    # 【搜索框】---过滤的字段名
    column_searchable_list = ('uname',)
    # 设置分页大小
    page_size = 10
