from django.views import View
from django.shortcuts import render, redirect
from hypercar import settings


class WelcomeView(View):
    def get(self, request):
        return render(request, 'tickets/welcome.html')


class MenuView(View):
    def get(self, request):
        return render(request, 'tickets/menu.html')


class Next(View):
    def get(self, request):
        return render(request, 'tickets/next.html', context={'ticket': settings.next_ticket})


class Processing(View):
    def get(self, request):
        context = {
            'oil_que': len(settings.service['change_oil']),
            'tires_que': len(settings.service['inflate_tires']),
            'diagnostic_que': len(settings.service['diagnostic']),
        }
        return render(request, 'tickets/processing.html', context=context)

    def post(self, request):
        #Next_ticket is for /next page showing of the ticket being processed
        if len(settings.service['change_oil']) > 0:
            settings.next_ticket = settings.service['change_oil'].popleft()
        elif len(settings.service['inflate_tires']) > 0:
            settings.next_ticket = settings.service['inflate_tires'].popleft()
        elif len(settings.service['diagnostic']) > 0:
            settings.next_ticket = settings.service['diagnostic'].popleft()
        else:
            settings.next_ticket = -1

        return redirect('/next')


class Service(View):
    def get(self, request, link):
        template_name = 'tickets/service.html'
        if settings.ticket_numbers == 0:
            settings.ticket_numbers = 1
            minutes_to_wait = 0
        else:
            settings.ticket_numbers += 1
            if link == 'change_oil':
                minutes_to_wait = 2 * len(settings.service['change_oil'])
            elif link == 'inflate_tires':
                minutes_to_wait = 2 * len(settings.service['change_oil']) + 5 * len(settings.service['inflate_tires'])
            elif link == 'diagnostic':
                minutes_to_wait = 2 * len(settings.service['change_oil']) + 5 * len(settings.service['inflate_tires']) + \
                    30 * len(settings.service['diagnostic'])

        settings.service[link].append(settings.ticket_numbers)

        context = {
            'ticket_numbers': settings.ticket_numbers,
            'minutes_to_wait': minutes_to_wait
        }

        return render(request, template_name, context)

