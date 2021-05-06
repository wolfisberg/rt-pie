from tensorflow.keras.layers import Input, Reshape, Conv2D, BatchNormalization
from tensorflow.keras.layers import MaxPool2D, Dropout, Permute, Flatten, Dense
from tensorflow.keras.models import Model


def get_model_crepe_without_time_component(block_size):
    layers = [1, 2, 3, 4, 5, 6]
    filters = [n * 32 for n in [32, 4, 4, 4, 8, 16]]
    widths = [512, 64, 64, 64, 64, 64]
    strides = [(4, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1)]

    x = Input(shape=(block_size,), name='input', dtype='float32')
    y = Reshape(target_shape=(block_size, 1, 1), name='input-reshape')(x)

    for layer, filters, width, strides in zip(layers, filters, widths, strides):
        y = Conv2D(filters, (width, 1), strides=strides, padding='same',
                   activation='relu', name="conv%d" % layer)(y)
        y = BatchNormalization(name="conv%d-BN" % layer)(y)
        y = MaxPool2D(pool_size=(2, 1), strides=None, padding='valid',
                      name="conv%d-maxpool" % layer)(y)
        y = Dropout(0.25, name="conv%d-dropout" % layer)(y)

    y = Permute((2, 1, 3), name="transpose")(y)
    y = Flatten(name="flatten")(y)
    y = Dense(360, activation='sigmoid', name="classifier")(y)

    model = Model(inputs=x, outputs=y)
    model.compile('adam', 'binary_crossentropy', metrics=['mse', 'mae'])

    return model
