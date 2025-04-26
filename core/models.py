import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# ENUMS
class StatutChoices(models.TextChoices):
    ACTIF = 'actif', 'Actif'
    ATTENTE = 'attente', 'En attente'
    DESACTIVE = 'desactive', 'Désactivé'

class ImportanceChoices(models.TextChoices):
    FAIBLE = 'faible', 'Faible'
    MOYENNE = 'moyenne', 'Moyenne'
    ELEVEE = 'elevee', 'Élevée'
    CRITIQUE = 'critique', 'Critique'

class ActionTypeChoices(models.TextChoices):
    CREATION = 'creation', 'Création'
    MODIFICATION = 'modification', 'Modification'
    SUPPRESSION = 'suppression', 'Suppression'
    CONSULTATION = 'consultation', 'Consultation'

class ItemTypeChoices(models.TextChoices):
    DOSSIER = 'dossier', 'Dossier'
    PIECE = 'piece', 'Pièce'

# USER MANAGER
class UserManager(BaseUserManager):
    def create_user(self, email, matricule, password=None, **extra_fields):
        if not email:
            raise ValueError('L’email est requis')
        email = self.normalize_email(email)
        user = self.model(email=email, matricule=matricule, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, matricule, password=None, **extra_fields):
        extra_fields.setdefault('est_admin', True)
        return self.create_user(email, matricule, password, **extra_fields)

# VALIDATION HISTORY
class ValidationHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    demande = models.ForeignKey('User', on_delete=models.CASCADE, related_name='demandes')
    valide_par = models.ForeignKey('User', on_delete=models.CASCADE, related_name='validations')
    statut = models.CharField(max_length=20, choices=StatutChoices.choices)
    commentaire = models.TextField(blank=True)
    date_demande = models.DateTimeField()
    date_validation = models.DateTimeField(null=True, blank=True)

# USER
class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    matricule = models.CharField(max_length=50, unique=True)
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    poste = models.ForeignKey('Poste', on_delete=models.SET_NULL, null=True)
    statut = models.CharField(max_length=20, choices=StatutChoices.choices)
    validation = models.ForeignKey(ValidationHistory, on_delete=models.SET_NULL, null=True)
    is_staff = models.BooleanField(default=False)
    date_inscription = models.DateTimeField(auto_now_add=True)
    derniere_connexion = models.DateTimeField(null=True, blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['matricule']

# DIRECTION, SERVICE, POSTE
class Direction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)

class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE)

class Poste(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    est_occupe = models.BooleanField(default=False)
    est_chef = models.BooleanField(default=False)

# FOLDER TYPE ET PIECE TYPE
class FolderType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    createur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_creation = models.DateTimeField()
    cree_a = models.CharField(max_length=255)

class PieceType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    type_dossier = models.ForeignKey(FolderType, on_delete=models.SET_NULL, null=True, blank=True)
    createur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    cree_a = models.CharField(max_length=255)

# KEYWORD
class Keyword(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)

# FOLDER
class Folder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    createur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    direction = models.ForeignKey(Direction, on_delete=models.SET_NULL, null=True)
    dossier_parent = models.ForeignKey(FolderType, on_delete=models.PROTECT)
    provenance = models.CharField(max_length=255)
    importance = models.CharField(max_length=20, choices=ImportanceChoices.choices)
    dossier_date = models.DateField()
    creation_date = models.DateTimeField(auto_now_add=True)
    derniere_modification = models.DateTimeField(auto_now=True)
    est_public = models.BooleanField(default=False)
    keyword = models.ManyToManyField(Keyword, through='FolderKeyword')
    est_supprime = models.BooleanField(default=False)

# PIECE
class Piece(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    fichier = models.FileField(upload_to='pieces/')
    fichier_taille = models.BigIntegerField()
    piece_date = models.DateField()
    date_televersement = models.DateTimeField(auto_now_add=True)
    createur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    entite = models.CharField(max_length=100)
    numero = models.CharField(max_length=50)
    type = models.ForeignKey(PieceType, on_delete=models.CASCADE)
    duree_vie = models.IntegerField()
    est_public = models.BooleanField(default=False)
    keyword = models.ManyToManyField(Keyword, through='PieceKeyword')
    est_supprime = models.BooleanField(default=False)

# HISTORIQUE
class PieceHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=50, choices=ActionTypeChoices.choices)
    action_date = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)

class FolderHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dossier = models.ForeignKey(Folder, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=50, choices=ActionTypeChoices.choices)
    action_date = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)

# PERMISSIONS
class FolderPermission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dossier = models.ForeignKey(Folder, on_delete=models.CASCADE)
    beneficiaire = models.ForeignKey(User, on_delete=models.CASCADE, related_name='permissions_dossier')
    direction_beneficiaire = models.ForeignKey(Direction, on_delete=models.SET_NULL, null=True, blank=True)
    structure_beneficiaire = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    peut_lire = models.BooleanField(default=False)
    peut_editer = models.BooleanField(default=False)
    peut_supprime = models.BooleanField(default=False)
    donneur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='dossier_donnes')
    attribution_date = models.DateTimeField(auto_now_add=True)

class PiecePermission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE)
    beneficiaire = models.ForeignKey(User, on_delete=models.CASCADE, related_name='permissions_piece')
    direction_beneficiaire = models.ForeignKey(Direction, on_delete=models.SET_NULL, null=True, blank=True)
    structure_beneficiaire = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    peut_lire = models.BooleanField(default=False)
    peut_editer = models.BooleanField(default=False)
    peut_supprime = models.BooleanField(default=False)
    donneur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='piece_donnes')
    attribution_date = models.DateTimeField(auto_now_add=True)

# CORBEILLE
class TrashItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item_type = models.CharField(max_length=50, choices=ItemTypeChoices.choices)
    piece = models.ForeignKey(Piece, on_delete=models.SET_NULL, null=True, blank=True)
    dossier = models.ForeignKey(Folder, on_delete=models.SET_NULL, null=True, blank=True)
    supprime_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='items_supprimes')
    date_suppression = models.DateTimeField(auto_now_add=True)
    justification = models.TextField(blank=True)
    est_restauré = models.BooleanField(default=False)
    date_restoration = models.DateTimeField(null=True, blank=True)
    restauré_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='items_restaures')

# KEYWORDS RELATIONS
class FolderKeyword(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)

class PieceKeyword(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
