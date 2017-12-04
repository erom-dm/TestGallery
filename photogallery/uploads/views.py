from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post
from django.contrib.auth.models import User
from django.core.files.base import File
import tempfile
from .insta_scrape import scrapper
from urllib.parse import urlparse
from urllib import request as req
from os.path import basename
from .forms import DeleteNewForm

from django.http import HttpResponse, HttpResponseRedirect

# import requests
@login_required
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['description'] and request.FILES['file']:
            post = Post()
            post.title = request.POST['title']
            post.description = request.POST['description']
            post.file = request.FILES['file']
            post.pub_date = timezone.datetime.now()
            post.author = request.user
            file = post.file.name
            if file.endswith('.mp4') or file.endswith('.webm') or file.endswith('.ogg'):
                post.vid_bool = True
            else:
                post.vid_bool = False
            post.save()
            return redirect('home')
        else:
            return render(request, 'uploads/create.html', {'error':'ERROR: You must fill all fields'})
        return render(request, 'uploads/create.html')
    else:
        return render(request, 'uploads/create.html')


def home(request):
    posts = Post.objects.order_by('-pub_date')
    return render(request, 'uploads/home.html', {'posts': posts})


def postdetail(request, upload_id):
    post = get_object_or_404(Post, pk=upload_id)
    return render(request, 'uploads/post_detail.html', {'post': post})


@login_required
def editpost(request, upload_id):
    user = request.user
    post = get_object_or_404(Post, pk=upload_id)
    if request.method == 'POST':
        if request.POST['title']:
            post.title = request.POST['title']
        if request.POST['description']:
            post.description = request.POST['description']
        else:
            post.description = " "
        if request.FILES != {}:
            post.file = request.FILES['file']
            file = post.file.name
            if file.endswith('.mp4') or file.endswith('.webm') or file.endswith('.ogg'):
                post.vid_bool = True
            else:
                post.vid_bool = False
        post.pub_date = timezone.datetime.now()
        post.save()
        return redirect('home')
    else:
        return render(request, 'uploads/edit_post.html', {'post': post, 'user': user})
    return render(request, 'uploads/edit_post.html', {'post': post})

@login_required
def download(request):
    if request.method == 'POST':
        if request.POST['url']:
            content = scrapper(request.POST['url'])
            post = Post()
            post.title = content[0]
            post.description = content[1]
            post.pub_date = timezone.datetime.now()          # content[3] will pull up datetime data from instagram
            post.author = request.user

            img_temp = tempfile.NamedTemporaryFile(delete=True)
            req_inst = req.Request(content[2], data=None)
            with req.urlopen(req_inst) as response:
                img_temp.write(response.read())
            img_temp.flush()
            filename = basename(urlparse(content[2]).path)
            post.file.save(filename, File(img_temp))
            img_temp.close()

            """ Alternative way of doing instagram media file download. Works perfectly fine with images, borderline
            unusable with video posts. Have no idea why. Magic.
            
            req = requests.get(content[2], stream=True)
            if req.status_code != requests.codes.ok:
                print("error I suppose?")
            fp = tempfile.NamedTemporaryFile()
            for block in req.iter_content(1048 * 8):
                if not block:
                    break
                fp.write(block)
            a = request.POST['url']
            file_name = a.split("/")[-1]
            post.file.save(file_name, fp, save=False)
            """
            file = post.file.name
            if file.endswith('.mp4') or file.endswith('.webm') or file.endswith('.ogg'):
                post.vid_bool = True
            else:
                post.vid_bool = False
            post.save()
            return redirect('home')
        else:
            return render(request, 'uploads/create_via_dl.html', {'error':'ERROR: You must fill the field'})
        return render(request, 'uploads/create_via_dl.html')
    else:
        return render(request, 'uploads/create_via_dl.html')


def delete_post(request, upload_id):
    post_to_delete = get_object_or_404(Post, id=upload_id)
    if request.method == 'POST':
        form = DeleteNewForm(request.POST, instance=post_to_delete)
        if form.is_valid():
            post_to_delete.delete()
            return redirect("home")
    else:
        form = DeleteNewForm(instance=post_to_delete)

    return render(request, 'uploads/delete_post.html', {'form': form, 'post': post_to_delete})


def user_uploads(request, fk):
    posts = Post.objects.filter(author__id=fk).order_by('-pub_date')
    author = User.objects.get(pk=fk)
    return render(request, 'uploads/user_uploads.html', {'posts': posts, 'author': author})
