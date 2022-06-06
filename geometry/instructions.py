"""Realizado por Diogo Batista"""
from core_ext.mesh import Mesh
from core_ext.texture import Texture

from geometry.rectangle import RectangleGeometry

from material.texture import TextureMaterial
from extras.text_texture import TextTexture

class InstructionsMesh(Mesh):
    def __init__(self):
        geometry = RectangleGeometry(1, 1)
        grid_texture = Texture(file_name="images/paper.png")
        material = TextureMaterial(texture=grid_texture)
        self.mesh = Mesh(
            geometry=geometry,
            material=material
        )

        geometry1 = RectangleGeometry(0.75,0.25)
        message1 = TextTexture(text="Press [Enter] to start playing",
                               font_file_name="fonts/ALGER.TTF",
                               background_color=[255,255,255,0],
                               font_size=40, font_color=[0, 0, 0],
                               image_width=768, image_height=256,
                               align_horizontal=0.5, align_vertical=0.5,
                               image_border_width=0)
        material1 = TextureMaterial(message1)
        self.mesh1 = Mesh(geometry1, material1)

        geometry2 = RectangleGeometry(0.75,0.25)
        message2 = TextTexture(text="- Shoot all targets to clear the level ",
                               font_file_name="fonts/ALGER.TTF",
                               background_color=[255,255,255,0],
                               font_size=32, font_color=[0, 0, 0],
                               image_width=768, image_height=256,
                               align_horizontal=0.5, align_vertical=0.5,
                               image_border_width=0)
        material2 = TextureMaterial(message2)
        self.mesh2 = Mesh(geometry2, material2)

        geometry3 = RectangleGeometry(0.75,0.25)
        message3 = TextTexture(text="- Clear all 5 levels to win                            ",
                               font_file_name="fonts/ALGER.TTF",
                               background_color=[255,255,255,0],
                               font_size=32, font_color=[0, 0, 0],
                               image_width=768, image_height=256,
                               align_horizontal=0.5, align_vertical=0.5,
                               image_border_width=0)
        material3 = TextureMaterial(message3)
        self.mesh3 = Mesh(geometry3, material3)

        geometry4 = RectangleGeometry(0.75,0.25)
        message4 = TextTexture(text="- Aim the bow with your mouse                      ",
                               font_file_name="fonts/ALGER.TTF",
                               background_color=[255,255,255,0],
                               font_size=32, font_color=[0, 0, 0],
                               image_width=768, image_height=256,
                               align_horizontal=0.5, align_vertical=0.5,
                               image_border_width=0)
        material4 = TextureMaterial(message4)
        self.mesh4 = Mesh(geometry4, material4)

        geometry5 = RectangleGeometry(0.75,0.25)
        message5 = TextTexture(text="- Fire the arrow with left mouse button",
                               font_file_name="fonts/ALGER.TTF",
                               background_color=[255,255,255,0],
                               font_size=32, font_color=[0, 0, 0],
                               image_width=768, image_height=256,
                               align_horizontal=0.5, align_vertical=0.5,
                               image_border_width=0)
        material5 = TextureMaterial(message5)
        self.mesh5 = Mesh(geometry5, material5)

        geometry6 = RectangleGeometry(0.75,0.25)
        message6 = TextTexture(text="- Be careful with the 3 types of wind       ",
                               font_file_name="fonts/ALGER.TTF",
                               background_color=[255,255,255,0],
                               font_size=32, font_color=[0, 0, 0],
                               image_width=768, image_height=256,
                               align_horizontal=0.5, align_vertical=0.5,
                               image_border_width=0)
        material6 = TextureMaterial(message6)
        self.mesh6 = Mesh(geometry6, material6)

        geometry7 = RectangleGeometry(0.75,0.25)
        message7 = TextTexture(text="- Press F to reset your aim position           ",
                               font_file_name="fonts/ALGER.TTF",
                               background_color=[255,255,255,0],
                               font_size=32, font_color=[0, 0, 0],
                               image_width=768, image_height=256,
                               align_horizontal=0.5, align_vertical=0.5,
                               image_border_width=0)
        material7 = TextureMaterial(message7)
        self.mesh7 = Mesh(geometry7, material7)

        geometry8 = RectangleGeometry(0.75,0.25)
        message8 = TextTexture(text="- Use F1 or F2 to change your view angle",
                               font_file_name="fonts/ALGER.TTF",
                               background_color=[255,255,255,0],
                               font_size=32, font_color=[0, 0, 0],
                               image_width=768, image_height=256,
                               align_horizontal=0.5, align_vertical=0.5,
                               image_border_width=0)
        material8 = TextureMaterial(message8)
        self.mesh8 = Mesh(geometry8, material8)

        geometry9 = RectangleGeometry(0.75,0.25)
        message9 = TextTexture(text="- Combine both to see a frontal angle    ",
                               font_file_name="fonts/ALGER.TTF",
                               background_color=[255,255,255,0],
                               font_size=32, font_color=[0, 0, 0],
                               image_width=768, image_height=256,
                               align_horizontal=0.5, align_vertical=0.5,
                               image_border_width=0)
        material9 = TextureMaterial(message9)
        self.mesh9 = Mesh(geometry9, material9)

        geometry10 = RectangleGeometry(0.75,0.25)
        message10 = TextTexture(text="Instructions",
                               font_file_name="fonts/Wide Latin Regular.ttf",
                               background_color=[255,255,255,0],
                               font_size=50, font_color=[0, 0, 0],
                               image_width=768, image_height=192,
                               align_horizontal=0.5, align_vertical=0.5,
                               image_border_width=0)
        material10 = TextureMaterial(message10)
        self.mesh10 = Mesh(geometry10, material10)
        
        self.mesh = super().__init__(geometry,material)
        self.mesh1 = Mesh(geometry1, material1)
        self.mesh1.translate(0,-0.3,0.05)

        self.mesh2 = Mesh(geometry2, material2)
        self.mesh2.translate(0,0.15,0.05)

        self.mesh3 = Mesh(geometry3, material3)
        self.mesh3.translate(0,0.1,0.05)

        self.mesh4 = Mesh(geometry4, material4)
        self.mesh4.translate(0,0.05,0.05)

        self.mesh5 = Mesh(geometry5, material5)
        self.mesh5.translate(0,0.0,0.05)

        self.mesh6 = Mesh(geometry6, material6)
        self.mesh6.translate(0,-0.05,0.05)

        self.mesh7 = Mesh(geometry7, material7)
        self.mesh7.translate(0,-0.1,0.05)

        self.mesh8 = Mesh(geometry8, material8)
        self.mesh8.translate(0,-0.15,0.05)

        self.mesh9 = Mesh(geometry9, material9)
        self.mesh9.translate(0,-0.2,0.05)

        self.mesh10 = Mesh(geometry10, material10)
        self.mesh10.translate(0,0.25,0.05)

        self.add(self.mesh1)
        self.add(self.mesh2)
        self.add(self.mesh3)
        self.add(self.mesh4)
        self.add(self.mesh5)
        self.add(self.mesh6)
        self.add(self.mesh7)
        self.add(self.mesh8)
        self.add(self.mesh9)
        self.add(self.mesh10)