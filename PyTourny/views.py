from django.shortcuts import render

from PyTournyApp.models import OfflineUser, OfflineWinner


def home(request):
    return render(request, 'home.html')


def offline(request):
    offline_users = OfflineUser.objects.all().order_by('id')
    offline_winners = OfflineWinner.objects.all().order_by('-wins')
    context = {'offline_users': offline_users, 'offline_winners': offline_winners}
    return render(request, 'offline.html', context)
