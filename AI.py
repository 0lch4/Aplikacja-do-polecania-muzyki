import json
import numpy as np
import tensorflow as tf
import time 

print("Im więcej będziesz mnie używać tym wyniki bedą lepsze :)")
time.sleep(0.5)
with open('wynik2.json') as f:
    data = json.load(f)

X = np.array([[data['tempo'], data['valence'], data['loudness'],
             data['energy'], data['time_signature'],data['danceability'],data['speechiness']] for i in range(len(data))])
Y = X.copy()

min_vals = np.array([[data['tempo']-5, data['valence']-0.1, data['loudness']-1,
                    data['energy']-0.1, data['time_signature'],data['danceability']-0.1,data['speechiness']-0.05] for i in range(len(data))])
max_vals = np.array([[data['tempo']+5, data['valence']+0.1, data['loudness']+1,
                    data['energy']+0.1, data['time_signature'],data['danceability']+0.1,data['speechiness']+0.05] for i in range(len(data))])

a = 0
b = 1
min_vals += 0.001
max_vals -= 0.001
X_norm = ((X - min_vals) / (max_vals - min_vals)) * (b - a) + a

model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(256, activation='relu', input_shape=(7,)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(7, activation='linear')
])

model.compile(optimizer='adam', loss='mean_squared_error')

model.fit(X_norm, Y, epochs=140, batch_size=16)

model.save('podobienstwo_piosenek.h5')

results = []
for i in range(len(X)):
    prediction = model.predict(X_norm[i].reshape(1, 7))
    results.append(prediction.tolist()[0])


results_dict = {
    "tempo": round(np.mean([result[0] for result in results]), 3),
    "valence": round(np.mean([result[1] for result in results]), 3),
    "loudness": round(np.mean([result[2] for result in results]), 3),
    "energy": round(np.mean([result[3] for result in results]), 3),
    "time_signature": int(round(np.mean([result[4] for result in results]), 0)),
    "danceability": int(round(np.mean([result[5] for result in results]), 0)),
    "speechiness": int(round(np.mean([result[6] for result in results]), 0)),
    "mode": data['mode'],
    "key": data['key']
}


with open('wynik3.json', 'w') as f:
    json.dump(results_dict, f)