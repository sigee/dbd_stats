import os
import tensorflow as tf

PERKS_IMAGE_SHAPE = (49, 49)
KILLERS_IMAGE_SHAPE = (40, 40)
ESCAPES_IMAGE_SHAPE = (60, 50)

EPOCHS = 100
BATCH_SIZE = 32


def build_model(num_classes, input_shape):
    local_model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(filters=8, kernel_size=(3, 3), activation='relu', input_shape=input_shape),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=2),
        tf.keras.layers.Conv2D(filters=16, kernel_size=(3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=2),
        tf.keras.layers.Conv2D(filters=32, kernel_size=(3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=2),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])
    return local_model


categories = ['perks', 'killers', 'escapes']
# categories = ['killers', 'escapes']
# categories = ['perks', 'escapes']
# categories = ['perks', 'killers']
# categories = ['perks']
# categories = ['killers']
# categories = ['escapes']
for category in categories:
    print('Creating model for: ' + category)
    if category == 'killers':
        IMAGE_SHAPE = KILLERS_IMAGE_SHAPE
    elif category == 'perks':
        IMAGE_SHAPE = PERKS_IMAGE_SHAPE
    elif category == 'escapes':
        IMAGE_SHAPE = ESCAPES_IMAGE_SHAPE
    else:
        IMAGE_SHAPE = (1, 1)

    TRAINING_DATA_DIR = 'input/dbd/' + category + '/training/'
    VALID_DATA_DIR = 'input/dbd/' + category + '/validation/'

    datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale=1. / 255
    )

    train_generator = datagen.flow_from_directory(
        TRAINING_DATA_DIR,
        shuffle=True,
        target_size=IMAGE_SHAPE,
    )

    class_names = [f.name for f in os.scandir(TRAINING_DATA_DIR) if f.is_dir()]

    valid_generator = datagen.flow_from_directory(
        VALID_DATA_DIR,
        shuffle=False,
        target_size=IMAGE_SHAPE,
    )

    tmp = list(IMAGE_SHAPE)
    tmp.append(3)

    model = build_model(len(class_names), tuple(tmp))
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
        loss=tf.keras.losses.CategoricalCrossentropy(from_logits=False),
        metrics=['accuracy']
    )
#     model.summary()

    history = model.fit(
        x=train_generator,
        batch_size=BATCH_SIZE,
        epochs=EPOCHS,
        verbose=1,
        validation_data=valid_generator,
        shuffle=True,
        steps_per_epoch=train_generator.samples // BATCH_SIZE,
        validation_steps=valid_generator.samples // BATCH_SIZE
    )

#     train_loss = history.history['loss']
#     train_acc = history.history['accuracy']
#     valid_loss = history.history['val_loss']
#     valid_acc = history.history['val_accuracy']

    model.save('../saved_model/dbd_' + category)
    with open(r'../saved_model/dbd_' + category + '/saved_labels.txt', 'w', encoding="utf-8") as fp:
        for item in class_names:
            fp.write("%s\n" % item)
