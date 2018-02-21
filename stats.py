import pickle

def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

def configStats(name="", games=0, wins=0, losses=0, ai=0, notai=0, diff=0, col=0):
    global stats
    default = dic = {"games":0, "wins":0, "losses":0, "ai":0, "notai":0, "diff":0, "col":0}
    dic = stats.get(name, default)
    dic["games"] += games
    dic["wins"] += wins
    dic["losses"] += losses
    dic["ai"] += ai
    dic["notai"] += notai
    dic["diff"] += diff
    dic["col"] += col
    stats[name] = dic
    save_obj(stats, "stats")

def readStats():
    global stats
    return stats

try:
    stats = load_obj("stats")
except:
    stats = {}
    save_obj(stats, "stats")