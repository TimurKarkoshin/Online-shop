﻿from django.views.generic.list import ListView
from .models import BrowsingHistory
from django.contrib.auth.mixins import LoginRequiredMixin


class HistoryView(LoginRequiredMixin, ListView):
    template_name = "history/view-histroy.jinja2"
    model = BrowsingHistory
    context_object_name = "history"

    def get_context_data(self, **kwargs):
        context = {"user_histroy": BrowsingHistory.objects.filter(user=self.request.user)}
        return context
