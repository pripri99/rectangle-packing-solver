import rectangle_packing_solver as rps
import random

# Define a problem
'''problem = rps.Problem(rectangles=[
    [4, 6],  # Format: [width, height] as list. Default rotatable: False
    (4, 4),  # Format: (width, height) as tuple. Default rotatable: False
    {"width": 2.1, "height": 3.2, "rotatable": False},  # Or can be defined as dict.
    {"width": 1, "height": 5, "rotatable": True},
])'''
problem = rps.Problem(rectangles=[
    {"width": 10, "height": 11, "rotatable": True, "label":"bed1"},  # Or can be defined as dict.
    {"width": 12, "height": 8, "rotatable": True, "label":"bed2"},
    {"width": 8, "height": 5, "rotatable": True, "label":"bath"},
    {"width": 10, "height": 10, "rotatable": True, "label":"kitchen"},
    {"width": 12, "height": 10, "rotatable": True, "label":"living"},
])
print("problem:", problem)
seeds = [random.randint(0, 999999) for i in range(0,100)]
for i in range(0,3):
    index = random.randint(0, len(seeds)-1)
    # Find a solution
    print("\n=== Solving without width/height constraints ===")
    solution = rps.Solver().solve(problem=problem)
    print("solution:", solution)
    image_path = "./test_output/noLimit/floorplan"+ str(i)+".png"
    # Visualization (to floorplan.png)
    rps.Visualizer().visualize(solution=solution, path=image_path)

    # [Other Usages]
    # We can also give a solution width (and/or height) limit, as well as progress bar and random seed
    print("\n=== Solving with width/height constraints ===")
    h = random.randint(20,50)
    w = random.randint(20,50)

    solution = rps.Solver().solve(problem=problem, height_limit=h, width_limit=w, show_progress=True, seed=seeds[index])
    print("solution:", solution)
    image_path = "./test_output/floorplan_seed"+ str(seeds[index])+"_hxw_"+ str(h)+"x"+str(w)+".png"
    rps.Visualizer().visualize(solution=solution, path=image_path)