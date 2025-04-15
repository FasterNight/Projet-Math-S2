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
    p1 = [x0, y0, z0]  # arrière intérieur
    p2 = [x0 + back_length, y0, z0]  # avant intérieur

    # Pointe triangulaire sur même X que p1
    p3 = [x0, y0, z0 + sign * back_length ]  # pointe extérieure unique

    # Points hauts (Y = y0 + thickness)
    p5 = [p1[0], p1[1] + thickness, p1[2]]
    p6 = [p2[0], p2[1] + thickness, p2[2]]
    p7 = [p3[0], p3[1] + thickness, p3[2]]

    # Faces (triangulaires pour certaines)
    verts = [
        [p1, p2, p3],       # base inférieure
        [p5, p6, p7],       # face supérieure
        [p1, p2, p6, p5],   # intérieur (côté fuselage)
        [p2, p3, p7, p6],   # bord avant
        [p3, p1, p5, p7],   # bord arrière
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

    # Points bas (Y = y0)
    p1 = [x0, y0, z0]  # arrière intérieur
    p2 = [x0 + back_length, y0, z0]  # avant intérieur

    # Pointe triangulaire vers le haut, inverser la direction sur l'axe X
    p3 = [x0, y0 + span, z0]  # avant extérieur, sur le même X que p1 (fixé sur x0)

    # Points hauts (Y = y0 + thickness)
    p5 = [p1[0], p1[1] + thickness, p1[2]]  # haut arrière intérieur
    p6 = [p2[0], p2[1] + thickness, p2[2]]  # haut avant intérieur
    p7 = [p3[0], p3[1] + thickness, p3[2]]  # haut avant extérieur (pointe)

    # Faces (triangulaires pour certaines)
    verts = [
        [p1, p2, p3],       # base inférieure
        [p5, p6, p7],       # face supérieure
        [p1, p2, p6, p5],   # intérieur (côté fuselage)
        [p2, p3, p7, p6],   # bord avant
        [p3, p1, p5, p7],   # bord arrière
    ]

    ax.add_collection3d(Poly3DCollection(verts, facecolors='darkblue', alpha=0.9, edgecolors='black'))


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
    origin=(0, 0, -2),           # Position sur le fuselage 
    span=3.0,                   # largeur au contact du fuselage 
    front_length=15.0,          # bord avant 
    back_length=13.5,           # bord arrière 
    thickness=0.5,              # épaisseur 
    side='right'         
)

draw_wing(
    ax,
    origin=(0, 0, 2),         # Position sur le fuselage 
    span=3.0,                  # Largeur au contact du fuselage
    front_length=15.0,         # Bord avant
    back_length=13.5,          # Bord arrière
    thickness=0.5,             # Épaisseur 
    side='left'                
)

# Ailes arrières
draw_wing(
    ax,
    origin=(-19.75, 0, -2),      # Position sur le fuselage 
    span=2.5,                  # Largeur au contact du fuselage 
    front_length=6.5,          # Bord avant 
    back_length=5.5,           # Bord arrière 
    thickness=0.5,             # Épaisseur 
    side='right'              
)

draw_wing(
    ax,
    origin=(-19.75, 0, 2),     # Position sur le fuselage 
    span=2.5,                  # Largeur au contact du fuselage
    front_length=6.5,          # Bord avant
    back_length=5.5,           # Bord arrière
    thickness=0.5,             # Épaisseur 
    side='left'                
)

# Dérivé verticale
draw_wing_top(
    ax,
    origin=(-19.75, 2, 0),       # Position au-dessus du fuselage 
    span=4.0,                    # Largeur au contact du fuselage 
    front_length=5.0,            # Bord avant 
    back_length=4.5,             # Bord arrière 
    thickness=0.5,               # Épaisseur verticale 
    side='left'
)



# Axes
ax.quiver(0, 0, 0, 20, 0, 0, color='red')   # X
ax.quiver(0, 0, 0, 0, 20, 0, color='blue')  # Y
ax.quiver(0, 0, 0, 0, 0, 20, color='green') # Z

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

ax.set_xlim(-25, 25)   # Axe X : longueur de l’avion
ax.set_ylim(-5, 5)     # Axe Y : hauteur (épaisseur du fuselage + ailes)
ax.set_zlim(-10, 10)   # Axe Z : envergure


ax.set_box_aspect([2, 1, 1])
plt.tight_layout()
plt.show()
