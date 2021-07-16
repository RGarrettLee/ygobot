from elosports.elo import Elo

eloLeague = Elo(k=20)

def newPlayerRating(player):
    eloLeague.addPlayer(player, rating = 1000)

def probability(p1, p2):
    return eloLeague.expectResult(eloLeague.ratingDict[p1], eloLeague.ratingDict[p2])

def eloUpdate(p1, p2):
    eloLeague.gameOver(winner = p1, loser = p2, winnerHome = 0)

    return ("{0}'s elo: {1}\n{2}'s elo: {3}".format(p1, eloLeague.ratingDict[p1], p2, eloLeague.ratingDict[p2]))

newPlayerRating('Sidewinder')
newPlayerRating('alex')

print(eloUpdate('Sidewinder', 'alex'))