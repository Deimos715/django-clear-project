from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    # Профиль
    path('profile/', views.profile, name='profile'),

    # Вход
    path('login/', views.user_login, name='login'), # Доступен всем
    
    # Выход
    path('logout/', views.user_logout, name='logout'), # Доступен всем
    
    # Регистрация
    path('registry/', views.registry, name='registry'), # Доступен всем
    # Активация
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    # Уведомление об отправке письма с активацией
    path('activation-sent/', views.activation_sent, name='activation_sent'), # Доступен всем
    # Изменить email в рамках сессии регистрации
    path('activation-email-change/', views.activation_email_change, name='activation_email_change'),
    # Успешная активация
    path('activation-end/', views.activation_end, name='activation_end'), # Доступен всем
    # Невалидная/просроченная активация
    path('activation-invalid/', views.activation_invalid, name='activation_invalid'), # Доступен всем
    # Повторная отправка письма активации
    path('activation-resend/', views.activation_resend, name='activation_resend'),
    
    # Изменение пароля
    path('password-change/', views.password_change, name='password_change'), # Доступен только авторизованным, неавторизованных перенаправляет на страницу входа
    # Успешное изменение пароля
    path('password-change/done/', views.password_change_done, name='password_change_done'), # Доступен только авторизованным, неавторизованных перенаправляет на страницу входа
    
    # Сброс пароля
    path('password-reset/', views.password_reset, name='password_reset'), # Доступен всем, сделан редирект для авторизованных
    # Успешный сброс пароля
    path('password-reset/done/', views.password_reset_end, name='password_reset_end'), # Доступен всем
    # Подтверждение сброса пароля
    path('password-reset/<slug:uidb64>/<slug:token>/', views.password_reset_confirm, name='password_reset_confirm'),
    # Завершение сброса пароля
    path('password-reset/complete/', views.password_reset_complete, name='password_reset_complete'), # Доступен всем

]
