import threading
import time
from flask import Flask, request, jsonify

# Gemeinsamer Zustand + Lock
_lock = threading.Lock()
_text = "Noch kein Text eingegeben"
_intervall = 2.0

app = Flask(__name__)


def get_text():
    with _lock:
        return _text


def set_text(neu):
    global _text
    with _lock:
        _text = neu


def get_intervall():
    with _lock:
        return _intervall


def set_intervall(neu):
    global _intervall
    with _lock:
        _intervall = neu


def anzeige():
    while True:
        print(f"[Anzeige] {get_text()}")
        time.sleep(get_intervall())


@app.route("/text", methods=["GET", "POST"])
def api_text():
    if request.method == "POST":
        daten = request.get_json(silent=True) or {}
        if "text" not in daten:
            return jsonify(fehler="Feld 'text' fehlt"), 400
        set_text(str(daten["text"]))
    return jsonify(text=get_text())


@app.route("/zeit", methods=["GET", "POST"])
def api_zeit():
    if request.method == "POST":
        daten = request.get_json(silent=True) or {}
        try:
            neu = float(daten["zeit"])
            if neu <= 0:
                raise ValueError
        except (KeyError, ValueError, TypeError):
            return jsonify(fehler="Feld 'zeit' muss eine Zahl > 0 sein"), 400
        set_intervall(neu)
    return jsonify(zeit=get_intervall())


def starte_flask():
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)


threading.Thread(target=anzeige, daemon=True).start()
threading.Thread(target=starte_flask, daemon=True).start()

# Hauptthread: Eingabe in Endlosschleife
while True:
    set_text(input("Neuer Text: "))
