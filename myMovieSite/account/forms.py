from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget

class Commentforms(forms.Form):
    movie_id = forms.IntegerField(widget=forms.HiddenInput)
    user = forms.CharField(widget=forms.HiddenInput)
    text = forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'))
class ForgetForm(forms.Form):
    email = forms.EmailField(label='邮箱', widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "请输入邮箱账号", "value": ""}),
                             max_length=100, error_messages={"required": "邮箱不能为空", "invalid": ""})
    verification_code = forms.CharField(
        label="验证码",
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'填写邮箱接受到的验证码'})
    )
    newpwd = forms.CharField(label='新密码', widget=forms.PasswordInput(
        attrs={'class':'form-control',"placeholder": "请输入新密码"}
    ))





