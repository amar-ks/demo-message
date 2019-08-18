from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from webmessage.forms import RegisterForm, EmailForm
from webmessage.models import EmailBox
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/webmessage/index/')
    else:
        if request.method == "POST":
            form = RegisterForm(request.POST or None)
            if form.is_valid():
                user = form.save(commit=False)
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user.set_password(password)
                user.save()
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return render(request, 'webmessage/index.html')
        else:
            form = RegisterForm()

        context = {
            "form": form,
        }
        return render(request, 'webmessage/register.html', context)


def login_user(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/webmessage/index/')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            print(username)
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)

                    return HttpResponseRedirect('/webmessage/index/')
                else:
                    return render(request, 'webmessage/login.html', {'error_message': 'Your account has been disabled'})
            else:
                return render(request, 'webmessage/login.html', {'error_message': 'Invalid login'})
        return render(request, 'webmessage/login.html')


def logout_user(request):
    logout(request)
    form = RegisterForm(request.POST or None)
    context = {
        "form": form,
        "error_message": "Successfully logout!"
    }
    return render(request, 'webmessage/login.html', context)


def compose(request):
    if not request.user.is_authenticated:
        return render(request, 'webmessage/login.html')
    else:
        form = EmailForm(request.POST or None, request.FILES or None)
        # print(form)
        if form.is_valid():
            compose_message = form.save(commit=False)
            compose_message.user = request.user
            # print(compose_message.sender_name)
            context = {
                'compose_message': compose_message,
                'form': form,
                'message': 'Message sent',
            }
            compose_message.save()
            return render(request, 'webmessage/compose.html', context)

        context = {
            'form': form
        }
        return render(request, 'webmessage/compose.html', context)


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'webmessage/login.html')
    else:
        messages = EmailBox.objects.all().order_by('created_date')
        if messages:
            paginator = Paginator(messages, 1)
            page = request.GET.get('page', 1)

            try:
                message_list = paginator.page(page)
            except PageNotAnInteger:
                message_list = paginator.page(1)
            except EmptyPage:
                message_list = paginator.page(paginator.num_pages)
            context = {
                'messages': messages,
                'message_list': message_list
            }

            return render(request, 'webmessage/index.html', context)
        else:
            return render(request, 'webmessage/index.html')


def outbox(request):
    if not request.user.is_authenticated:
        return render(request, 'webmessage/login.html')
    else:
        messages = EmailBox.objects.filter(user=request.user).order_by('created_date')
        if messages:
            paginator = Paginator(messages, 1)
            page = request.GET.get('page', 1)

            try:
                message_list = paginator.page(page)
            except PageNotAnInteger:
                message_list = paginator.page(1)
            except EmptyPage:
                message_list = paginator.page(paginator.num_pages)
            context = {
                'messages': messages,
                'message_list': message_list
            }
            return render(request, 'webmessage/outbox.html', context)
        else:
            return render(request, 'webmessage/outbox.html')


def detail(request, message_id):
    if not request.user.is_authenticated:
        return render(request, 'webmessage/login.html')
    else:
        # print(message_id)
        user = request.user
        msg = get_object_or_404(EmailBox, pk=message_id)
        return render(request, 'webmessage/detail.html', {'msg': msg, 'user': user})


def delete_message(request, message_id):
    if not request.user.is_authenticated:
        return render(request, 'webmessage/login.html')
    else:
        msg = EmailBox.objects.get(pk=message_id)
        msg.delete()

        return HttpResponseRedirect('/webmessage/index')
