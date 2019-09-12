from django.shortcuts import render,  get_object_or_404
from .models import post
from django.contrib.auth.models import User
# create login authorization to create new post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# from django.http import HttpResponse   only req when httpresponce like below

# Create your views here.


# posts = [
#     {
#         'author': 'Ram',
#         'date_posted': 'July 27',
#         'title': 'My Kathmandu',
#         'content': 'City'
#     },

#     {
#         'author': 'Messi',
#         'date_posted': 'August 02',
#         'title': 'My Barcelona',
#         'content': 'Football'
#     }
# ]


def home(request):
    context = {
        'posts': post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']


class UserPostListView(ListView):
    model = post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    # ordering = ['-date_posted']

    # to show all post of particular user
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = post
    success_url = '/'  # send url to home after deletion

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    # return HttpResponse('<h1>About</h1>')
    return render(request, 'blog/about.html', {'title': 'About'})
