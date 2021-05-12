import tensorflow as tf


def get_model_lstm(block_size):
    frame_step = block_size // 2
    sample_length = 3
    sample_rate = 16000
    num_frames = 1 + (sample_rate * sample_length - block_size) // frame_step

    output_dimension = 256
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.LSTM(output_dimension, return_sequences=True, input_shape=(num_frames, block_size)))
    model.add(tf.keras.layers.LSTM(output_dimension, return_sequences=True))
    model.add(tf.keras.layers.Dense(128, activation='relu'))
    model.add(tf.keras.layers.Dense(1, activation='relu'))
    model.compile(loss='mse', optimizer='adam', metrics=['mse'])
    return model
