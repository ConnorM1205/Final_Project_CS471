import numpy as np
import pandas as pd
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    roc_auc_score,
    precision_score,
)


class MVPMetrics:
    def __init__(self, years=list(range(1991, 2021))) -> None:
        self.years = years

    def find_ap(self, combo: pd.DataFrame):
        actual = combo.sort_values("Share", ascending=False).head(5)
        predicted = combo.sort_values("predictions", ascending=False)
        ps = []
        found = 0
        seen = 1
        for i, r in predicted.iterrows():
            if r["Player"] in actual["Player"].values:
                found += 1
                ps.append(found / seen)
            seen += 1

        return sum(ps) / len(ps)

    def add_ranks(self, combo: pd.DataFrame) -> pd.DataFrame:
        combo = combo.sort_values("Share", ascending=False)
        combo["Rk"] = list(range(1, combo.shape[0] + 1))
        combo = combo.sort_values("predictions", ascending=False)
        combo["Predicted_Rk"] = list(range(1, combo.shape[0] + 1))
        combo["Diff"] = combo["Rk"] - combo["Predicted_Rk"]
        return combo

    def backtest(self, stats, model, year, predictors):
        aps = []
        all_preds = []
        for year in self.years[5:]:
            train = stats[stats["Year"] < year]
            test = stats[stats["Year"] == year]
            model.fit(train[predictors], train["Share"])
            preds = model.predict(test[predictors])
            preds = pd.DataFrame(preds, columns=["predictions"], index=test.index)
            combo = pd.concat([test[["Player", "Share"]], preds], axis=1)
            combo = self.add_ranks(combo)
            all_preds.append(combo)
            aps.append(self.find_ap(combo))
        return sum(aps) / len(aps), aps, pd.concat(all_preds)
