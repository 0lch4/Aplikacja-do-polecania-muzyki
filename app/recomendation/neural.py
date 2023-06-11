import json
import numpy as np
import tensorflow as tf
from pathlib import Path

#neural network return similar results and write it to the file
def neural() -> None:
    file_path = Path("app/data/results/old_results.json")
    with file_path.open(mode="r") as f:
        data = json.load(f)
    model = tf.keras.models.load_model("app/neural_network/neural_network.h5")
    x = np.array(
        [
            [
                data["tempo"],
                data["valence"],
                data["loudness"],
                data["energy"],
                data["time_signature"],
                data["danceability"],
                data["speechiness"],
                data["mode"],
                data["key"],
                data["instrumentalness"],
                data["popularity"],
            ]
            for i in range(len(data))
        ]
    )
    y = x.copy()

    min_vals = np.array(
        [
            [
                data["tempo"] - 5,
                data["valence"] - 0.1,
                data["loudness"] - 1,
                data["energy"] - 0.1,
                data["time_signature"],
                data["danceability"] - 0.1,
                data["speechiness"] - 0.05,
                data["mode"] - 0,
                data["key"] - 0,
                data["instrumentalness"] - 0.01,
                data["popularity"] - 1,
            ]
            for i in range(len(data))
        ]
    )
    max_vals = np.array(
        [
            [
                data["tempo"] + 5,
                data["valence"] + 0.1,
                data["loudness"] + 1,
                data["energy"] + 0.1,
                data["time_signature"],
                data["danceability"] + 0.1,
                data["speechiness"] + 0.05,
                data["mode"] + 0,
                data["key"] + 0,
                data["instrumentalness"] + 0.01,
                data["popularity"] + 1,
            ]
            for i in range(len(data))
        ]
    )

    a = 0
    b = 1
    min_vals += 0.001
    max_vals -= 0.001
    x_norm = ((x - min_vals) / (max_vals - min_vals)) * (b - a) + a
    model = tf.keras.models.Sequential(
        [
            tf.keras.layers.Dense(256, activation="relu", input_shape=(11,)),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dense(64, activation="relu"),
            tf.keras.layers.Dense(11, activation="linear"),
        ]
    )
    model.compile(optimizer="adam", loss="mean_squared_error")
    model.fit(x_norm, y, epochs=120, batch_size=16)

    # overwrites neural network, so if you use it often results will be better
    model.save("app/neural_network/neural_network.h5")
    results = []
    for i in range(len(x)):
        prediction = model.predict(x_norm[i].reshape(1, 11))
        results.append(prediction.tolist()[0])

    results_dict = {
        "tempo": round(np.mean([result[0] for result in results]), 3),
        "valence": round(np.mean([result[1] for result in results]), 3),
        "loudness": round(np.mean([result[2] for result in results]), 3),
        "energy": round(np.mean([result[3] for result in results]), 3),
        "time_signature": int(round(np.mean([result[4] for result in results]), 0)),
        "danceability": int(round(np.mean([result[5] for result in results]), 0)),
        "speechiness": int(round(np.mean([result[6] for result in results]), 0)),
        "mode": int(round(np.mean([result[7] for result in results]), 0)),
        "key": int(round(np.mean([result[8] for result in results]), 0)),
        "instrumentalness": int(round(np.mean([result[9] for result in results]), 0)),
        "popularity": int(round(np.mean([result[10] for result in results]), 0)),
    }
    file_path = Path("app/data/results/new_results.json")
    with file_path.open(mode="w") as f:
        json.dump(results_dict, f, indent=2, ensure_ascii=False)
