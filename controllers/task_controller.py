"""
Contrôleur principal de l'application PyTasks.
Fait le lien entre les vues (UI) et les modèles (logique métier).
"""
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QMessageBox
from typing import Optional, List
from datetime import datetime

from models.task import Task, TaskState
from models.comment import Comment
from models.task_repository import TaskRepository
from utils.logger import Logger


class TaskController(QObject):
    """
    Contrôleur principal gérant la logique de l'application.
    Hérite de QObject pour pouvoir émettre des signaux Qt.
    """
    
    # Signaux pour notifier la vue des changements
    tasks_updated = Signal()  # Émis quand la liste change
    task_selected = Signal(Task)  # Émis quand une tâche est sélectionnée
    
    def __init__(self, repository: TaskRepository, logger: Logger):
        super().__init__()
        self.repository = repository
        self.logger = logger
        self.current_task: Optional[Task] = None
        self.tasks = []
    
    # ========== CHARGEMENT ==========
    
    def load_tasks(self):
        """Charge toutes les tâches depuis le repository"""
        try:
            self.tasks = self.repository.load_all()
            self.logger.log("info", f"{len(self.tasks)} tâche(s) chargée(s)")
            self.tasks_updated.emit()
        except Exception as e:
            self.logger.log("error", f"Erreur de chargement : {str(e)}")
            self.tasks = []
    
    # ========== CRÉATION ==========
    
    def create_task(self, title: str, description: str = "") -> bool:
        """
        Crée une nouvelle tâche.
        
        Returns:
            bool: True si succès, False sinon
        """
        try:
            # Validation
            if not title or not title.strip():
                self._show_error("Le titre est obligatoire")
                return False
            
            # Création
            task = Task(title=title, description=description)
            
            # Sauvegarde
            self.repository.save(task)
            
            # Log et notification
            self.logger.log("info", f"Tâche créée : '{task.title}'")
            self.load_tasks()  # Recharge la liste
            
            return True
            
        except ValueError as e:
            self._show_error(f"Erreur de validation : {str(e)}")
            return False
        except Exception as e:
            self.logger.log("error", f"Erreur création : {str(e)}")
            self._show_error(f"Erreur : {str(e)}")
            return False
    
    # ========== MISE À JOUR ==========
    
    def update_current_task(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        state: Optional[TaskState] = None
    ) -> bool:
        """
        Met à jour la tâche actuellement sélectionnée.
        
        Returns:
            bool: True si succès
        """
        if not self.current_task:
            self._show_error("Aucune tâche sélectionnée")
            return False
        
        try:
            # Mise à jour via la méthode métier
            self.current_task.update(
                title=title,
                description=description,
                start_date=start_date,
                end_date=end_date,
                state=state
            )
            
            # Sauvegarde
            self.repository.save(self.current_task)
            
            # Log
            self.logger.log("info", f"Tâche mise à jour : '{self.current_task.title}'")
            self.load_tasks()
            
            return True
            
        except ValueError as e:
            self._show_error(f"Validation échouée : {str(e)}")
            return False
        except Exception as e:
            self.logger.log("error", f"Erreur MAJ : {str(e)}")
            self._show_error(f"Erreur : {str(e)}")
            return False
        
    def set_waiting_for(self, task_id: str, waiting_for_id: Optional[str]) -> bool:
      """
      Définit la tâche dont dépend la tâche actuelle.
      
      Args:
          task_id: ID de la tâche à modifier
          waiting_for_id: ID de la tâche dont on dépend (None pour retirer)
      """
      try:
          task = self.repository.find_by_id(task_id)
          if not task:
              return False
          
          task.waiting_for = waiting_for_id
          task.updated_at = datetime.now()
          self.repository.save(task)
          
          if waiting_for_id:
              waiting_task = self.repository.find_by_id(waiting_for_id)
              self.logger.log(
                  "info",
                  f"Tâche '{task.title}' en attente de '{waiting_task.title if waiting_task else 'tâche inconnue'}'"
              )
          else:
              self.logger.log("info", f"Dépendance retirée de '{task.title}'")
          
          self.load_tasks()
          return True
          
      except Exception as e:
          self.logger.log("error", f"Erreur définition dépendance : {str(e)}")
          return False

    def start_waiting_task(self) -> bool:
        """Démarre la tâche en attente actuelle (passe à TODO)"""
        if not self.current_task:
            return False
        
        if self.current_task.state != TaskState.WAITING:
            return False
        
        try:
            self.current_task.start_task()
            self.repository.save(self.current_task)
            
            self.logger.log("success", f"Tâche démarrée : '{self.current_task.title}'")
            self.load_tasks()
            
            return True
            
        except Exception as e:
            self.logger.log("error", f"Erreur démarrage : {str(e)}")
            return False
    
    # ========== SUPPRESSION ==========
    
    def delete_task(self, task_id: str) -> bool:
        """Supprime une tâche"""
        try:
            task = self.repository.find_by_id(task_id)
            if not task:
                return False
            
            # Demande confirmation
            reply = QMessageBox.question(
                None,
                "Confirmation",
                f"Supprimer la tâche '{task.title}' ?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.repository.delete(task_id)
                self.logger.log("warning", f"Tâche supprimée : '{task.title}'")
                
                # Réinitialise la sélection
                if self.current_task and self.current_task.id == task_id:
                    self.current_task = None
                
                self.load_tasks()
                return True
            
            return False
            
        except Exception as e:
            self.logger.log("error", f"Erreur suppression : {str(e)}")
            self._show_error(f"Erreur : {str(e)}")
            return False
    
    # ========== CLÔTURE ==========
    
    def close_current_task(self) -> bool:
        """Clôture la tâche actuelle (état = DONE)"""
        if not self.current_task:
            return False
        
        try:
            self.current_task.close_task()
            self.repository.save(self.current_task)
            
            self.logger.log("success", f"Tâche clôturée : '{self.current_task.title}'")
            self.load_tasks()
            
            return True
            
        except Exception as e:
            self.logger.log("error", f"Erreur clôture : {str(e)}")
            return False
    
    # ========== COMMENTAIRES ==========
    
    def add_comment_to_current_task(self, content: str) -> bool:
        """Ajoute un commentaire à la tâche actuelle"""
        if not self.current_task:
            return False
        
        try:
            comment = Comment(content=content)
            self.current_task.add_comment(comment)
            self.repository.save(self.current_task)
            
            self.logger.log("info", f"Commentaire ajouté à '{self.current_task.title}'")
            self.task_selected.emit(self.current_task)  # Rafraîchit l'affichage
            
            return True
            
        except ValueError as e:
            self._show_error(f"Commentaire invalide : {str(e)}")
            return False
        
    def delete_comments_from_current_task(self, comments: List) -> bool:
        """
        Supprime plusieurs commentaires de la tâche actuelle.
        
        Args:
            comments: Liste des objets Comment à supprimer
            
        Returns:
            True si au moins un commentaire a été supprimé
        """
        if not self.current_task or not comments:
            return False
        
        try:
            deleted_count = self.current_task.remove_comments(comments)
            
            if deleted_count > 0:
                self.repository.save(self.current_task)
                
                # Log différent selon le nombre
                if deleted_count == 1:
                    comment_content = comments[0].content[:50]  # Limite à 50 caractères
                    self.logger.log(
                        "warning",
                        f"Commentaire supprimé de '{self.current_task.title}' : '{comment_content}'"
                    )
                else:
                    self.logger.log(
                        "warning",
                        f"{deleted_count} commentaires supprimés de '{self.current_task.title}'"
                    )
                
                self.task_selected.emit(self.current_task)  # Rafraîchit l'affichage
                return True
            
            return False
            
        except Exception as e:
            self.logger.log("error", f"Erreur suppression commentaire(s) : {str(e)}")
            return False
    
    # ========== SÉLECTION ==========
    
    def select_task(self, task_id: str):
        """Sélectionne une tâche par son ID"""
        task = self.repository.find_by_id(task_id)
        if task:
            self.current_task = task
            self.task_selected.emit(task)
    
    def deselect_task(self):
        """Désélectionne la tâche actuelle"""
        self.current_task = None
    
    # ========== RECHERCHE & FILTRE ==========
    
    def search_and_filter(self, query: str, state_filter: Optional[TaskState] = None):
        """
        Recherche et filtre les tâches.
        Met à jour self.tasks avec les résultats.
        """
        try:
            self.tasks = self.repository.search(query, state_filter)
            self.tasks_updated.emit()
        except Exception as e:
            self.logger.log("error", f"Erreur recherche : {str(e)}")
    
    # ========== UTILITAIRES ==========
    
    def _show_error(self, message: str):
        """Affiche une boîte de dialogue d'erreur"""
        QMessageBox.critical(None, "Erreur", message)
    
    def get_all_tasks(self):
        """Retourne la liste des tâches actuelles"""
        return self.tasks