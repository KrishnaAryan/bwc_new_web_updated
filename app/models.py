from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.core.validators import RegexValidator  # Correct import

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Phone number must be exactly 10 digits.',
            )
        ]
    )
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name




from django.db import models
from django.urls import reverse

class ProjectPage(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    client_name = models.CharField(max_length=100)
    completion = models.CharField(max_length=100)
    project_type = models.CharField(max_length=100)
    manager = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=200)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)  # Automatically set the field to now when the object is first created
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)  # Automatically set the field to now every time the object is saved

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project_detail', args=[self.slug])


    
class InteriorImage(models.Model):
    project = models.ForeignKey(ProjectPage, related_name='interior_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='projects/interior',null=True, blank=True)

    def __str__(self):
        return f"Interior Image for {self.project.title}"

class ArchitectureImage(models.Model):
    project = models.ForeignKey(ProjectPage, related_name='architecture_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='projects/architecture',null=True, blank=True)

    def __str__(self):
        return f"Architecture Image for {self.project.title}"

class BuildingImage(models.Model):
    project = models.ForeignKey(ProjectPage, related_name='building_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='projects/building',null=True, blank=True)

    def __str__(self):
        return f"Building Image for {self.project.title}"

class ExteriorImage(models.Model):
    project = models.ForeignKey(ProjectPage, related_name='exterior_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='projects/exterior',null=True, blank=True)

    def __str__(self):
        return f"Exterior Image for {self.project.title}"

class ThumbnailImage(models.Model):
    project = models.ForeignKey(ProjectPage, related_name='thumbnail_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='projects/thumbnail',null=True, blank=True)

    def __str__(self):
        return f"thumbnail Image for {self.project.title}"





class BlogPost(models.Model):
    image = models.ImageField(upload_to='blog/images/', blank=True, null=True)
    title = models.CharField(max_length=200)
    content_sort = models.CharField(max_length=200)
    content = RichTextField()
    date = models.DateTimeField()
    author = models.CharField(max_length=100)
    click_count = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, max_length=200)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title.replace(" ", "-"))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blogpost_detail', args=[self.slug])  # Ensure this matches the URL name



class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_open = models.BooleanField(default=True)  # Add this line
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)  # Add slug field

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title.replace(" ", "-"))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('job_detail', args=[self.slug])




class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.job.title}'


class DynamicURL(models.Model):
    path = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    meta_description = models.CharField(max_length=5000, blank=True, null=True)  # Adjusted to a reasonable length
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.path

    def get_absolute_url(self):
        return reverse('dynamic_view', args=[self.path])
    

from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import RegexValidator

class Package(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2)
    package_documents = models.FileField(upload_to='packages')
    # unique=True hata diya kyunki null/blank hone par multiple packages error create karenge
    color_code = models.CharField(max_length=20, blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=200, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Package"
        verbose_name_plural = "Packages"
        
    def get_absolute_url(self):
        return reverse('packagedownload', args=[self.slug])  

class PackageSummary(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='package_summaries')
    summary = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.package.name} - {self.summary}"
    
    class Meta:
        verbose_name = "Package Summary"
        verbose_name_plural = "Package Summaries"


class PackageDownload(models.Model):
    LOOKING_FOR_CHOICES = [
        ('immediate', 'Immediate'),
        ('exploring', 'Just exploring'),
        ('1_month', 'After 1 month'),
        ('3_months', 'After 3 months'),
        ('6_months', 'After 6 months'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^[6-9]\d{9}$', # Sahi Indian phone patterns ko accept karne ke liye
                message='Phone number must be exactly 10 digits and start with 6-9.',
            )
        ]
    )
    looking_for = models.CharField(max_length=20, choices=LOOKING_FOR_CHOICES)
    message = models.TextField(blank=True, null=True) # Optional form step ke liye safe
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PopupImage(models.Model):
    image = models.ImageField(upload_to='popup_images/')
    caption = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.caption if self.caption else 'Popup Image'




class Review(models.Model):

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    name = models.CharField(max_length=100)
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default='male'
    )
    projects = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name