# -*- coding: utf-8 -*-

from django.template import RequestContext
from coffin.shortcuts import render_to_response

def render(request, template_name, extra_context=None):
    return render_to_response(template_name, extra_context,
        context_instance=RequestContext(request))
