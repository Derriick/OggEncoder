#!/usr/bin/python3

import os
import subprocess
from os import getcwd, makedirs, listdir
from os.path import exists, isfile, isdir, splitext, abspath
from optparse import OptionParser
from sys import argv

DEFAULT_FILE_TYPES = ("flac", "wav")

# Génère les options de la commande
p = OptionParser()
p.add_option("-s", "--source", dest="source", default=".",
             help="Specify the input directory")
p.add_option("-d", "--destination", dest="destination", default=".",
             help="Specify the output directory")
p.add_option("-q", "--quality", dest="quality", default="3",
             help="Specify quality, between -1 (very low) and 10 (very high).\nFractional qualities (e.g. 2.75) are permitted.\nThe default quality level is 3.")
p.add_option("-e", "--extension", dest="extension", default="*",
        help="Speficy the extension of the files to process (default flac and wav)")
p.add_option("-c", "--copy", action="store_true", dest="copy", default=False,
             help="Copy the other files from source to destination")
options, args = p.parse_args()

# Encode tous les fichiers de "destination" récursivement,
# en gardant la même arborescence de fichiers
def encode(source, destination):
    files = [d for d in listdir(source) if not d.startswith(".")]

    # Vérifie si le dossier existe déjà, sinon le crée
    if not isdir(destination):
        # Vérifie qu'il n'existe pas un fichier du même nom
        if exists(destination):
            print ("File already exists: " + destination)
            return  # On quitte a fonction
        makedirs(destination)

    # Gère chaque fichier et dossier séparément
    for f in files:
        path = source + '/' + f

        # Vérfie le type de "f"
        if isdir(path):
            # Appelle la fonction "encode" récursivement
            encode(path, destination + '/' + f)
        elif isfile(path):
            name, ext = splitext(f)

            # Vérifie l'extension du fichier à encoder
            if ext[1:] in options.extension:
                # Génère et lance la commande shell
                cmd = ['oggenc', '-q' + options.quality , path, '-o', destination + '/' + name + '.ogg']
                subprocess.check_call(cmd, cwd=getcwd())
            elif options.copy:
                # Copie simplement le fichier
                cmd = ['cp', path, destination + '/' + f]
                subprocess.check_call(cmd, cwd=getcwd())
        else:
            print ("Error: " + path)

if options.extension == '*':
    options.extension = DEFAULT_FILE_TYPES

source = abspath(options.source)
destination = abspath(options.destination)

encode(source, destination)
