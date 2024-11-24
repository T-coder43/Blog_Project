from django import forms
from django.contrib.auth.forms import UserCreationForm

# 导入User模型
from django.contrib.auth.models import User
from .models import Profile


# 登录表单
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class UserRegisterForm(UserCreationForm):
    # 复写User的密码
    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password1') == data.get('password2'):
            return data.get('password1')
        else:
            raise forms.ValidationError("密码输入不一致,请重试。")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'avatar', 'bio')
