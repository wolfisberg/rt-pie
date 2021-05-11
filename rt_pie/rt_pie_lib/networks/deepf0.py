from tensorflow.keras.layers import Input, Reshape, Conv2D, BatchNormalization
from tensorflow.keras.layers import AveragePooling2D, Dropout, Permute, Flatten, Dense, Add, ReLU
from tensorflow.keras.models import Model


def __resblock(x, filters, kernel_size, dilation_rate, name):
    fx = Conv2D(filters, (kernel_size, 1), dilation_rate=(dilation_rate, 1), padding='same',
                activation='relu', name="dilation-conv%d" % name)(x)
    fx = BatchNormalization()(fx)
    fx = Conv2D(filters, 1, padding='same')(fx)
    out = Add()([x, fx])
    out = ReLU()(out)
    return out


def get_model_deepf0_without_time_compoonent(block_size):
    layers = 1
    filters = 128
    width = 512
    strides = (16, 1)
    dilation_rate = 8
    kernel_size = 64

    x = Input(shape=(block_size,), name='input', dtype='float32')
    y = Reshape(target_shape=(block_size, 1, 1), name='input-reshape')(x)

    y = Conv2D(filters, (width, 1), strides=strides, padding='same',
               activation='relu')(y)
    for i in range(4):
        y = __resblock(y, filters, kernel_size, dilation_rate, name=i)
    y = AveragePooling2D(pool_size=(2, 1), strides=None, padding='valid',
                         name="conv1d-avgpool")(y)
    y = Permute((2, 1, 3), name="transpose")(y)
    y = Flatten(name="flatten")(y)
    y = Dense(360, activation='sigmoid', name="classifier")(y)

    model = Model(inputs=x, outputs=y)
    model.compile('adam', 'binary_crossentropy', metrics=['mse', 'mae'])
    return model
