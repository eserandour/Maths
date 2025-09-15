#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import math

def quadrillage_avec_axes(
    largeur_cm=20,
    hauteur_cm=20,
    marge_mm=10,           # marge blanche autour du quadrillage
    graduation_mm=10,      # espacement des graduations (10 mm = 1 cm)
    subdivisions=10,       # nb de subdivisions par cm (10 = millimétré)
    points=None,           # liste de points [(nom, x, y), ...] à afficher
    axe_x_cm=None,         # position de l'axe X (cm depuis le bas de la zone utile)
    axe_y_cm=None,         # position de l'axe Y (cm depuis la gauche de la zone utile)
    fichier="quadrillage.png",
    dpi=600,               # résolution d'export
    decal_fleche=1.5,      # dépassement des flèches (mm)
    depart_axes_ext=0.8    # dépassement des axes au départ (mm)
):
    """
    Génère un quadrillage avec axes fléchés, graduations, labels x et y,
    et affiche éventuellement des points donnés sous la forme (nom, x, y).
    - Les axes peuvent être centrés ou décalés si axe_x_cm / axe_y_cm sont donnés.
    - Pas de graduation à l'extrême gauche/bas, ni collée aux flèches (droite/haut),
      sauf le 0 qui est toujours affiché.
    """

    # Dimensions utiles en mm
    largeur_mm = int(round(largeur_cm * 10))
    hauteur_mm = int(round(hauteur_cm * 10))
    L_tot = largeur_mm + 2 * marge_mm
    H_tot = hauteur_mm + 2 * marge_mm

    # Figure
    fig_w_in, fig_h_in = L_tot / 25.4, H_tot / 25.4
    fig, ax = plt.subplots(figsize=(fig_w_in, fig_h_in))
    ax.set_xlim(0, L_tot)
    ax.set_ylim(0, H_tot)
    ax.set_aspect("equal")
    ax.axis("off")

    # Zone utile
    xmin, xmax = marge_mm, marge_mm + largeur_mm
    ymin, ymax = marge_mm, marge_mm + hauteur_mm

    # Position des axes
    if axe_x_cm is None:
        axe_x = ymin + hauteur_mm // 2
    else:
        axe_x = ymin + axe_x_cm * 10

    if axe_y_cm is None:
        axe_y = xmin + largeur_mm // 2
    else:
        axe_y = xmin + axe_y_cm * 10

    # Styles du quadrillage
    color_sub = "lightgrey"   # petites subdivisions
    color_mid = "silver"      # traits 5 mm
    color_cm  = "darkgrey"    # traits 1 cm
    thin, thick5, thick10 = 0.3, 0.6, 1.0

    # Subdivisions (mm entre petites lignes)
    pas_mm = 10 / subdivisions if subdivisions and subdivisions > 0 else 10

    # Grille verticale
    n_x = int((xmax - xmin) / pas_mm)
    for i in range(n_x + 1):
        x = xmin + i * pas_mm
        lw, col = thin, color_sub
        if abs((x - xmin) % 10) < 1e-6:          # chaque cm
            lw, col = thick10, color_cm
        elif subdivisions >= 5 and abs((x - xmin) % 5) < 1e-6:  # chaque 5 mm
            lw, col = thick5, color_mid
        ax.plot([x, x], [ymin, ymax], color=col, linewidth=lw)

    # Grille horizontale
    n_y = int((ymax - ymin) / pas_mm)
    for j in range(n_y + 1):
        y = ymin + j * pas_mm
        lw, col = thin, color_sub
        if abs((y - ymin) % 10) < 1e-6:
            lw, col = thick10, color_cm
        elif subdivisions >= 5 and abs((y - ymin) % 5) < 1e-6:
            lw, col = thick5, color_mid
        ax.plot([xmin, xmax], [y, y], color=col, linewidth=lw)

    eps = 1e-6

    # ---- Axe X
    if ymin <= axe_x <= ymax:
        ax.annotate(
            "", xy=(xmax + decal_fleche, axe_x), xytext=(xmin - depart_axes_ext, axe_x),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=1.2)
        )
        n_min = math.ceil((xmin - axe_y) / graduation_mm)
        n_max = math.floor((xmax - axe_y - graduation_mm) / graduation_mm)
        for n in range(n_min, n_max + 1):
            xg = axe_y + n * graduation_mm
            if abs(xg - xmin) < eps and n != 0:  # pas de graduation extrême gauche sauf 0
                continue
            if abs(xg - xmax) < eps:             # pas de graduation extrême droite
                continue
            ax.plot([xg, xg], [axe_x - 2, axe_x + 2], color="black", linewidth=1)
            ax.text(xg, axe_x - 3, str(n), ha="center", va="top", fontsize=7)
        ax.text(xmax + decal_fleche + 2, axe_x, "x",
                fontsize=9, color="black", va="center", ha="left")

    # ---- Axe Y
    if xmin <= axe_y <= xmax:
        ax.annotate(
            "", xy=(axe_y, ymax + decal_fleche), xytext=(axe_y, ymin - depart_axes_ext),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=1.2)
        )
        m_min = math.ceil((ymin - axe_x) / graduation_mm)
        m_max = math.floor((ymax - axe_x - graduation_mm) / graduation_mm)
        for m in range(m_min, m_max + 1):
            yg = axe_x + m * graduation_mm
            if abs(yg - ymin) < eps and m != 0:  # pas de graduation extrême bas sauf 0
                continue
            if abs(yg - ymax) < eps:             # pas de graduation extrême haut
                continue
            ax.plot([axe_y - 2, axe_y + 2], [yg, yg], color="black", linewidth=1)
            ax.text(axe_y - 3, yg, str(m), ha="right", va="center", fontsize=7)
        ax.text(axe_y, ymax + decal_fleche + 2, "y",
                fontsize=9, color="black", ha="center", va="bottom")

    # Origine (0;0)
    ax.text(axe_y, axe_x - 3, "0", ha="center", va="top", fontsize=7)

    # ---- Points (nom, x, y) : croix noire + nom rapproché
    if points:
        for (nom, px, py) in points:
            gx = axe_y + px * graduation_mm
            gy = axe_x + py * graduation_mm
            ax.plot(gx, gy, marker="x", color="black", markersize=6, markeredgewidth=1.2, linestyle="None")
            ax.text(gx + 2, gy + 2, nom, fontsize=8, color="black", ha="left", va="bottom")

    # Export
    fig.savefig(fichier, dpi=dpi, bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    print("✅ Fichier généré :", fichier)


# =====================
# Exemples d'utilisation
# =====================
if __name__ == "__main__":
    # Exemple 1 : Quadrillage centré (par défaut)
    quadrillage_avec_axes(
        largeur_cm=20, hauteur_cm=20,
        graduation_mm=10, subdivisions=10,
        fichier="quadrillage_centre.png"
    )

    # Exemple 2 : Quadrillage avec axes décalés
    quadrillage_avec_axes(
        largeur_cm=20, hauteur_cm=20,
        graduation_mm=10, subdivisions=10,
        axe_x_cm=6,   # axe des X placé à 6 cm du bas
        axe_y_cm=5,   # axe des Y placé à 5 cm de la gauche
        points=[("A", 2, 3), ("B", -1, 4), ("C", 7, -2)],
        fichier="quadrillage_axes_decales.png"
    )
