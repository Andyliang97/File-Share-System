import os
import random
import string

from django.core.exceptions import ValidationError
from django.db.models import F
from django.http import HttpResponseRedirect, FileResponse, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View, DetailView, ListView
from .models import VideoInfo
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.auth.decorators import login_required


# Create your views here.


class IndexView(View):
    def get(self, request):
        return render(request, 'share/mainpage.html', {'videoinfo': VideoInfo.objects.order_by('-upload_time')[:5]})

    @method_decorator(login_required)
    def post(self, request):
        max_size = 30720 # 30MB = 30720KB
        if request.FILES:
            file = request.FILES.get("file")
            size = int(int(file.size) / 1024)
            try:
                if size > max_size:
                    raise ValidationError('File too large. Size should not exceed 30 MB.')
            except ValidationError:
                return render(request, 'share/mainpage.html', {'error_message': 'Size should not exceed 30 MB'})
            filename = file.name
            # print(len('share/static/share/file/' + filename))
            upload = VideoInfo(
                code=''.join(random.sample(string.digits, 8)),
                file_name=filename,
                download_path='share/static/share/file/' + filename,
                file_size=size,
                upload_ip=str(request.META['REMOTE_ADDR']),
                user=request.user
            )
            upload.save()
            with open('share/static/share/file/' + filename, 'wb') as f:
                f.write(file.read())
        return HttpResponseRedirect(reverse('share:detail', args=(int(upload.id),)))


class DetailView(DetailView):
    model = VideoInfo
    template_name = 'share/detail.html'


class ListView(ListView):
    template_name = 'share/mainpage.html'
    context_object_name = 'videoinfo'
    # print('here')

    def get_queryset(self):
        # print(self.kwargs['filename'])
        # print(VideoInfo.objects.all())
        # return VideoInfo.objects.filter(file_name__icontains=self.kwargs['filename'])
        videoSet = VideoInfo.objects.annotate(
            similarity=TrigramSimilarity('file_name', self.request.GET.get('search')),
        ).filter(similarity__gt=0.3).order_by('-similarity')
        # print(videoSet)
        return videoSet


def download(request, videoId):
    video_info = get_object_or_404(VideoInfo, pk=videoId)
    file_path = ''.join(['share/static/share/file/', video_info.file_name])
    # print(file_path)
    if os.path.exists(file_path):
        # print('exist')
        # with open(file_path, 'rb') as f:
        f = open(file_path, 'rb')
        response = FileResponse(f)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = ''.join(['attachment; filename=', video_info.file_name])
        video_info.download_count = F('download_count') + 1
        video_info.save()
        return response
    raise Http404


def delete(request, videoId):
    if request.method == 'GET':
        delete_item = get_object_or_404(VideoInfo, pk=videoId)  # either pk or id is fine
        print(delete_item.user)
        print(request.user)
        print(delete_item)
        if delete_item.user == request.user:
            delete_item.delete()
            return JsonResponse({'status': 'success', 'delete_item': delete_item.file_name})
        else:
            return JsonResponse({'status': 'fail', 'reason': 'User Not Authorized'})

