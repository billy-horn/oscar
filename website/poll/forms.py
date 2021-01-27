from django.forms import ModelForm
from .models import Choice

class PollForm(ModelForm):
	class Meta:
		model = Choice
		fields = ['choice_text', 'votes']