# coding=utf-8

import cv2 as cv
import numpy as np
from datetime import datetime
import math
import db as mdb
import proc_img
import logging

log_main = logging.getLogger('log')

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)
except:
    log_main.warning(u'Error importing RPi.GPIO!')


def create_img_description(frame, x, y, r, color=(0, 0, 0)):
    """
    draw on cam-image circle
    :return:
    """
    cv.circle(frame, (x, y), r, color, 4)
    return None


def create_img_discover_circle(frame, x, y, r):
    """
    draw result
    and write description consist of center position in pixels
    :return:
    """
    color = (0, 0, 0)
    font = cv.FONT_HERSHEY_SIMPLEX
    fontscale = 1
    linetype = 2
    cv.circle(frame, (x, y), r, color, 4)
    bottomleftcorneroftext = (x, y)
    cv.putText(frame, 'X:' + str(x) + ', Y:' + str(y),
               bottomleftcorneroftext,
               font,
               fontscale,
               color,
               linetype)
    return None

def main():
    """
    main loop
    :return:
    """
    log_main.debug(u'start running %s', datetime.now())
    rgb_color_of_screen_draws = (0, 0, 0)
    db = mdb.Mdb()
    # --- setup: ---
    show_processing_on_screen = db.get_setdefault_value_for_key('show_processing', 1)
    show_gotit_on_screen = db.get_setdefault_value_for_key('show_gotit', 1)
    # whay should be shown on screen (when allowed: 0 - long present circles, 1- only catch circles)
    onimg_mid0_or_moment1 = db.get_setdefault_value_for_key('mid0_or_moment1', 0)
    # minDist – Minimum distance between the centers of the detected circles
    mindist = db.get_setdefault_value_for_key('minDist', 100)
    # It is the higher threshold of the two passed to the Canny() edge detector (the lower one is twice smaller)
    higher_threshold = db.get_setdefault_value_for_key('higher_threshold', 1520)  # 1529-1530
    # --- do not change: ---
    if show_processing_on_screen:
        cv.cv.NamedWindow("camera_procesing", 0)
    pri = proc_img.ProcesingImg(0, mindist, higher_threshold)
    circles, gframe, cframe = pri.pickup_circles()
    try:
        img_size = gframe.shape
        log_main.info(u'calculate, depend of video-size:')
        pri.max_radius = int(min(img_size) / 2.2)
        pri.min_radius = int(pri.max_radius * 0.2)
        log_main.info(u'min_radius  = %s', pri.min_radius)
        log_main.info(u'max_radius  = %s', pri.max_radius)
    except:
        log_main.error(u'something wrong with web-cam image...')
        exit()
    dt_loop = datetime.now()
    saved_loops = 10
    needed_circle_like_repeat = int(saved_loops * 0.8)
    log_main.info(u'how many loops will be stored id DB: %s', saved_loops)
    log_main.info(u'how many hits to confirm: %s', needed_circle_like_repeat)
    empty_loop_count = 0
    prev_led_on1 = None
    while True:
        cofirmed_circles_list = []
        deltatime_loop = (datetime.now() - dt_loop).total_seconds()
        dt_loop = datetime.now()
        db.setupdate_value_for_key('loop', '1')
        db.setupdate_value_for_key('less_false', pri.less_false)
        circles, gframe, cframe = pri.pickup_circles()
        delete_older_than_seconds = math.ceil(deltatime_loop * saved_loops)
        db.delete_old_circles(delete_older_than_seconds)
        circles_count = None
        if circles is not None:
            circles_count = len(circles[0])
        pri.adopt_parametr2(circles_count)
        if circles_count:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                if onimg_mid0_or_moment1 == 1:
                    create_img_description(gframe, x, y, r, rgb_color_of_screen_draws)
                db.insert_new_circle(x, y, r)
                log_main.debug(u'circle discovered --> X: %s, Y: %s', x, y)
            for (x, y, r) in circles:
                delta_r = int(r * 0.25)
                delta_xy = delta_r
                like_this_circle = db.select_similar_circles(x-delta_xy, x+delta_xy,
                                                             y-delta_xy, y+delta_xy,
                                                             r-delta_r, r+delta_r)
                like_this_circle_count = len(like_this_circle)
                if like_this_circle_count >= needed_circle_like_repeat:
                    midd = [0, 0, 0]
                    for one in like_this_circle:
                        midd[0] += one[0]
                        midd[1] += one[1]
                        midd[2] += one[2]
                    midd[0] /= like_this_circle_count
                    midd[1] /= like_this_circle_count
                    midd[2] /= like_this_circle_count
                    if onimg_mid0_or_moment1 == 0:
                        create_img_description(gframe, midd[0], midd[1], midd[2], rgb_color_of_screen_draws)
                    log_main.debug(u'circle confirmed --> X: %s, Y: %s', midd[0], midd[1])
                    db.setupdate_value_for_key('led_on1', 1)
                    cofirmed_circles_list.append([x, y, r])
                    empty_loop_count = 0
                else:
                    if empty_loop_count < saved_loops:
                        empty_loop_count += 1
                if empty_loop_count > needed_circle_like_repeat:
                    db.setupdate_value_for_key('led_on1', 0)
                    log_main.debug(u'none of')
        led_on1 = db.get_setdefault_value_for_key('led_on1', 0, saved_loops)
        if led_on1 != prev_led_on1:
            if led_on1 == 0:
                log_main.info(u'LED-OFF')
                try:
                    GPIO.output(23, GPIO.LOW)
                except:
                    pass
                if show_gotit_on_screen:
                    cv.destroyWindow('camera_gotit')
            else:
                log_main.info(u'LED-ON:')
                try:
                    GPIO.output(23, GPIO.HIGH)
                except:
                    pass
                for one in cofirmed_circles_list:
                    log_main.info(u'circle X: %s, Y: %s, R: %s', one[0], one[1], one[2])
                    if show_gotit_on_screen:
                        create_img_discover_circle(cframe, one[0], one[1], one[2])
                if show_gotit_on_screen:
                    cv.imshow('camera_gotit', cframe)
        prev_led_on1 = led_on1
        if led_on1:
            # cv.circle(gframe, (10, 10), 10, rgb_color_of_screen_draws, 4)
            pass
        if show_processing_on_screen:
            cv.imshow('camera_procesing', gframe)

        if cv.cv.WaitKey(10) == 27:
            break
    cv. cv.DestroyAllWindows()
