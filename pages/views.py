from datetime import datetime
from django.shortcuts import render
import random
from django import forms


def is_christmas_today():
    today = datetime.now()
    if today.month == 12 and today.day == 25:
        return "Yes"
    else:
        return "No"


# Page1 is Main page
def page1(request):
    context = {
        'is_christmas': is_christmas_today()
    }
    return render(request, 'pages/page1.html', context)


class ParticipantForm(forms.Form):
    name = forms.CharField(label='Participant Name', max_length=100)


# Page2 is secret santa page
def page2(request):
    participants = request.session.get('participants', [])
    error_message = None

    if request.method == 'POST':
        if 'add_participant' in request.POST:
            new_participant = request.POST.get('name')
            if new_participant and new_participant not in participants:
                participants.append(new_participant)
                request.session['participants'] = participants
            else:
                error_message = "Already in the list or you entered an empty name."

        elif 'generate_pairs' in request.POST:
            if len(participants) > 1:
                pairs = generate_secret_santa_pairs(participants)
                request.session['pairs'] = pairs
            else:
                error_message = "A minimum of two participants to generate pairs."

        elif 'reset_game' in request.POST:
            request.session['participants'] = []
            request.session['pairs'] = []
            participants = []

    pairs = request.session.get('pairs', [])

    return render(request, 'pages/page2.html', {
        'participants': participants,
        'pairs': pairs,
        'error_message': error_message,
    })


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
