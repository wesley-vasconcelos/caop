from flask import Blueprint, request, jsonify
from datetime import datetime
from src.models import db
from src.models.prova import Prova
from src.models.instrutor import Instrutor

prova_bp = Blueprint('prova', __name__)

@prova_bp.route('/provas', methods=['GET'])
def get_provas():
    """Listar todas as provas"""
    try:
        provas = Prova.query.all()
        result = []
        for prova in provas:
            prova_dict = prova.to_dict()
            # Adicionar informações do instrutor
            instrutor = Instrutor.query.get(prova.instrutor_id)
            if instrutor:
                prova_dict['instrutor'] = instrutor.to_dict()
            result.append(prova_dict)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@prova_bp.route('/provas', methods=['POST'])
def create_prova():
    """Criar uma nova prova"""
    try:
        data = request.get_json()
        
        if not data or 'nome' not in data or 'data_aplicacao' not in data or 'instrutor_id' not in data:
            return jsonify({'error': 'Nome, data de aplicação e instrutor são obrigatórios'}), 400
        
        # Verificar se o instrutor existe
        instrutor = Instrutor.query.get(data['instrutor_id'])
        if not instrutor:
            return jsonify({'error': 'Instrutor não encontrado'}), 404
        
        # Converter string de data para objeto date
        try:
            data_aplicacao = datetime.strptime(data['data_aplicacao'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Formato de data inválido. Use YYYY-MM-DD'}), 400
        
        prova = Prova(
            nome=data['nome'],
            data_aplicacao=data_aplicacao,
            instrutor_id=data['instrutor_id']
        )
        
        db.session.add(prova)
        db.session.commit()
        
        # Retornar a prova com informações do instrutor
        result = prova.to_dict()
        result['instrutor'] = instrutor.to_dict()
        
        return jsonify(result), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@prova_bp.route('/provas/<int:prova_id>', methods=['GET'])
def get_prova(prova_id):
    """Obter uma prova específica"""
    try:
        prova = Prova.query.get_or_404(prova_id)
        result = prova.to_dict()
        
        # Adicionar informações do instrutor
        instrutor = Instrutor.query.get(prova.instrutor_id)
        if instrutor:
            result['instrutor'] = instrutor.to_dict()
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@prova_bp.route('/provas/instrutor/<int:instrutor_id>', methods=['GET'])
def get_provas_by_instrutor(instrutor_id):
    """Obter todas as provas de um instrutor específico"""
    try:
        # Verificar se o instrutor existe
        instrutor = Instrutor.query.get_or_404(instrutor_id)
        
        provas = Prova.query.filter_by(instrutor_id=instrutor_id).all()
        result = []
        for prova in provas:
            prova_dict = prova.to_dict()
            prova_dict['instrutor'] = instrutor.to_dict()
            result.append(prova_dict)
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@prova_bp.route('/provas/<int:prova_id>', methods=['PUT'])
def update_prova(prova_id):
    """Atualizar uma prova"""
    try:
        prova = Prova.query.get_or_404(prova_id)
        data = request.get_json()
        
        if 'nome' in data:
            prova.nome = data['nome']
        
        if 'data_aplicacao' in data:
            try:
                prova.data_aplicacao = datetime.strptime(data['data_aplicacao'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Formato de data inválido. Use YYYY-MM-DD'}), 400
        
        if 'instrutor_id' in data:
            # Verificar se o instrutor existe
            instrutor = Instrutor.query.get(data['instrutor_id'])
            if not instrutor:
                return jsonify({'error': 'Instrutor não encontrado'}), 404
            prova.instrutor_id = data['instrutor_id']
        
        db.session.commit()
        
        # Retornar a prova atualizada com informações do instrutor
        result = prova.to_dict()
        instrutor = Instrutor.query.get(prova.instrutor_id)
        if instrutor:
            result['instrutor'] = instrutor.to_dict()
        
        return jsonify(result), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@prova_bp.route('/provas/<int:prova_id>', methods=['DELETE'])
def delete_prova(prova_id):
    """Deletar uma prova"""
    try:
        prova = Prova.query.get_or_404(prova_id)
        db.session.delete(prova)
        db.session.commit()
        return jsonify({'message': 'Prova deletada com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

