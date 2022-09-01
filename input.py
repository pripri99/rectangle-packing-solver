# Load Data
import networkx as nx
import json

test_data = [
    {
        "1": {
                "1": {
                    "x": 12,
                    "y": 11,
                    "min_area": 90,
                    "max_area": 2622,
                    "adj_ref": 1,
                    "type": "Bedroom",
                    "label": "bed1"
                },
                "2": {
                    "x": 18,
                    "y": 11,
                    "min_area": 90,
                    "max_area": 2622,
                    "adj_ref": 2,
                    "type": "Living",
                    "label": "living"
                },
                "3": {
                    "x": 12,
                    "y": 9,
                    "min_area": 50,
                    "max_area": 2622,
                    "adj_ref": 3,
                    "type": "Bathroom",
                    "label": "bath"
                },
                "4": {
                    "x": 13,
                    "y": 11,
                    "min_area": 132,
                    "max_area": 2622,
                    "adj_ref": 4,
                    "type": "Kitchen",
                    "label": "kitchen"
                },
                "5": {
                    "x": 12,
                    "y": 5,
                    "min_area": 132,
                    "max_area": 2622,
                    "adj_ref": 5,
                    "type": "entrance",
                    "label": "entry"
                },
                "6": {
                    "x": 12,
                    "y": 4,
                    "min_area": 132,
                    "max_area": 2622,
                    "adj_ref": 6,
                    "type": "corridor",
                    "label": "cor."
                },
                "7": {
                    "x": 12,
                    "y": 4,
                    "min_area": 132,
                    "max_area": 2622,
                    "adj_ref": 7,
                    "type": "corridor",
                    "label": "cor."
                },
                "adjs": [(1,2), (1,7), (2,4), (4,5), (3,7), (3,6)],
                "adj_ban": [],
                "info": {
                    "name" : "Nordika 6102",
                    "url" : "https://dessinsdrummond.com/plan/nordika-moderne-rustique-1003289",
                    "dim" : (32,30)
                }
        }
    },
    {
        "1": {
                "1": {
                    "x": 12,
                    "y": 13,
                    "min_area": 90,
                    "max_area": 2622,
                    "adj_ref": 1,
                    "type": "Bedroom",
                    "label": "bed1"
                },
                "2": {
                    "x": 12,
                    "y": 14,
                    "min_area": 90,
                    "max_area": 2622,
                    "adj_ref": 2,
                    "type": "Living",
                    "label": "living"
                },
                "3": {
                    "x": 12,
                    "y": 4,
                    "min_area": 50,
                    "max_area": 2622,
                    "adj_ref": 3,
                    "type": "Bathroom",
                    "label": "bath1"
                },
                "4": {
                    "x": 12,
                    "y": 14,
                    "min_area": 132,
                    "max_area": 2622,
                    "adj_ref": 4,
                    "type": "Kitchen",
                    "label": "kitchen"
                },
                "5": {
                    "x": 14,
                    "y": 9,
                    "min_area": 132,
                    "max_area": 2622,
                    "adj_ref": 5,
                    "type": "entrance",
                    "label": "entry"
                },
                "6": {
                    "x": 12,
                    "y": 10,
                    "min_area": 90,
                    "max_area": 2622,
                    "adj_ref": 6,
                    "type": "Bedroom",
                    "label": "bed2"
                },
                "7": {
                    "x": 10,
                    "y": 9,
                    "min_area": 90,
                    "max_area": 2622,
                    "adj_ref": 7,
                    "type": "Bedroom",
                    "label": "bed3"
                },
                "8": {
                    "x": 7,
                    "y": 3,
                    "min_area": 90,
                    "max_area": 2622,
                    "adj_ref": 8,
                    "type": "Bathroom",
                    "label": "bath2"
                },
                "9": {
                    "x": 7,
                    "y": 5,
                    "min_area": 90,
                    "max_area": 2622,
                    "adj_ref": 9,
                    "type": "Bathroom",
                    "label": "laudry"
                },
                "10": {
                    "x": 11,
                    "y": 14,
                    "min_area": 90,
                    "max_area": 2622,
                    "adj_ref": 10,
                    "type": "dining",
                    "label": "dining"
                },
                "11": {
                    "x": 24,
                    "y": 20,
                    "min_area": 90,
                    "max_area": 2622,
                    "adj_ref": 11,
                    "type": "garage",
                    "label": "garage"
                },
                "12": {
                    "x": 15,
                    "y": 4,
                    "min_area": 90,
                    "max_area": 2622,
                    "adj_ref": 12,
                    "type": "corridor",
                    "label": "cor."
                },
                "adjs": [(1,3),(3,4),(10,4),(2,10),(7,8), (7,6), (5,9), (11,9), (5,11), (12,5), (12,4), (12,8), (12,6), (12,9)],
                "adj_ban": [(4,1), (4,7), (4,6)],
                "info": {
                    "name" : "Hygge 3286",
                    "url" : "https://dessinsdrummond.com/plan/hygge-scandinave-1003315",
                    "dim" : (64,49)
                }
        }
    },
]


#json.dumps(multikeys, indent=4)

with open('input_plans_01.json', 'w', encoding='utf-8') as f:
    json.dump(test_data, f, ensure_ascii=False, indent=4)
