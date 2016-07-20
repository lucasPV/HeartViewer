##################################################################
#  _                     _ __     ___                            #
# | |__   ___  __ _ _ __| |\ \   / (_) _____      _____ _ __     #
# | '_ \ / _ \/ _` | '__| __\ \ / /| |/ _ \ \ /\ / / _ \ '__|    #
# | | | |  __/ (_| | |  | |_ \ V / | |  __/\ V  V /  __/ |       #
# |_| |_|\___|\__,_|_|   \__| \_/  |_|\___| \_/\_/ \___|_|       # 
#                                                                #
# @Author: Lucas Pascotti Valem                                  #
##################################################################

import os
import sys
import time
import shutil
import subprocess
import datetime
import webbrowser
import threading
import tkinter
import pyunpack
import zipfile, rarfile
import tkinter.ttk as ttk
from pyunpack import Archive
from tkinter import messagebox, filedialog
from natsort import realsorted


#Parameters
pageTitle            = 'Heart Viewer'
backgroundColor      = '#181818'
fontColor            = '#EFEFEF'
buttonFillColor      = '#C0C0C0'
buttonFontColor      = '#000000'
fontSize             = '3'
selectionDir         = '/media/Dados/Manga/' 	#default directory on gui file selection
appVersion           = 'v6.0'
copyright            = '2016 Heart Viewer'
use7z                = True					#if you don't want to use the python extraction libs, use 7z instead (make sure you have it installed)
smartSorting         = True					#sort considering the numbers in the names
showHeader           = True
useZoom              = True
zoomCursor           = True					#shows a magnifying glass when the cursor is above an image
useDefaultBrowser    = True					#if false, you can select the browser below
browser              = 'firefox'			#if you are not in Linux, make sure that the browser is in the system PATH
imgExtensions        = ('.png', '.jpg', '.jpeg', '.bmp', '.jpe', '.gif', '.tif')
compressedExtensions = ('.zip', '.rar', '.7z', '.tar', '.bz2', '.gz', '.tgz', '.cbz', '.cbt', '.cbr', '.cba', '.cb7')


#Application Directories
storeDataDir  = 'tmp'
extractionDir = os.path.join(storeDataDir, 'extractions') #tmp/extractions
indexPageName = 'index.html'
iconPath      = os.path.join('icon', 'icon.png')
heartPath     = os.path.join('icon', 'heart.png')
imagePath     = os.path.join('icon', 'image.png')
albumPath     = os.path.join('icon', 'albums.png')
glassPath     = os.path.join('icon', 'glass.png')
folderPath    = os.path.join('icon', 'folder.png')
cssPath       = os.path.join('utils', 'style.css')
jsPath        = os.path.join('utils', 'script.js')


def normalizePath(string): #This is necessary for Windows compatibility
	s1 = '\\'
	s2 = '/'
	return string.replace(s1, s2)


def getFiles(fileList, path):
	listTmp = mySorted(os.listdir(path))
	for file in listTmp:
	    if file.lower().endswith(imgExtensions):
	        fileList.append(file)


def fillHtmlHeader(output, name, imgs):
	name = "'" + name + "'"
	name = name.replace('\\', '\\\\') #for windows compatibility

	total = len(imgs)

	print('<html>', file=output)
	print('<meta charset="UTF-8">', file=output)
	print('<head>', file=output)
	print('<title>' + pageTitle + '</title>', file=output)
	print('<link rel="icon" href="file://' + os.path.join(realPath, iconPath) + '">', file=output)
	print('<link rel="stylesheet" type="text/css" href="file://' + os.path.join(realPath, cssPath) + '">', file=output)
	print('<script src="file://' + os.path.join(realPath, jsPath) + '"></script>', file=output)
	print('</head>', file=output)
	print('<body style="background-color:' + backgroundColor + ';">', file=output)
	print('<font size="' + fontSize + '" color="' + fontColor +'">', file=output)
	print('<b>\n', file=output)
	if showHeader:
		print('<div class="top_rect">', file=output)
		print('<div class="title_pos"><img align=center src="file://' + os.path.join(realPath, heartPath) + '">', file=output)
		print(pageTitle + ' ' + appVersion + '</div>' , file=output)
		print('<div class="filename_pos"><img align=center src="file://' + os.path.join(realPath, folderPath) + '">', file=output)
		print('<input type=button onClick="alert(' + name + ');" value="Info"></div>', file=output)
		print('<img align=center src="file://' + os.path.join(realPath, imagePath) + '">', file=output)
		print('<input type="text" name="enter" class="enter" value="" onkeypress="jumpToImg(event,' + str(total) + ')" id="ref" style="width:58px;height:30px"/>', file=output)
		print('/' + str(total), file=output)
		print('<body onload="startTime()">', file=output)
		print('<div class="clock_pos" id="txt"></div>', file=output)
		print('<div class="zoom_pos"> <img align=center src="file://' + os.path.join(realPath, glassPath) + '">', file=output)
		print("<input type=button onClick='decImgsSize();' value='-'>", file=output)
		print("<input type=button onClick='incImgsSize();' value='+'></div>", file=output)
		if compressedFiles:
			pathToAlbum = os.path.join(tmpDir, indexPageName)
			pathToAlbum = normalizePath(pathToAlbum)
			print('<div class="album_pos"> <img align=center src="file://' + os.path.join(realPath, albumPath) + '">', file=output)
			print("<input type=button onClick=""location.href='file://" + pathToAlbum + "'"" value='Albums'></div>", file=output)
		print('</div>', file=output)


def fillHtmlImgs(output, imgs, path):
	total = len(imgs)
	i = 1
	print('<a name="top"></a>', file=output)
	print('<div class="manga" id="manga" align="center">', file=output)
	for file in imgs:
		print('<a name="' + str(i) + '"></a>', file=output)
		if not compressedFiles:
			print('<a name="'+ file + '"></a>', file=output)
		if showHeader and i == 1:
			print('<br/><br/>', file=output)
		print('\t<img id="img' + str(i) + '" src="file://' + path + '/' + file + '">', file=output)
		print('\t<p>[' + str(i) + '/' + str(total) + ']</p>', file=output)
		print('<br/>', file=output)
		i += 1
	print('</div>',  file=output)


def addZoomFeature(output, imgs):
	#Zoom cursor icon for each image
	if zoomCursor:
		i = 1
		print('\n<style>', file=output)
		for file in imgs:
			print('#img' + str(i) + '{ cursor:zoom-in; }', file=output)
			i += 1
		print('</style>\n', file=output)

	#Add a listener to each image
	print('\n<script>', file=output)
	i = 1
	for file in imgs:
		print("\ndocument.getElementById('img" + str(i) + "').addEventListener('click', function() {", file=output)
		print('\ttoggleFullscreen(this);', file=output)
		print('});', file=output)
		i += 1
	print('</script>\n', file=output)


def addAlbumButtons(output, prv, nxt):
	print('<center><form>', file=output)
	if prv:
		prv = normalizePath(prv)
		prv = "'file://" + prv + "'"
		print('<input style="width: 180px; padding: 10px; box-shaddow: 6px 6px 5px; #999999; -webkit-box-shadow: 6px 6px 5px #999999; -moz-box-shadow: 6px 6px 5px #999999; font-weight: bold; background: ' + buttonFillColor + '; color: ' + buttonFontColor + '; cursor: pointer; border-radius: 10px; border: 1px solid #D9D9D9; font-size: 100%;" type="button" value="Prev Album" onclick="href=window.location.href=' + prv + '" />', file=output)
	if nxt:
		nxt = normalizePath(nxt)
		nxt = "'file://" + nxt + "'"
		print('<input style="width: 180px; padding: 10px; box-shaddow: 6px 6px 5px; #999999; -webkit-box-shadow: 6px 6px 5px #999999; -moz-box-shadow: 6px 6px 5px #999999; font-weight: bold; background: ' + buttonFillColor + '; color: ' + buttonFontColor + '; cursor: pointer; border-radius: 10px; border: 1px solid #D9D9D9; font-size: 100%;" type="button" value="Next Album" onclick="href=window.location.href=' + nxt + '" />', file=output)
	print('</form></center>', file=output)


def fillHtmlFileEnd(output):
	print('<script>adjustImgs();</script>', file=output)
	print('<center><form>', file=output)
	print('<input style="width: 180px; padding: 10px; box-shaddow: 6px 6px 5px; #999999; -webkit-box-shadow: 6px 6px 5px #999999; -moz-box-shadow: 6px 6px 5px #999999; font-weight: bold; background: ' + buttonFillColor + '; color: ' + buttonFontColor + '; cursor: pointer; border-radius: 10px; border: 1px solid #D9D9D9; font-size: 100%;" type="button" value="Back to the top" onclick="window.location.href=' + "'#top'" + '" />', file=output)
	print('<small><aside><br/><br/>&copy;' + copyright + ' ' + appVersion + '</aside></small>', file=output)
	print('<a name="bottom"></a>', file=output)
	print('</form></center>', file=output)
	print('\n</b>',  file=output)
	print('</font>', file=output)
	print('</body>', file=output)
	print('</html>', file=output)


def unzipImgs(filename, path):
	with zipfile.ZipFile(filename, 'r') as zf:
		for file in zf.namelist():
			if file.lower().endswith(imgExtensions):
				zf.extract(file, path)

def unrarImgs(filename, path):
	with rarfile.RarFile(filename, 'r') as rf:
		for file in rf.namelist():
			if file.lower().endswith(imgExtensions):
				rf.extract(file, path)

def extractFile(filename, path):
	Archive(filename).extractall(path)


def extractFiles(window, fileDict, progressBar):
	step = 99.99/len(fileDict)
	for filename in mySorted(fileDict):
		path = fileDict[filename]
		fullPath = os.path.join(path, filename)
		pathToExtract = os.path.join(dirToExtract, os.path.splitext(filename)[0])
		fileDict[filename] = (path, pathToExtract)
		try:
			os.makedirs(pathToExtract)
			if use7z:
				os.system('7z x "' + fullPath + '" -o"' + pathToExtract + '"')
			else:
				if filename.lower().endswith(('.zip', '.rar')):
					try:
						if filename.lower().endswith('.zip'):
							unzipImgs(fullPath, pathToExtract)
						elif filename.lower().endswith('.rar'):
							unrarImgs(fullPath, pathToExtract)
					except:
						shutil.rmtree(pathToExtract)
						os.makedirs(pathToExtract)
						extractFile(fullPath, pathToExtract)
				else:
					extractFile(fullPath, pathToExtract)
		except:
			messagebox.showinfo("Error", "Couldn't extract file:\n" + fullPath)
			window.quit()
			os._exit(1)
		progressBar.step(step)
	window.quit()


if __name__ == "__main__":
	#Hide tkinter background window
	window = tkinter.Tk()
	window.withdraw()

	#Get the files
	fileList = []
	nArgs = len(sys.argv)
	if (nArgs == 1) or (sys.argv[1] == ""):
		fileList = filedialog.askopenfilename(multiple=True, initialdir=selectionDir)
		if not fileList:
			exit(1)
	else:
		for x in range(1, nArgs):
			fileList.append(os.path.abspath(sys.argv[x]))

	#Select the desired sorting method
	if smartSorting:
		mySorted = realsorted
	else:
		mySorted = sorted

	#Make a dictionary store the filename as key and the path as value
	fileDict = {}
	for file in fileList:
		path, filename = os.path.split(file)
		fileDict[filename] = path

	#Check if the given paths are valid
	for filename, path in fileDict.items():
		fullPath = os.path.join(path, filename)
		if not os.path.isfile(fullPath):
			if not os.path.isdir(fullPath):
				messagebox.showinfo("Error", "Invalid path:\n" + fullPath)
			else:
				messagebox.showinfo("Error", "This is a directory:\n" + fullPath + "\nYou need to select files!")
			exit(1)

	#Check if the extensions are valid
	compressedFiles = True
	if len(fileDict) == 1:
		for filename in fileDict:
			if not (filename.lower().endswith(compressedExtensions + imgExtensions)):
				messagebox.showinfo("Error", "This file is not an image or compressed file!")
				exit(1)
			if filename.lower().endswith(imgExtensions):
				compressedFiles = False
	else:
		for filename in fileDict:
			if not filename.lower().endswith(compressedExtensions):
				messagebox.showinfo("Error", "Multiple selection supports only compressed files!")
				exit(1)

	#Get the path of the script on this machine
	realPath = os.path.dirname(os.path.realpath(__file__))

	#Create folder to store html pages (if it doesn't exist yet)
	tmpDir = os.path.join(realPath, storeDataDir)
	if os.path.exists(tmpDir):
		shutil.rmtree(tmpDir)
	os.makedirs(tmpDir)

	#Create folder to extract compressed files (if it doesn't exist yet)
	dirToExtract = os.path.join(realPath, extractionDir)
	if os.path.exists(dirToExtract):
		shutil.rmtree(dirToExtract)
	os.makedirs(dirToExtract)

	if compressedFiles:
		#Get absolute directory to extract files
		dirToExtract = os.path.abspath(dirToExtract)

		#Extract files
		window.deiconify()
		window.wm_title("Opening Files")
		frame = ttk.Frame()
		frame.pack(expand=False, fill=tkinter.BOTH, side=tkinter.TOP)
		progressBar = ttk.Progressbar(frame, orient='horizontal', length=300, mode='determinate')
		progressBar.pack(expand=False, fill=tkinter.BOTH, side=tkinter.TOP)
		thread = threading.Thread(target=extractFiles, args=(window, fileDict,progressBar, ))
		thread.start()
		window.mainloop()
		thread.join()

		#Generate the index page header
		indexPage = open(os.path.join(tmpDir, indexPageName), 'w+')
		print('<!DOCTYPE html>', file=indexPage)
		print('<meta charset="UTF-8">', file=indexPage)
		print("<html>", file=indexPage)
		print("<body>", file=indexPage)
		print('<head>', file=indexPage)
		print('<title>' + pageTitle + '</title>', file=indexPage)
		print('<link rel="icon" href="file://' + os.path.join(realPath, iconPath)  + '">', file=indexPage)
		print('</head>', file=indexPage)
		print('<center><b><u><p> Generated albums: </p></u></b><br/>', file=indexPage)

		#Fill a list of directories with images and path of the albums for each selected file
		imgDirList = []
		albumList = []
		for filename, (path, pathToExtract) in mySorted(fileDict.items()):
			#Get all subdirectories relative to the first one
			searchDirs = [pathToExtract]
			for root, directories, filenames in os.walk(pathToExtract):
				if directories:
					for directory in directories:
						searchDirs.append(os.path.join(root, directory))

			#Get the directories that contain images
			imgDirs = []
			for directory in searchDirs:
				if "__MACOSX" in directory:
					continue
				for file in os.listdir(directory):
					if file.lower().endswith(imgExtensions):
						imgDirs.append(directory)
						break

			imgDirList.append(imgDirs)

			#Generate the albums name (paths)
			albums = []
			for directory in mySorted(imgDirs):
				rest, name = os.path.split(directory)
				albumName = os.path.join(os.path.join(pathToExtract, directory), name) + ".html"
				albums.append(albumName)

			albumList.append(albums)

		#Generate albums for each file
		x = 0
		for filename, (path, pathToExtract) in mySorted(fileDict.items()):
			imgDirs = imgDirList[x]
			albums = albumList[x]

			print('<b>' + filename + '</b>', file=indexPage)

			#Generate the albums for the file
			i = 0
			for directory in mySorted(imgDirs):
				#Generate the html file
				pageFile = open(albums[i], 'w+')
				imgs = []
				getFiles(imgs, directory)
				fillHtmlHeader(pageFile, os.path.splitext(albums[i])[0], imgs)
				fillHtmlImgs(pageFile, imgs, directory)
				if useZoom:
					addZoomFeature(pageFile, imgs)

				#Get the previous album link (if there's one)
				if i == 0:
					if (x-1 >= 0):
						prv = albumList[x-1][len(albumList[x-1])-1]
					else:
						prv = ""
				else:
					prv = albums[i-1]
				#Get the next album link (if there's one)
				if i+1 == len(albums):
					try:
						nxt = albumList[x+1][0]
					except:
						nxt = ""
				else:
					nxt = albums[i+1]
				#Add previous/next album buttons
				addAlbumButtons(pageFile, prv, nxt)

				fillHtmlFileEnd(pageFile)
				pageFile.close()

				#Add album page to index
				print('<b><p><a href="file://' + albums[i] + '">' + os.path.relpath(directory, dirToExtract) + ' </a></p></b>', file=indexPage)

				i += 1
			x += 1

		#End the index page
		print('<small><aside><br/><br/>&copy' + copyright + ' ' + appVersion + '</aside></small></center>', file=indexPage)
		print("</body>", file=indexPage)
		print("</html>", file=indexPage)
		indexPage.close()

		#Get the url
		url = "file://" + os.path.join(tmpDir, indexPageName)

	else:
		#Get filename, directory and name of the html to generate
		for name in fileDict:
			filename = name
			directory = fileDict[name]
			pageName = os.path.splitext(filename)[0] + ".html"

		#Generate the html file
		indexPage = open(os.path.join(tmpDir, pageName), 'w+')
		imgs = []
		getFiles(imgs, directory)
		fillHtmlHeader(indexPage, os.path.join(fileDict[name], name), imgs)
		fillHtmlImgs(indexPage, imgs, directory)
		if useZoom:
			addZoomFeature(indexPage, imgs)
		fillHtmlFileEnd(indexPage)
		indexPage.close()

		#Get the url
		url = "file://" + os.path.join(tmpDir, pageName) + "#" + filename

	#Open the html file in the browser
	if useDefaultBrowser:
		webbrowser.open(url)
	else:
		subprocess.Popen([browser, url])
		#subprocess.Popen([browser, "-P", "heartViewer", url])
