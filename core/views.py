from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import User

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    identifier = request.data.get('identifier')
    password = request.data.get('password')
    
    try:
        # Chercher par email ou matricule
        if '@' in identifier:
            user = User.objects.get(email=identifier)
        else:
            user = User.objects.get(matricule=identifier)
            
        if user.check_password(password):
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'matricule': user.matricule,
                    'nom': user.nom,
                    'prenom': user.prenom
                }
            })
    except User.DoesNotExist:
        pass
    
    return Response(
        {'error': 'Identifiants invalides'}, 
        status=status.HTTP_401_UNAUTHORIZED
    )