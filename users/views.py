from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from users.models import User
from users.serializers import UserSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        # делаем пользователя автоматически активным, присваиваем is_active=True
        user = serializer.save(is_active=True)
        """
        у нас в модели, хоть это нигде и не описано есть пароль. Обязательное поле. Будет запрашиваться. 
        Когда пользователь будет создавать себе аккаунт, у него будет пароль. 
        
        поэтому мы берем пароль пользователя в незахешированном виде, поэтому когда пароль в таком виде это не хорошо. 
        Нам надо его захешировать. У нас есть для этого функция set_password и сюда мы передаем user.password
        после этого сохраняем юзера.
        """
        user.set_password(user.password)
        user.save()
