from datetime import datetime
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}\n"
        with open("requests.log", "a") as log_file:
            log_file.write(log_entry)
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()
        # Restrict access if current time is after 9PM (21:00) or before 6PM (18:00)
        if now.hour >= 21 or now.hour < 18:
            return HttpResponseForbidden("Access to the messaging app is restricted between 9PM and 6PM.")
        return self.get_response(request)

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Dictionary to track {ip: [timestamps]}
        self.ip_message_times = {}

    def __call__(self, request):
        # Only apply to message POST requests
        if request.path.startswith('/api/messages') and request.method == 'POST':
            ip = self.get_client_ip(request)
            now = datetime.now()
            window = timedelta(minutes=1)
            times = self.ip_message_times.get(ip, [])

            # Remove timestamps older than 1 minute
            times = [t for t in times if now - t < window]
            if len(times) >= 5:
                return JsonResponse(
                    {"error": "Message rate limit exceeded. Max 5 messages per minute."},
                    status=429
                )
            times.append(now)
            self.ip_message_times[ip] = times

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip