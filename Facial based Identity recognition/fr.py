# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 16:38:10 2018

@author: kzile
"""
import os
import sys
sys.path.insert(0, './src')
from revised_inference import run_inference
from revised_classifier import train
import revised_train_softmax
import facenet
import imageio
import numpy as np
import shutil
import string

def reframe():
    
    path_to_new_aligned_data = './collected_dataset'
    new_data_tmp = facenet.get_dataset(path_to_new_aligned_data)
    
    # Directory to access processed images
    put_into_classifier_data = './reframed_dataset'
    
    print('Number of new persons adding to classifier: ' + str(len(new_data_tmp)))
    
    for person in new_data_tmp:
        
        # Decalring name of person
        name = person.name
        
        # Declaring number of images for this person
        nrof_image = len(person.image_paths)
        
        print('Number of images for {a}: {b}'.format(a=name, b=nrof_image))
        
        # Change directory to see if there is an existing folder for this person
        os.chdir(put_into_classifier_data)
        if not os.path.exists(name):
            os.mkdir(name)
            
        # Return to base directory
        os.chdir('../')
        
        # preprocess image
        for n in range(nrof_image):
            # Get image file name
            filename = person.image_paths[n].replace(path_to_new_aligned_data, '')
            ## \\ in replace represents only a single \
            filename = filename.replace('\\' + name + '\\', '')
            shutil.copyfile(person.image_paths[n], put_into_classifier_data + '/' + name + '/' + filename)
        
def collected():
    
    # Load dataset
    path_to_new_data = './recorder'
    
    # Arrange dataset
    list_of_pictures = os.listdir(path_to_new_data)
    list_of_pictures = sorted(list_of_pictures)    
    
    for pic in list_of_pictures:
        print(type(pic[-3:]))
        if pic[-3:] == 'jpg':
            name = ''
            for letter in pic:
                if letter in string.digits:
                    break
                else:
                    name += letter
            os.chdir(path_to_new_data)
            if not os.path.exists(name):
                os.mkdir(name)
            os.chdir('../')
            shutil.copyfile(path_to_new_data + '/' + pic, path_to_new_data + '/' + name + '/' + pic)
        else:
            pass

            
    
    # Creating a temporary folder for mtcnn_aligned images
    os.system('python ' +  './src/align/align_dataset_mtcnn.py ' + path_to_new_data + ' ' + path_to_new_data + '_rev' + ' ' + '--image_size 182 --margin 44')
    aligned_data = './recorder_rev'
    new_data_tmp = facenet.get_dataset(aligned_data)
    
    # Directory to access processed images
    ready_to_use = './collected_dataset'
    
    print('Number of new persons adding to dataset: ' + str(len(new_data_tmp)))
    
    for person in new_data_tmp:
        
        # Decalring name of person
        name = person.name
        
        # Declaring number of images for this person
        nrof_image = len(person.image_paths)
        
        print('Number of images for {a}: {b}'.format(a=name, b=nrof_image))
        
        # Change directory to see if there is an existing folder for this person
        os.chdir(ready_to_use)
        if not os.path.exists(name):
            os.mkdir(name)
        os.chdir('../')
        
        # preprocess image
        for n in range(nrof_image):
            # Load image
            img = facenet.load_data([person.image_paths[n]], False, False, 160)
            
            # Reformat to remove 1st dimension (which is no. of image in this case always 1)
            img = np.squeeze(img, axis=0)
            
            # Get image file name
            filename = person.image_paths[n].replace(aligned_data, '')
            ## \\ in replace represents only a single \
            filename = filename.replace('\\' + name + '\\', '')
            
            # Change directory ready_dataset then save
            # Note! This will overwrite any image files with the same name
            os.chdir(ready_to_use + '/' + name)
            imageio.imsave(filename, img)
            os.chdir('../..')
    
    # Deletes temporary folder with mtcnn_aligned images    
    shutil.rmtree(aligned_data, ignore_errors=None, onerror=None)
            
        