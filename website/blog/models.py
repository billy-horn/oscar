from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE )
	image = models.ImageField(default='default.jpg', upload_to='blog_pics')
	# user = models.OneToOneField(User, on_delete=models.CASCADE)
	metal = models.IntegerField(default=0)
	plastic = models.IntegerField(default=0)
	paper = models.IntegerField(default=0)
	cardboard = models.IntegerField(default=0)
	glass = models.IntegerField(default=0)
	trash = models.IntegerField(default=0)




	def __str__(self):
		return self.title


	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})

	def save(self, *args, **kwargs):
		super().save()

		img = Image.open(self.image.path)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)

class Classifier(models.Model):
	image = models.ImageField(default='default.jpg', upload_to='classify_pics')

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('classify-detail', kwargs={'pk': self.pk})

	def save(self, *args, **kwargs):
		super().save()
		img = Image.open(self.image.path)
		output_size = (384, 512)
		img.thumbnail(output_size)
		img.save(self.image.path)

