#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import math

def quadrillage_avec_axes(
    largeur_cm=20,
    hauteur_cm=20,
    marge_mm=10,
    subdivisions=10,     # nb de lignes par cm (10 = millimétré, 5 = tous les 2 mm, 1 = seulement cm)
    graduation_mm=10,    # espacement physique des graduations (mm) - 10 = 1 cm
    facteur_x=1.0,       # facteur d’échelle pour les valeurs affichées sur X
    facteur_y=1.0,       # facteur d’échelle pour les valeurs affichées sur Y
    axe_x_cm=None,       # position verticale de l’axe X (cm depuis le bas) ; None = centre
    axe_y_cm=None,       # position horizontale de l’axe Y (cm depuis la gauche) ; None = centre
    label_x="x",         # nom de l’axe des abscisses (mettre "" pour ne pas afficher)
    label_y="y",         # nom de l’axe des ordonnées (mettre "" pour ne pas afficher)
    points=None,         # ("A", x, y) ou ("A", x, y, {"offset_x_mm":..,"offset_y_mm":..})
    fonctions=None,      # ("f", f) | ("f", f, "couleur") | ("f", f, "couleur", {"offset_x_mm":..,"offset_y_mm":..})
    position_noms_fonctions="droite", # "milieu" ou "droite"
    nb_points=500,
    dpi=600,
    decal_fleche=1.4,    # dépassement de la flèche à droite/haut (mm)
    depart_axes_ext=0.8, # dépassement au départ à gauche/bas (mm)
    fichier="points_et_fonctions_dans_repere.png"
):

    if facteur_x <= 0 or facteur_y <= 0:
        raise ValueError("facteur_x et facteur_y doivent être > 0.")
    if position_noms_fonctions not in ("milieu", "droite"):
        raise ValueError('position_noms_fonctions doit être "milieu" ou "droite".')

    def fmt_fr(val: float) -> str:
        if abs(val) < 1e-12:
            val = 0.0
        if abs(val - round(val)) < 1e-9:
            return str(int(round(val)))
        s = f"{val:.12f}".rstrip('0').rstrip('.')
        return s.replace('.', ',')

    unit_to_mm_x = graduation_mm / facteur_x
    unit_to_mm_y = graduation_mm / facteur_y

    largeur_mm = int(round(largeur_cm * 10))
    hauteur_mm = int(round(hauteur_cm * 10))
    L_tot = largeur_mm + 2 * marge_mm
    H_tot = hauteur_mm + 2 * marge_mm

    fig_w_in, fig_h_in = L_tot / 25.4, H_tot / 25.4
    fig, ax = plt.subplots(figsize=(fig_w_in, fig_h_in))
    ax.set_xlim(0, L_tot)
    ax.set_ylim(0, H_tot)
    ax.set_aspect("equal")
    ax.axis("off")

    xmin, xmax = marge_mm, marge_mm + largeur_mm
    ymin, ymax = marge_mm, marge_mm + hauteur_mm

    axe_x = ymin + (hauteur_mm // 2) if axe_x_cm is None else ymin + axe_x_cm * 10
    axe_y = xmin + (largeur_mm // 2) if axe_y_cm is None else xmin + axe_y_cm * 10

    color_sub = "lightgrey"
    color_mid = "silver"
    color_cm  = "darkgrey"
    thin, thick5, thick10 = 0.3, 0.6, 1.0

    pas_mm = 10 / subdivisions if subdivisions and subdivisions > 0 else 10

    n_x = int((xmax - xmin) / pas_mm)
    for i in range(n_x + 1):
        x = xmin + i * pas_mm
        lw, col = thin, color_sub
        if abs((x - xmin) % 10) < 1e-6:
            lw, col = thick10, color_cm
        elif subdivisions >= 5 and abs((x - xmin) % 5) < 1e-6:
            lw, col = thick5, color_mid
        ax.plot([x, x], [ymin, ymax], color=col, linewidth=lw)

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

    if ymin <= axe_x <= ymax:
        ax.annotate("", xy=(xmax + decal_fleche, axe_x), xytext=(xmin - depart_axes_ext, axe_x),
                    arrowprops=dict(arrowstyle="->", color="black", linewidth=1.2))
        n_min = math.ceil((xmin - axe_y) / graduation_mm)
        n_max = math.floor((xmax - axe_y - graduation_mm) / graduation_mm)
        for n in range(n_min, n_max + 1):
            xg = axe_y + n * graduation_mm
            if abs(xg - xmin) < eps and n != 0:
                continue
            if abs(xg - xmax) < eps:
                continue
            ax.plot([xg, xg], [axe_x - 2, axe_x + 2], color="black", linewidth=1)
            ax.text(xg, axe_x - 3, fmt_fr(n * facteur_x), ha="center", va="top", fontsize=7)
        ax.text(xmax + decal_fleche + 2, axe_x, label_x, fontsize=9, va="center", ha="left")

    if xmin <= axe_y <= xmax:
        ax.annotate("", xy=(axe_y, ymax + decal_fleche), xytext=(axe_y, ymin - depart_axes_ext),
                    arrowprops=dict(arrowstyle="->", color="black", linewidth=1.2))
        m_min = math.ceil((ymin - axe_x) / graduation_mm)
        m_max = math.floor((ymax - axe_x - graduation_mm) / graduation_mm)
        for m in range(m_min, m_max + 1):
            yg = axe_x + m * graduation_mm
            if abs(yg - ymin) < eps and m != 0:
                continue
            if abs(yg - ymax) < eps:
                continue
            ax.plot([axe_y - 2, axe_y + 2], [yg, yg], color="black", linewidth=1)
            ax.text(axe_y - 3, yg, fmt_fr(m * facteur_y), ha="right", va="center", fontsize=7)
        ax.text(axe_y, ymax + decal_fleche + 2, label_y, fontsize=9, ha="center", va="bottom")

    ax.text(axe_y, axe_x - 3, "0", ha="center", va="top", fontsize=7)

    # ---- Points ----
    if points:
        for pt in points:
            nom, px, py = pt[0], pt[1], pt[2]
            opts = pt[3] if len(pt) >= 4 and isinstance(pt[3], dict) else {}
            off_x = opts.get("offset_x_mm", 2.0)
            off_y = opts.get("offset_y_mm", 2.0)

            gx = axe_y + px * unit_to_mm_x
            gy = axe_x + py * unit_to_mm_y
            ax.plot(gx, gy, marker="x", color="black", markersize=6, markeredgewidth=1.2, linestyle="None")
            ax.text(gx + off_x, gy + off_y, nom, fontsize=8, color="black", ha="left", va="bottom")

    # ---- Fonctions ----
    if fonctions:
        xmin_unit = (xmin - axe_y) / unit_to_mm_x
        xmax_unit = (xmax - axe_y) / unit_to_mm_x
        clip_rect = Rectangle((xmin, ymin), largeur_mm, hauteur_mm, transform=ax.transData)

        for f_def in fonctions:
            nom, f, col, opts = None, None, "black", {}
            if isinstance(f_def, tuple):
                if len(f_def) >= 1: nom = f_def[0]
                if len(f_def) >= 2: f = f_def[1]
                if len(f_def) >= 3: col = f_def[2] or "black"
                if len(f_def) >= 4 and isinstance(f_def[3], dict): opts = f_def[3]
            else:
                continue

            off_x = opts.get("offset_x_mm", 0.0)
            off_y = opts.get("offset_y_mm", 0.0)

            x_vals = np.linspace(xmin_unit, xmax_unit, nb_points)
            y_vals = np.array([f(x) for x in x_vals], dtype=float)
            gx = axe_y + x_vals * unit_to_mm_x
            gy = axe_x + y_vals * unit_to_mm_y

            line, = ax.plot(gx, gy, color=col, linewidth=1, clip_on=True)
            line.set_clip_path(clip_rect)

            if nom and len(gx) > 0:
                if position_noms_fonctions == "milieu":
                    idx = len(gx) // 2
                else:
                    inside = (gx <= xmax - 0.5) & (gx >= xmin + 0.5) & (gy >= ymin + 0.5) & (gy <= ymax - 0.5)
                    candidates = np.where(inside)[0]
                    idx = (candidates[-1] if len(candidates) > 0 else len(gx) - 1)
                tx = gx[idx] + off_x
                ty = gy[idx] + off_y
                ax.text(tx, ty, nom, fontsize=10, color=col, va="center", ha="left")

    fig.savefig(fichier, dpi=dpi, bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    print("✅ Fichier généré :", fichier)


# =====================
# Exemple
# =====================
if __name__ == "__main__":
    quadrillage_avec_axes(
        largeur_cm=20,
        hauteur_cm=20,
        subdivisions=10,
        graduation_mm=10,
        facteur_x=1.0,
        facteur_y=2.0,
        axe_x_cm=6,
        axe_y_cm=5,
        points=[
            ("A", 6, 5),
            ("B", 3, 2.5, {"offset_x_mm": 2, "offset_y_mm": -6}),
        ],
        fonctions=[
            ("f", lambda x: 0.5*x**2 - 2, "red",  {"offset_x_mm": 2, "offset_y_mm": -2}),
            ("g", lambda x: -x + 3,       "blue", {"offset_x_mm": -4, "offset_y_mm": 6}),
        ],
    )
