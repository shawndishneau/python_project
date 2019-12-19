from django.shortcuts import render, HttpResponse, redirect
from . models import User, Party, Messages, Comments
from django.contrib import messages
import bcrypt
import datetime

def welcome(request):
    if request.session.flush():
        if 'userid' not in request.session:
            request.session['userid'] = ''
    return render(request, 'project_app/welcome.html')

def registrationprocess(request):
    if request.method != 'POST':
        return redirect('/') 
    errors = User.objects.validate_registration(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
        request.session['userid'] = user.id 
        return redirect('/dashboard')

def loginprocess(request):
    if request.method != 'POST':
        return redirect('/')
    errors = User.objects.validate_login(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    else:
        user = User.objects.get(email= request.POST['log_email'])
        request.session['userid'] = user.id 
        return redirect('/dashboard')

def dashboard(request):
    if 'userid' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['userid']),
        'my_parties': Party.objects.filter(participant__id=request.session['userid']),
        # participant is the ManyToManyField
        'avail_parties': Party.objects.exclude(participant__id=request.session['userid']),
        # participant is the ManyToManyField
    }
    return render(request,'project_app/dashboard.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

def removeparty_process(request, id):
    if request.session['userid'] == '':
        return redirect('/')
    errors = Party.objects.validate_route(id)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/dashboard')
    this_party = Party.objects.get(id=int(id))
    # this_user = User.objects.get(id= request.session['userid'])
    if this_party.creator.id == request.session['userid']:
        this_party.delete()
        return redirect('/dashboard')
    return redirect('/dashboard')

def editinfo(request, id):
    if request.session['userid'] == '':
        return redirect('/')
    errors = Party.objects.validate_route(id)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/dashboard')
    context = {
        'user': User.objects.get(id=request.session['userid']),
        'party': Party.objects.get(id=int(id)),
    }
    return render(request, 'project_app/editparty.html', context)

def partyedit_process(request, id):
    if request.session['userid'] == '':
        return redirect('/')
    errors = Party.objects.validate_route(id)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            # extra_tags=key make errors look good when they show up on the screen
            # errors won't show up on both sides now
        return redirect('/dashboard')
    this_party = Party.objects.get(id=int(id))
    if this_party.creator.id != request.session['userid']:
        # creator comes from the foreign key field
        return redirect('/dashboard')
    errors = Party.objects.validate_party(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/party/'+id+'/editinfo')
    else:
        this_party.title=request.POST['title']
        this_party.description=request.POST['description']
        this_party.address=request.POST['address']
        this_party.city=request.POST['city']
        this_party.state=request.POST['state']
        this_party.zip_code=request.POST['zip_code']
        this_party.date=request.POST['date']
        # this_party.rating=request.POST['rating']
        this_party.updated_at = datetime.datetime.now()
        this_party.save()
        return redirect('/dashboard')

def newparty(request):
    if request.session['userid'] == '':
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['userid']),
    }
    return render(request, 'project_app/newparty.html', context)

def makeparty_process(request):
    if request.session['userid'] == '':
        return redirect('/')
    errors = Party.objects.validate_party(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            # extra_tags=key make errors look good when they show up on the screen
            # errors won't show up on both sides now
        return redirect('/party/new')
    else:
        this_user = User.objects.get(id=request.session['userid'])
        this_party = Party.objects.create(title=request.POST['title'], description=request.POST['description'], address=request.POST['address'], city=request.POST['city'], 
        state=request.POST['state'], zip_code=request.POST['zip_code'], date=request.POST['date'], creator=this_user)
        # creator comes from the foreign key from far left
        this_party.participant.add(this_user)
        # participant is the many to many field from far left
        this_party.save()
        return redirect('/dashboard')

def joinparty_process(request, id):
    if request.session['userid'] == '':
        return redirect('/')
    errors = Party.objects.validate_route(id=int(id))
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/dashboard')
    this_party = Party.objects.get(id=int(id))
    this_user = User.objects.get(id=request.session['userid'])
    user_parties = Party.objects.filter(participant=this_user)
    # participant is the ManyToManyField
    if this_party in user_parties:
        return redirect('/dashboard')
    else:
        this_party.participant.add(this_user)
        this_party.save()
        return redirect('/dashboard')

def partyinfo(request, id):
    if request.session['userid'] == '':
        return redirect('/')
    errors = Party.objects.validate_route(id)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/dashboard')
    party = Party.objects.get(id=int(id))
    user = User.objects.get(id=request.session['userid'])
    context = {
        'party': party,
        'user': user,
        'participants': User.objects.filter(party_joined=party),
        'acreator':Party.objects.get(id = int(id)).creator.id,
        'else': User.objects.filter(party_joined=party).exclude(id=Party.objects.get(id = int(id)).creator.id),
    }
    return render(request, 'project_app/partyinfo.html', context)

def cancelparty_process(request, id):
    if request.session['userid'] == '':
        return redirect('/')
    errors = Party.objects.validate_route(id)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/dashboard')
    this_party = Party.objects.get(id=int(id))
    this_user = User.objects.get(id=request.session['userid'])
    user_parties = Party.objects.filter(participant=this_user)
    # participant is the ManyToManyField
    if this_party not in user_parties:
        return redirect('/dashboard')
    else:
        this_party.participant.remove(this_user)
        # participant is the ManyToManyField
        this_party.save()
        return redirect('/dashboard')

def writemessage(request, id):
    if request.session['user'] == '':
        return redirect('/')
    logged_user = User.objects.get(id=request.session['user'])
    this_party = Party.objects.get(id=int(id))
    user_messages = Messages.objects.all()
    user_comments = Comments.objects.all()
    context = {
        'current_user': logged_user,
        'this_party': this_party,
        'user_messages': user_messages,
        'user_comments': user_comments,
    }
    return render(request, "project_app/messageboard.html", context)

# def writemessage(request):
#     if request.session['user'] == '':
#         return redirect('/')
#     logged_user = User.objects.get(id=request.session['user'])
#     user_messages = Messages.objects.all()
#     user_comments = Comments.objects.all()
#     context = {
#         'current_user': logged_user,
#         'user_messages': user_messages,
#         'user_comments': user_comments,
#     }
#     return render(request, "thewall_app/wall.html", context)

# def addmessage_process(request):
#     if request.session['user'] == '':
#         return redirect('/')
#     errors = Messages.objects.message_validator(request.POST)
#     if len(errors) > 0:
#         for key, value in errors.items():
#             messages.error(request, value)
#         return redirect('/wall')
#     user = User.objects.get(id=request.session['user'])
#     Messages.objects.create(message=request.POST['message'], user=user)
#     return redirect('/wall')

# def addcomments_process(request):
#     if request.session['user'] == '':
#         return redirect('/')
#     errors = Comments.objects.comment_validator(request.POST)
#     if len(errors) > 0:
#         for key, value in errors.items():
#             messages.error(request, value)
#         return redirect('/wall')
#     user = User.objects.get(id=request.session["user"])
#     message = Messages.objects.get(id=request.POST['msgid'])
#     Comments.objects.create(comment=request.POST['comment'], commenttomessage=message, commentmaker = user)
#     return redirect('/wall')