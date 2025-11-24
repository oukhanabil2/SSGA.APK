#!/usr/bin/env python3
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
