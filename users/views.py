from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm
from django.views.generic import ListView
from share.models import VideoInfo
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            # messages.success(request, f'Account Created for {username}!')
            return redirect('users:login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


class ProfileListView(ListView):
    model = VideoInfo
    template_name = 'users/profile.html'
    context_object_name = 'videoinfo'
    paginate_by = 10

    def get_queryset(self):
        return VideoInfo.objects.filter(user=self.request.user).order_by('-upload_time')




