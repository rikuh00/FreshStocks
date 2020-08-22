from Asset import Asset

dic = {"Music" : [["Spotify", "SPOT"], ["Tencent Music", "TME"], ["Vivendi", "VIV"]],
       "Fashion" : [["Gold", "GOLD"], ["Gap", "GPS"], ["Nike", "NKE"]],
       "Entertainment" : [["The Walt Disney Company", "DIS"], ["Netflix", "NFLX"], ["Six Flags", "SIX"]],
       "Sports" : [["Under Armour", "UA"], ["Electronic Arts Inc", "EA"], ["Dick's Sporting Goods", "DKS"]],
       "Technology" : [["Alphabet Inc", "GOOGL"], ["Tesla", "TSLA"], ["Amazon", "AMZN"]]
       }
if __name__ == '__main__':
       for x in dic:
              print(x)
              for i in range(len(dic[x])):
                     print(dic[x][i])
                     dic[x][i] = Asset(dic[x][i][0], dic[x][i][1])