def get_session_key(request):
    """Возвращает ID сессии. Создает сессию, если она не была создана."""
    session_key = request.session.session_key
    if not request.session.exists(session_key):
        request.session.create()
        session_key = request.session.session_key
    return session_key
