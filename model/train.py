import matplotlib.pyplot as plt
from keras.callbacks import EarlyStopping, ReduceLROnPlateau

from .cnn import cnn_model
from .preprocess import prepare_generator


def plot_history(history):
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs = range(1, len(acc) + 1)

    plt.plot(epochs, acc, label='Training accuracy')
    plt.plot(epochs, val_acc, label='Validation accuracy')
    plt.title('Training and validation accuracy')
    plt.legend()

    plt.figure()
    plt.plot(epochs, loss, label='Training loss')
    plt.plot(epochs, val_loss, label='Validation loss')
    plt.title('Training and validation loss')
    plt.legend()

    plt.show()


def train():
    model = cnn_model()

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    train_generator, validation_generator = prepare_generator()
    steps_per_epoch = train_generator.n // train_generator.batch_size
    validation_steps = validation_generator.n // validation_generator.batch_size

    early_stop = EarlyStopping(monitor='val_loss', patience=5, verbose=1)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=3, verbose=1)
    callbacks = [early_stop, reduce_lr]

    history = model.fit_generator(
        train_generator,
        steps_per_epoch=steps_per_epoch,
        epochs=100,
        callbacks=callbacks,
        validation_data=validation_generator,
        validation_steps=validation_steps
    )

    plot_history(history)


if __name__ == '__main__':
    train()
