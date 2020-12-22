import glob
import os

BUILD_DIR = "build"

def find_files(path):
    files = {}
    for file in glob.glob(path + "/**/*", recursive=True):
        if os.path.isfile(file):
            _, ext = os.path.splitext(file)
            if ext not in files:
                files[ext] = []
            files[ext].append(file)
    return files

os.makedirs(BUILD_DIR, exist_ok=True)

with open(BUILD_DIR+"/build.ninja", "w") as bf:
    with open("rule.ninja") as fr:
        bf.writelines(fr.readlines())
    bf.write("\n\n\n")

    files = find_files("LosTopos")
    objs = []
    for cpp in files[".cpp"]:
        obj = "{}.o".format(cpp)
        print("build {}: cpp $SRC/{}".format(obj, cpp), file=bf)
        objs.append(obj)
    bf.write("\n")
    libLosTopos = "LosTopos.a"
    print("build {}: link_library {}".format(libLosTopos, " ".join(objs)), file=bf)
    bf.write("\n\n\n")

    files = find_files("Apps/MultiTrackerSim")
    objs = []
    for cpp in files[".cpp"]:
        obj = "{}.o".format(cpp)
        print("build {}: cpp $SRC/{}".format(obj, cpp), file=bf)
        objs.append(obj)
    bf.write("\n")
    appMultiTrackerSim = "MultiTrackerSim"
    print("build {}: link_executable {}".format(appMultiTrackerSim, " ".join(objs + [libLosTopos])), file=bf)
    bf.write("\n\n\n")

    files = find_files("Apps/MultiTrackerViewer")
    objs = []
    for cpp in files[".cpp"]:
        obj = "{}.o".format(cpp)
        print("build {}: cpp $SRC/{}".format(obj, cpp), file=bf)
        objs.append(obj)
    bf.write("\n")
    appMultiTrackerViewer = "MultiTrackerViewer"
    print("build {}: link_executable {}".format(appMultiTrackerViewer, " ".join(objs + [libLosTopos])), file=bf)
    bf.write("\n\n\n")
    print("build all: phony {}".format(" ".join([libLosTopos, appMultiTrackerSim, appMultiTrackerViewer])), file=bf)

os.system("ninja -C " + BUILD_DIR)