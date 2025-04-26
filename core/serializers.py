from rest_framework import serializers
from .models import User, Direction, Service, Poste, FolderType, PieceType, Folder, Piece, Keyword
      
class UserSerializer(serializers.ModelSerializer):
    def validate_poste(self, value):
        if value:
            existing_user = User.objects.filter(poste=value).exclude(pk=getattr(self.instance, 'pk', None)).first()
            if existing_user:
                raise serializers.ValidationError(
                    f"Ce poste est déjà occupé par {existing_user.prenom} {existing_user.nom}"
                )
        return value

    class Meta:
        model = User
        fields = ['id', 'email', 'matricule', 'prenom', 'nom', 'poste', 
                 'statut', 'est_admin', 'date_inscription', 'derniere_connexion']
class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service 
        fields = '__all__'

class PosteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poste
        fields = '__all__'

class FolderTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FolderType
        fields = '__all__'

class PieceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PieceType
        fields = '__all__'

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = '__all__'

class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'
        
class PieceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Piece
        fields = '__all__'