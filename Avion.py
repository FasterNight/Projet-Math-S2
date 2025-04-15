import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from Tools import *
from Matrix import *

def cylindre_plein(ax, R, h, center=(0, 0, 0), resolution=20, color='gray', alpha=0.8):
    cx, cy, cz = center
    faces = []

    front_circle = []
    back_circle = []

    for i in range(resolution):
        theta = 2 * pi * i / resolution
        y = R * cos(theta)
        z = R * sin(theta)
        front_circle.append([cx, cy + y, cz + z])
        back_circle.append([cx + h, cy + y, cz + z])

    for i in range(resolution):
        next_i = (i + 1) % resolution
        p1 = front_circle[i]
        p2 = front_circle[next_i]
        p3 = back_circle[next_i]
        p4 = back_circle[i]
        faces.append([p1, p2, p3, p4])

    faces.append(front_circle)
    faces.append(back_circle[::-1]) 

    ax.add_collection3d(Poly3DCollection(faces, facecolors=color, alpha=alpha))


def draw_cone(ax, length, radius, center=(0, 0, 0), direction='x', reverse=False, resolution=50):
    theta = np.linspace(0, 2 * pi, resolution)
    z = np.linspace(0, length, resolution)
    theta, z = np.meshgrid(theta, z)

    r = (1 - z / length) * radius  

    if direction == 'x':
        if reverse:
            x = center[0] - z
        else:
            x = center[0] + z
        y = center[1] + r * np.cos(theta)
        z = center[2] + r * np.sin(theta)
    
    ax.plot_surface(x, y, z, color='orange', alpha=0.8)

def draw_wing(ax, origin, span, front_length, back_length, thickness, side='right'):
    """
    Dessine une aile trapézoïdale orientée vers l’avant (axe X), sur le côté du fuselage.
    
    origin: point d’ancrage (x, y, z)
    span: largeur du trapèze au contact du fuselage (le long de Z)
    front_length: longueur du bord avant (axe X)
    back_length: longueur du bord arrière (axe X)
    thickness: épaisseur verticale (axe Y)
    side: 'right' ou 'left' (Z− ou Z+)
    """

    x0, y0, z0 = origin
    sign = -1 if side == 'right' else 1

    # Points bas (Y = y0)
    p1 = [x0, y0, z0]  # arrière intérieur (côté fuselage)
    p2 = [x0 + back_length, y0, z0]  # avant intérieur

    p3 = [x0 + front_length, y0, z0 + sign * span]  # avant extérieur
    p4 = [x0, y0, z0 + sign * span]  # arrière extérieur

    # Points hauts (Y = y0 + thickness)
    p5 = [p1[0], p1[1] + thickness, p1[2]]
    p6 = [p2[0], p2[1] + thickness, p2[2]]
    p7 = [p3[0], p3[1] + thickness, p3[2]]
    p8 = [p4[0], p4[1] + thickness, p4[2]]

    verts = [
        [p1, p2, p3, p4],  # bas
        [p5, p6, p7, p8],  # haut
        [p1, p2, p6, p5],  # côté fuselage intérieur
        [p2, p3, p7, p6],  # bord avant
        [p3, p4, p8, p7],  # extérieur
        [p4, p1, p5, p8]   # bord arrière
    ]

    ax.add_collection3d(Poly3DCollection(verts, facecolors='darkblue', alpha=0.9, edgecolors='black'))

def draw_wing_top(ax, origin, span, front_length, back_length, thickness, side='right'):
    """
    Dessine une aile orientée le long de l'axe Y, attachée au fuselage.
    
    origin: point d’ancrage (x, y, z)
    span: largeur du trapèze au contact du fuselage (le long de X)
    front_length: longueur du bord avant (axe Z)
    back_length: longueur du bord arrière (axe Z)
    thickness: épaisseur verticale (axe Y)
    side: 'right' ou 'left' (X− ou X+)
    """
    
    x0, y0, z0 = origin
    sign = -1 if side == 'right' else 1

    # Points bas (X = x0)
    p1 = [x0, y0, z0]  # arrière intérieur (côté fuselage)
    p2 = [x0 + back_length, y0, z0]  # avant intérieur

    p3 = [x0 + front_length, y0 + sign * span, z0]  # avant extérieur
    p4 = [x0, y0 + sign * span, z0]  # arrière extérieur

    # Points hauts (X = x0 + thickness)
    p5 = [p1[0] + thickness, p1[1], p1[2]]
    p6 = [p2[0] + thickness, p2[1], p2[2]]
    p7 = [p3[0] + thickness, p3[1], p3[2]]
    p8 = [p4[0] + thickness, p4[1], p4[2]]

    verts = [
        [p1, p2, p3, p4],  # bas
        [p5, p6, p7, p8],  # haut
        [p1, p2, p6, p5],  # côté fuselage intérieur
        [p2, p3, p7, p6],  # bord avant
        [p3, p4, p8, p7],  # extérieur
        [p4, p1, p5, p8]   # bord arrière
    ]

    ax.add_collection3d(Poly3DCollection(verts, facecolors='blue', alpha=0.8, edgecolors='black'))


# Centre de l'avion
h = 39.5
g = 2
f = 6.5
r = 7

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

cylindre_plein(ax, R=g, h=h, center=(-19.75, 0, 0))
draw_cone(ax, length=f, radius=g, center=(-19.75, 0, 0), direction='x', reverse=True)
draw_cone(ax, length=r, radius=g, center=(19.75, 0, 0), direction='x')

# Ailes
base = 3.0
front = 15.0
back = 13.5
epaisseur = 0.5

wing_origin = (0, 0, 0)  


# Ailes Avant
draw_wing(
    ax,
    origin=(0, 0, 5),           # Position sur le fuselage 
    span=3.0,                   # largeur au contact du fuselage 
    front_length=15.0,          # bord avant 
    back_length=13.5,           # bord arrière 
    thickness=0.5,              # épaisseur 
    side='right'         
)

draw_wing(
    ax,
    origin=(0, 0, -5),         # Position sur le fuselage 
    span=3.0,                  # Largeur au contact du fuselage
    front_length=15.0,         # Bord avant
    back_length=13.5,          # Bord arrière
    thickness=0.5,             # Épaisseur 
    side='left'                
)

# Ailes arrières
draw_wing(
    ax,
    origin=(-19.75, 0, 4),      # Position sur le fuselage 
    span=2.5,                  # Largeur au contact du fuselage 
    front_length=6.5,          # Bord avant 
    back_length=5.5,           # Bord arrière 
    thickness=0.5,             # Épaisseur 
    side='right'              
)

draw_wing(
    ax,
    origin=(-19.75, 0, -4),     # Position sur le fuselage 
    span=2.5,                  # Largeur au contact du fuselage
    front_length=6.5,          # Bord avant
    back_length=5.5,           # Bord arrière
    thickness=0.5,             # Épaisseur 
    side='left'                
)

# Dérivé verticale
draw_wing_top(
    ax,
    origin=(-19.75, 5, 0),       # Position au-dessus du fuselage 
    span=4.0,                    # Largeur au contact du fuselage 
    front_length=5.0,            # Bord avant 
    back_length=4.5,             # Bord arrière 
    thickness=0.5,               # Épaisseur verticale 
)



# Axes
ax.quiver(0, 0, 0, 20, 0, 0, color='red')   # X
ax.quiver(0, 0, 0, 0, 20, 0, color='blue')  # Y
ax.quiver(0, 0, 0, 0, 0, 20, color='green') # Z

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')


ax.set_box_aspect([2, 1, 1])
plt.tight_layout()
plt.show()
