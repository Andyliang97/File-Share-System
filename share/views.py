import os
import random
import string

from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage, FileSystemStorage
from django.db.models import F
from django.http import HttpResponseRedirect, FileResponse, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View, DetailView, ListView
from .models import VideoInfo
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator


# Create your views here.

def image(request):
    return render(request, 'share/image.html', {'imageurl': default_storage.url('liangandy/django-dark.width-808.png')})


class IndexView(ListView):
    model = VideoInfo
    template_name = 'share/mainpage.html'
    context_object_name = 'videoinfo'
    ordering = ['-upload_time']
    paginate_by = 8


class UploadView(View):
    @method_decorator(login_required)
    def post(self, request):
        max_size = 4096 # 4MB = 4096KB
        if request.FILES:
            file = request.FILES.get("file")
            size = int(int(file.size) / 1024)
            try:
                print(size)
                if size > max_size:
                    raise ValidationError('File too large. Size should not exceed 4 MB.')
            except ValidationError:
                messages.warning(request, f'Error: File too large. Size should not exceed 4 MB.')
                return render(request, 'share/mainpage.html', {'error_message': 'Size should not exceed 30 MB'})
            filename = file.name
            aws_filename = request.user.username+'/'+filename
            '''
            store to /media/
            
            fs = FileSystemStorage()
            store_name=fs.save(request.user.username+'/'+filename, file)
            store_url=fs.url(store_name)
            '''
            print('prepare upload')
            if default_storage.exists(aws_filename):
                print('file already exist')
                messages.warning(request, f'Error: Failed to store due to duplicate file name. '
                                            f'Here is the file you uploaded before.')
                return render(request, 'share/mainpage.html', {'error_message': 'Failed to store due to duplicate file '
                                                                'name. Here is the file you uploaded before.'})
            else:
                # s3file = default_storage.open(filepath, 'w')
                default_storage.save(aws_filename, file)
                #s3file.close()
                upload = VideoInfo(
                    code=''.join(random.sample(string.digits, 8)),
                    file_name=filename,
                    download_path=default_storage.url(request.user.username+'/'+filename),
                    file_size=size,
                    upload_ip=str(request.META['REMOTE_ADDR']),
                    user=request.user,
                    aws_file_name=aws_filename
                )
                upload.save()

            '''Low level approach
            
            with open('share/static/share/file/' + filename, 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            '''
        return HttpResponseRedirect(reverse('share:detail',
                                            args=(int(VideoInfo.objects.get(aws_file_name=aws_filename).id),)))


class DetailView(DetailView):
    model = VideoInfo
    template_name = 'share/detail.html'


class ListView(ListView):
    template_name = 'share/mainpage.html'
    context_object_name = 'videoinfo'
    paginate_by = 6
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
    '''
    download from localhost
    file_path = ''.join([settings.MEDIA_ROOT, '/', video_info.file_name])
    '''
    print('media/'+video_info.download_path)
    if default_storage.exists(video_info.aws_file_name):
        f = default_storage.open(video_info.aws_file_name, 'r')
        response = FileResponse(f)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = ''.join(['attachment; filename=', video_info.file_name])
        video_info.download_count = F('download_count') + 1
        video_info.save()
        f.close()
        return response
    else:
        print('not found ')
    raise Http404


def delete(request, videoId):
    if request.method == 'POST':
        delete_item = get_object_or_404(VideoInfo, pk=videoId)  # either pk or id is fine
        if delete_item.user == request.user:
            delete_item.delete()
            default_storage.delete(delete_item.aws_file_name)
            return JsonResponse({'status': 'success', 'delete_item': delete_item.file_name})
        else:
            return JsonResponse({'status': 'fail', 'reason': 'User Not Authorized'})


@login_required
def check_pagination(request):
    if request.method == "GET":
        cur_user_file = VideoInfo.objects.filter(user=request.user)
        p = Paginator(cur_user_file, 10)
        return JsonResponse({'num_pages': p.num_pages})

