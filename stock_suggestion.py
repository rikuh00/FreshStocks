from Asset import Asset

dic = {"Music" : [["Spotify", "SPOT"], ["Tencent Music", "TME"], ["Vivendi", "VIV"], ["Warner Music Group", "WMG"], ["QRS Music Technologies", "QRSM"]],
       "Fashion" : [["Pandoras", "PNDORA"], ["Gap", "GPS"], ["Nike", "NKE"], ["Guess", "GES"], ["Adidas", "ADDYY"]],
       "Entertainment" : [["The Walt Disney Company", "DIS"], ["Netflix", "NFLX"], ["Six Flags", "SIX"], ["21st Century Fox", "FOX"], ["Cineplex", "CGX.TO"]],
       "Sports" : [["Under Armour", "UA"], ["Puma", "PUM"], ["Dick's Sporting Goods", "DKS"], ["Dover Motorsports", "DVD"], ["Boyd Gaming", "BYD"]],
       "Technology" : [["Alphabet Inc", "GOOGL"], ["Tesla", "TSLA"], ["Amazon", "AMZN"], ["Apple", "AAPL"], ["Microsoft", "MSFT"]]
       }


for x in dic:
       print(x)
       for i in range(len(dic[x])):
              print(i)
              dic[x][i] = [Asset(dic[x][i][0], dic[x][i][1])]