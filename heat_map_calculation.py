from __future__ import annotations

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def get_grid(
    xmax: int | float,
    ymax: int | float,
    xstart: int | float,
    ystart: int | float,
    xpoints: int,
    ypoints: int,
) -> list[list[float|str]]:
    grid = []
    for y in np.linspace(ystart, ymax, ypoints):
        for x in np.linspace(xstart, xmax, xpoints):
            grid.append([round(x, 1), round(y, 1)])
    return grid


def create_heatmap(df: pd.DataFrame) -> None:
    preset = df["preset"][0]
    df.drop("preset", axis=1)
    to_plot = df.pivot(index="x", columns="y", values="temp")
    sns.set(rc={"figure.figsize": (6.5, 4)})
    sns.heatmap(to_plot, vmax=preset, cmap="coolwarm", square=True).invert_yaxis()
    text = table.temp.describe()
    text = text[["mean", "std"]]
    plt.text(6.5, 4, "".join(str(text)), fontsize=10)
    plt.tight_layout()
    plt.savefig("heat_map.png")
    plt.show()


if __name__ == "__main__":
    action = input("start a new heatmap [new] or display previous [prev] ")
    table: pd.DataFrame
    if action == "new":
        grid = get_grid(22, 22, 1.5, 1.5, 5, 5)
        temp_preset = input("enter the preset temperature in °C ")
        for point in grid:
            temp = input(f"note temperature for point {point} ")
            point.append([temp, temp_preset])

        table = pd.DataFrame(grid, columns=["x", "y", "temp", "preset"])
        table.to_csv("heat_map.csv")
    elif action == "prev":
        try:
            table = pd.read_csv("heat_map.csv", index_col=0)
        except FileNotFoundError:
            print("invalid option, no previous run found")
            raise
    print(table.temp.describe())
    create_heatmap(table)
