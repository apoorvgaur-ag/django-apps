from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Customer


class CustomerLoginForm(forms.ModelForm):
	class Meta:
		model 				= Customer
		fields				= {
								'name',
								'mob_no',
					}
		widgets				= {
								'name': forms.TextInput(attrs={
										'placeholder' : 'Name',
									}),
								'mob_no': forms.TextInput(attrs={
										'value' : '',
										'placeholder' : 'Mobile Number',
									}),
					}

	def clean(self):						#for ensuring cleaned data and validation
		cleaned_data = super().clean()
		name = cleaned_data.get("name")
		mob_no = cleaned_data.get("mob_no")
		if name == "":
			raise ValidationError("Please enter a valid name")
		mobno_validity = mob_no < 9999999999 and mob_no >1000000000
		if not mobno_validity:
			raise ValidationError("Please enter a valid mobile number! Testing.....")

		return cleaned_data

	def check_login_name(self, user_obj, name):			#for checking that the inputed name is the same as stored name in case of entry existing prior to the current login
		stored_name = user_obj.customer.name
		formatted_stored_name = stored_name.lower()
		formatted_input_name = name.lower()
		if formatted_input_name == formatted_stored_name:
			return True
		else:
			self.add_error('name', ValidationError("Please enter the correct name!") )

		return False
