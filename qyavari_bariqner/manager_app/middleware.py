from datetime import datetime
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model

User = get_user_model()

class UpdateLastActivityMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            profile = request.user.userprofile  # Получаем профиль пользователя
            profile.last_activity = datetime.now()
            profile.save()
            print(f"Updated last_activity for {profile.user.username} to {profile.last_activity}")