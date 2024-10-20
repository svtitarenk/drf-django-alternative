from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from users.models import User, Donation
from users.serializers import UserSerializer, DonationSerializer
from users.services import convert_rub_to_usd, create_stripe_price, create_stripe_session


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


class DonationCreateAPIView(CreateAPIView):
    serializer_class = DonationSerializer
    queryset = Donation.objects.all()
    # permission_classes убрали, т.к. по дефолту доступен только авторизованным пользователям

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        # у нас создался платеж, у которого есть сумма. Нужно сумму конвертировать и сгенерировать ссылку на оплату
        amount_in_usd = convert_rub_to_usd(payment.amount)
        # создаем стоимость.
        price = create_stripe_price(amount_in_usd)
        # нужно получить id сессии, а также ссылку на оплату
        session_id, payment_link = create_stripe_session(price)
        # нам нужно в наш объект платежа, в поле session_id записать sission_id, а в pyment_link = link
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()
