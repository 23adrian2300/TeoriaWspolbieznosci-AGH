"""
Do tworzenia grafow wykorzystujemy biblioteke graphviz, wykorzystywana juz poprzednio w zadaniu domowym II. na podstawie stworzonych
zaleznosci dodajemy latwo odpowiednie wierzcholki oraz krawedzi i tworzymy graf. Pozostale funkcja zlozone sa do tworzenia kolorow
"""
import random

import graphviz

def generate_contrast_color(hex_color):
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)

    brightness = (r * 299 + g * 587 + b * 114) / 1000
    text_color = '#000000' if brightness > 128 else '#FFFFFF'

    return text_color

def blend_colors(color1, color2):
    r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
    r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)

    blended_color = "#{:02x}{:02x}{:02x}".format((r1 + r2) // 2, (g1 + g2) // 2, (b1 + b2) // 2)
    return blended_color

def draw_directed_graph(dependencies, name, FNF):
    dot = graphviz.Digraph(comment='Directed Graph')
    random.seed(10)

    color_dict = {}

    for i, fnf_list in enumerate(FNF):
        base_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        for node in fnf_list:
            if node not in color_dict:
                color_dict[node] = (base_color, generate_contrast_color(base_color))

    for dependency in dependencies:
        fill_color_node_0, text_color_node_0 = color_dict.get(dependency[0], ("#{:06x}".format(random.randint(0, 0xFFFFFF)), '#000000'))
        fill_color_node_1, text_color_node_1 = color_dict.get(dependency[1], ("#{:06x}".format(random.randint(0, 0xFFFFFF)), '#000000'))

        dot.node(dependency[0], style='filled', fillcolor=fill_color_node_0, fontcolor=text_color_node_0)
        dot.node(dependency[1], style='filled', fillcolor=fill_color_node_1, fontcolor=text_color_node_1)
        dot.edge(dependency[0], dependency[1])

    dot.render(f'graphs/directed_graph_{name}', format='png', cleanup=True)

