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
        print("🚀 Démarrage de PyTasks...")
        
        # Crée l'application Qt
        app = QApplication(sys.argv)
        app.setApplicationName("PyTasks")
        app.setOrganizationName("PyTasks")
        print("✅ QApplication créée")
        
        # Initialise les composants
        repository = TaskRepository("tasks.json")
        print("✅ Repository créé")
        
        logger = Logger()
        print("✅ Logger créé")
        
        controller = TaskController(repository, logger)
        print("✅ Controller créé")
        
        # Crée la fenêtre principale
        print("🪟 Création de la fenêtre...")
        window = MainWindow(controller)
        print("✅ MainWindow créée")
        
        window.show()
        print("✅ Fenêtre affichée")
        
        # Timer pour rafraîchir l'historique
        def refresh_history():
            window.update_history_display()
        
        timer = QTimer()
        timer.timeout.connect(refresh_history)
        timer.start(2000)
        print("✅ Timer configuré")
        
        print("🎉 Lancement de la boucle d'événements...")
        
        # Lance l'application
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"\n❌ ERREUR FATALE : {e}")
        import traceback
        traceback.print_exc()
        input("\nAppuyez sur Entrée pour quitter...")


if __name__ == "__main__":
    main()