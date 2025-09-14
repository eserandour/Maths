#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import matplotlib.pyplot as plt

def _fmt(val: float) -> str:
    """Formate un nombre sans .0 inutile (ex.: 2.0 -> 2, 2.50 -> 2.5)."""
    s = f"{val:.2f}".rstrip("0").rstrip(".")
    return s if s else "0"

def papier_grille_axes(
    largeur_cm=20,
    hauteur_cm=20,
    marge_mm=10,
    subdivisions=10,         # nb de lignes par cm (10 = millimétré, 5 = tous les 2 mm, 1 = seulement cm)
    graduation_mm=10,        # espacement physique des graduations (mm) - 10 = 1 cm
    facteur_x=1.0,           # facteur d’échelle pour les valeurs affichées sur X
    facteur_y=1.0,           # facteur d’échelle pour les valeurs affichées sur Y
    axe_x_mm=None,           # position verticale de l’axe X (mm depuis le bas) ; None = centre
    axe_y_mm=None,           # position horizontale de l’axe Y (mm depuis la gauche) ; None = centre
    label_x="x",             # nom de l’axe des abscisses (mettre "" pour ne pas afficher)
    label_y="y",             # nom de l’axe des ordonnées (mettre "" pour ne pas afficher)
    fichier="papier_grille_axes.png",
    dpi=600,
    decal_fleche=1.4,        # dépassement de la flèche à droite/haut (mm)
    depart_axes_ext=0.8      # dépassement au départ à gauche/bas (mm)
):
    """
    Génère une image PNG de papier quadrillé avec axes fléchés.
    - Quadrillage gris (subdivisions/cm) renforcé à 5 mm et 1 cm, sans cadre.
    - Axes fléchés : X de (xmin - depart_axes_ext) -> (xmax + decal_fleche),
                     Y de (ymin - depart_axes_ext) -> (ymax + decal_fleche).
    - Graduations/labels tous les 'graduation_mm' (par défaut 1 cm),
      valeurs multipliées par facteur_x / facteur_y.
    - Pas de graduation collée aux flèches (côté droit/haut).
    - Pas de graduation extrême gauche/bas — SAUF le **0**, qui est toujours affiché.
    - Origine (0;0) = croisement des axes (axe_x_mm / axe_y_mm).
    """

    # ---------- Dimensions ----------
    largeur_mm = int(round(largeur_cm * 10))
    hauteur_mm = int(round(hauteur_cm * 10))
    L_tot = largeur_mm + 2 * marge_mm
    H_tot = hauteur_mm + 2 * marge_mm

    # ---------- Figure ----------
    fig_w_in, fig_h_in = L_tot / 25.4, H_tot / 25.4
    fig, ax = plt.subplots(figsize=(fig_w_in, fig_h_in))
    ax.set_xlim(0, L_tot)
    ax.set_ylim(0, H_tot)
    ax.set_aspect("equal")
    ax.axis("off")

    # ---------- Zone utile ----------
    xmin, xmax = marge_mm, marge_mm + largeur_mm
    ymin, ymax = marge_mm, marge_mm + hauteur_mm

    # ---------- Position des axes ----------
    axe_x = ymin + hauteur_mm // 2 if axe_x_mm is None else ymin + int(round(axe_x_mm))
    axe_y = xmin + largeur_mm  // 2 if axe_y_mm is None else xmin + int(round(axe_y_mm))

    # ---------- Styles ----------
    color_sub = "lightgrey"   # petites subdivisions
    color_mid = "silver"      # lignes de 5 mm
    color_cm  = "darkgrey"    # lignes de 1 cm
    thin, thick5, thick10 = 0.3, 0.6, 1.0

    # ---------- Subdivisions ----------
    pas_mm = 10 / subdivisions if subdivisions and subdivisions > 0 else 10

    # ---------- Grille VERTICALE ----------
    n_x = int((xmax - xmin) / pas_mm)
    for i in range(n_x + 1):
        x = xmin + i * pas_mm
        lw, col = thin, color_sub
        if abs((x - xmin) % 10) < 1e-6:
            lw, col = thick10, color_cm
        elif subdivisions >= 5 and abs((x - xmin) % 5) < 1e-6:
            lw, col = thick5, color_mid
        ax.plot([x, x], [ymin, ymax], color=col, linewidth=lw)

    # ---------- Grille HORIZONTALE ----------
    n_y = int((ymax - ymin) / pas_mm)
    for j in range(n_y + 1):
        y = ymin + j * pas_mm
        lw, col = thin, color_sub
        if abs((y - ymin) % 10) < 1e-6:
            lw, col = thick10, color_cm
        elif subdivisions >= 5 and abs((y - ymin) % 5) < 1e-6:
            lw, col = thick5, color_mid
        ax.plot([xmin, xmax], [y, y], color=col, linewidth=lw)

    # ---------- Axes fléchés + graduations ----------
    eps = 1e-6

    # Axe X
    if ymin <= axe_x <= ymax:
        ax.annotate(
            "", xy=(xmax + decal_fleche, axe_x), xytext=(xmin - depart_axes_ext, axe_x),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=1.2)
        )
        if graduation_mm > 0:
            n_min = math.ceil((xmin - axe_y) / graduation_mm)
            n_max = math.floor((xmax - axe_y - graduation_mm) / graduation_mm)
            for n in range(n_min, n_max + 1):
                xg = axe_y + n * graduation_mm
                # si la graduation est collée au bord gauche, on la saute sauf si c'est 0
                if abs(xg - xmin) < eps and n != 0:
                    continue
                ax.plot([xg, xg], [axe_x - 2, axe_x + 2], color="black", linewidth=1)
                val = (n * graduation_mm / 10.0) * facteur_x
                ax.text(xg, axe_x - 3, _fmt(val), ha="center", va="top", fontsize=7, color="black") #, fontweight="bold")
        if label_x:
            ax.text(xmax + decal_fleche + 2, axe_x, label_x,
                    fontsize=9, color="black", va="center", ha="left")

    # Axe Y
    if xmin <= axe_y <= xmax:
        ax.annotate(
            "", xy=(axe_y, ymax + decal_fleche), xytext=(axe_y, ymin - depart_axes_ext),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=1.2)
        )
        if graduation_mm > 0:
            m_min = math.ceil((ymin - axe_x) / graduation_mm)
            m_max = math.floor((ymax - axe_x - graduation_mm) / graduation_mm)
            for m in range(m_min, m_max + 1):
                yg = axe_x + m * graduation_mm
                # si la graduation est collée au bord bas, on la saute sauf si c'est 0
                if abs(yg - ymin) < eps and m != 0:
                    continue
                ax.plot([axe_y - 2, axe_y + 2], [yg, yg], color="black", linewidth=1)
                val = (m * graduation_mm / 10.0) * facteur_y
                ax.text(axe_y - 3, yg, _fmt(val), ha="right", va="center", fontsize=7, color="black") #, fontweight="bold")
        if label_y:
            ax.text(axe_y, ymax + decal_fleche + 2, label_y,
                    fontsize=9, color="black", ha="center", va="bottom")

    # ---------- Export ----------
    fig.savefig(fichier, dpi=dpi, bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    print("Fichier généré :", fichier)


# =====================
# Exemples d'utilisation
# =====================
"""
if __name__ == "__main__":
    # Exemple 1 : Millimétré, axes au centre, côtés négatifs visibles (par défaut)
    papier_grille_axes(
        largeur_cm=20, hauteur_cm=20,
        subdivisions=10, graduation_mm=10,
        facteur_x=1, facteur_y=1,
        label_x="x", label_y="y",
        fichier="papier_millimetre.png"
    )

    # Exemple 2 : Subdivisions 5 (tous les 2 mm), origine décalée,
    # Y en dizaines de cm, labels personnalisés
    papier_grille_axes(
        largeur_cm=20, hauteur_cm=20,
        subdivisions=5, graduation_mm=10,
        facteur_x=1, facteur_y=10,
        axe_x_mm=50, axe_y_mm=30,
        label_x="x", label_y="y",
        fichier="papier_subdiv5.png"
    )

    # Exemple 3 : Millimétré, axes au centre, échelles différentes X/Y
    papier_grille_axes(
        largeur_cm=20, hauteur_cm=20,
        subdivisions=10, graduation_mm=10,
        facteur_x=1, facteur_y=10,
        label_x="X", label_y="Y",
        fichier="papier_diff_echelles.png"
    )

    # Exemple 4 : Axes en bas à gauche (origine dans le coin),
    # vérifie que la graduation **0** s'affiche au bord
    papier_grille_axes(
        largeur_cm=20, hauteur_cm=20,
        subdivisions=10, graduation_mm=10,
        facteur_x=1, facteur_y=1,
        axe_x_mm=0, axe_y_mm=0,             # origine en (xmin, ymin)
        label_x="x (cm)", label_y="y (cm)",
        fichier="papier_axes_en_coin.png"
    )
"""

if __name__ == "__main__":
    papier_grille_axes(
        largeur_cm=20, hauteur_cm=20, marge_mm=10,
        subdivisions=5, graduation_mm=10,
        facteur_x=1, facteur_y=10,
        axe_x_mm=50, axe_y_mm=30,
        label_x="x", label_y="y",
        fichier="repere.png"
    )
