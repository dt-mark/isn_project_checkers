import pickle, copy

emptyDic = {"games":0, "wins":0, "losses":0, "ai":0, "notai":0, "diff":0, "col":0, "moves":0, "eats":0, "time":0}
emptyStats = {"": emptyDic}

emptyOptions = {"ai": 1, "humanPlayer": -1, "difficulty": 0, "gColours":0}

def readFile(filename, default):
    try:
        var = loadObj(filename)
    except:
        var = default
        saveObj(var, filename)
    return var

def saveObj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def loadObj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

def configStats(file=readFile("stats", emptyStats), name="", games=0, wins=0, losses=0, ai=0, notai=0, diff=0, col=0, moves=0, eats=0, time=0):
    global emptyDic
    stats = file
    defaultNames = ["", " ", "nom du joueur noir", "nom du joueur blanc", "nom du joueur"]
    if name in defaultNames: return
    default = copy.deepcopy(emptyDic)
    dic = stats.get(name, default)
    dic["games"] = dic.get("games", default["games"]) + games
    dic["wins"] = dic.get("wins", default["wins"]) + wins
    dic["losses"] = dic.get("losses", default["losses"]) + losses
    dic["ai"] = dic.get("ai", default["ai"]) + ai
    dic["notai"] = dic.get("notai", default["notai"]) + notai
    dic["diff"] = dic.get("diff", default["diff"]) + diff
    dic["col"] = dic.get("col", default["col"]) + col
    dic["moves"] = dic.get("moves", default["moves"]) + moves
    dic["eats"] = dic.get("eats", default["eats"]) + eats
    dic["time"] = dic.get("time", default["time"]) + time
    stats[name] = dic
    saveObj(stats, "stats")

stats = readFile("stats", emptyStats)
options = readFile("options", emptyOptions)
