from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Customer(models.Model):

	user 				= models.OneToOneField(
										User,
										on_delete = models.CASCADE,
										null=True,
										blank=True,
										default=None,
									)
	name 				= models.CharField(
								max_length=50,
								blank=True,
								default="",
									)
	mob_no				= models.IntegerField(
								blank=True,
								null=True,
								default=None,
								validators	=	[				#validating that its a 10 digit mobile number
										MinValueValidator(1000000000,message="Please enter a valid mobile number.1"),
										MaxValueValidator(9999999999,message="Please enter a valid mobile number.2")
										]
									)

	def __str__(self):		#ensuring human readable title for the user in django admin
		return str(self.mob_no)+' '+self.name


#on creation of user customer instance is created as well
@receiver(post_save, sender = User)
def create_user_customer(sender, instance, created, **kwargs):
	if created:
		# print("CREATE USER CUSTOMER CALLED \n")
		# print(sender)
		# # print(instance)
		# print(created)
		Customer.objects.create(user=instance)

@receiver(post_save, sender = User)
def update_user_customer(sender, instance, **kwargs):
	instance.customer.save()
