from django.db import models


class BaseTable(models.Model):
    """
    公共字段列
    """

    class Meta:
        abstract = True
        verbose_name = "公共字段表"
        db_table = 'BaseTable'

    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)


class Project(BaseTable):
    """
    项目信息表
    """

    class Meta:
        verbose_name = "项目信息"
        db_table = "Project"

    name = models.CharField("项目名称", unique=True, null=False, max_length=100)
    desc = models.CharField("简要介绍", max_length=100, null=False)
    responsible = models.CharField("创建人", max_length=20, null=False)


class Config(BaseTable):
    """
    环境信息表
    """

    class Meta:
        verbose_name = "环境信息"
        db_table = "Config"

    name = models.CharField("环境名称", null=False, max_length=100)
    body = models.TextField("主体信息", null=False)
    base_url = models.CharField("请求地址", null=False, max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class API(BaseTable):
    """
    API信息表
    """

    class Meta:
        verbose_name = "接口信息"
        db_table = "API"

    name = models.CharField("接口名称", null=False, max_length=100)
    body = models.TextField("主体信息", null=False)
    url = models.CharField("请求地址", null=False, max_length=200)
    method = models.CharField("请求方式", null=False, max_length=10)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    relation = models.IntegerField("节点id", null=False)


class Case(BaseTable):
    """
    用例信息表
    """

    class Meta:
        verbose_name = "用例信息"
        db_table = "Case"

    tag = (
        (1, "冒烟用例"),
        (2, "集成用例"),
        (3, "监控脚本")
    )
    name = models.CharField("用例名称", null=False, max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    relation = models.IntegerField("节点id", null=False)
    length = models.IntegerField("API个数", null=False)
    tag = models.IntegerField("用例标签", choices=tag, default=2)


class CaseStep(BaseTable):
    """
    Test Case Step
    """

    class Meta:
        verbose_name = "用例信息 Step"
        db_table = "CaseStep"

    name = models.CharField("用例名称", null=False, max_length=100)
    body = models.TextField("主体信息", null=False)
    url = models.CharField("请求地址", null=False, max_length=200)
    method = models.CharField("请求方式", null=False, max_length=10)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    step = models.IntegerField("顺序", null=False)


class HostIP(BaseTable):
    """
    环境域名
    """

    class Meta:
        verbose_name = "HOST配置"
        db_table = "HostIP"

    name = models.CharField(null=False, max_length=20, unique=True, help_text="环境名称")
    hostInfo = models.TextField(null=False, help_text="环境详情")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, help_text="所属项目")


class Variables(BaseTable):
    """
    全局变量
    """

    class Meta:
        verbose_name = "全局变量"
        db_table = "Variables"

    key = models.CharField(null=False, max_length=100)
    value = models.CharField(null=False, max_length=1024)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Report(BaseTable):
    """
    报告存储
    """
    report_type = (
        (1, "调试"),
        (2, "异步"),
        (3, "定时")
    )

    class Meta:
        verbose_name = "测试报告"
        db_table = "Report"

    name = models.CharField("报告名称", null=False, max_length=100)
    type = models.IntegerField("报告类型", choices=report_type)
    summary = models.TextField("主体信息", null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Relation(models.Model):
    """
    树形结构关系
    """

    class Meta:
        verbose_name = "树形结构关系"
        db_table = "Relation"

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    tree = models.TextField("结构主题", null=False, default=[])
    type = models.IntegerField("树类型", default=1)


class ModelWithFileField(BaseTable):
    """
    文件信息表
    """
    class Meta:
        verbose_name = "文件信息表"
        db_table = "FileInfo"
        unique_together = [['project', 'name']]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to='testdatas', unique=True, null=True, blank=True)


class Pycode(BaseTable):
    """
    驱动文件表
    """

    class Meta:
        verbose_name = "驱动文件库"
        db_table = "pycodeFile"
        unique_together = [['project', 'name']]

    code = models.TextField("python代码", default="# _*_ coding:utf-8 _*_", null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=False)
    desc = models.CharField("简要介绍", max_length=100, null=True, blank=True)
