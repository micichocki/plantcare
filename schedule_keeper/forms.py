from .models import Plant, Post, Category, Follow
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
    class Meta:
        model = Category
        fields = "__all__"


class PlantForm(InstanceForm):
    class Meta:
        model = Plant
        fields = ["name", "description", "category", "watering_frequency", "img"]


class PostForm(InstanceForm):
    class Meta:
        model = Post
        fields = ["content", "img"]


class FollowForm(InstanceForm):
    class Meta:
        plant_id = forms.IntegerField()
        is_following = forms.BooleanField()
