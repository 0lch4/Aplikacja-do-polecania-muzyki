import json
import numpy as np
import tensorflow as tf

with open('wynik2.json') as f:
    data = json.load(f)

X = np.array([[data['tempo'], data['valence'], data['loudness'],
             data['energy'], data['time_signature']] for i in range(len(data))])
Y = X.copy()

min_vals = np.array([[data['tempo']-10, data['valence']-0.1, data['loudness']-1,
                    data['energy']-0.1, data['time_signature']] for i in range(len(data))])
max_vals = np.array([[data['tempo']+10, data['valence']+0.1, data['loudness']+1,
                    data['energy']+0.1, data['time_signature']] for i in range(len(data))])

a = 0
b = 1
min_vals += 0.001
max_vals -= 0.001
X_norm = ((X - min_vals) / (max_vals - min_vals)) * (b - a) + a

model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(256, activation='relu', input_shape=(5,)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(5, activation='linear')
])

model.compile(optimizer='adam', loss='mean_squared_error')

model.fit(X_norm, Y, epochs=120, batch_size=16)

model.save('podobienstwo_piosenek.h5')

results = []
for i in range(len(X)):
    prediction = model.predict(X_norm[i].reshape(1, 5))
    results.append(prediction.tolist()[0])


results_dict = {
    "tempo": round(np.mean([result[0] for result in results]), 3),
    "valence": round(np.mean([result[1] for result in results]), 3),
    "loudness": round(np.mean([result[2] for result in results]), 3),
    "energy": round(np.mean([result[3] for result in results]), 3),
    "time_signature": int(round(np.mean([result[4] for result in results]), 0))
}


with open('wynik3.json', 'w') as f:
    json.dump(results_dict, f)