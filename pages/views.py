from datetime import datetime
from django.shortcuts import render, redirect
import random
from django import forms


def is_christmas_today():
    today = datetime.now()
    return "Yes" if today.month == 12 and today.day == 25 else "No"


# Page1 is Main page
def page1(request):
    context = {
        'is_christmas': is_christmas_today()
    }
    return render(request, 'pages/page1.html', context)


class ParticipantForm(forms.Form):
    name = forms.CharField(label='Participant Name', max_length=100)


# Page2 is Secret Santa page
def page2(request):
    participants = request.session.get('participants', [])
    error_message = None

    if request.method == 'POST':
        if 'add_participant' in request.POST:
            error_message = add_participant(request, participants)
        elif 'generate_pairs' in request.POST:
            error_message = generate_pairs(request, participants)
        elif 'reset_game' in request.POST:
            reset_game(request)
            return redirect('page2')

    return render(request, 'pages/page2.html', {
        'participants': participants,
        'pairs': request.session.get('pairs', []),
        'error_message': error_message,
        'form': ParticipantForm()
    })


def add_participant(request, participants):
    # форма для перевірки та очищення вхідних даних
    form = ParticipantForm(request.POST)
    if form.is_valid():
        new_participant = form.cleaned_data['name']
        if new_participant and new_participant not in participants:
            participants.append(new_participant)
            request.session['participants'] = participants
            return None
        return "Already in the list or you entered an empty name."
    return "Invalid form submission."


def generate_pairs(request, participants):
    if len(participants) > 1:
        pairs = generate_secret_santa_pairs(participants)
        request.session['pairs'] = pairs
        return None
    return "A minimum of two participants is required to generate pairs."


def reset_game(request):
    request.session['participants'] = []
    request.session['pairs'] = []
    request.session.modified = True


def generate_secret_santa_pairs(participants):
    givers = list(participants)
    receivers = list(participants)
    random.shuffle(receivers)
    pairs = []
    for giver in givers:
        receiver = receivers.pop(0)
        while receiver == giver:
            receivers.append(receiver)
            receiver = receivers.pop(0)
        pairs.append((giver, receiver))

    return pairs
