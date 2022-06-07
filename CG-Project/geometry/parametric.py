from geometry.geometry import Geometry

import numpy


class ParametricGeometry(Geometry):
    def __init__(self,
                 u_start, u_end, u_resolution,
                 v_start, v_end, v_resolution,
                 surface_function):
        super().__init__()
        # Generate set of points on function
        delta_u = (u_end - u_start) / u_resolution
        delta_v = (v_end - v_start) / v_resolution

        positions = []
        for u_index in range(u_resolution + 1):
            xyz_array = []
            for v_index in range(v_resolution + 1):
                u = u_start + u_index * delta_u
                v = v_start + v_index * delta_v
                xyz_array.append(surface_function(u, v))
            positions.append(xyz_array)

        uvs = []
        for u_index in range(u_resolution + 1):
            uv_array = []
            for v_index in range(v_resolution + 1):
                u = u_index / u_resolution
                v = v_index / v_resolution
                uv_array.append([u, v])
            uvs.append(uv_array)
        
        # Normals
        def calc_normal(p0, p1, p2):
            """Face normals to each triangle"""
            v1 = numpy.array(p1) - numpy.array(p0)
            v2 = numpy.array(p2) - numpy.array(p0)
            normal = numpy.cross(v1, v2)
            normal = normal / numpy.linalg.norm(normal)
            return normal

        vertex_normals = []
        for u_index in range(u_resolution+1):
            v_array = []
            for v_index in range(v_resolution+1):
                u = u_start + u_index * delta_u
                v = v_start + v_index + delta_v
                h = 0.0001
                p_A = surface_function(u, v)
                p_B = surface_function(u+h, v)
                p_C = surface_function(u, v+h)
                normal_vector = calc_normal(p_A, p_B, p_C)
                v_array.append(normal_vector)
            vertex_normals.append(v_array)

        # Store vertex data
        position_data = []
        color_data = []
        uv_data = []
        # default vertex colors
        c1, c2, c3 = [1, 0, 0], [0, 1, 0], [0, 0, 1]
        c4, c5, c6 = [0, 1, 1], [1, 0, 1], [1, 1, 0]

        # Group vertex data into triangles
        # Note: .copy() is necessary to avoid storing references
        vertex_normal_data = []
        face_normal_data = []
        for x_index in range(u_resolution):
            for y_index in range(v_resolution):
                # position data
                p0 = positions[x_index + 0][y_index + 0]
                p1 = positions[x_index + 1][y_index + 0]
                p3 = positions[x_index + 0][y_index + 1]
                p2 = positions[x_index + 1][y_index + 1]
                position_data += [p0.copy(), p1.copy(), p2.copy(),
                                  p0.copy(), p2.copy(), p3.copy()]
                # color data
                color_data += [c1, c2, c3, c4, c5, c6]
                # uv data (texture coordinates)
                uv_a = uvs[x_index + 0][y_index + 0]
                uv_b = uvs[x_index + 1][y_index + 0]
                uv_d = uvs[x_index + 0][y_index + 1]
                uv_c = uvs[x_index + 1][y_index + 1]
                uv_data += [uv_a, uv_b, uv_c,
                            uv_a, uv_c, uv_d]
                # vertex normal vectors
                n0 = vertex_normals[x_index+0][y_index+0]
                n1 = vertex_normals[x_index+1][y_index+0]
                n3 = vertex_normals[x_index+0][y_index+1]
                n2 = vertex_normals[x_index+1][y_index+1]
                vertex_normal_data += [n0, n1, n2, n0, n2, n3]

                # face normal vectors
                fn0 = calc_normal(p0, p1, p2)
                fn1 = calc_normal(p0, p2, p3)
                face_normal_data += [fn0, fn0, fn0, fn1, fn1, fn1]

        self.add_attribute("vec3", "vertexPosition",  position_data)
        self.add_attribute("vec3", "vertexColor", color_data)
        self.add_attribute("vec2", "vertexUV", uv_data)
        self.add_attribute("vec3", "vertexNormal", vertex_normal_data)
        self.add_attribute("vec3", "faceNormal", face_normal_data)
        self.count_vertices()
