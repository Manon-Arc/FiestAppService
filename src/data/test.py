import pandas as pd
import os

# Chemin du fichier source
file_path = r'c:\Users\Utilisateur\Documents\B3_Dev\FiestAppService\src\data\data_soiree_diversified_1000.csv'

# Chemin du fichier de sortie (dans le même dossier)
output_path = os.path.join(os.path.dirname(file_path), 'data_soiree_sans_boit_ce_soir.csv')

# Lecture du fichier CSV
df = pd.read_csv(file_path)

# Affichage des informations sur le fichier original
print(f"Dimensions originales: {df.shape}")
print(f"Colonnes originales: {', '.join(df.columns)}")

# Suppression de la colonne 'boit_ce_soir'
if 'boit_ce_soir' in df.columns:
    df = df.drop(columns=['boit_ce_soir'])
    print("Colonne 'boit_ce_soir' supprimée avec succès")
else:
    print("La colonne 'boit_ce_soir' n'existe pas dans le fichier")

# Affichage des informations sur le fichier modifié
print(f"Nouvelles dimensions: {df.shape}")
print(f"Nouvelles colonnes: {', '.join(df.columns)}")

# Sauvegarde du fichier sans la colonne
df.to_csv(output_path, index=False)

print(f"Fichier sans la colonne 'boit_ce_soir' sauvegardé dans: {output_path}")