import pickle, copy

emptyDic = {"games":0, "wins":0, "losses":0, "ai":0, "notai":0, "diff":0, "col":0}
emptyStats = {"": emptyDic}

def readStats():
    global emptyStats
    try:
        stats = loadObj("stats")
    except:
        stats = emptyStats
        saveObj(stats, "stats")
    return stats

def saveObj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def loadObj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

def configStats(file=readStats(), name="", games=0, wins=0, losses=0, ai=0, notai=0, diff=0, col=0):
    global emptyDic
    stats = file
    defaultNames = ["", " ", "nom du joueur noir", "nom du joueur blanc", "nom du joueur"]
    if name in defaultNames: return
    default = copy.deepcopy(emptyDic)
    stats.get(name, default)["games"] += games
    stats.get(name, default)["wins"] += wins
    stats.get(name, default)["losses"] += losses
    stats.get(name, default)["ai"] += ai
    stats.get(name, default)["notai"] += notai
    stats.get(name, default)["diff"] += diff
    stats.get(name, default)["col"] += col
    stats[name] = stats.get(name, default)
    saveObj(stats, "stats")

stats = readStats()
