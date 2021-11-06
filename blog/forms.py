from django import forms
from .models import Comment


class AddCommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('body',)
		widgets = {
			'body': forms.Textarea(attrs={'class':'form-control'})
		}
		error_messages = {
			'body':{
				'required': 'This fields is required',
			}
		}
		help_texts = {
			'body':'max 400 char'
		}

class AddReplyForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('body',)