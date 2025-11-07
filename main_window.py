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
        self.ui.searchBar.textChanged.connect(self._on_search_changed)
        self.ui.stateFilter.currentTextChanged.connect(self._on_filter_changed)
        self.ui.taskList.itemClicked.connect(self._on_task_selected)
        self.ui.btnAdd.clicked.connect(self._on_add_task)
        self.ui.btnDelete.clicked.connect(self._on_delete_task)
        
        # === DÉTAILS TÂCHE ===
        self.ui.btnSave.clicked.connect(self._on_save_task)
        self.ui.btnClose.clicked.connect(self._on_close_task)
        self.ui.btnStartWork.clicked.connect(self._on_start_work)
        self.ui.btnStartTask.clicked.connect(self._on_start_task)
        self.ui.btnAbandon.clicked.connect(self._on_abandon_task)
        self.ui.btnAddComment.clicked.connect(self._on_add_comment)
        self.ui.commentInput.returnPressed.connect(self._on_add_comment)
        
        # Supprimer commentaire
        self.ui.btnDeleteComment.clicked.connect(self._on_delete_comment)
        self.ui.commentsList.itemSelectionChanged.connect(self._on_comment_selection_changed)
        
        # === HISTORIQUE ===
        self.ui.btnClearHistory.clicked.connect(self._on_clear_history)
        
        # === SIGNAUX DU CONTRÔLEUR ===
        self.controller.tasks_updated.connect(self._refresh_task_list)
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
    
    # ========== TÂCHES ==========
    
    @Slot(QListWidgetItem)
    def _on_task_selected(self, item: QListWidgetItem):
        """Déclenché quand on clique sur une tâche"""
        task_id = item.data(Qt.UserRole)
        self.controller.select_task(task_id)
        
        # Active le bouton supprimer
        self.ui.btnDelete.setEnabled(True)
    
    @Slot(Task)
    def _display_task_details(self, task: Task):
        """Affiche les détails d'une tâche"""
        self.ui.noSelectionLabel.setVisible(False)
        self.ui.taskDetailsGroup.setVisible(True)
        
        # Remplit les champs
        self.ui.titleEdit.setText(task.title)
        self.ui.descriptionEdit.setPlainText(task.description)
        
        # Affiche l'état (lecture seule)
        state_labels = {
            TaskState.TODO: "À faire",
            TaskState.IN_PROGRESS: "En cours",
            TaskState.DONE: "Réalisé",
            TaskState.ABANDONED: "Abandonné",
            TaskState.WAITING: "En attente"
        }
        self.ui.stateDisplay.setText(state_labels.get(task.state, "Inconnu"))
        
        # Gère l'affichage de la dépendance
        is_waiting = task.state == TaskState.WAITING
        self.ui.waitingForContainer.setVisible(is_waiting)
        
        if is_waiting:
            # Remplit la liste des tâches disponibles (lecture seule)
            self.ui.waitingForSelect.clear()
            self.ui.waitingForSelect.addItem("(Aucune)", None)
            
            all_tasks = self.controller.get_all_tasks()
            for t in all_tasks:
                if t.id != task.id and t.state != TaskState.DONE:
                    self.ui.waitingForSelect.addItem(t.title, t.id)
            
            # Sélectionne la tâche actuelle en attente
            if task.waiting_for:
                for i in range(self.ui.waitingForSelect.count()):
                    if self.ui.waitingForSelect.itemData(i) == task.waiting_for:
                        self.ui.waitingForSelect.setCurrentIndex(i)
                        break
            
            # ✨ Désactive le sélecteur (lecture seule, défini à la création)
            self.ui.waitingForSelect.setEnabled(False)
        
        # Dates
        if task.start_date:
            self.ui.startDateEdit.setDateTime(task.start_date)
        else:
            self.ui.startDateEdit.clear()
        
        if task.end_date:
            self.ui.endDateEdit.setDateTime(task.end_date)
        else:
            self.ui.endDateEdit.clear()
        
        # Gestion des boutons selon l'état
        is_done = task.state == TaskState.DONE
        is_abandoned = task.state == TaskState.ABANDONED
        is_waiting = task.state == TaskState.WAITING
        is_todo = task.state == TaskState.TODO
        is_in_progress = task.state == TaskState.IN_PROGRESS
        
        # Verrouillage des champs
        is_locked = is_done or is_abandoned
        self.ui.titleEdit.setReadOnly(is_locked)
        self.ui.descriptionEdit.setReadOnly(is_locked)
        self.ui.startDateEdit.setReadOnly(is_locked)
        self.ui.endDateEdit.setReadOnly(is_locked)
        
        # Boutons
        self.ui.btnSave.setEnabled(not is_locked)
        self.ui.btnClose.setEnabled(is_in_progress)  
        
        # Bouton "Démarrer" : visible si en attente, grisé si pas de dépendance satisfaite
        self.ui.btnStartWork.setVisible(is_todo)
        self.ui.btnStartTask.setVisible(is_waiting)
        if is_waiting:
            # Vérifie si la tâche dont on dépend est terminée
            can_start = True
            if task.waiting_for:
                waiting_task = self.controller.repository.find_by_id(task.waiting_for)
                if waiting_task and waiting_task.state != TaskState.DONE:
                    can_start = False
            
            self.ui.btnStartTask.setEnabled(can_start)
            
            # Tooltip explicatif
            if not can_start:
                self.ui.btnStartTask.setToolTip("La tâche dont vous dépendez n'est pas encore terminée")
            else:
                self.ui.btnStartTask.setToolTip("Démarrer cette tâche")
        
        # Bouton "Abandonner" : visible si pas déjà terminé/abandonné
        self.ui.btnAbandon.setVisible(not is_locked)

        # Style
        if is_locked:
            locked_style = "background-color: #f0f0f0; color: #666;"
            self.ui.titleEdit.setStyleSheet(locked_style)
            self.ui.descriptionEdit.setStyleSheet(locked_style)
            self.ui.startDateEdit.setStyleSheet(locked_style)
            self.ui.endDateEdit.setStyleSheet(locked_style)
        else:
            self.ui.titleEdit.setStyleSheet("")
            self.ui.descriptionEdit.setStyleSheet("")
            self.ui.startDateEdit.setStyleSheet("")
            self.ui.endDateEdit.setStyleSheet("")
        
        self._refresh_comments(task)
  
    @Slot()
    def _on_add_task(self):
        """Déclenché par le bouton Ajouter - Affiche une modale complète"""
        from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                                        QLineEdit, QTextEdit, QDateTimeEdit, QComboBox, 
                                        QPushButton, QFormLayout, QGroupBox)
        from PySide6.QtCore import QDateTime
        from datetime import datetime, timedelta
        
        # Créer la modale
        dialog = QDialog(self)
        dialog.setWindowTitle("Nouvelle tâche")
        dialog.setMinimumWidth(550)
        
        # Layout principal
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        
        # Champ Titre
        title_input = QLineEdit()
        title_input.setPlaceholderText("Entrez le titre de la tâche...")
        form_layout.addRow("Titre *:", title_input)
        
        # Champ Description
        description_input = QTextEdit()
        description_input.setPlaceholderText("Description détaillée (optionnel)...")
        description_input.setMaximumHeight(100)
        form_layout.addRow("Description :", description_input)
        
        # Date de début (date actuelle par défaut)
        start_date_input = QDateTimeEdit()
        start_date_input.setCalendarPopup(True)
        start_date_input.setDateTime(QDateTime.currentDateTime())
        form_layout.addRow("Date de début :", start_date_input)
        
        # Date de fin (date actuelle + 1 jour par défaut)
        end_date_input = QDateTimeEdit()
        end_date_input.setCalendarPopup(True)
        tomorrow = datetime.now() + timedelta(days=1)
        end_date_input.setDateTime(QDateTime(tomorrow))
        form_layout.addRow("Date de fin :", end_date_input)
        
        # État initial
        state_input = QComboBox()
        state_input.addItem("À faire", TaskState.TODO)
        state_input.addItem("En attente", TaskState.WAITING)
        state_input.setCurrentIndex(0)  # TODO par défaut
        form_layout.addRow("État initial :", state_input)
        
        layout.addLayout(form_layout)
        
        # Groupe "En attente de" (visible seulement si état = En attente)
        waiting_group = QGroupBox("Dépendance")
        waiting_layout = QVBoxLayout()
        
        # Recherche de tâche
        waiting_search = QLineEdit()
        waiting_search.setPlaceholderText("Rechercher une tâche...")
        waiting_layout.addWidget(waiting_search)
        
        # Liste des tâches
        waiting_select = QComboBox()
        waiting_select.addItem("(Sélectionnez une tâche)", None)
        waiting_layout.addWidget(waiting_select)
        
        waiting_group.setLayout(waiting_layout)
        waiting_group.setVisible(False)  # Caché par défaut
        layout.addWidget(waiting_group)
        
        # Fonction pour remplir la liste des tâches
        def populate_waiting_tasks(search_text=""):
            waiting_select.clear()
            waiting_select.addItem("(Sélectionnez une tâche)", None)
            
            all_tasks = self.controller.get_all_tasks()
            search_lower = search_text.lower()
            
            for task in all_tasks:
                # Filtre : pas de tâches Abandonnées ou Clôturées
                if task.state in [TaskState.ABANDONED, TaskState.DONE]:
                    continue
                
                # Recherche par nom
                if search_text and search_lower not in task.title.lower():
                    continue
                
                waiting_select.addItem(task.title, task.id)
        
        # Connection pour la recherche
        waiting_search.textChanged.connect(populate_waiting_tasks)
        
        # Boutons
        button_layout = QHBoxLayout()
        
        btn_cancel = QPushButton("Annuler")
        btn_cancel.clicked.connect(dialog.reject)
        
        btn_create = QPushButton("Créer")
        btn_create.setDefault(True)
        btn_create.clicked.connect(dialog.accept)
        
        button_layout.addStretch()
        button_layout.addWidget(btn_cancel)
        button_layout.addWidget(btn_create)
        
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        
        # ✨ FONCTION DE VALIDATION EN TEMPS RÉEL
        def validate_form():
            """Valide le formulaire et active/désactive le bouton Créer"""
            # Vérifie le titre
            has_title = bool(title_input.text().strip())
            
            # Vérifie les dates
            start_date = start_date_input.dateTime().toPython()
            end_date = end_date_input.dateTime().toPython()
            dates_valid = end_date >= start_date
            
            # Vérifie la dépendance si en attente
            selected_state = state_input.currentData()
            if selected_state == TaskState.WAITING:
                has_dependency = waiting_select.currentData() is not None
            else:
                has_dependency = True  # Pas nécessaire si pas en attente
            
            # Active le bouton seulement si tout est valide
            is_valid = has_title and dates_valid and has_dependency
            btn_create.setEnabled(is_valid)
            
            # Feedback visuel sur les champs invalides
            if not has_title:
                title_input.setStyleSheet("border: 1px solid #ff6b6b;")
            else:
                title_input.setStyleSheet("")
            
            if not dates_valid:
                end_date_input.setStyleSheet("border: 1px solid #ff6b6b;")
            else:
                end_date_input.setStyleSheet("")
            
            if selected_state == TaskState.WAITING and not has_dependency:
                waiting_select.setStyleSheet("border: 1px solid #ff6b6b;")
            else:
                waiting_select.setStyleSheet("")
        
        # Affiche/cache le groupe selon l'état sélectionné
        def on_state_changed(index):
            selected_state = state_input.itemData(index)
            is_waiting = selected_state == TaskState.WAITING
            waiting_group.setVisible(is_waiting)
            
            if is_waiting:
                populate_waiting_tasks()
            
            validate_form()  # ✨ Revalide après changement d'état
        
        state_input.currentIndexChanged.connect(on_state_changed)
        
        # ✨ Connecte tous les champs à la validation
        title_input.textChanged.connect(validate_form)
        start_date_input.dateTimeChanged.connect(validate_form)
        end_date_input.dateTimeChanged.connect(validate_form)
        waiting_select.currentIndexChanged.connect(validate_form)
        
        # ✨ Validation initiale (désactive le bouton si titre vide)
        validate_form()
        
        # Afficher la modale
        if dialog.exec() == QDialog.Accepted:
            title = title_input.text().strip()
            description = description_input.toPlainText().strip()
            start_date = start_date_input.dateTime().toPython()
            end_date = end_date_input.dateTime().toPython()
            state = state_input.currentData()
            
            # Récupère la dépendance si en attente
            waiting_for = None
            if state == TaskState.WAITING:
                waiting_for = waiting_select.currentData()
            
            # Créer la tâche (plus besoin de validation, le bouton était désactivé si invalide)
            try:
                task = Task(
                    title=title,
                    description=description,
                    start_date=start_date,
                    end_date=end_date,
                    state=state,
                    waiting_for=waiting_for
                )
                
                self.controller.repository.save(task)
                
                # Log adapté
                if waiting_for:
                    waiting_task = self.controller.repository.find_by_id(waiting_for)
                    waiting_title = waiting_task.title if waiting_task else "tâche inconnue"
                    self.controller.logger.log(
                        "info",
                        f"Tâche créée : '{task.title}' (en attente de '{waiting_title}')"
                    )
                else:
                    self.controller.logger.log("info", f"Tâche créée : '{task.title}'")
                
                self.controller.load_tasks()
                
                # Sélectionner automatiquement la tâche créée
                self.controller.select_task(task.id)
                
                # Trouver l'item dans la liste et le sélectionner visuellement
                for i in range(self.ui.taskList.count()):
                    item = self.ui.taskList.item(i)
                    if item.data(Qt.UserRole) == task.id:
                        self.ui.taskList.setCurrentItem(item)
                        break
                
                self.statusBar().showMessage("Tâche créée !", 3000)
                
            except ValueError as e:
                QMessageBox.critical(self, "Erreur de validation", str(e))
          
    @Slot()
    def _on_save_task(self):
        """Sauvegarde les modifications de la tâche actuelle"""
        if not self.controller.current_task:
            return
        
        # Récupère les valeurs des champs
        title = self.ui.titleEdit.text()
        description = self.ui.descriptionEdit.toPlainText()
        
        # Dates (peut être None)
        start_date = self.ui.startDateEdit.dateTime().toPython() if self.ui.startDateEdit.dateTime().isValid() else None
        end_date = self.ui.endDateEdit.dateTime().toPython() if self.ui.endDateEdit.dateTime().isValid() else None
        
        # Appelle le contrôleur
        success = self.controller.update_current_task(
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
        )
        
        if success:
            self.statusBar().showMessage("💾 Tâche enregistrée !", 3000)
        
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
        
    @Slot()
    def _on_close_task(self):
        """Clôture la tâche actuelle"""
        if not self.controller.current_task:
            return
        
        task = self.controller.current_task
        
        # Message détaillé
        message = (
            f"Clôturer la tâche '{task.title}' ?\n\n"
            "Actions effectuées :\n"
            "• État changé en 'Réalisé'\n"
            "• Date de fin mise à la date actuelle\n"
            "• Modification des champs verrouillée\n\n"
            "Les commentaires resteront accessibles."
        )
        
        reply = QMessageBox.question(
            self,
            "Clôturer la tâche",
            message,
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success = self.controller.close_current_task()
            if success:
                # Rafraîchit l'affichage (verrouillera les champs)
                self.controller.select_task(self.controller.current_task.id)
                self.statusBar().showMessage("Tâche clôturée et verrouillée !", 3000)
    
    @Slot()
    def _on_set_waiting(self):
        """Met la tâche en attente"""
        if not self.controller.current_task:
            return
        
        # Change l'état
        success = self.controller.update_current_task(state=TaskState.WAITING)
        
        if success:
            # Rafraîchit pour afficher le sélecteur
            self.controller.select_task(self.controller.current_task.id)
            self.statusBar().showMessage("Tâche mise en attente", 2000)

    @Slot()
    def _on_start_task(self):
        """Démarre une tâche en attente"""
        if not self.controller.current_task:
            return
        
        reply = QMessageBox.question(
            self,
            "Démarrer la tâche",
            f"Démarrer la tâche '{self.controller.current_task.title}' ?\n\n"
            "• État changé en 'À faire'\n"
            "• Dépendance retirée",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success = self.controller.start_waiting_task()
            
            if success:
                self.controller.select_task(self.controller.current_task.id)
                self.statusBar().showMessage("Tâche démarrée !", 2000)

    @Slot(int)
    def _on_waiting_for_changed(self, index):
        """Changement de la tâche en attente"""
        if not self.controller.current_task:
            return
        
        if self.controller.current_task.state != TaskState.WAITING:
            return
        
        waiting_for_id = self.ui.waitingForSelect.currentData()
        self.controller.set_waiting_for(self.controller.current_task.id, waiting_for_id)
    
    @Slot()
    def _on_start_work(self):
        """Commence le travail (passe à EN COURS)"""
        if not self.controller.current_task:
            return
        
        reply = QMessageBox.question(
            self,
            "Commencer la tâche",
            f"Commencer le travail sur '{self.controller.current_task.title}' ?\n\n"
            "• État changé en 'En cours'",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success = self.controller.start_work_on_task()
            
            if success:
                self.controller.select_task(self.controller.current_task.id)
                self.statusBar().showMessage("Travail commencé !", 2000)

    @Slot()
    def _on_abandon_task(self):
        """Abandonne la tâche"""
        if not self.controller.current_task:
            return
        
        reply = QMessageBox.question(
            self,
            "Abandonner la tâche",
            f"Abandonner la tâche '{self.controller.current_task.title}' ?\n\n"
            "Actions effectuées :\n"
            "• État changé en 'Abandonné'\n"
            "• Date de fin mise à la date actuelle\n"
            "• Modification des champs verrouillée\n\n"
            "Les commentaires resteront accessibles.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success = self.controller.abandon_task()
            
            if success:
                self.controller.select_task(self.controller.current_task.id)
                self.statusBar().showMessage("Tâche abandonnée", 2000)
    
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

    @Slot()
    def _on_comment_selection_changed(self):
        """Active/désactive le bouton supprimer selon la sélection"""
        selected_count = len(self.ui.commentsList.selectedItems())
        self.ui.btnDeleteComment.setEnabled(selected_count > 0)
        
        # Change le texte du bouton selon le nombre sélectionné
        if selected_count > 1:
            self.ui.btnDeleteComment.setText(f"Supprimer ({selected_count})")
        else:
            self.ui.btnDeleteComment.setText("Supprimer")

    @Slot()
    def _on_delete_comment(self):
        """Supprime les commentaires sélectionnés"""
        if not self.controller.current_task:
            return
        
        selected_items = self.ui.commentsList.selectedItems()
        if not selected_items:
            return
        
        # Récupère les objets Comment correspondants
        comments_to_delete = []
        for item in selected_items:
            comment_index = self.ui.commentsList.row(item)
            
            if 0 <= comment_index < len(self.controller.current_task.comments):
                comment = self.controller.current_task.comments[comment_index]
                comments_to_delete.append(comment)
        
        if not comments_to_delete:
            return
        
        # Message de confirmation adapté
        count = len(comments_to_delete)
        if count == 1:
            message = f"Supprimer ce commentaire ?\n\n{comments_to_delete[0].content}"
        else:
            message = f"Supprimer {count} commentaires sélectionnés ?"
        
        reply = QMessageBox.question(
            self,
            "Supprimer commentaire(s)",
            message,
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success = self.controller.delete_comments_from_current_task(comments_to_delete)
            
            if success:
                self._refresh_comments(self.controller.current_task)
                
                if count == 1:
                    self.statusBar().showMessage("Commentaire supprimé", 2000)
                else:
                    self.statusBar().showMessage(f"{count} commentaires supprimés", 2000)

    def _refresh_comments(self, task: Task):
      """Rafraîchit la liste des commentaires"""
      self.ui.commentsList.clear()
      
      for comment in task.comments:
          timestamp = comment.created_at.strftime("%d/%m/%Y %H:%M")
          item_text = f"[{timestamp}] {comment.content}"
          item = QListWidgetItem(item_text)
          self.ui.commentsList.addItem(item)

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