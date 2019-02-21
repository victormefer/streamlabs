from django.shortcuts import render


def events(request):
    context = {'streamer': request.POST.get('favorite')}
    return render(request, 'events/events.html', context=context)
