# programmingLaba1
A repository for submission of a lab

A module that creates html file - a map with closest and furthest locations where movies
were filmed when year, coordinates and path to a file given.

A file with 1000+ films for checking correctness of the code is attached.
Doctests rely on that file too - to check doctests you should download the file too.

Map contains 3 layers:
  first layer - all films from a given year (blue marks)
  second layer - 10 closest filming locations from a given year (darkpyrple marks)
  third layer - 10 furthest filming locations from a given year (red marks)
  
  Each mark contains a film name, coordinates and a location: ![Знімок екрана 2022-02-08 о 10 45 39](https://user-images.githubusercontent.com/92575094/152950611-17da3243-de54-4082-b09c-5f4af8e33fe7.png)

Launching from the command line supported:
argparse requires 4 arguments: year, latitude, longtitude, path to a file
>>> python main.py 2009 40 43 movieshere

This launching will create a file 'filmsmap.html'
Example of running this file: ![Знімок екрана 2022-02-08 о 10 55 13](https://user-images.githubusercontent.com/92575094/152952113-41e9278a-7403-4265-82ec-54947e3c7bea.png)
