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
