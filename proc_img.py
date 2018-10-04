# coding=utf-8

import cv2 as cv
import numpy as np
import logging

log_main = logging.getLogger('log')


class ProcesingImg:

    def __init__(self, vid, mindist, higher_threshold, min_radius=0, max_radius=0):
        """

        """
        self.cap = cv.VideoCapture(vid)
        self.less_false = 150  # will be adopted to cam-picture

        self.dp = 2
        self.minDist = mindist
        self.higher_threshold = higher_threshold
        self.less_false_min = 50
        self.less_false_max = 700
        self.blockSize = 11
        self.fvariable = 2.6
        self.max_radius = max_radius
        self.min_radius = min_radius
        # ---
        log_main.info(u'dp = %s', self.dp)
        log_main.info(u'dp – Inverse ratio of the accumulator resolution to the image resolution.')
        log_main.debug(u'For example, if dp=1 , the accumulator has the same resolution as the input image.')
        log_main.debug(u'If dp=2 , the accumulator has half as big width and height.')

        log_main.info(u'mindist = %s', self.minDist)
        log_main.info(u'mindist – Minimum distance between the centers of the detected circles.')
        log_main.debug(u'If the parameter is too small, multiple neighbor circles may be falsely detected ')
        log_main.debug(u'in addition to a true one.')
        log_main.debug(u'If it is too large, some circles may be missed.')

        log_main.info(u'higher_threshold = %s', self.higher_threshold)
        log_main.info(u'higher_threshold – First method-specific parameter. In case of CV_HOUGH_GRADIENT ,')
        log_main.info(u'it is the higher threshold of the two passed to the Canny() edge detector ')
        log_main.info(u'(the lower one is twice smaller)')

        log_main.info(u'less_false = %s', self.less_false)
        log_main.info(u'less_false – Second method-specific parameter. In case of CV_HOUGH_GRADIENT ,')
        log_main.info(u'it is the accumulator threshold for the circle centers at the detection stage.')
        log_main.debug(u'The smaller it is, the more false circles may be detected.')
        log_main.debug(u'Circles, corresponding to the larger accumulator values, will be returned first.')

        # ---
        log_main.info(u'blockSize = %s', self.blockSize)
        log_main.debug(u'blockSize − A variable of the integer type representing size of the pixelneighborhood used')
        log_main.debug(u' to calculate the threshold value.')
        log_main.info(u'C = %s', self.fvariable)
        log_main.debug(u'C − A variable of double type representing the constant used in the both methods ')
        log_main.debug(u'(subtracted from the mean or weighted mean).')

    def pickup_circles(self):
        """
        read frame from web-cam,
        convert to gray and black-white, try clear
        and pick-up circles from it
        :return:
        """
        ret, framer = self.cap.read()
        # print(type(frame))  # <type 'numpy.ndarray'>
        # img_size = frame.shape
        # print 'frame', img_size
        try:
            gray = cv.cvtColor(framer, cv.COLOR_BGR2GRAY)
            gray = cv.adaptiveThreshold(gray,
                                        255,
                                        cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv.THRESH_BINARY,
                                        self.blockSize,
                                        self.fvariable
                                        )
            kernel = np.ones((3, 3), np.uint8)
            gray = cv.erode(gray, kernel, iterations=1)
            # gray = erosion
            gray = cv.dilate(gray, kernel, iterations=1)
            # gray = dilation
            circles = cv.HoughCircles(gray,
                                      cv.cv.CV_HOUGH_GRADIENT,
                                      self.dp,
                                      self.minDist,
                                      param1=self.higher_threshold,
                                      param2=self.less_false,
                                      minRadius=self.min_radius,
                                      maxRadius=self.max_radius
                                      )
            log_main.debug(u'discovered circles: %s', circles)
        except:
            gray = None
            circles = None
        return circles, gray, framer

    def adopt_parametr2(self, circles_count=None):
        """
        adopt parametr of circle discover to situation (prev. discovered or not)
        :return:
        """
        if not circles_count:
            if self.less_false > self.less_false_min:
                self.less_false *= 0.9
                log_main.debug(u'(nothing discovered) adopt DOWN -- more probably false objects')
        else:
            # circles_count = len(circles[0])
            # print circles, '--->', circles_count
            if circles_count > 2 and self.less_false < self.less_false_max:
                if circles_count > 5:
                    self.less_false *= 2
                else:
                    self.less_false *= 1.1
                log_main.debug(u'(discovered more then two) adopt UP ++ less probably false objects')
        self.less_false = int(self.less_false)
        return None
