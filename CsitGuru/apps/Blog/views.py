from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView, View
from taggit.models import Tag

from .forms import BlogCommentForm, BlogSearchForm
from .models import Blog, Category, Visitior

"""
Bookmark functionality
"""
def bookmark_list(request):
    if request.user.is_authenticated:
        
        blog_queryset = Blog.objects.filter(bookmarks=request.user, status="published")
        context = {
            
            "blog_queryset": blog_queryset,
        }
        return render(request, "Blogs/bookmarked-blogs.html", context)
    else:
        return HttpResponse("Sign Up to Unlock this feature.")


def add_to_bookmark(request, pk):
    blog_obj = get_object_or_404(Blog, id=pk)
    blog_obj.bookmarks.add(request.user)
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


def remove_from_bookmark(request, pk):
    blog_obj = get_object_or_404(Blog, id=pk)

    blog_obj.bookmarks.remove(request.user)
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


"""
BLOGS
"""


class BlogView(View):
    def get(self, request):
        all_blogs = Blog.modelmanager.all().order_by(
            "published_date"
        )  
        print(all_blogs)
        paginator = Paginator(
            all_blogs, 8
        )  
        print('paginator:', paginator)

        page_var = "page" 
        page = request.GET.get(page_var)  
        try:
            paginate_queryset = paginator.page(page)
        except PageNotAnInteger:
            paginate_queryset = paginator.page(1)

        except EmptyPage:
            paginate_queryset = paginator.page(paginator.num_pages)

        print(paginate_queryset)
        context = {
            "page_var": page_var,
            "queryset": paginate_queryset,
        }
        return render(request, "Blogs/blogs.html", context)


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


class BlogDetailView(DetailView):
    model = Blog
    context_object_name = "i"

    def get(self, request, pk, slug):
        
        commentform = BlogCommentForm()
        blog_obj = Blog.modelmanager.get(id=pk, slug=slug)
        ip = get_client_ip(request)
        visitor_obj = Visitior.objects.filter(blog__id=pk)
        if visitor_obj.exists():
            print("The blog has already this visitor")
        else:
            visitior_obj, created = Visitior.objects.get_or_create(ipaddress=ip)
            blog_obj.views.add(visitior_obj)
            blog_obj.total_views = blog_obj.total_views + 1
            blog_obj.save()

        bookmarked = bool
        if request.user.is_authenticated:
            if blog_obj.bookmarks.filter(id=request.user.id).exists():
                bookmarked = True

        # Comments paginate
        allcomments = blog_obj.blogcomments.filter(status=True)
        print(allcomments)
        page = request.GET.get("comments", 10)
        paginator = Paginator(allcomments, 10) 
        try:
            comments = paginator.page(page)  
        except PageNotAnInteger: 
            comments = paginator.page(1)
        except EmptyPage:  
            comments = paginator.page(paginator.num_pages)
        context = {
            "i": blog_obj,
            
            "comment_form": commentform,
            "comments": comments,  
            "bookmarked": bookmarked,
            "allcomments": allcomments, 
        }

        return render(request, "Blogs/blog-detail.html", context)

    def post(self, request, pk, slug):
        blog_obj = Blog.modelmanager.get(id=pk, slug=slug)
        if request.user.is_authenticated:
            user_comment = None
            profile = request.user
            if request.method == "POST":
                comment_form = BlogCommentForm(request.POST)
                if comment_form.is_valid():
                    user_comment = comment_form.save(commit=False)
                    user_comment.blog = blog_obj 
                    user_comment.user = profile
                    user_comment.save()
                    return HttpResponseRedirect(
                        reverse("Blog:blog_detail", kwargs={"pk": blog_obj.id, "slug": blog_obj.slug})
                    )
        else:
            return HttpResponse("login to comment")


class BlogTagView(View):
    def get(self, request, slug):
        tag = get_object_or_404(Tag, slug=slug)
        common_tags = Blog.tags.most_common()[:6]
        blogsbytags = Blog.modelmanager.filter(tags=tag)
        context = {
            "tag": tag,
            "common_tags": common_tags,
            "blogsbytags": blogsbytags,
        }
        return render(request, "Blogs/blogs-by-tags.html", context)


class BlogSearchEngineView(View):
    def get(self, request):
        form = BlogSearchForm()
        q = ""
        results = []
        context = {}
        if "q" in request.GET:  
            print("User Query:", request.GET["q"])
            form = BlogSearchForm(request.GET)
            if form.is_valid():
                q = form.cleaned_data["q"]
                results = Blog.modelmanager.filter(title__icontains=q)
        context = {
            "q": q,
            "results": results,
        }
        return render(request, "Blogs/blog-search.html", context)


class BlogCategoryView(View):
    def get(self, request, category):
        category_obj = Category.objects.get(name=category)
        blog_queryset = Blog.modelmanager.filter(category=category_obj)

        context = {
            "blogs": blog_queryset,
        }
        return render(request, "Blogs/blogs-by-category.html", context)


class YourBlogsView(View):
    def get(self, request):
        blog_queryset = Blog.objects.filter(visibility="Private", author=request.user)
        print(blog_queryset)
        context = { "blogs": blog_queryset}
        return render(request, "Blogs/yourblog.html", context)


class YourBlogDetailView(View):
    def get(self, request, pk, slug):
        bookmarked = bool
        if request.user.is_authenticated:
            recentblogs = Blog.modelmanager.order_by("-published_date")[0:4]
            blog_obj = Blog.objects.get(id=pk, slug=slug, visibility="Private", author=request.user)
            print(blog_obj)
            if blog_obj.bookmarks.filter(id=request.user.id).exists():
                bookmarked = True
            context = {
                
                "recentblogs": recentblogs,
                "bookmarked": bookmarked,
                "i": blog_obj,
            }
            return render(request, "Blogs/yourblog-detail.html", context)
        else:
            return HttpResponse("You do not own this blog.")
