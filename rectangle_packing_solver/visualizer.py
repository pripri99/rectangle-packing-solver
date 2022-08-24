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

from .solution import Solution
import numpy as np
import math


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
        fig = plt.figure(figsize=(10, 10 * bb_height / bb_width + 0.5))
        ax = plt.axes()
        ax.set_aspect("equal")
        plt.xlim([0, bb_width])
        plt.ylim([0, bb_height])
        plt.xlabel("X")
        plt.ylabel("Y")
        #plt.title(title)

        # Plot every rectangle
        for i, rectangle in enumerate(positions):
            color, fontcolor = self.dict_room_color[rectangle["room_type"].lower()], "#ffffff"
            #print("COLOR FONTCOLOR:",color, fontcolor)
            c = [val/255 for val in color]
            color = (c[0],c[1],c[2], 1.0)
            
            #print("COLOR FONTCOLOR:",color, fontcolor)
            r = patches.Rectangle(
                xy=(rectangle["x"], rectangle["y"]),
                width=rectangle["width"],
                height=rectangle["height"],
                edgecolor="#000000",
                facecolor=color,
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
        plt.axis('off')
        # Output
        if path is None:
            plt.show()
        else:
            fig.savefig(path)

        plt.close()
    @classmethod
    def find_contour(self, all_rectangle):
        all_line = []
        return all_line
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
            tmp = xyto[1] + abs(xyto[0]-xyfrom[0])*0.05
            xyfrom = (xyfrom[0], tmp)
            xyto = (xyto[0], tmp)
            #offeset_y = abs(xyto[0]-xyfrom[0])*0.5
            #print("offset:", offeset_y)
            #offeset_x = 0

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
