import pandas as pd

def creer_mon_fichier_excel():
    """Crée un fichier Excel avec TOUS les 145 agents et TOUTES leurs données"""
    
    # TOUS LES 145 AGENTS AVEC DONNÉES COMPLÈTES
    vos_agents = [
        # Format: [Code, Nom, Prénom, Groupe, Téléphone, Adresse, Code_Panique, Poste, CIN, Date_Naissance, Matricule]
        
        # GROUPE A (37 agents)
        ['CPA', 'OUKHA', 'NABIL', 'A', '681564713854', '', 'CPA758609', '', 'J767890', '05/11/1974', 'S09278C'],
        ['CONA', 'EL JAMALI', 'Younes', 'A', '663290648', 'DP1400', 'CONA', '', 'A370180', '04/09/1992', 'S09425C'],
        ['MOTA', 'TISSIRT', 'hakim', 'A', '611160166', 'DP1400', 'MOT', '', 'B230482', '20/10/1968', 'S09279C'],
        ['ZA', 'DRAF', 'ANoureddine', 'A', '603482589815', '', 'ZA469875', '', '', '15/05/1974', 'S09179C'],
        ['Z2A', 'KAROUCHE', 'Fayçal', 'A', '', 'DP1400', 'Z2A743534', '', '', '', 'S13273C'],
        ['Z5A', 'LAWRIQAT TARIK', 'TARIK', 'A', '615296161', 'DP1400', 'Z5A794204', '', '', '17/04/1979', 'S11699C'],
        ['z6A', 'HARBIL', 'ANASS', 'A', '669001099', 'DP1400', 'z6A434690', '', '', '26/02/1984', 'S09153C'],
        ['Z7A', 'CHERKAOUI NOUA', 'AMAN', 'A', '', 'DP1400', 'Z7A', '', 'D216143', '01/12/1992', 'S11869C'],
        ['O1a', 'AALAMI ZAKARIA', '', 'A', '660269360913', '', 'O1aD990488', '', '', '02/06/1987', 'S09188C'],
        ['O1b', 'EL KADMIRI', 'YASSINE', 'A', '707937021228', '', 'O1bAA253632', '', '', '22/10/1986', 'S12667C'],
        ['O3A', 'EL GHALLA', 'ABDELALI', 'A', '663391782511', '', 'O3A729822', '', '', '30/06/1976', 'S09216C'],
        ['O4A', 'ANQACH', 'HASSAN', 'A', '313', '', 'O422745', '', '', '', 'RETRAITE'],
        ['O5A', 'LEKHEL', 'RACHID', 'A', '644734747848', '', 'O522984', '', '', '', 'RETRAITE'],
        ['O8A', 'AIT LMKADAM', 'LAHCEN', 'A', '626521862824', '', 'O8PB427081', '', '', '19/11/1977', 'S09229C'],
        ['O9A', 'OUTANOUT', 'OMAR', 'A', '6943677602813', '', 'O9A651335', '', '', '03/01/1972', 'S09251C'],
        ['O10A', 'ZOUHRI', 'HAMID', 'A', '625615979911', '', 'O10Z155268', '', '', '19/12/1968', 'S09861C'],
        ['O11A', 'ARRADI', 'TARIK', 'A', '326', '', 'O11AA345212', '', '', '25/11/1990', 'S09284C'],
        ['O12A', 'BOULAHFA', 'MOHAMED', 'A', '667877556855', '', 'O12FL33963', '', '', '30/06/1965', 'S09234C'],
        ['O13A', 'ZDIHRI', 'ABDERAHIM', 'A', '667370493826', '', 'O13AB187620', '', '', '05/11/1967', 'S09204C'],
        ['O14A', 'EL KHAOUI', 'ABDELTIF', 'A', '670768055838', '', 'O1422396', '', '', '', 'RETRAITE'],
        ['O15A', 'AIT BENALI', 'ABLKRIM', 'A', '641103141113', '', 'O15AD171008', '', '', '26/05/1987', 'S12072C'],
        ['O16A', 'HOUMMAY', 'MEHDI', 'A', '660994944827', '', 'O16AA33782', '', '', '22/09/1983', 'S09159C'],
        ['LIMA 2A', 'OUSSALLEM', 'KHALID', 'A', '715929737126', '', 'LIMA 2A653628', '', '', '29/07/1970', 'S09166C'],
        ['LIMA 4A', 'SAKANI', 'ABDELAZIZ', 'A', '842', '', 'LIMA 4', '', '', '', ''],
        ['L5A', 'SLYI', 'MOHAMED', 'A', '649068606913', '', 'L5AB129122', '', '', '22/03/1965', 'S09212C'],
        ['L6A', 'KHTIDAK', 'HICHAM', 'A', '660124827841', '', 'L6A766806', '', '', '09/09/1977', 'S09228C'],
        ['L7A', 'ECHOUHAIDI', 'RACHID', 'A', '670444699327', '', 'L7A471850', '', '', '24/02/1974', 'S09254C'],
        ['L8A', 'ABOUKAL', 'SAID', 'A', '661541861815', '', 'L8A418554', '', '', '11/04/1971', 'S09207C'],
        ['L9A', 'MOUNIR', 'IKHLOUFEN', 'A', '762695160914', '', 'L9AE234817', '', '', '17/06/1996', 'S12075C'],
        ['L10A', 'AMHZOUL', 'MUSTAPHA', 'A', '707331929926', '', 'L1022552', '', '', '', 'RETRAITE'],
        ['L11A', 'QOTBI', 'OTMAN', 'A', '681688161125', '', 'L11AA182381', '', '', '19/11/1986', 'S09156C'],
        ['L13A', 'ZEHDI', 'SALEM', 'A', '666788715118', '', 'L13A569901', '', '', '01/12/1967', 'S10068C'],
        ['L14A', 'BOUNHAR', 'MOHAMED', 'A', '614445839858', '', 'L14A772206', '', '', '23/04/1976', 'S09235C'],
        ['L15A', 'BOUCHRIHA', 'MOUNIR', 'A', '641871461999', '', 'L15A774225', '', '', '04/12/1978', 'S09424C'],
        ['L16A', 'ROUANI', 'AYOUB', 'A', '612510273328', '', 'L16AA48291', '', '', '07/06/1991', 'S09172C'],
        ['L18A', 'EL KAHLAOUI', 'ABDELLAH', 'A', '671415745826', '', 'L18A724698', '', '', '18/02/1975', 'S09199C'],
        ['L 20A', 'SATANI', 'BRAHIM', 'A', '660082965922', '', 'L 20', '', '', '', ''],
        
        # GROUPE B (36 agents)
        ['CPB', 'CHMARE', 'KHB', 'B', '660337343', '', 'A604196', '', '', '24/11/1971', 'S09274C'],
        ['CONB', 'IBRAHIM', 'Y', 'B', '662815350', '', 'C475743', '', '', '15/03/1976', 'S09275C'],
        ['MOTB', 'KAALI', 'B', 'B', '0777934644', '', 'Q210329', '', '', '25/11/1978', 'S12666C'],
        ['ZB', 'AIT OUMGHAR', 'ABDELAZIZ', 'B', '673743341', '', 'E284486', '', '', '23558', 'S09195C'],
        ['Z2B', 'TSOULI', 'ADIL', 'B', '0767872200', '', 'A414286', '', '', '44013', 'S09170C'],
        ['Z5B', 'KAMOUN', 'YOUNESS', 'B', '', '', 'C436844', '', '', '12/05/1971', 'S09180C'],
        ['z6B', 'ROCHDI', 'HASSAN', 'B', '65539574', '', 'A594182', '', '', '15/10/1969', 'S09173C'],
        ['Z7B', 'ATRASSI', 'TOUFIQ', 'B', '', '', '', '', '', '', ''],
        ['O1aB', 'JELOULI', 'MAROUAN', 'B', '637401598', '', 'AB335545', '', '', '30/01/1986', 'S09186C'],
        ['O1bB', 'KADI', 'ANNOUAR', 'B', '642889596', '', 'AE110942', '', '', '11/09/1990', 'S12672C'],
        ['O3B', 'EL FADEL', 'MOHAMED', 'B', '762731541', '', 'A783152', '', '', '28109', 'S09239C'],
        ['O4B', 'BOUAKRA', 'ABDELHAK', 'B', '673978815', '', 'A758824', '', '', '04/02/1972', 'S09197C'],
        ['O5B', 'HOUCINE', 'ASGHEN', 'B', '617152230', '', 'CB42565', '', '', '10/10/1972', 'S09225C'],
        ['O8B', 'RIFKI', 'KAMAL', 'B', '677019711', '', 'AB706610', '', '', '26/05/1982', 'S09185C'],
        ['O9B', 'HADIR', 'HAKIM', 'B', '622379633', '', 'AD217181', '', '', '30490', 'S09158C'],
        ['O10B', 'MOHAMED', 'BELASRI', 'B', '670108838', '', 'A755100', '', '', '25/05/1971', 'S09244C'],
        ['O11B', 'OUSSAAMA', 'MANSOURI', 'B', '691484070', '', 'A728886', '', '', '20/10/1975', 'S09956C'],
        ['O12B', 'MOHCINE', 'LAHYANE', 'B', '676454181', '', 'A779095', '', '', '06/02/1981', 'S12134C'],
        ['O13B', 'HASSAN', 'ABDOUSSI', 'B', '645308599', '', 'D424329', '', '', '28/11/1973', 'S09218C'],
        ['O14B', 'MOHAMED', 'ABEID', 'B', '663738283', '', 'A767986', '', '', '12/06/1972', 'S11698C'],
        ['O15B', 'ABDEHADI', 'FAKHAR', 'B', '648941710', '', 'AA207650', '', '', '08/11/1988', 'S11645C'],
        ['O16B', 'TAOUFIK', 'NAIM', 'B', '636552127', '', 'A762084', '', '', '15/12/1972', 'S09250C'],
        ['LIMA 2B', 'ZAHI', 'MOHAMED', 'B', '671614828', '', 'A566655', '', '', '20/03/1969', 'S09243C'],
        ['LIMA 4B', 'KHODAYR', 'AB', 'B', '696893480', '', 'A660675', '', '', '30357', 'S09162C'],
        ['L5B', 'BELAHMAR', 'MOHAMED', 'B', '676120413', '', 'AA207653', '', '', '2456', 'S11645C'],
        ['L6B', 'YOUSSEF', 'RACHAD', 'B', '608980660', '', 'AD152284', '', '', '10/09/1986', 'S09167C'],
        ['L7B', 'KADDAR', 'ANOUAR', 'B', '0610425223', '', 'AB155974', '', '', '27555', 'S09161C'],
        ['L8B', 'OUHADI', 'AHMED', 'B', '670469944', '', 'FL74690', '', '', '01/01/1968', 'S11697C'],
        ['L9B', 'EL HAMROUCHI', 'BOUZIANE', 'B', '0662765085', '', 'H207682', '', '', '38496', 'S12668C'],
        ['L10B', 'AKRAOUI', 'ABDELHAK', 'B', '660387282', '', 'AD57067', '', '', '01/01/1977', 'S09382C'],
        ['L11B', 'AHMED', 'NOUASSI', 'B', '666276247', '', 'A319132', '', '', '11/01/1968', 'S09211C'],
        ['L13B', 'RACHID', 'DAOU', 'B', '677772015', '', 'X127977', '', '', '01/08/1970', 'S09253C'],
        ['L14B', 'KANOUBI', 'ABDELGHANI', 'B', '606656164', '', 'A752774', '', '', '28/11/1970', 'S12670C'],
        ['L15B', 'HAMZA', 'BOUTJADIR', 'B', '615183020', '', 'AA40770', '', '', '30/06/1987', 'S09423C'],
        ['L16B', 'TAOUZI', 'NOUREDDINE', 'B', '767872200', '', 'A414286', '', '', '04/08/1970', 'S09169C'],
        ['L18B', 'SAKANI', 'ABDELAZIZ', 'B', '0662509676', '', 'Z428454', '', '', '31422', 'S13153C'],
        ['L 20B', 'SAID', 'RACHAKHA', 'B', '0648758364', '', 'RRR', '', '', '', ''],
        
        # GROUPE C (36 agents)
        ['CPC', 'BERRIMA', 'C', 'C', '660337343', '', 'A403963', '', '', '24/02/1967', 'S09271C'],
        ['CONC', 'HICHAM', 'NOUR', 'C', '665484503', '', 'A714632', '', '', '03/02/1982', 'S09174C'],
        ['MOTC', 'IDRISSI', 'C', 'C', '667999548', '', 'AB171068', '', '', '24/12/1972', 'S09276C'],
        ['ZC', 'mehdi', '', 'C', '665233677', '', 'AB47887', '', '', '15/01/1968', 'S09268C'],
        ['Z2C', 'GRINEH', 'KHALID', 'C', '', '', 'A670880', '', '', '29/09/1976', 'S09176C'],
        ['Z5C', 'MUSTAPHA', 'MULouANI', 'C', '661970781', '', 'AB96201', '', '', '18/11/1969', 'S09165C'],
        ['z6C', 'MOUSTAKIM', 'MOHA', 'C', '654718291', '', 'A764411', '', '', '15/07/1975', 'S09246C'],
        ['Z7C', 'EL AOUKLI', 'MOHAMED', 'C', '', '', '', '', '', '', ''],
        ['O1aC', 'ELKERRAOUI', 'JAOUAD', 'C', '', '', 'A471219', '', '', '21/10/1973', 'S09184C'],
        ['O1bC', 'CHOUKAIRI', 'AZIZ', 'C', '637014737', '', '', '', '', '22/04/1966', 'S09196C'],
        ['O3C', 'MAKAN', 'YOUNESS', 'C', '624125461', '', 'A070426', '', '', '03/07/1977', 'S09262C'],
        ['O4C', 'HMIJAN', 'BRAHIM', 'C', '678490326', '', '', '', '', '18/04/1985', 'S09214C'],
        ['O5C', 'ATTOUMI', 'YOUSSEF', 'C', '676800556', '', 'QA28049', '', '', '20/03/1970', 'S09263C'],
        ['O8C', 'TAOUFIKI', '', 'C', '656935477', '', 'BE58437', '', '', '01/08/1971', 'S09249C'],
        ['O9C', 'MOHAMED', 'ELYOUSSFI', 'C', '6666624637', '', 'AD148238', '', '', '05/02/1985', 'S09217C'],
        ['O10C', 'KHTIDAK', 'MOHAMED', 'C', '661564216', '', 'A315369', '', '', '14/09/1966', 'S09270C'],
        ['O11C', 'ARIBATE', 'MUSTAPHA', 'C', '660413159', '', 'A755764', '', '', '21/12/1973', 'S09178C'],
        ['O12C', 'AZERFI', 'SAID', 'C', '672499982', '', '22462', '', '', '', 'RETRAITE'],
        ['O13C', 'SAIB', 'HAMID', 'C', '642234491', '', 'AB81211', '', '', '30/06/1984', 'S09168C'],
        ['O14C', 'ALOUI', 'RACHID', 'C', '675660099', '', 'AB192453', '', '', '30/06/1972', 'S09252C'],
        ['O15C', 'YOUSSEF', 'ZOURAKI', 'C', '663868378', '', 'A441336', '', '', '12/03/1992', 'S09171C'],
        ['O16C', 'AZOUZ', 'ENNABAL', 'C', '698853826', '', 'A566483', '', '', '04/01/1967', 'S09291C'],
        ['LIMA2C', 'AKRAM', 'ELHILALI', 'C', '662665394', '', 'A427172', '', '', '26/01/1976', 'S12073C'],
        ['LIMA4C', 'MAGHAT', 'RACHID', 'C', '', '', '', '', '', '', ''],
        ['L5C', 'FAKIHI', 'ABDERRAHIM', 'C', '666669789', '', 'VA14500', '', '', '01/01/1967', 'S09157C'],
        ['L6C', 'RACHID', 'NOUR', 'C', '667663389', '', 'A429777', '', '', '24/03/1977', 'S09422C'],
        ['L7C', 'NAZIR', 'MOHAMED', 'C', '771550419', '', 'AD185171', '', '', '24/02/1989', 'S11696C'],
        ['L8C', 'HASSAN', 'ASMOUH', 'C', '667075689', '', 'A294489', '', '', '26/05/1965', 'S09221C'],
        ['L9C', 'TARIK', 'MELOIANI', 'C', '602574027', '', '', '', '', '', ''],
        ['L10C', 'DRISS', 'BENGHANMI', 'C', '660201164', '', 'AB532578', '', '', '01/01/1986', 'S12131C'],
        ['L11C', 'LKWISSI', 'LARBI', 'C', '662382842', '', 'MC13001', '', '', '03/07/1980', 'S09233C'],
        ['L13C', 'ABDELLAH', 'TABTI', 'C', '663229985', '', 'AD56680', '', '', '01/01/1979', 'S09194C'],
        ['L14C', 'MNAM', 'ABDEMOUNIM', 'C', '664914374', '', 'A727413', '', '', '04/11/1977', 'S09203C'],
        ['L15C', 'TOUFIK', 'ALHAFID', 'C', '662888444', '', 'AB197016', '', '', '04/02/1975', 'S09260C'],
        ['L16C', 'AZIZ', 'ELALOUSSI', 'C', '661098728', '', 'Z428454', '', '', '', ''],
        ['L18C', 'SAKANI', 'ABDELAZIZ', 'C', '662509676', '', 'A203082', '', '', '22350', 'RETRAITE'],
        ['L 20C', 'KARIM', 'FARASSI', 'C', '635419761', '', '', '', '', '', ''],
        
        # GROUPE D (36 agents)
        ['CPD', 'YAGOUB', 'D', 'D', '660336995', '', 'A0408930', '', '', '17/05/1966', 'S09272C'],
        ['COND', 'ALAHYANE', 'D', 'D', '668191854', '', 'JB49050', '', '', '01/01/1966', 'S09280C'],
        ['MOTD', 'ALAMI', 'D', 'D', '666195501', '', 'UA9796', '', '', '24/06/1967', 'S09277C'],
        ['ZD', 'SNAIDA', 'AHMED', 'D', '666362689', '', 'XA24831', '', '', '27174', 'S09195C'],
        ['Z2D', 'BOUTSON', 'MUSTAPHA', 'D', '', '', 'A692457', '', '', '14/02/1980', 'S09290C'],
        ['Z5D', 'MAHDAD', 'AYOUB', 'D', '682153784', '', 'AD210108', '', '', '23/03/1990', 'S11995C'],
        ['z6D', 'ZEROUAL', 'ABDELHAQ', 'D', '605119496', '', 'I495670', '', '', '13/08/1979', 'S09205C'],
        ['Z7D', 'KASMOUTI', 'MOHAMED', 'D', '', '', '', '', '', '', ''],
        ['O1aD', 'BEN KHADRA', 'imad', 'D', '682153784', '', 'AB624802', '', '', '12/02/1987', 'S12674C'],
        ['O1bD', 'HADARBACH', 'KHLIFI', 'D', '670059528', '', 'UA95212', '', '', '22/04/1968', 'S09190C'],
        ['O3D', 'ABARKAN', 'YAHYA', 'D', '0650651681', '', 'A632213', '', '', '15/12/1976', 'S09261C'],
        ['NO4D', 'KABDANI', 'MOHAMED', 'D', '611658102', '', 'A427567', '', '', '28/03/1976', 'S09240C'],
        ['O5D', 'FERZOUI', 'KHALED', 'D', '676745704', '', '22647', '', '', '', 'RETRAITE'],
        ['O8D', 'EL KABOURI', 'Lahcen', 'D', '663754454', '', 'A0365454', '', '', '14/07/1979', 'S09230C'],
        ['O9D', 'HADDIR', 'HAKIM', 'D', '677522349', '', 'AD217181', '', '', '23/06/1990', 'S09158C'],
        ['O10D', 'LOURIGHI', 'ADIL', 'D', '652869687', '', 'A742130', '', '', '19/02/1994', 'S12133C'],
        ['O11D', 'HAJJI', 'TOUFIK', 'D', '660024350', '', 'A679901', '', '', '15/08/1983', 'S09258C'],
        ['O12D', 'TOUNSSI', 'HASSAN', 'D', '668928626', '', 'A194910', '', '', '22828', 'S09223C'],
        ['O13D', 'CHAMI', 'HASSAN', 'D', '622564794', '', '', '', '', '01/01/1966', 'S09215C'],
        ['O14D', 'OUGHIL', 'MUSTAPHA', 'D', '677651378', '', 'D523912', '', '', '12/02/1979', 'S09248C'],
        ['O15D', 'MACHHAB', 'Abderahim', 'D', '668272975', '', 'E505332', '', '', '03/07/1974', 'S09164C'],
        ['O16D', 'BOULDGAG', 'D', 'D', '670357654', '', 'D388632', '', '', '01/01/1968', 'S09191C'],
        ['LIMA 2D', 'HANSALI', 'MOLAY AHMED', 'D', '', '', '', '', 'I196324', '01/10/1967', 'S12671C'],
        ['LIMA 4D', 'ERRAISSY', 'ABDELJALIL', 'D', '', '', '', '', 'JC337475', '', 'S13885C'],
        ['L5D', 'EL AISSAOUI', 'MOHMED', 'D', '666904691', '', 'AB26585', '', '', '30/06/1962', 'S09238C'],
        ['L6D', 'SIYADI', 'MAJID', 'D', '664619176', '', 'BK11512', '', '', '06/08/1962', 'S09201C'],
        ['L7D', 'AIT BOURI', 'HASSAN', 'D', '641103141', '', 'A406039', '', '', '11/02/1966', 'S09219C'],
        ['L8D', 'BOUTOU', 'MOHAMED', 'D', '670181844', '', '22462', '', '', '', 'RETRAITE'],
        ['L9D', 'KARIM', 'MEROURI', 'D', '639284992', '', 'AB11225', '', '', '', 'S15251C'],
        ['L10D', 'DAHANI', 'MOHAMED', 'D', '608246402', '', 'A756477', '', '', '07/03/1974', 'S09237C'],
        ['L11D', 'LACHGAR', 'MOHAMED', 'D', '662721021', '', 'AB122686', '', '', '17/03/1968', 'S09189C'],
        ['L13D', 'EL HILALI', 'Hicham', 'D', '649835024', '', 'AD35116', '', '', '02/02/1973', 'S09224C'],
        ['L14D', 'ELHARBI', 'MOHAMED', 'D', '613535275', '', 'AB208044', '', '', '05/08/1978', 'S09245C'],
        ['L15D', 'DAHBI', 'Jalal', 'D', '672792404', '', 'A768009', '', '', '05/12/1976', 'S09226C'],
        ['L16D', 'JABAL', 'Rachid', 'D', '628612647', '', 'A786241', '', '', '01/08/1979', 'S09255C'],
        ['L18D', 'GUARMA', 'MOHAMED', 'D', '699082100', '', 'AD200164', '', '', '20/02/1987', 'S12074C'],
        ['L 20D', 'FOZARI', 'ABDLILAH', 'D', '690108567', '', 'ACCUEIL', '', '', '', ''],
    ]
    
    # Création du DataFrame avec toutes les colonnes
    data = {
        'Code_Agent': [agent[0] for agent in vos_agents],
        'Nom': [agent[1] for agent in vos_agents], 
        'Prenom': [agent[2] for agent in vos_agents],
        'Groupe': [agent[3] for agent in vos_agents],
        'Telephone': [agent[4] for agent in vos_agents],
        'Adresse': [agent[5] for agent in vos_agents],
        'Code_Panique': [agent[6] for agent in vos_agents],
        'Poste': [agent[7] for agent in vos_agents],
        'CIN': [agent[8] for agent in vos_agents],
        'Date_Naissance': [agent[9] for agent in vos_agents],
        'Matricule': [agent[10] for agent in vos_agents]
    }
    
    df = pd.DataFrame(data)
    
    try:
        df.to_excel('base données cleanco.xlsx', index=False)
        print("✅ Fichier Excel 'base données cleanco.xlsx' créé avec succès!")
        print("📊 STRUCTURE COMPLÈTE AVEC 11 COLONNES:")
        print("-" * 80)
        print("Colonnes créées: Code_Agent, Nom, Prénom, Groupe, Telephone, Adresse, Code_Panique, Poste, CIN, Date_Naissance, Matricule")
        print("-" * 80)
        
        # Afficher les statistiques par groupe
        groupes = {}
        for agent in vos_agents:
            groupe = agent[3]
            if groupe not in groupes:
                groupes[groupe] = []
            groupes[groupe].append(agent)
        
        print(f"\n📋 RÉPARTITION PAR GROUPE:")
        total_agents = 0
        for groupe in sorted(groupes.keys()):
            count = len(groupes[groupe])
            total_agents += count
            print(f"   • Groupe {groupe}: {count} agents")
        
        print("-" * 80)
        print(f"\n📍 TOTAL: {total_agents} agents avec données complètes")
        print("💡 Fichier prêt pour l'import dans le système SGA")
        
        # Aperçu des premières lignes
        print(f"\n👁️  APERÇU DES DONNÉES (5 premières lignes):")
        print(df.head().to_string(index=False))
        
        print(f"\n🎯 PROCHAINES ÉTAPES:")
        print("1. Lancer: python interface_console.py")
        print("2. Option 1 → Gestion des Agents")
        print("3. Option 3 → Importer depuis Excel")
        print("4. Nom du fichier: base données cleanco.xlsx")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création du fichier: {e}")

if __name__ == "__main__":
    creer_mon_fichier_excel()
