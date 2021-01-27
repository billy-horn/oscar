from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Post, Classifier

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
	if created:
		Post.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, *args, **kwargs):
	instance.post.save()

@receiver(post_save, sender=User)
def create_image(sender, instance, created, *args, **kwargs):
	if created:
		Classifier.objects.create(user=instance)
