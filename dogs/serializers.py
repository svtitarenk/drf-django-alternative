from rest_framework.fields import SerializerMethodField
from rest_framework import serializers

from dogs.models import Dog, Breed
from dogs.validators import validate_forbidden_words


class BreedSerializer(serializers.ModelSerializer):
    dogs = serializers.SerializerMethodField()

    def get_dogs(self, breed):
        # получаем все собаки этой породы
        # return Dog.objects.filter(breed=breed)  # obj или breed это экземпляр порода, по которому ищем собаки

        # можно также сделать return имен собак.
        # делаем список и из перебора выбираем только имя.
        return [dog.name for dog in Dog.objects.filter(breed=breed)]

    class Meta:
        model = Breed
        # определяет какие поля нам будут возвращаться в ответе 200 (ОК)
        fields = '__all__'


class DogSerializer(serializers.ModelSerializer):
    breed = BreedSerializer(read_only=True)
    # прописываем валидатор черезе serializers. + validators + в списке передаем валидаторы
    name = serializers.CharField(validators=[validate_forbidden_words])

    class Meta:
        model = Dog
        # поля, которые будут задействованы из модели.
        # можем указать кортеж полей, либо указать all для вывода всех полей.
        # определяет какие поля нам будут возвращаться в ответе 200 (ОК)
        fields = '__all__'


class DogDetailSerializer(serializers.ModelSerializer):
    # нужно добавить поле, которое будет выводить собак такой же породы
    # если нам нужно добавить кастомное поле, нужно его прописать
    # но у нас не описан метод, как получать это поле, описываем ниже (def get_count_dog_with_same_breed)
    count_dog_with_same_breed = serializers.SerializerMethodField()

    # теперь поле breed будет определяться сериализатором BreedSerializer
    breed = BreedSerializer(read_only=True)  # включаем сериализатор порода в ответе.

    # метод прописываем как get и название поля выше.
    # передаем в него obj, instance Или dog как в тек.примере (неважно), т.к. класс по собаке
    def get_count_dog_with_same_breed(self, dog):
        # берем породу и фильтруем всех собак по этой породе.
        return Dog.objects.filter(breed=dog.breed).count()

    class Meta:
        model = Dog
        fields = ('name', 'breed', 'date_born', 'count_dog_with_same_breed',)
