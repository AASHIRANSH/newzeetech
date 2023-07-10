from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm, EditUserProfileForm, EditAdminProfileForm, SignInForm, ProfileUpdateForm
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm, UserChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash


#Registration
def sign_up(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = SignUpForm(request.POST)
            if fm.is_valid() :
                fm.save()
                messages.success(request,'Your Account was Created!')
                return HttpResponseRedirect('/users/signin/')
                # messages.add_message(request, messages.SUCCESS, 'Your Account Has Been Created!')
        else:
            fm = SignUpForm()
        return render(request, "sign_up.html", {'fm':fm})
    else:
        return HttpResponseRedirect('/users/profile')


'''Sign In / Login'''
def sign_in(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            # fm = AuthenticationForm(request=request, data=request.POST)
            fm = SignInForm(request=request, data=request.POST) #custom login form
            if fm.is_valid() :
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request,'Loggen-In Successfully!')
                    return HttpResponseRedirect('/users/profile/')
                # messages.add_message(request, messages.SUCCESS, 'Your Account Has Been Created!')
        else:
            # fm = AuthenticationForm()  
            fm = SignInForm() #custom login form#custom login form
        return render(request, "sign_in.html", {'form':fm})
    else:
        return HttpResponseRedirect('/users/profile/')
        

def user_profile(request):
    if request.user.is_authenticated:

        if request.method == 'POST':

            if request.user.is_superuser == True:
                fm = EditAdminProfileForm(request.POST, instance=request.user)
            else:
                fm = EditUserProfileForm(request.POST, instance=request.user)

            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            
            if fm.is_valid() and p_form.is_valid():
                fm.save()
                p_form.save()
                messages.success(request, f'Profile updated!!')
            return HttpResponseRedirect('/users/profile')
        else:
            if request.user.is_superuser == True:
                fm = EditAdminProfileForm(instance=request.user)
            else:
                fm = EditUserProfileForm(instance=request.user)

            p_form = ProfileUpdateForm(instance=request.user.profile)

        vars = {
            'form':fm,
            'p_form': p_form,
            'user':request.user
        }

        return render(request, "profile.html", vars)
    
    else:
        return HttpResponseRedirect('/users/signin')
    

def user_detail(request, id):
    if request.user.is_authenticated:
        pi = User.objects.get(pk=id)
        if request.user.is_superuser == True:
            fm = EditAdminProfileForm(instance=pi)
        else:
            fm = EditUserProfileForm(instance=pi)
        vars = {
            'form':fm
        }
        return render(request, "userdetail.html", vars)
    else:
        return HttpResponseRedirect('/users/signin')


def sign_out(request):
    logout(request)
    return HttpResponseRedirect('/users/signin')

'''change password with old password'''
def change_password(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = PasswordChangeForm(user=request.user, data=request.POST)
            if fm.is_valid() :
                fm.save()
                update_session_auth_hash(fm.user)
                messages.success(request,'Password was changed Successfully!')
                return HttpResponseRedirect('/users/profile')
        else:
            fm = PasswordChangeForm(user=request.user)
        vars = {
            'form':fm
        }
        return render(request, "change_password.html", vars)
    else:
        return HttpResponseRedirect('/users/signin')

'''change password without old password'''
def change_password2(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = SetPasswordForm(user=request.user, data=request.POST)
            if fm.is_valid() :
                fm.save()
                update_session_auth_hash(fm.user)
                messages.success(request,'Password was changed Successfully!')
                return HttpResponseRedirect('/users/profile')
        else:
            fm = SetPasswordForm(user=request.user)
        vars = {
            'form':fm
        }
        return render(request, "change_password.html", vars)
    else:
        return HttpResponseRedirect('/users/signin')


def custom_url(request, year):
    vars = {'year':year}
    return render(request, 'custom_url.html', vars)