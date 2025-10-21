# Todo (Chill)

Semplice demo: interfaccia `home.html` che comunica con un server Python (Flask) e persiste i todo in `db_python.json`.

Prerequisiti
- Python 3.8+ (consigliato 3.10+)

Installazione e avvio

1. Apri un terminale nella cartella del progetto `Todo(Chill)`.
2. (Opzionale ma consigliato) crea e attiva un virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Installa le dipendenze:

```powershell
pip install -r requirements.txt
```

Se non è presente `requirements.txt`, installa Flask direttamente:

```powershell
pip install Flask
```

4. Avvia il server Python:

```powershell
python server_python.py
```

Per default il server ascolta sulla porta `3001`. Apri il browser su `http://localhost:3001` per vedere `home.html`.

API
- GET `/api/todos` - Lista i todo
- POST `/api/todos` - Crea un todo (body JSON: `{ "text": "da fare" }`)
- PUT `/api/todos/:id` - Aggiorna un todo
- DELETE `/api/todos/:id` - Elimina un todo
- DELETE `/api/todos` - Elimina tutti i todo
- POST `/api/import` - Importa un array di todo (JSON array)

Note
- I dati vengono scritti in `db_python.json` nella stessa cartella.
- Se vuoi cambiare la porta, modifica la chiamata `app.run(port=3001)` in `server_python.py`.

Rimozione Node.js
- Tutti i file relativi al server Node/Express sono stati rimossi da questa cartella; il progetto utilizza ora esclusivamente il server Python.

Contatti
- Se hai bisogno di aiuto per configurare l'ambiente Python, fammi sapere e posso aggiungere istruzioni personalizzate.
