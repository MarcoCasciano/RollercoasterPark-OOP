# importo la classe Base dichiarativa di SQLAlchemy
from app.db.database import Base

# importo tutti i modelli così vengono registrati in Base.metadata
from app.models.attrazione import Attrazione
from app.models.famiglia import Famiglia
from app.models.visitatore import Visitatore
from app.models.giro import Giro

# definisco lista per silenziare avvisi 'unused import statement'
__all__ = ["Base", "Attrazione", "Famiglia", "Visitatore", "Giro"]

# espongo metadata che raccoglie tutti i modelli importati
# lo rendo facilmente accessibile a SQLAlchemy e Alembic
metadata = Base.metadata


