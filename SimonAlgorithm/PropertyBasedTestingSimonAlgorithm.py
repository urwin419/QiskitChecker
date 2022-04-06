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

#This line is the Lower bound of the length of the bitstring
b = int(lines[4].strip())   

#This line id the Upper bound of the length of the bitstring
c = int(lines[6].strip())

#This line indicates the Max Trial for each test
d = int(lines[8].strip())

#This line import the test mutant
mymodule = importlib.import_module(a)

#This function will generate a bit string for later tests.
#Note that the bitstring with all 0 will be removed as all 0 string 
#will always be a trivial solution to our problem
@st.composite
def draw_01s_for_simon(draw):
    m = []
    for i in range (b,c+1): 
        for numbers in itertools.product(["0", "1"], repeat=i):
            m.append(''.join(numbers))
        m.remove("0"*i)
    return draw(st.sampled_from(m))

#This test will check the number of valid output 
@given(draw_01s_for_simon())
@settings(deadline=None,max_examples=d)
def test_simon_number_of_output(bitstring):
    note("bitstring %s"%bitstring)
    result=mymodule.simon(bitstring)
    length = len(bitstring)
    results = result.keys()
    for k in results:
        if int(result[k])/10000 <= 0.01:
            results.remove(k)
    assert len(results) == 2**(length-1)
    f.write("\n##############Test Begin#################\n")
    f.write("The input string is "+bitstring+" and the length of string is "+str(length)+"\n")
    f.write(f"simon algorithm - result: {result}\n")
    f.write("The number of output is as expexted\n")
    f.write("###############Test End##################\n")

#This test will check the probability for each valid output
@given(draw_01s_for_simon())
@settings(deadline=None,max_examples=d)
def test_simon_output_probability_almost_equals(bitstring):
    note("bitstring %s"%bitstring)
    result=mymodule.simon(bitstring)
    length = len(bitstring)
    keys = result.keys()
    for key in keys:
        if int(result[key])/10000 >= 0.01:
            big = int(result[key])/10000 >= (1/(2**(length-1)))*0.8
            small =  int(result[key])/10000 <= (1/(2**(length-1)))*1.2
            assert big & small
    f.write("\n##############Test Begin#################\n")
    f.write("The input string is "+bitstring+" and the length of string is "+str(length)+"\n")
    f.write(f"Simon algorithm - result: {result}\n")
    f.write("Each output probability almost equals\n")
    f.write("###############Test End##################\n")

#This test will check the dotproduct for each valid output
@given(draw_01s_for_simon())
@settings(deadline=None,max_examples=d)
def test_simon_output_dotproduct_0(bitstring):
    note("bitstring %s"%bitstring)
    results=mymodule.simon(bitstring)
    length = len(bitstring)
    result = results.keys()
    m = []
    for k in result:
        if int(results[k])/10000 <= 0.01:
            result.remove(k)
    for resul in result:
        m.append(mymodule.dotp(bitstring, resul)) 
    assert m.count(0) >= len(m)/2 
    f.write("\n##############Test Begin#################\n")
    f.write("The input string is "+bitstring+" and the length of string is "+str(length)+"\n")
    f.write(f"Simon algorithm - result: {results}\n")
    f.write("The dotproduct results is as expected\n")
    f.write("###############Test End##################\n")


if __name__ == "__main__":

    #Open the result file ready to record
    f = open('result.txt','w')

    #Record the start time
    begintime = time()

    try:
        #Begin test
        test_simon_number_of_output()
        test_simon_output_probability_almost_equals()
        test_simon_output_dotproduct_0()

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
