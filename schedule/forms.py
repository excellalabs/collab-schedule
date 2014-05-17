from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import TimeAway

class TimeAwayForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(TimeAwayForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_action = 'time_away'

		self.helper.add_input(Submit('submit', 'Submit'))

	class Meta: 
		model = TimeAway
		fields = ['date']