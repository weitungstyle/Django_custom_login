from django.http import JsonResponse
from django.contrib.auth import authenticate, login, get_user_model
from django.core.exceptions import ValidationError
from .models import CustomUser
import json

# disable CSRF function
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        json_data = json.loads(data)
        username = json_data.get('username')
        password = json_data.get('password')
        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'reason': "Username already exists."}, status=400)
        try:
            CustomUser.objects.validate_password(password)
            user = CustomUser.objects.create_user(
                username=username, password=password)
            user.save()
            return JsonResponse({'success': True}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'reason': str(e)}, status=400)
    return JsonResponse({'success': False, 'reason': 'Invalid request method.'}, status=405)


@csrf_exempt
def signin(request):
    if request.method == 'POST':
        try:
            data = request.body.decode('utf-8')
            json_data = json.loads(data)
            username = json_data.get('username')
            password = json_data.get('password')
            if not username or not password:
                return JsonResponse({'success': False, 'reason': 'Username and password are required.'}, status=400)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True}, status=200)
            else:
                return JsonResponse({'success': False, 'reason': 'Invalid username or password.'}, status=401)
        except ValidationError as e:
            return JsonResponse({'success': False, 'reason': str(e)}, status=423)
        except Exception as e:
            return JsonResponse({'success': False, 'reason': str(e)}, status=400)
    return JsonResponse({'success': False, 'reason': 'Invalid request method.'}, status=405)
