from flask_restplus import Api
from flask import Blueprint


from api.controller.domains import api as domain_ns
from api.controller.concepts import api as concept_ns
import os


blueprint = Blueprint('Ontology APIs', __name__, url_prefix=os.getenv('urlPrefix'))

api = Api(blueprint,
          title='SCube Ontology APIs',
          version='2.0',
          description='Modernized Ontology APIs',
          # prefix='/api/ontologypy',
          doc='/docs/',
          )

api.add_namespace(domain_ns)
api.add_namespace(concept_ns)
