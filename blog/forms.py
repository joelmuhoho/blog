from django import forms
from django.contrib.auth.models import User
from .models import Post, Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Post title', 'maxlength':'60'}))
    text = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control mb-5', 'placeholder': 'Post body'}))
    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'id_image'})
    )
    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image.size > 4*1024*1024:
                raise ValidationError("Image file too large ( > 4mb )")
            return image
        else:
            raise ValidationError("Couldn't read uploaded image")

    class Meta:
        model = Post
        fields = ('title', 'text', 'image')


class CommentForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_method = 'POST'
    submit = helper.add_input(Submit('Comment', 'Comment'))
    text = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Comment', 'rows': '0'}))

    class Meta:
        model = Comment
        fields = ('text',)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    helper = FormHelper()
    helper.form_method = 'POST'
    submit = helper.add_input(Submit('Sign up', 'Sign up'))
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
