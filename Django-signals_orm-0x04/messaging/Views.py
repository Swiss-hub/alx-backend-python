# Django-Chat/views.py

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponseForbidden

User = get_user_model()

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('account_deleted')  # Or any page you want
    return HttpResponseForbidden("Only POST allowed.")

# c:\Users\ABC\Desktop\ALX\alx-backend-python\Django-signals_orm-0x04\messaging\views.py