from io import BytesIO
from PIL import Image

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.files.images import ImageFile
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.views.generic import TemplateView

from .models import Post, Plant, Follow
from .forms import PlantForm, PostForm


def index(request):
    return render(request, 'index.html')


@login_required
def plants(request):
    search = request.GET.get('search', None)
    if search:
        found_plants_queryset = Plant.objects.filter(
            Q(name__icontains=search) | Q(category__name__icontains=search))
        plant_list = list(found_plants_queryset)
        context = {'plant_list': plant_list, 'search': search}
    else:
        plant_list = Plant.objects.all()
        context = {'plant_list': plant_list}
    user = request.user
    for plant in plant_list:
        plant.is_following = Follow.objects.filter(user=user, plant=plant).exists()
    return render(request, 'schedule_keeper/plant_list.html', context)


@login_required
def plant_detail(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    posts = plant.post_set.all()
    if posts:
        context = {
            "plant": plant,
            "posts": posts
        }
    else:
        context = {
            "plant": plant,
            "posts": None
        }
    if request.user.is_authenticated:
        max_viewed_plants_length = 10
        viewed_plants = request.session.get('viewed_plants', [])
        viewed_plant = [plant.id, plant.name]
        if viewed_plant in viewed_plants:
            viewed_plants.pop(viewed_plants.index(viewed_plant))
        viewed_plants.insert(0, viewed_plant)
        viewed_plants = viewed_plants[0:max_viewed_plants_length]
        request.session['viewed_plants'] = viewed_plants

    follow_exists = Follow.objects.filter(user=request.user, plant=plant).exists()
    context["is_following"] = follow_exists

    return render(request, "schedule_keeper/plant_detail.html", context)


class PlantView(TemplateView):
    template_name = 'schedule_keeper/instance_form.html'
    form_class = PlantForm

    def get(self, request, pk):
        plant = get_object_or_404(Plant, pk=pk)
        related_posts = plant.posts.all()
        context = {"plant": plant, "posts": related_posts}
        return render(request, "schedule_keeper/plant_detail.html", context)

    def post(self, request, pk):
        plant = get_object_or_404(Plant, pk=pk)
        form = self.form_class(request.POST, request.FILES, instance=plant)

        if form.is_valid():
            form.save()
            return redirect("plant-detail", plant.pk)

        context = {
            "form": form,
            "instance": plant,
            "model_type": "Plant",
        }

        return render(request, self.template_name, context)


class PostView(TemplateView):
    template_name = 'schedule_keeper/instance_form.html'
    form_class = PostForm

    def get(self, request, plant_pk, post_pk=None):
        plant = get_object_or_404(Plant, pk=plant_pk)
        post = get_object_or_404(Post, plant_id=plant_pk, pk=post_pk) if post_pk else None

        if not self.check_permissions(request.user, post):
            raise PermissionDenied

        form = self.form_class(instance=post)
        context = {
            "form": form,
            "instance": post,
            "model_type": "Post",
            "related_instance": plant,
            "related_model_type": "Plant"
        }

        return render(request, self.template_name, context)

    def post(self, request, plant_pk, post_pk=None):
        plant = get_object_or_404(Plant, pk=plant_pk)
        post = get_object_or_404(Post, plant_id=plant_pk, pk=post_pk) if post_pk else None

        if not self.check_permissions(request.user, post):
            raise PermissionDenied

        form = self.form_class(request.POST, request.FILES, instance=post)

        if form.is_valid():
            updated_post = form.save(commit=False)

            updated_post.plant = plant
            updated_post.creator = request.user

            post_img = form.cleaned_data['img']
            if post_img:
                image = Image.open(post_img)
                image.thumbnail((300, 300))
                image_data = BytesIO()
                image.save(fp=image_data, format=image.format)
                image_file = ImageFile(image_data)
                updated_post.img.save(post_img.name, image_file)
                plant.img = updated_post.img.url
                plant.save()

            if post is None:
                messages.success(request, f"Post for \"{updated_post}\" created.")
            else:
                messages.success(request, f"Post for \"{updated_post}\" updated.")

            updated_post.save()

            return redirect("plant-detail", plant.pk)

        context = {
            "form": form,
            "instance": post,
            "model_type": "Post",
            "related_instance": plant,
            "related_model_type": "Plant"
        }

        return render(request, self.template_name, context)

    def check_permissions(self, user, post):
        return user.is_staff or post.user.id == user.id


def follow_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    follow, created = Follow.objects.get_or_create(user=request.user, plant=plant)

    if request.method == 'POST':
        if not created:
            follow.delete()
    referer = request.META.get('HTTP_REFERER', None)
    return redirect(referer or 'home')
