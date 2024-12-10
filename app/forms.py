from django import forms

from app.models import BlogPost, UserProfile, Comment, CategoryPost

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
    category_name = forms.CharField(
        max_length=100,
        required=False,  # 非必填，允许选择已有分类
        help_text="Enter a new category name, or leave blank to use an existing category.",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'New category name'})
    )

    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'category']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        category_name = self.cleaned_data.get('category_name')
        if category_name:
            category, created = CategoryPost.objects.get_or_create(name=category_name)
            self.instance.category = category
        return super().save(commit=commit)

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