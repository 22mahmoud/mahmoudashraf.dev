import logging

from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.template.response import TemplateResponse
from django.views import View
from django_htmx.http import HttpResponseClientRedirect
from wagtail.models import Page

from .forms import GuestbookForm
from .tasks import optimize_guestbook_html

logger = logging.getLogger(__name__)


class GuestbookView(View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        form = GuestbookForm(request.POST)
        is_htmx = request.htmx

        if form.is_valid():
            guestbook = form.save(commit=False)
            guestbook.message_html = form.render_message()
            guestbook.save()
            result = optimize_guestbook_html.enqueue(guestbook.id)  # type: ignore

            if result.errors:
                logger.warning(result.errors)

            if is_htmx:
                return HttpResponseClientRedirect("/guestbook")

            page = self.get_page(request)
            return redirect("/guestbook")

        if is_htmx:
            return render(request, "includes/guestbook_form.html", {"form": form})

        page = self.get_page(request)
        page_context = page.get_context(request)
        page_context["form"] = form

        return render(request, page.template, page_context)

    def get_page(self, request):
        page_id = request.POST.get("page_id")
        if not page_id:
            raise Http404("Page not specified")

        try:
            return Page.objects.live().public().get(id=page_id).specific  # type: ignore
        except Page.DoesNotExist:
            raise Http404("Page not found")

    def build_redirect_url(self, request, page):
        redirect_url = page.get_url(request)
        fragment = request.POST.get("source_url_fragment")
        if fragment and fragment.startswith("#"):
            redirect_url += fragment
        return redirect_url


def validate_guestbook_field(request):
    if request.method != "POST" or not request.headers.get("HX-Request"):
        return HttpResponseBadRequest("Invalid request")

    triggering_element_id = request.htmx.trigger
    if not triggering_element_id:
        return HttpResponseBadRequest("Missing trigger ID in htmx request.")

    field_name = triggering_element_id.removesuffix("-wrapper")

    form = GuestbookForm(request.POST)
    form.is_valid()

    if field_name not in form.fields:
        return HttpResponseBadRequest("Invalid field name derived from trigger.")

    template_fragment_name = field_name

    return TemplateResponse(
        request,
        f"includes/guestbook_form.html#{template_fragment_name}",
        {"form": form},
    )
