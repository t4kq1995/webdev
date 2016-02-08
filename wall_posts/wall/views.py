from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from wall.models import Message
from django.db import Error
from datetime import datetime


class LoginView(TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('index'))

        return super(LoginView, self).dispatch(request, *args, **kwargs)


class MessageView(TemplateView, View):
    template_name = 'message.html'

    @staticmethod
    def post(request):
        if request.is_ajax():
            if request.POST['status'] == 'main':
                answer = save_post(
                    request.user,
                    request.POST['message']
                )
                if answer:
                    return JsonResponse({'success': True})

            elif request.POST['status'] == 'other':
                answer = save_comment(
                    request.POST['id'],
                    request.user,
                    request.POST['message']
                )
                if answer:
                    return JsonResponse({'success': True})

            elif request.POST['status'] == 'delete':
                answer = delete_post(request.POST['id'])
                if answer:
                    return JsonResponse({'success': True})

            elif request.POST['status'] == 'update':
                answer = update_post(request.POST['id'])
                if answer:
                    return JsonResponse({'success': True})

            return JsonResponse({'success': False})

    def get_context_data(self, **kwargs):
        context = super(MessageView, self).get_context_data(**kwargs)
        context['all_messages'] = Message.objects.filter(parent_id=None).count()
        context['nodes'] = Message.objects.all()
        return context

"""
Helpful functions
"""


def save_post(user, message):
    try:
        Message.objects.create(
            user=user,
            message=message,
            date_save=datetime.now(),
            likes=0,
            parent=None
        ).save()
    except Error:
        return False
    return True


def save_comment(id_post, user, message):
    try:
        parent = Message.objects.get(pk=id_post)
        Message.objects.create(
            user=user,
            message=message,
            date_save=datetime.now(),
            likes=0,
            parent=parent
        ).save()
    except Error:
        return False
    return True


def delete_post(id_post):
    try:
        Message.objects.get(pk=id_post).delete()
    except Error:
        return False
    return True


def update_post(id_post):
    try:
        post = Message.objects.get(pk=id_post)
        post.likes += 1
        post.save()
    except Error:
        return False
    return True
