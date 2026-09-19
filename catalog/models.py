from django.db import models

class Ubication(models.Model):
    """
    Modelo que representa una ubicación del universo de Rick and Morty.
    """
    external_id = models.IntegerField(unique=True, help_text="ID original de la ubicación en la API externa")
    name = models.CharField(max_length=255, help_text="Nombre de la ubicación")
    type = models.CharField(max_length=255, help_text="Tipo o categoría de la ubicación")
    dimension = models.CharField(max_length=255, help_text="Dimensión a la que pertenece la ubicación")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Fecha de registro en la base de datos local")

    def __str__(self):
        return f"{self.name} ({self.dimension})"


class Episode(models.Model):
    """
    Modelo que representa un episodio de la serie.
    """
    external_id = models.IntegerField(unique=True, help_text="ID original del episodio en la API externa")
    name = models.CharField(max_length=255, help_text="Título del episodio")
    air_date = models.CharField(max_length=255, help_text="Fecha de emisión original")
    episode_code = models.CharField(max_length=50, help_text="Código de temporada y episodio (ej. S01E01)")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Fecha de registro en la base de datos local")

    def __str__(self):
        return f"{self.episode_code} - {self.name}"


class Character(models.Model):
    """
    Modelo principal que representa a un personaje con relaciones a Ubicación y Episodios.
    """
    external_id = models.IntegerField(unique=True, null=True, blank=True, help_text="ID original en la API")
    name = models.CharField(max_length=255, help_text="Nombre del personaje")
    status = models.CharField(max_length=50, help_text="Estado vital del personaje")
    species = models.CharField(max_length=100, help_text="Especie a la que pertenece")
    gender = models.CharField(max_length=50, help_text="Género del personaje")
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text="Enlace a la imagen oficial")
    
    location = models.ForeignKey(
        Ubication, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='residents',
        help_text="Ubicación asociada al personaje"
    )
    
    episodes = models.ManyToManyField(
        Episode, 
        related_name='characters',
        help_text="Episodios en los que ha participado el personaje"
    )
    
    updated_at = models.DateTimeField(auto_now=True, help_text="Última actualización del registro")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Fecha de creación del registro local")

    def __str__(self):
        return self.name