Założenia i rozwiązanie
=======================

Zadanie zostało rozwiązane na dorosłym komputerze z systemem Linux,
po czym przystosowane do posiadanejplatformy RaspberryPi.

Program pobiera obraz z kamery, przetwarza go na czarno-biały, wyszukuje okręgów i zwraca wynik:

#. włączając diodę LED,
#. ukazując okienko z obrazem i nadrukiem okręgu oraz cyfrowym przedstawieniem współrzędnych środka w pixelach (jeśli włączone)
#. wpis do logu o tym fakcie wraz ze współrzędnymi środka

Program przy każdej analzowanej klatce obrazu dokonuje adaptacji do treści obrazu.

Zauważyłem, że trudno jest dobraż stałe parametry, odpowiadające każdej z sytuacji - markerowi na kartce
lub losowemu obrazowi. Metodą prób i błędów dobrałem większość współczynników, zaś jeden z nich
jest dobierany dynamicznie w zależności od tego co zostało wcześniej wykryte.
Ten współczynnik to **less_false** jak czytamy w dokumentacji:

less_false – Second method-specific parameter. In case of CV_HOUGH_GRADIENT ,
it is the accumulator threshold for the circle centers at the detection stage.
The smaller it is, the more false circles may be detected.
Circles, corresponding to the larger accumulator values, will be returned first.

Niestety wykrywanie jest obarczone błędami.
Próbowałem ich uniknąć w ten sposób, aby zapisywać wykryte okręgi do tymczasowej tabeli w bazie danych (SQLite3)
a następnie sprawdzać powtarzalność wyników z pewną tolerancją.

Baza danych jest przechowywana w pamięci (szybkość), ale do celów debugu można ją zachować w pliku
- przekomentowanie około linii 13 w **db.py**.

Baza danych ma ponadto tabelę key-value, która umożliwia przechowywanie par klucz wartość i dzięki temu
(gdy debugowana) -podgląd tego co się dzieje.

Przy maszynach bardziej wydajnych niż RPi, łatwo można użyć bazy np MySQL i pracę oraz parametry przedstawiać w locie
używając np. mechanizmów AngularJS.


Wykrycie okręgów na kartce -na obrazie oryginalnym:


   .. image:: _static/img/1_final.png
      :scale: 100 %
      :alt: Wykrycie okręgów na kartce
      :align: center


- na obrazie czarno -białym:


   .. image:: _static/img/1_proc.png
      :scale: 100 %
      :alt: Wykrycie okręgów na kartce
      :align: center


Uruchomienie programu:
----------------------

Przed uruchomieniem należy podłączyć kamerę do USB (i mieć zainstalowane jej sterowniki).
Folder wewnętrzny log musi być zapisywalny przez program Pythona.

   .. code-block:: python

            pi@raspberrypi:~/Desktop/py_rpi $ python __init__.py

Działanie programu:

   .. code-block:: python

            pi@raspberrypi:~/Desktop/py_rpi $ python __init__.py
            /home/pi/Desktop/py_rpi/main.py:16: RuntimeWarning: This channel is already in use, continuing anyway.  Use GPIO.setwarnings(False) to disable warnings.
              GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)
            2018-10-04 19:44:15.822  INFO      log              dp = 2
            2018-10-04 19:44:15.852  INFO      log              dp – Inverse ratio of the accumulator resolution to the image resolution.
            2018-10-04 19:44:15.875  INFO      log              mindist = 100
            2018-10-04 19:44:15.887  INFO      log              mindist – Minimum distance between the centers of the detected circles.
            2018-10-04 19:44:15.901  INFO      log              higher_threshold = 1520
            2018-10-04 19:44:15.922  INFO      log              higher_threshold – First method-specific parameter. In case of CV_HOUGH_GRADIENT ,
            2018-10-04 19:44:15.928  INFO      log              it is the higher threshold of the two passed to the Canny() edge detector
            2018-10-04 19:44:15.957  INFO      log              (the lower one is twice smaller)
            2018-10-04 19:44:15.963  INFO      log              less_false = 150
            2018-10-04 19:44:15.974  INFO      log              less_false – Second method-specific parameter. In case of CV_HOUGH_GRADIENT ,
            2018-10-04 19:44:16.001  INFO      log              it is the accumulator threshold for the circle centers at the detection stage.
            2018-10-04 19:44:16.015  INFO      log              blockSize = 11
            2018-10-04 19:44:16.025  INFO      log              C = 2.6
            2018-10-04 19:44:19.665  INFO      log              calculate, depend of video-size:
            2018-10-04 19:44:19.672  INFO      log              min_radius  = 43
            2018-10-04 19:44:19.679  INFO      log              max_radius  = 218
            2018-10-04 19:44:19.697  INFO      log              how many loops will be stored id DB: 10
            2018-10-04 19:44:19.715  INFO      log              how many hits to confirm: 8
            2018-10-04 19:44:20.742  INFO      log              LED-OFF
            2018-10-04 19:44:31.769  INFO      log              LED-ON:
            2018-10-04 19:44:31.780  INFO      log              circle X: 439, Y: 235, R: 89
            2018-10-04 19:44:44.131  INFO      log              LED-OFF

Wykrycie okręgu (potwierdzonego wymaganą ilość razy) spowoduje zapis w logu (powyżej)
oraz zapalenie diody i ukazanie obrazu z nadrukiem.

Można wyłączyć obraz (obraz procesowania), ustawiając wartości '0' w miejsce '1' dla kluczy
'show_processing' i 'show_gotit' około linii 60 pliku main.py.

Podobnie można zmieniać wartości zmiennych procesu zamiany kolorowego obrazu na czarno-biały oraz wykrywania okręgów.

