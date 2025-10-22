from enum import Enum
from datetime import datetime
from typing import Optional, List
from models.comment import Comment
import uuid

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
    def __init__(
        self,
        title: str,
        description: str = "",
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        state: TaskState = TaskState.TODO,
        task_id: Optional[str] = None
    ):
        """
        Initialise une tâche.
        
        Args:
            title: Titre de la tâche (obligatoire)
            description: Description détaillée (optionnel)
            start_date: Date de début (optionnel)
            end_date: Date de fin (optionnel)
            state: État initial (par défaut: TODO)
            task_id: ID personnalisé (optionnel, sinon généré automatiquement)
        """
        # 1. Validation du titre (obligatoire)
        if not title or not title.strip():
            raise ValueError("Le titre est obligatoire")
        
        # 2. Génération ou assignation de l'UUID
        self.id = task_id if task_id else str(uuid.uuid4())
        
        # 3. Assignation des attributs
        self.title = title.strip()
        self.description = description.strip() if description else ""
        self.start_date = start_date  # Peut être None
        self.end_date = end_date      # Peut être None
        self.state = state
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
    
    def update(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        state: Optional[TaskState] = None
    ):
        """
        Met à jour les attributs de la tâche.
        
        Args:
            title: Nouveau titre (optionnel)
            description: Nouvelle description (optionnel)
            start_date: Nouvelle date de début (optionnel)
            end_date: Nouvelle date de fin (optionnel)
            state: Nouvel état (optionnel)
        """
        if title is not None:
            if not title.strip():
                raise ValueError("Titre vide interdit")
            self.title = title.strip()
        
        if description is not None:
            self.description = description.strip()
        
        if start_date is not None:
            self.start_date = start_date
        
        if end_date is not None:
            self.end_date = end_date
        
        if state is not None:
            self.state = state
        
        self._validate_dates()
        self.updated_at = datetime.now()

    def add_comment(self, comment):
      """
      Ajoute un commentaire à la tâche.
      
      Args:
          comment: Instance de Comment à ajouter
      """
      self.comments.append(comment)
      self.updated_at = datetime.now()

    
    def remove_comments(self, comments_to_remove: List['Comment']) -> int:
      """
      Supprime plusieurs commentaires.
      
      Args:
          comments_to_remove: Liste des objets Comment à supprimer
          
      Returns:
          Nombre de commentaires supprimés
      """
      initial_length = len(self.comments)
      comment_ids = {c.id for c in comments_to_remove}
      
      self.comments = [c for c in self.comments if c.id not in comment_ids]
      
      deleted_count = initial_length - len(self.comments)
      
      if deleted_count > 0:
          self.updated_at = datetime.now()
      
      return deleted_count
    
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