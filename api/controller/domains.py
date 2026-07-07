from flask import request
from flask_restplus import Resource

from api.model.Concept import Concept
from api.model.Domain import Domain
from api.service.services import get_all_domains, add_domain, get_domain, delete_domain, get_subdomains, \
    get_concepts_tree, update_domain, get_parent_domains

api = Domain.api
_domain = Domain.domain
concept_api = Concept.api
_concept = Concept.concept


@api.route('/<string:tenant_id>')
class DomainsList(Resource):
    @api.doc('list all domains')
    @api.marshal_list_with(_domain)
    def get(self, tenant_id):
        return get_all_domains(tenant_id)

    @api.doc('create a new domain')
    @api.expect([Domain.new_domain_req], validate=True)
    def post(self):
        data = request.json
        for domain in data:
            result = add_domain(domain)
            return result


@api.route('/<string:domain_id>')
class DisplayDomain(Resource):
    @api.doc('get domain details')
    def get(self, domain_id):
        domain = get_domain(domain_id)
        if domain is not None:
            return domain
        else:
            api.abort(404, "Domain not found!")

    @api.doc('update domain')
    @api.expect(Domain.new_domain_req, validate=True)
    def put(self, domain_id):
        domain = request.json
        return update_domain(domain_id, domain)

    @api.doc('delete a domain')
    def delete(self, domain_id):
        domain = delete_domain(domain_id)
        if domain is not None:
            return {"message": "Domain deleted successfully"}
        else:
            api.abort(404, "Domain not found!")


@api.route('/<string:domain_id>/subdomains')
class DisplaySubDomains(Resource):
    @api.doc('get subdomains of a domain')
    def get(self, domain_id):
        return get_subdomains(domain_id)


@api.route('/<string:domain_id>/conceptsTree')
class DisplayConceptsTree(Resource):
    @api.doc('get concepts tree of a domain')
    def get(self, domain_id):
        return get_concepts_tree(domain_id)


@api.route('/parents')
class DisplayParentDomains(Resource):
    @api.doc('get parent domains')
    def get(self):
        return get_parent_domains()
