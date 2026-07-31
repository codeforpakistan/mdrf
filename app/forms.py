from allauth.account.forms import LoginForm, SignupForm
from django import forms
from mptt.forms import TreeNodeChoiceField

from app.models import Disaster, Hazard, Subscription


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Assign classes to specific fields
        self.fields["login"].widget.attrs.update({"class": "form-control"})
        self.fields["password"].widget.attrs.update({"class": "form-control"})


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Assign classes to specific fields
        # self.fields["phone"].widget.attrs.update({"class": "form-control"})
        self.fields["email"].widget.attrs.update({"class": "form-control"})
        self.fields["username"].widget.attrs.update({"class": "form-control"})
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})


# class CustomPasswordForm(SignupForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Assign classes to specific fields
#         # self.fields["phone"].widget.attrs.update({"class": "form-control"})
#         self.fields["email"].widget.attrs.update({"class": "form-control"})
#         # self.fields["username"].widget.attrs.update({"class": "form-control"})
#         # self.fields["password1"].widget.attrs.update({"class": "form-control"})
#         # self.fields["password2"].widget.attrs.update({"class": "form-control"})


class SubscriptionForm(forms.ModelForm):
    hazard = TreeNodeChoiceField(queryset=Hazard.objects.all())
    class Meta:
        model = Subscription
        fields = ["hazard","disaster"]
        widgets = {
            "hazard": forms.Select(attrs={"class": "form-select"}),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Pull live data directly when the form instantiates
    #     self.fields['disaster'].choices = [
    #         (disaster.id, disaster.name) for disaster in Disaster.objects.all()
    #     ]