from datetime import datetime
from . import db

class Instrutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qra = db.Column(db.String(20), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com provas
    provas = db.relationship('Prova', backref='instrutor', lazy=True)

    def __repr__(self):
        return f'<Instrutor {self.qra} - {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'qra': self.qra,
            'nome': self.nome,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

