from sqlalchemy.orm import Session
from app.models.visitatore import Visitatore
from app.models.attrazione import Attrazione


def esegui_ciclo_simulazione(db: Session):
    # --- 1. SCARICO ---
    attrazioni_in_movimento = db.query(Attrazione).filter(Attrazione.tempo_attesa == 0).all()
    for attr in attrazioni_in_movimento:
        # Trova chi è a bordo di QUESTA attrazione e "liberalo"
        passeggeri = db.query(Visitatore).filter(Visitatore.attrazione_attuale_id == attr.id).all()
        for p in passeggeri:
            p.attrazione_attuale_id = None  # Torna libero
        attr.capienza_attuale = attr.capienza_massima

    # --- 2. SMISTAMENTO (Logica dei desideri) ---
    # Prendi i visitatori liberi che hanno ancora desideri
    liberi = db.query(Visitatore).filter(Visitatore.attrazione_attuale_id == None).all()
    for v in liberi:
        if v.attrazioni_desiderate:
            prossima = v.attrazioni_desiderate[0]
            giostra = db.query(Attrazione).filter(Attrazione.nome == prossima).first()

            if giostra and giostra.capienza_attuale > 0 and giostra.tempo_attesa == 0:
                # Carica
                v.attrazioni_completate.append(v.attrazioni_desiderate.pop(0))
                v.attrazione_attuale_id = giostra.id
                giostra.capienza_attuale -= 1
            else:
                # Metti in coda (logica semplificata per l'esempio)
                pass

    # --- 3. AVANZA TEMPO ---
    tutte = db.query(Attrazione).all()
    for a in tutte:
        if a.tempo_attesa > 0:
            a.tempo_attesa -= 1
        elif a.capienza_attuale < a.capienza_massima:
            a.tempo_attesa = 2  # Parte la corsa

    db.commit()
    return {"status": "Ciclo eseguito"}