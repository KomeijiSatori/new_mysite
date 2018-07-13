from django.http import JsonResponse

from common.base_view import BaseView

# Create your views here.
class TestView(BaseView):
    def get(self, request, *args, **kwargs):
        name = self.current_user.username
        return JsonResponse({"user_name": name})
