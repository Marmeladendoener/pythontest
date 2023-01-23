#!/usr/bin/env python3
from dialog import Dialog
from configparser import ConfigParser
import sys

a = Dialog(dialog="dialog")
cfg = ConfigParser()
cfg.read("config.ini")

def ändernLöschenEintrag():
    sections = cfg.sections()

    if sections:
        outputSections = [(str(index), value) for index, value in enumerate(sections)]
        code, tag = a.menu("Welche Person willst du bearbeiten?i ",
                           choices=outputSections)

        if code == Dialog.OK:
            inhalt = cfg.items(sections[int(tag)])
            oldName = inhalt[0][1]
            code, fields = a.form("Bitte fülle das folgende Formular aus: ",
                              [("Name", 1, 1, inhalt[0][1], 1, 25, 20, 20),
                               ("Adresse", 2, 1, inhalt[1][1], 2, 25, 20, 20),
                               ("Alter", 3, 1, inhalt[2][1], 3, 25, 20, 20)])
            if fields[0] and fields[1] and fields[2] and code == Dialog.OK:
                cfg.remove_section(oldName)
                cfg.add_section(fields[0])
                cfg.set(fields[0], "Name", fields[0])
                cfg.set(fields[0], "Adresse", fields[1])
                cfg.set(fields[0], "Alter", fields[2])

                with open("config.ini", "w") as configfile:
                    cfg.write(configfile)

                    startbildschirm()

            elif code == Dialog.OK: startbildschirm()
    
    else:
        code = a.msgbox("Keine Einträge vorhanden", title="", width=50, height=10)

    if code and code == Dialog.OK: startbildschirm()


def startbildschirm():
    code, tag = a.menu("Was willst du machen?: ",
                   choices=[("anzeigen", "Bestehende Einträge anzeigen lassen"),
                            ("erstellen", "Eintrag erstellen"),
                            ("bearbeiten", "Eintrag bearbeiten")])
    if code == Dialog.OK:
        if tag == "erstellen":
            erstelleEintrag()
        elif tag == "anzeigen":
            anzeigenEintrag()
        elif tag == "bearbeiten":
            ändernLöschenEintrag()

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

    if sections:
        outputSections = [(str(index), value) for index, value in enumerate(sections)]
        code, tag = a.menu("Von welcher Person willst du mehr wissen? ",
                           choices=outputSections)

        inhalt = cfg.items(sections[int(tag)])
        ausgabe = ""

        for key, value in inhalt:
            ausgabe += key + " = " + value + "\n"

        a.msgbox(ausgabe, title=sections[int(tag)], width=50, height=10)

    else:
        code = a.msgbox("Keine Einträge vorhanden", title="", width=50, height=10)

    if code and code == Dialog.OK: startbildschirm()


if __name__ == "__main__":
    startbildschirm()
