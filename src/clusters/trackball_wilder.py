from clusters.default_cluster import DefaultCluster
from geom import *
from key import Key, KeyFactory
import json
import os
# from clusters.cluster_common import *


class TrackballWild(DefaultCluster):
    key_diameter = 75
    translation_offset = [
        0,
        0,
        10
    ]
    rotation_offset = [
        0,
        0,
        0
    ]
    key_translation_offsets = [
        0,
        0,
        10
    ]
    key_rotation_offsets = [
        0,
        0,
        0
    ]
    post_offsets = [
            [14, -8, 3],
            [3, -9, -7],
            [-4, 4, -6],
            [-5, 18, 19]
        ]

    tl_off = 1.7

    wall_offsets = [
        [
            -1.0,
            1.0,
            0.0
        ],
        [
            0.0,
            0.0,
            0.0
        ],
        [
            0.0,
            0.0,
            0.0
        ],
        [
            0.0,
            0.0,
            0.0
        ]
    ]

    @staticmethod
    def name():
        return "TRACKBALL_WILD"


    def get_config(self):
        with open(os.path.join("src", "clusters", "json", "TRACKBALL_WILD.json"), mode='r') as fid:
            data = json.load(fid)

        superdata = super().get_config()

        # overwrite any super variables with this class' needs
        for item in data:
            superdata[item] = data[item]

        for item in superdata:
            if not hasattr(self, str(item)):
                print(self.name() + ": NO MEMBER VARIABLE FOR " + str(item))
                continue
            setattr(self, str(item), superdata[item])

        return superdata

    def __init__(self, parent_locals):
        super().__init__(parent_locals)
        for item in parent_locals:
            globals()[item] = parent_locals[item]

    # def _key_gen(self):
    #     self._keys = {}
    #     for index in range(len(self.key_data)):
    #         data = self.key_data[index]
    #         key = KeyFactory.new_key(data['id'], globals())
    #         key.rot = data['rot']
    #         t_off = data['pos']
    #         key.pos = [t_off[0], t_off[1] + self.key_diameter / 2, t_off[2]]
    #         key.plate_rot_z = data['plate_rot_z']
    #         adjust_pos, adjust_rot = self.position_rotation()
    #         key.translate(adjust_pos)
    #         key.rotate_deg(adjust_rot)
    #         self._keys[key.get_id()] = key

    def position_rotation(self):
        rot = [10, -15, 5]
        pos = self.thumborigin()
        # Changes size based on key diameter around ball, shifting off of the top left cluster key.
        shift = [-.9*self.key_diameter/2+27-42, -.1*self.key_diameter/2+3-20, -5]
        for i in range(len(pos)):
            pos[i] = pos[i] + shift[i] + self.translation_offset[i]

        for i in range(len(rot)):
            rot[i] = rot[i] + self.rotation_offset[i]

        return pos, rot


    def tl_wall(self, shape):
        return translate(self.tl_place(shape), self.wall_offsets[0])

    def mr_wall(self, shape):
        return translate(self.mr_place(shape), self.wall_offsets[1])

    def br_wall(self, shape):
        return translate(self.br_place(shape), self.wall_offsets[2])

    def bl_wall(self, shape):
        return translate(self.bl_place(shape), self.wall_offsets[3])

    def _key_gen(self):
        self._keys = {}
        for index in range(len(self.key_data)):
            data = self.key_data[index]
            key = KeyFactory.new_key(data['id'], globals())
            key.rot = data['rot']
            t_off = data['pos']
            key.pos = [t_off[0], t_off[1] + self.key_diameter / 2, t_off[2]]
            key.plate_rot_z = data['plate_rot_z']
            adjust_pos, adjust_rot = self.position_rotation()
            key.translate(adjust_pos)
            key.rotate_deg(adjust_rot)
            self._keys[key.get_id()] = key

    #
    # def tl_place(self, shape):
    #     shape = rotate(shape, [0, 0, 0])
    #     t_off = self.key_translation_offsets[0]
    #     shape = rotate(shape, self.key_rotation_offsets[0])
    #     shape = translate(shape, (t_off[0], t_off[1]+self.key_diameter/2, t_off[2]))
    #     shape = rotate(shape, [0, 0, -80])
    #     shape = self.track_place(shape)
    #
    #     return shape
    #
    # def mr_place(self, shape):
    #     shape = rotate(shape, [0, 0, 0])
    #     shape = rotate(shape, self.key_rotation_offsets[1])
    #     t_off = self.key_translation_offsets[1]
    #     shape = translate(shape, (t_off[0], t_off[1]+self.key_diameter/2, t_off[2]))
    #     shape = rotate(shape, [0, 0, -150])
    #     shape = self.track_place(shape)
    #
    #     return shape
    #
    # def br_place(self, shape):
    #     shape = rotate(shape, [0, 0, 180])
    #     shape = rotate(shape, self.key_rotation_offsets[2])
    #     t_off = self.key_translation_offsets[2]
    #     shape = translate(shape, (t_off[0], t_off[1]+self.key_diameter/2, t_off[2]))
    #     shape = rotate(shape, [0, 0, -195])
    #     shape = self.track_place(shape)
    #
    #     return shape
    #
    # def bl_place(self, shape):
    #     debugprint('thumb_bl_place()')
    #     shape = rotate(shape, [0, 0, 180])
    #     shape = rotate(shape, self.key_rotation_offsets[3])
    #     t_off = self.key_translation_offsets[3]
    #     shape = translate(shape, (t_off[0], t_off[1]+self.key_diameter/2, t_off[2]))
    #     shape = rotate(shape, [0, 0, -240])
    #     shape = self.track_place(shape)
    #
    #     return shape
    def tb_post_r(self):
        debugprint('post_r()')
        radius = ball_diameter/2 + ball_wall_thickness + ball_gap
        return translate(web_post(),
                         [1.0*(radius - post_adj), 0.0*(radius - post_adj), 0]
                         )

    def tb_post_tr(self):
        debugprint('post_tr()')
        radius = ball_diameter/2+ball_wall_thickness + ball_gap
        return translate(web_post(),
                         [0.5*(radius - post_adj), 0.866*(radius - post_adj), 0]
                         )


    def tb_post_tl(self):
        debugprint('post_tl()')
        radius = ball_diameter/2+ball_wall_thickness + ball_gap
        return translate(web_post(),
                         [-0.5*(radius - post_adj), 0.866*(radius - post_adj), 0]
                         )


    def tb_post_l(self):
        debugprint('post_l()')
        radius = ball_diameter/2+ball_wall_thickness + ball_gap
        return translate(web_post(),
                         [-1.0*(radius - post_adj), 0.0*(radius - post_adj), 0]
                         )

    def tb_post_bl(self):
        debugprint('post_bl()')
        radius = ball_diameter/2+ball_wall_thickness + ball_gap
        return translate(web_post(),
                         [-0.5*(radius - post_adj), -0.866*(radius - post_adj), 0]
                         )


    def tb_post_br(self):
        debugprint('post_br()')
        radius = ball_diameter/2+ball_wall_thickness + ball_gap
        return translate(web_post(),
                         [0.5*(radius - post_adj), -0.866*(radius - post_adj), 0]
                         )

    def thumb_1x_layout(self, shape, cap=False):
        debugprint('thumb_1x_layout()')

        shape_list = [
            self.tl_place(rotate(shape, [0, 0, self._keys[TL].plate_rot_z])),
            self.mr_place(rotate(shape, [0, 0, self._keys[MR].plate_rot_z])),
            self.br_place(rotate(shape, [0, 0, self._keys[BR].plate_rot_z])),
            self.bl_place(rotate(shape, [0, 0, self._keys[BL].plate_rot_z])),
        ]

        shapes = add(shape_list)

        return shapes

    def thumb_15x_layout(self, shape, cap=False, plate=True):
        debugprint('thumb_15x_layout()')
        if plate:
            if cap:
                shape = rotate(shape, (0, 0, 90))
                cap_list = [self.tl_place(rotate(shape, [0, 0, self._keys[TL].plate_rot_z])),
                            self.tr_place(rotate(shape, [0, 0, self._keys[MR].plate_rot_z]))]
                return add(cap_list)
            else:
                shape_list = [self.tl_place(rotate(shape, [0, 0, self._keys[TL].plate_rot_z]))]
                if not default_1U_cluster:
                    shape_list.append(self.mr_place(rotate(shape, [0, 0, self._keys[MR].plate_rot_z])))
                return union(shape_list)
        else:
            if cap:
                shape = rotate(shape, (0, 0, 90))
                shape_list = [self.tl_place(shape), self.mr_place(shape)]

                return add(shape_list)
            else:
                shape_list = [
                    self.tl_place(shape),
                ]
                if not default_1U_cluster:
                    shape_list.append(self.mr_place(shape))

                return union(shape_list)


    def track_place(self, shape):
        # pos, rot = self.position_rotation()
        # shape = rotate(shape, rot)
        # shape = translate(shape, pos)
        return shape

    def thumb_connectors(self, side="right"):
        print('thumb_connectors()')
        hulls = []

        # bottom 2 to tb
        hulls.append(
            triangle_hulls(
                [
                    self.track_place(self.tb_post_l()),
                    self.bl_place(web_post_tl()),
                    self.track_place(self.tb_post_bl()),
                    self.bl_place(web_post_tr()),
                    self.br_place(web_post_tl()),
                    self.track_place(self.tb_post_bl()),
                    self.br_place(web_post_tr()),
                    self.track_place(self.tb_post_br()),
                    self.br_place(web_post_tr()),
                    self.track_place(self.tb_post_br()),
                    self.mr_place(web_post_br()),
                    self.track_place(self.tb_post_r()),
                    self.mr_place(web_post_bl()),
                    self.tl_place(web_post_br( )),
                    self.track_place(self.tb_post_r()),
                    self.tl_place(web_post_bl( )),
                    self.track_place(self.tb_post_tr()),
                    cluster_key_place(web_post_bl(), 0, cornerrow),
                    self.track_place(self.tb_post_tl()),
                ]
            )
        )

        # bottom left
        hulls.append(
            triangle_hulls(
                [
                    self.bl_place(web_post_tr()),
                    self.br_place(web_post_tl()),
                    self.bl_place(web_post_br()),
                    self.br_place(web_post_bl()),
                ]
            )
        )

        # bottom right
        hulls.append(
            triangle_hulls(
                [
                    self.br_place(web_post_tr()),
                    self.mr_place(web_post_br()),
                    self.br_place(web_post_br()),
                    self.mr_place(web_post_tr()),
                ]
            )
        )
        # top right
        hulls.append(
            triangle_hulls(
                [
                    self.mr_place(web_post_bl()),
                    self.tl_place(web_post_br()),
                    self.mr_place(web_post_tl()),
                    self.tl_place(web_post_tr(off_h=self.tl_off)),
                ]
            )
        )

        hulls.append(
            triangle_hulls(
                [
                    cluster_key_place(web_post_br(), 1, cornerrow),
                    cluster_key_place(web_post_tl(), 2, lastrow),
                    cluster_key_place(web_post_bl(), 2, cornerrow),
                    cluster_key_place(web_post_tr(), 2, lastrow),
                    cluster_key_place(web_post_br(), 2, cornerrow),
                    cluster_key_place(web_post_bl(), 3, cornerrow),
                ]
            )
        )

        hulls.append(
            triangle_hulls(
                [
                    cluster_key_place(web_post_tr(), 3, lastrow),
                    cluster_key_place(web_post_br(), 3, lastrow),
                    cluster_key_place(web_post_tr(), 3, lastrow),
                    cluster_key_place(web_post_bl(), 4, cornerrow),
                ]
            )
        )

        return union(hulls)

    # todo update walls for wild track, still identical to orbyl
    def walls(self, side="right"):
        print('thumb_walls()')
        # thumb, walls
        shape = wall_brace(
            self.mr_place, .5, 1, web_post_tl(),
            (lambda sh: cluster_key_place(sh, 3, lastrow)), 0, -1, web_post_bl(),
        )
        shape = union([shape, wall_brace(
            self.mr_place, .5, 1, web_post_tl(),
            self.mr_place, .5, 1, web_post_tr(),
        )])
        # BOTTOM FRONT BETWEEN MR AND BR
        shape = union([shape, wall_brace(
            self.mr_place, .5, 1, web_post_tr(),
            self.br_place, 0, -1, web_post_br(),
        )])
        # BOTTOM FRONT AT BR
        shape = union([shape, wall_brace(
            self.br_place, 0, -1, web_post_br(),
            self.br_place, 0, -1, web_post_bl(),
        )])
        # BOTTOM FRONT BETWEEN BR AND BL
        shape = union([shape, wall_brace(
            self.br_place, 0, -1, web_post_bl(),
            self.bl_place, 0, -1, web_post_br(),
        )])
        # BOTTOM FRONT AT BL
        shape = union([shape, wall_brace(
            self.bl_place, 0, -1, web_post_br(),
            self.bl_place, -1, -1, web_post_bl(),
        )])
        # TOP LEFT BEHIND TRACKBALL
        shape = union([shape, wall_brace(
            self.track_place, -1.5, 0, self.tb_post_tl(),
            (lambda sh: left_cluster_key_place(sh, lastrow - 1, -1, side=ball_side, low_corner=True)), -1, 0, web_post(),
        )])
        # LEFT OF TRACKBALL
        shape = union([shape, wall_brace(
            self.track_place, -2, 0, self.tb_post_tl(),
            self.track_place, -2, 0, self.tb_post_l(),
        )])
        shape = union([shape, wall_brace(
            self.track_place, -2, 0, self.tb_post_l(),
            self.bl_place, -1, 0, web_post_tl(),
        )])

        # BEFORE BTUS
        #
        # # LEFT OF TRACKBALL
        # shape = union([shape, wall_brace(
        #     self.track_place, -1.5, 0, self.tb_post_tl(),
        #     self.track_place, -1, 0, self.tb_post_l(),
        # )])
        # shape = union([shape, wall_brace(
        #     self.track_place, -1, 0, self.tb_post_l(),
        #     self.bl_place, -1, 0, web_post_tl(),
        # )])

        shape = union([shape, wall_brace(
            self.bl_place, -1, 0, web_post_tl(),
            self.bl_place, -1, -1, web_post_bl(),
        )])

        return shape

    def connection(self, side='right'):

        print('thumb_connection()')
        # clunky bit on the top left thumb connection  (normal connectors don't work well)
        hulls = []

        # ======= These four account for offset between plate and wall methods
        hulls.append(
            triangle_hulls(
                [
                    self.tl_place(web_post_tl()),
                    self.tl_place(web_post_tl(off_h=self.tl_off)),
                    self.tl_place(web_post_tr(off_h=self.tl_off)),
                    self.tl_place(web_post_tr()),
                    self.tl_place(web_post_tl())
                ]
            )
        )

        hulls.append(
            triangle_hulls(
                [
                    self.tl_place(web_post_tl()),
                    self.tl_place(web_post_tl(off_h=self.tl_off)),
                    self.tl_place(web_post_bl()),
                    self.tl_place(web_post_tl())
                ]
            )
        )

        hulls.append(
            triangle_hulls(
                [
                    self.tl_place(web_post_tr()),
                    self.tl_place(web_post_tr(off_h=self.tl_off)),
                    self.tl_place(web_post_br()),
                    self.tl_place(web_post_tr())
                ]
            )
        )

        hulls.append(
            triangle_hulls(
                [
                    self.tl_place(web_post_br()),
                    self.tl_place(web_post_br()),
                    self.tl_place(web_post_bl()),
                    self.tl_place(web_post_br())
                ]
            )
        )

        #  ==========================

        hulls.append(
            triangle_hulls(
                [
                    cluster_key_place(web_post_bl(), 0, cornerrow),
                    left_cluster_key_place(web_post(), lastrow - 1, -1, side=side, low_corner=True),
                    # left_cluster_key_place(translate(web_post(), wall_locate1(-1, 0)), cornerrow, -1, low_corner=True),
                    self.track_place(self.tb_post_tl()),
                ]
            )
        )

        hulls.append(
            triangle_hulls(
                [
                    cluster_key_place(web_post_bl(), 0, cornerrow),
                    left_cluster_key_place(web_post(), lastrow - 1, -1, side=side, low_corner=True),
                    # left_cluster_key_place(translate(web_post(), wall_locate1(-1, 0)), cornerrow, -1, low_corner=True),
                    self.track_place(self.tb_post_tl()),
                ]
            )
        )

        hulls.append(
            triangle_hulls(
                [
                    cluster_key_place(web_post_bl(), 0, cornerrow),  # col 0 bottom, bottom left (at left side/edge)
                    self.tl_place(web_post_tl(off_h=self.tl_off)),  # top cluster key, bottom left (sort of top left)
                    self.tl_place(web_post_bl()),
                    cluster_key_place(web_post_bl(), 0, cornerrow),  # col 1 bottom, bottom left
                    # self.tl_place(web_post_tl(off_w=self.tl_off, off_h=self.tl_off))
                ]
            )
        )

        hulls.append(
            triangle_hulls(
                [
                    self.tl_place(web_post_tl(off_h=self.tl_off)),
                    cluster_key_place(web_post_bl(), 0, cornerrow),  # col 0 bottom, bottom left (at left side/edge)
                    cluster_key_place(web_post_br(), 0, cornerrow),
                    # self.tl_place(web_post_bl(off_w=self.tl_off, off_h=self.tl_off)),  # top cluster key, bottom left (sort of top left)
                    cluster_key_place(web_post_bl(), 1, cornerrow),  # col 1 bottom, bottom left
                    self.tl_place(web_post_tl(off_h=self.tl_off))
                ]
            )
        )

        # plates to columns 1 and 2
        hulls.append(
            triangle_hulls(
                [
                    # self.tl_place(web_post_tl()),
                    self.tl_place(web_post_tl(off_h=self.tl_off)),
                    cluster_key_place(web_post_bl(), 1, cornerrow),  # col 1 bottom, bottom right corner
                    cluster_key_place(web_post_br(), 1, cornerrow),  # col 1 bottom, bottom left corner
                    self.tl_place(web_post_tl(off_h=self.tl_off)),
                    # self.tl_place(web_post_tr()),
                    # self.tl_place(web_post_tl()),
                ]
            )
        )

        hulls.append(
            triangle_hulls(
                [
                    self.tl_place(web_post_tl(off_h=self.tl_off)),
                    cluster_key_place(web_post_bl(), 1, cornerrow),  # col 1 bottom, bottom right corner
                    cluster_key_place(web_post_br(), 1, cornerrow),  # col 1 bottom, bottom left corner
                    self.tl_place(web_post_tl(off_h=self.tl_off))
                ]
            )
        )

        hulls.append(
            triangle_hulls(
                [
                    self.tl_place(web_post_tl(off_h=self.tl_off)),
                    cluster_key_place(web_post_tl(), 2, lastrow),  # col 2 bottom, top left corner
                    cluster_key_place(web_post_bl(), 2, lastrow),  # col 2 bottom, bottom left corner
                    self.tl_place(web_post_tl(off_h=self.tl_off))
                ]
            )
        )

        hulls.append(
            triangle_hulls(
                [
                    self.tl_place(web_post_tl(off_h=self.tl_off)),
                    cluster_key_place(web_post_tl(), 2, lastrow),  # col 2 bottom, top left corner
                    cluster_key_place(web_post_br(), 1, cornerrow),  # col 2 bottom, bottom left corner
                    self.tl_place(web_post_tl(off_h=self.tl_off))
                ]
            )
        )

        hulls.append(
            triangle_hulls(
                [
                    self.tl_place(web_post_tl(off_h=self.tl_off)),
                    cluster_key_place(web_post_bl(), 2, lastrow),  # col 2 bottom, top left corner
                    self.tl_place(web_post_tr(off_h=self.tl_off)),  # col 2 bottom, bottom left corner
                    self.tl_place(web_post_tl(off_h=self.tl_off))
                ]
            )
        )

        hulls.append(
            triangle_hulls(
                [
                    self.tl_place(web_post_tr(off_h=self.tl_off)),
                    cluster_key_place(web_post_bl(), 2, lastrow),  # col 2 bottom, top left corner
                    cluster_key_place(web_post_br(), 2, lastrow),  # col 2 bottom, top left corner
                    self.tl_place(web_post_tr(off_h=self.tl_off))  # col 2 bottom, bottom left corner
                ]
            )
        )

        hulls.append(
            triangle_hulls(
                [
                    self.tl_place(web_post_tr(off_h=self.tl_off)),
                    cluster_key_place(web_post_br(), 2, lastrow),  # col 2 bottom, top left corner
                    cluster_key_place(web_post_bl(), 3, lastrow),  # col 2 bottom, top left corner
                    self.tl_place(web_post_tr(off_h=self.tl_off))  # col 2 bottom, bottom left corner
                ]
            )
        )

        hulls.append(
            triangle_hulls(
                [
                    self.tl_place(web_post_tr(off_h=self.tl_off)),
                    cluster_key_place(web_post_bl(), 3, lastrow),  # col 2 bottom, top left corner
                    self.mr_wall(web_post_tl()),
                    self.tl_place(web_post_tr(off_h=self.tl_off))  # col 2 bottom, bottom left corner
                ]
            )
        )

        # Duplicate of above, just offset by x: -0.5 to ensure wall thickness
        hulls.append(
            translate(triangle_hulls(
                [
                    self.tl_place(web_post_tr( off_h=self.tl_off)),
                    cluster_key_place(web_post_bl(), 3, lastrow),  # col 2 bottom, top left corner
                    self.mr_wall(web_post_tl()),
                    self.tl_place(web_post_tr(off_h=self.tl_off))  # col 2 bottom, bottom left corner
                ]
            ), [-0.5, 0, 0])
        )

        # hulls.append(
        #     triangle_hulls(
        #         [
        #             self.mr_wall(web_post_tr()),
        #             self.mr_wall(web_post_tl()),
        #             translate(self.mr_wall(web_post_tl()), [14, 15, -2]),
        #             self.mr_wall(web_post_tr()),
        #         ]
        #     )
        # )
        #
        # # Duplicate of above, just offset by x: -0.5 to ensure wall thickness
        # hulls.append(
        #     translate(triangle_hulls(
        #         [
        #             self.mr_wall(web_post_tr()),
        #             self.mr_wall(web_post_tl()),
        #             translate(self.mr_wall(web_post_tl()), [14, 15, -2]),
        #             self.mr_wall(web_post_tr()),
        #         ]
        #     ), [-0.5, 0, 0])
        # )


        hulls.append(
            triangle_hulls(
                [
                    cluster_key_place(web_post_br(), 2, lastrow),

                    cluster_key_place(web_post_bl(), 3, lastrow),
                    cluster_key_place(web_post_tr(), 2, lastrow),
                    cluster_key_place(web_post_tl(), 3, lastrow),
                    cluster_key_place(web_post_bl(), 3, cornerrow),
                    cluster_key_place(web_post_tr(), 3, lastrow),
                    cluster_key_place(web_post_br(), 3, cornerrow),
                    cluster_key_place(web_post_bl(), 4, cornerrow),
                ]
            )
        )
        shape = union(hulls)
        return shape

    def get_extras(self, shape, pos):
        posts = [shape]
        all_pos = []
        for i in range(len(pos)):
            all_pos.append(pos[i] + tb_socket_translation_offset[i])
        z_pos = abs(pos[2])
        for post_offset in self.post_offsets:
            support_z = z_pos + post_offset[2]
            new_offsets = post_offset.copy()
            new_offsets[2] = -z_pos
            support = cylinder(1.5, support_z, 10)
            support = translate(support, all_pos)
            support = translate(support, new_offsets)
            base = cylinder(4, 1, 10)
            new_offsets[2] = 0.5 - all_pos[2]
            base = translate(base, all_pos)
            base = translate(base, new_offsets)
            posts.append(base)
            support = union([support, base])
            posts.append(support)
        return union(posts)
