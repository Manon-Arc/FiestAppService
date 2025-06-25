import pandas as pd
import os

# Chemin du fichier source
file_path = r'c:\Users\Utilisateur\Documents\B3_Dev\FiestAppService\src\data\data_soiree.csv'

# Chemin du fichier de sortie (dans le même dossier)
output_path = os.path.join(os.path.dirname(file_path), 'data_soiree_user.csv')

# Lecture du fichier CSV
df = pd.read_csv(file_path)

df = df.drop(columns=['saison'])
df = df.drop(columns=['heure_debut'])
df = df.drop(columns=['heure_fin'])
df = df.drop(columns=['lieu'])

# Sauvegarde du fichier sans la colonne
df.to_csv(output_path, index=False)

print(f"Fichier sauvegardé dans: {output_path}")