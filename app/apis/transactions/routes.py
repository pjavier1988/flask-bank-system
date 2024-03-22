from . import transactions_bp
from app.containers import Container
from app.models.schemas import TransferSchema
from app.services.transaction_service import TransactionService
from app.exceptions import InsufficientFundsError, AccountNotExistsError, \
SameAccountError, NegativeValueError, SameAccountError
from dependency_injector.wiring import inject, Provide
from flask import request, jsonify, make_response
from flask import current_app



@transactions_bp.route('/transfer', methods=['POST'])
@inject
def transfer(transaction_service: TransactionService = Provide[Container.transaction_service]):
    schema = TransferSchema()
    data = request.json

    try:
        errors = schema.validate(data)
        if errors:
            return jsonify(errors), 400
        transaction_service.transfer(
            from_account_id=data.get('from_account'), 
            to_account_id=data.get('to_account'), 
            amount=data.get('amount')
        )
        response = {
            'code': 0,
            'message': 'Transfer Successful.',
            'data': {}
        }

        return response, 200
    except NegativeValueError as e:
            response = {
                'code': 1,
                'message': str(e),
                'data': {}
            }
            return response, 400
    except InsufficientFundsError as e:
            response = {
                'code': 1,
                'message': str(e),
                'data': {}
            }
            return response, 400
    except SameAccountError as e:
            response = {
                'code': 1,
                'message': str(e),
                'data': {}
            }
            return response, 400
    except AccountNotExistsError as e:
            response = {
                'code': 1,
                'message': str(e),
                'data': {}
            }
            return response, 400
    except Exception as e:
        current_app.logger.warning(e)
        return make_response(jsonify({"error": "An error occurred during the transfer"}), 500)

