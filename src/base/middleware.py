from django.conf import settings
from django.middleware.csp import ContentSecurityPolicyMiddleware


class WagtailAwareContentSecurityPolicyMiddleware(ContentSecurityPolicyMiddleware):
    """Skip CSP headers for public Wagtail page routes."""

    def process_response(self, request, response):
        resolver_match = getattr(request, "resolver_match", None)

        if resolver_match is not None and resolver_match.route.startswith(
            settings.WAGTAIL_ADMIN_PATH
        ):
            return response

        return super().process_response(request, response)
