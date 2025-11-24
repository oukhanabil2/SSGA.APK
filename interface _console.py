#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gestion_agents import GestionAgents
from recherche_cleanco import GestionRechercheCleanCo
from datetime import date
import sys

# =========================================================================
# 0. SÉCURITÉ : MOT DE PASSE
# =========================================================================
MOT_DE_PASSE_VALIDE = "Nabil1974"

def verifier_mot_de_passe():
    """Vérifie le mot de passe avant d'entrer dans l'application."""
    print("\n=============================================")
    print("      VÉRIFICATION D'IDENTITÉ")
    print("=============================================")
    tentatives_max = 3
    for i in range(tentatives_max):
        mdp = input("Mot de passe: ").strip()
        if mdp == MOT_DE_PASSE_VALIDE:
            print("✅ Authentification réussie.")
            return True
        print(f"❌ Mot de passe incorrect. Tentatives restantes : {tentatives_max - (i + 1)}")
    
    print("⛔ Trop de tentatives. Fermeture du programme.")
    return False

# =========================================================================
# 1. AFFICHAGE DU MENU (Interface courte)
# =========================================================================

def afficher_menu_principal():
    """Affiche le menu principal du système SGA."""
    print("\n=============================================")
    print("      MENU PRINCIPAL DU SGA")
    print("=============================================")
    print("1. 👤 Gestion de Agents (et Import CSV)")
    print("2. 🗓️ Gestion du Planning & des Shifts")
    print("3. 📊 Statistiques & Exportations")
    print("4. 📻 Gestion du Matériel Radio")
    print("5. 🚨 Gestion de Codes Panique")
    print("6. 🛠️ Initialiser des Agents de Test")
    print("7. 👕 Gestion des Habillement (Tailles & Fourniture)") 
    print("8. ⚠️ Gestion de la Discipline (Avertissements)") 
    print("9. 📅 Gestion des Congés par Période")
    print("10. 🔍 RECHERCHE Base Données CleanCo")
    print("0. 🍎 Quitter et Fermer la DB")
    print("=============================================")

def obtenir_entree(prompt, type_attendu=str):
    """Fonction utilitaire pour obtenir une entrée sécurisée de l'utilisateur."""
    while True:
        try:
            entree = input(prompt).strip()
            if not entree and type_attendu != str:
                return None
            
            if type_attendu == int:
                return int(entree)
            elif type_attendu == date:
                date.fromisoformat(entree) 
                return entree 
            else:
                return entree
        except ValueError:
            print(f"❌ Entrée invalide. Veuillez entrer un(e) {type_attendu.__name__} au format correct (YYYY-MM-JJ pour les dates).")
        except KeyboardInterrupt:
            print("\nOpération annulée.")
            return None

# =========================================================================
# 2. FONCTIONS DE SOUS-MENU COMPLÈTES
# =========================================================================

def menu_gestion_agents(gestionnaire):
    print("\n--- 1. GESTION DES AGENTS ---")
    print("1. Ajouter un agent")
    print("2. Lister les agents actifs")
    print("3. 📥 Importer des agents depuis Excel CleanCo")  # ✅ CHANGÉ
    print("4. 🗑️ Supprimer un agent (le marque comme inactif)")
    print("5. ✏️ Modifier les informations d'un agent (Nom, Prénom, Groupe, Entrée)") 
    print("0. Retour au menu principal")
    choix_sous_menu = obtenir_entree("Sélectionnez une sous-option : ")

    if choix_sous_menu == '1':
        code = obtenir_entree("Code Agent: ").upper()
        nom = obtenir_entree("Nom: ")
        prenom = obtenir_entree("Prénom: ")
        code_groupe = obtenir_entree("Code Groupe (A, B, C, D, E): ").upper()
        if all([code, nom, prenom, code_groupe]):
            gestionnaire.ajouter_agent(code, nom, prenom, code_groupe)
            
    elif choix_sous_menu == '2':
        gestionnaire.lister_agents()
        
    elif choix_sous_menu == '3':
        print("\n--- IMPORT DEPUIS EXCEL CLEANCO ---")
        print("📋 Le fichier Excel doit contenir:")
        print("   - Colonne 0: Code agent (ex: CPA)")
        print("   - Colonne 1: Nom") 
        print("   - Colonne 2: Prénom")
        print("   - Colonne 3: Groupe (A, B, C, D, E)")
        print("\n💡 Nom du fichier: 'base données cleanco.xlsx'")
        nom_fichier = obtenir_entree("Nom du fichier Excel: ")
        if nom_fichier:
            # ✅ UTILISER LA NOUVELLE MÉTHODE EXCEL
            gestionnaire.importer_agents_excel(nom_fichier)
            
    elif choix_sous_menu == '4':
        code = obtenir_entree("Code Agent à supprimer: ")
        if code:
            gestionnaire.supprimer_agent(code)

    elif choix_sous_menu == '5': 
        code = obtenir_entree("Code Agent à modifier: ").upper()
        
        print("\n--- Entrez les nouvelles valeurs (laissez vide pour ne pas modifier) ---")
        nom = obtenir_entree("Nouveau Nom: ")
        prenom = obtenir_entree("Nouveau Prénom: ")
        code_groupe = obtenir_entree("Nouveau Code Groupe (A, B, C, D, E): ").upper()
        date_entree = obtenir_entree("Nouvelle Date d'entrée (YYYY-MM-JJ) ou vide: ", date)
        
        gestionnaire.modifier_agent(code, nom, prenom, code_groupe, date_entree)

def menu_planning_shifts(gestionnaire):
    print("\n--- 2. GESTION DU PLANNING & SHIFTS ---")
    
    print("--- Affichages Individuels & Globaux ---")
    print("1. Calculer et afficher le planning mensuel **global** (Tous agents)")
    print("2. Calculer et afficher le planning mensuel **d'un agent** (+ Stats)")
    print("3. Calculer et afficher le planning trimestriel **global** (Tous agents)")
    
    print("--- Affichages par Groupe ---")
    print("4. Afficher le planning mensuel par **GROUPE (A, B, C, D, E)**")
    print("5. Afficher le planning trimestriel par **GROUPE**")
    print("6. Afficher le planning mensuel **TOUS GROUPES** (dans une seule vue)")
    
    print("--- Modifications / Absences ---")
    print("7. Enregistrer une absence (Congé [C], Maladie [M], Autre [A])")
    print("8. Modifier le shift d'un agent (ponctuel: 1, 2, 3, R, C, M, A)") 
    print("9. Échanger les shifts entre deux agents")
    print("10. ❌ Supprimer l'échange de shifts pour une date") 
    
    print("--- Jours Fériés ---")
    print("11. Ajouter un jour férié") 
    print("12. Supprimer un jour férié") 
    print("13. Lister les jours fériés de l'année") 

    print("--- Export par Groupe ---")
    print("14. 📁 Exporter le planning mensuel par Groupe (Excel)")
    print("15. 📁 Exporter le planning trimestriel par Groupe (Excel)")
    
    print("0. Retour au menu principal")
    choix_sous_menu = obtenir_entree("Sélectionnez une sous-option : ")

    if choix_sous_menu == '1':
        annee = obtenir_entree("Année (YYYY): ", int)
        mois = obtenir_entree("Mois (1-12): ", int)
        if annee and mois and 1 <= mois <= 12:
            gestionnaire.calculer_planning_mensuel(mois, annee)

    elif choix_sous_menu == '2':
        code = obtenir_entree("Code Agent: ").upper()
        annee = obtenir_entree("Année (YYYY): ", int)
        mois = obtenir_entree("Mois (1-12): ", int)
        if code and annee and mois and 1 <= mois <= 12:
            gestionnaire.calculer_planning_mensuel_agent(code, mois, annee)

    elif choix_sous_menu == '3':
        annee = obtenir_entree("Année de début (YYYY): ", int)
        mois_debut = obtenir_entree("Mois de début (1-12): ", int)
        if annee and mois_debut and 1 <= mois_debut <= 12:
            gestionnaire.calculer_planning_trimestriel(mois_debut, annee)
            
    elif choix_sous_menu == '4':
        code_groupe = obtenir_entree("Code Groupe (A, B, C, D, E): ").upper()
        annee = obtenir_entree("Année (YYYY): ", int)
        mois = obtenir_entree("Mois (1-12): ", int)
        if code_groupe and annee and mois:
            gestionnaire.afficher_planning_mensuel_groupe(code_groupe, mois, annee)

    elif choix_sous_menu == '5':
        code_groupe = obtenir_entree("Code Groupe (A, B, C, D, E): ").upper()
        annee = obtenir_entree("Année de début (YYYY): ", int)
        mois_debut = obtenir_entree("Mois de début (1-12): ", int)
        if code_groupe and annee and mois_debut:
            gestionnaire.afficher_planning_trimestriel_groupe(code_groupe, mois_debut, annee)
            
    elif choix_sous_menu == '6':
        annee = obtenir_entree("Année (YYYY): ", int)
        mois = obtenir_entree("Mois (1-12): ", int)
        if annee and mois:
            gestionnaire.afficher_planning_mensuel_tous_groupes(mois, annee)

    elif choix_sous_menu == '7':
        code = obtenir_entree("Code Agent: ").upper()
        jour_date = obtenir_entree("Date de l'absence (YYYY-MM-JJ): ", date)
        shift_code = obtenir_entree("Type d'absence (C, M, A): ").upper()
        if all([code, jour_date, shift_code]):
            gestionnaire.enregistrer_absence(code, jour_date, shift_code)

    elif choix_sous_menu == '8':
        code = obtenir_entree("Code Agent: ").upper()
        jour_date = obtenir_entree("Date à modifier (YYYY-MM-JJ): ", date)
        nouveau_shift = obtenir_entree("Nouveau shift (1, 2, 3, R, C, M, A): ").upper() 
        if all([code, jour_date, nouveau_shift]):
            gestionnaire.modifier_shift_ponctuel(code, jour_date, nouveau_shift)

    elif choix_sous_menu == '9':
        code_a = obtenir_entree("Code Agent A: ").upper()
        code_b = obtenir_entree("Code Agent B: ").upper()
        jour_date = obtenir_entree("Date de l'échange (YYYY-MM-JJ): ", date)
        if all([code_a, code_b, jour_date]):
            gestionnaire.echanger_shifts(code_a, code_b, jour_date)
            
    elif choix_sous_menu == '10': 
        code_a = obtenir_entree("Code Agent A (Optionnel): ").upper()
        code_b = obtenir_entree("Code Agent B (Optionnel): ").upper()
        jour_date = obtenir_entree("Date de l'échange à supprimer (YYYY-MM-JJ): ", date)
        if jour_date:
            gestionnaire.supprimer_echange(code_a, code_b, jour_date)

    elif choix_sous_menu == '11':
        jour_date = obtenir_entree("Date du jour férié (YYYY-MM-JJ): ", date)
        description = obtenir_entree("Description du jour férié: ")
        if all([jour_date, description]):
            gestionnaire.ajouter_jour_ferie(jour_date, description)

    elif choix_sous_menu == '12':
        jour_date = obtenir_entree("Date du jour férié à supprimer (YYYY-MM-JJ): ", date)
        if jour_date:
            gestionnaire.supprimer_jour_ferie(jour_date)

    elif choix_sous_menu == '13':
        annee = obtenir_entree("Année à lister (YYYY): ", int)
        if annee:
            gestionnaire.lister_jours_feries(annee)

    elif choix_sous_menu == '14':
        print("\n--- EXPORT PLANNING MENSUEL PAR GROUPE ---")
        annee = obtenir_entree("Année (YYYY): ", int)
        mois = obtenir_entree("Mois (1-12): ", int)
        code_groupe = obtenir_entree("Code Groupe à filtrer (ex: A): ").upper()
        if annee and mois and 1 <= mois <= 12 and code_groupe:
            nom_fichier = obtenir_entree("Nom du fichier de sortie (.xlsx): ")
            gestionnaire.exporter_planning_par_groupe(mois, annee, code_groupe, nom_fichier)

    elif choix_sous_menu == '15':
        print("\n--- EXPORT PLANNING TRIMESTRIEL PAR GROUPE ---")
        annee = obtenir_entree("Année de début (YYYY): ", int)
        mois = obtenir_entree("Mois de début (1-12): ", int)
        code_groupe = obtenir_entree("Code Groupe à filtrer (ex: B): ").upper()
        if annee and mois and 1 <= mois <= 12 and code_groupe:
            nom_fichier = obtenir_entree("Nom du fichier de sortie (.xlsx): ")
            gestionnaire.exporter_planning_par_groupe(mois, annee, code_groupe, nom_fichier, is_trimestriel=True)

def menu_stats_export(gestionnaire):
    print("\n--- 3. STATISTIQUES & EXPORTATIONS ---")
    print("1. Afficher les statistiques d'un agent pour un mois") 
    print("2. Afficher les statistiques globales pour un mois")
    print("3. 📁 Exporter les statistiques complètes de tous les agents (Excel)")
    print("4. 📁 Exporter le planning mensuel global (Excel)")
    print("5. 📁 Exporter le planning mensuel par agent (Excel)") 
    print("0. Retour au menu principal")
    choix_sous_menu = obtenir_entree("Sélectionnez une sous-option : ")

    if choix_sous_menu == '1':
        code = obtenir_entree("Code Agent: ").upper()
        annee = obtenir_entree("Année (YYYY): ", int)
        mois = obtenir_entree("Mois (1-12): ", int)
        if code and annee and mois and 1 <= mois <= 12:
            gestionnaire.afficher_statistiques(code, mois, annee)
    
    elif choix_sous_menu == '2':
        annee = obtenir_entree("Année (YYYY): ", int)
        mois = obtenir_entree("Mois (1-12): ", int)
        if annee and mois and 1 <= mois <= 12:
            gestionnaire.afficher_statistiques(None, mois, annee)
            
    elif choix_sous_menu == '3':
        annee = obtenir_entree("Année (YYYY): ", int)
        mois = obtenir_entree("Mois (1-12): ", int)
        if annee and mois and 1 <= mois <= 12:
            nom_fichier = obtenir_entree("Nom du fichier de sortie (.xlsx): ")
            gestionnaire.exporter_stats_excel(mois, annee, nom_fichier)

    elif choix_sous_menu == '4':
        annee = obtenir_entree("Année (YYYY): ", int)
        mois = obtenir_entree("Mois (1-12): ", int)
        if annee and mois and 1 <= mois <= 12:
            nom_fichier = obtenir_entree("Nom du fichier de sortie (.xlsx): ")
            gestionnaire.exporter_planning_mensuel_global(mois, annee, nom_fichier)

    elif choix_sous_menu == '5': 
        code = obtenir_entree("Code Agent: ").upper()
        annee = obtenir_entree("Année (YYYY): ", int)
        mois = obtenir_entree("Mois (1-12): ", int)
        if code and annee and mois and 1 <= mois <= 12:
            nom_fichier = obtenir_entree("Nom du fichier de sortie (.xlsx): ")
            gestionnaire.exporter_planning_mensuel_agent(code, mois, annee, nom_fichier)

def menu_gestion_radio(gestionnaire):
    print("\n--- 4. GESTION DU MATÉRIEL RADIO ---")
    print("1. Ajouter/Modifier une radio")
    print("2. Attribuer une radio à un agent")
    print("3. Enregistrer le retour d'une radio")
    print("4. Rapport de statut des radios")
    print("0. Retour au menu principal")
    choix_sous_menu = obtenir_entree("Sélectionnez une sous-option : ")

    if choix_sous_menu == '1':
        id_radio = obtenir_entree("ID de la radio (ex: R001): ").upper()
        modele = obtenir_entree("Modèle de la radio: ")
        statut = obtenir_entree("Statut (Disponible/HS/Réparation): ")
        if all([id_radio, modele, statut]):
            gestionnaire.ajouter_modifier_radio(id_radio, modele, statut)
    
    elif choix_sous_menu == '2':
        id_radio = obtenir_entree("ID de la radio à attribuer: ").upper()
        code_agent = obtenir_entree("Code Agent destinataire: ").upper()
        if all([id_radio, code_agent]):
            gestionnaire.attribuer_radio(id_radio, code_agent)

    elif choix_sous_menu == '3':
        id_radio = obtenir_entree("ID de la radio retournée: ").upper()
        if id_radio:
            gestionnaire.enregistrer_retour_radio(id_radio)
            
    elif choix_sous_menu == '4':
        gestionnaire.rapport_statut_radios()

def menu_codes_panique(gestionnaire):
    print("\n--- 5. GESTION DES CODES PANIQUE ---")
    print("1. Ajouter/Modifier un code panique pour un agent")
    print("2. Lister tous les codes panique")
    print("3. Supprimer un code panique")
    print("0. Retour au menu principal")
    choix_sous_menu = obtenir_entree("Sélectionnez une sous-option : ")
    
    if choix_sous_menu == '1':
        code_agent = obtenir_entree("Code Agent: ").upper()
        code_panique = obtenir_entree("Nouveau code panique: ")
        poste_nom = obtenir_entree("Nom du poste/emplacement: ")
        if all([code_agent, code_panique, poste_nom]):
            gestionnaire.ajouter_modifier_code_panique(code_agent, code_panique, poste_nom)
            
    elif choix_sous_menu == '2':
        gestionnaire.lister_codes_panique()
        
    elif choix_sous_menu == '3':
        code_agent = obtenir_entree("Code Agent pour suppression: ").upper()
        if code_agent:
            gestionnaire.supprimer_code_panique(code_agent)

def menu_gestion_habillement(gestionnaire): 
    print("\n--- 7. GESTION DES HABILLEMENTS ---")
    print("1. Ajouter/Modifier les tailles d'habillement et la date de fourniture")
    print("2. 📄 Rapport Global des Habillement")
    print("0. Retour au menu principal")
    choix_sous_menu = obtenir_entree("Sélectionnez une sous-option : ")
    
    if choix_sous_menu == '1':
        print("\n--- AJOUT/MODIFICATION HABILLEMENT ---")
        code = obtenir_entree("Code Agent: ").upper()
        
        habillement_data = {}
        for item in ['chemise', 'jacket', 'pantalon', 'cravate']:
            if item == 'cravate':
                prompt = f"{item.capitalize()} (Oui/Non, Date YYYY-MM-JJ) ou N/A: "
            else:
                prompt = f"{item.capitalize()} (Taille, Date YYYY-MM-JJ) ou N/A: "
                
            entree = obtenir_entree(prompt)
            if entree and entree.upper() != 'N/A':
                try:
                    valeur, date_fourniture = [x.strip() for x in entree.split(',', 1)]
                    date.fromisoformat(date_fourniture) 
                    habillement_data[item] = (valeur.upper() if item == 'cravate' else valeur, date_fourniture)
                except Exception:
                    print(f"❌ Format invalide pour {item}. (Ex: 42, 2025-11-01 ou Oui, 2025-11-01)")
            else:
                 habillement_data[item] = (None, None)

        if code and any(data for data, _ in habillement_data.values()):
            gestionnaire.ajouter_modifier_habillement(code, habillement_data)

    elif choix_sous_menu == '2':
        gestionnaire.rapport_habillement()

def menu_gestion_avertissements(gestionnaire): 
    print("\n--- 8. GESTION DE LA DISCIPLINE (AVERTISSEMENTS) ---")
    print("1. Enregistrer un avertissement")
    print("2. 📄 Historique des avertissements d'un agent")
    print("3. 📄 Rapport Global de tous les avertissements")
    print("0. Retour au menu principal")
    choix_sous_menu = obtenir_entree("Sélectionnez une sous-option : ")

    if choix_sous_menu == '1':
        print("\n--- ENREGISTRER UN AVERTISSEMENT ---")
        code = obtenir_entree("Code Agent: ").upper()
        type_av = obtenir_entree("Type d'avertissement (ORAL, ECRIT, MISE_A_PIED): ").upper()
        date_av = obtenir_entree("Date d'avertissement (YYYY-MM-JJ): ", date)
        description = obtenir_entree("Description / Motif: ")
        if all([code, type_av, date_av, description]):
            gestionnaire.enregistrer_avertissement(code, date_av, type_av, description)

    elif choix_sous_menu == '2':
        print("\n--- HISTORIQUE AGENT ---")
        code = obtenir_entree("Code Agent: ").upper()
        if code:
            gestionnaire.historique_avertissements_agent(code)

    elif choix_sous_menu == '3':
        gestionnaire.rapport_global_avertissements()

def menu_gestion_conges(gestionnaire):
    print("\n--- 9. GESTION DES CONGÉS PAR PÉRIODE ---")
    print("1. 📅 Ajouter un congé par période (du X au Y)")
    print("2. 🗑️ Supprimer un congé par période")
    print("3. 📋 Lister les congés d'un agent")
    print("0. Retour au menu principal")
    choix_sous_menu = obtenir_entree("Sélectionnez une sous-option : ")

    if choix_sous_menu == '1':
        print("\n--- AJOUT D'UN CONGÉ PAR PÉRIODE ---")
        code_agent = obtenir_entree("Code Agent: ").upper()
        date_debut = obtenir_entree("Date de début du congé (YYYY-MM-JJ): ", date)
        date_fin = obtenir_entree("Date de fin du congé (YYYY-MM-JJ): ", date)
        
        if all([code_agent, date_debut, date_fin]):
            gestionnaire.ajouter_conge_periode(code_agent, date_debut, date_fin)

    elif choix_sous_menu == '2':
        print("\n--- SUPPRESSION D'UN CONGÉ PAR PÉRIODE ---")
        code_agent = obtenir_entree("Code Agent: ").upper()
        date_debut = obtenir_entree("Date de début du congé à supprimer (YYYY-MM-JJ): ", date)
        date_fin = obtenir_entree("Date de fin du congé à supprimer (YYYY-MM-JJ): ", date)
        
        if all([code_agent, date_debut, date_fin]):
            gestionnaire.supprimer_conge_periode(code_agent, date_debut, date_fin)

    elif choix_sous_menu == '3':
        print("\n--- LISTE DES CONGÉS D'UN AGENT ---")
        code_agent = obtenir_entree("Code Agent: ").upper()
        if code_agent:
            gestionnaire.lister_conges_agent(code_agent)

def menu_recherche_cleanco():
    """Menu de recherche dans la base CleanCo - VERSION CORRIGÉE"""
    print("\n" + "="*50)
    print("🔍 RECHERCHE BASE CLEANCO")
    print("="*50)
    
    # Initialisation avec message de statut
    print("- [ ] Chargement: base données cleanco.xlsx")
    gestion_recherche = GestionRechercheCleanCo()
    
    if not gestion_recherche.est_charge():
        print("- [x] Échec du chargement. Retour au menu principal.")
        input("\n📝 Appuyez sur Entrée pour continuer...")
        return
    
    print("- [x] Chargement réussi !")
    print("✅ Base de données CleanCo prête pour la recherche!")
    
    while True:
        print("\n" + "="*40)
        print("OPTIONS DE RECHERCHE")
        print("="*40)
        print("1. Par nom")
        print("2. Par code") 
        print("3. Par matricule")
        print("4. Par téléphone")
        print("5. Par groupe")
        print("6. Par prénom")
        print("0. Retour au menu principal")
        print("-"*40)
        
        choix = input("Choisissez le type de recherche (0-6): ").strip()
        
        if choix == '0':
            print("\n↩️ Retour au menu principal...")
            break
            
        elif choix == '1':
            terme = input("Entrez le nom à rechercher: ").strip()
            if terme:
                resultats = gestion_recherche.rechercher_par_nom(terme)
                if not gestion_recherche.afficher_resultats(resultats):
                    print("\n❌ Aucun résultat trouvé pour ce nom")
            else:
                print("❌ Veuillez entrer un nom")
                
        elif choix == '2':
            terme = input("Entrez le code à rechercher: ").strip().upper()
            if terme:
                resultats = gestion_recherche.rechercher_par_code(terme)
                if not gestion_recherche.afficher_resultats(resultats):
                    print("\n❌ Aucun résultat trouvé pour ce code")
            else:
                print("❌ Veuillez entrer un code")
                
        elif choix == '3':
            terme = input("Entrez le numéro matricule: ").strip()
            if terme:
                resultats = gestion_recherche.rechercher_par_matricule(terme)
                if not gestion_recherche.afficher_resultats(resultats):
                    print("\n❌ Aucun résultat trouvé pour ce matricule")
            else:
                print("❌ Veuillez entrer un matricule")
                
        elif choix == '4':
            terme = input("Entrez le numéro de téléphone: ").strip()
            if terme:
                resultats = gestion_recherche.rechercher_par_telephone(terme)
                if not gestion_recherche.afficher_resultats(resultats):
                    print("\n❌ Aucun résultat trouvé pour ce téléphone")
            else:
                print("❌ Veuillez entrer un téléphone")
                
        elif choix == '5':
            terme = input("Entrez le groupe à rechercher: ").strip()
            if terme:
                resultats = gestion_recherche.rechercher_par_groupe(terme)
                if not gestion_recherche.afficher_resultats(resultats):
                    print("\n❌ Aucun résultat trouvé pour ce groupe")
            else:
                print("❌ Veuillez entrer un groupe")
                
        elif choix == '6':
            terme = input("Entrez le prénom à rechercher: ").strip()
            if terme:
                resultats = gestion_recherche.rechercher_par_prenom(terme)
                if not gestion_recherche.afficher_resultats(resultats):
                    print("\n❌ Aucun résultat trouvé pour ce prénom")
            else:
                print("❌ Veuillez entrer un prénom")
                
        else:
            print("❌ Choix invalide. Veuillez choisir entre 0 et 6.")
        
        # Pause après chaque recherche (comme dans les autres menus)
        if choix in ['1', '2', '3', '4', '5', '6']:
            input("\n📝 Appuyez sur Entrée pour continuer...")

# =========================================================================
# 3. BOUCLE PRINCIPALE (DISPATCH)
# =========================================================================

def main():
    if not verifier_mot_de_passe():
        sys.exit()

    print("\nConnexion à la base de données existante...")
    print("Système de Gestion des Agents (SGA) démarré.")
    
    try:
        gestionnaire = GestionAgents()
    except Exception as e:
        print(f"❌ Erreur critique lors de l'initialisation de la DB: {e}")
        return
    
    while True:
        afficher_menu_principal()
        choix = obtenir_entree("Sélectionnez une option : ")

        if choix == '0':
            gestionnaire.fermer_connexion()
            print("👋 Fermeture du système. Au revoir!")
            break
        
        elif choix == '1':
            menu_gestion_agents(gestionnaire)
        
        elif choix == '2':
            menu_planning_shifts(gestionnaire)

        elif choix == '3':
            menu_stats_export(gestionnaire)

        elif choix == '4':
            menu_gestion_radio(gestionnaire)

        elif choix == '5':
            menu_codes_panique(gestionnaire)
        
        elif choix == '6':
            gestionnaire.initialiser_agents_test()
            
        elif choix == '7':
            menu_gestion_habillement(gestionnaire)

        elif choix == '8':
            menu_gestion_avertissements(gestionnaire)
        
        elif choix == '9':
            menu_gestion_conges(gestionnaire)
        
        elif choix == '10':
            menu_recherche_cleanco()
        
        else:
            print("❌ Choix invalide. Veuillez sélectionner une option du menu.")

if __name__ == "__main__":
    main()
