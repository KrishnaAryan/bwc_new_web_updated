from django.urls import path
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap, BlogPostSitemap, JobDetailSitemap, DynamicUrlSitemap, ProjectSitemap, PackageSitemap
from . import views
from app.views import dynamic_view

sitemaps = {
    'static': StaticViewSitemap,
    'blog': BlogPostSitemap,
    'jobs': JobDetailSitemap,
    'dynamicurl': DynamicUrlSitemap,
    'projects': ProjectSitemap,
    'packages': PackageSitemap,
}

def robots_txt(request):
    with open('robots.txt', 'r') as file:
        robots_txt_content = file.read()
    return HttpResponse(robots_txt_content, content_type='text/plain')

urlpatterns = [
    path('', views.index, name='index'),
    path('service', views.service, name='service'),
    path('project-list', views.project_list, name='project_list'),
    path('project-<slug:slug>', views.project_detail, name='project_detail'),
    path('blogs', views.blogs, name='blogs'),
    path('blogs-<slug:slug>', views.blogs_details, name='blogpost_detail'),
    path('about', views.about, name='about'),
    path('job_list', views.job_list, name='job_list'),
    path('job/<slug:slug>', views.job_detail, name='job_detail'),
    path('job/<slug:slug>/apply', views.apply_for_job, name='apply_for_job'),
    path('contact', views.contact, name='contact'),
    path('banner', views.banner, name='banner'),
    path('success', views.success_view, name='success'),
    path('package', views.package, name='package'),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('package-<slug:slug>', views.packagedownload, name='packagedownload'),
    path('privacy-policy', views.privacy_policy, name='privacy-policy'),
    path('terms-and-conditions', views.termsconditions, name='terms-and-conditions'),
    path('<str:path>', dynamic_view, name='dynamic_view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'app.views.custom_404_view'
