import hypothesis.strategies as st
from hypothesis import given, settings, note
from time import *
import importlib
import itertools
import os

#Input the test parameters from the testscriprt file
testscript = open ('testscript.txt','r')

#Input each line
lines = testscript.readlines()

#This line is the test mutant
a = lines[1].strip() 

#This line is the Number of qubits For test_BV_output_match_input
b = int(lines[4].strip())   

#This line is the Length of the bitstring For test_BV_output_match_input
c = int(lines[6].strip())

#This line is the Number of qubits For test_BV_output_probability
d = int(lines[9].strip())

#This line is the Length of the bitstring For test_BV_output_probability
e = int(lines[11].strip())

#This line indicates the Max Trial for each test
f = int(lines[13].strip())

#This line import the test mutant
mymodule = importlib.import_module(a)

#This function will generate a bit string for test_BV_output_match_input
@st.composite
def draw_01s_for_match(draw):
    m = []
    for numbers in itertools.product(["0", "1"], repeat=c):
        m.append(''.join(numbers))
    return draw(st.sampled_from(m))

#This function will generate a bit string for test_BV_output_probability
@st.composite
def draw_01s_for_probability(draw):
    m = []
    for numbers in itertools.product(["0", "1"], repeat=e):
        m.append(''.join(numbers))
    return draw(st.sampled_from(m))

#This test will check whether the output string matches the input string
@given(draw_01s_for_match())
@settings(deadline=None,max_examples=f)
def test_BV_output_match_input(bitstring):
    note("bitstring %str"%bitstring)
    result=mymodule.bernstein_azirani(bitstring, b)
    results=max(result.values())
    for k in result.keys():
        if result[k] == results:
            assert k == bitstring
            f.write("\n##############Test Begin#################\n")
            f.write("The input string is "+bitstring+" and the length of string is "+str(b)+"\n")
            f.write(f"Bernstein-Vazirani algorithm - result: {result}\n")
            f.write("The output string matches the input string\n")
            f.write("###############Test End##################\n")

#This test will check the probability of the correct output 
@given(draw_01s_for_probability())
@settings(deadline=None,max_examples=f)
def test_BV_output_probability(bitstring):
    note("bitstring %str"%bitstring)
    result=mymodule.bernstein_azirani(bitstring, d)
    assert int(result[bitstring])/1000 >= 0.99
    f.write("\n##############Test Begin#################\n")
    f.write("The input string is "+bitstring+" and the length of string is "+str(d)+"\n")
    f.write(f"Bernstein-Vazirani algorithm - result: {result}\n")
    f.write("The output probability satisfies the expected value\n")
    f.write("###############Test End##################\n")


if __name__ == "__main__":

    #Open the result file ready to record
    f = open('result.txt','w')

    #Record the start time
    begintime = time()

    try:
        #Begin test
        test_BV_output_match_input()
        test_BV_output_probability()

    finally:
        #Record the end time
        endtime = time()
        
        #Calculate the execution time
        runtime = float(endtime - begintime)*1000.0

        #Write the execution time to the result file and close the file
        runtim = str(round(runtime,2))
        f.write('\nThe test runs for '+ runtim + ' ms\n')
        f.close()

        #Open the file window ready for viewing
        os.system("result.txt")
