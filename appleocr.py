from ocrmac import ocrmac
import os
#from PIL import Image
import PIL.Image
from PIL.ExifTags import TAGS
from pprint import pprint

from os import listdir
import numpy as np
import datetime
from csv import writer
from pathlib import Path
import datetime
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage import data
from skimage import transform
from skimage import io

import sys


def sort_by_X(annotations):
    array_x = []
    for i in range(len(annotations)):
        array_x.insert(i, annotations[i][2][0])
    
    #print(array_x)

    for i in range(len(annotations)):
        #print("start")

        #print(annotations[i:])
        #print(annotations[i][1][0])
        swap = i + np.argmin(array_x[i:])
        #print(i + np.argmin(annotations[i:]))
        #print("swap ",swap)
        (array_x[i], array_x[swap]) = (array_x[swap], array_x[i])
        (annotations[i], annotations[swap]) = (annotations[swap], annotations[i])
        #print("array_x ",array_x)
        #print("result ",annotations)
    return annotations

def sort_by_Y(annotations):
    array_y = []
    for i in range(len(annotations)):
        array_y.insert(i, annotations[i][2][1])
    
    #print(array_y)

    for i in range(len(annotations)):
        #print("start")

        #print(annotations[i:])
        #print(annotations[i][1][0])
        swap = i + np.argmin(array_y[i:])
        #print(i + np.argmin(annotations[i:]))
        #print("swap ",swap)
        (array_y[i], array_y[swap]) = (array_y[swap], array_y[i])
        (annotations[i], annotations[swap]) = (annotations[swap], annotations[i])
        #print("array_x ",array_x)
    return annotations

def find_line_y_for_text(text,annotations):    
    for i in range(len(annotations)):
        textinline = annotations[i][0]
        #print(linenum)
        #print()
        if text == textinline:
            #valuey is the initial y plus the height
            valuey = annotations[i][2][1]+annotations[i][2][3]+0.02

            return valuey

def find_line(line,annotations):    

    for i in range(len(annotations)):
        linenum = annotations[i][2][0]
        #print(linenum)
        #print()
        if (line-linenum)<0.03:
            return i

def find_text_between_X_values(xmin,xmax,annotations):    
    newarray = []
    for i in range(len(annotations)):
        #print("***",annotations[i][2])
        x = annotations[i][2][0]
        #print(float(x)>xmin)
        #print(float(x)<xmax)
        if float(x)>xmin and float(x)<xmax:
            newarray.insert(i,annotations[i])
        
    return newarray

def find_text_between_Y_values(ymin,ymax,annotations):    
    newarray = []
    for i in range(len(annotations)):
        y = annotations[i][2][1]
        if float(y)>ymin and float(y)<ymax:
            newarray.insert(i,annotations[i])
        
    return newarray

def first_approach_read(c,filename,camera,ordered):
    alldataarray = []
    count =0

    alldataarray.insert(count,c)
    count +=  1

    #***************************************************************
    #**********************get design no**********************
    #***************************************************************
    #designnumarray = find_text_between_Y_values(0,0.1,ordered)   
    designnumarray = find_text_between_Y_values(0.85,1,ordered)   
    #print(len(designnumarray))
    ''' this is the old way which was finding the first 
    two values but it's no robust enoguh
    designno = [ordered[0],ordered[1]]
    '''
    #sort them by Y so we get the bottom part of the image or headers first
    designno_byY = sort_by_X(designnumarray)
    print("\nDesign No.: ",designno_byY)
    #create a word iterating over all values in the array
    worddesignnumadd = ""
    for worddesignnumaddi in range(0,len(designno_byY)):
        worddesignnumadd += designno_byY[worddesignnumaddi][0]
    worddesignnumadd = worddesignnumadd.replace('Registered Design No','')
    worddesignnumadd = worddesignnumadd.replace('.','')
    print(worddesignnumadd)
    alldataarray.insert(count,worddesignnumadd)
    count += 1
    
    #***************************************************************
    #**********************get date application**********************
    #***************************************************************
    #dateapparray = find_text_between_Y_values(0.1,0.16,ordered)   
    dateapparray = find_text_between_Y_values(0.82,0.87,ordered)   
    #print(len(dateapparray))
    ''' this is the old way which was finding the  
    two values but it's no robust enoguh
    dateapp = [ordered[2],ordered[3]]
    '''
    #sort them by Y so we get the bottom part of the image or headers first
    dateapp_byY = sort_by_Y(dateapparray)
    print("\nDate app: ",dateapp_byY)
    #create a word iterating over all values in the array
    worddateappadd = ""
    for worddateappaddi in range(0,len(dateapp_byY)):
        worddateappadd += dateapp_byY[worddateappaddi][0]
    worddateappadd = worddateappadd.replace('Date of Application','')
    print(worddateappadd)
    alldataarray.insert(count,worddateappadd)
    count += 1

    #***************************************************************
    #**********************get date reg**********************
    #***************************************************************
    #dateregarray = find_text_between_Y_values(0.16,0.22,ordered)   
    dateregarray = find_text_between_Y_values(0.75,0.80,ordered)   
    #print(len(dateregarray))
    ''' this is the old way which was finding the  
    two values but it's no robust enoguh
    datereg = [ordered[4],ordered[5]]
    '''
    #sort them by Y so we get the bottom part of the image or headers first
    datereg_byY = sort_by_Y(dateregarray)
    print("\nDate reg: ",datereg_byY)
    #create a word iterating over all values in the array
    worddateregadd = ""
    for worddateregaddi in range(0,len(datereg_byY)):
        worddateregadd += datereg_byY[worddateregaddi][0]
    worddateregadd = worddateregadd.replace('Date as of which design registered','')
    print(worddateregadd)
    alldataarray.insert(count,worddateregadd)
    count += 1

    #***************************************************************
    #**********************get date cert**********************
    #***************************************************************
    #datecerarray = find_text_between_Y_values(0.22,0.28,ordered)  
    datecerarray = find_text_between_Y_values(0.70,0.75,ordered)    
    #print(len(datecerarray))
    ''' this is the old way which was finding the  
    two values but it's no robust enoguh
    datecert = [ordered[6],ordered[7]]
    '''
    #sort them by Y so we get the bottom part of the image or headers first
    datecer_byY = sort_by_Y(datecerarray)
    print("\nDate cer: ",datecer_byY)
    #create a word iterating over all values in the array
    worddateceradd = ""
    for worddateceraddi in range(0,len(datecer_byY)):
        worddateceradd += datecer_byY[worddateceraddi][0]
    worddateceradd = worddateceradd.replace('Certificate of registration issued','')
    print(worddateceradd)
    alldataarray.insert(count,worddateceradd)
    count += 1

    #***************************************************************
    #**********************get article**********************
    #***************************************************************
    #artarray = find_text_between_Y_values(0.28,0.47,ordered)
    artarray = find_text_between_Y_values(0.54,0.70,ordered)   
    #print(len(artarray))
    ''' this is the old way which was finding the  article
    #now get article
    i=8
    keepgoing=1
    art=[]
    linex = ordered[i][2][0]
    newlinex = ordered[i][2][0]
    while keepgoing==1:
        text = ordered[i][0]
        #print(text)
        texttofind = "Name and address"
        if texttofind.lower() in text.lower():
            keepgoing = 0
        else:                 
            newlinex = ordered[i][2][0]
            #check space to ensure it is in the same are
            if (newlinex-linex<0.09):
                art.insert(0,ordered[i])
        if keepgoing==0:
            break
        i=i+1

    #get art
    art_byY = sort_by_Y(art)
    #print("\nArticle: ",art_byY)
    wordart = ""
    #print(len(art_byY))
    '''
    #sort them by Y so we get the bottom part of the image or headers first
    art_byY = artarray#sort_by_Y(artarray)
    print("\nArticle: ",art_byY)
    #create a word iterating over all values in the array
    wordartadd = ""
    for wordartaddi in range(0,len(art_byY)):
        wordartadd += art_byY[wordartaddi][0]+" "
    wordartadd = wordartadd.replace('Article in respect of which design is registered','')
    print(wordartadd)
    alldataarray.insert(count,wordartadd)
    count += 1

    #***************************************************************
    #**********************get proprietor**********************
    #***************************************************************
    #proparray = find_text_between_Y_values(0.47,0.65,ordered) 
    perdesign = find_line_y_for_text("Address for Service",ordered)    
    #print ("1",perdesign)
    if perdesign == None:
        perdesign = 0.35
    #print ("2",perdesign)
    proparray = find_text_between_Y_values(perdesign,0.54,ordered)  
    #print(len(proparray))    
    #sort them by Y so we get the bottom part of the image or headers first
    prop_byY = proparray#sort_by_Y(artarray)
    print("\nProprietary: ",prop_byY)
    #create a word iterating over all values in the array
    wordpropadd = ""
    for wordpropaddi in range(0,len(prop_byY)):
        wordpropadd += prop_byY[wordpropaddi][0]+" "
    wordpropadd = wordpropadd.replace('Name and address of proprietor','')
    print(wordpropadd)
    alldataarray.insert(count,wordpropadd)
    count += 1

    #***************************************************************
    #**********************get address for service**********************
    #***************************************************************
    #addserarray = find_text_between_Y_values(0.65,0.81,ordered) 
    addserarray = find_text_between_Y_values(perdesign-0.2,perdesign,ordered)     
    #print(len(addserarray))    
    #sort them by Y so we get the bottom part of the image or headers first
    addser_byY = addserarray#sort_by_Y(artarray)
    print("\nAddress service: ",addser_byY)
    #create a word iterating over all values in the array
    wordaddseradd = ""
    for wordaddseraddi in range(0,len(addser_byY)):
        wordaddseradd += addser_byY[wordaddseraddi][0]+" "
    wordaddseradd = wordaddseradd.replace('Address for Service','')
    print(wordaddseradd)
    alldataarray.insert(count,wordaddseradd)
    count += 1

    #***************************************************************
    #**********************any other notes**********************
    #***************************************************************
    onotesarray = find_text_between_Y_values(0,perdesign-0.2,ordered)   
    print(len(onotesarray))    
    #sort them by Y so we get the bottom part of the image or headers first
    onotes_byY = onotesarray#sort_by_Y(artarray)
    print("\nOther notes: ",onotes_byY)
    #create a word iterating over all values in the array
    wordonotesadd = ""
    for wordonotesaddi in range(0,len(onotes_byY)):
        wordonotesadd += onotes_byY[wordonotesaddi][0]+" "
    print(wordonotesadd)
    alldataarray.insert(count,wordonotesadd)
    count += 1

    alldataarray.insert(count,datetime.datetime.now().strftime("%d/%B/%Y"))
    count += 1
    alldataarray.insert(count,"Izzy Barrett-Lally and Alfie Lien-Talks")
    count += 1
    alldataarray.insert(count,camera)
    count += 1
    alldataarray.insert(count,filename)
    count += 1
    alldataarray.insert(count,"BT53-209")
    return alldataarray
    

def write_to_csv(csvfile,data):
    with open(csvfile, 'a') as f_object:
        writer_object = writer(f_object)
        # Pass the list as an argument into
        # the writerow()
        writer_object.writerow(datatoadd)

        # Close the file object
        f_object.close()

def display_image(imagetodisplay):
    #images = "BT53-209/IMG_20240724_154908~2.jpg"
    fig, ax = plt.subplots()
    image = mpimg.imread(imagetodisplay)
    im = ax.imshow(image, interpolation='none')
    plt.show()    
# get the path/directory

folder_dir = "BT53-209"
c = 1
for images in os.listdir(folder_dir):
    # check if the image ends with png
    if (images.endswith(".jpg")):
        # images to add
        #imagetodisplay = folder_dir+"/"+"IMG_20240724_135949~2.jpg"#images
        #display_image(imagetodisplay)
        imagetodisplay = folder_dir+"/"+images
        print(imagetodisplay)
        #print(images)
        #annotations = ocrmac.OCR(folder_dir+"/"+images).recognize()
        #get the annotations
        image = PIL.Image.open(imagetodisplay)
        # Get the exif data and map to the correct tags
        exif_data = {
                        PIL.ExifTags.TAGS[k]: v
                        for k,v in image._getexif().items()
                        if k in PIL.ExifTags.TAGS
                    }

        #pprint(exif_data)
        annotations = ocrmac.OCR(image).recognize()
        #img = ocrmac.OCR('registration882209.png').annotate_PIL()
        #img
        #print("annotations ",annotations)
        #print(len(annotations))
        #assumes image is rotated
        #order first by x values of bounding boxes
        orderedbyy = sort_by_Y(annotations)

        '''
        #calculate how distorted it is
        #first: get the box to the left which is the first
        topx1 = ordered[0][2][0]
        topy1 = ordered[0][2][1]
        topx2 = ordered[0][2][2]
        topy2 = ordered[0][2][3]
        print(ordered[0][2])
        print (topy1-topy2)
        print (topx2-topx1)
        image = mpimg.imread(imagetodisplay)
        print(image.ndim)

        src = np.array([[0, 0], [0, image.shape[1]], [image.shape[0], image.shape[1]], [image.shape[0], 0]])
        dst = np.array([[180, 120], [0, image.shape[1]], [image.shape[0], image.shape[1]], [2870, 26]])

        tform3 = transform.ProjectiveTransform()
        tform3.estimate(src, dst)
        newimage = transform.warp(image, tform3, output_shape=(image.shape[0], image.shape[1]))
        print(newimage.ndim)
        
        #im = np.array(newimage,dtype=np.uint8)
        im = (newimage * 255).astype(np.uint8)
        pil_img = Image.fromarray(im ,'RGB')
        #print(pil_img.ndim)

        fig, ax = plt.subplots(nrows=3)
        ax[0].imshow(image, interpolation='none')
        ax[1].imshow(newimage, interpolation='none')
        ax[2].imshow(pil_img, interpolation='none')
        plt.show() 

        '''

        #print("\nresult ",ordered)
        #second_approach_read(annotations)
        #print(orderedbyy)
        reversedarray = orderedbyy[::-1]
        #print(reversedarray)
        datatoadd = first_approach_read(c,images,
            exif_data['Make']+" "+exif_data['Model'],reversedarray)
        write_to_csv("metadata.csv",datatoadd)
    c+=1
