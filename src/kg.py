from collections.abc import Mapping, Sequence
from typing import Any, Tuple

import networkx as nx

# Type declarations
Attribute = str
Entity = str | int
Relation = str | int
AttributeTriple = Tuple[Entity, Attribute, Any]
RelationQuadruple = Tuple[Entity, Relation, Entity, Mapping[Attribute, Any]]

class KnowledgeGraph:

    def __init__(self, attr_trips: Sequence[AttributeTriple] = None, rel_quads: Sequence[RelationQuadruple] = None) -> None:
        self.mdg = nx.MultiDiGraph()
        self.relations = set()
        if attr_trips:
            self.add_attribute_triples(attr_trips)
        if rel_quads:
            self.add_relation_quadruples(rel_quads)
    
    # Methods for KG management
    
    def add_attribute_triples(self, attr_trips: Sequence[AttributeTriple]) -> None:
        nodes = [(entity, {attribute: value})
                  for entity, attribute, value in attr_trips]
        self.mdg.add_nodes_from(nodes)
    
    def add_attribute_triple(self, attr_trip: AttributeTriple) -> None:
        self.mdg.add_node(attr_trip[0], **{attr_trip[1]: attr_trip[2]})

    def add_relation_quadruples(self, rel_quads: Sequence[RelationQuadruple]) -> None:
        edges = [(src_entity, dest_entity, relation, attributes)
                 for src_entity, relation, dest_entity, attributes in rel_quads]
        self.mdg.add_edges_from(edges)
    
    def add_relation_quadruple(self, rel_quad: RelationQuadruple) -> None:
        self.mdg.add_edge(rel_quad[0], rel_quad[2], key=rel_quad[1], **rel_quad[3])
        self.relations.add(rel_quad[1])
