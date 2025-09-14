import matplotlib.pyplot as plt

def papier_millimetre_png(
    largeur_cm=18, 
    hauteur_cm=18, 
    marge_mm=1, 
    fichier="papier_millimetre.png",
    dpi=600
):
    """
    Génère une image PNG de papier millimétré noir et blanc.
    
    largeur_cm : largeur du quadrillage en cm (hors marge)
    hauteur_cm : hauteur du quadrillage en cm (hors marge)
    marge_mm   : marge blanche autour (ajoutée en plus)
    fichier    : nom du fichier de sortie
    dpi        : résolution de sortie (600 = qualité impression)
    """

    # Conversion cm -> mm
    largeur_mm = largeur_cm * 10
    hauteur_mm = hauteur_cm * 10

    # Dimensions totales incluant la marge
    largeur_totale_mm = largeur_mm + 2 * marge_mm
    hauteur_totale_mm = hauteur_mm + 2 * marge_mm

    # Épaisseur des traits
    epaisseur_1 = 0.2
    epaisseur_5 = 0.4
    epaisseur_10 = 0.8

    # Taille de la figure en pouces
    fig_w_in = largeur_totale_mm / 25.4
    fig_h_in = hauteur_totale_mm / 25.4
    fig = plt.figure(figsize=(fig_w_in, fig_h_in))
    ax = plt.axes([0, 0, 1, 1])

    ax.set_xlim(0, largeur_totale_mm)
    ax.set_ylim(0, hauteur_totale_mm)
    ax.set_aspect('equal', adjustable='box')
    ax.axis('off')

    xmin, xmax = marge_mm, marge_mm + largeur_mm
    ymin, ymax = marge_mm, marge_mm + hauteur_mm

    # Quadrillage
    for x in range(int(xmin), int(xmax) + 1):
        lw = epaisseur_1
        if (x - xmin) % 10 == 0:
            lw = epaisseur_10
        elif (x - xmin) % 5 == 0:
            lw = epaisseur_5
        ax.plot([x, x], [ymin, ymax], color="black", linewidth=lw)

    for y in range(int(ymin), int(ymax) + 1):
        lw = epaisseur_1
        if (y - ymin) % 10 == 0:
            lw = epaisseur_10
        elif (y - ymin) % 5 == 0:
            lw = epaisseur_5
        ax.plot([xmin, xmax], [y, y], color="black", linewidth=lw)

    # Bordure du quadrillage
    ax.plot(
        [xmin, xmax, xmax, xmin, xmin], 
        [ymin, ymin, ymax, ymax, ymin], 
        color="black", linewidth=epaisseur_10
    )

    # Sauvegarde en PNG
    fig.savefig(fichier, dpi=dpi, bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    print(f"✅ Fichier généré : {fichier}")


# Exemple : papier quadrillé 10 × 10 cm + marge 1 mm
papier_millimetre_png(10, 10, marge_mm=1, fichier="papier_10x10.png")
