# coding:utf-8
import tensorflow as tf
import numpy as np
from PIL import Image
import os
import vgg2, vgg16
from ..settings import BASE_DIR


def read_img(path):
    img = Image.open(os.path.join(path))
    img = img.resize((224, 224), Image.ANTIALIAS)
    img_arr = np.array(img)

    # 构造数据空矩阵、标签空列表
    batch_arr = np.zeros((1, 224, 224, 3), dtype=np.uint8)
    label_arr = []

    batch_arr[0] = img_arr
    # 提取特征为第二通道，同时根据文件名，提取标签
    label_arr.append(0)
    return batch_arr, label_arr


def onehot(labels, i):
    n_sample = len(labels)
    onehot_labels = np.zeros((n_sample, i))
    onehot_labels[np.arange(n_sample), labels] = 1
    return onehot_labels


def secendory_detecct(image, label):
    tf.reset_default_graph()
    x_imgs = tf.placeholder(tf.float32, [None, 224, 224, 3], name='x-input')
    y_ = tf.placeholder(tf.float32, [None, 2], name='y-input')
    vgg = vgg2.vgg16(x_imgs)
    output = vgg.probs
    predict = tf.argmax(output, axis=1)
    l = tf.argmax(y_, axis=1)
    correct_pred = tf.equal(predict, l)
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
    apath = 'last/model/hard.ckpt'
    bpath = os.path.join(BASE_DIR, "data", apath)

    with tf.Session() as sess:
        saver = tf.train.Saver()
        saver.restore(sess, bpath)
        labels = onehot(label, 2)
        _, pre = sess.run([accuracy, predict], feed_dict={x_imgs: image, y_: labels})
        return pre



# path为图片完整地址，包括图片名
def primary_detect(path):
    x_imgs = tf.placeholder(tf.float32, [None, 224, 224, 3], name='x-input')
    y_ = tf.placeholder(tf.float32, [None, 3], name='y-input')

    vgg = vgg16.vgg16(x_imgs)
    output = vgg.probs

    predict = tf.argmax(output, axis=1)
    l = tf.argmax(y_, axis=1)
    correct_pred = tf.equal(predict, l)
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
    apath = 'san/model/san.ckpt'
    bpath = os.path.join(BASE_DIR, "data", apath)
    
    
    sess = tf.Session()
    saver = tf.train.Saver()
    saver.restore(sess, bpath)
    image, label = read_img(path)
    labels = onehot(label, 3)
    _, pre = sess.run([accuracy, predict], feed_dict={x_imgs: image, y_: labels})
    if pre == 2:
        sess.close()
        return secendory_detecct(image, label)
    else:
        return pre
    '''

    with tf.Session() as sess:
        saver = tf.train.Saver()
        saver.restore(sess, bpath)
        image, label = read_img(path)
        labels = onehot(label, 3)
        _, pre = sess.run([accuracy, predict], feed_dict={x_imgs: image, y_: labels})
        if pre == 2:
            return secendory_detecct(image, label)
        else:
            return pre
    
    '''


