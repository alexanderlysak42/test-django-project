from django.utils.http import url_has_allowed_host_and_scheme


def get_safe_next_url(request):
    next_url = request.POST.get(
        'next',
        request.GET.get(
            'next',
            '',
        ),
    )

    if not url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={
            request.get_host(),
        },
        require_https=request.is_secure(),
    ):
        return ''

    return next_url

