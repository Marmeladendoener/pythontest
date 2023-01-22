#!/usr/bin/env python3
from dialog import Dialog
from configparser import ConfigParser
import sys

a = Dialog(dialog="dialog")
cfg = ConfigParser()
cfg.read("config.ini")

def startbildschirm():
    code, tag = a.menu("Was willst du machen?: ",
                   choices=[("anzeigen", "Bestehende Einträge anzeigen lassen"),
                            ("erstellen", "Eintrag erstellen")])
    if code == Dialog.OK:
        if tag == "erstellen":
            erstelleEintrag()
        elif tag == "anzeigen":
            anzeigenEintrag()

def erstelleEintrag():
    code, fields = a.form("Bitte fülle das folgende Formular aus: ",
                              [("Name", 1, 1, "", 1, 25, 20, 20),
                               ("Adresse", 2, 1, "", 2, 25, 20, 20),
                               ("Alter", 3, 1, "", 3, 25, 20, 20)])
    
    if fields[0] and fields[1] and fields[2] and code == Dialog.OK:
        cfg.add_section(fields[0])
        cfg.set(fields[0], "Name", fields[0])
        cfg.set(fields[0], "Adresse", fields[1])
        cfg.set(fields[0], "Alter", fields[2])

        with open("config.ini", "w") as configfile:
            cfg.write(configfile)
        
        startbildschirm()
    
    elif code == Dialog.OK: startbildschirm()
    


def anzeigenEintrag():
    sections = cfg.sections()
    outputSections = [(str(index), value) for index, value in enumerate(sections)]
    
    code, tag = a.menu("Von welcher Person willst du mehr wissen? ",
                       choices=outputSections)
    
    inhalt = cfg.items(sections[int(tag)])
    ausgabe = ""
    for key, value in inhalt:
        ausgabe += key + " = " + value + "\n"
    
    a.msgbox(ausgabe, title=sections[int(tag)], width=50, height=10)
    if code == Dialog.OK: startbildschirm()



startbildschirm()
