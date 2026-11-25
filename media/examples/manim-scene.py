from manim import *


class Demo(Scene):
    def construct(self):
        self.camera.background_color = "#0B1020"
        t = Text("Mamat Media Forge", weight=BOLD, color="#E2E8F0").scale(0.9)
        c = Circle(radius=1.2, color="#38BDF8", stroke_width=6)
        self.play(Create(c), run_time=1.2)
        self.play(Transform(c, Square(side_length=2.2, color="#F472B6", fill_opacity=0.35)))
        self.play(Write(t), run_time=1.2)
        self.play(t.animate.to_edge(UP), FadeIn(Arrow(LEFT * 2, RIGHT * 2, color="#22C55E")))
        self.wait(0.6)
