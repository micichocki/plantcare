from .models import Plant, Post, Category
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class InstanceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        if kwargs.get("instance"):
            button_title = 'Save'
        else:
            button_title = 'Create'
        self.helper.add_input(Submit("", button_title))


class CategoryForm(InstanceForm):
    model = Category
    fields = "__all__"


class PlantForm(InstanceForm):
    model = Plant
    fields = "__all__"


class PostForm(InstanceForm):
    model = Post
    fields = ["plant", "content", "image"]
