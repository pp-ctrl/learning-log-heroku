from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
def logout_view(request):
    """logout user"""
    logout(request)
    return HttpResponseRedirect(reverse('learning_logs:index'))


def register(request):
    """register new user"""
    print('request',request.POST)
    if request.method != 'POST':
        # display empty register form
        form = UserCreationForm()
    else:
        #process date which has been filled into form
        form = UserCreationForm(data=request.POST)
        print('form',form)
        print(request.POST['password1'])
        print(request.POST['password2'])
        if form.is_valid():

            new_user = form.save()
            print('valid', new_user)
            # let the user log in automaticall and go to main page
            authenticate_user = authenticate(username=new_user.username,
                                             password=request.POST['password2'])


            login(request,authenticate_user)
            print("authenticate_userauthenticate_user",authenticate_user)
            return HttpResponseRedirect(reverse('learning_logs:index'))
        else:
            print(form.error_messages)
    context = {'form':form}
    return render(request,'users/register.html',context)
