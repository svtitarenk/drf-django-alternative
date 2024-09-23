from rest_framework.serializers import ModelSerializer

from dogs.models import Dog, Breed


class DogSerializer(ModelSerializer):
    class Meta:
        model = Dog
        # поля, которые будут задействованы из модели.
        # можем указать кортеж полей, либо указать all для вывода всех полей.
        # определяет какие поля нам будут возвращаться в ответе 200 (ОК)
        fields = '__all__'


class BreedSerializer(ModelSerializer):
    class Meta:
        model = Breed
        # определяет какие поля нам будут возвращаться в ответе 200 (ОК)
        fields = '__all__'
