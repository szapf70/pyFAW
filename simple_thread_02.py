import threading
import time
from flask import Flask, request, jsonify

# curl -X POST http://127.0.0.1:5000/text -H "Content-Type: application/json" -d "{\"text\": \"Hallo Welt\"}"

# Gemeinsamer Zustand
text = "Noch kein Text eingegeben"
intervall = 2.0

app = Flask(__name__)


def anzeige():
    while True:
        print(f"[Anzeige] {text}")
        time.sleep(intervall)


@app.route("/text", methods=["GET", "POST"])
def api_text():
    global text
    if request.method == "POST":
        daten = request.get_json(silent=True) or {}
        if "text" not in daten:
            return jsonify(fehler="Feld 'text' fehlt"), 400
        text = str(daten["text"])
    return jsonify(text=text)


@app.route("/zeit", methods=["GET", "POST"])
def api_zeit():
    global intervall
    if request.method == "POST":
        daten = request.get_json(silent=True) or {}
        try:
            neu = float(daten["zeit"])
            if neu <= 0:
                raise ValueError
        except (KeyError, ValueError, TypeError):
            return jsonify(fehler="Feld 'zeit' muss eine Zahl > 0 sein"), 400
        intervall = neu
    return jsonify(zeit=intervall)


def starte_flask():
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)


# Threads starten
threading.Thread(target=anzeige, daemon=True).start()
threading.Thread(target=starte_flask, daemon=True).start()

# Hauptthread:
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Beendet")

