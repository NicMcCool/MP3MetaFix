######################################
#                                    #
#           MP3 META FIX             #
#  Assigning Album Artist and Artist #
#  metadata to MP3 files based off   #
#       their parent folder          #  
#                                    #
######################################
#                                    #
#    Directory format should be:     #
#       Top Directory (i.e. Music)   #
#         > Artist Folder            #
#            >  Music tracks         #
#                                    #
######################################

import eyed3, os

topDirectory = input("Enter the parent directory:")
logFile = open("errors.log", "w")

def editMeta(topFolder):
    for root, dirs, files in os.walk(topDirectory + "\\" + topFolder):
        if not files:
            continue
        for f in files:
            if f.lower().endswith(('.mp3')):
                fullFile = os.path.join(root,f)
                changeFile = eyed3.load(fullFile)
                print(fullFile)
                changeCheck = 1
                try:
                    try:
                        print("OLD = " + str(changeFile.tag.album_artist))
                    except AttributeError:
                        print("OLD = Blank Value")   

                    try:
                        if changeFile.tag.album_artist != topFolder:
                            print("Album Artist doesn't match")
                            changeFile.tag.album_artist = topFolder
                            changeCheck += 1
                        else:
                            print("Album Artist matches.")
                    except AttributeError:
                            print("Album Artist is NONE")
                            try:
                                changeFile.tag.album_artist = topFolder
                            except AttributeError:
                                "Couldn't change the Album Artist."
                            changeCheck += 1
                    try:
                        if changeFile.tag.artist != topFolder:
                            print("Artist doesn't match")
                            changeFile.tag.artist = topFolder
                            changeCheck += 1
                        else:
                            print("Artist matches.")
                    except AttributeError:
                            print("Artist is NONE")
                            try:
                                changeFile.tag.artist = topFolder
                            except AttributeError:
                                "Couldn't change the Artist."
                            changeCheck += 1

                    if changeCheck > 1:
                        changeFile.tag.save()
                        print("NEW AA = " + str(changeFile.tag.album_artist))
                        print("NEW A = " + str(changeFile.tag.artist))
                    else:
                        print("No changes needed for " + f)
                except Exception:
                    logFile.write(fullFile)
                    logFile.close

def subDirOne(root_dir):
    entries = os.listdir(root_dir)
    all_dirs = []

    for entry in entries:
        path = os.path.join(root_dir, entry)
        if os.path.isdir(path):
            all_dirs.append(entry)

    return all_dirs

output_dirs = subDirOne(topDirectory)
print(output_dirs)

for item in sorted(output_dirs):
    editMeta(item)