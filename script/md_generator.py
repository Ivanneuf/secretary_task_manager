import os
import sys
from datetime import datetime
import pathlib
import time
#Extract Data into array here
from pypdf import PdfReader
import re
import pandas as pd
from markdown_pdf import MarkdownPdf,Section
from script.calendar_event import calendar_event
import locale
import calendar


class md_generator:
    def __init__(self):
        #Permet le retour de jour/mois en français, mettre en commentaire si on veut en anglais
        try:
            locale.setlocale(category=locale.LC_ALL,locale="fr_FR.utf8")
        except Exception as e:
            print(f"{e}\n Local n'a pas pu être set en français, les dates seront écris en anglais")
            #Pour windows, les utilisateurs de mac se démerderont
            locale.setlocale(category=locale.LC_ALL,locale="fr-CH")
            
        val_indisponible = "LA VALEUR EST MANQUANT DANS LES DATES DE TIRS"
        self.data_tableau = ["Role","Nom Prenom"]
        try:
            self.df = pd.read_csv('./data/valConst.csv',sep=";",index_col=0)
            self.nbMembre = len(self.df.loc["PRESENT_MEMBERS"]["Information"].split(','))
        except Exception as e:
            print("ERROR : Le fichier de données n'est pas au bon endroit ou son nom a été modifié. Cela ne devrait pas arriver si vous n'avez modifié que le contenue de valConst.csv avec excel ou à la main (mais dans ce cas la, je suis sur que le secrétaire ne verra pas sa)")
            print(f"{e}")
            sys.exit()
        self.annee_actuelle = datetime.now().year
        #Liste modifiable contenant des éléments qui seront automatiquement remplis.
        self.lstACalc = {"ANNEE" : str(self.annee_actuelle), "NB_PRESENT" : str(self.nbMembre), "ANNEE_PRECEDENT" : str(self.annee_actuelle-1),"TRAINING" : val_indisponible, "OPEN_DOORS" : val_indisponible, "CAMPAIGN":val_indisponible, "ENDING_SHOOT":val_indisponible}
        self.PATH_RES_FOLDER = sys.path[0] + "/" + str(self.annee_actuelle)
        pathlib.Path(self.PATH_RES_FOLDER).mkdir(exist_ok=True)


    def _get_lst_dynvar(self,pattern_needed : str,text_to_match: str):
        """
        Renvoie une list contenant tout les variables uniques nécessitant
        d'être completé
        """
        pattern_row_data = re.compile(pattern_needed)
        res = pattern_row_data.findall(text_to_match)
        return list(dict.fromkeys(res))
    
    def sanitize_word(self,word : str):
        """
        Retourne un string extrait d'un pdf correspondant à une var, en un string sans {{}}
        :param word str: Un string correspondant à cet structure {{VAR}}
        """
        #Remove '{{' and '}}' from the given word.
        return re.sub(r'{{(.*?)}}', r'\1', word)    
      
    def fill_md(self,f):
        """
        Remplis les trous dans le string du template. Les champs spécials (faire-parts/membres) sont traitée dans leurs fonctions dédiées.
        Renvoie un string contenant le string remplis, et une liste contenant les vars qui n'ont pas pu être trouvé et devant être fait depuis les fonctions (faire-part/membres)
        :param f openfile: Représente un fichier ouvert dans le dossier template
        """
        md_content = f.read() 
        lst_uni_var = self._get_lst_dynvar("\{[^}]*\}}",md_content)
        res_var = ""
        
        #entry_to_change correspond à {{Rôle}}
        for entry_to_change in lst_uni_var:
            cleaned_index = self.sanitize_word(entry_to_change)
            #cleaned_index correspond à Rôle
            if cleaned_index in self.lstACalc :
                md_content = md_content.replace(entry_to_change,self.lstACalc[cleaned_index])
            else :
                try:
                    md_content = md_content.replace(entry_to_change,self.df.loc[cleaned_index]["Information"])
                except:
                    res_var = entry_to_change
        return md_content,res_var
            
    def gen_md(self,filename : str):
        """ 
        Permet la création du markdown et du pdf du template avec les valeurs constante remplacé par celle attendu. 
        :param str filename: Le nom du fichier template (sans l'extension) à remplir et exporter en pdf
        """    
        
        try:
            f = open(f'template/{filename}.md', 'r') 
        except Exception as e:
            print(f"Erreur, vous n'avez pas mis le template {filename}.md dans le dossier template.")
            print(f"{e}")
            exit()
        md_content, empty = self.fill_md(f)
        self.save_md(filename,md_content)        
        
    def gen_member_md(self,filename:str):
        """
        Génère le md du template membres en un markdown complèter puis exporte en pdf
        :param filename str: Est égal à membres
        """
        
        try:
            f = open(f'template/{filename}.md', 'r') 
        except Exception as e:
            print(f"Erreur, vous avez supprimé/déplacé le template {filename}.md du dossier template.")
            print(f"{e}")
            exit()
        try:
            dm = pd.read_csv(f'./data/membres.csv',sep=";") 
        except Exception as e:
            print(f"Erreur, vous avez supprimé/déplacé le fichier membres.csv du dossier data.")
            print(f"{e}")
            exit()
        md_content,var_member = self.fill_md(f)
        #Remplacer par création du tableau html + par défaut Role | Nom Prénom
        array_html = "<table><tr>"
        for header in self.data_tableau:
            array_html += f"<th>{header}</th>"
        array_html += "</tr>"
        for idx in range(len(dm)):
            array_html += self.get_row_table(idx,dm)
        array_html += "</table>"
        md_content = md_content.replace(var_member,array_html)
        self.save_md(filename,md_content)
            
    def get_row_table(self,index:int,df_membre) -> str:
        """
        Retourne un string contenant le tableau en html pour les membres
        :param index int: Représente l'ID du membre voulu
        :param df_membre pandaDT: Représente le fichier .csv contenant les membres ouvert
        """
        row = "<tr>"
        #data_tableau contient les index en string (ex : Rôle). Chaque entrée représente une colonne, on peut combiner en incluant n élément dans une cellule en 
        #respectant la syntaxe Idx1 Idx2 (Nom Prénom)
        for val in self.data_tableau:
            if len(val.split(' ')) > 1:
                row += "<td>"
                for concat_val in val.split(' '):
                    row += df_membre.loc[index][concat_val] + " "     
                row += "</td>"
            else :
                row += "<td>" + df_membre.loc[index][val] + "</td>"
        return row + "</tr>"
                
            
    def gen_fp_md(self,filename:str):
        """
        Retourne un md complèter de faire_part, et l'exporte en pdf
        :param filename str: Égal à faire_part
        """
        isc_tools = calendar_event()
        lst_event = isc_tools.get_lst_date()
                    
        try:
            f = open(f'template/{filename}.md', 'r') 
        except Exception as e:
            print(f"Erreur, vous n'avez pas mis le template {filename}.md dans le dossier template.")
            print(f"{e}")
            exit()
            
        lst_OP = dict()
        
        for x in lst_event :
            match x[4]:
                case "Autres" :
                    if x[5] == "Tir":
                        self.lstACalc["ENDING_SHOOT"] = x[0]
                    else:
                        self.lstACalc["OPEN_DOORS"] = x[0]
                case "TR":
                    self.lstACalc["TRAINING"] = x[0]
                case "FS":
                    self.lstACalc["CAMPAIGN"] = x[0]
                case _:
                    jour_semaine = datetime.strptime(x[0], "%d.%m.%Y").strftime("%A")
                    elem_date = x[0].split('.')
                    mois = calendar.month_name[int(elem_date[1])]
                    lst_OP.setdefault(f"{jour_semaine} {x[1]}-{x[2]}",[]).append(f"{elem_date[0]} {mois}")
                    
                    
        md_content,entry_to_change = self.fill_md(f)
        md_content = md_content.replace(entry_to_change,self.fp_table(lst_OP))
        self.save_md(filename,md_content)
        
    def fp_table(self,lst_eventjour : dict):
        """
        Retourne un tableau en html contenant un en-tête avec le jour de la semaine + l'horaire
        de tir. Les lignes contiennent le jour/mois pour chaque séance.
        :param dict lst_eventjour: Contient nu dictionnaire avec comme index le jour de la semaine + horaire avec
        une liste contenant le jour/mois de la séance
        """
        
        res = "<table><tr>"
        for x in lst_eventjour:
            splt_time_day = x.split(' ')
            res += f"<th><p>{splt_time_day[0]}</p>{splt_time_day[1]}</th>"
        res += "</tr>"
        end_val = self.get_dict_longest(lst_eventjour)
        for x in range(end_val):
            res += "<tr>"
            for row in lst_eventjour:
                try:
                    res += f"<td>{lst_eventjour[row][x]}</td>"
                except:
                    res += "<td></td>"
            res += "</tr>"
        return res + "</table>"
    
    def save_md(self,filename:str,new_content:str):
        t = open(f'{self.PATH_RES_FOLDER}/{filename}_{self.annee_actuelle}.md', 'w') 
        t.write(new_content)
        t.close()
        print(f"Le fichier {filename}.md a été crée et importé en pdf avec succès")    
        self.md_to_pdf(f"{filename}_{self.annee_actuelle}")    
    
    def get_dict_longest(self,lst_evalute : dict) -> int:
        """
        Retourne la taille du jour avec le plus de séance de tir du dictionnaire. 
        :param lst_evalute dict: Un dictionnaire contenant pour chaque index un jour de la semaine avec sa liste d'événement
        """
        highest = 0
        cmpt = 0
        for days in lst_evalute:
            cmpt = 0    
            for event in days:
                cmpt += 1
            highest = cmpt if highest < cmpt else highest
        return highest
    
    def md_to_pdf(self,filename: str):
        """
        Permet d'exporter un markdown en pdf, le markdown peut contenir des éléments htmls qui seront pris
        en compte lors de la conversion.
        :param str filename: Le nom du fichier md qui doit être exporter
        """
        try:
            fMd = open(f'{self.PATH_RES_FOLDER}/{filename}.md', 'r')
        except Exception as e:
            print(f"ERROR, le fichier {filename} de l'année actuelle n'existe pas en md, assurez vous de crée le md auparavant")
            print(f"{e}")
            sys.exit()
        md_content = fMd.read()
        fMd.close()
        pdf = MarkdownPdf(toc_level=2)
        pdf.add_section(Section(md_content))
        pdf.save(f"{self.PATH_RES_FOLDER}/{filename}.pdf")
            