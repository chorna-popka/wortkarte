import six
import os
from google.cloud import translate_v2 as translate

basedir = os.path.abspath(os.path.dirname(__file__))
json_file = os.path.join(basedir, 'static/files/Word-cards-c28ca42966b3.json')


def translate_text(target, text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """

    translate_client = translate.Client.from_service_account_json(json_file)

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)

    return result["translatedText"]