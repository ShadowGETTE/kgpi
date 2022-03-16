from keras.preprocessing.image import ImageDataGenerator



train_dir = 'files/data/train'
val_dir = 'files/data/test'


def prepare_generator():
	train_datagen = ImageDataGenerator(
	    rescale=1./255,
	    rotation_range=10,
	    width_shift_range=0.1,
	    height_shift_range=0.1,
	    shear_range=0.1,
	    zoom_range=0.1,
	    horizontal_flip=True
	)
	val_datagen = ImageDataGenerator(rescale=1./255)

	train_generator = train_datagen.flow_from_directory(
	    train_dir,
	    target_size=(48,48),
	    batch_size=64,
	    color_mode="grayscale",
	    class_mode='categorical'
	)

	validation_generator = val_datagen.flow_from_directory(
	    val_dir,
	    target_size=(48,48),
	    batch_size=64,
	    color_mode="grayscale",
	    class_mode='categorical'
	)
	return (train_generator, validation_generator)
