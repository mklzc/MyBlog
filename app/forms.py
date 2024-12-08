from django import forms

from app.models import BlogPost, UserProfile, Comment


# 注册表单
class RegisterForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True)

    def clean(self):
        cleared_data = super().clean()
        password = cleared_data.get("password")
        confirm_password = cleared_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        return cleared_data

class LoginForm(forms.Form):
    email = forms.CharField(max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

class PostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'body']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio']

    avatar = forms.ImageField()
    bio = forms.CharField(widget=forms.Textarea, required=False)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']