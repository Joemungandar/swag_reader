# AUTOR: Jens Fabry

from tkinter import *
import tkinter.messagebox
from tkcalendar import DateEntry
import swag_datahandler as sdh


# Grundaufbau:
swag = Tk()
swag.title("SWaG-Tool")
swag.configure(bg="black")
swag_frame = Frame(relief=RAISED,bd=8,bg="green")
category = StringVar(swag_frame)
# TODO:Detect Key in Python (keylistener)

### Methoden:
# Methode, um Daten aus der gespeicherten json-Datei zu löschen
def erase_data():
    confirmed = tkinter.messagebox.askyesno(title="Eingabe leeren",message="Bist Du sicher?")
    if confirmed:
        print("Daten werden gelöscht...")
        file_name = category.get() + ".json"
        global datepicker_erase_from, datepicker_erase_until
        erase_from = datepicker_erase_from.get()
        erase_until = datepicker_erase_until.get()
        success = sdh.delete_from_Json_file(file_name, erase_from, erase_until)
        if not success:
            tkinter.messagebox.askyesno(title="Eingabefehler", message="Fehler bei der Eingabe! Bitte überprüfe, ob das Datum unten weiter in der Zukunft liegt, als das Datum oben!")


def keylistener(event):
    ACCEPTED = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]
    if not event.char in ACCEPTED:
        pass  
        # Dont let the character be inputed


# Methode zum Aufruf eines Extra-Fensters zum Leeren aller Textfelder & Anzeigen
def erase_data_menu():

    # Untermethode, um das Extra-Fenster wieder zu schließen
    def close_window():
        top.destroy()
        top.update()

    print("Daten löschen gedrückt...")
    top = Toplevel(swag)
    top.configure(bg="black")
    top_frame = Frame(top, relief=RAISED,bd=8,bg="green")

    # Label, Button:
    label_erase = Label(top_frame, text = "DATEN LÖSCHEN", font=30, background="green", height=4)
    label_from = Label(top_frame, text = "VON:", background="green", height=2)
    label_until = Label(top_frame, text = "BIS (inkl.):", background="green", height=2)
    global datepicker_erase_from, datepicker_erase_until
    datepicker_erase_from = DateEntry(top_frame, width=12, background="lime", foreground="black", date_pattern="dd.mm.yyyy")
    datepicker_erase_until = DateEntry(top_frame, width=12, background="lime", foreground="black", date_pattern="dd.mm.yyyy")
    button_erase_data = Button(top_frame, bg="red",fg="black", text="Daten löschen", command=erase_data)
    button_close = Button(top_frame, bg="orange", fg="black", text="Fenster schließen", command=close_window)

    # Layout:
    top_frame.grid()
    label_erase.grid(columnspan=2)
    label_from.grid()
    label_until.grid()
    button_erase_data.grid(columnspan=2)
    button_close.grid(columnspan=2)
    datepicker_erase_from.grid(column=1, row=1)
    datepicker_erase_until.grid(column=1, row=2)


# Methode zum Bestätigen/Abspeichern
def save_as_json():
    json_file = category.get() + ".json"
    try:
        meter_value = float(meter_graph.get())
        date = datepicker.get()
        last_reading, last_date = update_last_reading()
        print(last_date, type(last_date))
        if(last_reading > meter_value):
            tkinter.messagebox.askyesno(title="Messwert-Fehler", message="Es kann kein niedrigerer Wert als " + str(last_reading) + " eingegeben werden!")
            return
        check_date = sdh.check_dates(date, last_date)
        if not check_date:
            tkinter.messagebox.askyesno(title="Datum-Fehler", message="Es kann kein niedrigeres Datum als das letzte Datum (" + last_date + ") eingegeben werden!")
            return
        new_entry = {
            "Datum": datepicker.get(),
            ("Zählerstand_" + category.get()): meter_value
        }
        print("Speichere...")
        sdh.save_To_Json_File(json_file, new_entry)
        update_last_reading()
        print("Speichern erfolgreich!")
    except(ValueError):
        error_message = "Bitte Gib in das Feld eine gültige Dezimalzahl ein (mit PUNKT, kein Text, kein Komma!)"
        print(error_message)
        error = tkinter.messagebox.askyesno(title="FEHLER", message=error_message)

# Methode zur Ermittlung des letzten Zählerstands
def update_last_reading():
    data_name = category.get() + ".json"
    tmp_list_readings = sdh.read_data_from_file(data_name)
    if len(tmp_list_readings) == 0:
        print("Keine gefüllte Liste gefunden")
        label_info_last_reading["text"] = "---"
        default_date = "01.01.0001"
        return 0.0, default_date
    last_entry = tmp_list_readings[-1]
    reading_category = "Zählerstand_" + category.get()
    last_reading = last_entry[reading_category]
    print("Letzter Eintrag:", last_reading, type(last_reading))
    label_info_last_reading["text"] = last_reading
    last_date = last_entry["Datum"]
    return last_reading, last_date
    

# Methode zum richtigen Anzeigen der Einheit:
def update_unit(event):
    if (category.get() == "Strom" or category.get() == "Heizstrom"):
        label_unit["text"] = "kWh"
        label_unit_2["text"] = "kWh"
    else:
        label_unit["text"] = "m³"
        label_unit_2["text"] = "m³"
    update_last_reading()

# GUI-Methode zum Anzeigen des Graphen (Linien-Diagramm)
def show_graph_gui():
    tmp_category = category.get()
    print("Zeige Zählerstand", tmp_category, "..." )
    sdh.show_graph(tmp_category)

# GUI-Methode zum Anzeigen des Verbrauchs (Balken-diagramm)
def show_consumption_gui():
    tmp_category = category.get()
    print("Zeige Verbrauch", tmp_category, "...")
    sdh.show_consumption(tmp_category)

# Labels:
label_title = Label(swag_frame, bg="green", fg="black", text="SWAG-Tool", font=30, height=4)
label_category = Label(swag_frame, bg="green", fg="black", text="Kategorie:", height=2)
label_date = Label(swag_frame, bg="green", fg="black", text="Datum:", height=2)
label_meter_graph = Label(swag_frame, bg="green", fg="black", text="Zählerstand:", height=2)
label_seperator = Label(swag_frame, bg="green", fg="black", text="-----------------------------------", height=2)
label_last_reading = Label(swag_frame, bg="green", fg="black", text="Letzter Zählerstand: ")
label_info_last_reading = Label(swag_frame, bg="lime", fg="black", text="")
label_unit = Label(swag_frame, bg="green", fg="black", text="kWh")
label_unit_2 = Label(swag_frame, bg="green", fg="black", text="kWh")

# Drop-Down-Menu
category.set("Strom")
categories = ["Strom", "Wasser", "Gas", "Heizstrom"]
category_menu = OptionMenu(swag_frame, category, *categories, command=update_unit)

# Datums- & Textfelder:
datepicker = DateEntry(swag_frame, width=12, background="lime", foreground="black", date_pattern="dd.mm.yyyy")
meter_graph = Entry(swag_frame,bg="lime",fg="black")

# Buttons:
button_erase = Button(swag_frame,bg="red",fg="black", text="Zählerstände löschen...", command=erase_data_menu)
button_save = Button(swag_frame,bg="orange", fg="white", text="Speichere Daten...", command=save_as_json)
button_show_graph = Button(swag_frame, bg="lime", fg="black", text="Plot Zählerstand", command=show_graph_gui)
button_show_consumption = Button(swag_frame, bg="lime", fg="black", text="Plot Verbrauch", command=show_consumption_gui)

# Baue Umgebung:
swag_frame.grid()
# Labels
label_title.grid(column=0,row=0, columnspan=4)
label_category.grid(column=0, row=2)
label_date.grid(column=0, row=3)
label_meter_graph.grid(column=0, row=4)
label_seperator.grid(column=0,row=5,columnspan=4)
label_last_reading.grid(column=0, row=6)
label_info_last_reading.grid(column=1, row=6)
label_unit.grid(column=2, row=4)
label_unit_2.grid(column=2, row=6)
# Eingabe-Felder
category_menu.grid(column=1, row=2)
datepicker.grid(column=1, row=3)
meter_graph.grid(column=1, row=4)
# Buttons
button_save.grid(column=0, row=8, pady=10, padx=20, columnspan=4)
button_erase.grid(column=0, row=9, columnspan=4)
button_show_graph.grid(column = 0, row=10, pady=10, padx= 20, columnspan=2)
button_show_consumption.grid(column = 2, row=10, pady=10, padx= 20, columnspan=2)

# Update_event
swag.after(1, update_last_reading)

# Start Keylistener
swag.bind('<KeyPress>', keylistener)

# Starte Programm
swag.mainloop()