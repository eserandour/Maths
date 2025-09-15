#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

def papier_grille(
    largeur_cm=20,
    hauteur_cm=20,
    marge_mm=1,
    subdivisions=10,       # nb de lignes par cm (10 = millimétré, 5 = tous les 2 mm, 1 = seulement cm)
    fichier="papier_grille.png",
    dpi=600
):
    """
    Génère une image PNG de papier quadrillé (sans axes).
    - largeur_cm / hauteur_cm : dimensions utiles du quadrillage.
    - marge_mm : marge blanche autour.
    - subdivisions : nb de subdivisions par cm.
        * 10 = millimétré
        * 5 = tous les 2 mm
        * 1 = uniquement les cm
    - Le quadrillage affiche :
        * lignes fines pour les subdivisions,
        * lignes moyennes pour 5 mm,
        * lignes épaisses pour 1 cm.
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

    # ---------- Styles ----------
    color_sub = "lightgrey"   # petites subdivisions
    color_mid = "silver"      # lignes de 5 mm
    color_cm  = "darkgrey"    # lignes de 1 cm
    thin, thick5, thick10 = 0.3, 0.6, 1.0

    # ---------- Subdivisions ----------
    pas_mm = 10 / subdivisions if subdivisions and subdivisions > 0 else 10

    # Grille verticale
    n_x = int((xmax - xmin) / pas_mm)
    for i in range(n_x + 1):
        x = xmin + i * pas_mm
        lw, col = thin, color_sub
        if abs((x - xmin) % 10) < 1e-6:
            lw, col = thick10, color_cm
        elif subdivisions >= 5 and abs((x - xmin) % 5) < 1e-6:
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

    # ---------- Export ----------
    fig.savefig(fichier, dpi=dpi, bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    print("Fichier généré :", fichier)


# =====================
# Exemples d'utilisation
# =====================
if __name__ == "__main__":
    # Exemple 1 : Papier millimétré 20 x 20 cm
    papier_grille(
        largeur_cm=20, hauteur_cm=20,
        subdivisions=10,
        fichier="papier_millimetre.png"
    )

    # Exemple 2 : Quadrillage 20 x 20 cm avec lignes tous les 2 mm
    papier_grille(
        largeur_cm=20, hauteur_cm=20,
        subdivisions=5,
        fichier="papier_subdiv5.png"
    )

    # Exemple 3 : Quadrillage 20 x 20 cm avec seulement les cm
    papier_grille(
        largeur_cm=20, hauteur_cm=20,
        subdivisions=1,
        fichier="papier_cm.png"
    )
