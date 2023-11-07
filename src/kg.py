from collections import Counter
from collections.abc import Mapping, Sequence
from typing import Any, List, Set, Tuple

import networkx as nx

# Type declarations
Attribute = str
Entity = str | int
Relation = str | int
AttributeTriple = Tuple[Entity, Attribute, Any]
RelationQuadruple = Tuple[Entity, Relation, Entity, Mapping[Attribute, Any]]


class KnowledgeGraph:
    def __init__(
        self,
        attr_trips: Sequence[AttributeTriple] = None,
        rel_quads: Sequence[RelationQuadruple] = None,
    ) -> None:
        self.mdg = nx.MultiDiGraph()
        self._ontology = Counter()
        if attr_trips:
            self.add_attribute_triples(attr_trips)
        if rel_quads:
            self.add_relation_quadruples(rel_quads)

    # Methods for KG management

    def add_attribute_triples(
        self, attr_trips: Sequence[AttributeTriple]
    ) -> None:
        nodes = [
            (entity, {attribute: value})
            for entity, attribute, value in attr_trips
        ]
        self._maintain_onto_adding_trips(attr_trips)
        self.mdg.add_nodes_from(nodes)

    def add_attribute_triple(self, attr_trip: AttributeTriple) -> None:
        self._maintain_onto_adding_trips([attr_trip])
        self.mdg.add_node(attr_trip[0], **{attr_trip[1]: attr_trip[2]})

    def add_relation_quadruples(
        self, rel_quads: Sequence[RelationQuadruple]
    ) -> None:
        edges = [
            (src_entity, dest_entity, relation, attributes)
            for src_entity, relation, dest_entity, attributes in rel_quads
        ]
        self._maintain_onto_adding_quads(rel_quads)
        self.mdg.add_edges_from(edges)

    def add_relation_quadruple(self, rel_quad: RelationQuadruple) -> None:
        self.mdg.add_edge(
            rel_quad[0], rel_quad[2], key=rel_quad[1], **rel_quad[3]
        )
        self._maintain_onto_adding_quads([rel_quad])

    # Methods for accessing KG data

    def entities(self) -> Set[Entity]:
        return set(self.mdg.nodes())

    def ontology(self) -> Counter:
        return self._ontology

    def relations(self) -> Set[Relation]:
        return set([onto_trip[1] for onto_trip in self.ontology().keys()])

    def attribute_triples(self, entity: Entity = None) -> Set[AttributeTriple]:
        if entity:
            if entity not in self.entities():
                raise LookupError(f"Entity {entity} not in knowledge graph")
            nodes = [(entity, self.mdg.nodes(data=True)[entity])]
        else:
            nodes = self.mdg.nodes(data=True)
        triples = set()
        for node in nodes:
            triples.update(
                set([(node[0], attr, val) for attr, val in node[1].items()])
            )
        return triples

    def relation_quadruples(
        self, head_entity: Entity = None, tail_entity: Entity = None
    ) -> List[RelationQuadruple]:
        if head_entity and tail_entity:
            all_quads_from_head = list(
                self.mdg.edges(head_entity, data=True, keys=True)
            )
            quads = [
                quad for quad in all_quads_from_head if quad[1] == tail_entity
            ]
        elif head_entity:
            quads = list(self.mdg.edges(head_entity, data=True, keys=True))
        else:
            quads = list(self.mdg.edges(data=True, keys=True))
        quads = [
            (src_entity, relation, dest_entity, attributes)
            for src_entity, dest_entity, relation, attributes in quads
        ]
        return quads


    # Ontology maintenance from adding or removing entities or relations

    def _maintain_onto_adding_trips(self, attr_trips: Sequence[AttributeTriple]) -> None:
        # Update ontology relation triples if type is updated
        new_type_triples = [attr_trip for attr_trip in attr_trips if attr_trip[1] == "type"]
        onto_update = Counter()
        for new_type_triple in new_type_triples:
            head_entity = new_type_triple[0]
            if head_entity in self.entities():
                # Relations from head entity might exist
                old_head_type = [attr_trip[2] for attr_trip 
                    in self.attribute_triples(head_entity) if attr_trip[1] == "type"]
                old_head_type = old_head_type[0] if old_head_type else "unknown"
                new_head_type = new_type_triple[2]
                for relation_quad in self.relation_quadruples(head_entity):
                    tail_entity = relation_quad[2]
                    tail_type = [attr_trip[2] for attr_trip 
                        in self.attribute_triples(tail_entity) if attr_trip[1] == "type"]
                    tail_type = tail_type[0] if tail_type else "unknown"

                    relation = relation_quad[1]
                    old_onto_triple = (old_head_type, relation, tail_type)
                    new_onto_triple = (new_head_type, relation, tail_type)
                    if old_onto_triple != new_onto_triple:
                        onto_update.update({old_onto_triple: -1, new_onto_triple: 1})
        
        self._ontology.update(onto_update)
    
    def _maintain_onto_adding_quads(self, rel_quads: Sequence[RelationQuadruple]) -> None:
        onto_triples = []
        for rel_quad in rel_quads:
            head_entity, relation, tail_entity = rel_quad[:3]
            head_type = [attr_trip[2] for attr_trip 
                    in self.attribute_triples(head_entity) if attr_trip[1] == "type"]
            head_type = head_type[0] if head_type else "unknown"
            tail_type = [attr_trip[2] for attr_trip 
                    in self.attribute_triples(tail_entity) if attr_trip[1] == "type"]
            tail_type = tail_type[0] if tail_type else "unknown"
            onto_triple = (head_type, relation, tail_type)
            onto_triples += [onto_triple]
        self._ontology.update(onto_triples)

    
    # Sanity check - manual ontology generation

    def _generate_onto_from_mdg(self) -> None:
        ontology = Counter()
        for head_entity, adj in self.mdg.adjacency():
            for tail_entity, edges in adj.items():
                for relation in edges.keys():
                    head_type = self.mdg.nodes[head_entity]["type"]
                    tail_type = self.mdg.nodes[tail_entity]["type"]
                    ontology.update([(head_type, relation, tail_type)])
        self._ontology = ontology
