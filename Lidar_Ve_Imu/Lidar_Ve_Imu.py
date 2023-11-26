#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan, Imu
from geometry_msgs.msg import Twist
import numpy as np
from math import pi
from tf.transformations import euler_from_quaternion
from time import sleep

def LidarIslemleri( lidarVerisi ): #Anlik Lidar Verisi ve Veriyi Bolgelere Ayirma
    arr1 = np.array(lidarVerisi.ranges[0:44]) #Sol On
    arr1 = arr1[arr1 != 0.0]
    if len(arr1) == 0:
        arr1 = np.array([1.0])
    # arr2 = np.array(lidarVerisi.ranges[45:89])
    # arr2 = arr2[arr2 != 0.0]
    # if len(arr2) == 0:
    #     arr2 = np.array([1.0])
    # arr3 = np.array(lidarVerisi.ranges[90:134])
    # arr3 = arr3[arr3 != 0.0]
    # if len(arr3) == 0:
    #     arr3 = np.array([1.0])
    # arr4 = np.array(lidarVerisi.ranges[135:179])
    # arr4 = arr4[arr4 != 0.0]
    # if len(arr4) == 0:
    #     arr4 = np.array([1.0])
    # arr5 = np.array(lidarVerisi.ranges[180:224])
    # arr5 = arr5[arr5 != 0.0]
    # if len(arr5) == 0:
    #     arr5 = np.array([1.0])
    arr6 = np.array(lidarVerisi.ranges[225:269]) #Sag Orta - 1
    arr6 = arr6[arr6 != 0.0]
    if len(arr6) == 0:
        arr6 = np.array([1.0])
    arr7 = np.array(lidarVerisi.ranges[270:314]) #Sag Orta -2 
    arr7 = arr7[arr7 != 0.0]
    if len(arr7) == 0:
        arr7 = np.array([1.0])
    arr8 = np.array(lidarVerisi.ranges[315:359]) #Sag On
    arr8 = arr8[arr8 != 0.0]
    if len(arr8) == 0:
        arr8 = np.array([1.0])
    bolgeler = {
        '1':        min(min(arr1), 10),  #1 (45 derece)
        # '2':        min(min(arr2), 10),  #2 (45 derece)
        # '3':        min(min(arr3), 10),  #3 (45 derece)
        # '4':        min(min(arr4), 10),  #4 (45 derece)
        # '5':        min(min(arr5), 10),  #5 (45 derece)
        '6':        min(min(arr6), 10),  #6 (45 derece)
        '7':        min(min(arr7), 10),  #7 (45 derece)
        '8':        min(min(arr8), 10),  #8 (45 derece)
    }
    # print( bolgeler )
    OtonomHareket( bolgeler )

hiz = Twist()
hiz.linear.x = 0.0
hiz.angular.z = 0.0

yaw = 0.0
def ImuIslemleri( imuVerisi ): #Anlik Imu Verisi
    global yaw
    rot_q = imuVerisi.orientation
    yaw = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])[2]

anlikX = 0.0
anlikY = 0.0
def OdomIslemleri( odomVerisi ): #Anlik Odometry Verisi
    global anlikX, anlikY
    anlikX = odomVerisi.pose.pose.position.x 
    anlikY = odomVerisi.pose.pose.position.y

kontrol = 0
print("Kontrol: ", kontrol)
def OtonomDonus(): #Saga - Sola Otonom Donus
    global hiz, yaw, kontrol
    if ( istenilenYaw >= ( ( -1 ) * pi ) and istenilenYaw <= ( ( -1 ) * ( pi / 2 ) ) and yaw > ( pi / 2 ) and yaw < ( pi ) ) or ( istenilenYaw >= ( pi / 2 ) and istenilenYaw <= ( pi ) and yaw < ( ( -1 ) * ( pi / 2 ) ) and yaw > ( ( -1 ) * pi ) ):
        if ( istenilenYaw - yaw ) > 0.01: #Burasi Euler Acilari Olarak Butune Dahil Edilemeyen Istisna Bolge (Normalin Tam Tersi Donmesi Gerekiyor.)
            print("Saga")
            hiz.angular.z = -0.2
            rospy.Publisher("/cmd_vel", Twist, queue_size=1).publish(hiz)
        elif ( istenilenYaw - yaw ) < -0.01:
            print("Sola")
            hiz.angular.z = 0.2
            rospy.Publisher("/cmd_vel", Twist, queue_size=1).publish(hiz)
        else:
            print("Donus Bitti")
            hiz.angular.z = 0.0
            rospy.Publisher("/cmd_vel", Twist, queue_size=1).publish(hiz)
            sleep( 0.5 )
            rospy.Publisher("/cmd_vel", Twist, queue_size=1).publish(hiz)
            kontrol += 1
            print("Kontrol: ", kontrol)
    else:
        if ( istenilenYaw - yaw ) > 0.01:
            print("Sola")
            hiz.angular.z = 0.2
            rospy.Publisher("/cmd_vel", Twist, queue_size=1).publish(hiz)
        elif ( istenilenYaw - yaw ) < -0.01:
            print("Saga")
            hiz.angular.z = -0.2
            rospy.Publisher("/cmd_vel", Twist, queue_size=1).publish(hiz)
        else:
            print("Donus Bitti")
            hiz.angular.z = 0.0
            rospy.Publisher("/cmd_vel", Twist, queue_size=1).publish(hiz)
            sleep( 0.5 )
            rospy.Publisher("/cmd_vel", Twist, queue_size=1).publish(hiz)
            kontrol += 1
            print("Kontrol: ", kontrol)

def OtonomDuz():
    global hiz, kontrol
    print("Duz")
    hiz.linear.x = 0.16
    rospy.Publisher("/cmd_vel", Twist, queue_size=1).publish(hiz)

istenilenYaw = 0.0
def OtonomDur():
    global hiz, kontrol, istenilenYaw
    print("Dur")
    hiz.linear.x = 0.0
    hiz.angular.z = 0.0
    rospy.Publisher("/cmd_vel", Twist, queue_size=1).publish(hiz)
    sleep( 0.5 )
    rospy.Publisher("/cmd_vel", Twist, queue_size=1).publish(hiz)
    
ilkX = 0.0
ilkY = 0.0
alinanYol = 0.0
def OtonomHareket( bolgeler ): #Kontrol Degiskenyle Otomata Kullanarak Otonom Hareket
    global hiz, kontrol, yaw, istenilenYaw, ilkX, ilkY, anlikX, anlikY, alinanYol
    if kontrol == 0: #Engele Kadar Duz Gitme ve Durma
        if bolgeler['1'] > 0.5 and bolgeler['8'] > 0.5:
            OtonomDuz()
        else:
            OtonomDur()
            istenilenYaw = yaw + ( ( pi ) / 2 )
            if istenilenYaw > pi:
                istenilenYaw += ( ( -2 ) * pi ) 
            kontrol = 1
            print("Kontrol: ", kontrol)
    elif kontrol == 1: #Engelden Kacmak Icin Ilk 90 Derece Donus (Sola)
        ilkX = anlikX
        ilkY = anlikY
        OtonomDonus()
    elif kontrol == 2: #Engelden Uzaklasmak Icin Gitme Ve Uzaklasinca Durma (Ayrica Aldigi Yolu Hesaplama)
        if bolgeler['6'] < 1 or bolgeler['7'] < 1:
            OtonomDuz()
        else:
            OtonomDur()
            alinanYol = ( ( ( anlikX - ilkX ) **2 ) + ( ( anlikY - ilkY ) **2 ) )**0.5
            istenilenYaw -= ( pi / 2 )
            if istenilenYaw < ( ( -1 ) * pi ):
                istenilenYaw += ( 2 * pi )
            kontrol = 3
            print("Kontrol: ", kontrol)
    elif kontrol == 3: #Engelden Kacmak Icin Ikinci 90 Derece Donus (Saga)
        OtonomDonus()
    elif kontrol == 4: #Engeli Gorene Kadar Duz Gitme
        if bolgeler['6'] > 1 or bolgeler['7'] > 1:
            OtonomDuz()
        else:
            kontrol = 5
            print("Kontrol: ", kontrol)
    elif kontrol == 5: #Engel Sagindan Cikana Kadar Duz Gitme Ve Durma 
        if bolgeler['6'] < 1 or bolgeler['7'] < 1:
            OtonomDuz()
        else:
            OtonomDur()
            istenilenYaw -= ( pi / 2 )
            if istenilenYaw < ( ( -1 ) * pi ):
                istenilenYaw += ( 2 * pi )
            kontrol = 6
            print("Kontrol: ", kontrol)
    elif kontrol == 6: #Engelden Kacmak Icin Ucuncu 90 Derece Donus (Saga)
        ilkX = anlikX
        ilkY = anlikY
        OtonomDonus()
    elif kontrol == 7: #Aldigi Yol Kadar Duz Gitmek
        if (abs( ( ( ( ( anlikX - ilkX ) **2 ) + ( ( anlikY - ilkY ) **2 ) ) **0.5 ) - alinanYol ) > 0.02):
            OtonomDuz()
        else:
            OtonomDur()
            istenilenYaw = yaw + ( ( pi ) / 2 )
            if istenilenYaw > pi:
                istenilenYaw += ( ( -2 ) * pi ) 
            kontrol = 8
            print("Kontrol: ", kontrol)
    elif kontrol == 8: #Son Donus (Sola)
        OtonomDonus()
    elif kontrol == 9: #Engelden Kacisin Bitisi ve Siradaki Engele Gecis
        print("Engelden Kacis Bitti!")
        kontrol = 0
        print("Kontrol: ", kontrol)

rospy.init_node('Otonom_Engelden_Kacis')
rospy.Subscriber("/scan", LaserScan, LidarIslemleri)
rospy.Subscriber("/imu", Imu, ImuIslemleri)
rospy.Subscriber("/odom", Odometry, OdomIslemleri)
rospy.spin()