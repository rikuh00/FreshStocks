from Asset import Asset

interest_stocks = {"Music" : [["Spotify", "SPOT", 2], ["Tencent Music", "TME", 1], ["Vivendi", "VIV", 2]],
       "Fashion" : [["Gold", "GOLD", 5], ["Gap", "GPS", 4], ["Nike", "NKE", 1]],
       "Entertainment" : [["The Walt Disney Company", "DIS", 1], ["Netflix", "NFLX", 0], ["Six Flags", "SIX", 3]],
       "Sports" : [["Under Armour", "UA", 2], ["Electronic Arts Inc", "EA", 4], ["Dick's Sporting Goods", "DKS", 1]],
       "Technology" : [["Alphabet Inc", "GOOGL", 2], ["Tesla", "TSLA", 3], ["Amazon", "AMZN", 0]]
                   }
def interest_function():
       for x in interest_stocks:
              print(x)
              for i in range(len(interest_stocks[x])):
                     print(interest_stocks[x][i])
                     interest_stocks[x][i] = Asset(interest_stocks[x][i][0], interest_stocks[x][i][1])