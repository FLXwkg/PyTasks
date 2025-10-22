"""
Système de logging pour l'historique.
"""
from datetime import datetime
from typing import List


class Logger:
    """Logger simple pour enregistrer les actions"""
    
    def __init__(self):
        self.logs: List[str] = []
    
    def log(self, level: str, message: str):
        """
        Enregistre un log.
        
        Args:
            level: 'info', 'warning', 'error', 'success'
            message: Message à logger
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level.upper()}] {message}"
        self.logs.append(log_entry)
        print(log_entry)  # Affiche aussi en console
    
    def get_all_logs(self) -> str:
        """Retourne tous les logs formatés"""
        return "\n".join(self.logs)
    
    def clear(self):
        """Efface tous les logs"""
        self.logs.clear()