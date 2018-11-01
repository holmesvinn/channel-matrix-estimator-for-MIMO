import numpy as np
import matplotlib.pyplot as plt
import time
import math 
import cv2
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import cmath


show = False

d = 200
ripple = 1

width = 850
height = 600

w = width/9
w = int(w)
h = height/1.5
h = int(h)
w_2=int(width/2)


img = np.zeros((height,width,3), np.uint8)
img[:] = 255

img2 = np.zeros((height,width,3),np.uint8)
img2[:] = 255


cv2.namedWindow('parameters')

def callback(x):
    pass

cv2.createTrackbar('Frequency(KHz)','parameters',1,200,callback)
cv2.createTrackbar('Distance(meters)','parameters',240,300,callback)
cv2.createTrackbar('Seperation(meters)','parameters',100,100,callback)
cv2.createTrackbar('write(file)','parameters',0,1,callback)



while 1:

    cv2.imshow("MIMO System Model",img) 
    
    distance = cv2.getTrackbarPos('Distance(meters)','parameters')
    seperation = cv2.getTrackbarPos('Seperation(meters)','parameters')
    frequency = cv2.getTrackbarPos('Frequency(KHz)','parameters')
    write_data = cv2.getTrackbarPos('write(file)','parameters')
    if frequency == 0:
        frequency = 1
    wavelength = 300000/frequency
    img[:] = 255

    cv2.circle(img,(w,h), 5, (106, 61, 219), -1)
    cv2.circle(img,(w,h-230), 5, (99,19,247), -1)
    
    cv2.putText(img,'2 x 2 MIMO Configuration',(300,50), cv2.FONT_HERSHEY_SIMPLEX, 0.8,(128,0,0),2,cv2.LINE_AA)
    cv2.putText(img,'TX1',(w,h-180), cv2.FONT_HERSHEY_SIMPLEX, 0.7,(190,101,75),2,cv2.LINE_AA)
    cv2.putText(img,'TX2',(w,h+40), cv2.FONT_HERSHEY_SIMPLEX, 0.7,(99,19,247),2,cv2.LINE_AA)

    coord1 = (w_2+int(distance),h+20)
    coord2 = (w_2+int(distance),h-250-seperation)
    ccoord1 = (w_2+int(distance),h)
    ccoord2 = (w_2+int(distance),h-230-seperation)

    
    cv2.putText(img,'Rx1',(ccoord1[0],ccoord1[1]-20), cv2.FONT_HERSHEY_SIMPLEX, 0.7,(190,101,75),2,cv2.LINE_AA)
    cv2.putText(img,'Rx2',(ccoord2[0],ccoord2[1]+30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,(99,19,247),2,cv2.LINE_AA)

    cv2.circle(img,ccoord1,5,(106, 61, 219),-1)
    cv2.circle(img,ccoord2,5,(106, 61, 219),-1)
    cv2.line(img,ccoord1,(w,h),(0,0,0),1)
    cv2.line(img,ccoord2,(w,h),(0,0,0),1)
    cv2.line(img,ccoord1,(w,h-230),(0,0,0),1)
    cv2.line(img,ccoord2,(w,h-230),(0,0,0),1)
    
    dist1 = math.sqrt(((h-coord1[1])**2)+((w-coord1[0])**2))
    dist2 = math.sqrt(((h-coord2[1])**2)+((w-coord2[0])**2))
    dist3 = math.sqrt(((h-230-coord1[1])**2)+((w-coord1[0])**2))
    dist4 = math.sqrt(((h-230-coord2[1])**2)+((w-coord2[0])**2))
    dist5 = 170
    dist6 = math.sqrt(((coord1[1]-coord2[1])**2)+((coord1[0]-coord2[0])**2))

    delr = (dist6/(wavelength*2))
    delt = (dist5/(wavelength*2))

    phir12 = 90
    phir11 = 90 + math.atan(dist5/dist1)
    phir22 = math.atan(dist1/dist6)
    phir21 = math.atan(dist6/dist1)

    phit21 = 90
    phit22 = 90 + math.atan(dist6/dist1)
    phit11 = math.atan(dist1/dist5)
    phit12 = phit11+phir11-phir12

    aa11 = ((4*3.14*dist3)**2)/(wavelength**2)
    aa22 = ((4*3.14*dist2)**2)/(wavelength**2)
    aa12 = ((4*3.14*dist4)**2)/(wavelength**2)
    aa21 = ((4*3.14*dist1)**2)/(wavelength**2)

    

    a11 = 2*(math.cos(2*3.14*dist3/wavelength) - math.sin(2*3.14*dist3/wavelength)*1j)
    a22 = 2*(math.cos(2*3.14*dist2/wavelength) - math.sin(2*3.14*dist2/wavelength)*1j)
    a12 = 2*(math.cos(2*3.14*dist4/wavelength) - math.sin(2*3.14*dist4/wavelength)*1j)
    a21 = 2*(math.cos(2*3.14*dist1/wavelength) - math.sin(2*3.14*dist1/wavelength)*1j)
    
    er1 = [0.707, math.cos(2*3.14*delr*math.cos(phir11)) - math.sin(2*3.14*delr*math.cos(phir11))*1j]

    er2= [0.707, math.cos(2*3.14*delr*math.cos(phir12)) - math.sin(2*3.14*delr*math.cos(phir12))*1j]

    er3 = [0.707 , math.cos(2*3.14*delr*math.cos(phir21)) - math.sin(2*3.14*delr*math.cos(phir21))*1j]

    er4 = [0.707, math.cos(2*3.14*delr*math.cos(phir22)) - math.sin(2*3.14*delr*math.cos(phir22))*1j]
    

    et1= [0.707, math.cos(2*3.14*delt*math.cos(phit11)) - math.sin(2*3.14*delt*math.cos(phit11))*1j]

    et2 = [0.707, math.cos(2*3.14*delt*math.cos(phit12)) - math.sin(2*3.14*delt*math.cos(phit12))*1j]

    et3 = [0.707,math.cos(2*3.14*delt*math.cos(phit21)) - math.sin(2*3.14*delt*math.cos(phit21))*1j]

    et4 = [0.707, math.cos(2*3.14*delt*math.cos(phit22)) - math.sin(2*3.14*delt*math.cos(phit22))*1j]

    h1 = [er1[0]*et1[0], er1[0]*et1[1], er1[1]*et1[0], er1[1]* et1[1]]
    h2 = [er2[0]*et2[0], er2[0]*et2[1], er2[1]*et2[0], er2[1]* et2[1]]
    h3 = [er3[0]*et3[0], er3[0]*et3[1], er3[1]*et3[0], er3[1]* et3[1]]
    h4 = [er4[0]*et4[0], er4[0]*et4[1], er4[1]*et4[0], er4[1]* et4[1]]

    val1 = a11*h1[0]+a12*h2[0]+a12*h2[0]+a12*h2[0] 
    val2 = a11*h1[1]+a12*h2[1]+a12*h2[1]+a12*h2[1]
    val3 =  a11*h1[2]+a12*h2[2]+a12*h2[2]+a12*h2[2]
    val4 =  a11*h1[3]+a12*h2[3]+a12*h2[3]+a12*h2[3]

    real = [val1.real, val2.real,val3.real,val4.real]
    imaginery = [val1.imag,val2.imag,val3.imag,val4.imag]

    print(real, imaginery)
    rval1 = cmath.polar(val1)
    rval2 = cmath.polar(val2)
    rval3 = cmath.polar(val3)
    rval4 = cmath.polar(val4)
    
    if show == True:
        cv2.imshow("Model parameters",img2)
        img2[:] = 255
        cv2.putText(img2,'MIMO Channel Parameters',(50,50), cv2.FONT_HERSHEY_SIMPLEX, 0.685,(190,101,75),2,cv2.LINE_AA)
        cv2.putText(img2,str('%0.2f + %0.2fi' % (val1.real, val1.imag)),(50,150), cv2.FONT_HERSHEY_SIMPLEX, 0.685,(190,101,75),2,cv2.LINE_AA)
        cv2.putText(img2,str('%0.2f + %0.2fi' % (val2.real, val2.imag)),(300,150), cv2.FONT_HERSHEY_SIMPLEX, 0.685,(190,101,75),2,cv2.LINE_AA)
        cv2.putText(img2,str('%0.2f + %0.2fi' % (val3.real, val3.imag)),(50,200), cv2.FONT_HERSHEY_SIMPLEX, 0.685,(190,101,75),2,cv2.LINE_AA)
        cv2.putText(img2,str('%0.2f + %0.2fi' % (val4.real, val4.imag)),(300,200), cv2.FONT_HERSHEY_SIMPLEX, 0.685,(190,101,75),2,cv2.LINE_AA)
        if write_data == 1:
            f = open("channels.txt","a")
            f.write(str(rval1)+"\n"+str(rval2)+"\n"+str(rval3)+"\n"+str(rval4)+"\n")

        
        
            



    cv2.putText(img,str('%.3f'%(dist1/10)),(int((w+ccoord1[0])/2), int((h+ccoord1[1])/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7,(190,101,75),2,cv2.LINE_AA)
    cv2.putText(img,str('%.3f'%(dist2/10)),(int((w-80+ccoord2[0])/2), int((h+ccoord2[1])/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7,(99,19,247),2,cv2.LINE_AA)
    cv2.putText(img,str('%.3f'%(dist3/10)),(int((w+ccoord1[0])/2), int((h-230+ccoord1[1])/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7,(99,19,247),2,cv2.LINE_AA)
    cv2.putText(img,str('%.3f'%(dist4/10)),(int((w+ccoord2[0])/2), int((h-230+ccoord2[1])/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7,(99,19,247),2,cv2.LINE_AA)

    if frequency < 25:
        cv2.circle(img,(w,h), ripple, (220,0,0), 1)
        cv2.circle(img,(w,h), ripple*2, (200,0,0), 1)
        cv2.circle(img,(w,h), ripple*4, (100,0,0), 1)
        cv2.circle(img,(w,h), ripple*6, (5,0,0), 1)

        cv2.circle(img,(w,h-230), ripple, (0,0,220), 1)
        cv2.circle(img,(w,h-230), ripple*2, (0,0,200), 1)
        cv2.circle(img,(w,h-230), ripple*4, (0,0,100), 1)
        cv2.circle(img,(w,h-230), ripple*6, (0,0,5), 1)

    elif frequency < 50:
        cv2.circle(img,(w,h), ripple, (220,0,0), 3)
        cv2.circle(img,(w,h), ripple*2, (200,0,0), 3)
        cv2.circle(img,(w,h), ripple*3, (150,0,0), 3)
        cv2.circle(img,(w,h), ripple*4, (100,0,0), 3)
        cv2.circle(img,(w,h), ripple*5, (50,0,0), 3)
        cv2.circle(img,(w,h), ripple*6, (5,0,0), 2)

        cv2.circle(img,(w,h-230), ripple, (0,0,220), 2)
        cv2.circle(img,(w,h-230), ripple*2, (0,0,200), 2)
        cv2.circle(img,(w,h-230), ripple*3, (0,0,150), 2)
        cv2.circle(img,(w,h-230), ripple*4, (0,0,100), 2)
        cv2.circle(img,(w,h-230), ripple*5, (0,0,50), 2)
        cv2.circle(img,(w,h-230), ripple*6, (0,0,5), 2)


    elif frequency < 100:
        cv2.circle(img,(w,h), ripple, (220,0,0), 2)
        cv2.circle(img,(w,h), ripple*2, (200,0,0), 2)
        cv2.circle(img,(w,h), int(ripple*2.5), (175,0,0), 2)
        cv2.circle(img,(w,h), ripple*3, (150,0,0), 2)
        cv2.circle(img,(w,h), int(ripple*3.5), (125,0,0), 2)
        cv2.circle(img,(w,h), ripple*4, (100,0,0), 2)
        cv2.circle(img,(w,h), int(ripple*4.5), (75,0,0), 2)
        cv2.circle(img,(w,h), ripple*5, (50,0,0), 2)
        cv2.circle(img,(w,h), ripple*6, (5,0,0), 2)

        cv2.circle(img,(w,h-230), ripple, (0,0,220), 2)
        cv2.circle(img,(w,h-230), ripple*2, (0,0,200), 2)
        cv2.circle(img,(w,h-230), int(ripple*2.5), (0,0,175), 2)
        cv2.circle(img,(w,h-230), ripple*3, (0,0,150), 2)
        cv2.circle(img,(w,h-230), int(ripple*3.5), (0,0,125), 2)
        cv2.circle(img,(w,h-230), ripple*4, (0,0,100), 2)
        cv2.circle(img,(w,h-230), int(ripple*4.5), (0,0,75), 2)
        cv2.circle(img,(w,h-230), ripple*5, (0,0,50), 2)
        cv2.circle(img,(w,h-230), ripple*6, (0,0,5), 2)
    
    elif frequency <255:
        cv2.circle(img,(w,h), ripple, (255, 255, 255), 2)
        cv2.circle(img,(w,h), ripple*2, (200,200,200), 17)
        cv2.circle(img,(w,h), int(ripple*2.5), (175,175,175), 2)
        cv2.circle(img,(w,h), int(ripple*2.8), (162,162,162), 2)
        cv2.circle(img,(w,h), ripple*3, (150,150,150), 2)
        cv2.circle(img,(w,h), int(ripple*3.5), (125,125,125), 2)
        cv2.circle(img,(w,h), int(ripple*3.8), (112,112,112), 2)
        cv2.circle(img,(w,h), ripple*4, (100,100,100), 2)
        cv2.circle(img,(w,h), int(ripple*4.5), (75,75,75), 2)
        cv2.circle(img,(w,h), int(ripple*4.8), (62,62,62), 2)
        cv2.circle(img,(w,h), ripple*5, (50,50,50), 2)
        cv2.circle(img,(w,h), int(ripple*5.5), (50,50,50), 2)
        cv2.circle(img,(w,h), int(ripple*5.8), (25,25,25), 2)
        cv2.circle(img,(w,h), ripple*6, (5,5,5), 2)

        cv2.circle(img,(w,h-230), ripple, (255, 255, 255), 2)
        cv2.circle(img,(w,h-230), ripple*2, (200,200,200), 17)
        cv2.circle(img,(w,h-230), int(ripple*2.5), (175,175,175), 2)
        cv2.circle(img,(w,h-230), int(ripple*2.8), (162,162,162), 2)
        cv2.circle(img,(w,h-230), ripple*3, (150,150,150), 2)
        cv2.circle(img,(w,h-230), int(ripple*3.5), (125,125,125), 2)
        cv2.circle(img,(w,h-230), int(ripple*3.8), (112,112,112), 2)
        cv2.circle(img,(w,h-230), ripple*4, (100,100,100), 2)
        cv2.circle(img,(w,h-230), int(ripple*4.5), (75,75,75), 2)
        cv2.circle(img,(w,h-230), int(ripple*4.8), (62,62,62), 2)
        cv2.circle(img,(w,h-230), ripple*5, (50,50,50), 2)
        cv2.circle(img,(w,h-230), int(ripple*5.5), (50,50,50), 2)
        cv2.circle(img,(w,h-230), int(ripple*5.8), (25,25,25), 2)
        cv2.circle(img,(w,h-230), ripple*6, (5,5,5), 2)

    ripple = ripple+10
    if ripple*7 > width:
        ripple = 1

    time.sleep(0.085)

    k = cv2.waitKey(1)
    if k == ord('q'):
        break 
    if k == ord('s'):
        show = True
    if k == ord('h'):
        show = False

cv2.destroyAllWindows()