from django.shortcuts import render
from django.http import  HttpResponseRedirect, Http404
from django.urls import reverse
from .forms import TopicForm, EntryForm
from .models import Topic, Entry
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    """the main page of learning log"""
    return render(request,'learning_logs/index.html')

# @login_required(login_url='/login/')
# @login_required()
@login_required
def topics(request):
    # print(request,'test')
    """display all the topics"""
    # topics = Topic.objects.order_by('date_added')
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request,'learning_logs/topics.html', context)

@login_required
def topic(request,topic_id):
    """display the single topic and all the related item"""
    topic = Topic.objects.get(id=topic_id)
    # confirm if the topic belongs to owner
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic,'entries':entries}
    return render(request,'learning_logs/topic.html',context)

@login_required
def new_topic(request):
    """add new topic"""
    if request.method != 'POST':
        #not yet submited data and create new one
        form = TopicForm()
    else:
        #To process data when the post submit the data
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            # form.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    context = {'form':form}
    return render(request, 'learning_logs/new_topic.html',context)

@login_required
def new_entry(request,topic_id):
    """Add new item in one specific topic"""
    topic = Topic.objects.get(id = topic_id)

    if request.method != 'POST':
        # create empty form due to not submit data
        form = EntryForm
    else:
        # process data which is submited by POST
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic_id]))
    context = {'topic':topic,'form':form}
    return render(request,'learning_logs/new_entry.html',context)

@login_required
def edit_entry(request,entry_id):
    """edit the exist item"""
    entry = Entry.objects.get(id = entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        #process data which is submited by POST
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic.id]))

    context = {'entry':entry,'topic':topic,'form':form}
    return render(request,'learning_logs/edit_entry.html',context)
