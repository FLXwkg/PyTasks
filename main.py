"""
Point d'entrée de l'application PyTasks.
"""
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

from models.task_repository import TaskRepository
from controllers.task_controller import TaskController
from main_window import MainWindow
from utils.logger import Logger


def main():
    """Fonction principale de l'application"""
    
    try:        
        # Crée l'application Qt
        app = QApplication(sys.argv)
        app.setApplicationName("PyTasks")
        app.setOrganizationName("PyTasks")
        
        try:
            with open("styles.qss", "r", encoding="utf-8") as f:
                app.setStyleSheet(f.read())
            print("✅ Styles chargés")
        except FileNotFoundError:
            print("⚠️  Fichier styles.qss non trouvé, thème par défaut utilisé")
  
        # Initialise les composants
        repository = TaskRepository("tasks.json")
        
        logger = Logger()
        
        controller = TaskController(repository, logger)
        
        # Crée la fenêtre principale
        window = MainWindow(controller)
        
        window.show()
        
        # Timer pour rafraîchir l'historique
        def refresh_history():
            window.update_history_display()
        
        timer = QTimer()
        timer.timeout.connect(refresh_history)
        timer.start(2000)

        print("✅ Application créée")
        
        # Lance l'application
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"\n❌ ERREUR FATALE : {e}")
        import traceback
        traceback.print_exc()
        input("\nAppuyez sur Entrée pour quitter...")


if __name__ == "__main__":
    main()