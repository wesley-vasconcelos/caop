from flask import Blueprint, request, jsonify
from src.models import db
from src.models.instrutor import Instrutor

instrutor_bp = Blueprint('instrutor', __name__)

@instrutor_bp.route('/instrutores', methods=['GET'])
def get_instrutores():
    """Listar todos os instrutores"""
    try:
        instrutores = Instrutor.query.all()
        return jsonify([instrutor.to_dict() for instrutor in instrutores]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@instrutor_bp.route('/instrutores', methods=['POST'])
def create_instrutor():
    """Criar um novo instrutor"""
    try:
        data = request.get_json()
        
        if not data or 'qra' not in data or 'nome' not in data:
            return jsonify({'error': 'QRA e nome são obrigatórios'}), 400
        
        # Verificar se o QRA já existe
        existing_instrutor = Instrutor.query.filter_by(qra=data['qra']).first()
        if existing_instrutor:
            return jsonify({'error': 'QRA já cadastrado'}), 400
        
        instrutor = Instrutor(
            qra=data['qra'],
            nome=data['nome']
        )
        
        db.session.add(instrutor)
        db.session.commit()
        
        return jsonify(instrutor.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@instrutor_bp.route('/instrutores/<int:instrutor_id>', methods=['GET'])
def get_instrutor(instrutor_id):
    """Obter um instrutor específico"""
    try:
        instrutor = Instrutor.query.get_or_404(instrutor_id)
        return jsonify(instrutor.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@instrutor_bp.route('/instrutores/<int:instrutor_id>', methods=['PUT'])
def update_instrutor(instrutor_id):
    """Atualizar um instrutor"""
    try:
        instrutor = Instrutor.query.get_or_404(instrutor_id)
        data = request.get_json()
        
        if 'qra' in data:
            # Verificar se o novo QRA já existe (exceto para o próprio instrutor)
            existing_instrutor = Instrutor.query.filter_by(qra=data['qra']).first()
            if existing_instrutor and existing_instrutor.id != instrutor_id:
                return jsonify({'error': 'QRA já cadastrado'}), 400
            instrutor.qra = data['qra']
        
        if 'nome' in data:
            instrutor.nome = data['nome']
        
        db.session.commit()
        return jsonify(instrutor.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@instrutor_bp.route('/instrutores/<int:instrutor_id>', methods=['DELETE'])
def delete_instrutor(instrutor_id):
    """Deletar um instrutor"""
    try:
        instrutor = Instrutor.query.get_or_404(instrutor_id)
        db.session.delete(instrutor)
        db.session.commit()
        return jsonify({'message': 'Instrutor deletado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

