# -*- coding: utf-8 -*-

from django import forms
from django.db.models import Q
from emailconfirmation.models import EmailAddress

class EmailForm(forms.Form):
    email = forms.EmailField()

    def __init__(self, user, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean_email(self):
        email = self.cleaned_data['email']

        try:
            email = EmailAddress.objects.get(email=email)
            raise forms.ValidationError(u'Esse e-mail já está sendo usado')
        except EmailAddress.DoesNotExist:
            pass

        return email

    def save(self):
        email =  EmailAddress.objects.add_email(self.user,
            self.cleaned_data['email'])

        if email:
            email.verified = True
            email.set_as_primary()
            EmailAddress.objects.filter(Q(user=self.user) |\
                Q(email=email.email)).exclude(id=email.id).delete()

        return email
