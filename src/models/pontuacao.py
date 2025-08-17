from datetime import datetime
from . import db

class Pontuacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qra_aluno = db.Column(db.String(20), nullable=False)
    pontuacao = db.Column(db.Float, nullable=False)
    prova_id = db.Column(db.Integer, db.ForeignKey('prova.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Pontuacao {self.qra_aluno} - {self.pontuacao}>'

    def to_dict(self):
        return {
            'id': self.id,
            'qra_aluno': self.qra_aluno,
            'pontuacao': self.pontuacao,
            'prova_id': self.prova_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

