from datetime import datetime
from . import db

class Prova(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    data_aplicacao = db.Column(db.Date, nullable=False)
    instrutor_id = db.Column(db.Integer, db.ForeignKey('instrutor.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com pontuações
    pontuacoes = db.relationship('Pontuacao', backref='prova', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Prova {self.nome} - {self.data_aplicacao}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'data_aplicacao': self.data_aplicacao.isoformat() if self.data_aplicacao else None,
            'instrutor_id': self.instrutor_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

