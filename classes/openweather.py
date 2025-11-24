import os
import requests
from dotenv import load_dotenv, find_dotenv
from io import BytesIO
from PIL import Image, ImageTk

load_dotenv(find_dotenv())

API_KEY = os.environ.get('OPENWEATHER_API_KEY')

class OpenWeather:
    def get_weather(self, city: str) -> dict[str, int | str | ImageTk.PhotoImage | None]:
        """ Récupère la météo pour une ville. """
        res = dict()
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=fr"
            response = requests.get(url)
            data = response.json()

            res: dict[str, int | str | ImageTk.PhotoImage | None] = {
                "response": response.status_code,
                "icon": None
            }

            if res["response"] == 200:
                temp = data['main']['temp']
                description = data['weather'][0]['description']
                humidity = data['main']['humidity']
                icon_code = data['weather'][0]['icon']
                message = f"Ville: {city}\nTempérature: {temp}°C\nMétéo: {description}\nHumidité: {humidity}%"

                res.update({
                    "icon": self._display_weather_icon(icon_code),
                    "message": message
                })
            else:
                res["message"] = f"Erreur: {data.get('message', 'Erreur inconnue')}"
        except Exception as e:
            res["message"] = f"Erreur de connexion: {str(e)}"

        return res

    def _display_weather_icon(self, icon_code: str) -> ImageTk.PhotoImage | None:
        """Télécharge et retourne l'icône météo"""
        photo = None
        try:
            # URL de l'icône OpenWeather (taille 2x pour meilleure qualité)
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

            icon_response = requests.get(icon_url)
            icon_data = Image.open(BytesIO(icon_response.content))
            photo = ImageTk.PhotoImage(icon_data)
        except Exception as e:
            print(f"Erreur lors du chargement de l'icône: {e}")

        return photo