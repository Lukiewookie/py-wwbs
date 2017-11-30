#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt

#Nacteni dat
data = pd.read_csv("outfile.csv")

data["dwnld"] = data["dwnld"].astype("category")
data["upld"] = data["upld"].astype("category")

#ax = data.plot.scatter(y="PROSPECH", x="HLUK",
                      # title="Prospech v porovnanim s prumernym hlukem u maturit")

#plt.plot(np.unique("HLUK"), np.poly1d(np.polyfit("HLUK", "PROSPECH", 1))(np.unique("HLUK")))
plt.show()