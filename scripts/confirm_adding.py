import pandas as pd

from __init__ import data_dir
from kg import KnowledgeGraph
from networkx.utils import graphs_equal

kg1 = KnowledgeGraph()
kg2 = KnowledgeGraph()
i = 0
with pd.read_csv(data_dir + "/kg.csv", dtype=str, chunksize=100000) as reader:
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
        kg1.add_attribute_triples(attr_trips)
        for attr_trip in attr_trips:
            kg2.add_attribute_triple(attr_trip)

        rel_quads = [
            (
                row["x_index"],
                row["relation"],
                row["y_index"],
                {"display_relation": row["display_relation"]},
            )
            for _, row in chunk.iterrows()
        ]
        kg1.add_relation_quadruples(rel_quads)
        for rel_quad in rel_quads:
            kg2.add_relation_quadruple(rel_quad)

        print(graphs_equal(kg1.mdg, kg2.mdg))
        i += 1
        if i % 5 == 0:
            print(f"Processed {i*100000} rows")
            break

print(kg1._ontology == kg2._ontology)
kg2._generate_onto_from_mdg()
print(kg1._ontology == kg2._ontology)
