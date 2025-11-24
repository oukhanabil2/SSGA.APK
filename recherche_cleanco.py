#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os

class GestionRechercheCleanCo:
    def __init__(self):
        self.df = None
        self.charger_base_donnees()
    
    def charger_base_donnees(self):
    """Version adaptée APK"""
    try:
        # CHEMINS ANDROID APK
        chemins_possibles = [
            'base données cleanco.xlsx',
            './base données cleanco.xlsx',
            '/storage/emulated/0/Download/base données cleanco.xlsx',
        ]
        
        # Le reste reste identique...
            
            print("🔍 Recherche du fichier CleanCo...")
            chemin_trouve = None
            
            for chemin in chemins_possibles:
                if os.path.exists(chemin):
                    chemin_trouve = chemin
                    print(f"✅ FICHIER TROUVÉ: {chemin}")
                    break
                else:
                    print(f"   ❌ {chemin}")
            
            if not chemin_trouve:
                print("\n❌ Aucun chemin valide trouvé.")
                print("\n💡 SOLUTIONS:")
                print("   1. Mettez le fichier dans le dossier de l'application Pydroid")
                print("   2. Utilisez l'upload dans Pydroid (menu Fichiers → Upload)")
                print("   3. Vérifiez le nom exact: 'base données cleanco.xlsx'")
                return False
            
            print(f"\n📁 Chargement depuis: {chemin_trouve}")
            
            # Chargement du fichier Excel
            self.df = pd.read_excel(chemin_trouve)
            print(f"✅ Fichier chargé avec succès !")
            print(f"📊 {len(self.df)} lignes importées")
            
            # Test de recherche automatique
            print("\n🧪 Test de recherche automatique...")
            test_result = self.rechercher_par_code('CPA')
            if len(test_result) > 0:
                nom_trouve = test_result.iloc[0, 1] if pd.notna(test_result.iloc[0, 1]) else "N/A"
                prenom_trouve = test_result.iloc[0, 2] if pd.notna(test_result.iloc[0, 2]) else "N/A"
                print(f"   ✅ Test réussi: {nom_trouve} {prenom_trouve} trouvé")
            else:
                print("   ⚠️ Aucun résultat pour le test 'CPA'")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement: {str(e)}")
            return False
    
    def rechercher_par_nom(self, nom):
        """Recherche par nom (colonne 1)"""
        if self.df is None:
            return pd.DataFrame()
        try:
            resultat = self.df[self.df.iloc[:, 1].str.contains(str(nom), case=False, na=False)]
            return resultat
        except:
            return pd.DataFrame()
    
    def rechercher_par_code(self, code):
        """Recherche par code (colonne 0)"""
        if self.df is None:
            return pd.DataFrame()
        try:
            resultat = self.df[self.df.iloc[:, 0] == code.upper()]
            return resultat
        except:
            return pd.DataFrame()
    
    def rechercher_par_matricule(self, matricule):
        """Recherche par matricule (colonne 10)"""
        if self.df is None:
            return pd.DataFrame()
        try:
            resultat = self.df[self.df.iloc[:, 10] == matricule]
            return resultat
        except:
            return pd.DataFrame()
    
    def rechercher_par_telephone(self, telephone):
        """Recherche par téléphone (colonne 4)"""
        if self.df is None:
            return pd.DataFrame()
        try:
            resultat = self.df[self.df.iloc[:, 4] == telephone]
            return resultat
        except:
            return pd.DataFrame()
    
    def rechercher_par_groupe(self, groupe):
        """Recherche par groupe (colonne 3)"""
        if self.df is None:
            return pd.DataFrame()
        try:
            resultat = self.df[self.df.iloc[:, 3].str.contains(str(groupe), case=False, na=False)]
            return resultat
        except:
            return pd.DataFrame()
    
    def rechercher_par_prenom(self, prenom):
        """Recherche par prénom (colonne 2)"""
        if self.df is None:
            return pd.DataFrame()
        try:
            resultat = self.df[self.df.iloc[:, 2].str.contains(str(prenom), case=False, na=False)]
            return resultat
        except:
            return pd.DataFrame()
    
    def afficher_resultats(self, resultats):
        """Affiche les résultats de recherche"""
        if resultats is None or len(resultats) == 0:
            print("\n❌ Aucun résultat trouvé")
            return False
        
        print(f"\n✅ {len(resultats)} résultat(s) trouvé(s):")
        print("=" * 60)
        
        for index, ligne in resultats.iterrows():
            print(f"👤 Personne trouvée:")
            print(f"   📋 Code: {ligne.iloc[0]}")
            print(f"   👤 Nom: {ligne.iloc[1]}")
            print(f"   👤 Prénom: {ligne.iloc[2]}")
            print(f"   🏢 Groupe: {ligne.iloc[3]}")
            print(f"   📞 Téléphone: {ligne.iloc[4]}")
            print(f"   📍 Adresse: {ligne.iloc[5]}")
            print(f"   🚨 Code panique: {ligne.iloc[6]}")
            print(f"   💼 Poste: {ligne.iloc[7]}")
            print(f"   🆔 C.I.N: {ligne.iloc[8]}")
            print(f"   🎂 Date de naissance: {ligne.iloc[9]}")
            print(f"   🔢 N° Matricule: {ligne.iloc[10]}")
            print("-" * 40)
        return True
    
    def est_charge(self):
        """Vérifie si la base est chargée"""
        return self.df is not None and len(self.df) > 0

# Test autonome
if __name__ == "__main__":
    print("🧪 Test du module recherche_cleanco...")
    recherche = GestionRechercheCleanCo()
    if recherche.est_charge():
        print("✅ Module prêt à l'emploi!")
    else:
        print("❌ Module non chargé")
