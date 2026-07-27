import os
import sys
from datetime import datetime
from ics import Calendar, Event, Todo
#Extract Data into array here
from pypdf import PdfReader
import re
import pandas as pd


class calendar_event:
     
    def __init__(self):
        self.annee_actuelle = datetime.now().year
        self.PATH_RES_FOLDER = sys.path[0] + "/" + str(self.annee_actuelle)

    def get_pdf_data(self,cur_page :list(),lst_date : list()):
        """
        Modifie la liste entrée en paramètre pour qu'elle inclus tout les champs correspondant
        à une séance de tir.
        :param cur_page list: Correspond à une liste contenant chaque ligne de texte d'une page du pdf
        :param lst_date list: Correspond à une liste stockant les champs contenant les séances de tir
        """
        pattern_row_data = re.compile("^(\d{2}.\d{2}.\d{4}).*")
        for entry in cur_page:
            if pattern_row_data.match(entry):
                lst_date.append(entry.split(" "))
            
    #Renvoi un ics avec des dates formater à UTC+2
    def export_to_calendar(self):
        """
        Créer un .ics, contenant les dates des séances de tirs. Ces dates
        peuvent être exportée dans google calendar. 12.03.2025 Il n'est actuellement
        pas possible d'importer des rappels ou d'utiliser des couleurs pour différencier
        les événements
        """

        entry_data = self.get_lst_date()
                
        #Create ISC
        delim = "-"
        c = Calendar()
        for entry in entry_data:
            e = Event()
            ymd = entry[0].split(".")
            ymd[0], ymd[2] = ymd[2], ymd[0]
            date_event = delim.join(ymd)
            e.name = "Évenement de type " + entry[4]
            e.begin = datetime.fromisoformat(date_event +"T" + entry[1] +":00+02:00")
            e.end = datetime.fromisoformat(date_event +"T" + entry[2] + ":00+02:00")
            c.events.add(e)
        c.events
        # [<Event 'My cool event' begin:2014-01-01 00:00:00 end:2014-01-01 00:00:01>]
        with open( self.PATH_RES_FOLDER +'/Date_Tir.ics', 'w') as my_file:
            my_file.writelines(c.serialize_iter())
        print("Les séances de tirs ont été exportées avec succès")

    def get_lst_date(self) -> []:
        """
        Retourne une liste contenant chaque date obtenus dans le pdf. Utilisé dans 
        la fonction export_to_calendar
        """
        try:
            reader = PdfReader(f'data/Annonce_des_jours_de_tirs_{self.annee_actuelle}.pdf')
        except Exception as e:
            print(f"ERREUR, le fichier n'est pas trouvable dans le dossier data, veuillez insèrer un pdf nommée Annonce_des_jours_de_tirs_{self.annee_actuelle}.pdf")
            print(f"{e}")
            sys.exit()
        date_lst = []
        
        #for each page, we extract the text and split into array before matching it
        for x in range(len(reader.pages)):
            page = reader.pages[x]
            raw_text = page.extract_text()
            split_txt = raw_text.splitlines()
            self.get_pdf_data(split_txt,date_lst)
        return date_lst

    def export_reminder(self):

        try:
            self.df = pd.read_csv('./data/event.csv',sep=";")
        except Exception as e:
            print("ERREUR, VOUS N'AVEZ PAS INCLUT UN FICHIER event.csv DANS LE DOSSIER DATA")
            print(f"{e}")
            sys.exit()
        #Create ISC
        c = Calendar()
        for index,entry in self.df.iterrows():
            e = Event()
            e.name = entry['Description']
            e.begin = datetime.fromisoformat(entry["DateDebut"] +"T" + entry["HeureDebut"] +":00+02:00")
            e.end = datetime.fromisoformat(entry["DateFin"] +"T" + entry["HeureFin"] + ":00+02:00")
            c.events.add(e)
        c.events
        # [<Event 'My cool event' begin:2014-01-01 00:00:00 end:2014-01-01 00:00:01>]
        with open( self.PATH_RES_FOLDER +'/Event.ics', 'w') as my_file:
            my_file.writelines(c.serialize_iter())
        print("Les événement ont été exportées avec succès")
        