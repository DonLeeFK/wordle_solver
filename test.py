from solveWordle import selectNewCandidates
from solveWordle import generatePattern

#candidates = ['rider', 'riper', 'riser', 'river', 'rodeo', 'roger', 'rover', 'ruder', 'ruler']
candidates = ['blond', 'flood']
for word in candidates:
    pattern = generatePattern(word, 'blood')
    #print(word, pattern)
print(selectNewCandidates('blood', '🟩 🟩 🟩 🟥 🟩', candidates))