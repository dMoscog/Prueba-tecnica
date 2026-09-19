import requests
from django.core.management.base import BaseCommand
from catalog.models import Ubication, Episode, Character


class Command(BaseCommand):
    help = "Sincroniza ubicaciones, episodios y personajes desde la API de Rick and Morty"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Iniciando sincronización con la API..."))

        # 1. Sincronizar Ubicaciones
        self.sync_ubications()

        # 2. Sincronizar Episodios
        self.sync_episodes()

        # 3. Sincronizar Personajes y sus relaciones
        self.sync_characters()

        self.stdout.write(self.style.SUCCESS("Sincronización completada exitosamente."))

    def sync_ubications(self):
        url = "https://rickandmortyapi.com/api/location"
        while url:
            response = requests.get(url)
            data = response.json()
            
            for item in data['results']:
                Ubication.objects.update_or_create(
                    external_id=item['id'],
                    defaults={
                        'name': item['name'],
                        'type': item['type'],
                        'dimension': item['dimension'],
                    }
                )
            url = data['info']['next']
        self.stdout.write("Ubicaciones sincronizadas.")

    def sync_episodes(self):
        url = "https://rickandmortyapi.com/api/episode"
        while url:
            response = requests.get(url)
            data = response.json()
            
            for item in data['results']:
                Episode.objects.update_or_create(
                    external_id=item['id'],
                    defaults={
                        'name': item['name'],
                        'air_date': item['air_date'],
                        'episode_code': item['episode'],
                    }
                )
            url = data['info']['next']
        self.stdout.write("Episodios sincronizados.")

    def sync_characters(self):
        url = "https://rickandmortyapi.com/api/character"
        while url:
            response = requests.get(url)
            data = response.json()
            
            for item in data['results']:
                # Buscar ubicación relacionada si existe
                location_obj = None
                location_data = item.get('location')
                if location_data and location_data.get('url'):
                    loc_id = int(location_data['url'].split('/')[-1])
                    location_obj = Ubication.objects.filter(external_id=loc_id).first()

                # Crear o actualizar el personaje
                character, created = Character.objects.update_or_create(
                    external_id=item['id'],
                    defaults={
                        'name': item['name'],
                        'status': item['status'],
                        'species': item['species'],
                        'gender': item['gender'],
                        'image_url': item['image'],
                        'location': location_obj,
                    }
                )

                # Asociar los episodios en la relación ManyToMany
                episode_ids = [int(ep_url.split('/')[-1]) for ep_url in item['episode']]
                episodes_objs = Episode.objects.filter(external_id__in=episode_ids)
                character.episodes.set(episodes_objs)

            url = data['info']['next']
        self.stdout.write("Personajes sincronizados.")