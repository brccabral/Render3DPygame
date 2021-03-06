from __future__ import annotations
import math
import numpy as np
import pygame
from matrix_functions import rotate_x, rotate_y

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import GameWindow


class Camera:
    def __init__(self, render: GameWindow, position):
        self.render = render
        self.position = np.array([*position, 1.0])
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])
        # horizontal and vertical field of view
        self.h_fov = math.pi / 3
        self.v_fov = self.h_fov * (render.height / render.width)
        # clip distance
        self.near_plane = 0.1
        self.far_plane = 100

        # movement
        self.moving_speed = 1.2
        self.rotation_speed = 0.5

    def control(self, dt):
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.position -= self.right * self.moving_speed * dt
        if key[pygame.K_d]:
            self.position += self.right * self.moving_speed * dt
        if key[pygame.K_w]:
            self.position += self.forward * self.moving_speed * dt
        if key[pygame.K_s]:
            self.position -= self.forward * self.moving_speed * dt
        if key[pygame.K_q]:
            self.position += self.up * self.moving_speed * dt
        if key[pygame.K_e]:
            self.position -= self.up * self.moving_speed * dt

        # rotation
        if key[pygame.K_LEFT]:
            self.camera_yaw(-self.rotation_speed * dt)
        if key[pygame.K_RIGHT]:
            self.camera_yaw(self.rotation_speed * dt)
        if key[pygame.K_DOWN]:
            self.camera_pitch(-self.rotation_speed * dt)
        if key[pygame.K_UP]:
            self.camera_pitch(self.rotation_speed * dt)

    def camera_yaw(self, angle):
        rotate = rotate_y(angle)
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def camera_pitch(self, angle):
        rotate = rotate_x(angle)
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def translate_matrix(self):
        x, y, z, w = self.position
        return np.array(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 1],
                [0, 0, 1, 0],
                [-x, -y, -z, 1],
            ]
        )

    def rotate_matrix(self):
        rx, ry, rz, w = self.right
        fx, fy, fz, w = self.forward
        ux, uy, uz, w = self.up
        return np.array(
            [
                [rx, ux, fx, 0],
                [ry, uy, fy, 0],
                [rz, uz, fz, 0],
                [0, 0, 0, 1],
            ]
        )

    def camera_matrix(self):
        return self.translate_matrix() @ self.rotate_matrix()
