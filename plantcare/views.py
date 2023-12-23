from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from schedule_keeper.models import Plant


def profile(request):
    user = request.user
    viewed_plants = request.session.get('viewed_plants', [])
    plants = [get_object_or_404(Plant, id=plant_id) for plant_id, _ in viewed_plants]

    return render(request, 'profile.html', {"plant_list": plants})
