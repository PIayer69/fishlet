from django.shortcuts import render
from django.contrib.auth.models import User


# Create your views here.
def profile(request, pk):
    user = User.objects.get(id=pk)
    user_sets = user.set_set.all()
    context = {
        'user': user,
        'sets': user_sets
    }
    return render(request, 'profiles/profile.html', context)