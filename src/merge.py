from copy import deepcopy

from kg import KnowledgeGraph

def simple_merge(kg1: KnowledgeGraph, kg2: KnowledgeGraph) -> KnowledgeGraph:
    merged_kg = deepcopy(kg1)
    kg2_trips, kg2_quads = kg2.attribute_triples(), kg2.relation_quadruples()
    merged_kg.add_attribute_triples(kg2_trips)
    merged_kg.add_relation_quadruples(kg2_quads)
    return merged_kg