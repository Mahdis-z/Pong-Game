
# coding: utf-8

# In[91]:


from cv2 import imshow, waitKey, destroyAllWindows,circle, imread, putText, FONT_HERSHEY_SIMPLEX, VideoWriter
from numpy import ones
from random import randint, sample
from time import sleep
import numpngw

def move(ground,x_s,y_s,length,thick,v,v_s,color,color_s,lr):
    if lr == 1:
        for col in range(3):
            ground[y_s-thick//2:y_s+thick//2,x_s-length//2:x_s-length//2+v+v_s,col]=color[col]
            ground[y_s-thick//2:y_s+thick//2,x_s+length//2:x_s+length//2+v+v_s,col]=color_s[col]
    elif lr == -1:
        for col in range(3):
            ground[y_s-thick//2:y_s+thick//2,x_s-length//2-v-v_s:x_s-length//2,col]=color_s[col]
            ground[y_s-thick//2:y_s+thick//2,x_s+length//2-v-v_s:x_s+length//2,col]=color[col]
    return ground
    
dim_y = 450
dim_x = int(dim_y *0.8)
out = VideoWriter('Pong.mp4',4, 40, (dim_x,dim_y))
color = [110,180,150]
color_s = [250,255,255]
ground = ones((dim_y,dim_x,3),'uint8')
radius,thick, length = 10,14,80
x,y = randint(radius+1,dim_x-radius-1), randint(radius+1,int(dim_y-radius-1-0.1*dim_y-thick+0.5))
v=6
vx = sample([v,-v],1)[0]
vy = -v
v_s=1
#wiper = ones((thick,v+1,3),'uint8')
stick = ones((thick,length,3),'uint8')
for col in range(3):
    ground[:,:,col] = color[col] 
    #wiper[:,:,col] = color[col] 
    stick[:,:,col] = color_s[col]
x_s = dim_x//2
y_s = int(0.9*dim_y+0.5)
ground[y_s-thick//2:y_s+thick//2,x_s-length//2:x_s+length//2,:]=stick
iterate = 0
key = 255
while True:
    ground[dim_y-38:dim_y-15,88:110,:]=200
    putText(ground,"speed: "+str(max(0,min(iterate//300,7)-5)+1),(10,dim_y-20),FONT_HERSHEY_SIMPLEX,0.7,[100,100,101])
    iterate+=1
    circle(ground,(x,y),radius-3,[250,250,255],15)
    imshow('ground',ground)
    #key = waitKey(1) & 0xFF
    i = 0
    while i<(7-min(iterate//300,6)):
        i+=1
        imshow('ground',ground)
        if iterate%2==0 and min(iterate//300,7)>=7:
            out.write(ground)
        key = waitKey(1) & 0xFF
        if iterate//300 <= 6:
            sleep(0.0003)
        if key == 27:
            break
    
    if key == 27:
        break
    if key == ord('p'):
        key = waitKey(0) & 0xFF
        if key == 27:
            break
    elif key == ord('d') and x_s+length//2 < dim_x:
        ground = move(ground,x_s,y_s,length,thick,v,v_s,color,color_s,lr=1)
        x_s+=v+v_s
    elif key == ord('a') and x_s-length//2 >= v+v_s:
        ground = move(ground,x_s,y_s,length,thick,v,v_s,color,color_s,lr=-1)
        x_s-=v+v_s
    ## solver-----------

    if x_s < x and x_s < dim_x-length//2-v: 
        if vy == v:
            lr = 1    
        else: 
            lr = (x_s<dim_x//2)*1 - (x_s>dim_x//2)*1
        ground = move(ground,x_s,y_s,length,thick,v,v_s,color,color_s,lr=lr)
        x_s= x_s +lr*(v+v_s)
    elif x_s > x and x_s > length//2+v:
        if vy == v:
            lr = -1    
        else: 
            lr = (x_s<dim_x//2)*1 - (x_s>dim_x//2)*1
        ground = move(ground,x_s,y_s,length,thick,v,v_s,color,color_s,lr=lr)
        x_s= x_s +lr*(v+v_s)

    ##------------------
    circle(ground,(x,y),radius-3,color,15)
    if  x+vx >= dim_x -radius or radius >= x+vx:
        vx=-vx
    if  y+vy <= radius:
        vy=-vy
    if (x_s-length//2-radius <= x+vx <= x_s+length//2+radius and  y+2*vy+radius>= y_s-thick//2+1):
        #ground[y_s-thick//2:y_s+thick//2,x_s-length//2:x_s+length//2,:]=stick
        vy = -v
    if y > dim_y+radius:
        putText(ground,"Game Over",(dim_x//2-100,dim_y//2),FONT_HERSHEY_SIMPLEX,1.0,[255,255,255])
        imshow('ground',ground)
        waitKey(0)
        break
    x+=vx
    y+=vy
out.release()
destroyAllWindows()

