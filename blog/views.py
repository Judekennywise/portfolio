from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.generic import ListView

from blog.models import Post, Comment
from blog.forms import CommentForm
def blog_index(request):
    posts = Post.objects.all().order_by('-created_on')
    context = {
        "posts": posts,
    }
    return render(request, 'blog_index.html', context)

def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by(
        '-created_on'
    )
    context = {
        "category": category,
        "posts": posts
    }
    return render(request, 'blog_category.html', context)


def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post
            )
            comment.save()


    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
        "form": form
    }

    return render(request, 'blog_detail.html', context)


class Search(ListView):
    model = Post
    template_name = 'search.html'
    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Post.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )
        return object_list
