from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def profile(request):
    user = request.user
    return render(request, 'base.html')
