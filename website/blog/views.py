from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
	ListView,
	DetailView, 
	CreateView,
	UpdateView,
	DeleteView,
)
from .models import Post, Classifier

from django.urls import reverse_lazy
from django.contrib import messages

import numpy as np
# import matplotlib.pyplot as plt
from PIL import Image
import tensorflow as tf
# import os
# import PIL
# from pathlib import Path
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras import utils


def home(request):
	context = {
		'posts': Post.objects.all()
	}
	return render(request, 'blog/home.html', context)


class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 6

	# if request.GET.get('Next') == 'Next':
	# 	print('user clicked summary')

class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_posts.html'
	context_object_name = 'posts'
	paginate_by = 6

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
	model = Post

class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
	model = Post
	fields = ['title', 'image']
	success_message = "%(title)s was created successfully."

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content']
	success_message = "%(title)s was updated successfully."


	def form_valid(self, form):
		form.instance.author = self.request.user
		obj = self.get_object()
		return super(PostUpdateView, self).form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False



# Working post delete with success message!
# Help and code taken from link below:
# https://stackoverflow.com/questions/48777015/djangos-successmessagemixin-not-working-with-deleteview
class PostDeleteView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'
	success_message = "%(title)s was removed successfully."


	def delete(self, request, *args, **kwargs):
		obj = self.get_object()
		messages.success(self.request, self.success_message % obj.__dict__)
		return super(PostDeleteView, self).delete(request, *args, **kwargs)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class ClassifyCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
	model = Classifier
	fields = ['image']
	# success_url = "/classify/detail"
	success_message = "Image was successfully uploaded."
	template_name = 'blog/classify_form.html'

	# img_height = 384
	# img_width = 512

	# classes = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']
	# new_model = tf.keras.models.load_model('tf_models/model-75-67')
	# new_img_path = 'media/classify_pics/beercan.png'
	# img = keras.preprocessing.image.load_img(
	#     new_img_path, target_size=(img_height, img_width)
	# )
	# img_array = keras.preprocessing.image.img_to_array(img)
	# img_array = tf.expand_dims(img_array, 0) # Create a batch

	# predictions = new_model.predict(img_array)
	# score = tf.nn.softmax(predictions[0])
	# max_class = classes[np.argmax(score)]
	# max_score = 100 * np.max(score)
	# def get(self, *args, **kwargs):
	# 	print('Processing GET request')
	# 	resp = super().get(*args, **kwargs)
	# 	print('Finished processing GET request')
	# 	return render(resp, self.template_name, {'form': form})
	# 	# return resp
# if form.is_valid():
#     image = form.save() # this creates the model, the upload paths are created here!
#     image.patient = patient
#     image.enhanced.save("enhanced_" + image.original.name, main(image.original.path)) # I made this up to avoid conflicts in your storage
#     image.segmented.save("segmented_" + image.original.name, segment(image.enhanced.path))
#     image.save() # this updates the model with the new images
#     messages.success(request,"Image added successfully!") # I moved this here, more accurate, in case save fails....
#     return HttpResponseRedirect(reverse_lazy('patients:patient_detail', kwargs={'pk' : image.patient.pk}))

	def form_valid(self, form):
		form.instance.author = self.request.user
		# image = form.save()
		# image.save()
		# form.instance.image = self.image
		return super().form_valid(form)



# class ClassifyCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
# 	model = Classifier
# 	fields = ['image']
# 	# success_url = "/classify/detail"
# 	success_message = "Image was successfully uploaded."
# 	template_name = 'blog/classify_form.html'

# 	img_height = 384
# 	img_width = 512

# 	classes = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']
# 	new_model = tf.keras.models.load_model('tf_models/model-75-67')
# 	new_img_path = 'media/classify_pics/beercan.png'
# 	img = keras.preprocessing.image.load_img(
# 	    new_img_path, target_size=(img_height, img_width)
# 	)
# 	img_array = keras.preprocessing.image.img_to_array(img)
# 	img_array = tf.expand_dims(img_array, 0) # Create a batch

# 	predictions = new_model.predict(img_array)
# 	score = tf.nn.softmax(predictions[0])
# 	max_class = classes[np.argmax(score)]
# 	max_score = 100 * np.max(score)


# 	def form_valid(self, form):
# 		form.instance.author = self.request.user
# 		return super().form_valid(form)



class ClassifyDetailView(DetailView):
	model = Classifier
	template_name = 'blog/classify_detail.html'
	img_height = 384
	img_width = 512


	def image_predict(request):
		fileObj=request.FILES['filePath']
		fs=FileSystemStorage()
		filePathName=fs.save(fileObj.name,fileObj)
		filePathName=fs.url(filePathName)
		return '.'+filePathName

	classes = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']
	new_model = tf.keras.models.load_model('tf_models/model-75-67')
	new_img_path = 'media/classify_pics/beercan.png'
	# new_img_path = Image.open(post.instance.image)

	img = keras.preprocessing.image.load_img(
	    new_img_path, target_size=(img_height, img_width)
	)
	img_array = keras.preprocessing.image.img_to_array(img)
	img_array = tf.expand_dims(img_array, 0) # Create a batch

	predictions = new_model.predict(img_array)
	score = tf.nn.softmax(predictions[0])
	max_class = classes[np.argmax(score)]
	max_score = round(100 * np.max(score), 2)

	print(
	    "This image most likely belongs to {} with a {:.2f} percent confidence."
	    .format(classes[np.argmax(score)], 100 * np.max(score))
	)

	# def get(self, *args, **kwargs):
	# 	print('Processing GET request')
	# 	resp = super().get(*args, **kwargs)
	# 	print('Finished processing GET request')
	# 	return render(resp, self.template_name, {'form': form})
		# return resp

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		data['max_class'] = self.max_class
		data['max_score'] = self.max_score
		# data['image_path'] = self.new_img_path
		data['image_path'] = self.model.image
		return data
	# def get_context_data(self, **kwargs):
	# 	context = super(ClassifyDetailView, self).get_context_data(**kwargs)
	# 	context['max_class']= self.request.
	# 	return context
	# return render(request, 'classify_detail.html', {"max_score": max_score, "max_class": max_class})




	# img_height = 384
	# img_width = 512
	# new_model = tf.keras.models.load_model('tf_models/model-75-67')
	# new_img_path = model.image
	# img = keras.preprocessing.image.load_img(
	#     new_img_path, target_size=(img_height, img_width)
	# )
	# img_array = keras.preprocessing.image.img_to_array(img)
	# img_array = tf.expand_dims(img_array, 0) # Create a batch

	# predictions = model.predict(img_array)
	# score = tf.nn.softmax(predictions[0])

	# print(
	#     "This image most likely belongs to {} with a {:.2f} percent confidence."
	#     .format(classes[np.argmax(score)], 100 * np.max(score))
	# )

def classify(request):
	img_height = 384
	img_width = 512

	classes = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']
	new_model = tf.keras.models.load_model('tf_models/model-75-67')
	# new_img_path = 'media/classify_pics/beercan.png'
	new_img_path = 'media/classify_pics/beercan.png'

	img = keras.preprocessing.image.load_img(
	    new_img_path, target_size=(img_height, img_width)
	)
	img_array = keras.preprocessing.image.img_to_array(img)
	img_array = tf.expand_dims(img_array, 0) # Create a batch

	predictions = new_model.predict(img_array)
	score = tf.nn.softmax(predictions[0])
	max_class = classes[np.argmax(score)]
	max_score = 100 * np.max(score)
	return render(request, 'classify_detail.html', {"max_score": max_score, "max_class": max_class})




def about(request):
	return render(request, 'blog/about.html', {'title': 'About'})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


