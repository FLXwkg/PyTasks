"""
Vue principale de l'application PyTasks.
Connecte l'interface utilisateur au contrôleur.
"""
from PySide6.QtWidgets import QMainWindow, QListWidgetItem, QInputDialog, QMessageBox
from PySide6.QtCore import Qt, Slot
from datetime import datetime

from views.ui_main import Ui_MainWindow
from controllers.task_controller import TaskController
from models.task import Task, TaskState


class MainWindow(QMainWindow):
    """
    Fenêtre principale de l'application.
    Gère l'affichage et les interactions utilisateur.
    """
    
    def __init__(self, controller: TaskController):
        print("  🔨 MainWindow.__init__() appelé")
        
        try:
            super().__init__()
            print("  ✅ super().__init__() OK")
        except Exception as e:
            print(f"  ❌ Erreur super().__init__(): {e}")
            raise
        
        try:
            # Setup UI
            self.ui = Ui_MainWindow()
            print("  ✅ Ui_MainWindow() créé")
        except Exception as e:
            print(f"  ❌ Erreur création Ui_MainWindow: {e}")
            raise
        
        try:
            self.ui.setupUi(self)
            print("  ✅ setupUi() terminé")
        except Exception as e:
            print(f"  ❌ Erreur setupUi(): {e}")
            import traceback
            traceback.print_exc()
            raise
        
        try:
            # Contrôleur
            self.controller = controller
            print("  ✅ Contrôleur assigné")
            
            # État interne
            self.current_state_filter = None
            print("  ✅ État interne initialisé")
            
            # Connecter les signaux
            print("  🔌 Connection des signaux...")
            self._connect_signals()
            print("  ✅ Signaux connectés")
            
            # Charger les données initiales
            print("  📂 Chargement des données...")
            self.controller.load_tasks()
            print("  ✅ Données chargées")
            
        except Exception as e:
            print(f"  ❌ Erreur dans l'initialisation: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    # ========== CONNEXION DES SIGNAUX ==========
    
    def _connect_signals(self):
        """Connecte tous les signaux de l'UI au contrôleur"""
        
        # === SIDEBAR ===
        # Recherche
        self.ui.searchBar.textChanged.connect(self._on_search_changed)
        
        # Filtre par état
        self.ui.stateFilter.currentTextChanged.connect(self._on_filter_changed)
        
        # Sélection d'une tâche
        self.ui.taskList.itemClicked.connect(self._on_task_selected)
        
        # Boutons CRUD
        self.ui.btnAdd.clicked.connect(self._on_add_task)
        self.ui.btnDelete.clicked.connect(self._on_delete_task)
        
        # === DÉTAILS TÂCHE ===
        # Boutons actions
        self.ui.btnSave.clicked.connect(self._on_save_task)
        self.ui.btnClose.clicked.connect(self._on_close_task)
        
        # Commentaires
        self.ui.btnAddComment.clicked.connect(self._on_add_comment)
        self.ui.commentInput.returnPressed.connect(self._on_add_comment)  # Entrée = ajouter
        
        # === HISTORIQUE ===
        self.ui.btnClearHistory.clicked.connect(self._on_clear_history)
        
        # === SIGNAUX DU CONTRÔLEUR ===
        # Quand la liste change
        self.controller.tasks_updated.connect(self._refresh_task_list)
        
        # Quand une tâche est sélectionnée
        self.controller.task_selected.connect(self._display_task_details)
    
    # ========== RECHERCHE & FILTRE ==========
    
    @Slot()
    def _on_search_changed(self):
        """Déclenché quand le texte de recherche change"""
        query = self.ui.searchBar.text()
        self.controller.search_and_filter(query, self.current_state_filter)
    
    @Slot(str)
    def _on_filter_changed(self, state_text: str):
        """Déclenché quand le filtre d'état change"""
        # Conversion texte -> TaskState
        state_map = {
            "Tous les états": None,
            "À faire": TaskState.TODO,
            "En cours": TaskState.IN_PROGRESS,
            "Réalisé": TaskState.DONE,
            "Abandonné": TaskState.ABANDONED,
            "En attente": TaskState.WAITING
        }
        
        self.current_state_filter = state_map.get(state_text)
        
        # Applique le filtre
        query = self.ui.searchBar.text()
        self.controller.search_and_filter(query, self.current_state_filter)
    
    # ========== AFFICHAGE LISTE ==========
    
    @Slot()
    def _refresh_task_list(self):
        """Rafraîchit la liste des tâches affichées"""
        self.ui.taskList.clear()
        
        tasks = self.controller.get_all_tasks()
        
        for task in tasks:
            # Icône selon l'état
            icon_map = {
                TaskState.TODO: "📋",
                TaskState.IN_PROGRESS: "⚙️",
                TaskState.DONE: "✅",
                TaskState.ABANDONED: "❌",
                TaskState.WAITING: "⏳"
            }
            icon = icon_map.get(task.state, "📋")
            
            # Crée l'item
            item = QListWidgetItem(f"{icon} {task.title}")
            item.setData(Qt.UserRole, task.id)  # Stocke l'ID dans l'item
            
            self.ui.taskList.addItem(item)
        
        # Met à jour la barre de statut
        self.statusBar().showMessage(f"{len(tasks)} tâche(s)")
    
    # ========== SÉLECTION TÂCHE ==========
    
    @Slot(QListWidgetItem)
    def _on_task_selected(self, item: QListWidgetItem):
        """Déclenché quand on clique sur une tâche"""
        task_id = item.data(Qt.UserRole)
        self.controller.select_task(task_id)
        
        # Active le bouton supprimer
        self.ui.btnDelete.setEnabled(True)
    
    @Slot(Task)
    def _display_task_details(self, task: Task):
        """Affiche les détails d'une tâche dans le panneau de droite"""
        # Cache le label "Aucune sélection"
        self.ui.noSelectionLabel.setVisible(False)
        
        # Affiche le groupe de détails
        self.ui.taskDetailsGroup.setVisible(True)
        
        # Remplit les champs
        self.ui.titleEdit.setText(task.title)
        self.ui.descriptionEdit.setPlainText(task.description)
        
        # État
        state_index_map = {
            TaskState.TODO: 0,
            TaskState.IN_PROGRESS: 1,
            TaskState.DONE: 2,
            TaskState.ABANDONED: 3,
            TaskState.WAITING: 4
        }
        self.ui.stateEdit.setCurrentIndex(state_index_map.get(task.state, 0))
        
        # Dates
        if task.start_date:
            self.ui.startDateEdit.setDateTime(task.start_date)
        else:
            self.ui.startDateEdit.clear()
        
        if task.end_date:
            self.ui.endDateEdit.setDateTime(task.end_date)
        else:
            self.ui.endDateEdit.clear()
        
        # Commentaires
        self._refresh_comments(task)
    
    def _refresh_comments(self, task: Task):
        """Rafraîchit la liste des commentaires"""
        self.ui.commentsList.clear()
        
        for comment in task.comments:
            timestamp = comment.created_at.strftime("%d/%m/%Y %H:%M")
            item_text = f"💬 [{timestamp}] {comment.content}"
            self.ui.commentsList.addItem(item_text)
    
    # ========== CRÉATION TÂCHE ==========
    
    @Slot()
    def _on_add_task(self):
        """Déclenché par le bouton Ajouter"""
        # Boîte de dialogue pour le titre
        title, ok = QInputDialog.getText(
            self,
            "Nouvelle tâche",
            "Titre de la tâche :"
        )
        
        if ok and title:
            # Boîte de dialogue pour la description (optionnel)
            description, ok = QInputDialog.getMultiLineText(
                self,
                "Nouvelle tâche",
                "Description (optionnel) :"
            )
            
            if ok:
                success = self.controller.create_task(title, description)
                
                if success:
                    self.statusBar().showMessage("✅ Tâche créée !", 3000)
    
    # ========== MODIFICATION TÂCHE ==========
    
    @Slot()
    def _on_save_task(self):
        """Sauvegarde les modifications de la tâche actuelle"""
        if not self.controller.current_task:
            return
        
        # Récupère les valeurs des champs
        title = self.ui.titleEdit.text()
        description = self.ui.descriptionEdit.toPlainText()
        
        # État
        state_map = [
            TaskState.TODO,
            TaskState.IN_PROGRESS,
            TaskState.DONE,
            TaskState.ABANDONED,
            TaskState.WAITING
        ]
        state = state_map[self.ui.stateEdit.currentIndex()]
        
        # Dates (peut être None)
        start_date = self.ui.startDateEdit.dateTime().toPython() if self.ui.startDateEdit.dateTime().isValid() else None
        end_date = self.ui.endDateEdit.dateTime().toPython() if self.ui.endDateEdit.dateTime().isValid() else None
        
        # Appelle le contrôleur
        success = self.controller.update_current_task(
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
            state=state
        )
        
        if success:
            self.statusBar().showMessage("💾 Tâche enregistrée !", 3000)
    
    # ========== SUPPRESSION TÂCHE ==========
    
    @Slot()
    def _on_delete_task(self):
        """Supprime la tâche sélectionnée"""
        current_item = self.ui.taskList.currentItem()
        if not current_item:
            return
        
        task_id = current_item.data(Qt.UserRole)
        
        if self.controller.delete_task(task_id):
            # Cache les détails
            self._hide_task_details()
            
            # Désactive le bouton supprimer
            self.ui.btnDelete.setEnabled(False)
            
            self.statusBar().showMessage("🗑️ Tâche supprimée", 3000)
    
    # ========== CLÔTURE TÂCHE ==========
    
    @Slot()
    def _on_close_task(self):
        """Clôture la tâche actuelle"""
        if not self.controller.current_task:
            return
        
        # Demande confirmation
        reply = QMessageBox.question(
            self,
            "Clôturer la tâche",
            f"Clôturer la tâche '{self.controller.current_task.title}' ?\n\n"
            "Elle sera marquée comme 'Réalisé' avec la date de fin actuelle.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success = self.controller.close_current_task()
            
            if success:
                # Rafraîchit l'affichage
                self.controller.select_task(self.controller.current_task.id)
                self.statusBar().showMessage("✅ Tâche clôturée !", 3000)
    
    # ========== COMMENTAIRES ==========
    
    @Slot()
    def _on_add_comment(self):
        """Ajoute un commentaire à la tâche actuelle"""
        if not self.controller.current_task:
            return
        
        content = self.ui.commentInput.text().strip()
        
        if not content:
            return
        
        success = self.controller.add_comment_to_current_task(content)
        
        if success:
            # Vide le champ
            self.ui.commentInput.clear()
            
            # Rafraîchit les commentaires
            self._refresh_comments(self.controller.current_task)
            
            self.statusBar().showMessage("💬 Commentaire ajouté", 2000)
    
    # ========== HISTORIQUE ==========
    
    @Slot()
    def _on_clear_history(self):
        """Efface l'historique des logs"""
        reply = QMessageBox.question(
            self,
            "Effacer l'historique",
            "Voulez-vous effacer tout l'historique ?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.controller.logger.clear()
            self.ui.historyLog.clear()
            self.statusBar().showMessage("🗑️ Historique effacé", 2000)
    
    def update_history_display(self):
        """Met à jour l'affichage de l'historique"""
        logs = self.controller.logger.get_all_logs()
        self.ui.historyLog.setPlainText(logs)
    
    # ========== UTILITAIRES ==========
    
    def _hide_task_details(self):
        """Cache le panneau de détails"""
        self.ui.taskDetailsGroup.setVisible(False)
        self.ui.noSelectionLabel.setVisible(True)