btn_add_warsztat = Button(frame_buttons, text="Dodaj warsztat", width=20, command=lambda: dodaj_obiekt("warsztat"))
btn_add_pracownik = Button(frame_buttons, text="Dodaj pracownika", width=20, command=lambda: dodaj_obiekt("pracownik"))
btn_add_klient = Button(frame_buttons, text="Dodaj klienta", width=20, command=lambda: dodaj_obiekt("klient"))

btn_edit = Button(frame_buttons, text="Aktualizuj zaznaczony", width=20, command=edytuj_obiekt)
btn_delete = Button(frame_buttons, text="Usuń zaznaczony", width=20, command=usun_obiekt)
btn_show_all = Button(frame_buttons, text="Pokaż wszystkie", width=20, command=pokaz_wszystkie)
btn_show_selected = Button(frame_buttons, text="Pokaż wybrany warsztat", width=20, command=pokaz_wybrany_warsztat)

btn_add_warsztat.grid(row=0, column=0, padx=5, pady=5)
btn_add_pracownik.grid(row=0, column=1, padx=5, pady=5)
btn_add_klient.grid(row=0, column=2, padx=5, pady=5)

btn_edit.grid(row=1, column=0, padx=5, pady=5)
btn_delete.grid(row=1, column=1, padx=5, pady=5)
btn_show_all.grid(row=1, column=2, padx=5, pady=5)
btn_show_selected.grid(row=2, column=0, columnspan=3, pady=5)

odswiez_listy()
pokaz_wszystkie()

root.mainloop()