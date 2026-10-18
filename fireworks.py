"""A dependency-free fireworks animation built with tkinter.

Run with: python fireworks.py
Click anywhere in the window to launch a firework.
"""

from __future__ import annotations

import math
import random
import tkinter as tk
from dataclasses import dataclass


WIDTH = 960
HEIGHT = 600
BACKGROUND = "#070b1a"
GRAVITY = 0.07
FRAME_MS = 16


@dataclass
class Particle:
    x: float
    y: float
    vx: float
    vy: float
    color: str
    life: int
    radius: float = 2.5

    def update(self) -> None:
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.992
        self.vy = self.vy * 0.992 + GRAVITY
        self.life -= 1
        self.radius = max(0.4, self.radius * 0.985)


class Fireworks:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.canvas = tk.Canvas(
            root,
            width=WIDTH,
            height=HEIGHT,
            bg=BACKGROUND,
            highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True)
        self.particles: list[Particle] = []
        self.frame = 0

        self.canvas.create_text(
            WIDTH // 2,
            35,
            text="Click anywhere to launch fireworks",
            fill="#9fb3ff",
            font=("Segoe UI", 16, "bold"),
        )
        self.canvas.bind("<Button-1>", self.on_click)
        self.animate()

    @staticmethod
    def random_color() -> str:
        palette = (
            "#ff4d6d",
            "#ffd166",
            "#06d6a0",
            "#4cc9f0",
            "#b517ff",
            "#f8f9fa",
        )
        return random.choice(palette)

    def explode(self, x: float, y: float) -> None:
        color = self.random_color()
        count = random.randint(55, 90)

        for index in range(count):
            angle = 2 * math.pi * index / count + random.uniform(-0.04, 0.04)
            speed = random.uniform(1.6, 5.8)
            self.particles.append(
                Particle(
                    x=x,
                    y=y,
                    vx=math.cos(angle) * speed,
                    vy=math.sin(angle) * speed,
                    color=color if random.random() > 0.15 else "#ffffff",
                    life=random.randint(55, 105),
                    radius=random.uniform(1.7, 3.2),
                )
            )

    def on_click(self, event: tk.Event) -> None:
        self.explode(event.x, event.y)

    def animate(self) -> None:
        self.canvas.delete("particle")

        alive: list[Particle] = []
        for particle in self.particles:
            particle.update()
            if particle.life <= 0 or particle.y > HEIGHT + 20:
                continue

            glow = particle.radius * 2.4
            self.canvas.create_oval(
                particle.x - glow,
                particle.y - glow,
                particle.x + glow,
                particle.y + glow,
                fill=particle.color,
                outline="",
                stipple="gray50",
                tags="particle",
            )
            self.canvas.create_oval(
                particle.x - particle.radius,
                particle.y - particle.radius,
                particle.x + particle.radius,
                particle.y + particle.radius,
                fill=particle.color,
                outline="",
                tags="particle",
            )
            alive.append(particle)

        self.particles = alive
        self.frame += 1

        if self.frame % 75 == 0 and len(self.particles) < 350:
            self.explode(
                random.randint(100, WIDTH - 100),
                random.randint(100, HEIGHT // 2),
            )

        self.root.after(FRAME_MS, self.animate)


def main() -> None:
    root = tk.Tk()
    root.title("Python Fireworks")
    root.geometry(f"{WIDTH}x{HEIGHT}")
    root.resizable(False, False)
    Fireworks(root)
    root.mainloop()


if __name__ == "__main__":
    main()
