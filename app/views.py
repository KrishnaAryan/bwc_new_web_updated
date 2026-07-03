from django.utils.translation import gettext_lazy as _
from .forms import *
from .models import *
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render, get_object_or_404
from .models import BlogPost
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import timedelta


def index(request):
    projects = ProjectPage.objects.all()
    popup_image = PopupImage.objects.first()
    reviews = Review.objects.filter(is_active=True)
    context = {
        'projects': projects,
        'popup_image':popup_image,
        'reviews':reviews
    }
    return render(request, 'index.html',context)




def project_list(request):
    projects = ProjectPage.objects.all()
    return render(request, 'project.html', {'projects': projects})


def project_detail(request, slug):
    project = get_object_or_404(ProjectPage, slug=slug)

    interior_images = project.interior_images.exclude(image='')
    architecture_images = project.architecture_images.exclude(image='')
    building_images = project.building_images.exclude(image='')
    exterior_images = project.exterior_images.exclude(image='')
    thumbnail_images = project.thumbnail_images.exclude(image='')

    # ONLY VALID IMAGES
    all_images = (
        list(interior_images) +
        list(architecture_images) +
        list(building_images) +
        list(exterior_images) +
        list(thumbnail_images)
    )

    return render(request, 'project_detail.html', {
        'project': project,
        'all_images': all_images,
        'interior_images': interior_images,
        'architecture_images': architecture_images,
        'building_images': building_images,
        'exterior_images': exterior_images,
        'thumbnail_images': thumbnail_images,
    })




def about(request):
    return render(request, 'about.html')

def service(request):
    return render(request, 'services.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        try:
            ContactMessage.objects.create(name=name, email=email, phone=phone, message=message)
            return redirect('success')  # Ensure you have a 'success' URL pattern and view
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return render(request, 'contact.html')



def success_view(request):
    return render(request, 'success.html')




def custom_404_view(request, exception):
    return render(request, '404.html', status=404)



def blogs(request):
    
    blog_posts = BlogPost.objects.order_by('-click_count', '-date')

    
    trending_time_frame = timezone.now() - timedelta(days=7)

    
    trending_posts = [post for post in blog_posts if post.click_count >= 100 and post.date >= trending_time_frame]
    new_posts = [post for post in blog_posts if post not in trending_posts]

    posts_per_page = 5

    
    trending_paginator = Paginator(trending_posts, posts_per_page)
    trending_page = request.GET.get('trending_page')

    try:
        trending_posts_page = trending_paginator.page(trending_page)
    except PageNotAnInteger:
        trending_posts_page = trending_paginator.page(1)
    except EmptyPage:
        trending_posts_page = trending_paginator.page(trending_paginator.num_pages)

    
    new_paginator = Paginator(new_posts, posts_per_page)
    new_page = request.GET.get('new_page')

    try:
        new_posts_page = new_paginator.page(new_page)
    except PageNotAnInteger:
        new_posts_page = new_paginator.page(1)
    except EmptyPage:
        new_posts_page = new_paginator.page(new_paginator.num_pages)

    context = {
        'include_main_css': False,
        'trending_posts_page': trending_posts_page,
        'new_posts_page': new_posts_page,
    }

    return render(request, 'blogs.html', context)

def blogs_details(request, slug):  
    blog_post = get_object_or_404(BlogPost, slug=slug)

    
    blog_post.click_count += 1
    blog_post.save()

    context = {
        "blog_post": blog_post,
    }

    return render(request, 'blog_detalils.html', context)









def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'careers.html', {'jobs': jobs})



def job_detail(request, slug):
    try:
        job = get_object_or_404(Job, slug=slug)
    except Job.DoesNotExist:
        job = None
    return render(request, 'job_detail.html', {'job': job})




def apply_for_job(request, slug):
    job = get_object_or_404(Job, slug=slug)
    if not job.is_open:
        return render(request, 'job_closed.html', {'job': job})
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.save()
            return redirect('job_detail', slug=job.slug)
    else:
        form = ApplicationForm()
    return render(request, 'apply_for_job.html', {'form': form, 'job': job})


# def PrivacyPolicy(request):
#     return render(request, 'PrivacyPolicy.html')

# def TermsConditions(request):
#     return render(request, 'Terms&Conditions.html')



def dynamic_view(request, path):
    dynamic_url = get_object_or_404(DynamicURL, path=path)
    return render(request, 'dynamic_template.html', {'dynamic_url': dynamic_url})




# def package(request):
#     packages = Package.objects.all()
#     form = PackageDownloadForm()

#     if request.method == 'POST':
#         form = PackageDownloadForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # Add any success logic here (e.g., redirect to a thank you page)
#             return redirect('packagedownload')  # Replace with your actual URL

#     context = {
#         'packages': packages,
#         'form': form,  # Pass the form to the template context
#     }
#     return render(request, 'package.html', context)


def package(request):
    packages = Package.objects.all()
    return render(request, 'package.html', {
        'packages': packages
    })


from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, render
from .models import Package
from .forms import PackageDownloadForm
import mimetypes

def packagedownload(request, slug):
    packages = get_object_or_404(Package, slug=slug)
    form = PackageDownloadForm()

    if request.method == 'POST':
        form = PackageDownloadForm(request.POST)
        if form.is_valid():
            form.save()

            try:
                file_path = packages.package_documents.path
                mime_type, _ = mimetypes.guess_type(file_path)

                response = FileResponse(
                    open(file_path, 'rb'),
                    content_type=mime_type
                )
                response['Content-Disposition'] = f'attachment; filename="{packages.package_documents.name}"'
                return response

            except FileNotFoundError:
                raise Http404("File not found")

    return render(request, 'package_download.html', {
        'packages': packages,
        'form': form
    })

from django.shortcuts import render

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def termsconditions(request):
    return render(request, 'terms_and_conditions.html')


def banner(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        try:
            ContactMessage.objects.create(name=name, email=email, phone=phone, message=message)
            return redirect('success')  # Ensure you have a 'success' URL pattern and view
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return render(request, 'banner.html')