# programmingLaba1
A repository for submitting a lab

A module that creates HTML file - a map with closest and furthest locations where movies
were filmed when year, coordinates, and path to a file given.

A file with 1000+ films for checking the correctness of the code is attached.
Doctests rely on that file - to check doctests, you should download the file.
 
The map contains 3 layers:
  first layer - all films from a given year (blue marks);
  second layer - 10 closest filming locations from a given year (dark purple marks);
  third layer - 10 furthest filming locations from a given year (red marks).
  
  Each mark contains a film name, coordinates, and a location: ![Знімок екрана 2022-02-08 о 10 45 39](https://user-images.githubusercontent.com/92575094/152950611-17da3243-de54-4082-b09c-5f4af8e33fe7.png)

Launching from the command line is supported:
argparse requires 4 arguments: year, latitude, longitude, the path to a file
>>> python main.py 2009 40 43 movieshere

This launching will create a file 'filmsmap.html'.
Example of running this file: ![Знімок екрана 2022-02-08 о 10 55 13](https://user-images.githubusercontent.com/92575094/152952113-41e9278a-7403-4265-82ec-54947e3c7bea.png)

The approximate work time needed for a program with this input is 30 seconds.
