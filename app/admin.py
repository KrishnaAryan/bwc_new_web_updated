from django.contrib import admin
from .models import *

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'message', 'timestamp']
    search_fields = ['name', 'email', 'phone', 'timestamp']
    list_filter = ['timestamp']






from django.contrib import admin
from .models import ProjectPage, InteriorImage, ArchitectureImage, BuildingImage, ExteriorImage

class InteriorImageInline(admin.TabularInline):
    model = InteriorImage
    extra = 1

class ArchitectureImageInline(admin.TabularInline):
    model = ArchitectureImage
    extra = 1

class BuildingImageInline(admin.TabularInline):
    model = BuildingImage
    extra = 1

class ExteriorImageInline(admin.TabularInline):
    model = ExteriorImage
    extra = 1
    
class ThumbnailImageInline(admin.TabularInline):
    model = ThumbnailImage
    extra = 1

@admin.register(ProjectPage)
class ProjectPageAdmin(admin.ModelAdmin):
    inlines = [ThumbnailImageInline,InteriorImageInline, ArchitectureImageInline, BuildingImageInline, ExteriorImageInline]







admin.site.register(BlogPost)


from django.contrib import admin
from django.utils.html import format_html
from .models import Job, Application

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_open')
    list_filter = ('is_open', 'created_at')
    search_fields = ('title', 'description')
    actions = ['make_open', 'make_closed']

    @admin.action(description='Mark selected jobs as open')
    def make_open(self, request, queryset):
        queryset.update(is_open=True)

    @admin.action(description='Mark selected jobs as closed')
    def make_closed(self, request, queryset):
        queryset.update(is_open=False)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'job', 'applied_at', 'download_resume')
    list_filter = ('job', 'applied_at')
    search_fields = ('name', 'email', 'job__title')

    def download_resume(self, obj):
        if obj.resume:
            return format_html('<a href="{}" download>Download</a>', obj.resume.url)
        return "No resume uploaded"
    download_resume.short_description = 'Resume'







# @admin.register(DynamicURL)
# class DynamicURLAdmin(admin.ModelAdmin):
#     list_display = ('path', 'title')
#     search_fields = ('path', 'title')


from import_export.admin import ImportExportModelAdmin
@admin.register(DynamicURL)
class DynamicURLAdmin(ImportExportModelAdmin):
    list_display = ('path', 'title','meta_description')



# from .models import Package, PackageSummary

# class PackageSummaryInline(admin.TabularInline):
#     model = PackageSummary
#     extra = 1

# @admin.register(Package)
# class PackageAdmin(admin.ModelAdmin):
#     inlines = [PackageSummaryInline]
#     list_display = ('name', 'price', 'offer_price', 'slug')
#     search_fields = ('name', 'slug')

# # @admin.register(PackageSummary)
# # class PackageSummaryAdmin(admin.ModelAdmin):
# #     list_display = ('package', 'summary')
# #     search_fields = ('package__name', 'summary')


# class PackageDownloadAdmin(admin.ModelAdmin):
#     list_display = ('name', 'email', 'phone', 'looking_for', 'timestamp')
#     list_filter = ('looking_for', 'timestamp')
#     search_fields = ('name', 'email', 'phone', 'looking_for')

# admin.site.register(PackageDownload, PackageDownloadAdmin)




from django.contrib import admin
from .models import Package, PackageSummary, PackageDownload

# 1. Package ke andar hi Summary dikhane ke liye Inline
class PackageSummaryInline(admin.TabularInline):
    model = PackageSummary
    extra = 1

# 2. Package Admin Configuration
@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    inlines = [PackageSummaryInline]
    list_display = ('name', 'price', 'offer_price', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)} # Name likhte hi slug apne aap ban jayega

# 3. PackageDownload Admin Configuration
@admin.register(PackageDownload)
class PackageDownloadAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'looking_for', 'timestamp')
    list_filter = ('looking_for', 'timestamp')
    search_fields = ('name', 'email', 'phone')
    ordering = ('-timestamp',) # Nayi leads sabse upar dikhengi




@admin.register(PopupImage)
class PopupImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'caption', 'image')
    search_fields = ('caption',)
    list_filter = ('caption',)
    
    
    
    


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'gender',
        'projects',
        'is_active',
        'created_at'
    )

    list_filter = ('gender', 'is_active')
    search_fields = ('name', 'projects', 'message')
    list_editable = ('is_active',)

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'gender', 'projects')
        }),
        ('Review Content', {
            'fields': ('message',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )