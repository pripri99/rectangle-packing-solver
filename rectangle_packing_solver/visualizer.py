# Copyright 2022 Kotaro Terada
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Tuple

import matplotlib.patches as patches
from matplotlib import pylab as plt
from matplotlib import collections as mc

from .solution import Solution
import numpy as np
import math
from scipy.spatial import ConvexHull
import random
from shapely.geometry import LineString
from shapely.ops import polygonize


class Visualizer:
    """
    A floorplan visualizer.
    """

    def __init__(self) -> None:
        # Default font size is 12
        plt.rcParams["font.size"] = 14
        self.dict_room_color = {
                        'bathroom': (31, 119, 180),
                        'bedroom': (44, 160, 44),
                        'border': (0, 0, 0),
                        'dining': (214, 39, 40),
                        'entrance': (227, 119, 194),
                        'garage': (140, 86, 75),
                        'kitchen': (148, 103, 189),
                        'living': (255, 127, 14),
                        'stair': (188, 189, 34),
                        'corridor': (247,163,10),
                        'extra': (211,212,212),
                        }

    def visualize(self, solution: Solution, path: str = "floorplan.png", title: str = "Floorplan") -> None:
        if not isinstance(solution, Solution):
            raise TypeError("Invalid argument: 'solution' must be an instance of Solution.")

        positions = solution.floorplan.positions
        bounding_box = solution.floorplan.bounding_box

        # Figure settings
        bb_width = bounding_box[0]
        bb_height = bounding_box[1]
        fig = plt.figure(figsize=(10, 10 * bb_height / bb_width + 2))
        ax = plt.axes()
        ax.set_aspect("equal")
        plt.xlim([-1, bb_width+1])
        plt.ylim([-1, bb_height+1])
        #plt.xlabel("X")
        #plt.ylabel("Y")
        #plt.title(title)

        r = patches.Rectangle(
                xy=(-1, -1),
                width=bounding_box[0]+2,
                height=bounding_box[1]+2,
                edgecolor="#000000",
                facecolor="#ffffff",
                alpha=1.0,
                fill=True,
            )
        ax.add_patch(r)


        #add outside walls
        contour = self.find_contour(positions)
        outside_walls = None #polygon with largest aread
        max_area = 0
        #self.find_loops(contour)
        for pol in list(polygonize(contour)):
            print("pol:", pol, "area:", pol.area)
            if pol.area > max_area: 
                max_area = pol.area
                outside_walls = pol
            #plt.plot(*pol.exterior.xy)
            color= self.dict_room_color["corridor"]
            c = [val/255 for val in color]
            color = (c[0],c[1],c[2], 1.0)
            patch = patches.Polygon(np.array(pol.exterior.xy).T, fc=color)
            ax.add_patch(patch)

        #points = np.array([p for rect in positions for p in self.get_points(rect)])
        #hull = ConvexHull(points)
        print("contour:", contour)
        # print(lines)

        #c = [(random.randint(0,255), random.randint(0,255), random.randint(0,255)) for line in contour]
        #c = [(0,0,0) for line in contour]

        #lc = mc.LineCollection(contour, colors=c, linewidths=3)
        #ax.add_collection(lc)

        ordered_positions = []
        for rect in positions:
            if rect["room_type"].lower() not in ["bedroom", "bathroom", "garage"]:
                ordered_positions.append(rect)
        for rect in positions:
            if rect["room_type"].lower() in ["bedroom", "bathroom", "garage"]:
                ordered_positions.append(rect)
        

        # Plot every rectangle
        for i, rectangle in enumerate(ordered_positions):
            color, fontcolor = self.dict_room_color[rectangle["room_type"].lower()], "#000000"
            #print("COLOR FONTCOLOR:",color, fontcolor)
            c = [val/255 for val in color]
            color = (c[0],c[1],c[2], 1.0)
            thicc = 0

            color_for_edge = color
            if rectangle["room_type"].lower() in ["bedroom", "bathroom", "garage"]:
                color_for_edge = "#000000"
                thicc = 4
            #print("COLOR FONTCOLOR:",color, fontcolor)
            r = patches.Rectangle(
                xy=(rectangle["x"], rectangle["y"]),
                width=rectangle["width"],
                height=rectangle["height"],
                edgecolor=color_for_edge,
                facecolor=color,
                lw = thicc,
                alpha=1.0,
                fill=True,
            )
            ax.add_patch(r)

            # Add text label
            centering_offset = 0.011
            center_x = rectangle["x"] + rectangle["width"] / 2 - bb_width * centering_offset
            center_y = rectangle["y"] + rectangle["height"] / 2 - bb_height * centering_offset
            ax.text(x=center_x, y=center_y, s=rectangle["label"], fontsize=18, color=fontcolor) #change id to label for s

            # Add dimension lines
            side = [(rectangle["x"], rectangle["y"]), (rectangle["x"]+rectangle["width"], rectangle["y"])]
            #print("side:", side, side[0], side[1])
            self.annotate_dim(ax, side[0], side[1])
            side = [(rectangle["x"], rectangle["y"]), (rectangle["x"], rectangle["y"]+rectangle["height"])]
            #print("side:", side)
            self.annotate_dim(ax, side[0], side[1])
        
        if outside_walls != None:
            patch = patches.Polygon(np.array(outside_walls.exterior.xy).T, ec="#000000", lw=10, fill=False)
            ax.add_patch(patch)

        plt.axis('off')
        # Output
        if path is None:
            plt.show()
        else:
            fig.savefig(path)

        plt.close()
    @classmethod
    def find_loops(self, all_line):
        all_loops = []
        while len(all_line) > 0:
            loop = [random.choice(all_line)]
        print("all loops", all_loops)
        return all_loops


    @classmethod
    def find_contour(self, all_rectangle):
        all_lines = []
        points = [p for rect in all_rectangle for p in self.get_points(rect)]
        #hull = ConvexHull(points)
        # get all sides rectangle
        for rect in all_rectangle:
            p = self.get_points(rect)
            all_side = [[p[0],p[1]],[p[1],p[2]],[p[2],p[3]],[p[3],p[0]]]
            all_lines += all_side
        # lines that are not rectangle sides
        extra_lines = []
        for p1 in points:
            for p2 in points:
                if p1 != p2:
                    if p1[0]==p2[0] or p1[1]==p2[1]:
                        if [p1,p2] not in all_lines and [p2,p1] not in all_lines:
                            all_lines.append([p1,p2])
                            extra_lines.append([p1,p2])
        
        line_use = {}
        for line in all_lines:
            line_use[tuple(line)] = 0
            for rect in all_rectangle:
                p = self.get_points(rect)
                all_side = [[p[0],p[1]],[p[1],p[2]],[p[2],p[3]],[p[3],p[0]]]
                for side in all_side:
                    l1 = LineString(line)
                    l2 = LineString(side)
                    if l1.crosses(l2) or l1.covers(l2) or l2.crosses(l1) or l2.covers(l1) or l1.overlaps(l2) or l2.overlaps(l1) : 
                        if line_use[tuple(line)]  == 6 :
                            print(line, "in",  side)
                        line_use[tuple(line)] += 1
                        break #only one side can overlap
        
        bad_lines = []
        for line in line_use:
            if line_use[tuple(line)] == 0:
                bad_lines.append([line[0], line[1]])
        
        outside_lines = []
        for line in line_use:
            if line_use[tuple(line)] == 1:
                touch = False
                for extra_line in bad_lines:
                    l1 = LineString(line)
                    l2 = LineString(extra_line)
                    if l1.covers(LineString(l2)) or l2.covers(LineString(l1)): 
                        touch = True
                        break
                #print(line)
                if touch == False: outside_lines.append([line[0], line[1]])
        #print("line use:", line_use)
        return outside_lines
    @classmethod
    def distance(self, a,b):
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
    @classmethod
    def is_between(self, a,c,b):
        return self.distance(a,c) + self.distance(c,b) == self.distance(a,b)
    @classmethod
    def are_overlapping(self, r, s):
        return r[1] >= s[0] and s[1] >= r[0]
    @classmethod
    def rect_contains_line(self, rect, line):
        p = self.get_points(rect)
        all_side = [[p[0],p[1]],[p[1],p[2]],[p[2],p[3]],[p[3],p[0]]]

        for side in all_side:
            if line[0] in side or self.is_between(side[0], line[0], side[1]):
                if (line[1] in side or self.is_between(side[0], line[1], side[1]) or self.is_between(line[0], side[0], line[1])
                or self.is_between(line[0], side[1], line[1])):
                    return True
            if line[1] in side or self.is_between(side[0], line[1], side[1]):
                if (line[0] in side or self.is_between(side[0], line[0], side[1]) or self.is_between(line[0], side[0], line[1])
                or self.is_between(line[0], side[1], line[1])):
                    return True

        return False
    @classmethod
    def get_points(self, rectangle):
        return [(rectangle["x"], rectangle["y"]), (rectangle["x"]+rectangle["width"], rectangle["y"]),
        (rectangle["x"]+rectangle["width"], rectangle["y"]+rectangle["height"]),
        (rectangle["x"], rectangle["y"]+rectangle["height"])]
    
    @classmethod
    def annotate_dim(self, ax, xyfrom, xyto, text=None):
        #print("xyfrom, xyto",xyfrom, xyto,)
        offeset_x = -1*abs(xyto[1]-xyfrom[1])*0.1
        offeset_y = 0
        # vertical line
        # if xyfrom[0] == xyto[0]:
        #     # move to right == increase x
        #     tmp = xyto[0] + 1
        #     xyfrom = (tmp, xyfrom[1])
        #     xyto = (tmp, xyto[1])
        # horizontal line
        if xyfrom[1] == xyto[1]:
            # move up == increase y
            tmp = xyto[1] + 1.3
            xyfrom = (xyfrom[0], tmp)
            xyto = (xyto[0], tmp)
            #offeset_y = abs(xyto[0]-xyfrom[0])*0.5
            #print("offset:", offeset_y)
            #offeset_x = 0
        # vertical line
        if xyfrom[0] == xyto[0]:
            # move left == increase x
            tmp = xyto[0] + 1.3
            xyfrom = (tmp, xyfrom[1])
            xyto = (tmp, xyto[1])

        if text is None:
            text = str(
                round(math.sqrt((xyfrom[0]-xyto[0])**2 + (xyfrom[1]-xyto[1])**2), 2))

        ax.annotate("", xyfrom, xyto, arrowprops=dict(arrowstyle='<->'))
        ax.text((xyto[0]+xyfrom[0])/2+offeset_x,
                (xyto[1]+xyfrom[1])/2+offeset_y, text, fontsize=12)

    @classmethod
    def get_color(cls, i: int = 0) -> Tuple[str, str]:
        """
        Gets rectangle face color (and its font color) from matplotlib cmap.
        """
        cmap = plt.get_cmap("tab10")
        color = cmap(i % cmap.N)
        brightness = max(color[0], color[1], color[2])

        if 0.85 < brightness:
            fontcolor = "#000000"
        else:
            fontcolor = "#ffffff"

        return (color, fontcolor)
