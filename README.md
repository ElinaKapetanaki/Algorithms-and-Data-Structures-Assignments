# Algorithms and Data Structures Assignments

In the framework of the Algorithms and Data Structures class the following algorithms were implemented using the programming language Python:


## Commentz - Walter String Matching
The Commentz-Walter string matching algorithm that matches and reports the position of multiple strings in a text efficiently using the data structure trie / prefix tree. <br><br>
 Use the following command to run the program from cmd (where -v is optional for verbose output and kw is for the keywords you want to match in the text)
```
python commentz_walter.py [-v] kw [kw...] input_filename
```
Read the full discription [here](https://github.com/dmst-algorithms-course/assignment-2023-3/blob/main/assignment-2023-3.pdf).

## Interval Graphs 
An algorithm that checks whether a graph is a chordal graph and whether it is an interval graph, using Lexicographic Breadth First Search (LexBFS) and Asteroidal Triple-Free (AT-free) check. <br><br>
 Use the following command to run the program from cmd (where task options are: lexbfs, chordal, interval)
```
python interval_graphs.py task input_filename
```
Read the full discription [here](https://github.com/dmst-algorithms-course/assignment-2023-2/blob/main/assignment-2023-2.pdf).

## Lance Williams Clustering
A hierarchical clustering algorithm using the Lance-Williams formula for calculating the distance between clusters. <br> <br>
 Use the following command to run the program from cmd (where clustering method options are: single, complete, average, ward)
```
python lance_williams.py clustering_method input_filename
```
Read the full discription [here](https://github.com/dmst-algorithms-course/assignment-2023-1/blob/main/assignment-2023-1.pdf).
