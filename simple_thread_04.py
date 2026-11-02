import threading
import time
from flask import Flask, request, jsonify

# curl "http://127.0.0.1:5000/textloop?loop=off"
# curl "http://127.0.0.1:5000/textloop?loop=on"
# curl "http://127.0.0.1:5000/textloop"



# Gemeinsamer Zustand + Lock
_lock = threading.Lock()
_text = "Noch kein Text eingegeben"
_intervall = 2.0

# Event: gesetzt = Anzeige läuft, gelöscht = Anzeige pausiert
_loop_aktiv = threading.Event()
_loop_aktiv.set()  # Start: Anzeige läuft

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
        _loop_aktiv.wait()  # blockiert, solange das Event nicht gesetzt ist
        print(f"[Anzeige] {time.strftime("%H:%M:%S")} {get_text()}")
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


@app.route("/textloop", methods=["GET"])
def api_textloop():
    wert = request.args.get("loop")
    if wert is not None:
        wert = wert.lower()
        if wert == "on":
            _loop_aktiv.set()
        elif wert == "off":
            _loop_aktiv.clear()
        else:
            return jsonify(fehler="Argument 'loop' muss 'on' oder 'off' sein"), 400
    return jsonify(loop="on" if _loop_aktiv.is_set() else "off")


def starte_flask():
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)


threading.Thread(target=anzeige, daemon=True).start()
threading.Thread(target=starte_flask, daemon=True).start()

# Hauptthread:
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Beendet")
