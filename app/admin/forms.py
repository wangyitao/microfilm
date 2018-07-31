# -*- coding: utf-8 -*-
# @Author : Felix Wang
# @time   : 2018/7/9 21:51

# 表单处理文件

from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, PasswordField, SubmitField, TextAreaField, FileField, SelectField, \
    SelectMultipleField  # 导入需要的字段
from wtforms.validators import DataRequired, ValidationError, EqualTo

from app.models import Admin, Tag, Auth, Role


# 登录表单
class LoginForm(FlaskForm):
    """
    管理员登录表单
    """
    account = StringField(
        label="账号",  # 标签
        validators=[
            DataRequired('请输入账号')
        ],  # 验证器
        description='账号',  # 描述
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入账号！',
            'required': 'required',
        },  # 附加选项
    )
    pwd = PasswordField(
        label="密码",  # 标签
        validators=[
            DataRequired('请输入密码')
        ],  # 验证器
        description='密码',  # 描述
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入密码！',
            'required': 'required',
        },  # 附加选项
    )

    submit = SubmitField(
        '登录',
        render_kw={
            'class': 'btn btn-primary btn-block btn-flat',
        }
    )

    # 自定义账号验证
    def validate_account(self, field):
        account = field.data
        admin = Admin.query.filter_by(name=account).count()
        if admin == 0:
            raise ValidationError('账号不存在！')


# 标签表单
class TagForm(FlaskForm):
    # input
    name = StringField(
        label="名称",
        validators=[
            DataRequired("标签名不能为空")
        ],
        description="标签",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入标签名称！"
        }
    )
    # 按钮
    submit = SubmitField(
        '编辑',
        render_kw={
            "class": "btn btn-primary",
        }
    )


# 电影表单，表单都是按照数据表对照的写
class MovieForm(FlaskForm):
    title = StringField(
        label="片名",
        validators=[
            DataRequired("片名不能为空！")
        ],
        description="片名",
        render_kw={
            "class": "form-control",
            "id": "input_title",
            "placeholder": "请输入片名！"
        }
    )
    url = FileField(
        label="文件",
        validators=[
            DataRequired("请上传文件！")
        ],
        description="文件",
    )
    info = TextAreaField(
        label="简介",
        validators=[
            DataRequired("简介不能为空！")
        ],
        description="简介",
        render_kw={
            "class": "form-control",
            "rows": 10
        }
    )
    logo = FileField(
        label="封面",
        validators=[
            DataRequired("请上传封面！")
        ],
        description="封面",
    )

    star = SelectField(
        label="星级",
        validators=[
            DataRequired("请选择星级！")
        ],
        # star的数据类型
        coerce=int,
        choices=[(1, "1星"), (2, "2星"), (3, "3星"), (4, "4星"), (5, "5星")],
        description="星级",
        render_kw={
            "class": "form-control",
        }
    )
    # 标签要在数据库中查询已存在的标签
    tag_id = SelectField(
        label="标签",
        validators=[
            DataRequired("请选择标签！")
        ],
        coerce=int,
        # 通过列表生成器生成列表
        choices=[(v.id, v.name) for v in Tag.query.all()],
        description="标签",
        render_kw={
            "class": "form-control",
        }
    )
    area = StringField(
        label="地区",
        validators=[
            DataRequired("请输入地区！")
        ],
        description="地区",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入地区！"
        }
    )
    length = StringField(
        label="片长",
        validators=[
            DataRequired("片长不能为空！")
        ],
        description="片长",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入片长！"
        }
    )
    release_time = StringField(
        label="上映时间",
        validators=[
            DataRequired("上映时间不能为空！")
        ],
        description="上映时间",
        render_kw={
            "class": "form-control",
            "placeholder": "请选择上映时间！",
            "id": "input_release_time"
        }
    )
    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary",
        }
    )


# 电影预告
class PreviewForm(FlaskForm):
    title = StringField(
        label="预告标题",
        validators=[
            DataRequired("预告标题不能为空！")
        ],
        description="预告标题",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入预告标题！"
        }
    )
    logo = FileField(
        label="预告封面",
        validators=[
            DataRequired("预告封面不能为空！")
        ],
        description="预告封面",
    )
    submit = SubmitField(
        '编辑',
        render_kw={
            "class": "btn btn-primary",
        }
    )


class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label="旧密码",
        validators=[
            DataRequired("旧密码不能为空！")
        ],
        description="旧密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入旧密码！",
        }
    )
    new_pwd = PasswordField(
        label="新密码",
        validators=[
            DataRequired("新密码不能为空！")
        ],
        description="新密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入新密码！",
        }
    )
    submit = SubmitField(
        '编辑',
        render_kw={
            "class": "btn btn-primary",
        }
    )

    def validate_old_pwd(self, field):
        from flask import session
        pwd = field.data
        name = session["admin"]
        admin = Admin.query.filter_by(
            name=name
        ).first()
        if not admin.check_pwd(pwd):
            raise ValidationError("旧密码错误！")


# 权限管理
class AuthForm(FlaskForm):
    name = StringField(
        label="权限名称",
        validators=[
            DataRequired("权限名称不能为空！")
        ],
        description="权限名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入权限名称！"
        }
    )
    url = StringField(
        label="权限地址",
        validators=[
            DataRequired("权限地址不能为空！")
        ],
        description="权限地址",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入权限地址！"
        }
    )
    submit = SubmitField(
        '编辑',
        render_kw={
            "class": "btn btn-primary",
        }
    )


# 角色管理
class RoleForm(FlaskForm):
    name = StringField(
        label="角色名称",
        validators=[
            DataRequired("角色名称不能为空！")
        ],
        description="角色名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入角色名称！"
        }
    )
    # 多选框
    auths = SelectMultipleField(
        label="权限列表",
        validators=[
            DataRequired("权限列表不能为空！")
        ],
        # 动态数据填充选择栏：列表生成器
        coerce=int,
        choices=[(v.id, v.name) for v in Auth.query.all()],
        description="权限列表",
        render_kw={
            "class": "form-control",
        }
    )
    submit = SubmitField(
        '编辑',
        render_kw={
            "class": "btn btn-primary",
        }
    )


class AdminForm(FlaskForm):
    name = StringField(
        label="管理员名称",
        validators=[
            DataRequired("管理员名称不能为空！")
        ],
        description="管理员名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员名称！",
        }
    )
    pwd = PasswordField(
        label="管理员密码",
        validators=[
            DataRequired("管理员密码不能为空！")
        ],
        description="管理员密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员密码！",
        }
    )
    repwd = PasswordField(
        label="管理员重复密码",
        validators=[
            DataRequired("管理员重复密码不能为空！"),
            EqualTo('pwd', message="两次密码不一致！")
        ],
        description="管理员重复密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员重复密码！",
        }
    )
    role_id = SelectField(
        label="所属角色",
        coerce=int,
        choices=[(v.id, v.name) for v in Role.query.all()],
        render_kw={
            "class": "form-control",
        }
    )
    submit = SubmitField(
        '编辑',
        render_kw={
            "class": "btn btn-primary",
        }
    )


# 标签表单
class TaobaoForm(FlaskForm):
    # input
    name = StringField(
        label="物品名",
        validators=[
            DataRequired("需要抓取的标题名不能为空")
        ],
        description="物品名",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入标签名称！"
        }
    )
    num = StringField(
        label="数目",
        validators=[
            DataRequired("需要抓取数目")
        ],
        description="数目",
        render_kw={
            "class": "form-control",
            "id": "input_name2",
            "placeholder": "请输入需要抓取的数目！"
        }
    )
    # 按钮
    submit = SubmitField(
        '编辑',
        render_kw={
            "class": "btn btn-primary",
        }
    )


# 淘宝详情表单
class TaobaoDetailForm(FlaskForm):
    # input
    # type_name = StringField(
    #     label="关键字",
    #     validators=[
    #         DataRequired("关键字不能为空")
    #     ],
    #     description="关键字",
    #     render_kw={
    #         "class": "form-control",
    #         "id": "input_name1",
    #         "placeholder": "请输入关键字名称！"
    #     }
    # )
    # id = StringField(
    #     label="编号",
    #     validators=[
    #         DataRequired("编号")
    #     ],
    #     description="编号",
    #     render_kw={
    #         "class": "form-control disabled",
    #         "id": "input_name2",
    #         "placeholder": ""
    #     }
    # )
    zh_title = StringField(
        label="中文标题",
        validators=[
            DataRequired("中文标题")
        ],
        description="中文标题",
        render_kw={
            "class": "form-control",
            "id": "input_name3",
            "placeholder": "请输入中文标题"
        }
    )
    en_title = StringField(
        label="英文标题",
        validators=[
            DataRequired("英文标题")
        ],
        description="英文标题",
        render_kw={
            "class": "form-control",
            "id": "input_name4",
            "placeholder": "请输入英文标题"
        }
    )
    # view_sales = StringField(
    #     label="销量",
    #     validators=[
    #         DataRequired("销量")
    #     ],
    #     description="销量",
    #     render_kw={
    #         "class": "form-control",
    #         "id": "input_name5",
    #         "placeholder": "请输入销量"
    #     }
    # )
    # 按钮
    submit = SubmitField(
        '入库',
        render_kw={
            "class": "btn btn-primary",
        }
    )


class WishForm(FlaskForm):
    # name = StringField(
    #     label="产品名称",
    #     validators=[
    #         DataRequired("产品名称")
    #     ],
    #     description="产品名称",
    #     render_kw={
    #         "class": "form-control",
    #         # "id": "input_name4",
    #         "placeholder": "可接受BG00003GG"
    #     }
    # )
    sku = StringField(
        label="SKU",
        validators=[
            DataRequired("SKU")
        ],
        description="SKU",
        render_kw={
            "class": "form-control",
            "id": "pro_sku",
            "placeholder": "可接受BG00003GG"
        }
    )
    parent_sku = StringField(
        label="ParentSKU",
        validators=[
            DataRequired("ParentSKU")
        ],
        description="ParentSKU",
        render_kw={
            "class": "form-control",
            "id": "ParentSKU",
            "placeholder": "可接受BG00003GG"
        }
    )
    name = StringField(
        label="产品标题",
        validators=[
            DataRequired("产品标题")
        ],
        description="产品标题",
        render_kw={
            "class": "form-control",
            "id": "pro_name",
            "placeholder": "可接受Nikon D5100 DSLR Camera (Body Only) USA MODEL"
        }
    )

    description = TextAreaField(
        label="产品描述",
        validators=[
            DataRequired("简介不能为空！")
        ],
        description="产品描述",
        render_kw={
            "class": "form-control",
            "rows": 10,
            "placeholder": "可接受Nikon D5100 DSLR Camera (Body Only) USA MODEL"

        }
    )
    tags = StringField(
        label="产品标签",
        validators=[
            DataRequired("产品标签")
        ],
        description="产品标签",
        render_kw={
            "class": "form-control",
            "id": "pro_tag",
            # "onchange" : "tag_num()",
            # "id": "input_name4",
            "placeholder": "输入标签名"
        }
    )
    inventory = StringField(
        label="产品库存",
        validators=[
            DataRequired("产品库存")
        ],
        description="产品库存",
        render_kw={
            "class": "form-control",
            # "id": "input_name4",
            "placeholder": "输入产品库存"
        }
    )
    shipping = FloatField(
        label="产品运费",
        validators=[
            DataRequired("产品运费")
        ],
        description="产品运费",
        render_kw={
            "class": "form-control",
            # "id": "input_name4",
            "placeholder": "输入产品运费"
        }
    )
    price = FloatField(
        label="产品实际价格",
        validators=[
            DataRequired("产品价格")
        ],
        description="产品价格",
        render_kw={
            "class": "form-control",
            # "id": "input_name4",
            "placeholder": "输入产品实际价格"
        }
    )
    msrp = FloatField(
        label="产品建议零售价",
        validators=[
            DataRequired("产品价格")
        ],
        description="产品价格",
        render_kw={
            "class": "form-control",
            # "id": "input_name4",
            "placeholder": "输入建议零售价"
        }
    )
    main_image = StringField(
        label="主图地址",
        validators=[
            DataRequired("主图地址")
        ],
        description="主图地址",
        render_kw={
            "class": "form-control",
            "id": "main_img",
            "placeholder": "输入主图地址"
        }
    )
    extra_images = StringField(
        label="附图地址",
        validators=[
            DataRequired("附图地址")
        ],
        description="附图地址",
        render_kw={
            "class": "form-control",
            "id": "extra_img",
            "placeholder": "输入附图地址，多张附图用|隔开"
        }
    )
    shipping_time = StringField(
        label="运送时间",
        validators=[
            DataRequired("运送时间")
        ],
        description="运送时间",
        render_kw={
            "class": "form-control",
            # "id": "extra_img",
            "placeholder": "输入运送时间，例如：5-10"
        }
    )
    color = StringField(
        label="产品颜色",
        validators=[
            DataRequired("产品颜色")
        ],
        description="产品颜色",
        render_kw={
            "class": "form-control",
            "id": "pro_color",
            "placeholder": "输入产品颜色，例如：red,blue,green  用英文输入法下的,隔开,可以为空"
        }
    )
    size = StringField(
        label="产品尺寸",
        validators=[
            DataRequired("产品尺寸")
        ],
        description="产品尺寸",
        render_kw={
            "class": "form-control",
            "id": "pro_size",
            "placeholder": "输入产品颜色，例如：Large, Medium, Small, 5, 6, 7.5  用英文输入法下的,隔开，可以为空"
        }
    )
    submit = SubmitField(
        '上传产品',
        render_kw={
            "class": "btn btn-primary",
        }
    )
