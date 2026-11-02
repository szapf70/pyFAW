import threading
import time

text = "Noch kein Text eingegeben"

def anzeige():
    while True:
        print(f"[Anzeige] {text}")
        time.sleep(5)

# Anzeige-Thread starten (daemon=True, damit das Programm beim Beenden des Hauptthreads sauber endet)
threading.Thread(target=anzeige, daemon=True).start()

# Hauptthread: Eingabe in Endlosschleife
while True:
    text = input("Neuer Text: ")
