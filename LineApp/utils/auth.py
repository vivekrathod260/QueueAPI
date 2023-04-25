import jwt

def auth(request):
    header = request.META.get('HTTP_AUTHORIZATION', '')
    if header.startswith('JWT '):
        token = header[4:]
    else:
        return -1

    try:
        decoded = jwt.decode(token, 'vivekkey', algorithms=['HS256'])
        print(decoded)
        return decoded.get("userName")
    except jwt.exceptions.DecodeError:
        return 0