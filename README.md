QiskitChecker
================
QiskitChecker is a property-based testing frame for quantum programs in Qiskit. It is capable of generating random inputs and testing the pre-chosen properties automatically.

QiskitChecker is developed in Python and below I will provide a brief introduction on how to install the environment and how to execute the tests.

Environment Installation
============
Qiskit supports Python 3.7 and later.Anaconda is recommanded for version management and and interacting with Qiskit.

The installation guide for Qiskit can be found on:
https://qiskit.org/documentation/getting_started.html

How to run the tests
===========
QiskitChecker includes three algorithms under test. They are the Deutsch-Jozsa Algorithm, the Bernstein-Vazirani Algorithm and the Simon's Algorithm. The algorithm themselves and the property-based tests are already written in each folder. You can simply execute the tests via command line by:
```python PropertyBasedTestingForDeutschJozsaAlgorithm.py```

```python PropertyBasedTestingBernsteinVaziraniAlgorithm.py```

```python PropertyBasedTestingSimonAlgorithm.py```

And the test result will be written into the result.txt file for future inspection.

How to customise the tests
=============
The mutant used and the test parameters are pre-defined in testscript.txt file in each folder. Parameters inside the file can be changed to build your own tests. Mutants are algorithm code with slight changes. Most of them will report error when testing. 
