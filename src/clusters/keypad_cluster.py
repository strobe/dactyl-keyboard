
# from clusters.default_cluster import DefaultCluster
from clusters.trackball_orbyl import TrackballOrbyl
import json
import os
from key import Key, KeyFactory as KF
from common import *
from trackball import TrackballPart

keys = [
        ["MX", "MX", "MX", "MX"],
        ["MX", None, None, "MX"],
        ["MX", None, None, "MX"],
        ["MX", "MX", "MX", "MX"]
    ]

class KeypadCluster(TrackballOrbyl):
    @staticmethod
    def name():
        return "KEYPAD_CLUSTER"

    def __init__(self, parent_locals):
        super().__init__(parent_locals)
        self.locals = parent_locals
        for item in parent_locals:
            globals()[item] = parent_locals[item]
        self.is_tb = True
        self.build_cluster_keys()

    def track_place(self, shape, offsets=(0, 0, 0)):
        pos, rot = self.position_rotation()
        pos = combine(pos, offsets)
        shape = rotate(shape, rot)
        shape = translate(shape, pos)
        return shape

    def build_cluster_keys(self):

        vert_off = keyswitch_height + 8
        horiz_off = keyswitch_width + 8

        c_pos, _ = self.position_rotation()
        c_rot = [5, 5, 5]
        c_pos[0] -= 32
        c_pos[1] += 32

        for row in range(len(keys)):
            for col in range(len(keys[row])):
                val = keys[row][col]
                if val is not None:
                    key = KF.new_key_by_row_column(row, col, self.locals)
                    key.pos = [horiz_off * col, -vert_off * row, 0]
                    key.update_pos_rot(c_pos, c_rot)
                    keys[row][col] = key
                else:
                    keys[row][col] = KF.NONE_KEY

        KF.build_neighbors(keys)

    # def build_keys(self):
    #     origin = [0, 0, 0]
    #     vert_off = keyswitch_height + 7
    #     horiz_off = keyswitch_width + 7
    #     off_x = 5
    #     top_y = -10
    #
    #     c_pos, c_rot = self.position_rotation()
    #
    #     z_inc = 5
    #     last_key = None
    #     for i in range(3):
    #         key = KF.new_key(str(i), self.locals)
    #         off_y = top_y - (vert_off * i)
    #         key.pos = (origin[0] + off_x, origin[1] + off_y, 0)
    #         key.rot = (20, 0, 10)
    #         key.add_wall("right")
    #
    #         key.update_pos_rot(c_pos, c_rot)
    #
    #         if last_key is not None:
    #             key.add_neighbor(last_key.get_id(), "t")
    #             key.add_neighbor("wall", "r")
    #             last_key.add_neighbor(key.get_id(), "b")
    #
    #         if i == 2:
    #             key.add_neighbor("wall", "b")
    #             key.add_neighbor("corner", "br")
    #
    #         last_key = key
    #
    #     off_y = top_y - (2 * vert_off)
    #     left_most_x = off_x - (3 * horiz_off)
    #
    #     for i in range(3):
    #         key = KF.new_key(str(i + 3), self.locals)
    #         off_x = left_most_x + (i * horiz_off)
    #         key.pos = (origin[0] + off_x, origin[1] + off_y, 0)
    #         key.rot = (20, 0, 10)
    #         key.add_neighbor("wall", "b")
    #         if i == 0:
    #             key.add_neighbor("wall", "l")
    #
    #         last_key = add_neighbor(key, last_key)
    #         key.update_pos_rot(c_pos, c_rot)
    #
    #     height = 2 * z_inc
    #     off_x = left_most_x + (2 * horiz_off)
    #     off_y += vert_off
    #     for i in range(2):
    #         key = KF.new_key(str(i + 6), self.locals)
    #         off_y = off_y + (vert_off * i)
    #         key.pos = (origin[0] + off_x, origin[1] + off_y, 0)
    #         key.rot = (20, 0, 10)
    #         key.add_wall("left")
    #         last_key = add_neighbor(key, last_key)
    #         key.update_pos_rot(c_pos, c_rot)

    def thumbcaps(self, side="right"):
        return self.thumb_1x_layout(sa_cap(1), True)

    def thumb_1x_layout(self, shape, cap=False):
        shapes = []
        for r in range(len(keys)):
            for c in range(len(keys[r])):
                key = KF.get_key_by_id(KF.get_rc_id(r, c))
                if not key.is_none():
                    shapes.append(key.render(None, cap))

        return union(shapes)

    def thumb_15x_layout(self, shape, cap=False, plate=True):
        return []

    def build_corner(self, part, facing, corner_type):
        return []

    def build_wall(self, part, facing):
        return []

    def get_join(self, part, neighb):
        for k in neighb.neighbors:
            v = neighb.neighbors[k]
            if v is part:
                return k

        return None

    def get_points(self, part1, side1, part2, side2):
        side_points = {
            "t": ["tl", "tr"],
            "b": ["bl", "br"],
            "l": ["tl", "bl"],
            "r": ["tr", "br"],
            "tl": ["tl"],
            "bl": ["bl"],
            "tr": ["tr"],
            "br": ["br"]
        }

        sp1 = [part1.get_point_at(x, off=(0, 0, 3)) for x in side_points[side1]]
        sp2 = [part2.get_point_at(x, off=(0, 0, 3)) for x in side_points[side2]]

        return [
            hull_from_points(sp1 + sp2),
            # hull_from_points([
            #     part2.get_point_at(sp2[0]),
            #     part1.get_point_at(sp1[1]),
            #     part2.get_point_at(sp2[2])
            # ])
        ]

    def get_connection(self, part, side, neighb):
        neighb_side = self.get_join(part, neighb)
        points = self.get_points(part, side, neighb, neighb_side)

        return hull_from_points(points)

    def thumb_connectors(self, side="right"):
        processed = {}
        hulls = []
        for r in range(len(keys)):
            for c in range(len(keys[r])):
                key = KF.get_key_by_row_col(r, c)
                if key.get_id() not in processed.keys():
                    processed[key.get_id()] = []
                if not key.is_none():
                    for side in key.neighbors:
                        neighb = key.neighbors[side]
                        if side in processed[key.get_id()]:
                            continue
                        if neighb in ["inner_corner", "outer_corner"]:
                            pass
                            # hulls.append(union(self.build_corner(key, side, neighb)))
                        elif neighb == "wall":
                            pass
                            # hulls.append(union(self.build_wall(key, side)))
                        else:
                            if neighb.get_id() not in processed.keys():
                                processed[neighb.get_id()] = []
                            neighb_side = self.get_join(key, neighb)
                            points = self.get_points(key, side, neighb, neighb_side)
                            # hull = hull_from_points(points)
                            hulls = hulls + points
                            processed[neighb.get_id()].append(neighb_side)
                            processed[key.get_id()].append(side)
        # spheres = []
        # for point in hulls:
        #     spheres.append(translate(sphere(2), point))

        return union(hulls)

    def walls(self, side="right"):
        return []

    def connection(self, side="right"):
        return []

    # def thumb(self, side="right"):
    #     return []



