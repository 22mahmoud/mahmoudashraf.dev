from bs4 import BeautifulSoup, Tag
from django_tasks import task

from src.guestbook.utils import highlight_code, optimize_img_tag


@task()
def optimize_guestbook_html(guestbook_id: int):
    from src.guestbook.models import Guestbook

    try:
        guestbook = Guestbook.objects.get(id=guestbook_id)
    except Guestbook.DoesNotExist:
        return

    if not guestbook.message_html:
        return

    soup = BeautifulSoup(guestbook.message_html, "html.parser")

    for pre in soup.find_all("pre"):
        if isinstance(pre, Tag):
            highlight_code(pre)

    for img in soup.find_all("img"):
        if isinstance(img, Tag):
            optimize_img_tag(img)

    guestbook.message_html = str(soup)
    guestbook.save(update_fields=["message_html"])
