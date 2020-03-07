import random
import string

from django.utils.text import slugify

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

# from xhtml2pdf import pisa

'''
random_string_generator is located here:
http://joincfe.com/blog/random-string-generator-in-python/
'''


def random_string_generator(size=8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_order_id_generator(instance):
    """
        This is for a Django project with order_id field.
    """
    order_new_id = random_string_generator().upper()
    # order_new_id = random. for _ in range(10)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_id=order_new_id).exists()
    if qs_exists:
        return unique_order_id_generator(instance)
    return order_new_id


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """

    if new_slug is not None:
        slug = new_slug
    else:
        try:
            slug = slugify(instance.title(), allow_unicode=True)
        except:
            slug = slugify(instance.title, allow_unicode=True)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        if not slug:
            new_slug = "fastpick-{randstr}".format(
                randstr=random_string_generator(size=4))
        else:
            new_slug = "{slug}-{randstr}".format(
                slug=slug,
                randstr=random_string_generator(size=4))
        return unique_slug_generator(instance, new_slug=new_slug)

    return slug

    # PDF Marker

#
# def render_to_pdf(template_src, context_dict={}):
#     template = get_template(template_src)
#     html = template.render(context_dict)
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result, encoding='utf-8')
#
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return None


# pisaStatus = pisa.CreatePDF(
#     StringIO(sourceHtml.encode('utf-8')),
#     dest=resultFile,
#     encoding='utf-8')
