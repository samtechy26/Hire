from django.db import models
from django.contrib.auth.models import User
from job.models import Job
from PIL import Image
from django.core.validators import MinValueValidator, MaxValueValidator

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default = 'default.png', upload_to='profile_pics')
    tagline = models.CharField(max_length=200,  default='Enter your tagline here')
    bio = models.CharField(max_length=1000, default='Enter your bio here')
    favourite = models.ManyToManyField(User, related_name='favorited_by', blank=True)


    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path) 


class Review(models.Model):
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_frelancer')
    employer = models.ForeignKey(User,on_delete=models.CASCADE, related_name='reviews_employer')
    project = models.ForeignKey(Job, related_name='reviews' , on_delete=models.CASCADE) 
    comment = models.TextField()
    rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    timely = models.BooleanField(default=False)
    on_budget = models.BooleanField(default=False)
    active = models.BooleanField(default = True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return str(self.id)