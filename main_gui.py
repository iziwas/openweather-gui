from tkinter import Tk, LabelFrame, Entry, Button, Label, messagebox, Frame
from src.classes.openweather import OpenWeather
from http import HTTPStatus


class MainGui(Tk):
  def __init__(self):
    super().__init__()
    self.title("Météo OpenWeather")
    self.geometry("400x300")

    # Séparer création et placement
    frame = LabelFrame(self, text="City", padx=10, pady=10)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    self.city_input = Entry(frame, width=30)
    self.city_input.pack(pady=5)

    self.button_city = Button(frame, text="Météo", command=self.submit_city)
    self.button_city.pack(pady=5)

    # Frame pour contenir l'icône et le résultat côte à côté
    self.result_frame = Frame(frame)
    self.result_frame.pack(pady=10)

    self.icon_label = Label(self.result_frame, justify="left")
    self.icon_label.grid(row=0, column=0, padx=10, sticky="n")

    # Zone d'affichage des résultats
    self.result_label = Label(self.result_frame, text="", justify="left", font=("Arial", 12))
    self.result_label.grid(row=0, column=1, sticky="w")

  def submit_city(self):
    city = self.city_input.get().strip()
    if not city:
      messagebox.showwarning("Attention", "Veuillez entrer une ville")
      return

    ow = OpenWeather()
    res = ow.get_weather(city)

    if res["response"] != HTTPStatus.OK:
      messagebox.showerror("Erreur", res["message"])
      return

    self.result_label.config(text=res["message"])

    # Afficher l'icône
    # Garder une référence dans l'attribut `image` pour éviter le garbage collection
    self.icon_label.config(image=res["icon"])
    self.icon_label.image = res["icon"]


