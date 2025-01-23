from manim import *

class NeuralNetworkToMatrix(Scene):
    def construct(self):
        NODE_COLOR = BLUE
        EDGE_COLOR = GRAY
        NODE_RADIUS = 0.3
        VERTICAL_SPACING = 1.5

        def create_arrow_between_nodes(start_node, end_node, weight_index, position_type):
            if isinstance(start_node, VGroup):
                start_center = start_node[0].get_center()
            else:
                start_center = start_node.get_center()

            if isinstance(end_node, VGroup):
                end_center = end_node[0].get_center()
            else:
                end_center = end_node.get_center()

            direction = end_center - start_center
            unit_vector = direction / np.linalg.norm(direction)

            start_point = start_center + unit_vector * NODE_RADIUS
            end_point = end_center - unit_vector * NODE_RADIUS

            arrow = Arrow(
                start_point,
                end_point,
                buff=0,
                color=EDGE_COLOR,
                tip_length=0.15
            )

            weight_label = MathTex(f"w_{weight_index}", font_size=24)

            if position_type == "normal":
                label_position = arrow.point_from_proportion(0.5)
                offset = np.array([0, 0.2, 0])
            elif position_type == "top_crossing":
                label_position = arrow.point_from_proportion(0.25)
                offset = np.array([0, 0.2, 0])
            elif position_type == "bottom_crossing":
                label_position = arrow.point_from_proportion(0.15)
                offset = np.array([0, 0.3, 0])

            weight_label.move_to(label_position + offset)
            return arrow, weight_label

        input_layer_circles = VGroup(
            *[Circle(radius=NODE_RADIUS, color=NODE_COLOR, fill_opacity=0.3) for _ in range(2)]
        )
        input_labels = VGroup(
            MathTex("x_1", font_size=36),
            MathTex("x_2", font_size=36)
        )
        input_layer = VGroup()
        for circ, lbl in zip(input_layer_circles, input_labels):
            lbl.move_to(circ.get_center())
            input_layer.add(VGroup(circ, lbl))

        # Hidden layer (2 circles)
        hidden_layer = VGroup(*[
            Circle(radius=NODE_RADIUS, color=NODE_COLOR, fill_opacity=0.3)
            for _ in range(2)
        ])

        # Output layer (1 circle)
        output_layer = Circle(radius=NODE_RADIUS, color=NODE_COLOR, fill_opacity=0.3)

        # Arrange them
        input_layer.arrange(DOWN, buff=VERTICAL_SPACING).move_to(LEFT * 6)
        hidden_layer.arrange(DOWN, buff=VERTICAL_SPACING).move_to(LEFT * 0)
        output_layer.move_to(RIGHT * 4)

        edges = VGroup()
        weight_labels = VGroup()

        # Input->Hidden: w1, w2, w3, w4
        input_hidden_specs = [
            (0, 0, 1, "normal"),
            (1, 0, 3, "bottom_crossing"),
            (0, 1, 2, "top_crossing"),
            (1, 1, 4, "normal")
        ]
        for s, e, w_idx, p_type in input_hidden_specs:
            arr, wlbl = create_arrow_between_nodes(
                input_layer[s], hidden_layer[e], w_idx, p_type
            )
            edges.add(arr)
            weight_labels.add(wlbl)

        # Hidden->Output: w5, w6
        hidden_to_output = [
            (0, None, 5, "top_crossing"),
            (1, None, 6, "bottom_crossing")
        ]
        for s, _, w_idx, p_type in hidden_to_output:
            arr, wlbl = create_arrow_between_nodes(
                hidden_layer[s], output_layer, w_idx, p_type
            )
            edges.add(arr)
            weight_labels.add(wlbl)

        input_label = Text("Input Layer", font_size=24).next_to(input_layer, UP)
        hidden_label = Text("Hidden Layer", font_size=24).next_to(hidden_layer, UP)
        output_label = Text("Output Layer", font_size=24).next_to(output_layer, UP)

        self.play(
            Create(input_layer[0][0]),
            Create(input_layer[1][0]),
            run_time=1.0
        )

        self.play(
            Write(input_layer[0][1]),
            Write(input_layer[1][1]),
            run_time=0.8
        )

        self.play(
            Create(hidden_layer[0]),
            Create(hidden_layer[1]),
            run_time=1.0
        )

        for ar, wlbl in zip(edges[:4], weight_labels[:4]):
            self.play(Create(ar), Write(wlbl), run_time=0.4)

        self.play(Create(output_layer), run_time=0.8)

        for ar, wlbl in zip(edges[4:], weight_labels[4:]):
            self.play(Create(ar), Write(wlbl), run_time=0.4)

        self.play(
            Write(input_label),
            Write(hidden_label),
            Write(output_label),
            run_time=1.5
        )

        edges_first_node = VGroup(edges[0], edges[1])
        edges_second_node = VGroup(edges[2], edges[3])

        def create_pulse_animation(edge_group, color):
            return AnimationGroup(
                *[edge.animate.set_color(color) for edge in edge_group],
                lag_ratio=0
            )

        for _ in range(2):
            self.play(create_pulse_animation(edges_first_node, RED), run_time=0.4)
            self.play(create_pulse_animation(edges_first_node, GRAY), run_time=0.4)
            self.play(create_pulse_animation(edges_second_node, GREEN_D), run_time=0.4)
            self.play(create_pulse_animation(edges_second_node, GRAY), run_time=0.4)


        input_matrix = MathTex("\\begin{bmatrix} x_1 & x_2 \\end{bmatrix}").scale(1.2)
        weight_matrix = MathTex("\\begin{bmatrix} w_1 & w_2 \\\\ w_3 & w_4 \\end{bmatrix}").scale(1.2)
        hidden_matrix = MathTex("\\begin{bmatrix} a_1 & a_2 \\end{bmatrix}").scale(1.2)

        input_matrix.move_to(LEFT * 6)
        hidden_matrix.move_to(LEFT * 0)
        weight_matrix.move_to(LEFT * 3)

        mult_sign = MathTex("\\times").scale(1.2)
        equals_sign = MathTex("=").scale(1.2)
        mult_sign.move_to(midpoint(input_matrix.get_right(), weight_matrix.get_left()))
        equals_sign.move_to(midpoint(weight_matrix.get_right(), hidden_matrix.get_left()))

        self.play(
            FadeOut(edges),
            FadeOut(weight_labels),
            FadeOut(output_layer),
            FadeOut(output_label),   
            run_time=1.3
        )

        self.play(
            ReplacementTransform(VGroup(*input_layer), input_matrix),
            run_time=1.3
        )
        self.play(Write(mult_sign))
        self.play(Write(weight_matrix), run_time=1.5)
        self.play(Write(equals_sign))
        self.play(
            ReplacementTransform(hidden_layer, hidden_matrix),
            run_time=1.3
        )

        left_side1 = MathTex("a_1", "=")
        right_side1 = MathTex("x_1w_1 + x_2w_3")
        left_side2 = MathTex("a_2", "=")
        right_side2 = MathTex("x_1w_2 + x_2w_4")

        eq1 = VGroup(left_side1, right_side1)
        eq2 = VGroup(left_side2, right_side2)
        for eq in [eq1, eq2]:
            eq[1].next_to(eq[0], RIGHT, buff=0.15)

        eq_group = VGroup(eq1, eq2).arrange(DOWN, buff=0.5).scale(0.9)
        eq_group.next_to(hidden_matrix, RIGHT, buff=1)

        rect_w = eq_group.width + 0.6
        rect_h = eq_group.height + 0.4
        rectangle = Rectangle(width=rect_w, height=rect_h, color=YELLOW)
        rectangle.move_to(eq_group)
        rectangle.set_x(eq_group.get_left()[0] + rectangle.width/2 + 0.1)
        eq_group.set_x(rectangle.get_center()[0])

        self.play(Create(rectangle))
        self.play(
            Write(VGroup(left_side1, right_side1, left_side2, right_side2)),
            run_time=1.5
        )

        sigma1 = MathTex("\\sigma(", ")", font_size=36)
        sigma2 = MathTex("\\sigma(", ")", font_size=36)

        shift_amt = 0.4
        target_rect = Rectangle(
            width=rect_w + shift_amt,
            height=rect_h,
            color=YELLOW
        )
        target_rect.move_to(rectangle)
        target_rect.set_x(rectangle.get_left()[0] + target_rect.width/2)

        self.play(Transform(rectangle, target_rect), run_time=0.8)
        self.play(
            right_side1.animate.shift(RIGHT * shift_amt),
            right_side2.animate.shift(RIGHT * shift_amt),
            run_time=0.8
        )

        for sig, eq in [(sigma1, eq1), (sigma2, eq2)]:
            sig[0].next_to(eq[0], RIGHT, buff=0.08)
            sig[1].next_to(eq[1], RIGHT, buff=0.08)
        self.play(
            *[Write(part) for sig in [sigma1, sigma2] for part in sig],
            run_time=1.0
        )

        self.wait(2)
        self.play(
            FadeOut(rectangle),
            FadeOut(VGroup(left_side1, right_side1, left_side2, right_side2)),
            FadeOut(VGroup(sigma1[0], sigma1[1], sigma2[0], sigma2[1])),
            run_time=1.0
        )

        final_input_layer = VGroup(*[
            VGroup(
                Circle(radius=NODE_RADIUS, color=NODE_COLOR, fill_opacity=0.3),
                MathTex(f"x_{i+1}", font_size=36)
            ) for i in range(2)
        ]).arrange(DOWN, buff=VERTICAL_SPACING)
        for grp in final_input_layer:
            grp[1].move_to(grp[0].get_center())
        final_input_layer.move_to(LEFT * 6)

        final_hidden_layer = VGroup(*[
            VGroup(
                Circle(radius=NODE_RADIUS, color=NODE_COLOR, fill_opacity=0.3),
                MathTex(f"a_{i+1}", font_size=36)
            ) for i in range(2)
        ]).arrange(DOWN, buff=VERTICAL_SPACING)
        for grp in final_hidden_layer:
            grp[1].move_to(grp[0].get_center())
        final_hidden_layer.move_to(LEFT * 0)

        final_output_layer = VGroup(
            Circle(radius=NODE_RADIUS, color=NODE_COLOR, fill_opacity=0.3),
            MathTex("", font_size=36)
        )
        final_output_layer[1].move_to(final_output_layer[0].get_center())
        final_output_layer.move_to(RIGHT * 4)

        self.play(
            ReplacementTransform(hidden_matrix, VGroup(*final_hidden_layer)),
            ReplacementTransform(input_matrix, VGroup(*final_input_layer)),
            FadeOut(weight_matrix),
            FadeOut(mult_sign),
            FadeOut(equals_sign),
            input_label.animate.next_to(final_input_layer, UP),
            hidden_label.animate.next_to(final_hidden_layer, UP),
            run_time=1.5
        )

        self.play(
            Create(final_output_layer[0]),
            Write(final_output_layer[1]),
            Write(output_label),
            run_time=1.2
        )

        final_edges = VGroup()
        final_wlabels = VGroup()

        back_specs = [
            (0, 0, 1, "normal"),
            (0, 1, 2, "top_crossing"),
            (1, 0, 3, "bottom_crossing"),
            (1, 1, 4, "normal")
        ]
        for s_i, e_i, w_i, pos_t in back_specs:
            ar, w_l = create_arrow_between_nodes(
                final_input_layer[s_i],
                final_hidden_layer[e_i],
                w_i,
                pos_t
            )
            final_edges.add(ar)
            final_wlabels.add(w_l)

        ho_specs = [
            (0, None, 5, "top_crossing"),
            (1, None, 6, "bottom_crossing")
        ]
        for s_i, _, w_i, pos_t in ho_specs:
            ar, w_l = create_arrow_between_nodes(
                final_hidden_layer[s_i],
                final_output_layer,
                w_i,
                pos_t
            )
            final_edges.add(ar)
            final_wlabels.add(w_l)

        for ar, w_l in zip(final_edges, final_wlabels):
            self.play(Create(ar), Write(w_l), run_time=0.4)

        self.wait(2)

        hidden_matrix_2 = MathTex("\\begin{bmatrix} a_1 & a_2 \\end{bmatrix}").scale(1.2)
        weight_matrix_2 = MathTex("\\begin{bmatrix} w_5 \\\\ w_6 \\end{bmatrix}").scale(1.2)
        output_matrix_2 = MathTex("\\begin{bmatrix} y \\end{bmatrix}").scale(1.2)

        hidden_matrix_2.move_to(LEFT * 6)
        weight_matrix_2.move_to(LEFT * 3)
        output_matrix_2.move_to(LEFT * 0)

        mult_sign_2 = MathTex("\\times").scale(1.2)
        equals_sign_2 = MathTex("=").scale(1.2)
        mult_sign_2.move_to(midpoint(hidden_matrix_2.get_right(), weight_matrix_2.get_left()))
        equals_sign_2.move_to(midpoint(weight_matrix_2.get_right(), output_matrix_2.get_left()))

        w5_label = final_wlabels[-2]
        w6_label = final_wlabels[-1]

        w5_arrow = final_edges[-2]
        w6_arrow = final_edges[-1]

        self.play(
            FadeOut(final_input_layer),
            FadeOut(input_label),
            FadeOut(w5_arrow),
            FadeOut(w6_arrow),
            *[FadeOut(ar) for ar in final_edges[:-2]],   # w1..w4 arrows
            *[FadeOut(lbl) for lbl in final_wlabels[:-2]],  # w1..w4 labels
            run_time=1.3
        )

        self.play(
            ReplacementTransform(VGroup(*final_hidden_layer), hidden_matrix_2),
            ReplacementTransform(final_output_layer, output_matrix_2),
            ReplacementTransform(VGroup(w5_label, w6_label), weight_matrix_2),
            hidden_label.animate.next_to(hidden_matrix_2, UP),
            output_label.animate.next_to(output_matrix_2, UP),
            run_time=1.6
        )

        self.play(Write(mult_sign_2), Write(equals_sign_2), run_time=1.0)

        final_eq = MathTex("y = \\sigma(a_1w_5 + a_2w_6)").scale(1.2)
        final_eq.next_to(output_matrix_2, RIGHT, buff=1.5)
        final_eq.shift(LEFT * 0.4 + UP * 2.0)  

        eq_rect = Rectangle(
            width=final_eq.width + 0.4,
            height=final_eq.height + 0.4,
            color=YELLOW
        )
        eq_rect.move_to(final_eq)

        self.play(Create(eq_rect), Write(final_eq), run_time=1.5)
        self.wait(2)

        final_final_input_layer = VGroup(*[
            VGroup(
                Circle(radius=NODE_RADIUS, color=NODE_COLOR, fill_opacity=0.3),
                MathTex(f"x_{i+1}", font_size=36)
            ) for i in range(2)
        ]).arrange(DOWN, buff=VERTICAL_SPACING)
        for grp in final_final_input_layer:
            grp[1].move_to(grp[0].get_center())
        final_final_input_layer.move_to(LEFT * 6)

        final_final_hidden_layer = VGroup(*[
            VGroup(
                Circle(radius=NODE_RADIUS, color=NODE_COLOR, fill_opacity=0.3),
                MathTex(f"a_{i+1}", font_size=36)
            ) for i in range(2)
        ]).arrange(DOWN, buff=VERTICAL_SPACING)
        for grp in final_final_hidden_layer:
            grp[1].move_to(grp[0].get_center())
        final_final_hidden_layer.move_to(LEFT * 0)

        final_final_output_layer = VGroup(
            Circle(radius=NODE_RADIUS, color=NODE_COLOR, fill_opacity=0.3),
            MathTex("y", font_size=36)
        )
        final_final_output_layer[1].move_to(final_final_output_layer[0].get_center())
        final_final_output_layer.move_to(RIGHT * 4)

        final_input_label = Text("Input Layer", font_size=24)
        final_hidden_label = Text("Hidden Layer", font_size=24)
        final_output_label = Text("Output Layer", font_size=24)

        final_input_label.next_to(final_final_input_layer, UP)
        final_hidden_label.next_to(final_final_hidden_layer, UP)
        final_output_label.next_to(final_final_output_layer, UP)

        self.play(
            FadeOut(eq_rect),
            FadeOut(final_eq),
            FadeOut(mult_sign_2),
            FadeOut(equals_sign_2),
            run_time=1.0
        )

        self.play(
            ReplacementTransform(hidden_matrix_2, final_final_input_layer),
            ReplacementTransform(output_matrix_2, final_final_output_layer),
            FadeOut(weight_matrix_2),
            Create(final_final_hidden_layer),
            ReplacementTransform(hidden_label, final_hidden_label),
            ReplacementTransform(output_label, final_output_label),
            Write(final_input_label),
            run_time=1.6
        )

        final2_edges = VGroup()
        final2_labels = VGroup()

        recon_input_to_hidden = [
            (0, 0, 1, "normal"),
            (0, 1, 2, "top_crossing"),
            (1, 0, 3, "bottom_crossing"),
            (1, 1, 4, "normal")
        ]
        for sidx, eidx, widx, pos in recon_input_to_hidden:
            arrow, wlbl = create_arrow_between_nodes(
                final_final_input_layer[sidx],
                final_final_hidden_layer[eidx],
                widx,
                pos
            )
            final2_edges.add(arrow)
            final2_labels.add(wlbl)

        recon_hidden_to_out = [
            (0, None, 5, "top_crossing"),
            (1, None, 6, "bottom_crossing")
        ]
        for sidx, _, widx, pos in recon_hidden_to_out:
            arrow, wlbl = create_arrow_between_nodes(
                final_final_hidden_layer[sidx],
                final_final_output_layer,
                widx,
                pos
            )
            final2_edges.add(arrow)
            final2_labels.add(wlbl)

        for arrow, wlbl in zip(final2_edges, final2_labels):
            self.play(Create(arrow), Write(wlbl), run_time=0.4)

        self.wait(2)

class GradientCalculation(Scene):
    def construct(self):
        NODE_COLOR = BLUE
        EDGE_COLOR = GRAY
        NODE_RADIUS = 0.3
        VERTICAL_SPACING = 1.5
        GRADIENT_COLOR = RED_D
        
        existing_network = self.mobjects
        target_position = UP * 2
        self.play(
            *[mob.animate.shift(target_position) for mob in existing_network],
            run_time=1.5
        )
        
        gradient_title = Text("Gradient Storage", font_size=24)
        gradient_title.to_edge(DOWN).shift(DOWN * 0.5)
        
        grad_input_layer = VGroup(*[
            Circle(radius=NODE_RADIUS, color=GRADIENT_COLOR, fill_opacity=0.2)
            for _ in range(2)
        ])
        grad_input_layer.arrange(DOWN, buff=VERTICAL_SPACING)
        grad_input_layer.move_to(LEFT * 6)  
            
        grad_hidden_layer = VGroup(*[
            Circle(radius=NODE_RADIUS, color=GRADIENT_COLOR, fill_opacity=0.2)
            for _ in range(2)
        ])
        grad_hidden_layer.arrange(DOWN, buff=VERTICAL_SPACING)
        grad_hidden_layer.move_to(LEFT * 0)  
            
        grad_output_layer = Circle(radius=NODE_RADIUS, color=GRADIENT_COLOR, fill_opacity=0.2)
        grad_output_layer.move_to(RIGHT * 4)  
        
        grad_network = VGroup(grad_input_layer, grad_hidden_layer, grad_output_layer)
        grad_network.shift(DOWN * 2)
        
        grad_edges = VGroup()
        grad_labels = VGroup()
        
        def create_gradient_arrow(start_node, end_node, weight_index, position_type="normal"):
            if isinstance(start_node, VGroup):
                start_center = start_node.get_center()
            else:
                start_center = start_node.get_center()

            if isinstance(end_node, VGroup):
                end_center = end_node.get_center()
            else:
                end_center = end_node.get_center()

            direction = end_center - start_center
            unit_vector = direction / np.linalg.norm(direction)

            start_point = start_center + unit_vector * NODE_RADIUS
            end_point = end_center - unit_vector * NODE_RADIUS

            arrow = Arrow(
                start_point,
                end_point,
                buff=0,
                color=GRADIENT_COLOR,
                tip_length=0.15
            )

            weight_label = MathTex(f"\\Delta w_{weight_index}", color=GRADIENT_COLOR, font_size=24)

            if position_type == "normal":
                label_position = arrow.point_from_proportion(0.5)
                offset = np.array([0, 0.2, 0])
            elif position_type == "top_crossing":
                label_position = arrow.point_from_proportion(0.25)
                offset = np.array([0, 0.2, 0])
            elif position_type == "bottom_crossing":
                label_position = arrow.point_from_proportion(0.15)
                offset = np.array([0, 0.3, 0])

            weight_label.move_to(label_position + offset)
            return arrow, weight_label

        input_hidden_specs = [
            (0, 0, 1, "normal"),
            (0, 1, 2, "top_crossing"),
            (1, 0, 3, "bottom_crossing"),
            (1, 1, 4, "normal")
        ]
        for s, e, w_idx, pos_type in input_hidden_specs:
            arrow, label = create_gradient_arrow(
                grad_input_layer[s], grad_hidden_layer[e], w_idx, pos_type
            )
            grad_edges.add(arrow)
            grad_labels.add(label)
            
        hidden_output_specs = [
            (0, None, 5, "top_crossing"),
            (1, None, 6, "bottom_crossing")
        ]
        for s, _, w_idx, pos_type in hidden_output_specs:
            arrow, label = create_gradient_arrow(
                grad_hidden_layer[s], grad_output_layer, w_idx, pos_type
            )
            grad_edges.add(arrow)
            grad_labels.add(label)
        
        self.play(Write(gradient_title))
        
        self.play(
            *[Create(node) for node in grad_input_layer],
            *[Create(node) for node in grad_hidden_layer],
            Create(grad_output_layer),
            run_time=1.0
        )
        
        for edge, label in zip(grad_edges, grad_labels):
            self.play(
                Create(edge),
                Write(label),
                run_time=0.3
            )
        
        original_weight = [mob for mob in existing_network 
                         if isinstance(mob, MathTex) and "w_1" in mob.tex_string][0]
        gradient_weight = grad_labels[0]  # Δw₁
        
        self.play(
            original_weight.animate.set_color(EDGE_COLOR),
            gradient_weight.animate.set_color(GRADIENT_COLOR),
            run_time=1.0
        )
        
        update_text = MathTex("w = w - \\eta \\cdot \\Delta w", font_size=36)
        update_text.to_corner(UR, buff=0.5)
        update_text.shift(LEFT * 0.5 + DOWN * 2)
        
        central_diff = MathTex(
            "\\Delta w = \\frac{\\partial C}{\\partial w} \\approx \\frac{C(w + \\epsilon) - C(w - \\epsilon)}{2\\epsilon}",
            font_size=36
        )

        central_diff.next_to(update_text, DOWN, buff=1.0)  
        central_diff.shift(LEFT * 0.8)
        
        bg_rect = Rectangle(
            width=central_diff.width + 0.4,
            height=central_diff.height + 0.2,
            fill_color=BLACK,
            fill_opacity=0.8,
            stroke_width=0
        )
        bg_rect.move_to(central_diff)
        
        self.play(Write(update_text))
        self.play(
            FadeIn(bg_rect),
            Write(central_diff)
        )
        
        for i, (grad_label, orig_weight) in enumerate(zip(grad_labels, 
            [mob for mob in existing_network if isinstance(mob, MathTex) and "w_" in mob.tex_string])):
            self.play(
                grad_label.animate.set_color(YELLOW),
                orig_weight.animate.set_color(YELLOW),
                run_time=0.3
            )
            self.play(
                grad_label.animate.set_color(GRADIENT_COLOR),
                orig_weight.animate.set_color(EDGE_COLOR),
                run_time=0.3
            )
        
        self.wait(2)
        
class CombinedScene(Scene):
    def construct(self):
        NeuralNetworkToMatrix.construct(self)
        GradientCalculation.construct(self)
