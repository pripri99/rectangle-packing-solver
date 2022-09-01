import rectangle_packing_solver as rps
import random
import json
from pathlib import Path

# Define a problem
'''problem = rps.Problem(rectangles=[
    [4, 6],  # Format: [width, height] as list. Default rotatable: False
    (4, 4),  # Format: (width, height) as tuple. Default rotatable: False
    {"width": 2.1, "height": 3.2, "rotatable": False},  # Or can be defined as dict.
    {"width": 1, "height": 5, "rotatable": True},
])
problem = rps.Problem(rectangles=[
    {"width": 10, "height": 11, "rotatable": True, "type":"bedroom", "label":"bed1"},  # Or can be defined as dict.
    {"width": 12, "height": 8, "rotatable": True, "type":"bedroom", "label":"bed2"},
    {"width": 8, "height": 5, "rotatable": True, "type":"bathroom", "label":"bath"},
    {"width": 10, "height": 10, "rotatable": True, "type":"kitchen", "label":"kitchen"},
    {"width": 12, "height": 10, "rotatable": True, "type":"living", "label":"living"},
    {"width": 4, "height": 10, "rotatable": True, "type":"corridor", "label":"cor1"},
])'''
problem = rps.Problem(rectangles=[
    {"width": 4, "height": 18, "rotatable": True, "type":"corridor", "label":"cor1"},
    {"width": 10, "height": 11, "rotatable": True, "type":"bedroom", "label":"bed2"},  # Or can be defined as dict.
    {"width": 8, "height": 11, "rotatable": True, "type":"bathroom", "label":"bath"},
    {"width": 13, "height": 13, "rotatable": True, "type":"bedroom", "label":"bed1"},
    {"width": 10, "height": 11, "rotatable": True, "type":"kitchen", "label":"kitchen"},
    {"width": 10, "height": 12, "rotatable": True, "type":"dining", "label":"dining"},
    {"width": 12, "height": 14, "rotatable": True, "type":"living", "label":"living"},
    {"width": 6, "height": 8, "rotatable": True, "type":"entrance", "label":"entry"},
    
])
problem = rps.Problem(rectangles=[
    {"width": 14, "height": 15, "rotatable": True, "type":"kitchen", "label":"kitchen"},
    {"width": 16, "height": 17, "rotatable": True, "type":"dining", "label":"dining"},
    {"width": 24, "height": 33, "rotatable": True, "type":"living", "label":"living"},
    {"width": 14, "height": 11, "rotatable": True, "type":"entrance", "label":"entry"},
    {"width": 4, "height": 8, "rotatable": True, "type":"bathroom", "label":"bath2"},
    {"width": 19, "height": 18, "rotatable": True, "type":"bedroom", "label":"suite"},
    {"width": 11, "height": 11, "rotatable": True, "type":"bedroom", "label":"bed1"},
    {"width": 11, "height": 11, "rotatable": True, "type":"bedroom", "label":"bed2"},
    {"width": 33, "height": 25, "rotatable": True, "type":"garage", "label":"garage"},
    {"width": 11, "height": 10, "rotatable": True, "type":"bathroom", "label":"buanderie"},
    {"width": 14, "height": 11, "rotatable": True, "type":"dining", "label":"dining2"},
    {"width": 17, "height": 18, "rotatable": True, "type":"living", "label":"family room"},
    {"width": 12, "height": 12, "rotatable": True, "type":"corridor", "label":"bureau"},
    {"width": 4, "height": 8, "rotatable": True, "type":"bathroom", "label":"bath1"},
       
])

f = open('input_plans_01.json')
data = json.load(f)
data_num = random.randint(0, len(data)-1)
data_num = 0
plan_rooms = []
plan_width = data[data_num]["1"]["info"]["dim"][0]
plan_height = data[data_num]["1"]["info"]["dim"][1]
for key in data[data_num]["1"]:
    if key not in ["adjs", "adj_ban", "info", "land", "envelope"]:
        room = data[data_num]["1"][key]
        room_data = {"width": room["x"], "height": room["y"], "rotatable": True, "type":room["type"].lower(), "label":room["label"].lower()}
        plan_rooms.append(room_data)
        #print(key)
problem = rps.Problem(rectangles=plan_rooms)

print("problem:", problem)
seeds = [random.randint(0, 999999) for i in range(0,100)]
plan_name = data[data_num]["1"]["info"]["name"]
#all_adjs = [[(0,10), (0,1), (8,10), (3,1), (3,12)], [(3,1), (3,12), (3,2), (2,5), (2,11), (6,4), (7,13)], [(8,9), (5,12), (2,12)]]
DIR = plan_name+"_plan_"+ str(data_num) + "_"+ str(len(problem.rectangles))+"rooms"
Path("./test_output/"+DIR).mkdir(parents=True, exist_ok=True)
complete_path = "./test_output/"+DIR
for i in range(0,1):
    adj_list = [(e[0]-1, e[1]-1) for e in data[data_num]["1"]["adjs"]] #random.choice(all_adjs)
    banned_adjs = data[data_num]["1"]["adj_ban"] #[(0,4), (0,13), (0,5)]
    adj_info = [[p for p in adj_list],banned_adjs]
    index = random.randint(0, len(seeds)-1)
    # Find a solution
    print("\n=== Solving without width/height constraints ===")
    solution = rps.Solver().solve(problem=problem, adj= adj_info,show_progress=True)
    print("solution:", solution)
    image_path = complete_path+"/floorplan_noLimit_"+ str(i)+".png"
    # Visualization (to floorplan.png)
    rps.Visualizer().visualize(solution=solution, path=image_path)
    print("INPUT ADJ:", adj_list)
    #continue

    # [Other Usages]
    # We can also give a solution width (and/or height) limit, as well as progress bar and random seed
    print("\n=== Solving with width/height constraints ===")
    h = random.randint(plan_height, plan_height+5)
    w = random.randint(plan_width,plan_width+5)
    adj_info = [[p for p in adj_list],banned_adjs]

    solution = rps.Solver().solve(problem=problem, height_limit=h, width_limit=w, show_progress=True, seed=seeds[index], adj= adj_info.copy())
    print("solution:", solution)
    image_path = complete_path+"/floorplan_seed"+ str(seeds[index])+"_hxw_"+ str(h)+"x"+str(w)+".png"
    rps.Visualizer().visualize(solution=solution, path=image_path)
    print("INPUT ADJ:", adj_list)