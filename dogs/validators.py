from rest_framework.serializers import ValidationError

forbidden_words = ['ставки', "крипта", "продам", "гараж"]


def validate_forbidden_words(value):
    if value.lower() in forbidden_words:
        raise ValidationError(f"Слово '{value}' запрещено в использовании.")
