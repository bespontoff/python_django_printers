from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render
from django_auth_ldap.backend import LDAPBackend  # , populate_user

from .forms import AuthForm


def login_view(request):
    if request.method == 'POST':  # для POST пытаемся аутентифицировать пользователя
        auth_form = AuthForm(request.POST)
        if auth_form.is_valid():
            username = auth_form.cleaned_data['username']
            password = auth_form.cleaned_data['password']

            auth = LDAPBackend()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.groups.filter(name__in=['WG_Access_PrintersFunc']).exists():
                    if user.is_active:
                        login(request, user)
                        return HttpResponse('Успешная авторизация')
                    else:
                        return HttpResponse('Успешная авторизация, но пользователь отключен')
                else:
                    return HttpResponse('Успешная авторизация, но нет группы')
            else:
                auth_form.add_error('__all__', 'Ошибка! Проверьте правильность логина и пароля.')

            # if user:
            #     if user.is_active:
            #         login(request, user)
            #         return HttpResponse('Успешная авторизация')
            #     else:
            #         auth_form.add_error('__all__', 'Ошибка! Учетная запись пользователя не активна.')
            # else:
            #     auth_form.add_error('__all__', 'Ошибка! Проверьте правильность логина и пароля.')

    else:  # для всех остальных запросов просто отображаем форму, в .т.ч. с ошибками
        auth_form = AuthForm()

    context = {
        'form': auth_form
    }
    return render(request, 'app_auth_users/login.html', context=context)


class AnotherLoginView(LoginView):
    template_name = 'app_auth_users/login.html'

# # LDAP authentication backend

# from django_auth_ldap.backend import LDAPBackend
# from django.contrib.auth import get_user_model

# class MyLDAPBackend(LDAPBackend):
#     """ A custom LDAP authentication backend """

#     def authenticate(self, username, password):
#         """ Overrides LDAPBackend.authenticate to save user password in django """

#         user = LDAPBackend.authenticate(self, username, password)

#         # If user has successfully logged, save his password in django database
#         if user:
#             user.set_password(password)
#             user.save()

#         return user

#     def get_or_create_user(self, username, ldap_user):
#         """ Overrides LDAPBackend.get_or_create_user to force from_ldap to True """
#         kwargs = {
#             'username': username,
#             'defaults': {'from_ldap': True}
#         }
#         user_model = get_user_model()
#         return user_model.objects.get_or_create(**kwargs)


# # Classical authentication backend

# from django.contrib.auth import get_backends, get_user_model
# from django.contrib.auth.backends import ModelBackend

# class MyAuthBackend(ModelBackend):
#     """ A custom authentication backend overriding django ModelBackend """

#     @staticmethod
#     def _is_ldap_backend_activated():
#         """ Returns True if MyLDAPBackend is activated """
#         return MyLDAPBackend in [b.__class__ for b in get_backends()]

#     def authenticate(self, username, password):
#         """ Overrides ModelBackend to refuse LDAP users if MyLDAPBackend is activated """

#         if self._is_ldap_backend_activated():
#             user_model = get_user_model()
#             try:
#                 user_model.objects.get(username=username, from_ldap=False)
#             except:
#                 return None

#         user = ModelBackend.authenticate(self, username, password)

#         return user
