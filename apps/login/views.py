from django.shortcuts import render,redirect
from .models import User,Comment,Message
from django.contrib import messages
import bcrypt



def index(request):
    return render(request,'login/login.html')

def success(request):
    if not 'userid' in request.session:
        messages.error(request, "Please log in")
        return redirect('/')
    return render(request,'login/success.html')

def wall(request):
    if not 'userid' in request.session:
        messages.error(request,'Please log in')
        return redirect('/')
    context = {
        'x' : Message.objects.all(),
        'y' : Comment.objects.all(),
    }
    return render (request,'login/wall.html',context)


def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            # redirect the user back to the form to fix the errors
        return redirect('/')
    hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],birthday=request.POST['birthday'],password=hash1)
    request.session['userid']=User.objects.last().id
    request.session['fname']=User.objects.last().first_name
    messages.error(request, "Successfully registered")
    return redirect('/success')


def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            # redirect the user back to the form to fix the errors
        return redirect('/')		
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['userid']=user.id
        request.session['fname']=user.first_name
        messages.error(request, "Successfully loged in")
        return redirect('/success')

def login_wall(request):
    return redirect('/wall')

def post(request):
    user = User.objects.get(id=request.session['userid'])
    print(user)
    Message.objects.create(message=request.POST['message'],user=user)
    return redirect('/wall')

def post_comment(request,id):
    user=User.objects.get(id=request.session['userid'])
    message = Message.objects.get(id=id)
    Comment.objects.create(comment=request.POST['comment'],user=user,message=message)
    return redirect('/wall')

def delete(request,id):
    x=Message.objects.get(id=id)
    x.delete()
    return redirect('/wall')
        

def log_out(request):
    request.session.clear()
    return redirect('/')
def leave(request):
    request.session.clear()
    return redirect('/')

# Create your views here.
