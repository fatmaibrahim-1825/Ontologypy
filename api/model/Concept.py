from flask_restplus import Namespace, fields


class Concept:
    api = Namespace('domains', description='Concept related operations')
    Keyword = api.model('Keyword', {'term': fields.String(required=True, description='keyword term'),
                                    'definition': fields.String(required=True, description='keyword term definition')})
    concept = api.model('concept', {
        'id': fields.String(required=True, description='concept Id'),
        'name': fields.String(required=True, description='concept name'),
        'description': fields.String(required=False, description='concept description'),
        'depth': fields.String(required=False, description='concept depth'),
        'has_is_a': fields.String(required=False, description='concept above'),
        'part_of': fields.String(required=False, description="concept above"),
        'has_part': fields.List(fields.String(required=False, description="concept under"), required=False, description='concepts under'),
        'has_prereq': fields.String(required=False, description='concept prerequisite'),
        "has_follow": fields.String(required=False, description="concept concept after"),
        'keywords': fields.List(fields.Nested(Keyword),
                                required=False, description='concept keywords')
    })

    new_concept_req = api.model('New concept request', {
        'name': fields.String(required=True, description='concept name'),
        'description': fields.String(required=False, description='concept description'),
        'depth': fields.String(required=False, description='concept depth'),
        'has_is_a': fields.String(required=False, description='concept above'),
        'part_of': fields.String(required=False, description="concept above"),
        'has_part': fields.List(fields.String(required=False, description="concept under"), required=False, description='concepts under'),
        'has_prereq': fields.String(required=False, description='concept prerequisite'),
        "has_follow": fields.String(required=False, description="concept concept after"),
        'keywords': fields.List(fields.Nested(Keyword), required=False, description='concept keywords')
    })

    new_relation_req = api.model('New relation request', {
        'concept1': fields.String(required=True, description='concept 1'),
        'relation': fields.String(required=True, description='relation between two concepts',
                                  enum=["has_is_a", "has_part", "part_of", "has_prereq", "has_follow",
                                        "has_terminology", "keywords"]),
        'concept2': fields.String(required=True, description='concept 2'),
    })

    new_keywords_req = api.model('New Keywords request', {
        'keywords': fields.List(fields.Nested(Keyword), required=True, description='concept keywords')
    })
