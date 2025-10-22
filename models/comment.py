from datetime import datetime
from typing import Optional
import uuid

class Comment:
    def __init__(self, content: str, comment_id: Optional[str] = None):
        if not content or not content.strip():
            raise ValueError("Commentaire vide interdit")
        
        self.id = comment_id if comment_id else str(uuid.uuid4())
        self.content = content.strip()
        self.created_at = datetime.now()
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "content": self.content,
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Comment':
        comment = cls(data["content"], data["id"])
        comment.created_at = datetime.fromisoformat(data["created_at"])
        return comment