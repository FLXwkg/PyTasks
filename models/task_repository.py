import json
import os
from typing import List, Optional
from models.task import Task, TaskState

class TaskRepository:
    def __init__(self, file_path: str = "tasks.json"):
        self.file_path = file_path
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Crée le fichier s'il n'existe pas"""
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)
    
    def load_all(self) -> List[Task]:
        """Charge toutes les tâches"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Task.from_dict(task_data) for task_data in data]
        except json.JSONDecodeError:
            return []  # Fichier corrompu = liste vide
    
    def save(self, task: Task):
        """Sauvegarde/Update une tâche"""
        tasks = self.load_all()
        
        # Cherche si déjà existante
        for i, t in enumerate(tasks):
            if t.id == task.id:
                tasks[i] = task  # Update
                break
        else:
            tasks.append(task)  # Create
        
        # Sauvegarde tout
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump([t.to_dict() for t in tasks], f, ensure_ascii=False, indent=2)
    
    def delete(self, task_id: str) -> bool:
        """Supprime une tâche par son ID"""
        tasks = self.load_all()
        initial_length = len(tasks)
        
        # Filtre : garde toutes les tâches SAUF celle à supprimer
        tasks = [t for t in tasks if t.id != task_id]
        
        # Si la liste est plus courte, on a bien supprimé quelque chose
        if len(tasks) < initial_length:
            # Sauvegarde la nouvelle liste sans la tâche supprimée
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(
                    [t.to_dict() for t in tasks],
                    f,
                    ensure_ascii=False,
                    indent=2
                )
            return True  # Suppression réussie
        
        return False  # Aucune tâche trouvée avec cet ID
    
    def search(self, query: str, state_filter: Optional[TaskState] = None) -> List[Task]:
        """Recherche + filtre"""
        tasks = self.load_all()
        results = []
        
        query_lower = query.lower() if query else ""
        
        for task in tasks:
            # Filtre par état
            if state_filter and task.state != state_filter:
                continue
            
            # Recherche dans titre (case-insensitive)
            if query and query_lower not in task.title.lower():
                continue
            
            results.append(task)
        
        return results