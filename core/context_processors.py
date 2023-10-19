from core.models import Notification,History


def default(request):
    try:
        notifications = Notification.objects.filter(user=request.user).order_by("-id")[:10]
        history = History.objects.filter(user=request.user).order_by("-id")[:10]

    except:
        notifications = None
        history = None

    return {
        "notifications":notifications,
        "history":history

    }