from flask import Blueprint, request, jsonify
from sqlalchemy import func
from src.models import db
from src.models.pontuacao import Pontuacao
from src.models.prova import Prova
from src.models.instrutor import Instrutor

pontuacao_bp = Blueprint('pontuacao', __name__)

@pontuacao_bp.route('/pontuacoes', methods=['GET'])
def get_pontuacoes():
    """Listar todas as pontuações"""
    try:
        pontuacoes = Pontuacao.query.all()
        result = []
        for pontuacao in pontuacoes:
            pontuacao_dict = pontuacao.to_dict()
            # Adicionar informações da prova
            prova = Prova.query.get(pontuacao.prova_id)
            if prova:
                pontuacao_dict['prova'] = prova.to_dict()
            result.append(pontuacao_dict)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pontuacao_bp.route('/pontuacoes', methods=['POST'])
def create_pontuacao():
    """Criar uma nova pontuação"""
    try:
        data = request.get_json()
        
        if not data or 'qra_aluno' not in data or 'pontuacao' not in data or 'prova_id' not in data:
            return jsonify({'error': 'QRA do aluno, pontuação e prova são obrigatórios'}), 400
        
        # Verificar se a prova existe
        prova = Prova.query.get(data['prova_id'])
        if not prova:
            return jsonify({'error': 'Prova não encontrada'}), 404
        
        # Verificar se já existe pontuação para este aluno nesta prova
        existing_pontuacao = Pontuacao.query.filter_by(
            qra_aluno=data['qra_aluno'],
            prova_id=data['prova_id']
        ).first()
        
        if existing_pontuacao:
            return jsonify({'error': 'Já existe pontuação para este aluno nesta prova'}), 400
        
        pontuacao = Pontuacao(
            qra_aluno=data['qra_aluno'],
            pontuacao=float(data['pontuacao']),
            prova_id=data['prova_id']
        )
        
        db.session.add(pontuacao)
        db.session.commit()
        
        # Retornar a pontuação com informações da prova
        result = pontuacao.to_dict()
        result['prova'] = prova.to_dict()
        
        return jsonify(result), 201
    except ValueError:
        return jsonify({'error': 'Pontuação deve ser um número válido'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@pontuacao_bp.route('/pontuacoes/lote', methods=['POST'])
def create_pontuacoes_lote():
    """Criar múltiplas pontuações de uma vez"""
    try:
        data = request.get_json()
        
        if not data or 'pontuacoes' not in data:
            return jsonify({'error': 'Lista de pontuações é obrigatória'}), 400
        
        pontuacoes_criadas = []
        
        for item in data['pontuacoes']:
            if 'qra_aluno' not in item or 'pontuacao' not in item or 'prova_id' not in item:
                return jsonify({'error': 'Cada pontuação deve ter QRA do aluno, pontuação e prova'}), 400
            
            # Verificar se a prova existe
            prova = Prova.query.get(item['prova_id'])
            if not prova:
                return jsonify({'error': f'Prova {item["prova_id"]} não encontrada'}), 404
            
            # Verificar se já existe pontuação para este aluno nesta prova
            existing_pontuacao = Pontuacao.query.filter_by(
                qra_aluno=item['qra_aluno'],
                prova_id=item['prova_id']
            ).first()
            
            if existing_pontuacao:
                # Atualizar pontuação existente
                existing_pontuacao.pontuacao = float(item['pontuacao'])
                pontuacoes_criadas.append(existing_pontuacao.to_dict())
            else:
                # Criar nova pontuação
                pontuacao = Pontuacao(
                    qra_aluno=item['qra_aluno'],
                    pontuacao=float(item['pontuacao']),
                    prova_id=item['prova_id']
                )
                db.session.add(pontuacao)
                pontuacoes_criadas.append(pontuacao.to_dict())
        
        db.session.commit()
        return jsonify({'pontuacoes': pontuacoes_criadas}), 201
    except ValueError:
        return jsonify({'error': 'Pontuação deve ser um número válido'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@pontuacao_bp.route('/pontuacoes/prova/<int:prova_id>', methods=['GET'])
def get_pontuacoes_by_prova(prova_id):
    """Obter todas as pontuações de uma prova específica"""
    try:
        # Verificar se a prova existe
        prova = Prova.query.get_or_404(prova_id)
        
        pontuacoes = Pontuacao.query.filter_by(prova_id=prova_id).all()
        result = []
        for pontuacao in pontuacoes:
            pontuacao_dict = pontuacao.to_dict()
            pontuacao_dict['prova'] = prova.to_dict()
            result.append(pontuacao_dict)
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pontuacao_bp.route('/resultados/aluno/<string:qra_aluno>', methods=['GET'])
def get_resultados_aluno(qra_aluno):
    """Obter o resultado total de um aluno específico"""
    try:
        # Buscar todas as pontuações do aluno
        pontuacoes = Pontuacao.query.filter_by(qra_aluno=qra_aluno).all()
        
        if not pontuacoes:
            return jsonify({'error': 'Nenhuma pontuação encontrada para este aluno'}), 404
        
        total_pontuacao = sum(p.pontuacao for p in pontuacoes)
        total_provas = len(pontuacoes)
        media = total_pontuacao / total_provas if total_provas > 0 else 0
        
        # Detalhes das provas
        detalhes_provas = []
        for pontuacao in pontuacoes:
            prova = Prova.query.get(pontuacao.prova_id)
            if prova:
                detalhes_provas.append({
                    'prova_id': prova.id,
                    'nome_prova': prova.nome,
                    'data_aplicacao': prova.data_aplicacao.isoformat(),
                    'pontuacao': pontuacao.pontuacao
                })
        
        resultado = {
            'qra_aluno': qra_aluno,
            'total_pontuacao': total_pontuacao,
            'total_provas': total_provas,
            'media': round(media, 2),
            'detalhes_provas': detalhes_provas
        }
        
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pontuacao_bp.route('/resultados', methods=['GET'])
def get_resultados_todos_alunos():
    """Obter resultados de todos os alunos"""
    try:
        # Buscar todos os QRAs únicos
        qras_alunos = db.session.query(Pontuacao.qra_aluno).distinct().all()
        
        resultados = []
        for (qra_aluno,) in qras_alunos:
            pontuacoes = Pontuacao.query.filter_by(qra_aluno=qra_aluno).all()
            
            total_pontuacao = sum(p.pontuacao for p in pontuacoes)
            total_provas = len(pontuacoes)
            media = total_pontuacao / total_provas if total_provas > 0 else 0
            
            resultado = {
                'qra_aluno': qra_aluno,
                'total_pontuacao': total_pontuacao,
                'total_provas': total_provas,
                'media': round(media, 2)
            }
            resultados.append(resultado)
        
        # Ordenar por total de pontuação (decrescente)
        resultados.sort(key=lambda x: x['total_pontuacao'], reverse=True)
        
        return jsonify(resultados), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pontuacao_bp.route('/pontuacoes/<int:pontuacao_id>', methods=['PUT'])
def update_pontuacao(pontuacao_id):
    """Atualizar uma pontuação"""
    try:
        pontuacao = Pontuacao.query.get_or_404(pontuacao_id)
        data = request.get_json()
        
        if 'pontuacao' in data:
            pontuacao.pontuacao = float(data['pontuacao'])
        
        if 'qra_aluno' in data:
            pontuacao.qra_aluno = data['qra_aluno']
        
        db.session.commit()
        
        # Retornar a pontuação atualizada com informações da prova
        result = pontuacao.to_dict()
        prova = Prova.query.get(pontuacao.prova_id)
        if prova:
            result['prova'] = prova.to_dict()
        
        return jsonify(result), 200
    except ValueError:
        return jsonify({'error': 'Pontuação deve ser um número válido'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@pontuacao_bp.route('/pontuacoes/<int:pontuacao_id>', methods=['DELETE'])
def delete_pontuacao(pontuacao_id):
    """Deletar uma pontuação"""
    try:
        pontuacao = Pontuacao.query.get_or_404(pontuacao_id)
        db.session.delete(pontuacao)
        db.session.commit()
        return jsonify({'message': 'Pontuação deletada com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

