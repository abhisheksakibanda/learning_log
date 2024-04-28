"""
Views for the Learning Log app.
"""
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TopicForm, EntryForm
from .models import Topic, Entry


def index(request):
    """The home page for Learning Log."""
    if request.user.is_authenticated:
        return redirect(to='learning_logs:topics')
    return render(request, template_name='learning_logs/index.html')


@login_required
def all_topics(request):
    """Show all topics."""
    user_topics = ((Topic.objects.filter(owner=request.user) | Topic.objects.filter(public=True))
                   .order_by('date_added'))
    context = {'topics': user_topics}
    return render(request, template_name='learning_logs/topics.html', context=context)


@login_required
def show_topic(request, topic_id):
    """Show a single topic and all its entries."""
    topic = get_object_or_404(Topic, id=topic_id)
    # Make sure the topic belongs to the current user.
    check_topic_owner(topic, request.user)

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, template_name='learning_logs/topic.html', context=context)


@login_required
def add_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            if 'public' in request.POST:
                new_topic.public = True
            new_topic.save()
            return redirect('learning_logs:topics')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, template_name='learning_logs/new_topic.html', context=context)


@login_required
def add_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = get_object_or_404(Topic, id=topic_id)
    check_topic_owner(topic, request.user)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.show_topic = topic
            new_entry.save()
            return redirect(to='learning_logs:topic', topic_id=topic_id)

    # Display a blank or invalid form.
    context = {'topic': topic, 'form': form}
    return render(request, template_name='learning_logs/new_entry.html', context=context)


@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = get_object_or_404(Entry, id=entry_id)
    entry_topic = entry.topic
    check_topic_owner(entry_topic, request.user)

    if request.method != "POST":
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='learning_logs:topic', topic_id=entry_topic.id)

    context = {'entry': entry, 'topic': entry_topic, 'form': form}
    return render(request, template_name='learning_logs/edit_entry.html', context=context)


def check_topic_owner(topic, request_user):
    """
    Check if the topic belongs to the current user.
    """
    if topic.owner != request_user:
        if not topic.public:
            raise Http404
