from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup

root = Tk()
root.geometry("1400x800")
root.title("Mapa Warsztatów")

map_widget = tkintermapview.TkinterMapView(root, width=900, height=700, corner_radius=0)
map_widget.grid(row=0, column=1, rowspan=999)
map_widget.set_position(52.23, 21.0)
map_widget.set_zoom(6)

frame = Frame(root)
frame.grid(row=0, column=0, sticky=N, padx=10, pady=10)

Label(frame, text="Nazwa").grid(row=0, column=0)
entry_name = Entry(frame)
entry_name.grid(row=0, column=1)

Label(frame, text="Miejscowość").grid(row=1, column=0)
entry_location = Entry(frame)
entry_location.grid(row=1, column=1)

Label(frame, text="Warsztat (jeśli dotyczy)").grid(row=2, column=0)
entry_warsztat = Entry(frame)
entry_warsztat.grid(row=2, column=1)

listbox_warsztaty = Listbox(frame, height=8, width=40)
listbox_pracownicy = Listbox(frame, height=8, width=40)
listbox_klienci = Listbox(frame, height=8, width=40)

listbox_warsztaty.grid(row=5, column=0, columnspan=2, pady=5)
listbox_pracownicy.grid(row=7, column=0, columnspan=2, pady=5)
listbox_klienci.grid(row=9, column=0, columnspan=2, pady=5)

Label(frame, text="Warsztaty").grid(row=4, column=0)
Label(frame, text="Pracownicy").grid(row=6, column=0)
Label(frame, text="Klienci").grid(row=8, column=0)

frame_buttons = Frame(frame)
frame_buttons.grid(row=3, column=0, columnspan=2, pady=10)

obiekty = []
tryb_edycji = None
edycja_index = None

class Obiekt:
    def __init__(self, typ, nazwa, miejscowosc, warsztat=None):
        self.typ = typ
        self.nazwa = nazwa
        self.miejscowosc = miejscowosc
        self.warsztat = warsztat
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=nazwa)

    def get_coordinates(self):
        url = f"https://pl.wikipedia.org/wiki/{self.miejscowosc}"
        try:
            response = requests.get(url).text
            soup = BeautifulSoup(response, "html.parser")
            latitude = float(soup.select(".latitude")[1].text.replace(",", "."))
            longitude = float(soup.select(".longitude")[1].text.replace(",", "."))
            return [latitude, longitude]
        except:
            return [52.23, 21.0]

def format_etykiety(obiekt):
    if obiekt.typ == "warsztat":
        return f"[Warsztat] {obiekt.nazwa} ({obiekt.miejscowosc})"
    elif obiekt.typ == "pracownik":
        nr = sum(1 for o in obiekty if o.typ == "pracownik" and o.warsztat == obiekt.warsztat and obiekty.index(o) <= obiekty.index(obiekt))
        return f"[Pracownik {nr}] {obiekt.nazwa} ({obiekt.miejscowosc}) w {obiekt.warsztat}"
    elif obiekt.typ == "klient":
        return f"[Klient] {obiekt.nazwa} ({obiekt.miejscowosc}) w {obiekt.warsztat}"

def odswiez_listy():
    listbox_warsztaty.delete(0, END)
    listbox_pracownicy.delete(0, END)
    listbox_klienci.delete(0, END)
    for obiekt in obiekty:
        if obiekt.typ == "warsztat":
            listbox_warsztaty.insert(END, format_etykiety(obiekt))
        elif obiekt.typ == "pracownik":
            listbox_pracownicy.insert(END, format_etykiety(obiekt))
        elif obiekt.typ == "klient":
            listbox_klienci.insert(END, format_etykiety(obiekt))

def dodaj_obiekt(typ):
    global tryb_edycji, edycja_index
    nazwa = entry_name.get()
    miejscowosc = entry_location.get()
    warsztat = entry_warsztat.get()
    if nazwa and miejscowosc:
        if tryb_edycji:
            stary = obiekty[edycja_index]
            stary.marker.delete()
            obiekty[edycja_index] = Obiekt(typ, nazwa, miejscowosc, warsztat if warsztat else None)
            tryb_edycji = None
            edycja_index = None
            btn_edit.config(text="Aktualizuj zaznaczony")
        else:
            obiekt = Obiekt(typ, nazwa, miejscowosc, warsztat if warsztat else None)
            obiekty.append(obiekt)
        entry_name.delete(0, END)
        entry_location.delete(0, END)
        entry_warsztat.delete(0, END)
        odswiez_listy()
        pokaz_wszystkie()

def usun_obiekt():
    zaznaczony = None
    if listbox_warsztaty.curselection():
        zaznaczony = ("warsztat", listbox_warsztaty.curselection()[0])
    elif listbox_pracownicy.curselection():
        zaznaczony = ("pracownik", listbox_pracownicy.curselection()[0])
    elif listbox_klienci.curselection():
        zaznaczony = ("klient", listbox_klienci.curselection()[0])
    if zaznaczony:
        typ, idx = zaznaczony
        count = -1
        for i, obiekt in enumerate(obiekty):
            if obiekt.typ == typ:
                count += 1
            if count == idx and obiekt.typ == typ:
                obiekt.marker.delete()
                obiekty.pop(i)
                break
        odswiez_listy()
        pokaz_wszystkie()

def edytuj_obiekt():
    global tryb_edycji, edycja_index
    zaznaczony = None
    if listbox_warsztaty.curselection():
        zaznaczony = ("warsztat", listbox_warsztaty.curselection()[0])
    elif listbox_pracownicy.curselection():
        zaznaczony = ("pracownik", listbox_pracownicy.curselection()[0])
    elif listbox_klienci.curselection():
        zaznaczony = ("klient", listbox_klienci.curselection()[0])
    if zaznaczony:
        typ, idx = zaznaczony
        count = -1
        for i, obiekt in enumerate(obiekty):
            if obiekt.typ == typ:
                count += 1
            if count == idx and obiekt.typ == typ:
                entry_name.delete(0, END)
                entry_name.insert(0, obiekt.nazwa)
                entry_location.delete(0, END)
                entry_location.insert(0, obiekt.miejscowosc)
                entry_warsztat.delete(0, END)
                entry_warsztat.insert(0, obiekt.warsztat if obiekt.warsztat else "")
                tryb_edycji = typ
                edycja_index = i
                btn_edit.config(text="Zapisz zmiany")
                break

def pokaz_wszystkie():
    for obiekt in obiekty:
        if obiekt.marker:
            obiekt.marker.delete()
            obiekt.marker = None
    for obiekt in obiekty:
        obiekt.marker = map_widget.set_marker(obiekt.coordinates[0], obiekt.coordinates[1], text=obiekt.nazwa)

def pokaz_wybrany_warsztat():
    zaznaczone = listbox_warsztaty.curselection()
    if not zaznaczone:
        return
    idx = zaznaczone[0]

    count = -1
    wybrany_warsztat = None
    for obiekt in obiekty:
        if obiekt.typ == "warsztat":
            count += 1
        if count == idx:
            wybrany_warsztat = obiekt
            break
    if wybrany_warsztat is None:
        return

    for obiekt in obiekty:
        if obiekt.marker:
            obiekt.marker.delete()
            obiekt.marker = None

    wybrany_warsztat.marker = map_widget.set_marker(wybrany_warsztat.coordinates[0], wybrany_warsztat.coordinates[1], text=wybrany_warsztat.nazwa)

    for obiekt in obiekty:
        if obiekt.typ in ["pracownik", "klient"] and obiekt.warsztat == wybrany_warsztat.nazwa:
            obiekt.marker = map_widget.set_marker(obiekt.coordinates[0], obiekt.coordinates[1], text=obiekt.nazwa)
