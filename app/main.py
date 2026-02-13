"""
Simulatore di parco divertimenti "ROLLERCOASTER".

Simula il funzionamento di un parco divertimenti con famiglie che fruiscono
di diverse attrazioni.
Gestisce code, capienza e movimenti delle giostre.
"""

import random

LISTA_ATTRAZIONI_BAMBINI = ["Tazze", "Bruco", "Covo dei Pirati"]
LISTA_ATTRAZIONI_RAGAZZI = ["Raptor", "Blue Tornado", "Space Vertigo"]
# gli adulti si adeguano alle attrazioni scelte dai bambini in quanto accompagnatori


class PuntoCartesiano:
    """Rappresenta un punto in un sistema di coordinate cartesiane bidimensionale."""

    def __init__(self, x: int = 0, y: int = 0):
        """
        Inizializza un punto cartesiano.

        Args:
            x: Coordinata x (default: 0)
            y: Coordinata y (default: 0)
        """
        self.x: int = int(x)
        self.y: int = int(y)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    @classmethod
    def genera_random(cls):
        """
        Genera un punto cartesiano con coordinate casuali tra 0 e 5.

        Returns:
            PuntoCartesiano con coordinate random
        """
        return cls(random.randint(0, 5), random.randint(0, 5))


class Umano:
    """Classe base che rappresenta una persona nel parco."""

    def __init__(self,
                 posizione: PuntoCartesiano = None,
                 nome: str = "",
                 cognome: str = "",
                 tipo: str = "umano",
                 attrazioni_desiderate: list[str] = None):
        """
        Inizializza un umano.

        Args:
            posizione: posizione iniziale (se None viene chiamata genera_random())
            nome: nome della persona
            cognome: cognome della persona
            tipo: tipo di persona (umano, bambino, ragazzo, adulto)
            attrazioni_desiderate: lista di attrazioni che vorrebbe visitare
        """
        self.posizione = posizione if posizione is not None else PuntoCartesiano.genera_random()
        self.nome = nome.capitalize()
        self.cognome = cognome.capitalize()
        self.tipo = tipo.lower()
        self.attrazioni_desiderate = attrazioni_desiderate if attrazioni_desiderate is not None else []
        self.attrazioni_completate: list[str] = []

    def __repr__(self):
        return f"<{self.tipo.capitalize()}: {self.nome} {self.cognome} @ {self.posizione}>"

    def ha_completato_tutto(self) -> bool:
        """
        Verifica se la persona ha completato tutte le attrazioni desiderate.

        Returns:
            True se non ci sono più attrazioni da visitare, altrimenti False
        """
        return len(self.attrazioni_desiderate) == 0


class Bambino(Umano):
    """Rappresenta un bambino con attrazioni adatte alla sua età."""

    def __init__(self, posizione: PuntoCartesiano = None, nome: str = "", cognome: str = ""):
        """
        Inizializza un bambino con attrazioni casuali prese da LISTA_ATTRAZIONI_BAMBINI.

        Args:
            posizione: posizione iniziale
            nome: nome del bambino
            cognome: cognome del bambino
        """
        attrazioni_desiderate = random.sample(LISTA_ATTRAZIONI_BAMBINI, k=len(LISTA_ATTRAZIONI_BAMBINI))
        super().__init__(posizione, nome, cognome, "bambino", attrazioni_desiderate)


class Ragazzo(Umano):
    """Rappresenta un ragazzo con attrazioni adatte alla sua età."""

    def __init__(self, posizione: PuntoCartesiano = None, nome: str = "", cognome: str = ""):
        """
        Inizializza un ragazzo con attrazioni casuali prese da LISTA_ATTRAZIONI_RAGAZZI.

        Args:
            posizione: posizione iniziale
            nome: nome del ragazzo
            cognome: cognome del ragazzo
        """
        attrazioni_desiderate = random.sample(LISTA_ATTRAZIONI_RAGAZZI, k=len(LISTA_ATTRAZIONI_RAGAZZI))
        super().__init__(posizione, nome, cognome, "ragazzo", attrazioni_desiderate)


class Adulto(Umano):
    """Rappresenta un adulto che accompagna i bambini."""

    def __init__(self, posizione: PuntoCartesiano = None, nome: str = "", cognome: str = ""):
        """
        Inizializza un adulto con attrazioni per bambini (accompagnamento).

        Args:
            posizione: Posizione iniziale
            nome: Nome dell'adulto
            cognome: Cognome dell'adulto
        """
        attrazioni_desiderate = random.sample(LISTA_ATTRAZIONI_BAMBINI, k=len(LISTA_ATTRAZIONI_BAMBINI))
        super().__init__(posizione, nome, cognome, "adulto", attrazioni_desiderate)


class Location:
    """Classe base che rappresenta una location nel parco."""

    def __init__(self, nome: str, posizione: PuntoCartesiano = None):
        """
        Inizializza una location.

        Args:
            nome: nome della location
            posizione: posizione cartesiana (se None viene chiamata genera_random())
        """
        self.nome: str = nome.title()
        self.posizione = posizione if posizione is not None else PuntoCartesiano.genera_random()

    def __repr__(self):
        return f"{self.nome} @ {self.posizione}"


class Attrazione(Location):
    """Rappresenta un'attrazione del parco con gestione di code e capienza."""

    def __init__(self, nome: str, posizione: PuntoCartesiano = None, per_bambini: bool = True,
                 capienza_max: int = 5):
        """
        Inizializza un'attrazione.

        Args:
            nome: nome dell'attrazione
            posizione: posizione dell'attrazione
            per_bambini: True se adatta ai bambini, False se per ragazzi
            capienza_max: numero massimo di persone per corsa
        """
        super().__init__(nome, posizione)
        self.per_bambini = per_bambini
        self.capienza_massima = capienza_max
        self.capienza_attuale = capienza_max
        self.tempo_attesa = 0
        self.clienti_a_bordo: list[Umano] = []
        self.clienti_in_coda: list[Umano] = []

    def __repr__(self):
        stato = "La giostra è FERMA" if self.tempo_attesa == 0 else f"La giostra è IN MOVIMENTO ({self.tempo_attesa})"
        return f"[{self.nome.upper()}] Posti liberi: {self.capienza_attuale}/{self.capienza_massima} | Coda: {len(self.clienti_in_coda)} | {stato}"

    def attrazione_disponibile(self) -> bool:
        """
        Verifica se l'attrazione può accettare nuovi clienti.

        Returns:
            True se è ferma e ha posti liberi, False altrimenti
        """
        return self.tempo_attesa == 0 and self.capienza_attuale > 0

    def carica_cliente(self, cliente: Umano) -> bool:
        """
        Fa salire un cliente sull'attrazione se disponibile.

        Args:
            cliente: l'Umano da far salire

        Returns:
            True se il cliente è salito con successo, altrimenti False
        """
        if not self.attrazione_disponibile():
            return False

        # 1. Gestione Attrazione
        self.clienti_a_bordo.append(cliente)
        self.capienza_attuale -= 1

        # 2. Gestione Cliente (Sposta il desiderio solo qui!)
        if cliente.attrazioni_desiderate:
            # Usiamo pop(0) solo nel momento in cui siamo certi del carico
            completata = cliente.attrazioni_desiderate.pop(0)
            cliente.attrazioni_completate.append(completata)

        return True

    def aggiungi_a_coda(self, cliente: Umano):
        """
        Aggiunge un cliente alla coda dell'attrazione.

        Args:
            cliente: Il cliente da aggiungere in coda
        """
        self.clienti_in_coda.append(cliente)

    def scarica_clienti(self) -> list[Umano]:
        """
        Fa scendere tutti i clienti dall'attrazione e ripristina la capienza.

        Returns:
            lista dei clienti scesi
        """
        clienti_scesi = self.clienti_a_bordo[:]
        self.clienti_a_bordo = []
        self.capienza_attuale = self.capienza_massima
        return clienti_scesi

    def avvia_giostra(self, durata: int = 2):
        """
        Avvia l'attrazione se ci sono clienti a bordo.

        Args:
            durata: numero di cicli di attesa (default: 2)
        """
        if self.clienti_a_bordo:
            self.tempo_attesa = durata

    def avanza_tempo(self):
        """Decrementa il tempo di attesa dell'attrazione se in movimento."""
        if self.tempo_attesa > 0:
            self.tempo_attesa -= 1


class Famiglia:
    """Rappresenta una famiglia composta da adulti, bambini e ragazzi."""

    def __init__(self, cognome: str, adulti: list[Adulto] = None, bambini: list[Bambino] = None,
                 ragazzi: list[Ragazzo] = None):
        """
        Inizializza una famiglia.

        Args:
            cognome: cognome della famiglia
            adulti: lista di adulti (default: [])
            bambini: lista di bambini (default: [])
            ragazzi: lista di ragazzi (default: [])
        """
        self.cognome = cognome.capitalize()
        self.adulti = adulti if adulti is not None else []
        self.bambini = bambini if bambini is not None else []
        self.ragazzi = ragazzi if ragazzi is not None else []

        self.membri_famiglia = self.adulti + self.bambini + self.ragazzi
        for membro in self.membri_famiglia:
            membro.cognome = self.cognome

    def __repr__(self):
        return f"Famiglia {self.cognome} (Membri: {len(self.membri_famiglia)})"


def genera_famiglia(lista_nomi=None, lista_cognomi=None) -> Famiglia:
    """
    Genera una famiglia casuale con due adulti, un ragazzo e un bambino.

    Args:
        lista_nomi: lista di nomi tra cui scegliere (default: nomi italiani comuni)
        lista_cognomi: lista di cognomi tra cui scegliere (default: cognomi italiani comuni)

    Returns:
        Una nuova istanza di Famiglia con membri generati casualmente
    """
    nomi = lista_nomi or ["Marco", "Giovanni", "Paolo", "Luca", "Laura", "Sofia"]
    cognomi = lista_cognomi or ["Rossi", "Bianchi", "Verdi", "Viola"]
    cognome_scelto = random.choice(cognomi)

    return Famiglia(
        cognome = cognome_scelto,
        adulti = [Adulto(nome=random.choice(nomi)), Adulto(nome=random.choice(nomi)),],
        ragazzi = [Ragazzo(nome=random.choice(nomi))],
        bambini = [Bambino(nome=random.choice(nomi))]
    )


def stampa_statistiche(clienti: list[Umano]):
    """
    Stampa statistiche dettagliate di tutte le persone nel parco.

    Args:
        clienti: Lista di tutti i clienti del parco
    """
    print("\n" + "=" * 60)
    print("STATISTICHE FINALI")
    print("=" * 60)
    for cliente in clienti:
        completate = len(cliente.attrazioni_completate)
        rimanenti = len(cliente.attrazioni_desiderate)
        print(f"{cliente.nome} {cliente.cognome} ({cliente.tipo}): {completate} completate, {rimanenti} rimanenti")
        if cliente.attrazioni_completate:
            print(f"  → Completate: {', '.join(cliente.attrazioni_completate)}")
        if cliente.attrazioni_desiderate:
            print(f"  → Mancanti: {', '.join(cliente.attrazioni_desiderate)}")


def main():
    """
    Funzione principale che esegue la simulazione del parco divertimenti.

    Crea le attrazioni e le famiglie, poi esegue la simulazione ciclo per ciclo
    gestendo lo scarico, caricamento e movimento delle attrazioni.

    ARCHITETTURA:

    - clienti_liberi: clienti pronti per salire
    - tutti_i_clienti: tutti i clienti nel parco (per controlli e statistiche)
    - dizionario_attrazioni: nome → oggetto Attrazione

    CICLO DI SIMULAZIONE:

    1. SCARICO (tempo_attesa = 0 e clienti_a_bordo non vuoto)
       - Attrazioni finite scaricano i clienti
       - Clienti scesi → clienti_liberi
       - Ripristino capienza

    2. SMISTAMENTO (clienti_liberi)
       - Per ogni cliente con attrazioni_desiderate non vuota:
         a) Determina prossima attrazione desiderata
         b) Se attrazione ha posto e tempo_attesa = 0:
            - Carica
            - Rimuovi da clienti_liberi
         c) Altrimenti:
            - Aggiungi a coda
            - Rimuovi da clienti_liberi

    3. CARICO DALLE CODE (attrazioni con tempo_attesa = 0)
       - Riempie attrazioni vuote con clienti in coda
       - clienti_in_coda → clienti_a_bordo
       - Decrementa capienza_attuale

    4. MOVIMENTO
       - Attrazioni con clienti_a_bordo: avvia (tempo_attesa = 2)
       - Attrazioni in movimento: decrementa tempo_attesa

    5. CHECK FINALE
       - Se tutti i clienti hanno completato → fine simulazione
       - Usa tutti_i_clienti per il controllo globale

    """

    dizionario_attrazioni : dict[str, Attrazione] = {
        "Bruco": Attrazione("Bruco", per_bambini=True),
        "Covo dei Pirati": Attrazione("Covo dei Pirati", per_bambini=True),
        "Tazze": Attrazione("Tazze", per_bambini=True),
        "Raptor": Attrazione("Raptor", per_bambini=False),
        "Blue Tornado": Attrazione("Blue Tornado", per_bambini=False),
        "Space Vertigo": Attrazione("Space Vertigo", per_bambini=False)
    }
    # a differenza delle liste di attrazioni questa struttura contiene oggetti Attrazione

    clienti_liberi = []
    tutti_i_clienti = []

    # popolo le liste con ciclo for
    for _ in range(5):
        f = genera_famiglia()
        clienti_liberi.extend(f.membri_famiglia)
        tutti_i_clienti.extend(f.membri_famiglia)

    # All'inizio clienti_liberi e tutti_i_clienti contengono gli stessi elementi.
    # Durante la simulazione:
    # - clienti_liberi: lista dinamica di chi non è in coda o su un'attrazione
    # - tutti_i_clienti: lista statica di riferimento per statistiche e controllo completamento

    max_ripetizioni = 50
    for ciclo in range(max_ripetizioni):
        print(f"\n{'=' * 60}")
        print(f"CICLO {ciclo}")
        print(f"{'=' * 60}")

        for attr in dizionario_attrazioni.values():
            if attr.tempo_attesa == 0 and attr.clienti_a_bordo:
                clienti_scesi = attr.scarica_clienti()
                clienti_liberi.extend(clienti_scesi)

        for cliente in clienti_liberi[:]:
            if cliente.attrazioni_desiderate:
                meta = cliente.attrazioni_desiderate[0]
                giostra = dizionario_attrazioni[meta]

                if giostra.carica_cliente(cliente):
                    clienti_liberi.remove(cliente)
                else:
                    giostra.aggiungi_a_coda(cliente)
                    clienti_liberi.remove(cliente)

        for attr in dizionario_attrazioni.values():
            if attr.tempo_attesa == 0:
                while attr.capienza_attuale > 0 and attr.clienti_in_coda:
                    cliente = attr.clienti_in_coda.pop(0)
                    attr.carica_cliente(cliente)

                attr.avvia_giostra()
            else:
                attr.avanza_tempo()

            print(attr)

        tutti_hanno_finito = all(c.ha_completato_tutto() for c in tutti_i_clienti)
        if tutti_hanno_finito:
            print(f"\n TUTTI I CLIENTI HANNO COMPLETATO LE ATTRAZIONI! (Ciclo {ciclo})")
            break

        risposta = input("\nInvio per continuare, 'q' per uscire: ")
        if risposta.lower() == 'q':
            break

    stampa_statistiche(tutti_i_clienti)


if __name__ == "__main__":
    main()
