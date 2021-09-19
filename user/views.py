from django.shortcuts import render

from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

from .forms import CustomerLoginForm

# Create your views here.
class LoginView(View):
	template_name = 'login.html'
	customer_form_class = CustomerLoginForm

	def get(self, request, *args, **kwargs):
		customer_form = self.customer_form_class()
		context = {
					'customer_form' : customer_form,
				}
		return render( request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		context = {}

		if 'menu_login_form_submit' in request.POST:
			customer_form = self.customer_form_class(request.POST)
			if customer_form.is_valid():
				data = customer_form.cleaned_data
				try:			#try this to check if the user exists, if it is a new user then authenticate step will throw an exception
					user_obj = User.objects.get(username=data["mob_no"])
					# check for correct credentials otherwise reject the login info
					if customer_form.check_login_name(user_obj=user_obj, name=data["name"]):
						username = user_obj.username
						password = "<Your chosen password, common for all users>"
						user = authenticate(username=username,password=password)
						if user is not None:			#user authentication is complete
							login(request,user)
						return HttpResponseRedirect('<next page url>')
					

				except User.DoesNotExist: #if the user is new
					new_user = User.objects.create_user(data["mob_no"],password="<Your chosen password, common for all users>")
					new_user.save()
					new_user.refresh_from_db() #this step is very important
					new_user.customer.name = data["name"]
					new_user.customer.mob_no = data["mob_no"]
					new_user.save()
					username = new_user.username
					password = "<your password>"
					user = authenticate(username=username,password=password)
					if user is not None:		#loggin in after creating the new user as the user willl be directed towards the next page
						login(request,user)
					return HttpResponseRedirect('<next page url>')


# take care of previous created user and new user as well. Need to save the forms accordingly

		context['customer_form'] = customer_form

		return render(request, self.template_name, context)		#incase of errors



