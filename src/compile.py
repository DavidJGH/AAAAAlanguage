import glob
import json
import os
import shutil

publisher = "MutigenTiger"

langPath = '../language'
outPath = '../out'
includePath = '../include'

if not os.path.exists(outPath):
    os.makedirs(outPath)

existingFiles = glob.glob(outPath + '/unzipped/*')
for fileName in existingFiles:
    os.remove(fileName)

existingFiles = glob.glob(outPath + '/*.zip')
for fileName in existingFiles:
    os.remove(fileName)

if not os.path.exists(outPath+'/unzipped'):
    os.makedirs(outPath+'/unzipped')

languageFiles = glob.glob(langPath + '/*')

strings = {}

for filename in languageFiles:
    file = open(filename)
    data = json.load(file)
    strings.update(data['strings'])
    file.close()

result = {'strings': strings}

outputFile = open(outPath + '/unzipped/' + 'output.language', 'a')
outputFile.write(json.dumps(result))
outputFile.close()

includeFiles = glob.glob(includePath + '/*')

modname = ""
version = ""

for filename in includeFiles:
    if "manifest.json" in filename:
        manifestFile = open(filename)
        manifestData = json.load(manifestFile)
        modname = manifestData['name']
        version = manifestData['version_number']
        manifestFile.close()
    shutil.copy2(filename, outPath+'/unzipped')

shutil.make_archive(outPath+'/'+publisher+'-'+modname+'-'+version, 'zip', outPath+'/unzipped')

print('version ' + version + ' successfully compiled!')
