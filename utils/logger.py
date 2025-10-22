"""
Système de logging pour l'historique avec persistance.
"""
from datetime import datetime
from typing import List
import os


class Logger:
    """Logger avec sauvegarde automatique dans un fichier"""
    
    def __init__(self, log_file: str = "history.log"):
        self.log_file = log_file
        self.logs: List[str] = []
        self._load_logs()
    
    def _load_logs(self):
        """Charge les logs depuis le fichier"""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    self.logs = [line.strip() for line in f.readlines()]
            except Exception as e:
                print(f"Erreur chargement logs : {e}")
                self.logs = []
        else:
            self.logs = []
    
    def _save_logs(self):
        """Sauvegarde les logs dans le fichier"""
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(self.logs) + '\n')
        except Exception as e:
            print(f"Erreur sauvegarde logs : {e}")
    
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
        
        # Sauvegarde automatique
        self._save_logs()
    
    def get_all_logs(self) -> str:
        """Retourne tous les logs formatés"""
        return "\n".join(self.logs)
    
    def clear(self):
        """Efface tous les logs"""
        self.logs.clear()
        self._save_logs()