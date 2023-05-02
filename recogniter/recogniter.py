import cv2
import os
import environ
import numpy
from keras.applications import vgg16
from keras.models import Model
from keras import optimizers
from keras.layers import Input
from keras.layers.core import Flatten, Dense, Dropout
from keras import backend as K
from keras.layers import BatchNormalization

env = environ.Env()


class Recogniter():
    def __init__(self):
        print('Recogniter initializing')
        self.data_dir = env('DATA_FOLDER')
        self.labels = self.__get_labels()
        self.model = self.__get_model()
        print('Recogniter has initialized')

    def process_image(self, file_name):
        print(f'Image {file_name} processing')
        file_path = os.path.join(os.getcwd(), self.data_dir, file_name)
        image = self.__cut_sign(file_path)

        preprocessed = self.__prepare_image(image)

        predicted = self.model.predict(preprocessed)
        result = self.labels[predicted[0].argmax()]
        print(f'Sign has been detected: "{self.labels[predicted[0].argmax()].strip()}" with probability {max(predicted[0]) * 100}%')
        return result



    def __cut_sign(self, path):
        image = cv2.imread(path)

        x = image.shape[0] // 2 - 50
        y = image.shape[1] // 2 - 50
        h = 100

        image = image[x:x + h, y:y + h]

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(hsv, (5, 5), 0)
        thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY)[1]

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        clean = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

        contours = cv2.findContours(clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]

        result = image.copy()
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            result = result[y:y + h, x:x + w]


        return result

    def __get_labels(self):
        labels_path = 'assets/labels.txt'
        with open(os.path.join(os.getcwd(), 'recogniter', labels_path), "r") as f:
            labels = f.readlines()

        return labels

    def __get_model(self):
        weights = os.path.join(os.getcwd(), 'recogniter', 'assets', 'vgg16_deepstreet_training.h5')
        img_rows, img_cols = 224, 224

        if K.image_data_format() == 'channels_first':
            shape_ord = (3, img_rows, img_cols)
        else:  # channel_last
            shape_ord = (img_rows, img_cols, 3)

        vgg16_model = vgg16.VGG16(weights=None, include_top=False, input_tensor=Input(shape_ord))

        # add last fully-connected layers
        x = Flatten(input_shape=vgg16_model.output.shape)(vgg16_model.output)
        x = Dense(4096, activation='relu', name='ft_fc1')(x)
        x = Dropout(0.5)(x)
        x = BatchNormalization()(x)
        predictions = Dense(43, activation='softmax')(x)

        model = Model(inputs=vgg16_model.input, outputs=predictions)

        # compile the model
        model.compile(optimizer=optimizers.SGD(learning_rate=1e-4, momentum=0.9),
                      loss='categorical_crossentropy', metrics=['accuracy'])

        model.load_weights(weights)

        return model

    def __prepare_image(self, image):
        list = []

        res = cv2.resize(image, (224, 224)).astype(numpy.float32)
        res = res[:, :, ::-1]
        # Zero-center by mean pixel
        res -= numpy.mean(res)
        list.append(res)

        return numpy.array(list)
