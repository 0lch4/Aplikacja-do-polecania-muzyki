import json
import numpy as np
import tensorflow as tf
from pathlib import Path

PARAMETERS = (
    "tempo",
    "valence",
    "loudness",
    "energy",
    "time_signature",
    "danceability",
    "speechiness",
    "mode",
    "key",
    "instrumentalness",
    "popularity",
)


DIFFRENCE_LIMIT = (5, 0.1, 1, 0.1, 0, 0.1, 0.05, 0, 0, 0.01, 1)


# neural network return similar results and write it to the file
def neural() -> None:
    file_path = Path("app/data/results/old_results.json")
    with file_path.open(mode="r") as f:
        data = json.load(f)
    model = tf.keras.models.load_model("app/neural_network/neural_network.h5")
    # old song parameters
    x = np.array([[data[key] for key in PARAMETERS] for _ in range(len(data))])
    # expected data (similar so i copy x)
    y = x.copy()

    # min data values
    min_vals = np.array(
        [
            [data[key] - offset for key, offset in zip(PARAMETERS, DIFFRENCE_LIMIT)]
            for _ in range(len(data))
        ]
    )

    # max data values
    max_vals = np.array(
        [
            [data[key] + offset for key, offset in zip(PARAMETERS, DIFFRENCE_LIMIT)]
            for _ in range(len(data))
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
    for _ in range(len(x)):
        prediction = model.predict(x_norm[_].reshape(1, 11))
        results.append(prediction.tolist()[0])

    results_dict = {
        key: round(np.mean([r[i] for r in results]), None if i > 3 else 3)
        for i, key in enumerate(PARAMETERS)
    }

    file_path = Path("app/data/results/new_results.json")
    with file_path.open(mode="w") as f:
        json.dump(results_dict, f, indent=2, ensure_ascii=False)
