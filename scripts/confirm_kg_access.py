import pandas as pd

from __init__ import data_dir
from kg import KnowledgeGraph

i = 5
kg = KnowledgeGraph()
with pd.read_csv(data_dir + "/kg.csv", dtype=str, chunksize=10) as reader:
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

        kg.add_attribute_triples(attr_trips)
        kg.add_relation_quadruples(rel_quads)
        print(kg._ontology)
        i += 1
        if i % 5 == 0:
            break

print(kg.relations())
# print(kg.entities())
# print(kg.attribute_triples())
# print(kg.attribute_triples("11592"))

kg.add_relation_quadruple(
    ("2", "protein-protein", "2122", {"display_relation": "ppi"})
)
kg.add_relation_quadruple(("2", "target", "2122", {"display_relation": "tgt"}))
kg.add_relation_quadruple(("2", "target", "2122", {"display_relation": "tgt"}))
a = kg.relation_quadruples()
print("\n\n\n", a)
# print(kg.relation_quadruples("2"))
# print(kg.relation_quadruples("2", "2122"))
