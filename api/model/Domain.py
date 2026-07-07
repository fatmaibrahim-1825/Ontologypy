from flask_restplus import Namespace, fields


class Domain:
    api = Namespace('domains', description='Domain related operations')
    domain = api.model('domain', {
        'id': fields.String(required=True, description='domain Id'),
        'name': fields.String(required=True, description='domain name'),
        # 'description': fields.String(required=False, description='domain description'),

    })

    new_domain_req = api.model('New domain request', {
        'name': fields.String(required=True, description='domain name'),
        'description': fields.String(required=False, description='domain description'),
        'parent_domain_id': fields.String(required=False, description='parent domain id'),
    })
