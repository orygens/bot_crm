# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from apps.utils.shortcuts import render
from coffin.shortcuts import redirect
from account.forms import EmailForm
from emailconfirmation.models import EmailAddress

@login_required
def email(request):
    try:
        email = EmailAddress.objects.get(user=request.user)
    except EmailAddress.DoesNotExist:
        email = None

    if request.method == 'POST':
        form = EmailForm(request.user, request.POST)

        if form.is_valid():
            form.save()

            return redirect('account_email')
    else:
        form = EmailForm(request.user)

    return render(request, 'account/email.html', {'email': email, 'form': form})
