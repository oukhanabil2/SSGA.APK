import sqlite3
import pandas as pd 
import csv
from datetime import date, timedelta
from calendar import monthrange
import os
from tabulate import tabulate 

# Constantes pour la traduction et la logique
JOURS_FRANCAIS = {
    'Mon': 'Lun', 'Tue': 'Mar', 'Wed': 'Mer', 'Thu': 'Jeu',
    'Fri': 'Ven', 'Sat': 'Sam', 'Sun': 'Dim'
}

# Date d'affectation fixe demandée par l'utilisateur
DATE_AFFECTATION_BASE = "2025-11-01"

class GestionAgents:
    def __init__(self, db_name="planning.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._initialiser_db()

    def _initialiser_db(self):
        """Initialise la base de données avec les tables nécessaires (complètes)."""
        # Tables principales
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS agents (
                code TEXT PRIMARY KEY,
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL,
                code_groupe TEXT NOT NULL,
                date_entree TEXT,
                date_sortie TEXT,
                statut TEXT DEFAULT 'actif'
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS planning (
                code_agent TEXT,
                date TEXT,
                shift TEXT,
                origine TEXT,
                PRIMARY KEY (code_agent, date)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS jours_feries (
                date TEXT PRIMARY KEY,
                description TEXT
            )
        """)
        # Tables annexes 
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS codes_panique (
                code_agent TEXT PRIMARY KEY,
                code_panique TEXT NOT NULL,
                poste_nom TEXT NOT NULL,
                FOREIGN KEY (code_agent) REFERENCES agents(code)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS radios (
                id_radio TEXT PRIMARY KEY,
                modele TEXT NOT NULL,
                statut TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS historique_radio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_radio TEXT,
                code_agent TEXT,
                date_attribution TEXT NOT NULL,
                date_retour TEXT,
                FOREIGN KEY (id_radio) REFERENCES radios(id_radio),
                FOREIGN KEY (code_agent) REFERENCES agents(code)
            )
        """)
        # Habillement
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS habillement (
                code_agent TEXT PRIMARY KEY,
                chemise_taille TEXT,
                chemise_date TEXT,
                jacket_taille TEXT,
                jacket_date TEXT,
                pantalon_taille TEXT,
                pantalon_date TEXT,
                cravate_oui TEXT,
                cravate_date TEXT,
                FOREIGN KEY (code_agent) REFERENCES agents(code)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS avertissements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code_agent TEXT,
                date_avertissement TEXT NOT NULL,
                type_avertissement TEXT NOT NULL,
                description TEXT,
                FOREIGN KEY (code_agent) REFERENCES agents(code)
            )
        """)
        # Table pour les congés par période
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS conges_periode (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code_agent TEXT,
                date_debut TEXT NOT NULL,
                date_fin TEXT NOT NULL,
                date_creation TEXT NOT NULL,
                FOREIGN KEY (code_agent) REFERENCES agents(code)
            )
        """)

        self.conn.commit()

    def fermer_connexion(self):
        """Ferme la connexion à la base de données."""
        self.conn.close()

    # =========================================================================
    # IMPORTATION EXCEL CLEANCO - MÉTHODE CORRIGÉE
    # =========================================================================

    def importer_agents_excel(self, nom_fichier):
        """Importe les agents directement depuis un fichier Excel CleanCo - VERSION CORRIGÉE"""
        try:
            if not os.path.exists(nom_fichier):
                print(f"❌ Erreur : Le fichier '{nom_fichier}' est introuvable.")
                print("💡 Vérifiez le nom du fichier et son emplacement.")
                return False
            
            print(f"📊 Chargement du fichier Excel: {nom_fichier}")
            
            # Lecture du fichier Excel avec gestion d'erreurs améliorée
            try:
                df = pd.read_excel(nom_fichier)
                print(f"✅ Fichier chargé: {len(df)} lignes trouvées")
            except Exception as e:
                print(f"❌ ERREUR LECTURE EXCEL: {e}")
                print("🔧 Causes possibles:")
                print("   - Fichier Excel corrompu")
                print("   - Format de fichier non supporté")
                print("   - Fichier protégé par mot de passe")
                print("💡 Essayez de sauvegarder le fichier en format .xlsx récent")
                return False
            
            # Aperçu des colonnes
            print("📋 Structure du fichier:")
            for i, col in enumerate(df.columns):
                sample_value = df.iloc[0, i] if len(df) > 0 else 'N/A'
                print(f"   Colonne {i}: '{col}' → Exemple: {sample_value}")
            
            agents_importes = 0
            agents_ignores = 0
            erreurs = []
            
            # Parcourir chaque ligne du fichier Excel
            for index, ligne in df.iterrows():
                try:
                    # Gestion robuste des valeurs NaN et conversion
                    code = str(ligne.iloc[0]).strip().upper() if pd.notna(ligne.iloc[0]) and ligne.iloc[0] != '' else ""
                    nom = str(ligne.iloc[1]).strip() if pd.notna(ligne.iloc[1]) and ligne.iloc[1] != '' else ""
                    prenom = str(ligne.iloc[2]).strip() if pd.notna(ligne.iloc[2]) and ligne.iloc[2] != '' else ""
                    groupe = str(ligne.iloc[3]).strip().upper() if pd.notna(ligne.iloc[3]) and ligne.iloc[3] != '' else ""
                    
                    # Vérifier que les champs obligatoires sont remplis
                    if not code or code == 'NAN' or code == 'NONE':
                        erreurs.append(f"Ligne {index+1}: Code agent manquant ou invalide")
                        agents_ignores += 1
                        continue
                    
                    if not nom:
                        erreurs.append(f"Ligne {index+1}: Nom manquant")
                        agents_ignores += 1
                        continue
                        
                    if not prenom:
                        erreurs.append(f"Ligne {index+1}: Prénom manquant")
                        agents_ignores += 1
                        continue
                        
                    if not groupe or groupe not in ['A', 'B', 'C', 'D', 'E']:
                        erreurs.append(f"Ligne {index+1}: Groupe invalide '{groupe}' (doit être A, B, C, D ou E)")
                        agents_ignores += 1
                        continue
                    
                    # Vérifier si l'agent existe déjà
                    self.cursor.execute("SELECT code FROM agents WHERE code=?", (code,))
                    existe = self.cursor.fetchone()
                    
                    if existe:
                        # Mettre à jour l'agent existant
                        self.cursor.execute('''
                            UPDATE agents 
                            SET nom = ?, prenom = ?, code_groupe = ?, date_sortie = NULL
                            WHERE code = ?
                        ''', (nom, prenom, groupe, code))
                        print(f"🔄 Agent mis à jour: {code} - {nom} {prenom}")
                    else:
                        # Ajouter un nouvel agent
                        self.cursor.execute('''
                            INSERT INTO agents (code, nom, prenom, code_groupe, date_entree, date_sortie)
                            VALUES (?, ?, ?, ?, ?, NULL)
                        ''', (code, nom, prenom, groupe, DATE_AFFECTATION_BASE))
                        print(f"✅ Nouvel agent ajouté: {code} - {nom} {prenom}")
                    
                    agents_importes += 1
                    
                except Exception as e:
                    erreur_msg = f"Ligne {index+1}: {str(e)}"
                    erreurs.append(erreur_msg)
                    agents_ignores += 1
                    print(f"❌ {erreur_msg}")
                    continue
            
            # Sauvegarder les changements
            self.conn.commit()
            
            # Rapport final détaillé
            print(f"\n📈 IMPORT EXCEL TERMINÉ:")
            print(f"   ✅ Agents importés/mis à jour: {agents_importes}")
            print(f"   ⚠️ Lignes ignorées: {agents_ignores}")
            
            if erreurs:
                print(f"\n❌ Erreurs rencontrées ({len(erreurs)}):")
                for erreur in erreurs[:5]:  # Affiche seulement les 5 premières erreurs
                    print(f"   - {erreur}")
                if len(erreurs) > 5:
                    print(f"   ... et {len(erreurs) - 5} autres erreurs")
            
            return agents_importes > 0
            
        except PermissionError:
            print(f"❌ ERREUR: Permission refusée pour le fichier '{nom_fichier}'!")
            print("💡 Fermez le fichier Excel s'il est ouvert dans un autre programme.")
            return False
        except Exception as e:
            print(f"❌ ERREUR CRITIQUE lors de l'import Excel: {e}")
            return False

    # =========================================================================
    # LOGIQUE DES CYCLES ET SHIFTS
    # =========================================================================

    def _cycle_standard_8j(self, jour_cycle):
        """Définit la rotation continue de 8 jours (1, 1, 2, 2, 3, 3, R, R)."""
        cycle = ['1', '1', '2', '2', '3', '3', 'R', 'R']
        return cycle[jour_cycle % 8]

    def _get_decalage_standard(self, code_groupe):
        """Définit le décalage en jours pour les groupes A/B/C/D."""
        if code_groupe.upper() == 'A':
            return 0
        elif code_groupe.upper() == 'B':
            return 2
        elif code_groupe.upper() == 'C':
            return 4
        elif code_groupe.upper() == 'D':
            return 6
        return 0

    def _cycle_c_diff(self, jour_date: date, code_agent):
        """Définit le cycle E (5/7)."""
        jour_semaine = jour_date.weekday()
        
        if jour_semaine >= 5: 
            return 'R'
            
        self.cursor.execute("SELECT code FROM agents WHERE code_groupe='E' AND date_sortie IS NULL ORDER BY code")
        agents_du_groupe = [a[0] for a in self.cursor.fetchall()]
        
        try:
            index_agent = agents_du_groupe.index(code_agent)
        except ValueError:
            return 'R'

        num_semaine = jour_date.isocalendar()[1]
        
        jour_pair = (jour_semaine % 2 == 0)
        
        # Agent 1 (index 0) : S1 dominant les semaines impaires
        if index_agent == 0:
            if num_semaine % 2 != 0: 
                return '1' if jour_pair else '2' 
            else: 
                return '2' if jour_pair else '1'
        
        # Agent 2 (index 1) : S2 dominant les semaines impaires
        if index_agent == 1:
            if num_semaine % 2 != 0: 
                return '2' if jour_pair else '1'
            else: 
                return '1' if jour_pair else '2'

        return 'R'
    
    def _get_shift_theorique_rotation(self, code_agent, jour_date: date):
        """Calcule le shift de rotation (1, 2, 3, R)."""
        self.cursor.execute("SELECT code_groupe, date_entree, date_sortie FROM agents WHERE code=?", (code_agent,))
        agent_info = self.cursor.fetchone()

        if not agent_info:
            return '-'

        code_groupe, date_entree_str, date_sortie_str = agent_info
        
        if date_sortie_str and jour_date >= date.fromisoformat(date_sortie_str):
             return '-' 
        
        date_entree = date.fromisoformat(date_entree_str)
        if jour_date < date_entree:
             return '-' 
        
        delta_jours = (jour_date - date_entree).days
        jour_cycle_base = delta_jours

        if code_groupe == 'E':
            return self._cycle_c_diff(jour_date, code_agent)
        
        elif code_groupe in ['A', 'B', 'C', 'D']:
            decalage = self._get_decalage_standard(code_groupe)
            jour_cycle_decale = jour_cycle_base + decalage
            return self._cycle_standard_8j(jour_cycle_decale)
        
        else:
            return 'R' 

    # =========================================================================
    # GESTION DES CONGÉS PAR PÉRIODE
    # =========================================================================

    def ajouter_conge_periode(self, code_agent, date_debut, date_fin):
        """Ajoute un congé sur une période donnée, les dimanches restent en repos."""
        code_agent = code_agent.upper()
        
        # Vérifier que l'agent existe
        self.cursor.execute("SELECT code FROM agents WHERE code=? AND date_sortie IS NULL", (code_agent,))
        if not self.cursor.fetchone():
            print(f"❌ Agent {code_agent} non trouvé ou inactif.")
            return False

        try:
            date_debut_obj = date.fromisoformat(date_debut)
            date_fin_obj = date.fromisoformat(date_fin)
            
            if date_debut_obj > date_fin_obj:
                print("❌ La date de début doit être avant la date de fin.")
                return False

            # Enregistrer la période de congé
            date_creation = date.today().isoformat()
            self.cursor.execute(
                "INSERT INTO conges_periode (code_agent, date_debut, date_fin, date_creation) VALUES (?, ?, ?, ?)",
                (code_agent, date_debut, date_fin, date_creation)
            )

            # Appliquer les congés jour par jour
            current_date = date_debut_obj
            jours_conges = 0
            
            while current_date <= date_fin_obj:
                jour_date_str = current_date.isoformat()
                
                # Vérifier si c'est un dimanche (weekday() = 6)
                if current_date.weekday() == 6:
                    # Dimanche = repos forcé
                    self.cursor.execute(
                        "INSERT OR REPLACE INTO planning (code_agent, date, shift, origine) VALUES (?, ?, ?, 'CONGE_DIMANCHE')",
                        (code_agent, jour_date_str, 'R')
                    )
                else:
                    # Jour de semaine = congé
                    self.cursor.execute(
                        "INSERT OR REPLACE INTO planning (code_agent, date, shift, origine) VALUES (?, ?, ?, 'CONGE_PERIODE')",
                        (code_agent, jour_date_str, 'C')
                    )
                    jours_conges += 1
                
                current_date += timedelta(days=1)

            self.conn.commit()
            print(f"✅ Congé enregistré pour {code_agent} du {date_debut} au {date_fin}")
            print(f"📅 {jours_conges} jour(s) de congé effectif(s) (hors dimanches)")
            return True

        except Exception as e:
            print(f"❌ Erreur lors de l'ajout du congé: {e}")
            return False

    def supprimer_conge_periode(self, code_agent, date_debut, date_fin):
        """Supprime un congé sur une période donnée et rétablit le planning théorique."""
        code_agent = code_agent.upper()
        
        try:
            date_debut_obj = date.fromisoformat(date_debut)
            date_fin_obj = date.fromisoformat(date_fin)
            
            # Supprimer la période de congé enregistrée
            self.cursor.execute(
                "DELETE FROM conges_periode WHERE code_agent=? AND date_debut=? AND date_fin=?",
                (code_agent, date_debut, date_fin)
            )
            
            # Supprimer les shifts de congé dans la période
            current_date = date_debut_obj
            jours_supprimes = 0
            
            while current_date <= date_fin_obj:
                jour_date_str = current_date.isoformat()
                
                # Supprimer les enregistrements de congé
                self.cursor.execute(
                    "DELETE FROM planning WHERE code_agent=? AND date=? AND origine IN ('CONGE_PERIODE', 'CONGE_DIMANCHE')",
                    (code_agent, jour_date_str)
                )
                
                # Supprimer aussi le shift théorique pour forcer le recalcul
                self.cursor.execute(
                    "DELETE FROM planning WHERE code_agent=? AND date=? AND origine='THEORIQUE'",
                    (code_agent, jour_date_str)
                )
                
                jours_supprimes += 1
                current_date += timedelta(days=1)

            self.conn.commit()
            print(f"✅ Congé supprimé pour {code_agent} du {date_debut} au {date_fin}")
            print(f"🔄 Planning théorique rétabli pour {jours_supprimes} jour(s)")
            return True

        except Exception as e:
            print(f"❌ Erreur lors de la suppression du congé: {e}")
            return False

    def lister_conges_agent(self, code_agent):
        """Liste tous les congés enregistrés pour un agent."""
        code_agent = code_agent.upper()
        
        self.cursor.execute(
            "SELECT date_debut, date_fin, date_creation FROM conges_periode WHERE code_agent=? ORDER BY date_debut",
            (code_agent,)
        )
        conges = self.cursor.fetchall()
        
        if not conges:
            print(f"⚠️ Aucun congé enregistré pour l'agent {code_agent}.")
            return

        print(f"\n--- LISTE DES CONGÉS POUR {code_agent} ---")
        headers = ["Début", "Fin", "Durée", "Créé le"]
        data = []
        
        for date_debut, date_fin, date_creation in conges:
            debut_obj = date.fromisoformat(date_debut)
            fin_obj = date.fromisoformat(date_fin)
            duree = (fin_obj - debut_obj).days + 1
            data.append([date_debut, date_fin, f"{duree} jour(s)", date_creation])
        
        print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

    # =========================================================================
    # GESTION DES AGENTS (AVEC DATE FIXE)
    # =========================================================================

    def ajouter_agent(self, code, nom, prenom, code_groupe):
        """Ajoute un nouvel agent à la base de données avec une date d'entrée fixe."""
        code = code.upper()
        code_groupe = code_groupe.upper()
        
        date_entree = DATE_AFFECTATION_BASE 
        
        if code_groupe not in ['A', 'B', 'C', 'D', 'E']:
             print("❌ Code de groupe invalide. Utilisez A, B, C, D ou E.")
             return False
             
        try:
            self.cursor.execute(
                "INSERT OR REPLACE INTO agents (code, nom, prenom, code_groupe, date_entree, date_sortie) VALUES (?, ?, ?, ?, ?, NULL)",
                (code, nom, prenom, code_groupe, date_entree)
            )
            self.conn.commit()
            print(f"✅ Agent {code} ajouté/mis à jour (Date d'entrée: {date_entree}).")
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            print(f"❌ Erreur lors de l'ajout de l'agent {code}: {e}")
            return False

    def modifier_agent(self, code_agent, nom, prenom, code_groupe, date_entree):
        """Modifie les informations d'un agent existant."""
        code_agent = code_agent.upper()
        
        self.cursor.execute("SELECT nom, prenom, code_groupe, date_entree FROM agents WHERE code=?", (code_agent,))
        agent_info = self.cursor.fetchone()
        
        if not agent_info:
            print(f"❌ Agent {code_agent} non trouvé.")
            return

        nom_new = nom if nom else agent_info[0]
        prenom_new = prenom if prenom else agent_info[1]
        code_groupe_new = code_groupe.upper() if code_groupe else agent_info[2]
        date_entree_new = date_entree if date_entree else agent_info[3]
        
        if code_groupe_new not in ['A', 'B', 'C', 'D', 'E']:
            print("❌ Nouveau code de groupe invalide. Modification annulée.")
            return
            
        try:
            self.cursor.execute(
                """UPDATE agents SET nom=?, prenom=?, code_groupe=?, date_entree=? 
                   WHERE code=?""",
                (nom_new, prenom_new, code_groupe_new, date_entree_new, code_agent)
            )
            self.conn.commit()
            print(f"✅ Agent {code_agent} modifié avec succès.")
            
            if code_groupe_new != agent_info[2] or date_entree_new != agent_info[3]:
                 self.cursor.execute("DELETE FROM planning WHERE code_agent=? AND origine='THEORIQUE'", (code_agent,))
                 self.conn.commit()
                 print("⚠️ Planning théorique effacé pour forcer la regénération.")
                 
        except Exception as e:
            print(f"❌ Erreur lors de la modification de l'agent: {e}")

    def supprimer_agent(self, code_agent):
        """Marque un agent comme sorti (date_sortie)."""
        code_agent = code_agent.upper()
        try:
            date_sortie = date.today().isoformat()
            self.cursor.execute(
                "UPDATE agents SET date_sortie = ? WHERE code = ? AND date_sortie IS NULL",
                (date_sortie, code_agent)
            )
            
            if self.cursor.rowcount > 0:
                date_debut_suppression = (date.today() + timedelta(days=1)).isoformat()
                self.cursor.execute(
                    "DELETE FROM planning WHERE code_agent = ? AND date >= ?",
                    (code_agent, date_debut_suppression)
                )
                self.conn.commit()
                print(f"✅ Agent {code_agent} marqué comme sorti à la date {date_sortie} et son planning futur a été effacé.")
            else:
                print(f"⚠️ Agent {code_agent} non trouvé ou déjà marqué comme inactif.")
        except Exception as e:
            print(f"❌ Erreur lors de la suppression de l'agent: {e}")

    def lister_agents(self):
        """Liste tous les agents actifs."""
        self.cursor.execute("SELECT code, nom, prenom, code_groupe FROM agents WHERE date_sortie IS NULL ORDER BY code_groupe, code")
        agents = self.cursor.fetchall()
        if not agents:
            print("⚠️ Aucun agent actif trouvé.")
            return []
            
        print("\n--- LISTE DES AGENTS ACTIFS ---")
        for code, nom, prenom, groupe in agents:
            print(f"[{groupe:<1}] {code:<8} - {nom} {prenom}")
        print("-" * 35)
        return agents

    def importer_agents_csv(self, nom_fichier):
        """Importe les agents à partir d'un fichier CSV."""
        try:
            with open(nom_fichier, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                agents_importes = 0
                for row in reader:
                    code = row.get('code', '').upper()
                    nom = row.get('nom', '')
                    prenom = row.get('prenom', '')
                    code_groupe = row.get('code_groupe', '').upper()
                    date_entree = row.get('date_entree', DATE_AFFECTATION_BASE) 
                    
                    if code and nom and code_groupe:
                        if self.ajouter_agent_from_csv(code, nom, prenom, code_groupe, date_entree):
                            agents_importes += 1
            print(f"✅ {agents_importes} agent(s) importé(s) ou mis(s) à jour avec succès.")
        except FileNotFoundError:
            print(f"❌ Erreur : Le fichier '{nom_fichier}' est introuvable.")
        except Exception as e:
            print(f"❌ Erreur lors de l'importation CSV: {e}")
            
    def ajouter_agent_from_csv(self, code, nom, prenom, code_groupe, date_entree):
        """Méthode utilitaire pour l'import CSV."""
        code = code.upper()
        code_groupe = code_groupe.upper()
        if code_groupe not in ['A', 'B', 'C', 'D', 'E']:
             print("❌ Code de groupe invalide. Utilisez A, B, C, D ou E.")
             return False
        try:
            self.cursor.execute(
                "INSERT OR REPLACE INTO agents (code, nom, prenom, code_groupe, date_entree, date_sortie) VALUES (?, ?, ?, ?, ?, NULL)",
                (code, nom, prenom, code_groupe, date_entree)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"❌ Erreur lors de l'ajout de l'agent {code} via CSV: {e}")
            return False

    def initialiser_agents_test(self):
        """Initialise des agents de test avec la date d'affectation fixe."""
        agents_de_test = [
            {'code': 'A01', 'nom': 'Dupont', 'prenom': 'Alice', 'code_groupe': 'A'},
            {'code': 'B02', 'nom': 'Martin', 'prenom': 'Bob', 'code_groupe': 'B'},
            {'code': 'C03', 'nom': 'Lefevre', 'prenom': 'Carole', 'code_groupe': 'C'},
            {'code': 'D04', 'nom': 'Dubois', 'prenom': 'David', 'code_groupe': 'D'},
            {'code': 'E01', 'nom': 'Zahiri', 'prenom': 'Ahmed', 'code_groupe': 'E'}, 
            {'code': 'E02', 'nom': 'Zarrouk', 'prenom': 'Benoit', 'code_groupe': 'E'}  
        ]
        
        compteur = 0
        print("\n--- INITIALISATION DES AGENTS DE TEST ---")
        for agent in agents_de_test:
            if self.ajouter_agent_from_csv(agent['code'], agent['nom'], agent['prenom'], agent['code_groupe'], DATE_AFFECTATION_BASE):
                compteur += 1
                
        self.conn.commit()
        print(f"✅ {compteur} agents de test ajoutés/mis à jour (Date d'entrée: {DATE_AFFECTATION_BASE}).")

    # =========================================================================
    # GESTION PLANNING & SHIFTS
    # =========================================================================
    
    def _get_shift_effectif(self, code_agent, jour_date: str):
        """Récupère le shift enregistré ou calcule le shift théorique, et l'enregistre."""
        
        self.cursor.execute("SELECT shift FROM planning WHERE code_agent=? AND date=?", (code_agent, jour_date))
        result = self.cursor.fetchone()
        
        if result:
            return result[0]

        # Si pas d'enregistrement manuel, on calcule le théorique
        date_obj = date.fromisoformat(jour_date)
        shift_theorique = self._get_shift_theorique_rotation(code_agent, date_obj) 
        
        if shift_theorique == '-':
             return '-' 
             
        self.cursor.execute(
            "INSERT OR REPLACE INTO planning (code_agent, date, shift, origine) VALUES (?, ?, ?, 'THEORIQUE')",
            (code_agent, jour_date, shift_theorique)
        )
        self.conn.commit()
        return shift_theorique

    def calculer_planning_mensuel(self, mois, annee):
        """Calcule et affiche le planning théorique du mois pour tous les agents."""
        
        _, jours_mois = monthrange(annee, mois)
        
        self.cursor.execute("SELECT code FROM agents WHERE date_sortie IS NULL ORDER BY code_groupe, code")
        agents_codes = [a[0] for a in self.cursor.fetchall()]
        
        header_cols = [f"{i:02d}-{JOURS_FRANCAIS[date(annee, mois, i).strftime('%a')]}" for i in range(1, jours_mois + 1)]
        header = ["Agent"] + header_cols
        
        planning_data = []
        ferie_row = ["Férié"]
        
        for i in range(1, jours_mois + 1):
             jour_date = date(annee, mois, i).isoformat()
             ferie_row.append("Oui" if self._est_jour_ferie(jour_date) else "")

        for code in agents_codes:
            row = [code]
            for i in range(1, jours_mois + 1):
                jour_date = date(annee, mois, i).isoformat()
                shift = self._get_shift_effectif(code, jour_date)
                row.append(shift)
            planning_data.append(row)
            
        df_planning = pd.DataFrame([ferie_row] + planning_data, columns=header).set_index(header[0])
        
        print(f"\n--- PLANNING MENSUEL GLOBAL {mois:02d}/{annee} ---")
        try:
            print(tabulate(df_planning, headers='keys', tablefmt="fancy_grid"))
        except ImportError:
            print("❌ Erreur: La bibliothèque 'tabulate' est requise pour l'affichage.")
            print(df_planning.to_string())
            
        footer = "\n" + "=" * 50
        footer += "\nProgramme par : Oukha Nabil"
        footer += "\nFonction : Chef de Patrouille 👮‍♂️"
        footer += "\n" + "=" * 50
        print(footer)
        
        return df_planning

    def afficher_planning_mensuel_groupe(self, code_groupe, mois, annee):
        """Affiche le planning mensuel pour un groupe spécifique."""
        code_groupe = code_groupe.upper()
        
        self.cursor.execute("SELECT code, nom, prenom FROM agents WHERE code_groupe=? AND date_sortie IS NULL ORDER BY code", (code_groupe,))
        agents_info = self.cursor.fetchall()
        
        if not agents_info:
            print(f"❌ Aucun agent actif trouvé dans le groupe {code_groupe}.")
            return

        _, jours_mois = monthrange(annee, mois)
        
        header_cols = [f"{i:02d}-{JOURS_FRANCAIS[date(annee, mois, i).strftime('%a')]}" for i in range(1, jours_mois + 1)]
        header = ["Agent"] + header_cols
        
        planning_data = []
        ferie_row = ["Férié"]
        for i in range(1, jours_mois + 1):
             jour_date = date(annee, mois, i).isoformat()
             ferie_row.append("Oui" if self._est_jour_ferie(jour_date) else "")

        for code, nom, prenom in agents_info:
            row = [f"{code} ({nom[0]}{prenom[0]})"]
            for i in range(1, jours_mois + 1):
                jour_date = date(annee, mois, i).isoformat()
                shift = self._get_shift_effectif(code, jour_date)
                row.append(shift)
            planning_data.append(row)
            
        df_planning = pd.DataFrame([ferie_row] + planning_data, columns=header).set_index(header[0])
        
        print(f"\n--- PLANNING MENSUEL GROUPE {code_groupe} {mois:02d}/{annee} ---")
        try:
            print(tabulate(df_planning, headers='keys', tablefmt="fancy_grid"))
        except ImportError:
            print(df_planning.to_string())

    def calculer_planning_mensuel_agent(self, code_agent, mois, annee):
        """Calcule et affiche le planning du mois pour un agent spécifique ET ses statistiques."""
        code_agent = code_agent.upper()
        
        self.cursor.execute("SELECT code, nom, prenom FROM agents WHERE code=? AND date_sortie IS NULL", (code_agent,))
        agent_info = self.cursor.fetchone()
        
        if not agent_info:
            print(f"❌ Agent {code_agent} non trouvé ou inactif.")
            return

        code, nom, prenom = agent_info
        _, jours_mois = monthrange(annee, mois)
        
        header = ["Jour", "Date", "Shift", "Férié"] 
        planning_data = []

        for i in range(1, jours_mois + 1):
            jour_date_obj = date(annee, mois, i)
            jour_date_str = jour_date_obj.isoformat()
            jour_semaine = JOURS_FRANCAIS[jour_date_obj.strftime('%a')]
            
            shift = self._get_shift_effectif(code, jour_date_str)
            est_ferie = "Oui" if self._est_jour_ferie(jour_date_str) else ""
            
            planning_data.append([jour_semaine, f"{i:02d}/{mois:02d}", shift, est_ferie])
            
        df_planning = pd.DataFrame(planning_data, columns=header)
        
        print(f"\n--- PLANNING MENSUEL {mois:02d}/{annee} pour {code} - {nom} {prenom} ---")
        try:
            print(df_planning.to_markdown(index=False)) 
        except ImportError:
            print(df_planning.to_string(index=False))

        # AFFICHAGE DES STATISTIQUES INDIVIDUELLES
        self.afficher_statistiques(code_agent, mois, annee)

    def calculer_planning_trimestriel(self, mois_debut, annee):
        """Calcule et affiche le planning trimestriel (3 mois)."""
        print(f"\n--- PLANNING TRIMESTRIEL à partir de {mois_debut:02d}/{annee} ---")
        
        for i in range(3):
            mois_courant = (mois_debut + i - 1) % 12 + 1
            annee_courante = annee + (mois_debut + i - 1) // 12
            
            print(f"\n>>> MOIS {mois_courant:02d}/{annee_courante} <<<")
            self.calculer_planning_mensuel(mois_courant, annee_courante)

    def _calculer_stats_base(self, code_agent, mois, annee):
        """Calcule les statistiques brutes des shifts pour un mois donné - VERSION CORRIGÉE ."""
        _, jours_mois = monthrange(annee, mois)
        stats = {'1': 0, '2': 0, '3': 0, 'R': 0, 'C': 0, 'M': 0, 'A': 0, '-': 0} 
        feries_travailles = 0 
        total_shifts_effectues = 0

        for i in range(1, jours_mois + 1):
            jour_date_str = date(annee, mois, i).isoformat()
            self._get_shift_effectif(code_agent, jour_date_str)

        date_debut = date(annee, mois, 1).isoformat()
        date_fin = date(annee, mois, jours_mois).isoformat()
        
        self.cursor.execute("""
            SELECT shift, date FROM planning 
            WHERE code_agent=? AND date BETWEEN ? AND ?
        """, (code_agent, date_debut, date_fin))
        
        planning_records = self.cursor.fetchall()

        for shift_effectif, jour_date_str in planning_records:
            
            if shift_effectif in stats:
                stats[shift_effectif] += 1
                
                if shift_effectif in ['1', '2', '3']:
                    total_shifts_effectues += 1
                    
                    if self._est_jour_ferie(jour_date_str):
                        feries_travailles += 1 
                        
        # CALCUL  CORRECT : Total shifts opérationnels = shifts normaux + fériés travaillés (crédit prime)
        total_shifts_operationnels = total_shifts_effectues + feries_travailles
                        
        return stats, feries_travailles, total_shifts_effectues, total_shifts_operationnels

    def _calculer_stats_base_global(self, mois, annee):
        """Calcule les statistiques consolidées pour tous les agents actifs."""
        self.cursor.execute("SELECT code FROM agents WHERE date_sortie IS NULL")
        agents_codes = [a[0] for a in self.cursor.fetchall()]
        
        stats_globales = {'1': 0, '2': 0, '3': 0, 'R': 0, 'C': 0, 'M': 0, 'A': 0, '-': 0}
        total_feries_global = 0
        total_shifts_global = 0
        total_operationnels_global = 0

        for code in agents_codes:
            try:
                stats_agent, feries_agent, total_shifts_agent, total_operationnels_agent = self._calculer_stats_base(code, mois, annee)
                for shift_type in stats_globales.keys():
                    stats_globales[shift_type] += stats_agent.get(shift_type, 0)
                total_feries_global += feries_agent
                total_shifts_global += total_shifts_agent
                total_operationnels_global += total_operationnels_agent
            except Exception:
                pass

        return stats_globales, total_feries_global, total_shifts_global, total_operationnels_global

    def afficher_statistiques(self, code_agent, mois, annee):
        """Affiche les statistiques d'un agent ou les statistiques globales pour un mois."""
        
        if code_agent is None:
            stats, total_feries, total_shifts, total_operationnels = self._calculer_stats_base_global(mois, annee)
            titre = f"--- SYNTHÈSE STATISTIQUE GLOBALE {mois:02d}/{annee} ---"
        else:
            code_agent = code_agent.upper()
            self.cursor.execute("SELECT nom, prenom FROM agents WHERE code=?", (code_agent,))
            agent_info = self.cursor.fetchone()
            
            if not agent_info:
                print(f"❌ Agent {code_agent} non trouvé.")
                return

            try:
                stats, total_feries, total_shifts, total_operationnels = self._calculer_stats_base(code_agent, mois, annee)
            except Exception as e:
                print(f"❌ Erreur lors du calcul des statistiques pour {code_agent}: {e}")
                return
            
            titre = f"--- SYNTHÈSE STATISTIQUE MENSUELLE pour {code_agent}   ({mois:02d}/{annee}) ---"

        
        stats_data = [
            ['Shifts Matin (1)', stats.get('1', 0)],
            ['Shifts Après-midi (2)', stats.get('2', 0)],
            ['Shifts Nuit (3)', stats.get('3', 0)],
            ['Jours Repos (R)', stats.get('R', 0)],
            ['Congés (C)', stats.get('C', 0)],
            ['Maladie (M)', stats.get('M', 0)],
            ['Autre Absence (A)', stats.get('A', 0)],
            ['Fériés travaillés (Crédit Prime)', total_feries], 
            ['Non-planifié (-)', stats.get('-', 0)],
            ['**TOTAL SHIFTS OPÉRATIONNELS **', f"**{total_operationnels}**"]
        ]
        
        print(titre)
        print(tabulate(stats_data, headers=["Description", "Jours Effectifs"], tablefmt="fancy_grid"))

    def enregistrer_absence(self, code_agent, jour_date: str, shift_code):
        """Enregistre une absence pour un agent (C, M, A)."""
        code_agent = code_agent.upper()
        shift_code = shift_code.upper()
        if shift_code not in ['C', 'M', 'A']:
            print("❌ Type d'absence invalide. Utilisez C (Congé), M (Maladie) ou A (Autre).")
            return
            
        self.cursor.execute("SELECT code FROM agents WHERE code=? AND date_sortie IS NULL", (code_agent,))
        if not self.cursor.fetchone():
            print(f"❌ Agent {code_agent} non trouvé ou inactif.")
            return

        try:
            self.cursor.execute(
                "INSERT OR REPLACE INTO planning (code_agent, date, shift, origine) VALUES (?, ?, ?, 'ABSENCE')",
                (code_agent, jour_date, shift_code)
            )
            self.conn.commit()
            print(f"✅ Absence ({shift_code}) enregistrée pour {code_agent} le {jour_date}.")
        except Exception as e:
            print(f"❌ Erreur lors de l'enregistrement de l'absence: {e}")

    def modifier_shift_ponctuel(self, code_agent, jour_date: str, nouveau_shift):
        """Modifie le shift ponctuel d'un agent."""
        code_agent = code_agent.upper()
        nouveau_shift = nouveau_shift.upper()
        if nouveau_shift not in ['1', '2', '3', 'R', 'C', 'M', 'A']: 
            print("❌ Shift invalide. Utilisez 1, 2, 3, R, C, M, ou A.")
            return

        self.cursor.execute("SELECT code FROM agents WHERE code=? AND date_sortie IS NULL", (code_agent,))
        if not self.cursor.fetchone():
            print(f"❌ Agent {code_agent} non trouvé ou inactif.")
            return

        try:
            self.cursor.execute(
                "INSERT OR REPLACE INTO planning (code_agent, date, shift, origine) VALUES (?, ?, ?, 'MANUEL')",
                (code_agent, jour_date, nouveau_shift)
            )
            self.conn.commit()
            print(f"✅ Shift de {code_agent} modifié en '{nouveau_shift}' pour le {jour_date}.")
        except Exception as e:
            print(f"❌ Erreur lors de la modification du shift: {e}")

    def echanger_shifts(self, code_agent_a, code_agent_b, jour_date: str):
        """Échange les shifts entre deux agents pour un jour donné."""
        code_agent_a = code_agent_a.upper()
        code_agent_b = code_agent_b.upper()
        
        self.cursor.execute("SELECT code FROM agents WHERE code=? OR code=?", (code_agent_a, code_agent_b))
        if len(self.cursor.fetchall()) < 2:
            print("❌ Un ou les deux agents sont introuvables/inactifs.")
            return

        shift_a = self._get_shift_effectif(code_agent_a, jour_date)
        shift_b = self._get_shift_effectif(code_agent_b, jour_date)
        
        if shift_a == '-' or shift_b == '-':
             print("❌ L'un des agents n'est pas planifié à cette date.")
             return
        
        if shift_a == shift_b:
             print("⚠️ Les deux agents ont déjà le même shift. Aucun échange nécessaire.")
             return

        try:
            self.cursor.execute(
                "INSERT OR REPLACE INTO planning (code_agent, date, shift, origine) VALUES (?, ?, ?, 'ECHANGE')",
                (code_agent_a, jour_date, shift_b)
            )
            self.cursor.execute(
                "INSERT OR REPLACE INTO planning (code_agent, date, shift, origine) VALUES (?, ?, ?, 'ECHANGE')",
                (code_agent_b, jour_date, shift_a)
            )
            self.conn.commit()
            print(f"✅ Échange de shifts réussi pour le {jour_date}: {code_agent_a} a pris {shift_b} et {code_agent_b} a pris {shift_a}.")
        except Exception as e:
            print(f"❌ Erreur lors de l'échange des shifts: {e}")

    # =========================================================================
    # GESTION JOURS FÉRIÉS AUTOMATIQUE MAROC
    # =========================================================================

    def ajouter_jour_ferie(self, jour_date: str, description):
        """Ajoute un jour férié manuellement."""
        try:
            self.cursor.execute(
                "INSERT OR REPLACE INTO jours_feries (date, description) VALUES (?, ?)",
                (jour_date, description)
            )
            self.conn.commit()
            print(f"✅ Jour férié '{description}' ajouté le {jour_date}.")
        except Exception as e:
            print(f"❌ Erreur lors de l'ajout du jour férié: {e}")

    def supprimer_jour_ferie(self, jour_date: str):
        """Supprime un jour férié."""
        try:
            self.cursor.execute("DELETE FROM jours_feries WHERE date=?", (jour_date,))
            if self.cursor.rowcount > 0:
                self.conn.commit()
                self._recalculer_planning_apres_changement_ferie(jour_date)
                print(f"✅ Jour férié du {jour_date} supprimé et planning théorique recalculé.")
            else:
                print(f"⚠️ Aucun jour férié trouvé à cette date: {jour_date}.")
        except Exception as e:
            print(f"❌ Erreur lors de la suppression du jour férié: {e}")

    def _recalculer_planning_apres_changement_ferie(self, jour_date_str):
        """Efface les shifts théoriques pour un jour donné pour forcer la regénération."""
        try:
            self.cursor.execute("DELETE FROM planning WHERE date = ? AND origine = 'THEORIQUE'", (jour_date_str,))
            self.conn.commit()
        except Exception as e:
            print(f"❌ Erreur lors du recalcul après changement de jour férié: {e}")

    def _est_jour_ferie(self, jour_date: str):
        """Vérifie si une date est un jour férié (automatique Maroc + manuel)."""
        # Vérifier d'abord les jours fériés manuels
        self.cursor.execute("SELECT 1 FROM jours_feries WHERE date=?", (jour_date,))
        if self.cursor.fetchone() is not None:
            return True
        
        # Vérifier les jours fériés automatiques du Maroc
        return self._est_jour_ferie_maroc(jour_date)

    def _est_jour_ferie_maroc(self, jour_date: str):
        """Détermine si une date est un jour férié au Maroc (calcul automatique)."""
        from datetime import date
        
        try:
            annee = int(jour_date[:4])
            mois = int(jour_date[5:7])
            jour = int(jour_date[8:10])
            date_obj = date(annee, mois, jour)
        except:
            return False
        
        # JOURS FÉRIÉS FIXES DU MAROC
        jours_feries_fixes = {
            (1, 1): "Nouvel An",
            (1, 11): "Manifeste de l'Indépendance",
            (5, 1): "Fête du Travail",
            (7, 30): "Fête du Trône",
            (8, 14): "Allégeance Oued Eddahab",
            (8, 20): "Révolution du Roi et du Peuple", 
            (8, 21): "Fête de la Jeunesse",
            (11, 6): "Marche Verte",
            (11, 18): "Fête de l'Indépendance"
        }
        
        # Vérifier les jours fixes
        if (mois, jour) in jours_feries_fixes:
            return True
        
        return False

    def lister_jours_feries(self, annee):
        """Liste tous les jours fériés (automatiques + manuels) pour une année donnée."""
        from datetime import date
        
        print(f"\n--- JOURS FÉRIÉS POUR {annee} (MAROC) ---")
        
        # Jours fériés fixes automatiques
        print("🔹 Jours fériés fixes (automatiques):")
        jours_fixes = [
            (date(annee, 1, 1), "Nouvel An"),
            (date(annee, 1, 11), "Manifeste de l'Indépendance"),
            (date(annee, 5, 1), "Fête du Travail"),
            (date(annee, 7, 30), "Fête du Trône"),
            (date(annee, 8, 14), "Allégeance Oued Eddahab"),
            (date(annee, 8, 20), "Révolution du Roi et du Peuple"),
            (date(annee, 8, 21), "Fête de la Jeunesse"),
            (date(annee, 11, 6), "Marche Verte"),
            (date(annee, 11, 18), "Fête de l'Indépendance")
        ]
        
        for date_ferie, description in sorted(jours_fixes):
            print(f"   {date_ferie} : {description}")
        
        # Jours fériés manuels
        date_debut = f"{annee}-01-01"
        date_fin = f"{annee}-12-31"
        
        self.cursor.execute("SELECT date, description FROM jours_feries WHERE date BETWEEN ? AND ? ORDER BY date", (date_debut, date_fin))
        feries_manuels = self.cursor.fetchall()
        
        if feries_manuels:
            print("\n🔹 Jours fériés manuels ajoutés:")
            for jour_date, description in feries_manuels:
                print(f"   {jour_date} : {description} (manuel)")

    # =========================================================================
    # GESTION DES CODES PANIQUE
    # =========================================================================

    def ajouter_modifier_code_panique(self, code_agent, code_panique, poste_nom):
        """Ajoute ou modifie le code panique pour un agent."""
        code_agent = code_agent.upper()
        try:
            self.cursor.execute(
                "INSERT OR REPLACE INTO codes_panique (code_agent, code_panique, poste_nom) VALUES (?, ?, ?)",
                (code_agent, code_panique, poste_nom)
            )
            self.conn.commit()
            print(f"✅ Code panique pour {code_agent} mis à jour : {code_panique} ({poste_nom}).")
        except Exception as e:
            print(f"❌ Erreur lors de l'ajout/modification du code panique: {e}")

    def lister_codes_panique(self):
        """Liste tous les codes panique."""
        self.cursor.execute("""
            SELECT c.code_agent, a.nom, a.prenom, c.code_panique, c.poste_nom 
            FROM codes_panique c JOIN agents a ON c.code_agent = a.code
            ORDER BY c.code_agent
        """)
        codes = self.cursor.fetchall()
        if not codes:
            print("⚠️ Aucun code panique enregistré.")
            return

        print("\n--- CODES PANIQUE ENREGISTRÉS ---")
        headers = ["Code Agent", "Nom Prénom", "Code Panique", "Poste"]
        data = [[c[0], f"{c[1]} {c[2]}", c[3], c[4]] for c in codes]
        print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

    def supprimer_code_panique(self, code_agent):
        """Supprime le code panique d'un agent."""
        code_agent = code_agent.upper()
        try:
            self.cursor.execute("DELETE FROM codes_panique WHERE code_agent=?", (code_agent,))
            if self.cursor.rowcount > 0:
                self.conn.commit()
                print(f"✅ Code panique de {code_agent} supprimé.")
            else:
                print(f"⚠️ Aucun code panique trouvé pour l'agent {code_agent}.")
        except Exception as e:
            print(f"❌ Erreur lors de la suppression du code panique: {e}")

    # =========================================================================
    # GESTION DU MATÉRIEL RADIO
    # =========================================================================

    def ajouter_modifier_radio(self, id_radio, modele, statut):
        """Ajoute ou modifie une radio."""
        id_radio = id_radio.upper()
        statut = statut.upper()
        if statut not in ['DISPONIBLE', 'HS', 'RÉPARATION', 'ATTRIBUÉE']:
            print("❌ Statut invalide. Utilisez Disponible, HS, Réparation ou Attribuée.")
            return

        try:
            self.cursor.execute(
                "INSERT OR REPLACE INTO radios (id_radio, modele, statut) VALUES (?, ?, ?)",
                (id_radio, modele, statut)
            )
            self.conn.commit()
            print(f"✅ Radio {id_radio} ({modele}) mise à jour. Statut: {statut}.")
        except Exception as e:
            print(f"❌ Erreur lors de l'ajout/modification de la radio: {e}")

    def attribuer_radio(self, id_radio, code_agent):
        """Attribue une radio à un agent."""
        id_radio = id_radio.upper()
        code_agent = code_agent.upper()
        date_attribution = date.today().isoformat()
        
        self.cursor.execute("SELECT statut FROM radios WHERE id_radio=?", (id_radio,))
        radio_statut = self.cursor.fetchone()
        
        if not radio_statut:
            print(f"❌ Radio {id_radio} non trouvée.")
            return
        if radio_statut[0] != 'DISPONIBLE':
            print(f"⚠️ Radio {id_radio} n'est pas DISPONIBLE (Statut: {radio_statut[0]}).")
            return
        
        try:
            self.cursor.execute("UPDATE radios SET statut='ATTRIBUÉE' WHERE id_radio=?", (id_radio,))
            
            self.cursor.execute(
                "INSERT INTO historique_radio (id_radio, code_agent, date_attribution, date_retour) VALUES (?, ?, ?, NULL)",
                (id_radio, code_agent, date_attribution)
            )
            self.conn.commit()
            print(f"✅ Radio {id_radio} attribuée à l'agent {code_agent} le {date_attribution}.")
        except Exception as e:
            print(f"❌ Erreur lors de l'attribution de la radio: {e}")

    def enregistrer_retour_radio(self, id_radio):
        """Enregistre le retour d'une radio et la marque comme DISPONIBLE."""
        id_radio = id_radio.upper()
        date_retour = date.today().isoformat()
        
        self.cursor.execute("SELECT statut FROM radios WHERE id_radio=?", (id_radio,))
        radio_statut = self.cursor.fetchone()
        
        if not radio_statut:
            print(f"❌ Radio {id_radio} non trouvée.")
            return
        if radio_statut[0] != 'ATTRIBUÉE':
            print(f"⚠️ Radio {id_radio} n'est pas marquée comme ATTRIBUÉE (Statut: {radio_statut[0]}).")
            return

        try:
            self.cursor.execute("UPDATE radios SET statut='DISPONIBLE' WHERE id_radio=?", (id_radio,))
            
            self.cursor.execute(
                """UPDATE historique_radio SET date_retour=? 
                   WHERE id_radio=? AND date_retour IS NULL""",
                (date_retour, id_radio)
            )
            self.conn.commit()
            print(f"✅ Radio {id_radio} retournée et marquée comme DISPONIBLE le {date_retour}.")
        except Exception as e:
            print(f"❌ Erreur lors de l'enregistrement du retour de la radio: {e}")

    def rapport_statut_radios(self):
        """Affiche le statut actuel de toutes les radios."""
        self.cursor.execute("""
            SELECT r.id_radio, r.modele, r.statut, 
                   h.code_agent, a.prenom, a.nom
            FROM radios r
            LEFT JOIN historique_radio h ON r.id_radio = h.id_radio AND h.date_retour IS NULL
            LEFT JOIN agents a ON h.code_agent = a.code
            ORDER BY r.id_radio
        """)
        rapport = self.cursor.fetchall()

        if not rapport:
            print("⚠️ Aucune radio enregistrée.")
            return

        print("\n--- RAPPORT DE STATUT DES RADIOS ---")
        headers = ["ID Radio", "Modèle", "Statut", "Attribué à"]
        data = []
        for id_r, modele, statut, code_a, prenom, nom in rapport:
            if statut == 'ATTRIBUÉE' and code_a:
                attribue = f"{code_a} - {prenom} {nom}"
            else:
                attribue = ""
            data.append([id_r, modele, statut, attribue])
            
        print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

    # =========================================================================
    # EXPORTATIONS
    # =========================================================================

    def exporter_stats_excel(self, mois, annee, nom_fichier):
        """Exporte les statistiques complètes de tous les agents pour le mois donné."""
        if not nom_fichier.lower().endswith('.xlsx'):
            nom_fichier += '.xlsx'
            
        self.cursor.execute("SELECT code, nom, prenom, code_groupe FROM agents WHERE date_sortie IS NULL ORDER BY code_groupe, code")
        agents_info = self.cursor.fetchall()
        
        stats_data = []
        for code, nom, prenom, groupe in agents_info:
            stats, feries, total_shifts, total_operationnels = self._calculer_stats_base(code, mois, annee)
            
            row = {
                'Code': code,
                'Nom': nom,
                'Prénom': prenom,
                'Groupe': groupe,
                'Shifts Matin (1)': stats.get('1', 0),
                'Shifts Après-midi (2)': stats.get('2', 0),
                'Shifts Nuit (3)': stats.get('3', 0),
                'Repos (R)': stats.get('R', 0),
                'Congés (C)': stats.get('C', 0),
                'Maladie (M)': stats.get('M', 0),
                'Autres (A)': stats.get('A', 0),
                'Fériés (Crédit Prime)': feries,
                'TOTAL SHIFTS OPÉRATIONNELS (CPA)': total_operationnels
            }
            stats_data.append(row)
            
        df_stats = pd.DataFrame(stats_data)

        try:
            df_stats.to_excel(nom_fichier, index=False, sheet_name=f"Stats_{mois:02d}_{annee}")
            print(f"✅ Statistiques complètes exportées dans '{nom_fichier}'.")
        except Exception as e:
            print(f"❌ Erreur lors de l'exportation des statistiques en Excel: {e}")

    def exporter_planning_mensuel_global(self, mois, annee, nom_fichier):
        """Exporte le planning mensuel global (Tous agents) en Excel."""
        if not nom_fichier.lower().endswith('.xlsx'):
            nom_fichier += '.xlsx'
        
        # Réutilise la logique de calculer_planning_mensuel pour obtenir le DataFrame
        df_planning = self.calculer_planning_mensuel(mois, annee) 
        
        try:
            df_planning.to_excel(nom_fichier, sheet_name=f"Planning_Global_{mois:02d}_{annee}")
            print(f"✅ Planning mensuel global exporté dans '{nom_fichier}'.")
        except Exception as e:
            print(f"❌ Erreur lors de l'exportation du planning global en Excel: {e}")

    def exporter_planning_mensuel_agent(self, code_agent, mois, annee, nom_fichier):
        """Exporte le planning mensuel d'un seul agent."""
        code_agent = code_agent.upper()
        if not nom_fichier.lower().endswith('.xlsx'):
            nom_fichier += '.xlsx'

        self.cursor.execute("SELECT nom, prenom FROM agents WHERE code=? AND date_sortie IS NULL", (code_agent,))
        agent_info = self.cursor.fetchone()
        
        if not agent_info:
            print(f"❌ Agent {code_agent} non trouvé ou inactif.")
            return

        _, jours_mois = monthrange(annee, mois)
        
        header = ["Jour", "Date", "Shift", "Férié"]
        planning_data = []

        for i in range(1, jours_mois + 1):
            jour_date_obj = date(annee, mois, i)
            jour_date_str = jour_date_obj.isoformat()
            jour_semaine = JOURS_FRANCAIS[jour_date_obj.strftime('%a')]
            
            shift = self._get_shift_effectif(code_agent, jour_date_str)
            est_ferie = "Oui" if self._est_jour_ferie(jour_date_str) else ""
            
            planning_data.append([jour_semaine, f"{i:02d}/{mois:02d}", shift, est_ferie])
            
        df_planning = pd.DataFrame(planning_data, columns=header)
        
        try:
            df_planning.to_excel(nom_fichier, index=False, sheet_name=f"{code_agent}_{mois:02d}_{annee}")
            print(f"✅ Planning mensuel pour l'agent {code_agent} ({agent_info[0]} {agent_info[1]}) exporté dans '{nom_fichier}'.")
        except Exception as e:
            print(f"❌ Erreur lors de l'exportation du planning en Excel: {e}")

    # =========================================================================
    # GESTION HABILLEMENT
    # =========================================================================

    def ajouter_modifier_habillement(self, code_agent, habillement_data):
        """Ajoute ou modifie les informations d'habillement d'un agent."""
        code_agent = code_agent.upper()
        try:
            self.cursor.execute(
                """INSERT OR REPLACE INTO habillement (code_agent, chemise_taille, chemise_date, jacket_taille, jacket_date, pantalon_taille, pantalon_date, cravate_oui, cravate_date) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (code_agent,
                 habillement_data['chemise'][0], habillement_data['chemise'][1],
                 habillement_data['jacket'][0], habillement_data['jacket'][1],
                 habillement_data['pantalon'][0], habillement_data['pantalon'][1],
                 habillement_data['cravate'][0], habillement_data['cravate'][1])
            )
            self.conn.commit()
            print(f"✅ Informations d'habillement pour {code_agent} mises à jour.")
        except Exception as e:
            print(f"❌ Erreur lors de l'ajout/modification de l'habillement: {e}")

    def rapport_habillement(self):
        """Affiche un rapport global des tailles d'habillement et des dates de fourniture."""
        self.cursor.execute("""
            SELECT a.code, a.nom, a.prenom, h.chemise_taille, h.chemise_date, 
                   h.jacket_taille, h.jacket_date, h.pantalon_taille, h.pantalon_date, 
                   h.cravate_oui, h.cravate_date
            FROM agents a 
            LEFT JOIN habillement h ON a.code = h.code_agent
            WHERE a.date_sortie IS NULL
            ORDER BY a.code
        """)
        rapport = self.cursor.fetchall()

        if not rapport:
            print("⚠️ Aucun agent actif trouvé pour le rapport d'habillement.")
            return

        print("\n--- RAPPORT GLOBAL DES HABILLEMENTS ---")
        headers = ["Agent", "Nom Prénom", "Chemise (T/D)", "Jacket (T/D)", "Pantalon (T/D)", "Cravate (O/N/D)"]
        data = []
        for row in rapport:
            code, nom, prenom = row[0], row[1], row[2]
            
            chemise = f"{row[3] or '-'} / {row[4] or '-'}"
            jacket = f"{row[5] or '-'} / {row[6] or '-'}"
            pantalon = f"{row[7] or '-'} / {row[8] or '-'}"
            cravate = f"{row[9] or '-'} / {row[10] or '-'}"
            
            data.append([code, f"{nom} {prenom}", chemise, jacket, pantalon, cravate])
            
        print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

    # =========================================================================
    # GESTION DES AVERTISSEMENTS
    # =========================================================================

    def enregistrer_avertissement(self, code_agent, date_av, type_av, description):
        """Enregistre un avertissement disciplinaire pour un agent."""
        code_agent = code_agent.upper()
        type_av = type_av.upper()
        if type_av not in ['ORAL', 'ECRIT', 'MISE_A_PIED']:
            print("❌ Type d'avertissement invalide (ORAL, ECRIT, MISE_A_PIED).")
            return

        try:
            self.cursor.execute(
                "INSERT INTO avertissements (code_agent, date_avertissement, type_avertissement, description) VALUES (?, ?, ?, ?)",
                (code_agent, date_av, type_av, description)
            )
            self.conn.commit()
            print(f"✅ Avertissement ({type_av}) enregistré pour {code_agent} le {date_av}.")
        except Exception as e:
            print(f"❌ Erreur lors de l'enregistrement de l'avertissement: {e}")

    def historique_avertissements_agent(self, code_agent):
        """Affiche l'historique des avertissements d'un agent."""
        code_agent = code_agent.upper()
        self.cursor.execute("""
            SELECT date_avertissement, type_avertissement, description 
            FROM avertissements 
            WHERE code_agent=? 
            ORDER BY date_avertissement DESC
        """, (code_agent,))
        historique = self.cursor.fetchall()
        
        if not historique:
            print(f"⚠️ Aucun avertissement trouvé pour l'agent {code_agent}.")
            return

        print(f"\n--- HISTORIQUE DES AVERTISSEMENTS pour {code_agent} ---")
        headers = ["Date", "Type", "Description"]
        print(tabulate(historique, headers=headers, tablefmt="fancy_grid"))

    def rapport_global_avertissements(self):
        """Affiche un rapport global de tous les avertissements actifs."""
        self.cursor.execute("""
            SELECT a.code, a.nom, a.prenom, av.date_avertissement, av.type_avertissement, av.description
            FROM avertissements av
            JOIN agents a ON av.code_agent = a.code
            WHERE a.date_sortie IS NULL
            ORDER BY av.date_avertissement DESC, a.code
        """)
        rapport = self.cursor.fetchall()
        
        if not rapport:
            print("⚠️ Aucun avertissement actif trouvé.")
            return

        print("\n--- RAPPORT GLOBAL DES AVERTISSEMENTS ACTIFS ---")
        headers = ["Agent", "Nom Prénom", "Date", "Type", "Description"]
        data = [[r[0], f"{r[1]} {r[2]}", r[3], r[4], r[5]] for r in rapport]
        print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

    # =========================================================================
    # MÉTHODES POUR L'API WEB
    # =========================================================================

    def recuperer_agents_pour_api(self):
        """Récupère tous les agents actifs pour l'API web"""
        try:
            self.cursor.execute("""
                SELECT code, nom, prenom, code_groupe, date_entree, statut 
                FROM agents 
                WHERE date_sortie IS NULL 
                ORDER BY code_groupe, code
            """)
            agents = []
            for row in self.cursor.fetchall():
                agents.append({
                    'id': row[0],
                    'code': row[0],
                    'nom': row[1],
                    'prenom': row[2],
                    'code_groupe': row[3],
                    'date_entree': row[4],
                    'statut': row[5] if row[5] else 'actif'
                })
            return agents
        except Exception as e:
            print(f"❌ Erreur récupération agents API: {e}")
            return []

    def recuperer_planning_mensuel_api(self, mois, annee):
        """Récupère le planning mensuel pour l'API web"""
        try:
            _, jours_mois = monthrange(annee, mois)
            planning_data = []
            
            # Récupérer tous les agents actifs
            agents = self.recuperer_agents_pour_api()
            
            for jour in range(1, jours_mois + 1):
                date_str = date(annee, mois, jour).isoformat()
                jour_data = {
                    'date': date_str,
                    'jour_semaine': JOURS_FRANCAIS[date(annee, mois, jour).strftime('%a')],
                    'shifts': {}
                }
                
                for agent in agents:
                    shift = self._get_shift_effectif(agent['code'], date_str)
                    jour_data['shifts'][agent['code']] = shift
                
                planning_data.append(jour_data)
            
            return {
                'mois': mois,
                'annee': annee,
                'planning': planning_data,
                'agents': agents
            }
        except Exception as e:
            print(f"❌ Erreur récupération planning API: {e}")
            return {}

    def get_stats_globales_api(self):
        """Récupère les statistiques globales pour l'API web"""
        try:
            # Compter les agents par groupe
            self.cursor.execute("""
                SELECT code_groupe, COUNT(*) 
                FROM agents 
                WHERE date_sortie IS NULL 
                GROUP BY code_groupe
            """)
            groupes_stats = {row[0]: row[1] for row in self.cursor.fetchall()}
            
            # Agents totaux
            total_agents = sum(groupes_stats.values())
            
            # Planning du jour
            aujourdhui = date.today().isoformat()
            self.cursor.execute("SELECT COUNT(*) FROM planning WHERE date = ? AND shift IN ('1', '2', '3')", (aujourdhui,))
            shifts_aujourdhui = self.cursor.fetchone()[0] or 0
            
            return {
                'total_agents': total_agents,
                'active_agents': total_agents,
                'present_today': shifts_aujourdhui,
                'shifts_today': shifts_aujourdhui,
                'groupes': groupes_stats,
                'radios_disponibles': self._compter_radios_disponibles(),
                'avertissements_actifs': self._compter_avertissements_actifs()
            }
        except Exception as e:
            print(f"❌ Erreur stats API: {e}")
            return {}

    def _compter_radios_disponibles(self):
        """Compte les radios disponibles"""
        try:
            self.cursor.execute("SELECT COUNT(*) FROM radios WHERE statut = 'DISPONIBLE'")
            return self.cursor.fetchone()[0] or 0
        except:
            return 0

    def _compter_avertissements_actifs(self):
        """Compte les avertissements actifs"""
        try:
            self.cursor.execute("""
                SELECT COUNT(*) FROM avertissements av
                JOIN agents a ON av.code_agent = a.code
                WHERE a.date_sortie IS NULL
            """)
            return self.cursor.fetchone()[0] or 0
        except:
            return 0

    def ajouter_agent_via_api(self, data):
        """Ajoute un agent via l'API web"""
        try:
            return self.ajouter_agent(
                data['code'],
                data['nom'],
                data['prenom'], 
                data['code_groupe']
            )
        except Exception as e:
            print(f"❌ Erreur ajout agent API: {e}")
            return False

if __name__ == "__main__":
    # Test de la classe
    gestion = GestionAgents()
    print("✅ Module gestion_agents chargé avec succès!")
