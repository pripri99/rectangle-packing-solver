import rectangle_packing_solver as rps
import random

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
print("problem:", problem)
seeds = [random.randint(0, 999999) for i in range(0,100)]
random_num = str(random.randint(0,99))
all_adjs = [[(4,5), (5,6)], [(0,1), (0,2), (0,3)]]
for i in range(0,3):
    adj_list = random.choice(all_adjs)
    banned_adjs = [(2,4)]
    adj_info = [[p for p in adj_list],banned_adjs]
    index = random.randint(0, len(seeds)-1)
    # Find a solution
    print("\n=== Solving without width/height constraints ===")
    solution = rps.Solver().solve(problem=problem, adj= adj_info)
    print("solution:", solution)
    image_path = "./test_output/noLimit/floorplan_"+random_num+"_"+ str(i)+".png"
    # Visualization (to floorplan.png)
    rps.Visualizer().visualize(solution=solution, path=image_path)
    print("INPUT ADJ:", adj_list)
    #continue

    # [Other Usages]
    # We can also give a solution width (and/or height) limit, as well as progress bar and random seed
    print("\n=== Solving with width/height constraints ===")
    h = random.randint(30,40)
    w = random.randint(41,51)
    adj_info = [[p for p in adj_list],banned_adjs]

    solution = rps.Solver().solve(problem=problem, height_limit=h, width_limit=w, show_progress=True, seed=seeds[index], adj= adj_info.copy())
    print("solution:", solution)
    image_path = "./test_output/floorplan_seed"+ str(seeds[index])+"_hxw_"+ str(h)+"x"+str(w)+".png"
    rps.Visualizer().visualize(solution=solution, path=image_path)
    print("INPUT ADJ:", adj_list)