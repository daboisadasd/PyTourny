from django.shortcuts import render
from .models import OfflineUser, OfflineWinner


def home(request):
    return render(request, 'home.html')


def offline(request):
    # retrieve all offline users
    offline_users = OfflineUser.objects.all()

    # retrieve all offline winners and their win counts
    offline_winners = OfflineWinner.objects.all()

    # sort the winners by number of wins (in descending order)
    sorted_winners = sorted(offline_winners, key=lambda x: x.wins, reverse=True)

    return render(request, 'offline.html', {'offline_users': offline_users, 'sorted_winners': sorted_winners})
