import pandas as pd
from networkx.utils import graphs_equal

from __init__ import data_dir
from kg import KnowledgeGraph
from merge import simple_merge

kg1 = KnowledgeGraph()
kg2 = KnowledgeGraph()
kg3 = KnowledgeGraph()
i = 0
with pd.read_csv(data_dir + "/kg.csv", dtype=str, chunksize=100) as reader:
    for chunk in reader:
        attr_trips = [
            (row["x_index"], "name", row["x_name"])
            for _, row in chunk.iterrows()
        ]
        attr_trips += [
            (row["x_index"], "type", row["x_type"])
            for _, row in chunk.iterrows()
        ]
        attr_trips += [
            (row["x_index"], "source", row["x_source"])
            for _, row in chunk.iterrows()
        ]
        attr_trips += [
            (row["y_index"], "name", row["y_name"])
            for _, row in chunk.iterrows()
        ]
        attr_trips += [
            (row["y_index"], "type", row["y_type"])
            for _, row in chunk.iterrows()
        ]
        attr_trips += [
            (row["y_index"], "source", row["y_source"])
            for _, row in chunk.iterrows()
        ]

        rel_quads = [
            (
                row["x_index"],
                row["relation"],
                row["y_index"],
                {"display_relation": row["display_relation"]},
            )
            for _, row in chunk.iterrows()
        ]

        kg3.add_attribute_triples(attr_trips)
        kg3.add_relation_quadruples(rel_quads)
        if i < 20:
            kg1.add_attribute_triples(attr_trips)
            kg1.add_relation_quadruples(rel_quads)
        elif i <= 20 and i <= 30:
            kg1.add_attribute_triples(attr_trips)
            kg1.add_relation_quadruples(rel_quads)
            kg2.add_attribute_triples(attr_trips)
            kg2.add_relation_quadruples(rel_quads)
        else:
            kg2.add_attribute_triples(attr_trips)
            kg2.add_relation_quadruples(rel_quads)

        i += 1
        print(i)
        if i % 50 == 0:
            break

kg4 = simple_merge(kg1, kg2)
print(graphs_equal(kg3.mdg, kg4.mdg))
print(kg3.entities() == kg4.entities())
print(kg3.attribute_triples() == kg4.attribute_triples())
print(kg3.relation_triples() == kg4.relation_triples())
print(kg3.ontology() == kg4.ontology())
