# Outils de secrétaire
Ce programme a pour but de faciliter la création de divers documents pour la société, il faut cependant fournir quelques documents au préalable.
Ces documents doivent être placés dans le dossier template, ou data.

# Premier Lancement
- sudo locale-gen fr_FR.utf8 pour unbutu

# Entrée
- Insèrer les documents voulus sous format markdown dans le dossier template. Vous pouvez également ajouter des éléments HTML
dans ce markdown qui seront pris en compte lors de la création en PDF. La liste des variables constantes est située dans le fichier
valConst.csv situé dans le dossier Data. Veuillez respecter le format {{Variable}} pour que le programme remplisse automatiquement les champs

- Un fichier valConst.csv situé dans le dossier data. Vous pouvez modifier ce dossier pour ajouter des nouvelles variables ou changer
celles existants. Ce fichier peut être ouvert en Excel, veuillez cependant respecter le format imposé (Trois cellules). Certaines valeurs
ne sont pas affichées dans ce fichier car ils sont calculés automatiquement
- - ANNEE : L'année actuelle
- - NB_PRESENT : Le nombre de membres présents durant l'assemblée générale
- - ANNEE_PRECEDENT : L'année précédente
- - TRAINING / OPEN_DOORS / CAMPAIGN / ENDING_SHOOT Correspond aux dates de certains événements. Elles se remplissent automatiquement lors de la création du faire-part

- Un PDF contenant les dates des jours de tirs. Un PDF d'exemple existe dans le dossier data (qui doit contenir votre nouveau planning)
- Un fichier cSV contenant les informations pour les rappels. Merci de suivre le format de date (Année-Mois-Jour)

# Programming
Cette partie doit être complète pour contenir des éléments devant être modifiés depuis le code
- md_generator
- - Data_tableau est un tableau utilisé pour la fonction membres uniquement. Elle permet de définir les champs que votre tableau doit contenir

# Utilisation
python3 main.py <br>
Lorsque le programme démarre, vous aurez une liste de choix : Créer un/des mds à partir de templates et les exporter en PDF, Créer un fichier contenant les dates des séances de tirs, Effectuer les deux commandes précédentes ou encore exporter un/des markdowns en PDF. Cette dernière fonction est utilisée si vous avez modifié quelques lignes directement sur les markdowns situés dans le dossier de l'année.

# Sortie 
Le programme crée un dossier correspondant à l'année actuelle, avec ( en assumant que vous avez choisi l'option de tout exécuter), un fichier PDF et Markdown
par template, compléter par les valeurs contenues dans valConst. Vous aurez aussi un fichier.ics contenant les dates des séances de tir que vous pourrez
importer dans un calendrier comme Google Calendar

[Vous devriez normalement voir un exemple de convocation](img/pdf.png)