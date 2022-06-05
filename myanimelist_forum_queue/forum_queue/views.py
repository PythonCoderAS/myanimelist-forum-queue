from django.core.exceptions import SuspiciousOperation
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from threading import Thread
from .forms import PostForm
from .models import Post
from .worker import lock, post as make_post

# Create your views here.
def index_view(request):
    return render(request, 'forum_queue/index.html')


board_type_mappings = {
    1: "board_id",
    2: "club_id",
    3: "anime_id",
    4: "manga_id"
}


def api_queue_view(request):
    form_data = PostForm(request.POST)
    if not form_data.is_valid():
        raise SuspiciousOperation("Request had invalid data.")
    kwargs = {"body": form_data.cleaned_data['body']}
    if form_data.cleaned_data["is_part"]:
        kwargs["part_number"] = int(form_data.cleaned_data["title"])
        kwargs["title"] = "[Unknown Title]"
    kwargs[board_type_mappings[form_data.cleaned_data["board_type"]]] = int(form_data.cleaned_data["board_id"])
    post = Post(**kwargs)
    post.save()

    def after():
        with lock:
            make_post(post)

    Thread(target=after).start()

    return JsonResponse({"id": post.id, "html": render_to_string('forum_queue/post.html', {"item": post})})
