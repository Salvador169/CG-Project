""" 
Shoot The Target
Consiste num jogo de arco e flecha, onde o objetivo é acertar pelo menos um projétil em cada alvo, de modo a passar os cinco diferentes níveis.

Realizado por: 
Carlos Carvalho 64583
David Pereira 64586
Diogo Batista 64587
Pedro Salvador 64590
"""

import random
import numpy as np
import math

from core.base import Base
from core.matrix import Matrix

from core_ext.camera import Camera
from core_ext.mesh import Mesh
from core_ext.renderer import Renderer
from core_ext.scene import Scene
from core_ext.texture import Texture

from extras.movement_camera import MovementCamera
from extras.movement_rig import MovementRig
from extras.target_rig import TargetRig

from geometry.pyramid import PyramidGeometry
from geometry.polygon import PolygonGeometry
from geometry.sphere import SphereGeometry
from geometry.rectangle import RectangleGeometry
from geometry.bow import BowMesh
from geometry.arrow import ArrowMesh
from geometry.target import TargetMesh
from geometry.tripe import TripeMesh
from geometry.game_over import GameOver
from geometry.main_page import MainPageMesh
from geometry.instructions import InstructionsMesh
from geometry.winning import Winning

from material.material import Material
from material.texture import TextureMaterial
from material.sprite import SpriteMaterial
from material.flat import FlatMaterial

from light.ambient import AmbientLight
from light.point import PointLight



class Example(Base):
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.cameraRig = MovementCamera()
        self.rig = MovementRig()
        self.cameraRig.add(self.camera)
        self.rig.add(self.cameraRig)
        # self.camera.set_position([0,0,5])
        self.bow = BowMesh()
        self.bow.scale(0.5)
        self.arrow = ArrowMesh()
        self.bow.set_position([-0.3,0,-0.3])
        self.arrow.set_position([-0.175,0.3,0])
        self.arrow.rotate_x(-math.pi/2, local=False)

        self.ambient1 = AmbientLight(color=[0.9, 0.9, 0.9])
        self.ambient2 = AmbientLight(color=[1, 1, 1])
        self.ambient3 = AmbientLight(color=[0.5, 0.5, 0.5])
        self.ambient4 = AmbientLight(color=[0.8, 0.8, 0.8])
        self.ambient5 = AmbientLight(color=[0.7, 0.7, 0.7])
        self.point1 = PointLight(color=[1, 0, 0], position=[230, -2.9, 0])
        self.point2 = PointLight(color=[1, 0, 0], position=[200, -2.9, -8])
        self.point3 = PointLight(color=[1, 0, 0], position=[165, -2.9, 5])
        self.point4 = PointLight(color=[1, 0, 0], position=[200,5,20])
        self.scene.add(self.ambient1)


        vertex_shader_code = """
            uniform mat4 projectionMatrix;
            uniform mat4 viewMatrix;
            uniform mat4 modelMatrix;
            in vec3 vertexPosition;
            in vec2 vertexUV;
            out vec2 UV;

            void main()
            {
                gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
                UV = vertexUV;
            }
        """
        fragment_shader_code = """
            uniform sampler2D rgbNoise;
            uniform sampler2D image;
            in vec2 UV;
            uniform float time;
            out vec4 fragColor;

            void main()
            {
                vec2 uvShift = UV + vec2(-0.033, 0.07) * time;
                vec4 noiseValues = texture2D(rgbNoise, uvShift);
                vec2 uvNoise = UV + 0.01 * noiseValues.rg;
                fragColor = texture2D(image, uvNoise);
            }
        """


        geometry = RectangleGeometry(width = 0.5, height = 0.125)
        tile_set = Texture("images/energy_bar.png")
        sprite_material = SpriteMaterial(tile_set, {
            "billboard" : 1, 
            "tileCount" : [1, 4],
            "tileNumber" : 0 
        })

        geometry1 = RectangleGeometry(width = 0.5, height = 0.125)
        tile_set1 = Texture("images/arrow_number1.png")
        sprite_material1 = SpriteMaterial(tile_set1, {
            "billboard" : 1, 
            "tileCount" : [1, 4],
            "tileNumber" : 0 
        })

        geometry2 = RectangleGeometry(width = 0.5, height = 0.1)
        tile_set2 = Texture("images/niveis.png")
        sprite_material2 = SpriteMaterial(tile_set2, {
            "billboard" : 1, 
            "tileCount" : [1, 5],
            "tileNumber" : 0 
        })

        geometry3 = RectangleGeometry(width = 0.15, height = 0.2)
        tile_set3 = Texture("images/wind_colors.png")
        sprite_material3 = SpriteMaterial(tile_set3, {
            "billboard" : 1, 
            "tileCount" : [3, 2],
            "tileNumber" : 0 
        })

        self.mainPage = MainPageMesh()
        self.mainPage.set_position([10, 0, -100])

        self.instructions = InstructionsMesh()
        self.instructions.set_position([7.5, 0, -100])

        self.gameOver = GameOver()
        self.gameOver.set_position([5, 0, -100])

        self.winning = Winning()
        self.winning.set_position([2.5, 0, -100])

        self.sprite = Mesh(geometry, sprite_material)
        self.sprite.set_position([0.55,-0.45,-1])
        self.sprite1 = Mesh(geometry1, sprite_material1)
        self.sprite1.set_position([0.55,-0.3,-1])
        self.sprite2 = Mesh(geometry2, sprite_material2)
        self.sprite2.set_position([0,0.55,-1])
        self.sprite3 = Mesh(geometry3, sprite_material3)
        self.sprite3.set_position([0,0.45,-1])
        self.rig.add(self.bow)
        self.rig.add(self.arrow)
        self.rig.add(self.sprite)
        self.rig.add(self.sprite1)
        self.rig.add(self.sprite2)
        self.rig.add(self.sprite3)
        self.rig.set_position([0, 0, 20])
        self.scene.add(self.rig)

        self.arrows=[]
        self.arrows.append(ArrowMesh())
        self.arrows.append(ArrowMesh())
        self.arrows.append(ArrowMesh())
        self.arrows[0].set_position([-2, 0, 100])
        self.arrows[1].set_position([-2, 2, 100])
        self.arrows[2].set_position([2, 0, 100])

        # LEVEL 1
        self.sky_geometry = SphereGeometry(radius=50)
        self.sky_material = FlatMaterial(texture=Texture(file_name="images/sky1.jpg"), property_dict={"doubleSide": True, "baseColor": [1,1,1]})
        self.sky = Mesh(self.sky_geometry, self.sky_material)
        self.scene.add(self.sky)
        self.grass_geometry = RectangleGeometry(width=100, height=100)
        self.grass_material = TextureMaterial(
            texture=Texture(file_name="images/grass.jpg"),
            property_dict={"repeatUV": [50, 50]}
        )
        self.grass = Mesh(self.grass_geometry, self.grass_material)
        self.grass.rotate_x(-math.pi/2)
        self.grass.translate(0,0,-3)
        self.scene.add(self.grass)
        #=================================================

        # LEVEL 2
        self.sky_geometry1 = SphereGeometry(radius=50)
        self.sky_material1 = FlatMaterial(texture=Texture(file_name="images/sky1.jpg"), property_dict={"doubleSide": True})
        self.sky1 = Mesh(self.sky_geometry1, self.sky_material1)
        self.sky1.translate(101,0,0)
        self.scene.add(self.sky1)
        self.grass_geometry1 = RectangleGeometry(width=100, height=100)
        self.grass_material1 = TextureMaterial(
            texture=Texture(file_name="images/sand.jpg"),
            property_dict={"repeatUV": [50, 50]}
        )
        self.grass1 = Mesh(self.grass_geometry1, self.grass_material1)
        self.grass1.rotate_x(-math.pi/2)
        self.grass1.translate(101,0,-3)
        self.scene.add(self.grass1)
        #=================================================

        # LEVEL 3
        self.sky_geometry2 = SphereGeometry(radius=50)
        self.sky_material2 = FlatMaterial(texture=Texture(file_name="images/night.jpg"), property_dict={"doubleSide": True})
        self.sky2 = Mesh(self.sky_geometry2, self.sky_material2)
        self.sky2.translate(-101,0,0)
        self.scene.add(self.sky2)
        self.grass_geometry2 = RectangleGeometry(width=100, height=100)
        self.grass_material2 = TextureMaterial(
            texture=Texture(file_name="images/grass.jpg"),
            property_dict={"repeatUV": [50, 50]}
        )
        self.grass2 = Mesh(self.grass_geometry2, self.grass_material2)
        self.grass2.rotate_x(-math.pi/2)
        self.grass2.translate(-101,0,-3)
        self.scene.add(self.grass2)
        #=================================================

        # LEVEL 4
        nether_sky_geometry = SphereGeometry(radius=50)
        nether_sky_material = FlatMaterial(texture=Texture(file_name="images/sky1.jpg"), property_dict={"doubleSide": True})
        nether_sky = Mesh(nether_sky_geometry, nether_sky_material)
        nether_sky.translate(202,0,0)
        nether_sky_geometry1 = SphereGeometry(radius=49.9)#se der erro meter 49
        nether_sky_material1 = TextureMaterial(texture=Texture(file_name="images/volcano.png"), property_dict={"doubleSide": True})
        nether_sky1 = Mesh(nether_sky_geometry1, nether_sky_material1)
        nether_sky1.translate(202,0,0)
        self.scene.add(nether_sky)
        self.scene.add(nether_sky1)

        nether_geometry = RectangleGeometry(width=100, height=100)
        rgb_noise_texture = Texture("images/rgb-noise.jpg")
        grid_texture = Texture("images/lava.jpg")
        self.distort_material = Material(vertex_shader_code, fragment_shader_code)
        self.distort_material.add_uniform("sampler2D", "rgbNoise", [rgb_noise_texture.texture_ref, 1])
        self.distort_material.add_uniform("sampler2D", "image", [grid_texture.texture_ref, 2])
        self.distort_material.add_uniform("float", "time", 0.0)
        self.distort_material.locate_uniforms()

        self.magma = Mesh(nether_geometry, self.distort_material)
        self.magma.rotate_x(-math.pi/2)
        self.magma.translate(202,0,-3)
        self.scene.add(self.magma)
        #=================================================

        # LEVEL 5
        end_sky_geometry = SphereGeometry(radius=50)
        end_sky_material = FlatMaterial(texture=Texture(file_name="images/black_sky.png"), property_dict={"doubleSide": True})
        end_sky = Mesh(end_sky_geometry, end_sky_material)
        end_sky.translate(-202,0,0)
        self.scene.add(end_sky)
        end_geometry = RectangleGeometry(width=100, height=100)
        end_material = TextureMaterial(
            texture=Texture(file_name="images/moon.jpg"),
            property_dict={"repeatUV": [40, 40]}
        )
        end = Mesh(end_geometry, end_material)
        end.rotate_x(-math.pi/2)
        end.translate(-202,0,-3)
        self.scene.add(end)
        #=================================================

        # SCENARIO LEVEL 1
        tree_material = TextureMaterial(texture=Texture(file_name="images/tree.png"))
        tree_geometry = RectangleGeometry(10,10)
        tree_geometry.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.tree = Mesh(tree_geometry, tree_material)
        self.tree.set_position([10, 2, 0])
        self.scene.add(self.tree)

        tree_geometry1 = RectangleGeometry(10,10)
        tree_geometry1.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.tree1 = Mesh(tree_geometry1, tree_material)
        self.tree1.set_position([15, 2, 10])
        self.scene.add(self.tree1)

        tree_geometry2 = RectangleGeometry(10,10)
        tree_geometry2.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.tree2 = Mesh(tree_geometry2, tree_material)
        self.tree2.set_position([-10, 2, 0])
        self.scene.add(self.tree2)

        tree_geometry3 = RectangleGeometry(10,10)
        tree_geometry3.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.tree3 = Mesh(tree_geometry3, tree_material)
        self.tree3.set_position([-15, 2, 10])
        self.scene.add(self.tree3)

        tree_geometry4 = RectangleGeometry(10,10)
        tree_geometry4.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.tree4 = Mesh(tree_geometry4, tree_material)
        self.tree4.set_position([-15, 2, 20])
        self.scene.add(self.tree4)

        tree_geometry5 = RectangleGeometry(10,10)
        tree_geometry5.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.tree5 = Mesh(tree_geometry5, tree_material)
        self.tree5.set_position([15, 2, 20])
        self.scene.add(self.tree5)

        tree_geometry6 = RectangleGeometry(10,10)
        tree_geometry6.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.tree6 = Mesh(tree_geometry6, tree_material)
        self.tree6.set_position([-10, 2, 35])
        self.scene.add(self.tree6)

        tree_geometry7 = RectangleGeometry(10,10)
        tree_geometry7.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.tree7 = Mesh(tree_geometry7, tree_material)
        self.tree7.set_position([10, 2, 35])
        self.scene.add(self.tree7)

        tree_geometry8 = RectangleGeometry(10,10)
        tree_geometry8.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.tree8 = Mesh(tree_geometry8, tree_material)
        self.tree8.set_position([0, 2, 35])
        self.scene.add(self.tree8)

        gate_material = TextureMaterial(texture=Texture(file_name="images/gate.png"))
        gate_geometry = RectangleGeometry(15,10)
        self.gate = Mesh(gate_geometry, gate_material)
        self.gate.set_position([0, -1.5, -30])
        self.scene.add(self.gate)

        gate_material1 = TextureMaterial(texture=Texture(file_name="images/gate2.png"), property_dict={"doubleSide": True})
        gate_geometry1 = RectangleGeometry(15,10)
        self.gate1 = Mesh(gate_geometry1, gate_material1)
        self.gate1.set_position([14.5, -1.5, -30])
        self.scene.add(self.gate1)

        gate_geometry2 = RectangleGeometry(15,10)
        self.gate2 = Mesh(gate_geometry2, gate_material1)
        self.gate2.set_position([29, -1.5, -30])
        self.scene.add(self.gate2)

        gate_geometry3 = RectangleGeometry(15,10)
        self.gate3 = Mesh(gate_geometry3, gate_material1)
        self.gate3.set_position([-14.5, -1.5, -30])
        self.scene.add(self.gate3)

        gate_geometry4 = RectangleGeometry(15,10)
        self.gate4 = Mesh(gate_geometry4, gate_material1)
        self.gate4.set_position([-29, -1.5, -30])
        self.scene.add(self.gate4)

        gate_geometry5 = RectangleGeometry(15,10)
        self.gate5 = Mesh(gate_geometry5, gate_material1)
        self.gate5.set_position([-36.25, -1.5, -22.75])
        self.gate5.rotate_y(math.pi/2)
        self.scene.add(self.gate5)

        gate_geometry6 = RectangleGeometry(15,10)
        self.gate6 = Mesh(gate_geometry6, gate_material1)
        self.gate6.set_position([36.25, -1.5, -22.75])
        self.gate6.rotate_y(math.pi/2)
        self.scene.add(self.gate6)

        gate_geometry7 = RectangleGeometry(15,10)
        self.gate7 = Mesh(gate_geometry7, gate_material1)
        self.gate7.set_position([-36.25, -1.5, -8.25])
        self.gate7.rotate_y(math.pi/2)
        self.scene.add(self.gate7)

        gate_geometry8 = RectangleGeometry(15,10)
        self.gate8 = Mesh(gate_geometry8, gate_material1)
        self.gate8.set_position([36.25, -1.5, -8.25])
        self.gate8.rotate_y(math.pi/2)
        self.scene.add(self.gate8)

        gate_geometry9 = RectangleGeometry(15,10)
        self.gate9 = Mesh(gate_geometry9, gate_material1)
        self.gate9.set_position([-36.25, -1.5, 6.25])
        self.gate9.rotate_y(math.pi/2)
        self.scene.add(self.gate9)

        gate_geometry10 = RectangleGeometry(15,10)
        self.gate10 = Mesh(gate_geometry10, gate_material1)
        self.gate10.set_position([36.25, -1.5, 6.25])
        self.gate10.rotate_y(math.pi/2)
        self.scene.add(self.gate10)

        gate_geometry11 = RectangleGeometry(15,10)
        self.gate11 = Mesh(gate_geometry11, gate_material1)
        self.gate11.set_position([-36.25, -1.5, 20.75])
        self.gate11.rotate_y(math.pi/2)
        self.scene.add(self.gate11)

        gate_geometry12 = RectangleGeometry(15,10)
        self.gate12 = Mesh(gate_geometry12, gate_material1)
        self.gate12.set_position([36.25, -1.5, 20.75])
        self.gate12.rotate_y(math.pi/2)
        self.scene.add(self.gate12)

        gate_geometry13 = RectangleGeometry(15,10)
        self.gate13 = Mesh(gate_geometry13, gate_material1)
        self.gate13.set_position([-29, -1.5, 28])
        self.scene.add(self.gate13)

        gate_geometry14 = RectangleGeometry(15,10)
        self.gate14 = Mesh(gate_geometry14, gate_material1)
        self.gate14.set_position([29, -1.5, 28])
        self.scene.add(self.gate14)

        gate_geometry15 = RectangleGeometry(15,10)
        self.gate15 = Mesh(gate_geometry15, gate_material1)
        self.gate15.set_position([-14.5, -1.5, 28])
        self.scene.add(self.gate15)

        gate_geometry16 = RectangleGeometry(15,10)
        self.gate16 = Mesh(gate_geometry16, gate_material1)
        self.gate16.set_position([14.5, -1.5, 28])
        self.scene.add(self.gate16)

        gate_geometry17 = RectangleGeometry(15,10)
        self.gate17 = Mesh(gate_geometry17, gate_material1)
        self.gate17.set_position([0, -1.5, 28])
        self.scene.add(self.gate17)

        #=================================================

        # SCENARIO LEVEL 2

        big_pyramid_material = TextureMaterial(texture=Texture(file_name="images/pyramid.jpg"), property_dict={"repeatUV": [25, 25]})
        big_pyramid = PyramidGeometry(radius=30, height=30, sides=4, height_segments=25)
        self.big_pyramid = Mesh(big_pyramid, big_pyramid_material)
        self.big_pyramid.set_position([140, 3.12, -25])
        self.scene.add(self.big_pyramid)

        medium_pyramid_material = TextureMaterial(texture=Texture(file_name="images/pyramid.jpg"), property_dict={"repeatUV": [25, 25]})
        medium_pyramid = PyramidGeometry(radius=20, height=20, sides=4, height_segments=25)
        self.medium_pyramid = Mesh(medium_pyramid, medium_pyramid_material)
        self.medium_pyramid.set_position([80, 3.12, -25])
        self.scene.add(self.medium_pyramid)

        small_pyramid_material = TextureMaterial(texture=Texture(file_name="images/pyramid.jpg"), property_dict={"repeatUV": [25, 25]})
        small_pyramid = PyramidGeometry(radius=10, height=10, sides=4, height_segments=25)
        self.small_pyramid = Mesh(small_pyramid, small_pyramid_material)
        self.small_pyramid.set_position([140, 0, 10])
        self.scene.add(self.small_pyramid)

        camel_material = TextureMaterial(texture=Texture(file_name="images/camel.png"))
        camel = RectangleGeometry(5,5)
        self.camel = Mesh(camel, camel_material)
        camel.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.camel.set_position([106, 0, 22.5])
        self.scene.add(self.camel)

        camel1 = RectangleGeometry(2.5,2.5)
        self.camel1 = Mesh(camel1, camel_material)
        camel1.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.camel1.set_position([60, -2, 0])
        self.scene.add(self.camel1)

        camel2 = RectangleGeometry(2.5,2.5)
        self.camel2 = Mesh(camel2, camel_material)
        camel2.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.camel2.set_position([120, -2, -30])
        self.scene.add(self.camel2)

        camel3 = RectangleGeometry(2.5,2.5)
        self.camel3 = Mesh(camel3, camel_material)
        camel3.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.camel3.set_position([60, -2, 5])
        self.scene.add(self.camel3)

        camel4 = RectangleGeometry(2.5,2.5)
        self.camel4 = Mesh(camel4, camel_material)
        camel4.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.camel4.set_position([60, -2, -15])
        self.scene.add(self.camel4)

        palm_material = TextureMaterial(texture=Texture(file_name="images/palm.png"))
        palm = RectangleGeometry(15,15)
        self.palm = Mesh(palm, palm_material)
        palm.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.palm.set_position([60, 0, -25])
        self.scene.add(self.palm)

        palm1 = RectangleGeometry(15,15)
        self.palm1 = Mesh(palm1, palm_material)
        palm1.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.palm1.set_position([89, 0, -35])
        self.scene.add(self.palm1)

        palm2 = RectangleGeometry(15,15)
        self.palm2 = Mesh(palm2, palm_material)
        palm2.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.palm2.set_position([140, 0, -5])
        self.scene.add(self.palm2)

        palm3 = RectangleGeometry(15,15)
        self.palm3 = Mesh(palm3, palm_material)
        palm3.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.palm3.set_position([140, 0, 20])
        self.scene.add(self.palm3)

        #=================================================

        # SCENARIO LEVEL 3
        grave_material = TextureMaterial(texture=Texture(file_name="images/spooky_tree.png"), property_dict={"doubleSide": True})
        skpy_material = TextureMaterial(texture=Texture(file_name="images/spky_tree.png"), property_dict={"doubleSide": True})
        grave_geometry = RectangleGeometry(2,3)
        grave_geometry.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.grave = Mesh(grave_geometry, grave_material)
        self.grave.set_position([-91, -1.5, -20])
        self.scene.add(self.grave)

        grave_geometry1 = RectangleGeometry(2,3)
        grave_geometry1.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.grave1 = Mesh(grave_geometry1, grave_material)
        self.grave1.set_position([-91, -1.5, 15])
        self.scene.add(self.grave1)

        grave_geometry2 = RectangleGeometry(2,3)
        grave_geometry2.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.grave2 = Mesh(grave_geometry2, grave_material)
        self.grave2.set_position([-91, -1.5, -10])
        self.scene.add(self.grave2)

        grave_geometry3 = RectangleGeometry(2,3)
        grave_geometry3.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.grave3 = Mesh(grave_geometry3, grave_material)
        self.grave3.set_position([-91, -1.5, -5])
        self.scene.add(self.grave3)

        grave_geometry4 = RectangleGeometry(2,3)
        grave_geometry4.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.grave4 = Mesh(grave_geometry4, grave_material)
        self.grave4.set_position([-91, -1.5, 0])
        self.scene.add(self.grave4)

        grave_geometry5 = RectangleGeometry(2,3)
        grave_geometry5.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.grave5 = Mesh(grave_geometry5, grave_material)
        self.grave5.set_position([-91, -1.5, 5])
        self.scene.add(self.grave5)

        grave_geometry6 = RectangleGeometry(2,3)
        grave_geometry6.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.grave6 = Mesh(grave_geometry6, grave_material)
        self.grave6.set_position([-91, -1.5, 10])
        self.scene.add(self.grave6)

        grave_geometry7 = RectangleGeometry(10,10)
        grave_geometry7.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.grave7 = Mesh(grave_geometry7, skpy_material)
        self.grave7.set_position([-91, 2, -15])
        self.scene.add(self.grave7)

        grave_geometry8 = RectangleGeometry(2,3)
        grave_geometry8.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.grave8 = Mesh(grave_geometry8, grave_material)
        self.grave8.set_position([-91, -1.5, 20])
        self.scene.add(self.grave8)

        grave_geometry9 = RectangleGeometry(2,3)
        grave_geometry9.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.grave9 = Mesh(grave_geometry9, grave_material)
        self.grave9.set_position([-81, -1.5, -20])
        self.scene.add(self.grave9)

        grave_geometry10 = RectangleGeometry(2,3)
        grave_geometry10.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.grave10 = Mesh(grave_geometry10, grave_material)
        self.grave10.set_position([-81, -1.5, -15])
        self.scene.add(self.grave10)

        grave_geometry11 = RectangleGeometry(2,3)
        grave_geometry11.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.grave11 = Mesh(grave_geometry6, grave_material)
        self.grave11.set_position([-81, -1.5, -10])
        self.scene.add(self.grave6)

        grave_geometry12 = RectangleGeometry(2,3)
        grave_geometry12.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.grave12 = Mesh(grave_geometry12, grave_material)
        self.grave12.set_position([-81, -1.5, -5])
        self.scene.add(self.grave12)

        grave_geometry13 = RectangleGeometry(2,3)
        grave_geometry13.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.grave13 = Mesh(grave_geometry13, grave_material)
        self.grave13.set_position([-81, -1.5, 0])
        self.scene.add(self.grave13)

        grave_geometry14 = RectangleGeometry(10,10)
        grave_geometry14.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.grave14 = Mesh(grave_geometry14, skpy_material)
        self.grave14.set_position([-81, 2, 5])
        self.scene.add(self.grave14)

        grave_geometry15 = RectangleGeometry(2,3)
        grave_geometry15.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.grave15 = Mesh(grave_geometry15, grave_material)
        self.grave15.set_position([-81, -1.5, 10])
        self.scene.add(self.grave15)

        grave_geometry16 = RectangleGeometry(2,3)
        grave_geometry16.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.grave16 = Mesh(grave_geometry16, grave_material)
        self.grave16.set_position([-81, -1.5, 15])
        self.scene.add(self.grave16)

        grave_geometry17 = RectangleGeometry(2,3)
        grave_geometry17.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.grave17 = Mesh(grave_geometry17, grave_material)
        self.grave17.set_position([-81, -1.5, 20])
        self.scene.add(self.grave17)

        lgrave_geometry = RectangleGeometry(2,3)
        lgrave_geometry.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.lgrave = Mesh(lgrave_geometry, grave_material)
        self.lgrave.set_position([-121, -1.5, -20])
        self.scene.add(self.lgrave)

        lgrave_geometry1 = RectangleGeometry(2,3)
        lgrave_geometry1.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.lgrave1 = Mesh(lgrave_geometry1, grave_material)
        self.lgrave1.set_position([-121, -1.5, -15])
        self.scene.add(self.lgrave1)

        lgrave_geometry2 = RectangleGeometry(2,3)
        lgrave_geometry2.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.lgrave2 = Mesh(lgrave_geometry2, grave_material)
        self.lgrave2.set_position([-111, -1.5, -10])
        self.scene.add(self.lgrave2)

        lgrave_geometry3 = RectangleGeometry(2,3)
        lgrave_geometry3.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.lgrave3 = Mesh(lgrave_geometry3, grave_material)
        self.lgrave3.set_position([-111, -1.5, -5])
        self.scene.add(self.lgrave3)

        lgrave_geometry4 = RectangleGeometry(2,3)
        lgrave_geometry4.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.lgrave4 = Mesh(lgrave_geometry4, grave_material)
        self.lgrave4.set_position([-111, -1.5, 0])
        self.scene.add(self.lgrave4)

        lgrave_geometry5 = RectangleGeometry(2,3)
        lgrave_geometry5.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.lgrave5 = Mesh(lgrave_geometry5, grave_material)
        self.lgrave5.set_position([-111, -1.5, 5])
        self.scene.add(self.lgrave5)

        lgrave_geometry6 = RectangleGeometry(2,3)
        lgrave_geometry6.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.lgrave6 = Mesh(lgrave_geometry6, grave_material)
        self.lgrave6.set_position([-111, -1.5, 10])
        self.scene.add(self.lgrave6)

        lgrave_geometry7 = RectangleGeometry(2,3)
        lgrave_geometry7.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.lgrave7 = Mesh(lgrave_geometry7, grave_material)
        self.lgrave7.set_position([-111, -1.5, 15])
        self.scene.add(self.lgrave7)

        lgrave_geometry8 = RectangleGeometry(2,3)
        lgrave_geometry8.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.lgrave8 = Mesh(lgrave_geometry8, grave_material)
        self.lgrave8.set_position([-111, -1.5, 20])
        self.scene.add(self.lgrave8)

        lgrave_geometry9 = RectangleGeometry(2,3)
        lgrave_geometry9.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.lgrave9 = Mesh(lgrave_geometry9, grave_material)
        self.lgrave9.set_position([-121, -1.5, -20])
        self.scene.add(self.lgrave9)

        lgrave_geometry10 = RectangleGeometry(2,3)
        lgrave_geometry10.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.lgrave10 = Mesh(lgrave_geometry10, grave_material)
        self.lgrave10.set_position([-121, -1.5, -15])
        self.scene.add(self.lgrave10)

        lgrave_geometry11 = RectangleGeometry(10,10)
        lgrave_geometry11.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.lgrave11 = Mesh(lgrave_geometry11, skpy_material)
        self.lgrave11.set_position([-121, 2, -10])
        self.scene.add(self.lgrave11)

        lgrave_geometry12 = RectangleGeometry(2,3)
        lgrave_geometry12.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.lgrave12 = Mesh(lgrave_geometry12, grave_material)
        self.lgrave12.set_position([-121, -1.5, -5])
        self.scene.add(self.lgrave12)

        lgrave_geometry13 = RectangleGeometry(2,3)
        lgrave_geometry13.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.lgrave13 = Mesh(lgrave_geometry13, grave_material)
        self.lgrave13.set_position([-121, -1.5, 0])
        self.scene.add(self.lgrave13)

        lgrave_geometry14 = RectangleGeometry(2,3)
        lgrave_geometry14.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.lgrave14 = Mesh(lgrave_geometry14, grave_material)
        self.lgrave14.set_position([-121, -1.5, 5])
        self.scene.add(self.lgrave14)

        lgrave_geometry15 = RectangleGeometry(2,3)
        lgrave_geometry15.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.lgrave15 = Mesh(lgrave_geometry15, grave_material)
        self.lgrave15.set_position([-121, -1.5, 10])
        self.scene.add(self.lgrave15)

        lgrave_geometry16 = RectangleGeometry(10,10)
        lgrave_geometry16.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.lgrave16 = Mesh(lgrave_geometry16, skpy_material)
        self.lgrave16.set_position([-121, 2, 15])
        self.scene.add(self.lgrave16)

        lgrave_geometry17 = RectangleGeometry(2,3)
        lgrave_geometry17.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.lgrave17 = Mesh(lgrave_geometry17, grave_material)
        self.lgrave17.set_position([-121, -1.5, 20])
        self.scene.add(self.lgrave17)

        spookygate_material = TextureMaterial(texture=Texture(file_name="images/gate.png"))
        spookygate_geometry = RectangleGeometry(15,10)
        self.spookygate = Mesh(spookygate_geometry, spookygate_material)
        self.spookygate.set_position([-101, 0, -30])
        self.scene.add(self.spookygate)

        spookygate_material1 = TextureMaterial(texture=Texture(file_name="images/gate2.png"), property_dict={"doubleSide": True})
        spookygate_geometry1 = RectangleGeometry(15,10)
        self.spookygate1 = Mesh(spookygate_geometry1, spookygate_material1)
        self.spookygate1.set_position([-86.5, 0, -30])
        self.scene.add(self.spookygate1)

        spookygate_geometry2 = RectangleGeometry(15,10)
        self.spookygate2 = Mesh(spookygate_geometry2, spookygate_material1)
        self.spookygate2.set_position([-72, 0, -30])
        self.scene.add(self.spookygate2)

        spookygate_geometry3 = RectangleGeometry(15,10)
        self.spookygate3 = Mesh(spookygate_geometry3, spookygate_material1)
        self.spookygate3.set_position([-115.5, 0, -30])
        self.scene.add(self.spookygate3)

        spookygate_geometry4 = RectangleGeometry(15,10)
        self.spookygate4 = Mesh(spookygate_geometry4, spookygate_material1)
        self.spookygate4.set_position([-130, 0, -30])
        self.scene.add(self.spookygate4)

        spookygate_geometry5 = RectangleGeometry(15,10)
        self.spookygate5 = Mesh(spookygate_geometry5, spookygate_material1)
        self.spookygate5.set_position([-137.25, 0, -22.75])
        self.spookygate5.rotate_y(math.pi/2)
        self.scene.add(self.spookygate5)

        spookygate_geometry6 = RectangleGeometry(15,10)
        self.spookygate6 = Mesh(spookygate_geometry6, spookygate_material1)
        self.spookygate6.set_position([-64.75, 0, -22.75])
        self.spookygate6.rotate_y(math.pi/2)
        self.scene.add(self.spookygate6)

        spookygate_geometry7 = RectangleGeometry(15,10)
        self.spookygate7 = Mesh(spookygate_geometry7, spookygate_material1)
        self.spookygate7.set_position([-137.25, 0, -8.25])
        self.spookygate7.rotate_y(math.pi/2)
        self.scene.add(self.spookygate7)

        spookygate_geometry8 = RectangleGeometry(15,10)
        self.spookygate8 = Mesh(spookygate_geometry8, spookygate_material1)
        self.spookygate8.set_position([-64.75, 0, -8.25])
        self.spookygate8.rotate_y(math.pi/2)
        self.scene.add(self.spookygate8)

        spookygate_geometry9 = RectangleGeometry(15,10)
        self.spookygate9 = Mesh(spookygate_geometry9, spookygate_material1)
        self.spookygate9.set_position([-137.25, 0, 6.25])
        self.spookygate9.rotate_y(math.pi/2)
        self.scene.add(self.spookygate9)

        spookygate_geometry10 = RectangleGeometry(15,10)
        self.spookygate10 = Mesh(spookygate_geometry10, spookygate_material1)
        self.spookygate10.set_position([-64.75, 0, 6.25])
        self.spookygate10.rotate_y(math.pi/2)
        self.scene.add(self.spookygate10)

        spookygate_geometry11 = RectangleGeometry(15,10)
        self.spookygate11 = Mesh(spookygate_geometry11, spookygate_material1)
        self.spookygate11.set_position([-137.25, 0, 20.75])
        self.spookygate11.rotate_y(math.pi/2)
        self.scene.add(self.spookygate11)

        spookygate_geometry12 = RectangleGeometry(15,10)
        self.spookygate12 = Mesh(spookygate_geometry12, gate_material1)
        self.spookygate12.set_position([-64.75, 0, 20.75])
        self.spookygate12.rotate_y(math.pi/2)
        self.scene.add(self.spookygate12)

        spookygate_geometry13 = RectangleGeometry(15,10)
        self.spookygate13 = Mesh(spookygate_geometry13, spookygate_material1)
        self.spookygate13.set_position([-130, 0, 28])
        self.scene.add(self.spookygate13)

        spookygate_geometry14 = RectangleGeometry(15,10)
        self.spookygate14 = Mesh(spookygate_geometry14, spookygate_material1)
        self.spookygate14.set_position([-72, 0, 28])
        self.scene.add(self.spookygate14)

        spookygate_geometry15 = RectangleGeometry(15,10)
        self.spookygate15 = Mesh(spookygate_geometry15, spookygate_material1)
        self.spookygate15.set_position([-115.5, 0, 28])
        self.scene.add(self.spookygate15)

        spookygate_geometry16 = RectangleGeometry(15,10)
        self.spookygate16 = Mesh(spookygate_geometry16, spookygate_material1)
        self.spookygate16.set_position([-86.5, 0, 28])
        self.scene.add(self.spookygate16)

        spookygate_geometry17 = RectangleGeometry(15,10)
        self.spookygate17 = Mesh(spookygate_geometry17, spookygate_material1)
        self.spookygate17.set_position([-101, 0, 28])
        self.scene.add(self.spookygate17)

        spky_geometry = RectangleGeometry(10,10)
        spky_geometry.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.spky = Mesh(spky_geometry, skpy_material)
        self.spky.set_position([-96, 2, 35])
        self.scene.add(self.spky)

        spky_geometry1 = RectangleGeometry(10,10)
        spky_geometry1.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.spky1 = Mesh(spky_geometry1, skpy_material)
        self.spky1.set_position([-116, 2, 35])
        self.scene.add(self.spky1)

        spky_geometry2 = RectangleGeometry(10,10)
        spky_geometry2.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.spky2 = Mesh(spky_geometry2, skpy_material)
        self.spky2.set_position([-140, 2, 0])
        self.scene.add(self.spky2)

        spky_geometry3 = RectangleGeometry(10,10)
        spky_geometry3.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.spky3 = Mesh(spky_geometry3, skpy_material)
        self.spky3.set_position([-140, 2, 20])
        self.scene.add(self.spky3)

        spky_geometry4 = RectangleGeometry(10,10)
        spky_geometry4.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.spky4 = Mesh(spky_geometry4, skpy_material)
        self.spky4.set_position([-140, 2, -20])
        self.scene.add(self.spky4)

        spky_geometry5 = RectangleGeometry(10,10)
        spky_geometry5.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.spky5 = Mesh(spky_geometry5, skpy_material)
        self.spky5.set_position([-60, 2, 0])
        self.scene.add(self.spky5)

        spky_geometry6 = RectangleGeometry(10,10)
        spky_geometry6.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.spky6 = Mesh(spky_geometry6, skpy_material)
        self.spky6.set_position([-60, 2, 20])
        self.scene.add(self.spky6)

        spky_geometry7 = RectangleGeometry(10,10)
        spky_geometry7.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.spky7 = Mesh(spky_geometry7, skpy_material)
        self.spky7.set_position([-60, 2, -20])
        self.scene.add(self.spky7)

        spky_geometry8 = RectangleGeometry(10,10)
        spky_geometry8.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.spky8 = Mesh(spky_geometry8, skpy_material)
        self.spky8.set_position([-111, 2, -40])
        self.scene.add(self.spky8)

        spky_geometry9 = RectangleGeometry(10,10)
        spky_geometry9.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.spky9 = Mesh(spky_geometry9, skpy_material)
        self.spky9.set_position([-81, 2, -40])
        self.scene.add(self.spky9)

        dead_material = TextureMaterial(texture=Texture(file_name="images/dead1.png"))
        dead_geometry = RectangleGeometry(6,3)
        dead_geometry.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.dead = Mesh(dead_geometry, dead_material)
        self.dead.set_position([-123, -1.5, 1])
        self.scene.add(self.dead)

        dead_material1 = TextureMaterial(texture=Texture(file_name="images/dead.png"))
        dead_geometry1 = RectangleGeometry(6,3)
        dead_geometry1.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.dead1 = Mesh(dead_geometry1, dead_material1)
        self.dead1.set_position([-98, -1.5, -5])
        self.scene.add(self.dead1)

        #=================================================

        # SCENARIO LEVEL 4

        ground_material = TextureMaterial(texture=Texture(file_name="images/magma.jpg"), property_dict={"doubleSide": True})
        ground_geometry = PolygonGeometry(sides=15, radius=2.5)
        self.ground = Mesh(ground_geometry, ground_material)
        self.ground.set_position([200, -2.9, 20])
        self.ground.rotate_x(math.pi/2)
        self.scene.add(self.ground)

        ground_geometry1 = PolygonGeometry(sides=15, radius=5)
        self.ground1 = Mesh(ground_geometry1, ground_material)
        self.ground1.set_position([165, -2.9, 5])
        self.ground1.rotate_x(math.pi/2)
        self.scene.add(self.ground1)

        ground_geometry2 = PolygonGeometry(sides=15, radius=5)
        self.ground2 = Mesh(ground_geometry2, ground_material)
        self.ground2.set_position([200, -2.9, -10])
        self.ground2.rotate_x(math.pi/2)
        self.scene.add(self.ground2)

        ground_geometry3 = PolygonGeometry(sides=15, radius=5)
        self.ground3 = Mesh(ground_geometry3, ground_material)
        self.ground3.set_position([230, -2.9, 0])
        self.ground3.rotate_x(math.pi/2)
        self.scene.add(self.ground3)

        rock_material = TextureMaterial(texture=Texture(file_name="images/rock.png"))
        rock_geometry = RectangleGeometry(10,10)
        rock_geometry.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.rock = Mesh(rock_geometry, rock_material)
        self.rock.set_position([170, -2.9, -14])
        self.scene.add(self.rock)

        rock_geometry1 = RectangleGeometry(5,5)
        rock_geometry1.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.rock1 = Mesh(rock_geometry1, rock_material)
        self.rock1.set_position([220, -2.9, 20])
        self.scene.add(self.rock1)

        rock_geometry2 = RectangleGeometry(5,5)
        rock_geometry2.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.rock2 = Mesh(rock_geometry2, rock_material)
        self.rock2.set_position([230, -2.9, 10])
        self.scene.add(self.rock2)

        rock_geometry3 = RectangleGeometry(5,5)
        rock_geometry3.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.rock3 = Mesh(rock_geometry3, rock_material)
        self.rock3.set_position([180, -2.9, -10])
        self.scene.add(self.rock3)

        rock_geometry4 = RectangleGeometry(5,5)
        rock_geometry4.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.rock4 = Mesh(rock_geometry4, rock_material)
        self.rock4.set_position([210, -2.9, -30])
        self.scene.add(self.rock4)

        rock_geometry5 = RectangleGeometry(5,5)
        rock_geometry5.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.rock5 = Mesh(rock_geometry5, rock_material)
        self.rock5.set_position([230, -2.9, -15])
        self.scene.add(self.rock5)

        rock_geometry6 = RectangleGeometry(5,5)
        rock_geometry6.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.rock6 = Mesh(rock_geometry6, rock_material)
        self.rock6.set_position([170, -2.9, 25])
        self.scene.add(self.rock6)

        plane_material = TextureMaterial(texture=Texture(file_name="images/plane.png"), property_dict={"doubleSide": True})
        plane_geometry = RectangleGeometry(25,25)
        self.plane = Mesh(plane_geometry, plane_material)
        self.plane.rotate_x(math.pi/2)
        self.plane.set_position([180, 30, 0])
        self.scene.add(self.plane)
        
        #=================================================

        # SCENARIO LEVEL 5

        astronaut_material = TextureMaterial(texture=Texture(file_name="images/astronaut.png"))
        astronaut_geometry = RectangleGeometry(5,5)
        astronaut_geometry.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.astronaut = Mesh(astronaut_geometry, astronaut_material)
        self.astronaut.set_position([-203, 0, 20])
        self.scene.add(self.astronaut)

        earth_material = TextureMaterial(texture=Texture(file_name="images/earth.png"))
        earth_geometry = RectangleGeometry(50,50)
        earth_geometry.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.earth = Mesh(earth_geometry, earth_material)
        self.earth.set_position([-200, 20, -30])
        self.scene.add(self.earth)

        meteor_material = TextureMaterial(texture=Texture(file_name="images/meteor.png"))
        meteor_geometry = RectangleGeometry(15,15)
        meteor_geometry.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.meteor = Mesh(meteor_geometry, meteor_material)
        self.meteor.set_position([-220, 25, -35])
        self.scene.add(self.meteor)

        satellite_material = TextureMaterial(texture=Texture(file_name="images/satellite.png"))
        satellite_geometry = RectangleGeometry(5,5)
        satellite_geometry.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.satellite = Mesh(satellite_geometry, satellite_material)
        self.satellite.set_position([-160, 10, 0])
        self.scene.add(self.satellite)

        flag_material = TextureMaterial(texture=Texture(file_name="images/flag.png"))
        flag_geometry = RectangleGeometry(5,5)
        flag_geometry.apply_matrix(Matrix.make_rotation_y(3.14)) 
        self.flag = Mesh(flag_geometry, flag_material)
        self.flag.set_position([-203, 0, 22])
        self.scene.add(self.flag)

        self.scene.add(self.arrows[0])
        self.scene.add(self.arrows[1])
        self.scene.add(self.arrows[2])
        self.scene.add(self.mainPage)
        self.scene.add(self.instructions)
        self.scene.add(self.gameOver)
        self.scene.add(self.winning)

        self.lives = 3
        self.angle = 0
        self.shooting = False
        self.level = 1

        self.tiro = -1
        self.collision = False
        self.win = False
        self.wind = random.randint(1,2)
        self.sprite3.material.uniform_dict["tileNumber"].data = self.wind
        self.moveWind = 0

        
        self.target = []
        self.target.append(TargetMesh())
        self.target.append(TargetMesh())
        self.target.append(TargetMesh())
        self.target.append(TargetMesh())
        self.target.append(TargetMesh())
        self.target.append(TargetMesh())
        self.target.append(TargetMesh())
        self.target.append(TargetMesh())
        self.target.append(TargetMesh())
        self.target.append(TargetMesh())
        self.target.append(TargetMesh())
        self.target.append(TargetMesh())

        self.target[0].translate(0.9, 0.3, -0.05)
        self.target[1].translate(0.9, 0.3, -0.05)
        self.target[2].translate(0.9, 0.3, -0.05)
        self.target[3].translate(0.9, 0.3, -0.05)
        self.target[4].translate(0.9, 0.3, -0.05)
        self.target[5].translate(0.9, 0.3, -0.05)
        self.target[6].translate(0.9, 0.3, -0.05)
        self.target[7].translate(0.9, 0.3, -0.05)
        self.target[8].translate(0.9, 0.3, -0.05)
        self.target[9].translate(0.9, 0.3, -0.05)
        self.target[10].translate(0.9, 0.3, -0.05)
        self.target[11].translate(0.9, 0.3, -0.05)



        self.tripe = []
        self.tripe.append(TripeMesh())
        self.tripe.append(TripeMesh())
        self.tripe.append(TripeMesh())
        self.tripe.append(TripeMesh())
        self.tripe.append(TripeMesh())
        self.tripe.append(TripeMesh())
        self.tripe.append(TripeMesh())
        self.tripe.append(TripeMesh())
        self.tripe.append(TripeMesh())
        self.tripe.append(TripeMesh())
        self.tripe.append(TripeMesh())
        self.tripe.append(TripeMesh())

        self.targetRig = []
        self.targetRig.append(TargetRig())
        self.targetRig.append(TargetRig())
        self.targetRig.append(TargetRig())
        self.targetRig.append(TargetRig())
        self.targetRig.append(TargetRig())
        self.targetRig.append(TargetRig())
        self.targetRig.append(TargetRig())
        self.targetRig.append(TargetRig())
        self.targetRig.append(TargetRig())
        self.targetRig.append(TargetRig())
        self.targetRig.append(TargetRig())
        self.targetRig.append(TargetRig())

        self.targetRig[0].add(self.tripe[0])
        self.targetRig[0].add(self.target[0])
        self.targetRig[1].add(self.tripe[1])
        self.targetRig[1].add(self.target[1])
        self.targetRig[2].add(self.tripe[2])
        self.targetRig[2].add(self.target[2])
        self.targetRig[3].add(self.tripe[3])
        self.targetRig[3].add(self.target[3])
        self.targetRig[4].add(self.tripe[4])
        self.targetRig[4].add(self.target[4])
        self.targetRig[5].add(self.tripe[5])
        self.targetRig[5].add(self.target[5])
        self.targetRig[6].add(self.tripe[6])
        self.targetRig[6].add(self.target[6])
        self.targetRig[7].add(self.tripe[7])
        self.targetRig[7].add(self.target[7])
        self.targetRig[8].add(self.tripe[8])
        self.targetRig[8].add(self.target[8])
        self.targetRig[9].add(self.tripe[9])
        self.targetRig[9].add(self.target[9])
        self.targetRig[10].add(self.tripe[10])
        self.targetRig[10].add(self.target[10])
        self.targetRig[11].add(self.tripe[11])
        self.targetRig[11].add(self.target[11])


        #NIVEL 1 ALVOS
        self.targetRig[0].set_position([0, -1.8, -5])

        #NIVEL 2 ALVOS
        self.targetRig[1].set_position([77, -1.8, 5])
        self.targetRig[1].rotate_y(math.pi/2)
        self.targetRig[2].set_position([126, -1.8, 10])
        self.targetRig[2].rotate_y(-math.pi/2)

        #NIVEL 3 ALVOS
        self.targetRig[3].set_position([-81, -1.8, 2])
        self.targetRig[3].rotate_y(-math.pi/2)
        self.targetRig[4].set_position([-95, -1.8, -15])
        self.targetRig[5].set_position([-130, -1.8, 3])
        self.targetRig[5].rotate_y(math.pi/2)

        #NIVEL 4 ALVOS
        self.targetRig[6].set_position([165, -1.8, 5])
        self.targetRig[6].rotate_y(math.pi/2)
        self.targetRig[7].set_position([200, -1.8, -10])
        self.targetRig[8].set_position([230, -1.8, 0])
        self.targetRig[8].rotate_y(-math.pi/2)

        #NIVEL 5 ALVOS
        self.targetRig[9].set_position([-173, -1.8, 8])
        self.targetRig[9].rotate_y(-math.pi/2)
        self.targetRig[10].set_position([-200, -1.8, -13])
        self.targetRig[11].set_position([-220, -1.8, 25])
        self.targetRig[11].rotate_y(math.pi/2)


        self.scene.add(self.targetRig[0])
        self.scene.add(self.targetRig[1])
        self.scene.add(self.targetRig[2])
        self.scene.add(self.targetRig[3])
        self.scene.add(self.targetRig[4])
        self.scene.add(self.targetRig[5])
        self.scene.add(self.targetRig[6])
        self.scene.add(self.targetRig[7])
        self.scene.add(self.targetRig[8])
        self.scene.add(self.targetRig[9])
        self.scene.add(self.targetRig[10])
        self.scene.add(self.targetRig[11])

        self.targetsCollided = []
        self.targetsCollided = [False for i in range(12)]


    def update(self):
        self.distort_material.uniform_dict["time"].data += self.delta_time/4

        self.tree.look_at(self.camera.global_position)
        self.tree1.look_at(self.camera.global_position)
        self.tree2.look_at(self.camera.global_position)
        self.tree3.look_at(self.camera.global_position)
        self.tree4.look_at(self.camera.global_position)
        self.tree5.look_at(self.camera.global_position)
        self.tree6.look_at(self.camera.global_position)
        self.tree7.look_at(self.camera.global_position)
        self.tree8.look_at(self.camera.global_position)
        
        self.grave.look_at(self.camera.global_position)
        self.grave1.look_at(self.camera.global_position)
        self.grave2.look_at(self.camera.global_position)
        self.grave3.look_at(self.camera.global_position)
        self.grave4.look_at(self.camera.global_position)
        self.grave5.look_at(self.camera.global_position)
        self.grave6.look_at(self.camera.global_position)
        self.grave7.look_at(self.camera.global_position)
        self.grave8.look_at(self.camera.global_position)
        self.grave9.look_at(self.camera.global_position)
        self.grave10.look_at(self.camera.global_position)
        self.grave11.look_at(self.camera.global_position)
        self.grave12.look_at(self.camera.global_position)
        self.grave13.look_at(self.camera.global_position)
        self.grave14.look_at(self.camera.global_position)
        self.grave15.look_at(self.camera.global_position)
        self.grave16.look_at(self.camera.global_position)
        self.grave17.look_at(self.camera.global_position)
        self.lgrave.look_at(self.camera.global_position)
        self.lgrave1.look_at(self.camera.global_position)
        self.lgrave2.look_at(self.camera.global_position)
        self.lgrave3.look_at(self.camera.global_position)
        self.lgrave4.look_at(self.camera.global_position)
        self.lgrave5.look_at(self.camera.global_position)
        self.lgrave6.look_at(self.camera.global_position)
        self.lgrave7.look_at(self.camera.global_position)
        self.lgrave8.look_at(self.camera.global_position)
        self.lgrave9.look_at(self.camera.global_position)
        self.lgrave10.look_at(self.camera.global_position)
        self.lgrave11.look_at(self.camera.global_position)
        self.lgrave12.look_at(self.camera.global_position)
        self.lgrave13.look_at(self.camera.global_position)
        self.lgrave14.look_at(self.camera.global_position)
        self.lgrave15.look_at(self.camera.global_position)
        self.lgrave16.look_at(self.camera.global_position)
        self.lgrave17.look_at(self.camera.global_position)

        self.camel.look_at(self.camera.global_position)
        self.camel1.look_at(self.camera.global_position)
        self.camel2.look_at(self.camera.global_position)
        self.camel3.look_at(self.camera.global_position)
        self.camel4.look_at(self.camera.global_position)
        
        self.palm.look_at(self.camera.global_position)
        self.palm1.look_at(self.camera.global_position)
        self.palm2.look_at(self.camera.global_position)
        self.palm3.look_at(self.camera.global_position)
        
        self.dead.look_at(self.camera.global_position)
        self.dead1.look_at(self.camera.global_position)

        self.spky.look_at(self.camera.global_position)
        self.spky1.look_at(self.camera.global_position)
        self.spky2.look_at(self.camera.global_position)
        self.spky3.look_at(self.camera.global_position)
        self.spky4.look_at(self.camera.global_position)
        self.spky5.look_at(self.camera.global_position)
        self.spky6.look_at(self.camera.global_position)
        self.spky7.look_at(self.camera.global_position)
        self.spky8.look_at(self.camera.global_position)
        self.spky9.look_at(self.camera.global_position)

        self.rock.look_at(self.camera.global_position)
        self.rock1.look_at(self.camera.global_position)
        self.rock2.look_at(self.camera.global_position)
        self.rock3.look_at(self.camera.global_position)
        self.rock4.look_at(self.camera.global_position)
        self.rock5.look_at(self.camera.global_position)
        self.rock6.look_at(self.camera.global_position)
        
        self.earth.look_at(self.camera.global_position)
        self.meteor.look_at(self.camera.global_position)

        self.astronaut.look_at(self.camera.global_position)
        
        self.satellite.look_at(self.camera.global_position)

        self.flag.look_at(self.camera.global_position)

        self.cameraRig.update(self.input, self.level, self.win)
        self.renderer.render(self.scene, self.camera)
        if self.wind == 0:
            self.moveWind = 0.1
        elif self.wind == 1:
            self.moveWind = -0.01
        elif self.wind == 2:
            self.moveWind = 0.01
        elif self.wind == 3:
            self.moveWind = 0.05
        elif self.wind == 4:
            self.moveWind = -0.1
        elif self.wind == 5:
            self.moveWind = -0.05
        self.sprite2.material.uniform_dict["tileNumber"].data = self.level-1
        if self.cameraRig.isGame == True:
            self.win = False
            self.rig.update(self.input, self.delta_time*2)
            if self.level == 5:
                self.rig.set_position([0,0,20])
            if self.level == 2:
                self.rig.set_position([100,0,20])
            if self.level == 3:
                self.rig.set_position([-100,0,20])
            if self.level == 4:
                self.rig.set_position([200,0,20])
            if self.level == 5:
                self.rig.set_position([-200,0,20])
            if self.level == 6:
                self.level = 1
                self.wind = random.randint(1,2)
                self.sprite3.material.uniform_dict["tileNumber"].data = self.wind
            if self.lives == 0 and self.collision == True:
                if self.level == 1 and self.targetsCollided[0] == True:
                    self.scene.remove(self.ambient1)
                    self.scene.add(self.ambient2)
                if self.level == 2 and (self.targetsCollided[1] == True or self.targetsCollided[2] == True):
                    self.scene.remove(self.ambient2)
                    self.scene.add(self.ambient3)
                if self.level == 3 and (self.targetsCollided[3] == True or self.targetsCollided[4] == True or self.targetsCollided[5] == True):
                    self.scene.remove(self.ambient3)
                    self.scene.add(self.ambient4)
                    self.scene.add(self.point1)
                    self.scene.add(self.point2)
                    self.scene.add(self.point3)
                    self.scene.add(self.point4)
                if self.level == 4 and (self.targetsCollided[6] == True or self.targetsCollided[7] == True or self.targetsCollided[8] == True):
                    self.scene.remove(self.ambient4)
                    self.scene.remove(self.point1)
                    self.scene.remove(self.point2)
                    self.scene.remove(self.point3)
                    self.scene.remove(self.point4)
                    self.scene.add(self.ambient5)
                if self.level == 1:
                    self.wind = np.random.choice(np.arange(0, 6), p=[0.1, 0.25, 0.25, 0.15, 0.1, 0.15])
                elif self.level == 2:
                    self.wind = np.random.choice(np.arange(0, 6), p=[0.1, 0.15, 0.15, 0.25, 0.1, 0.25])
                elif self.level == 3:
                    self.wind = np.random.choice(np.arange(0, 6), p=[0.2, 0.10, 0.10, 0.2, 0.2, 0.2])
                elif self.level == 4:
                    self.wind = np.random.choice(np.arange(0, 6), p=[0.3, 0, 0, 0.2, 0.3, 0.2])
                self.rig._look_attachment.set_local_matrix(self.rig.getInitalMatrix())
                self.lives = 3
                self.tiro = -1
                self.level = self.level+1
                self.rig.set_position([0,0,20])
                self.arrows[0].set_position([-2, 0, 100])
                self.arrows[1].set_position([-2, 2, 100])
                self.arrows[2].set_position([2, 0, 100])
                self.sprite3.material.uniform_dict["tileNumber"].data = self.wind
                if self.level == 2 and self.targetsCollided[0] == False:
                    self.level=6
                    self.targetsCollided = [False for i in range(12)]
                if self.level == 3 and (self.targetsCollided[1] == False or self.targetsCollided[2] == False):
                    self.scene.remove(self.ambient2)
                    self.scene.add(self.ambient1)
                    self.level=6
                    self.targetsCollided = [False for i in range(12)]
                if self.level == 4 and (self.targetsCollided[3] == False or self.targetsCollided[4] == False or self.targetsCollided[5] == False):
                    self.scene.remove(self.ambient3)
                    self.scene.add(self.ambient1)
                    self.level=6
                    self.targetsCollided = [False for i in range(12)]
                if self.level == 5 and (self.targetsCollided[6] == False or self.targetsCollided[7] == False or self.targetsCollided[8] == False):
                    self.scene.remove(self.ambient4)
                    self.scene.remove(self.point1)
                    self.scene.remove(self.point2)
                    self.scene.remove(self.point3)
                    self.scene.remove(self.point4)
                    self.scene.add(self.ambient1)
                    self.level=6
                    self.targetsCollided = [False for i in range(12)]
                if self.level == 6 and self.targetsCollided[9] == True and self.targetsCollided[10] == True and self.targetsCollided[11] == True:
                    self.scene.remove(self.ambient5)
                    self.scene.add(self.ambient1)
                    self.win = True
                    self.level=6
                    self.targetsCollided = [False for i in range(12)]

            if self.rig.isShooting() == True and self.shooting == False:
                # self.tiro = self.tiro+1
                self.shooting = True
                self.arrows[self.tiro].set_local_matrix(self.arrow.global_matrix)
                self.rig._look_attachment.children_list[2].set_position([-0.175,0,5])
                self.lives = self.lives-1
                self.collision = False
            
            if self.rig.isShooting() == True and self.shooting == True:
                if self.rig.getPower() < 5:
                    self.angle = self.angle + 1/self.rig.getPower()*0.1
                elif self.rig.getPower() < 30:
                    self.angle = self.angle + 1/self.rig.getPower()*0.5
                else:
                    self.angle = self.angle + 1/self.rig.getPower()*1
                self.arrows[self.tiro].translate(self.moveWind,self.rig.getPower()*0.01,math.cos(self.angle)-1)
            else:
                self.shooting = False
                self.angle = 0
                self.rig._look_attachment.children_list[2].set_position([-0.175,0,0])
                tileNumber = math.floor(self.rig.getPower() / 30)
                self.sprite.material.uniform_dict["tileNumber"].data = tileNumber
                tileNumber1 = self.lives
                self.sprite1.material.uniform_dict["tileNumber"].data = tileNumber1
                self.rig.update(self.input, self.delta_time)
        else:
            
            self.rig._look_attachment.set_local_matrix(self.rig.getInitalMatrix())
        


        #COLLISION
        arrowCenter = self.arrows[self.tiro].global_position
        
        targetCenter = []
        targetCenter.append(self.target[0].global_position)
        targetCenter.append(self.target[1].global_position)
        targetCenter.append(self.target[2].global_position)
        targetCenter.append(self.target[3].global_position)
        targetCenter.append(self.target[4].global_position)
        targetCenter.append(self.target[5].global_position)
        targetCenter.append(self.target[6].global_position)
        targetCenter.append(self.target[7].global_position)
        targetCenter.append(self.target[8].global_position)
        targetCenter.append(self.target[9].global_position)
        targetCenter.append(self.target[10].global_position)
        targetCenter.append(self.target[11].global_position)

        
        #TARGET 1
        vector1=np.array(arrowCenter)
        vector11=np.array(targetCenter[0])
        dist1= math.sqrt(abs((vector11[0]-vector1[0])**2+(vector11[1]-vector1[1])**2 +(vector11[2]-vector1[2])**2))

        #TARGET 2
        vector2=np.array(arrowCenter)
        vector21=np.array(targetCenter[1])
        dist2= math.sqrt(abs((vector21[0]-vector2[0])**2+(vector21[1]-vector2[1])**2 +(vector21[2]-vector2[2])**2))

        #TARGET 3
        vector3=np.array(arrowCenter)
        vector31=np.array(targetCenter[2])
        dist3= math.sqrt(abs((vector31[0]-vector3[0])**2+(vector31[1]-vector3[1])**2 +(vector31[2]-vector3[2])**2))

        #TARGET 4
        vector4=np.array(arrowCenter)
        vector41=np.array(targetCenter[3])
        dist4= math.sqrt(abs((vector41[0]-vector4[0])**2+(vector41[1]-vector4[1])**2 +(vector41[2]-vector4[2])**2))

        #TARGET 5
        vector5=np.array(arrowCenter)
        vector51=np.array(targetCenter[4])
        dist5= math.sqrt(abs((vector51[0]-vector5[0])**2+(vector51[1]-vector5[1])**2 +(vector51[2]-vector5[2])**2))

        #TARGET 6
        vector6=np.array(arrowCenter)
        vector61=np.array(targetCenter[5])
        dist6= math.sqrt(abs((vector61[0]-vector6[0])**2+(vector61[1]-vector6[1])**2 +(vector61[2]-vector6[2])**2))

        #TARGET 7
        vector7=np.array(arrowCenter)
        vector71=np.array(targetCenter[6])
        dist7= math.sqrt(abs((vector71[0]-vector7[0])**2+(vector71[1]-vector7[1])**2 +(vector71[2]-vector7[2])**2))

        #TARGET 8
        vector8=np.array(arrowCenter)
        vector81=np.array(targetCenter[7])
        dist8= math.sqrt(abs((vector81[0]-vector8[0])**2+(vector81[1]-vector8[1])**2 +(vector81[2]-vector8[2])**2))

        #TARGET 9
        vector9=np.array(arrowCenter)
        vector91=np.array(targetCenter[8])
        dist9= math.sqrt(abs((vector91[0]-vector9[0])**2+(vector91[1]-vector9[1])**2 +(vector91[2]-vector9[2])**2))

        #TARGET 10
        vector10=np.array(arrowCenter)
        vector101=np.array(targetCenter[9])
        dist10= math.sqrt(abs((vector101[0]-vector10[0])**2+(vector101[1]-vector10[1])**2 +(vector101[2]-vector10[2])**2))

        #TARGET 11
        vector11=np.array(arrowCenter)
        vector111=np.array(targetCenter[10])
        dist11= math.sqrt(abs((vector111[0]-vector11[0])**2+(vector111[1]-vector11[1])**2 +(vector111[2]-vector11[2])**2))

        #TARGET 12
        vector12=np.array(arrowCenter)
        vector121=np.array(targetCenter[11])
        dist12= math.sqrt(abs((vector121[0]-vector12[0])**2+(vector121[1]-vector12[1])**2 +(vector121[2]-vector12[2])**2))

        #TARGET 1
        if ( dist1 <= 0.7 and 2.5 >= arrowCenter[2]):
            self.targetsCollided[0] = True
            self.rig.setShooting(False)
            self.collision = True
            if self.tiro < 2:
                self.tiro = self.tiro + 1
                self.rig.setPower(0)

        #TARGET 2
        if ( dist2 <= 0.7 and 2.5 >= arrowCenter[1]):
            self.targetsCollided[1] = True
            self.rig.setShooting(False)
            self.collision = True
            if self.tiro < 2:
                self.tiro = self.tiro + 1
                self.rig.setPower(0)
        
        #TARGET 3
        if ( dist3 <= 0.7 and 2.5 >= arrowCenter[1]):
            self.targetsCollided[2] = True
            self.rig.setShooting(False)
            self.collision = True
            if self.tiro < 2:
                self.tiro = self.tiro + 1
                self.rig.setPower(0)

        #TARGET 4
        if ( dist4 <= 0.7 and 2.5 >= arrowCenter[1]):
            self.targetsCollided[3] = True
            self.rig.setShooting(False)
            self.collision = True
            if self.tiro < 2:
                self.tiro = self.tiro + 1
                self.rig.setPower(0)

        #TARGET 5
        if ( dist5 <= 0.7 and 2.5 >= arrowCenter[2]):
            self.targetsCollided[4] = True
            self.rig.setShooting(False)
            self.collision = True
            if self.tiro < 2:
                self.tiro = self.tiro + 1
                self.rig.setPower(0)

        #TARGET 6
        if ( dist6 <= 0.7 and 2.5 >= arrowCenter[1]):
            self.targetsCollided[5] = True
            self.rig.setShooting(False)
            self.collision = True
            if self.tiro < 2:
                self.tiro = self.tiro + 1
                self.rig.setPower(0)
        
        #TARGET 7
        if ( dist7 <= 0.7 and 2.5 >= arrowCenter[1]):
            self.targetsCollided[6] = True
            self.rig.setShooting(False)
            self.collision = True
            if self.tiro < 2:
                self.tiro = self.tiro + 1
                self.rig.setPower(0)

        #TARGET 8
        if ( dist8 <= 0.7 and 2.5 >= arrowCenter[2]):
            self.targetsCollided[7] = True
            self.rig.setShooting(False)
            self.collision = True
            if self.tiro < 2:
                self.tiro = self.tiro + 1
                self.rig.setPower(0)

        #TARGET 9
        if ( dist9 <= 0.7 and 2.5 >= arrowCenter[1]):
            self.targetsCollided[8] = True
            self.rig.setShooting(False)
            self.collision = True
            if self.tiro < 2:
                self.tiro = self.tiro + 1
                self.rig.setPower(0)

        #TARGET 10
        if ( dist10 <= 0.7 and 2.5 >= arrowCenter[1]):
            self.targetsCollided[9] = True
            self.rig.setShooting(False)
            self.collision = True
            if self.tiro < 2:
                self.tiro = self.tiro + 1
                self.rig.setPower(0)

        #TARGET 11
        if ( dist11 <= 0.7 and 2.5 >= arrowCenter[2]):
            self.targetsCollided[10] = True
            self.rig.setShooting(False)
            self.collision = True
            if self.tiro < 2:
                self.tiro = self.tiro + 1
                self.rig.setPower(0)

        #TARGET 12
        if ( dist12 <= 0.7 and 2.5 >= arrowCenter[1]):
            self.targetsCollided[11] = True
            self.rig.setShooting(False)
            self.collision = True
            if self.tiro < 2:
                self.tiro = self.tiro + 1
                self.rig.setPower(0)

        if self.arrows[self.tiro].global_position[1] < -3+0.175:
            self.rig.setShooting(False)
            self.collision = True
            if self.tiro < 2:
                self.tiro = self.tiro + 1
                self.rig.setPower(0)

Example(screen_size=[800, 600]).run()