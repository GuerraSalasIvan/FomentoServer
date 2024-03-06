from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator,MinLengthValidator
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserLogin(AbstractUser):
    administrador=1
    cliente=2
    entrenador=3
    
    ROLES= ((administrador,'administrador'),
            (cliente,'cliente'),
            (entrenador,'entrenador'),
            )
    
    rol = models.PositiveSmallIntegerField(choices=ROLES, default=1)
    
    #Agregar estos atributos para evitar el conflicto
    #groups = models.ManyToManyField('auth.Group', related_name='custom_user_groups')
    #user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_permissions')
    
    
    
    
class Usuarios(models.Model):
    
    edad = models.IntegerField()
    media = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(99)])
    GENERO = [
        ('MAS','Masculino'),
        ('FEM','Femenino'),
        ('---','Sin_Asignar'),
    ]
    #Si no se especifica el género, no se puede participar en deportes.
    sexo = models.CharField(
        max_length = 3,
        choices= GENERO,
        default = '---'
    )
    
    rol=models.OneToOneField(UserLogin, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.rol.first_name
    
    
    
class Deportes(models.Model):
    DEPORTES = [
        ('FUT','Futbol'),
        ('BSK','Baloncesto'),
        ('PDL','Padel'),
        ('---','Sin_Asignar'),
    ]
    
    deporte = models.CharField(
        max_length = 3,
        choices= DEPORTES,
        default = '---'
    )
    
    def __str__(self):
        if self.deporte == 'BSK':
            resultado='Baloncesto'
        elif self.deporte == 'FUT':
            resultado='Futbol'
        elif self.deporte == 'PDL':
            resultado='Padel'
        else:
            resultado='Sin especificar'
        
        return resultado
    
    
class Liga(models.Model):
    LIGA = [
        ('2ªReg','Segunda Regional'),
        ('1ºReg','Primera Regional'),
        ('DivHonor','Division de honor'),
        ('Nacional','Nacional'),
        ('---','Sin asignar'),
        
    ]
    
    liga = models.CharField(
        max_length = 8,
        choices= LIGA,
        default = '---',
    )
    
    def __str__(self):
        return self.liga
    
class Colores(models.Model):
    COLORES = [
        ('Blanco','Blanco'),
        ('Negro','Negro'),
        ('Amarillo','Amarillo'),
        ('Rojo','Rojo'),
        ('Azul','Azul'),
        ('Rosa','Rosa'),
        ('Morado','Morado'),
        ('Verde','Verde'),
        ('Gris','Gris'),
        ('Marron','Marron'),
        ('Gris','Gris'),
        ('Naranja','Naranja'),
        ('---','Sin asignar'),
        
    ]
    
    color = models.CharField(
        max_length = 10,
        choices= COLORES,
        default = '---',
    )
    
    def __str__(self):
        return self.color
    
    
class Equipos(models.Model):
    nombre = models.CharField(max_length=60)
    capacidad = models.IntegerField(default=1)
    color_eq_1 = models.ForeignKey(Colores, related_name=("color_eq_1"), on_delete=models.CASCADE)
    color_eq_2 = models.ForeignKey(Colores, related_name=("color_eq_2"), on_delete=models.CASCADE)
    media_equipo = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(99)])
    
    deporte = models.ForeignKey(Deportes, verbose_name=("deporte"), on_delete=models.CASCADE)
    usuario_valoracion = models.ManyToManyField(Usuarios, through="Votacion", related_name="votacion_usuario")   
    usuario = models.ManyToManyField(Usuarios, through="Rel_Usu_Equi", related_name="usuario_equipo") 
    liga = models.ForeignKey(Liga, verbose_name=("Liga"), on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre + ' ('+ str(self.deporte.deporte)+')'
    
    
    
    
class Entrenador(models.Model):

    rol = models.OneToOneField(UserLogin, on_delete=models.CASCADE)
    
    equipo = models.ManyToManyField(Equipos, verbose_name=("equipo"))
    
    

class Ubicacion(models.Model):
    nombre = models.CharField(max_length=150)
    capacidad = models.IntegerField()
    calle = models.CharField(max_length=150)
    
    lat = models.FloatField(verbose_name=("latitud"))
    lng = models.FloatField(verbose_name=("longitud")) 
    
    equipo = models.ManyToManyField(Equipos, verbose_name=("equipo"))
    deporte = models.ManyToManyField(Deportes, verbose_name=("deporte"))
    
    def __str__(self):
        return self.nombre+'  ('+self.calle+')'
    

class Detalles_Ubicacion(models.Model):
    ubicacion  = models.OneToOneField(Ubicacion, verbose_name=("ubicacion"), on_delete=models.CASCADE)
    incidentes = models.BooleanField()
    cubierto = models.BooleanField()
    
    
    
class Perfil_Publico(models.Model):
    descripcion = models.TextField()
    lugar_fav = models.ForeignKey(Ubicacion, verbose_name=("lugar_fav"), on_delete=models.CASCADE)
    deportes_fav = models.TextField()
    hitos_publicos = models.TextField()
    #me faltaba la relacion con usuarios
    usuarios = models.OneToOneField(Usuarios, on_delete=models.CASCADE)
    
    def __str__(self):
        return 'Perfil publico de '+self.usuarios.rol.first_name
    

class Rel_Usu_Equi(models.Model):
    usuario = models.ForeignKey(Usuarios, verbose_name=("usuario"), on_delete=models.CASCADE)
    
    equipos = models.ForeignKey(Equipos, verbose_name=("equipos"), on_delete=models.CASCADE) 
    
    
class Rel_Equi_Ubi(models.Model):
    ubicacion = models.ForeignKey(Ubicacion, verbose_name=("ubicacion"), on_delete=models.CASCADE)
    
    equipos = models.ForeignKey(Equipos, verbose_name=("equipos"), on_delete=models.CASCADE) 


class Rel_Dep_Ubi(models.Model):
    deporte = models.ForeignKey(Deportes, verbose_name=("deporte"), on_delete=models.CASCADE)
    
    equipos = models.ForeignKey(Equipos, verbose_name=("equipos"), on_delete=models.CASCADE) 
    
class Votacion(models.Model):
    puntuacion = models.IntegerField(default=0)
    comentario = models.CharField(max_length=400)
    fecha = models.DateTimeField(default=timezone.now)
    
    usuarios = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    equipos = models.ForeignKey(Equipos, on_delete=models.CASCADE)
    
class Partido(models.Model):
    fecha = models.DateTimeField()
    ubicacion = models.ForeignKey(Ubicacion, verbose_name=("ubicacion"), on_delete=models.CASCADE)
    equipo_local = models.ForeignKey(Equipos, related_name=("equipo_local"), on_delete=models.CASCADE)
    equipo_visitante = models.ForeignKey(Equipos, related_name=("equipo_visitiante"), on_delete=models.CASCADE)
    color_local = models.ForeignKey(Colores, related_name=("color_local"), on_delete=models.CASCADE)
    color_visitante = models.ForeignKey(Colores, related_name=("color_visitante"), on_delete=models.CASCADE)
    puntos_local = models.IntegerField(default=0)
    puntos_visitante = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.equipo_local)+' vs '+str(self.equipo_visitante) + str(self.fecha.strftime("%Y-%m"))
    
    