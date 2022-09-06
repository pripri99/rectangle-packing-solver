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

import graphlib
import random
from .utility import segments_distance
from typing import Any, Dict, List, Optional, Tuple
from xmlrpc.client import Boolean

from .floorplan import Floorplan
from .problem import Problem


class ObliqueGrid:
    def __init__(self, grid: List[List[int]], coordinates: List[Dict]) -> None:
        self.grid = grid
        self.coordinates = coordinates


class SequencePair:
    """
    A class of Sequence-Pair.
    """

    def __init__(self, pair: Tuple[List, List] = ([], [])) -> None:
        if not isinstance(pair, tuple):
            raise TypeError("Invalid argument: 'pair' must be a tuple.")
        if len(pair) != 2:
            raise ValueError("Invalid argument: Length of 'pair' must be two.")

        self.pair = pair
        self.gp = pair[0]  # G_{+}
        self.gn = pair[1]  # G_{-}

        if len(self.gp) != len(self.gn):
            raise ValueError("Lists in the pair must be the same length.")
        self.n = len(self.gp)

        self.oblique_grid = self.pair_to_obliquegrid(pair=self.pair)

    def decode(self, problem: Problem, rotations: Optional[List] = None, adjacency: Optional[List] = [[],[]], display: Optional[Boolean] = False) -> Floorplan:
        """
        Decode:
            Based on the sequence pair and the problem with rotations information, calculate a floorplan
            (bounding box, area, and rectangle positions).
        """

        if not isinstance(problem, Problem):
            raise TypeError("Invalid argument: 'problem' must be an instance of Problem.")

        if problem.n != self.n:
            raise ValueError("'problem.n' must be the same as the sequence-pair length.")

        if rotations is not None:
            if len(rotations) != self.n:
                raise ValueError("'rotations' length must be the same as the sequence-pair length.")

        coords = self.oblique_grid.coordinates

        # Width and height dealing with rotations
        width_wrot = []
        height_wrot = []
        all_label = []
        all_r_type = []
        for i in range(self.n):
            w_range = random.randint(-2,2)
            h_range = random.randint(-2,2)
            all_label.append(problem.rectangles[i]["label"])
            all_r_type.append(problem.rectangles[i]["room_type"])
            if (rotations is None) or (rotations[i] % 2 == 0):
                # no rotation
                width_wrot.append(problem.rectangles[i]["width"]+w_range)
                height_wrot.append(problem.rectangles[i]["height"]+h_range)
            else:
                # with rotation
                assert problem.rectangles[i]["rotatable"]
                width_wrot.append(problem.rectangles[i]["height"]+h_range)
                height_wrot.append(problem.rectangles[i]["width"]+w_range)

        # Calculate the longest path in the "Horizontal Constraint Graph" (G_h)
        # This time complexity is O(n^2), may be optimized...
        graph_h: Dict[int, List] = {i: [] for i in range(self.n)}
        for i in range(self.n):
            for j in range(self.n):
                # When j is right of i, set an edge from j to i
                if (coords[i]["a"] < coords[j]["a"]) and (coords[i]["b"] < coords[j]["b"]):
                    graph_h[j].append(i)

        # Topological order of DAG (G_h)
        topo_h = graphlib.TopologicalSorter(graph_h)
        torder_h = list(topo_h.static_order())

        # Calculate W (bounding box width) from G_h
        dist_h = [width_wrot[i] for i in range(self.n)]
        for i in torder_h:
            dist_h[i] += max([dist_h[e] for e in graph_h[i]], default=0)
        bb_width = max(dist_h)

        # Calculate the longest path in the "Vertical Constraint Graph" (G_v)
        # This time complexity is O(n^2), may be optimized...
        graph_v: Dict[int, List] = {i: [] for i in range(self.n)}
        for i in range(self.n):
            for j in range(self.n):
                # When j is above i, set an edge from j to i
                if (coords[i]["a"] > coords[j]["a"]) and (coords[i]["b"] < coords[j]["b"]):
                    graph_v[j].append(i)

        # Topological order of DAG (G_v)
        topo_v = graphlib.TopologicalSorter(graph_v)
        torder_v = list(topo_v.static_order())

        # Calculate H (bounding box height) from G_v
        dist_v = [height_wrot[i] for i in range(self.n)]
        for i in torder_v:
            dist_v[i] += max([dist_v[e] for e in graph_v[i]], default=0)
        bb_height = max(dist_v)

        # Calculate bottom-left positions
        positions = []
        for i in range(self.n):
            positions.append(
                {
                    "id": i,
                    "x": dist_h[i] - width_wrot[i],  # distance from left edge
                    "y": dist_v[i] - height_wrot[i],  # distande from bottom edge
                    "width": width_wrot[i],
                    "height": height_wrot[i],
                    "room_type":all_r_type[i],
                    "label": all_label[i],
                }
            )
        penalty = self.adjacency_penalty(positions=positions, adjacency=adjacency, display=display)
        small_gap = self.gap_count(positions=positions, limit=3, display=display)
        penalty = penalty + small_gap*6
        #area = -3 if penalty > 0 else -1


        return Floorplan(bounding_box=(bb_width, bb_height), positions=positions, penalty=penalty)
    @classmethod
    def adjacency_penalty(self, positions: List[Dict], adjacency: List, display: Optional[Boolean]= False) -> int:
        """
        Count valid adjs (and/or invalid adjs) and assign cost to it
        """
        
        adj_list = []
        adj_name = []
        for room in positions:
            x_min = room["x"]
            x_max = room["x"] + room["width"]
            y_min = room["y"]
            y_max = room["y"] + room["height"]
            top_left = (room["x"], room["y"] + room["height"])
            bottom_right = (room["x"] + room["width"], room["y"])
            corners = [(x_min, y_min),(x_min, y_max),(x_max, y_max),(x_max, y_min)]
            for room2 in positions:
                if room2["id"] != room["id"]:
                    tl = (room2["x"], room2["y"] + room2["height"])
                    br = (room2["x"] + room2["width"], room2["y"])
                    if self.check_overlap(rect1=[top_left,bottom_right],rect2=[tl,br]) == True:
                        pair = (room["id"], room2["id"])
                        if pair not in adj_list and pair[::-1] not in adj_list:
                            adj_list.append(pair)
                            adj_name.append([(room["label"], room2["label"])])

            
        if display == True: print("ADJS LIST:", adj_list, "ADJS Names:", adj_name)
        penalty = -6
        wanted_adj, banned_adj = adjacency
        for edge in wanted_adj:
            if edge not in adj_list and edge[::-1] not in adj_list:
                penalty = penalty + 6
            if edge in adj_list and edge[::-1] in adj_list:
                penalty = penalty - 6
        for edge in banned_adj:
            if edge in adj_list or edge[::-1] in adj_list:
                penalty = penalty + 12
        '''for edge in adj_list:
            if edge not in wanted_adj and edge[::-1] not in wanted_adj:
                penalty = penalty + 1
        '''
        return penalty
    @classmethod
    def gap_count(self, positions: List[Dict], limit: int = 3, display: Optional[Boolean]= False) -> int:
        """
        Count small gaps in the plan
        """
        n_gap = 0
        done = []
        for room in positions:
            a = (room["x"], room["y"])
            b = (room["x"], room["y"] + room["height"])
            c = (room["x"] + room["width"], room["y"] + room["height"])
            d = (room["x"] + room["width"], room["y"])
            all_sides = [[a,b], [b,c], [c,d], [d,a]]
            for room2 in positions:
                if room2["id"] != room["id"]:
                    a = (room2["x"], room2["y"])
                    b = (room2["x"], room2["y"] + room2["height"])
                    c = (room2["x"] + room2["width"], room2["y"] + room2["height"])
                    d = (room2["x"] + room2["width"], room2["y"])
                    all_sides_r2 = [[a,b], [b,c], [c,d], [d,a]]

                    for s1 in all_sides:
                        for s2 in all_sides_r2:
                            #print("segments:",[s1,s2])
                            d = segments_distance(s1[0][0], s1[0][1], s1[1][0], s1[1][1], s2[0][0], s2[0][1], s2[1][0], s2[1][1])
                            if [s1,s2] not in done and d > 0  and d <= limit:
                                n_gap += 1
                                done += [[s1,s2],[s2,s1]]
        if display: print("Number of gaps:", n_gap)
        return n_gap
    @classmethod
    def check_overlap(cls, rect1: List, rect2: List) -> Boolean:
        tl1, br1 = rect1
        tl2, br2 = rect2

        # if rectangle has area 0, no overlap
        if tl1[0] == br1[0] or tl1[1] == br1[1] or br2[0] == tl2[0] or tl2[1] == br2[1]:
            return False
        
        # If one rectangle is on left side of other
        if tl1[0] > br2[0] or tl2[0] > br1[0]:
            return False
    
        # If one rectangle is above other
        if br1[1] > tl2[1] or br2[1] > tl1[1]:
            return False

        return True

    def encode(self) -> None:
        """
        Encode:
            TODO
        """
        raise NotImplementedError()

    def __repr__(self) -> str:
        return "SequencePair(" + str(self.pair) + ")"

    @classmethod
    def pair_to_obliquegrid(cls, pair: Tuple[List, List]) -> ObliqueGrid:
        """
        Convert a Sequence-pair (a tuple of G_{+} and G_{-}) to Oblique-grid.
        """

        n = len(pair[0])
        gp = pair[0]
        gn = pair[1]

        # Oblique grid is basically an n x n 2d array
        grid = [[-1 for _ in range(n)] for _ in range(n)]
        coordinates = [{"a": -1, "b": -1} for _ in range(n)]

        # This time complexity is O(n^2), may be optimized...
        for i in range(n):
            index_p = gp.index(i)
            index_n = gn.index(i)
            grid[index_p][index_n] = i
            coordinates[i] = {"a": index_p, "b": index_n}

        return ObliqueGrid(grid=grid, coordinates=coordinates)

    @classmethod
    def obliquegrid_to_pair(cls, oblique_grid: ObliqueGrid) -> Tuple[List, List]:
        """
        Convert an Oblique-grid to Sequence-pair (a tuple of G_{+} and G_{-}).
        """

        n = len(oblique_grid.grid)
        gp = [-1 for _ in range(n)]  # G_{+}
        gn = [-1 for _ in range(n)]  # G_{-}

        # This time complexity is O(n^2), may be optimized...
        for x in range(n):
            for y in range(n):
                rectangle_id = oblique_grid.grid[x][y]
                if rectangle_id != -1:
                    gp[x] = rectangle_id
                    gn[y] = rectangle_id

        return (gp, gn)

    ################################################################
    # Operators
    ################################################################

    def __eq__(self, other: Any) -> Any:
        return self.pair == other.pair

    def __ne__(self, other: Any) -> Any:
        return not self.__eq__(other)
