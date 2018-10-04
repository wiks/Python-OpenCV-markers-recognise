Zadanie i sprzęt
================

Przesyłam zadanie.
------------------

Proszę wykonać na Raspberry Pi aplikację do przetwarzania obrazu (może być z użyciem kamerki internetowej
i biblioteki OpenCV), która służyłaby do wykrywania na obrazie obecność okrągłych markerów
(mogą być np. wydrukowane na kartce papieru) i podawała ich pozycję (w pikselach) na obrazie.
Dodatkowo fakt, że jakikolwiek marker pojawił się na obrazie powinien być zasygnalizowany sprzętowo
np. za pomocą zapalenia diody LED.

Sprzęt i oprogramowanie
=======================

RaspberryPi 2
-------------

OS - Raspbian GNU/Linux 9

   .. code-block:: python

        Python 2.7.13 (default, Jan 19 2017, 14:48:08)

        [GCC 6.3.0 20170124] on linux2

        >>> import cv2

        >>> cv2.__version__

        '2.4.9.1'


Python -moduły
--------------

Praktycznie to co po instalacji systemu, plus OpenCV2 i drivery web-kamery:

   .. code-block:: python

        pi@raspberrypi:~ $ sudo pip freeze
        automationhat==0.0.4
        backports.shutil-get-terminal-size==1.0.0
        blinker==1.3
        blinkt==0.1.0
        Cap1xxx==0.1.3
        chardet==2.3.0
        click==6.6
        colorama==0.3.7
        cryptography==1.7.1
        decorator==4.0.11
        drumhat==0.0.5
        enum34==1.1.6
        envirophat==0.0.6
        ExplorerHAT==0.4.2
        Flask==0.12.1
        fourletterphat==0.0.2
        gpiozero==1.4.0
        idna==2.2
        ipaddress==1.0.17
        ipython==5.1.0
        ipython-genutils==0.1.0
        itsdangerous==0.24
        Jinja2==2.8
        keyring==10.1
        keyrings.alt==1.3
        lxkeymap==0.1
        MarkupSafe==0.23
        mcpi==0.1.1
        microdotphat==0.1.3
        mote==0.0.3
        motephat==0.0.2
        numpy==1.12.1
        oauthlib==2.0.1
        pathlib2==2.1.0
        pexpect==4.2.1
        phatbeat==0.0.2
        pianohat==0.0.5
        picamera==1.13
        pickleshare==0.7.4
        picraft==1.0
        piglow==1.2.4
        pigpio==1.38
        Pillow==4.0.0
        prompt-toolkit==1.0.9
        ptyprocess==0.5.1
        pyasn1==0.1.9
        pycrypto==2.6.1
        pygame==1.9.3
        Pygments==2.2.0
        pygobject==3.22.0
        pyinotify==0.9.6
        PyJWT==1.4.2
        pyOpenSSL==16.2.0
        pyserial==3.2.1
        pyxdg==0.25
        rainbowhat==0.0.2
        requests==2.12.4
        requests-oauthlib==0.7.0
        RPi.GPIO==0.6.3
        RTIMULib==7.2.1
        scipy==0.18.1
        scrollphat==0.0.7
        scrollphathd==1.0.1
        SecretStorage==2.3.1
        sense-emu==1.0
        sense-hat==2.2.0
        simplegeneric==0.8.1
        simplejson==3.10.0
        six==1.10.0
        skywriter==0.0.7
        sn3218==1.2.7
        spidev==3.3
        touchphat==0.0.1
        traitlets==4.3.1
        twython==3.4.0
        urllib3==1.19.1
        wcwidth==0.1.7
        Werkzeug==0.11.15

WebCam
------

Użyta kamera: Microsoft Webcam Lifecam HD3000 (podobna do: https://dealshabibi.com/product/microsoft-webcam-lifecam-hd3000/ )

GPIO
----

Użyta jako BCM, pin 23 jako wyjście, LED-ON gdy stan wysoki. Podłączona LED z rezystorem 1kOhm.

Użycie:
-------

Raspberry Pi obsługiwana przez VNC.

