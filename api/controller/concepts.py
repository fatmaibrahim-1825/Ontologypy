from flask import request
from flask_restplus import Resource

from api.model.Concept import Concept
from api.service import generate_id
from api.service.services import add_concept, get_concept, get_concepts, delete_concept, add_relation, \
    get_relation, get_concept_tree, get_concept_by_name, add_concept_keywords, get_concept_keywords, update_concept

api = Concept.api
_concept = Concept.concept


@api.route('/<string:domain_id>/concepts')
class DisplayDomainConcepts(Resource):
    @api.doc('get domain concepts')
    def get(self, domain_id):
        return get_concepts(domain_id)

    @api.doc('create a new concept')
    @api.expect([Concept.new_concept_req], validate=True)
    def post(self, domain_id):
        data = request.json
        result = []
        for concept in data:
            result.append(add_concept(domain_id, concept))
        return result


@api.route('/<string:domain_id>/concepts/<string:concept_id>')
class DisplayConcept(Resource):
    @api.doc('get concept')
    def get(self, domain_id, concept_id):
        concept = get_concept(domain_id, concept_id)
        if concept is not None:
            return concept
        else:
            api.abort(404, "Concept not found!")

    @api.doc('update concept')
    @api.expect(Concept.new_concept_req, validate=True)
    def put(self, domain_id, concept_id):
        concept = request.json
        return update_concept(domain_id, concept_id, concept)

    @api.doc('delete a concept')
    def delete(self, domain_id, concept_id):
        concept = get_concept(domain_id, concept_id)
        if concept is not None:
            results = delete_concept(domain_id, concept_id)
            return {"message": "Concept {0} deleted successfully".format(concept_id)}
        else:
            api.abort(404, "Couldn't find concept")


@api.route('/<string:domain_id>/concepts/<string:concept_id>/<string:relation>')
class DisplayRelation(Resource):
    @api.doc('get concept relation')
    def get(self, domain_id, concept_id, relation):
        concept = get_relation(concept_id, relation)
        if concept is not None:
            return concept
        else:
            api.abort(404, "Concept not found!")


@api.route('/<string:domain_id>/concepts/add_relation')
class AddRelation(Resource):
    @api.doc('create a new relation')
    @api.expect(Concept.new_relation_req, validate=True)
    def post(self, domain_id):
        data = request.json
        concept = get_concept(domain_id, data['concept1'])
        if concept is not None:
            result = add_relation(data)
            return result


@api.route('/<string:domain_id>/concepts/<string:concept_id>/tree')
class DisplayConceptTree(Resource):
    @api.doc('get concept relation')
    def get(self, domain_id, concept_id):
        concept = get_concept_tree(domain_id, concept_id)
        if concept is not None:
            return concept
        else:
            api.abort(404, "Concept not found!")


@api.route('/<string:domain_id>/concepts/name/<string:concept_name>')
class DisplayConcept(Resource):
    @api.doc('get concept by name')
    # @api.marshal_with(_concept)
    def get(self, domain_id, concept_name):
        concept = get_concept_by_name(domain_id, concept_name)
        if concept is not None:
            return concept
        else:
            api.abort(404, "Concept not found!")


@api.route('/<string:domain_id>/concepts/<string:concept_id>/keywords')
class DisplayConceptKeywords(Resource):
    @api.doc('get concept keywords')
    def get(self, domain_id, concept_id):
        keywords = get_concept_keywords(domain_id, concept_id)
        if keywords is not None:
            return keywords
        else:
            api.abort(404, "Not found!")

    @api.doc('add concept keywords')
    @api.expect(Concept.new_keywords_req, validate=True)
    def post(self, domain_id, concept_id):
        data = request.json
        return add_concept_keywords(domain_id, concept_id, data['keywords'])
