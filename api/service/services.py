from time import clock_getres
from api.model import Domain
from SPARQLWrapper import SPARQLWrapper2, POST

from api.model.Concept import Concept
from api.service import generate_id, queries, endpoint, generate_uuid


def get_all_domains(ont):
    query = queries['Queries']['GetAllDomains']
    domains = []
    sparql = SPARQLWrapper2(endpoint+ont)
    sparql.setQuery(query)
    results = sparql.query()

    for binding in results.bindings:
        domains.append({
            "id": binding['id'].value,
            "name": binding['name'].value,
        })
    return domains


def get_domain(domain_id):
    query = queries['Queries']['GetDomain']
    query = query.replace('ID', domain_id)
    sparql = SPARQLWrapper2(endpoint)
    sparql.setQuery(query)
    ret = sparql.query()

    domain = None
    for binding in ret.bindings:
        domain = {
            "id": domain_id,
            "name": binding['name'].value,
        }
        if 'description' in binding:
            domain['description'] = binding['description'].value

    # GetSubDomains
    query = queries['Queries']['GetSubDomains']
    query = query.replace('ID', domain_id)
    sparql = SPARQLWrapper2(endpoint)
    sparql.setQuery(query)
    ret = sparql.query()

    subdomains = []
    if domain is not None:
        for binding in ret.bindings:
            subdomains.append(
                {"id": binding['id'].value, "name": binding['name'].value})
        domain['has_subdomain'] = subdomains
    return domain


def get_domain_by_name(domain_name):
    query = queries['Queries']['GetDomainByName']
    query = query.replace('DOMAIN_NAME', domain_name.title())
    sparql = SPARQLWrapper2(endpoint)
    sparql.setQuery(query)
    ret = sparql.query()
    domain = None
    for binding in ret.bindings:
        domain = {
            "id": binding['id'].value,
            "name": domain_name.title(),
        }
    return domain


def add_domain(domain: Domain):
    domain_id = generate_id(domain['name'])
    domain['id'] = domain_id
    domain['name'] = domain['name'].title()

    d = get_domain_by_name(domain['name'])
    if d is not None:
        return {"message": "domain '{0}' exists already".format(
                domain['name'])}
    else:
        if 'parent_domain_id' in domain:
            query = queries['Queries']['Add_Relation']
            query = query.replace('CONCEPT1', domain['parent_domain_id']).replace('RELATION', 'has_subdomain').replace(
                'CONCEPT2', domain['id'])
            sparql = SPARQLWrapper2(endpoint)
            sparql.setQuery(query)
            sparql.setMethod(POST)
            sparql.query()

        statements = "INSERT DATA {"+" so:{0} rdf:type so:Domain; so:id '{0}'; so:name '{1}'@en;".format(
            domain_id, domain['name'])
        if 'description' in domain:
            statements += "so:description    '{0}'@en;".format(
                domain['description'])
        statements += "}"

        query = queries['Queries']['Query']
        query = query.replace('STATEMENTS', statements)
        sparql = SPARQLWrapper2(endpoint)
        sparql.setQuery(query)
        sparql.setMethod(POST)
        sparql.query()
        return domain


def delete_domain(domain_id):
    print("delete_domain", domain_id)
    domain = get_domain(domain_id)
    if domain:
        query = queries['Queries']['DeleteDomain']
        query = query.replace('ID', domain_id)
        sparql = SPARQLWrapper2(endpoint)
        sparql.setQuery(query)
        sparql.setMethod(POST)
        results = sparql.query()
        if results.response.read():
            query = queries['Queries']['RemoveDomain']
            query = query.replace('ID', domain_id)
            sparql = SPARQLWrapper2(endpoint)
            sparql.setQuery(query)
            sparql.setMethod(POST)
            results = sparql.query()
            return {"message": "Domain deleted successfully"}
        else:
            return {"message": "Couldn't delete domain"}
    else:
        return None


def get_subdomains(domain_id):
    query = queries['Queries']['GetSubDomains']
    query = query.replace('ID', domain_id)
    sparql = SPARQLWrapper2(endpoint)
    sparql.setQuery(query)
    ret = sparql.query()
    domains = []
    for binding in ret.bindings:
        domains.append({
            "id": binding['id'].value,
            "name": binding['name'].value,
        })
    return domains


def update_domain(domain_id, domain):
    domain['id'] = domain_id
    domain['name'] = domain['name'].title()

    d = get_domain(domain_id)
    if d is not None:
        x = get_domain_by_name(domain['name'])
        if x is not None and x['id'] != domain['id']:
            return {"message": "there is a domain with the same name '{0}', please enter a unique name".format(domain['name'])}
        else:
            delete_domain(domain_id)

            if 'parent_domain_id' in domain:
                query = queries['Queries']['Add_Relation']
                query = query.replace('CONCEPT1', domain['parent_domain_id']).replace('RELATION', 'has_subdomain').replace(
                    'CONCEPT2', domain['id'])
                sparql = SPARQLWrapper2(endpoint)
                sparql.setQuery(query)
                sparql.setMethod(POST)
                sparql.query()

            statements = "INSERT DATA {"+" so:{0} rdf:type so:Domain; so:id '{0}'; so:name '{1}'@en;".format(
                domain_id, domain['name'])
            if 'description' in domain:
                statements += "so:description    '{0}'@en;".format(
                    domain['description'])
            statements += "}"

            query = queries['Queries']['Query']
            query = query.replace('STATEMENTS', statements)
            sparql = SPARQLWrapper2(endpoint)
            sparql.setQuery(query)
            sparql.setMethod(POST)
            results = sparql.query()
            if results.response.code == 200:
                return {"message": "domain '{0}' updated successfully".format(domain_id)}
            else:
                return {"message": "domain '{0}' failed to be updated".format(domain_id)}
    else:
        return {"message": "Domain {0} not found".format(domain_id)}


def get_concepts(domain_id):
    query = queries['Queries']['GetAllConcepts']
    query = query.replace('ID', domain_id)
    sparql = SPARQLWrapper2(endpoint)
    sparql.setQuery(query)
    ret = sparql.query()
    concepts = []
    for binding in ret.bindings:
        concepts.append({
            "id": binding['id'].value,
            "name": binding['name'].value,
        })
    return concepts


def get_concept(domain_id, concept_id):
    query = queries['Queries']['GetConcept']
    query = query.replace('DOMAIN_ID', domain_id).replace('ID', concept_id)
    sparql = SPARQLWrapper2(endpoint)
    sparql.setQuery(query)
    ret = sparql.query()
    concept = None
    for binding in ret.bindings:
        concept = {"id": concept_id, "name": binding['name'].value}
        if 'description' in binding:
            concept['description'] = binding['description'].value
        if 'depth' in binding:
            concept['depth'] = binding['depth'].value
    if concept is not None:
        concept["has_is_a"] = get_relation(concept_id, "has_is_a")
        concept["has_part"] = get_relation(concept_id, "has_part")
        concept["has_prereq"] = get_relation(concept_id, "has_prereq")
        concept["instance_of"] = get_relation(concept_id, "instance_of")
        concept["has_follow"] = get_relation(concept_id, "has_follow")
        concept["has_terminology"] = get_relation(
            concept_id, "has_terminology")
    return concept


def get_concept_by_name(domain_id, concept_name):
    query = queries['Queries']['GetConceptByName']
    query = query.replace('DOMAIN_ID', domain_id).replace(
        'NAME', concept_name.title())
    sparql = SPARQLWrapper2(endpoint)
    sparql.setQuery(query)
    ret = sparql.query()
    concept = None
    for binding in ret.bindings:
        concept = {
            "id": binding['id'].value,
            "name": concept_name.title(),
        }
        if 'description' in binding:
            concept['description'] = binding['description'].value
        if 'depth' in binding:
            concept['depth'] = binding['depth'].value
    print(concept)
    if concept is not None:
        concept["has_is_a"] = get_relation_2(concept['id'], "has_is_a")
        concept["part_of"] = get_relation_2(concept['id'], "part_of")
        concept["has_part"] = get_relation(concept['id'], "has_part")
        concept["has_prereq"] = get_relation_2(concept['id'], "has_prereq")
        concept["has_follow"] = get_relation_2(concept['id'], "has_follow")
        concept["has_terminology"] = get_relation(
            concept['id'], "has_terminology")
    print(concept)
    return concept


def add_concept(domain_id, concept):
    concept_id = generate_uuid()
    concept['id'] = concept_id
    concept['name'] = concept['name'].title()

    cons = get_concept_by_name(domain_id, concept['name'])
    if cons is not None:
        return {"message": "concept '{0}' exists already in this domain".format(
                concept['name'])}
    else:

        statements = "INSERT DATA {"+" so:{0}    so:has_concept    so:{1}. so:{1} rdf:type    so:Concept; so:id   '{1}'; so:name   '{2}'@en".format(
            domain_id, concept_id, concept['name'])
        if "description" in concept:
            statements += "; so:description    '{0}'@en".format(
                concept['description'])
        if "depth" in concept:
            statements += "; so:depth   '{0}'".format(concept['depth'])

        if "has_is_a" in concept:
            statements += "; so:has_is_a   so:{0}".format(concept['has_is_a'])

        if "part_of" in concept:
            statements += "; so:part_of   so:{0}".format(concept['part_of'])

        if "has_part" in concept:
            for x in concept['has_part']:
                statements += "; so:has_part   so:{0}".format(x)

        if 'has_prereq' in concept:
            statements += "; so:has_prereq   so:{0}".format(
                concept['has_prereq'])

        if 'has_follow' in concept:
            statements += "; so:has_follow   so:{0}".format(
                concept['has_follow'])

        if "part_of" in concept:
            statements += ". so:{0}   so:has_part   so:{1}.".format(
                concept['part_of'], concept_id)
        statements += "}"
        print(statements)
        query = queries['Queries']['Query']
        query = query.replace('STATEMENTS', statements)

        sparql = SPARQLWrapper2(endpoint)
        sparql.setQuery(query)
        sparql.setMethod(POST)
        results = sparql.query()

        if results.response.code == 200:
            return {"message": "concept '{0}' added successfully".format(concept['name'])}
        else:
            return {"message": "concept '{0}' failed to be added".format(concept['name'])}


def update_concept(domain_id, concept_id, concept):
    concept['id'] = concept_id
    concept['name'] = concept['name'].title()

    cons = get_concept(domain_id, concept_id)
    if cons is not None:
        con = get_concept_by_name(domain_id, concept['name'])
        if con is not None and con['id'] != concept['id']:
            return {"message": "there is a concept with the same name '{0}', please enter a unique name".format(concept['name'])}
        else:
            delete_concept(domain_id, concept_id)

            statements = "INSERT DATA {"+" so:{0}    so:has_concept    so:{1}. so:{1} rdf:type    so:Concept; so:id   '{1}'; so:name   '{2}'@en;".format(
                domain_id, concept_id, concept['name'])
            if "description" in concept:
                statements += "so:description    '{0}'@en;".format(
                    concept['description'])
            if "depth" in concept:
                statements += "so:depth   '{0}';".format(concept['depth'])

            if "has_is_a" in concept:
                statements += "so:has_is_a   so:{0};".format(
                    concept['has_is_a'])

            if "part_of" in concept:
                statements += "so:part_of   so:{0};".format(concept['part_of'])

            if "has_part" in concept:
                for x in concept['has_part']:
                    statements += "so:has_part   so:{0};".format(x)

            if 'has_prereq' in concept:
                statements += "so:has_prereq   so:{0};".format(
                    concept['has_prereq'])

            if 'has_follow' in concept:
                statements += "so:has_follow   so:{0};".format(
                    concept['has_follow'])
            statements += "}"

            query = queries['Queries']['Query']
            query = query.replace('STATEMENTS', statements)

            sparql = SPARQLWrapper2(endpoint)
            sparql.setQuery(query)
            sparql.setMethod(POST)
            results = sparql.query()

            if results.response.code == 200:
                return {"message": "concept '{0}' updated successfully".format(concept_id)}
            else:
                return {"message": "concept '{0}' failed to be updated".format(concept_id)}
    else:
        return {"message": "concept '{0}' not found".format(concept_id)}


def delete_concept(domain_id, concept_id):
    statements = "DELETE WHERE {" + " so:{0}  ?predicate  ?object. so:{1}   so:has_concept  so:{0}".format(
        concept_id, domain_id)
    statements += "}"
    query = queries['Queries']['Query']
    query = query.replace('STATEMENTS', statements)
    sparql = SPARQLWrapper2(endpoint)
    sparql.setQuery(query)
    sparql.setMethod(POST)
    results = sparql.query()
    return results


def get_relation(concept_id, relation):
    query = queries['Queries']['Get_Relation']
    query = query.replace('CONCEPT_ID', concept_id).replace(
        'RELATION', relation)
    concepts = []
    sparql = SPARQLWrapper2(endpoint)
    sparql.setQuery(query)
    results = sparql.query()
    for binding in results.bindings:
        c = {
            "id": binding['id'].value,
            "name": binding['name'].value,
        }
        c[relation] = get_relation(c['id'], relation)

        concepts.append(c)
    return concepts


def get_concept_relations(concept):
    concept["has_is_a"] = get_relation_2(concept['id'], "has_is_a")
    concept["part_of"] = get_relation_2(concept['id'], "part_of")
    concept["has_part"] = get_relation(concept['id'], "has_part")
    concept["has_prereq"] = get_relation_2(concept['id'], "has_prereq")
    concept["has_follow"] = get_relation_2(concept['id'], "has_follow")
    concept["has_terminology"] = get_relation(
        concept['id'], "has_terminology")
    return concept


def get_relation_2(concept_id, relation):
    statements = "SELECT * WHERE {" + " so:{0}  so:{1}  ?object. ?object  so:id ?id; so:name  ?name".format(
        concept_id, relation)
    statements += "}"
    query = queries['Queries']['Query']
    query = query.replace('STATEMENTS', statements)
    concept = {}
    sparql = SPARQLWrapper2(endpoint)
    sparql.setQuery(query)
    results = sparql.query()
    for binding in results.bindings:
        concept = {
            "id": binding['id'].value,
            "name": binding['name'].value,
        }
        concept[relation] = get_relation_2(concept['id'], relation)
    return concept


def add_relation(data):
    query = queries['Queries']['Add_Relation']
    query = query.replace('CONCEPT1', data['concept1']).replace('RELATION', data['relation']).replace('CONCEPT2',
                                                                                                      data['concept2'])
    sparql = SPARQLWrapper2(endpoint)
    sparql.setQuery(query)
    sparql.setMethod(POST)
    results = sparql.query()
    return {"message": 'relation added successfully'}


def get_concept_tree(domain_id, concept_id):
    concept = get_concept(domain_id, concept_id)
    concept = get_concept_relations(concept)

    return concept


def get_concept_keywords(domain_id, concept_id):
    query = queries['Queries']['Get_Concept_keywords']
    query = query.replace('DOMAIN_ID', domain_id).replace(
        'CONCEPT_ID', concept_id)
    keywords = []
    sparql = SPARQLWrapper2(endpoint)
    sparql.setQuery(query)
    results = sparql.query()
    for binding in results.bindings:
        keywords.append(
            {'term': binding['term'].value, 'definition': binding['definition'].value})
    return keywords


def add_concept_keywords(domain_id, concept_id, keywords):
    for keyword in keywords:
        keyword_id = generate_id(keyword['term'])
        query = queries['Queries']['Add_Concept_Keyword']
        query = query.replace('DOMAIN_ID', domain_id).replace('CONCEPT_ID', concept_id).replace('KEYWORD_ID',
                                                                                                keyword_id).replace(
            'TERM', keyword['term']).replace('DEFINITION', keyword['definition'])
        sparql = SPARQLWrapper2(endpoint)
        sparql.setQuery(query)
        sparql.setMethod(POST)
        results = sparql.query()
    return {"message": 'keywords added successfully'}


def get_concepts_tree(domain_id):
    root_concepts = get_domain_root_concepts(domain_id)
    for concept in root_concepts:
        concept = get_concept_relations(concept)
    return root_concepts


def get_domain_root_concepts(domain_id):
    query = queries['Queries']['GetDomainRootConcepts']
    query = query.replace('DOMAIN_ID', domain_id)
    sparql = SPARQLWrapper2(endpoint)
    sparql.setQuery(query)
    ret = sparql.query()
    concepts = []
    ids = []
    for binding in ret.bindings:
        id = binding['id'].value
        if (id not in ids):
            ids.append(id)
            concept = ({
                "id": id,
                "name": binding['name'].value,
                # "description": binding['description'].value,
                # "depth": binding['depth'].value,
            })
            if 'description' in binding:
                concept['description'] = binding['description'].value
            if 'depth' in binding:
                concept['depth'] = binding['depth'].value
            concepts.append(concept)
    print(concepts)
    return concepts


def get_parent_domains():
    query = queries['Queries']['GetParentDomains']
    sparql = SPARQLWrapper2(endpoint)
    sparql.setQuery(query)
    ret = sparql.query()
    domains = []
    for binding in ret.bindings:
        domains.append({
            "id": binding['id'].value,
            "name": binding['name'].value,
        })
    return domains
