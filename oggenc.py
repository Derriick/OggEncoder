#!/usr/bin/python3

import os
import sys
from os              import getcwd, makedirs, listdir
from os.path         import exists, isfile, isdir, splitext, abspath
from optparse        import OptionParser
from sys             import argv
from subprocess      import Popen, PIPE, STDOUT
from multiprocessing import Pool 

DEFAULT_FILE_TYPES = ("flac", "wav")
THREADS = 2
DEVNULL = open(os.devnull, 'wb')

# Génère les options de la commande
p = OptionParser()
p.add_option("-i", "--input", dest="inp", default=".",
			 help="Specify the source directory")
p.add_option("-o", "--output", dest="out", default=".",
			 help="Specify the destination directory")
p.add_option("-q", "--quality", dest="quality",
			 help="Specify quality, between -1 (very low) and 10 (very high).\nFractional qualities (e.g. 2.75) are permitted.\nThe default quality level is 3.")
p.add_option("-b", "--bitrate", dest="bitrate",
			 help="Specify bitrate value to use instead of quality")
p.add_option("-e", "--encoder", dest="encoder", default="ogg",
			 help="Specify the encoder to use for the conversion")
p.add_option("-s", "--source", dest="source", default="*",
			 help="Speficy the extension of the files to process (default flac and wav)")
p.add_option("-d", "--destination", dest="destination",
			 help="Speficy the extension of the destination files (default corresponds to chosen encoder)")
p.add_option("-c", "--copy", action="store_true", dest="copy", default=False,
			 help="Copy the other files from source to destination directory")
p.add_option("-f", "--force", action="store_true", dest="force", default=False,
			 help="Overwrite existing files")
p.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False,
			 help="Display encoder output on stdout")
p.add_option("-t", "--threads", dest="threads", default=THREADS,
			 help="Specify the number of threads")
options, args = p.parse_args()

def is_number(n):
	if n == None:
		return False
	try:
		float(n)
	except ValueError:
		return False
	return True

def get_encoder(encoder):
	if encoder == 1:
		return ["oggenc"]
	elif encoder == 2:
		return ["opusenc"]
	elif encoder == 3:
		return ["lame"]
	elif encoder == 4:
		return ["ffmpeg"]

def get_quality(encoder):
	if options.quality == None and options.bitrate == None:
		return []
	elif encoder == 1:
		if is_number(options.bitrate):
			return ["--bitrate", options.bitrate]
		elif options.bitrate == None and is_number(options.quality):
			return ["--quality", options.quality]
	elif encoder == 2:
		if options.quality != None or options.bitrate == None:
			print ("Quality cannot be specified with opusenc")
			sys.exit(2)
		elif is_number(options.bitrate):
			return ["--bitrate", options.bitrate]
	elif encoder == 3:
		if options.quality == None:
			if options.bitrate == None:
				print ("Specify quality or bitrate")
				sys.exit(2)
			elif is_number(options.bitrate):
				return ["-b", options.bitrate, "--cbr"]
		elif options.bitrate == None:
			if options.quality == "h":
				return ["-h"]
			elif options.quality == "f":
				return ["-f"]
			elif options.quality == "v":
				return ["-v"]
			elif options.quality == "medium":
				return ["--preset", "medium"]
			elif options.quality == "standard":
				return ["--preset", "standard"]
			elif options.quality == "extreme":
				return ["--preset", "extreme"]
			elif options.quality == "insane":
				return ["--preset", "insane"]
			elif is_number(options.quality):
				return ["-V", options.quality]
	elif encoder == 4:
		return []
	print ("Wrong quality or bitrate")
	sys.exit(2)

def get_extension(encoder):
	if options.destination == None:
		if encoder == 1:
			return ".ogg"
		elif encoder == 2:
			return ".opus"
		elif encoder == 3:
			return ".mp3"
		elif encoder == 4:
			return ".m4a"
	else:
		return '.' + options.destination

# Encode tous les fichiers de "out" récursivement,
# en gardant la même arborescence de fichiers
def get_args(inp, out, base_cmd, encoder, extension):
	files = [d for d in listdir(inp) if not d.startswith(".")]
	args = []
	
	# Vérifie si le dossier existe déjà, sinon le crée
	if not isdir(out):
		# Vérifie qu'il n'existe pas un fichier du même nom
		if exists(out):
			print ("File already exists: " + out)
			return  # On quitte a fonction
		makedirs(out)

	# Gère chaque fichier et dossier séparément
	for input_file in files:
		path = inp + '/' + input_file

		# Vérfie le type de input_file
		if isdir(path):
			# Appelle la fonction "get_args" récursivement
			args += get_args(path, out + '/' + input_file, base_cmd, encoder, extension)
		elif isfile(path):
			name, ext = splitext(input_file)
			output_file = out + '/' + name + extension

			if not exists(output_file) or options.force:
				# Vérifie l'extension du fichier à encoder
				if ext[1:] in options.source:
					# Génère et lance la commande shell
					if encoder == 1:
						args.append(base_cmd + [path, '-o', output_file])
					elif encoder == 2:
						args.append(base_cmd + [path, output_file])
					elif encoder == 3:
						args.append(base_cmd + [path, output_file])
					elif encoder == 4:
						args.append(base_cmd + ["-i", path, "-c:a", "alac", output_file])
				elif options.copy:
					# Copie simplement le fichier
					args.append(['cp', path, out + '/' + input_file])
			else:
				print (output_file + " already exists")
		else:
			print ("Error: " + path)
	return args

def encode(cmd):
	p = Popen(cmd, stdin=PIPE, stdout=out, stderr=STDOUT)
	p.wait()



if "ogg" in options.encoder or "vorbis" in options.encoder:
	encoder = 1
elif "opus" in options.encoder:
	encoder = 2
elif "lame" in options.encoder or "mp3" in options.encoder:
	encoder = 3
elif "m4a" in options.encoder or "alac" in options.encoder:
	encoder = 4
else:
	print (options.encoder + " is not a valid encoder")
	sys.exit(1)

if options.source == '*':
	options.source = DEFAULT_FILE_TYPES

base_cmd = get_encoder(encoder) + get_quality(encoder)
extension = get_extension(encoder)
source = abspath(options.inp)
destination = abspath(options.out)

if (options.verbose):
	out = None
else:
	out = DEVNULL

args = get_args(source, destination, base_cmd, encoder, extension)

pool = Pool(int(options.threads))
pool.map(encode, args)
