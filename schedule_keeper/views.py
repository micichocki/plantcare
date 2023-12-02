from io import BytesIO
from PIL import Image

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.files.images import ImageFile
from django.core.exceptions import PermissionDenied
from django.db.models import Q

from .models import Post, Plant, Follow
from .forms import PostForm


def index(request):
    return render(request, 'index.html')


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
    user =
    for plant in plant_list:

    return render(request, 'schedule_keeper/plant_list.html', context)


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
    return render(request, "schedule_keeper/plant_detail.html", context)


@login_required
def post_edit(request, plant_pk, post_pk=None):
    plant = get_object_or_404(Plant, pk=plant_pk)
    if post_pk is not None:
        post = get_object_or_404(Post, plant_id=plant_pk, pk=post_pk)
        user = request.user
        if not user.is_staff and post.user.id != user.id:
            raise PermissionDenied
    else:
        post = None

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            updated_post = form.save(commit=False)
            updated_post.plant = plant

            post_image = form.cleaned_data['image']
            if post_image:
                image = Image.open(post_image)
                image.thumbnail((300, 300))
                image_data = BytesIO()
                image.save(fp=image_data, format=post_image.image.format)
                image_file = ImageFile(image_data)
                post.post_image.save(post_image.name, image_file)

            if post is None:
                messages.success(request, "Post for \"{}\" created.".format(post))
            else:
                messages.success(request, "Post for \"{}\" updated.".format(post))
            post.save()
            messages.success(request, f"Post {post} was successfully updated.")
            return redirect("plant_detail", plant.pk)
    else:
        form = PostForm(instance=post)

    return render(request, "schedule_keeper/instance-form.html",
                  {"form": form,
                   "instance": post,
                   "model_type": "Post",
                   "related_instance": plant,
                   "related_model_type": "Plant"
                   })
