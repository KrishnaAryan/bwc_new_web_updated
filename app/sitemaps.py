from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import BlogPost, Job, DynamicURL, ProjectPage, Package

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return [
            'index', 'about', 'contact', 'blogs', 'job_list', 
            'privacy-policy', 'terms-and-conditions', 'service'
        ]

    def location(self, item):
        return reverse(item)

class BlogPostSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return BlogPost.objects.all()

    def lastmod(self, obj):
        return obj.date

class JobDetailSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return Job.objects.all()

    def lastmod(self, obj):
        return obj.created_at

class DynamicUrlSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return DynamicURL.objects.all()

    def lastmod(self, obj):
        return obj.created_at

class ProjectSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ProjectPage.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

class PackageSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return Package.objects.all()

    # def lastmod(self, obj):
    #     return obj.updated_at
