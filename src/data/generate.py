import pandas as pd
import numpy as np
import os

def generate_realistic_profiles(n_samples=500):
    """
    Génère des profils utilisateurs hétérogènes en se basant sur des règles métier
    pour assurer le réalisme des données.
    """
    np.random.seed(42) # Pour des résultats reproductibles
    
    data = []
    
    for _ in range(n_samples):
        # 1. Générer les caractéristiques de base du profil
        genre = np.random.choice(['male', 'female'])
        age = np.random.randint(18, 55)
        conso_level = np.random.choice(['occasionally', 'regularly', 'seasoned'], p=[0.4, 0.4, 0.2])

        # Taille plus réaliste selon le genre
        if genre == 'male':
            taille = int(round(np.random.normal(178, 7)))  # Distribution normale autour de 178cm
            taille = max(160, min(200, taille))  # Limiter les valeurs extrêmes
        else: # femme
            taille = int(round(np.random.normal(165, 6)))  # Distribution normale autour de 165cm
            taille = max(150, min(185, taille))  # Limiter les valeurs extrêmes

        # Poids corrélé à la taille (basé sur un IMC moyen)
        imc_base = np.random.normal(24, 3)  # IMC moyen avec variation
        imc_base = max(18.5, min(35, imc_base))  # Limiter à des valeurs réalistes
        poids = int(round(imc_base * (taille ** 2)))

        # 2. Définir une consommation de BASE selon le niveau de consommation
        if conso_level == 'occasionally':
            base_biere = np.random.triangular(0, 1.5, 3)  # Pic autour de 1.5
            base_soft = np.random.triangular(2, 4, 6)     # Pic autour de 4
            base_pizza = np.random.triangular(3, 4, 6)    # Pic augmenté autour de 4
        elif conso_level == 'regularly':
            base_biere = np.random.triangular(2, 4, 6)    # Pic autour de 4
            base_soft = np.random.triangular(1, 3, 5)     # Pic autour de 3
            base_pizza = np.random.triangular(3, 5, 8)    # Pic augmenté autour de 5
        else: # seasoned
            base_biere = np.random.triangular(4, 6, 9)    # Pic autour de 6
            base_soft = np.random.triangular(0, 2, 4)     # Pic autour de 2
            base_pizza = np.random.triangular(4, 6, 9)    # Pic augmenté autour de 6

        # 3. Appliquer des MODIFICATEURS pour le réalisme
        
        # Modificateur de genre (plus précis)
        if genre == 'female':
            coef_genre = np.random.triangular(0.6, 0.8, 1.0)  # Réduction plus nuancée pour les femmes
            base_biere *= coef_genre
            base_soft *= 2 - coef_genre  # Compensation inversée pour les softs

        # Modificateur de corpulence (basé sur l'IMC plutôt que le poids brut)
        imc = poids / (taille ** 2)
        if imc < 20:  # Personne mince
            facteur_corpulence = 0.9
        elif imc < 25:  # Corpulence normale
            facteur_corpulence = 1.0
        elif imc < 30:  # Surpoids modéré
            facteur_corpulence = 1.1
        else:  # Surpoids important
            facteur_corpulence = 1.2
            
        base_pizza *= facteur_corpulence
        
        # Modificateur d'âge (plus nuancé)
        if genre == 'male':
            if age < 25:
                age_factor_biere = 0.9  # Jeunes hommes
            elif age < 35:
                age_factor_biere = 1.0  # Hommes jeunes adultes
            elif age < 45:
                age_factor_biere = 1.2  # Hommes d'âge moyen (pic de consommation)
            else:
                age_factor_biere = 1.1  # Hommes plus âgés
        else:  # femme
            if age < 25:
                age_factor_biere = 0.9  # Jeunes femmes
            elif age < 30:
                age_factor_biere = 1.0  # Femmes jeunes adultes
            else:
                age_factor_biere = 0.8  # Femmes plus âgées

        base_biere *= age_factor_biere
        
        # Les plus jeunes mangent légèrement plus de pizza
        if age < 25:
            base_pizza *= 1.1

        # 4. Finaliser les valeurs avec une variation réaliste
        # Variation proportionnelle à la valeur de base
        final_biere = base_biere * np.random.uniform(0.85, 1.15)  # ±15% de variation
        final_soft = base_soft * np.random.uniform(0.85, 1.15)
        final_pizza = base_pizza * np.random.uniform(0.9, 1.1)  # ±10% pour pizza
        
        # Assurer que les valeurs sont des entiers positifs
        final_biere = max(0, int(round(final_biere)))
        final_soft = max(1, int(round(final_soft)))  # Au moins 1 verre de soft
        final_pizza = max(1, int(round(final_pizza)))  # Au moins 1 part de pizza

        data.append([
            genre, age, taille, poids, conso_level, 
            final_biere, final_soft, final_pizza
        ])

    df = pd.DataFrame(data, columns=['biologicalGender', 'age', 'height', 'weight', 'alcoholConsumption', 'beer', 'softDrink', 'pizzaSlice'])
    return df
# --- Exécution du script ---
if __name__ == "__main__":
    # Génération des profils
    nouveaux_profils_df = generate_realistic_profiles(n_samples=2000)  # Augmenté à 1000 profils
    
    # Obtenir le chemin absolu du répertoire actuel
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)  # Remonter d'un niveau
    
    # Créer le dossier 'data' s'il n'existe pas déjà
    data_dir = os.path.join(parent_dir, 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Chemin du nouveau fichier (nom différent pour éviter toute confusion)
    output_path = os.path.join(data_dir, 'data_soiree_user.csv')
    
    # Sauvegarder directement le nouveau jeu de données
    nouveaux_profils_df.to_csv(output_path, index=False)

    print(f"Nouveau jeu de données avec {len(nouveaux_profils_df)} profils généré avec succès.")
    print(f"Fichier sauvegardé dans : {output_path}")
    print("\nExtrait des profils générés :")
    print(nouveaux_profils_df.head())
    
    # Afficher quelques statistiques pour vérification
    print("\nStatistiques des profils générés :")
    print(nouveaux_profils_df.describe().round(2))
    
    # Afficher des exemples de segments spécifiques
    male_aguerri = nouveaux_profils_df[(nouveaux_profils_df['biologicalGender'] == 'male') & 
                                      (nouveaux_profils_df['alcoholConsumption'] == 'seasoned')]
    print("\nHomme aguerri (moyenne de bière) :", male_aguerri['beer'].mean().round(2))

    female_occasionnel = nouveaux_profils_df[(nouveaux_profils_df['biologicalGender'] == 'female') & 
                                          (nouveaux_profils_df['alcoholConsumption'] == 'occasionally')]
    print("Femme occasionnelle (moyenne de bière) :", female_occasionnel['beer'].mean().round(2))