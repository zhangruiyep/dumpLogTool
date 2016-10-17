import os
import fnmatch
import ConfigParser
import extract

def findFile(filename):
	results = []
	for file in os.listdir("."):
		if fnmatch.fnmatch(file, filename):
			#print "found "+file
			results.append(file)
	return results

def findFilePath(filename, rootdir):
	result = []
	#print rootdir
	for root, subFolders, files in os.walk(rootdir):
		#print root, subFolders, files
		for f in files:  
			if fnmatch.fnmatch(f, filename):  
				result.append(os.path.join(root, f)) 
	return result 
	
def findPkg(filenames, rootdir):
	#print filenames, rootdir
	result = []
	for root, subFolders, files in os.walk(rootdir):
		#print root, subFolders, files
		for f in files:
			for filename in filenames:  
				if fnmatch.fnmatch(f, filename):  
					result.append(os.path.join(root, f)) 
	return result 

def extractFind(filename, rootdir):
	result = []
	files = findFilePath(filename, rootdir)
	#print filename, rootdir
	if len(files) == 1:
		#print "got path " + os.path.dirname(files[0])
		return os.path.dirname(files[0])

	elif len(files) == 0:
		print "%s not found" % filename
		
		print "maybe it is in archive..."
		cf = ConfigParser.ConfigParser()
		cf.read(os.path.join(os.path.split(os.path.realpath(__file__))[0],"cfg.ini"))
		toolName = cf.get("Tool", "Name")
		FileTypes = cf.get("Tool", "FileTypes")
		
		pkgTypes = FileTypes.split(';')
		# find archive and extract
		pkgs = findPkg(pkgTypes, rootdir)
		if len(pkgs) == 0:
			#print "pkgs not found"
			return None
		else:
			print pkgs
			for p in pkgs:
				arch = extract.archive(p, toolName)
				if arch.extractFile() == 0:
					pass
				else:
					print "ERR: %s format err" % p
					pass
			
			# pkg may be double archived, like .tar.gz
			pkgs2 = findPkg(pkgTypes, rootdir)
			for p in pkgs2:
				if p not in pkgs:
					arch = extract.archive(p, toolName)
					if arch.extractFile() == 0:
						pass
					else:
						print "ERR: %s format err" % p
						pass
			
			#print "checking again..."
			files = findFilePath(filename, rootdir)
			if len(files) == 0:
				#print "vmlinux not found again!"
				return None
			elif len(files) == 1:
				#print "got vmliux at " + os.path.dirname(files[0])
				return os.path.dirname(files[0])

	else:
		print "Find multi dump logs. Please change path to choose one."
		return None