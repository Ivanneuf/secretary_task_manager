import os
import sys
from datetime import datetime
from script.md_generator import md_generator
from script.calendar_event import calendar_event
from simple_term_menu import TerminalMenu



class user_interface:
        
    def __init__(self):
        try:
            self.md_tools = md_generator()
        except Exception as e:
            print(f"{e}")
            sys.exit()
        try:
            self.isc_tools = calendar_event()
        except Exception as e:
            print(f"{e}")
            sys.exit()
        self.msg_aide = "Utiliser la touche tabulation ou espace pour sélectionner plusieurs éléments. Utiliser Enter pour sélectionner une commande ou valider l'ensemble des commandes sélectionnées"
        self.annee_actuelle = datetime.now().year
            
                
    def _gen_all_md(self):    
        self.md_tools.gen_md("convocation_ag")
        self.md_tools.gen_fp_md("faire_part")
        self.md_tools.gen_member_md("membres")
        self.md_tools.gen_md("pv_ag")
        
    def _menu_md(self):
        """
        Affiche le menu pour convertir les templates en markdowns remplis
        """
        option_md = ["Créer la convocation","Crée le fair part","Créer les membres","Crée le pv","Exit pour returner au menu précédent"]
        terminal_menu = TerminalMenu(option_md,
                                    title="Exporter un fichier en pdf",
                                    multi_select=True,
                                    show_multi_select_hint=True,
                                    show_multi_select_hint_text=self.msg_aide)
        while True:
            menu_entry_index = terminal_menu.show()
            for idx in menu_entry_index:
                match idx:
                    case 0:
                        self.md_tools.gen_md("convocation_ag")
                    case 1:
                        self.md_tools.gen_fp_md("faire_part")
                    case 2:
                        self.md_tools.gen_member_md("membres")
                    case 3:
                        self.md_tools.gen_md("pv_ag")
                    case 4:
                        return None
    
    def _menu_pdf(self):
        """
        Retourne un menu permettant l'exportation de un/tout le(s) fichiers md stocké dans le dossier de l'année actuel. Cet fonction
        ne vérifie pas si le fichier voulu existe.
        """     

        lst_available_pdf = []
        for file in  os.listdir(f"./{datetime.now().year}"):
            if file.endswith(".md"):
                lst_available_pdf.append(file[:-3])
                
                
        if len(lst_available_pdf) == 0:
            print("Vous n'avez pas de fichier md exportable, veuillez les crée d'abords.")
            return None
    
        option_pdf = []
        for file in lst_available_pdf:
            option_pdf.append(f"{file}")
                        
        option_pdf.append(f"Retourner au menu précèdent")
        terminal_menu = TerminalMenu(option_pdf,
                                     title="Exporter un fichier en pdf",
                                     multi_select=True,
                                     show_multi_select_hint=True,
                                     show_multi_select_hint_text=self.msg_aide)
        while True:
            menu_entry_index = terminal_menu.show()
            for select_opt in terminal_menu.chosen_menu_entries:
                if select_opt.startswith("Retourner"):
                    return None
                else:
                    self.md_tools.md_to_pdf(select_opt)
            
    def _menu_ics(self):
        """
        Affiche le menu pour convertir les csv en fichier ics pour exporter dans google calendar
        """
        option_ics = ["Séance de tir","Rappels/Événement","Retourner au menu précédent"]
                                
        terminal_menu = TerminalMenu(option_ics,
                                     title="Exporter les dates en ics",
                                     multi_select=True,
                                     show_multi_select_hint=True,
                                     show_multi_select_hint_text=self.msg_aide)
        while True:
            menu_entry_index = terminal_menu.show()
            for idx in menu_entry_index:
                match idx:
                    case 0:
                        self.isc_tools.export_to_calendar()
                    case 1:
                        self.isc_tools.export_reminder()
                    case 2:
                        return None
    def run(self):
        """
        lst_file is a list containing all the filename in the template folder
        This function let you start the interace, allowing the user to have the
        programm execute the task needed
        """
        
        option_main = ["Créer des MD/PDF","Exporter des dates","Tout exécuter","Exporter des pdfs","Quitter le programme"]
                                
        terminal_menu = TerminalMenu(option_main,
                                     title="Menu Principale")
                   
        while True:
            menu_entry_index = terminal_menu.show()
            match menu_entry_index:
                case 0:
                    self._menu_md()
                case 1:
                    self._menu_ics()
                case 2:
                    event_date = self.isc_tools.export_to_calendar()
                    self._gen_all_md()
                case 3:
                    self._menu_pdf()
                case 4:
                    print("Passez une bonne journée!")
                    return None
                
