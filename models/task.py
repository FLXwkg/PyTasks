from enum import Enum
from datetime import datetime
import uuid
from comment import Comment 

class TaskState(Enum):
    """Les 5 états possibles"""
    TODO = "À faire"
    IN_PROGRESS = "En cours"
    DONE = "Réalisé"
    ABANDONED = "Abandonné"
    WAITING = "En attente"
    
    @classmethod
    def from_string(cls, state_str: str):
        """Convertit une chaîne en TaskState"""
        for state in cls:
            if state.value == state_str:
                return state
        raise ValueError(f"État invalide: {state_str}")

class Task:
    def __init__(self, title: str, description: str = ""):
        # 1. Validation du titre (obligatoire)
        if not title or not title.strip():
            raise ValueError("Le titre est obligatoire")
        
        # 2. Génération de l'UUID
        self.id = str(uuid.uuid4())
        
        # 3. Assignation des attributs
        self.title = title.strip()
        self.description = description.strip()
        self.state = TaskState.TODO
        self.comments = []  # Liste vide au départ
        
        # 4. Timestamps
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
        # 5. Validation métier
        self._validate_dates()
    
    def _validate_dates(self):
        """Règle métier : end_date > start_date"""
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValueError("Date de fin avant date de début")
    
    def update(self, title=None, description=None):
        """Met à jour et recalcule updated_at"""
        if title is not None:
            if not title.strip():
                raise ValueError("Titre vide interdit")
            self.title = title.strip()
        if description is not None:
            self.description = description.strip()
        self._validate_dates()
        self.updated_at = datetime.now()
    
    def close_task(self):
        """Clôture = DONE + end_date auto"""
        self.state = TaskState.DONE
        self.end_date = datetime.now()
        self.updated_at = datetime.now()
    
    def to_dict(self) -> dict:
        """Pour sauvegarder en JSON"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "state": self.state.value,  # Enum -> string
            "comments": [c.to_dict() for c in self.comments],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """Pour charger depuis JSON"""
        from models.comment import Comment
        
        task = cls(
            title=data["title"],
            description=data.get("description", ""),
            start_date=datetime.fromisoformat(data["start_date"]) if data.get("start_date") else None,
            end_date=datetime.fromisoformat(data["end_date"]) if data.get("end_date") else None,
            state=TaskState.from_string(data["state"]),
            task_id=data["id"]
        )
        
        # Restaure les timestamps
        task.created_at = datetime.fromisoformat(data["created_at"])
        task.updated_at = datetime.fromisoformat(data["updated_at"])
        
        # Restaure les commentaires
        task.comments = [Comment.from_dict(c) for c in data.get("comments", [])]
        
        return task