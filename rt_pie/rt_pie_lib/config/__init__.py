import tensorflow as tf


PARSING_CONFIG_NOISE = {
    'data': tf.io.VarLenFeature(tf.string),
    'data_sampling_rate': tf.io.VarLenFeature(tf.int64),
    'data_num_channels': tf.io.VarLenFeature(tf.int64),
    'data_width': tf.io.VarLenFeature(tf.int64),
}

PARSING_CONFIG_SPEECH = {
    'data': tf.io.VarLenFeature(tf.string),
    'data_sampling_rate': tf.io.VarLenFeature(tf.int64),
    'data_num_channels': tf.io.VarLenFeature(tf.int64),
    'data_width': tf.io.VarLenFeature(tf.int64),
    'pitch': tf.io.VarLenFeature(tf.float32),
    'pitch_confidence': tf.io.VarLenFeature(tf.float32),
}
