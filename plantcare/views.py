from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from schedule_keeper.models import Plant, Follow


def profile(request):
    user = request.user

    followed_plants = Plant.objects.filter(follow__user=user)

    viewed_plants = request.session.get('viewed_plants', [])
    plants = [get_object_or_404(Plant, id=plant_id) for plant_id, _ in viewed_plants]

    return render(request, 'profile.html', {"followed_plants": followed_plants, "viewed_plants": plants})
