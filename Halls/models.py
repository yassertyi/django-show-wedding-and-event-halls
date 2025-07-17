from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone


class Client(models.Model):
    name = models.CharField(max_length=250)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=180)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.name


class Halls(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='halls')
    name = models.CharField(max_length=250)
    capacity = models.IntegerField()
    price = models.IntegerField()
    address = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, unique=True)
    body = models.TextField(default='Default Text', blank=True)
    photo = models.ImageField(upload_to='images/%Y', blank=True, null=True)
    active = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now) 

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()  
        super(Halls, self).save(*args, **kwargs)

    def generate_unique_slug(self):
        base_slug = slugify(self.name)
        slug = base_slug
        num = 1

        while Halls.objects.filter(slug=slug).exists():
            slug = f'{base_slug}-{num}'
            num += 1

        return slug    

    def get_absolute_url(self):
        return reverse('halls:halls_detail', args=[self.slug])

    def __str__(self):
        return self.name



class Shar(models.Model):
    halls = models.ForeignKey(Halls, on_delete=models.CASCADE, related_name='shar')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Shar by {self.name} on {self.halls}'
    
    def get_absolute_url(self):
        return reverse('halls:shar_detail', args=[self.id])
