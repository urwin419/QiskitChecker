import hypothesis.strategies as st
from hypothesis import given, settings, note
from time import *
import importlib
import os

#Input the test parameters from the testscriprt file
testscript = open ('testscript.txt','r')

#Input each line 
lines = testscript.readlines()

#This line is the Lower bound For test_DJ_balanced_input_length_equal_to_output 
a = lines[4].strip()   

#This line is the Upper bound For test_DJ_balanced_input_length_equal_to_output 
b = lines[6].strip()   

#This line is the Lower bound For test_DJ_balanced_result_contains_no_0s
c = lines[9].strip()

#This line is the Upper bound For test_DJ_balanced_result_contains_no_0s
d = lines[11].strip()

#This line is the Lower bound For test_DJ_constant_input_length_equal_to_output
e = lines[14].strip()

#This line is the Upper bound For test_DJ_constant_input_length_equal_to_output
f = lines[16].strip()

#This line is the Low bound For test_DJ_constant_result_contains_no_1s
g = lines[19].strip()

#This line is the Upper bound For test_DJ_constant_result_contains_no_1s
h = lines[21].strip()

#This line is the test mutant
i = lines[1].strip()

#This line is the Max Trial for each test
j = lines[33].strip()

#This line is the Low bound For test_DJ_balanced_probability
o = lines[29].strip()

#This line is the Upper bound For test_DJ_balanced_probability
p = lines[31].strip()

#This line is the Low bound For test_DJ_constant_probability
r = lines[24].strip()

#This line is the Upper bound For test_DJ_constant_probability
s = lines[26].strip()

#This line import the test mutant
mymodule = importlib.import_module(i)

#This test will check the output in constant mode 
@given(st.integers(min_value= int(g), max_value= int(h)))
@settings(deadline=None,max_examples=int(j))
def test_DJ_constant_result_contains_no_1s(leng):
    note("leng %i"%leng)
    result=mymodule.deutsch_jozsa('constant', leng)
    results=max(result.values())
    for k in result.keys():
        if result[k] == results:
            assert "1" not in k
            f.write("\n##############Test Begin#################\n")
            f.write("The problem space is "+str(leng)+" and in constant mode\n")
            f.write(f"Deutsch Jozsa - Constant Oracle: {result}\n")
            f.write("There is no 1s in the result for 1000 shots\n")
            f.write("##############Test End#################\n")

#This test will check the output length in constant mode 
@given(st.integers(min_value= int(e), max_value= int(f)))
@settings(deadline=None,max_examples=int(j))
def test_DJ_constant_input_length_equal_to_output(leng):
    note("leng %i"%leng)
    result=mymodule.deutsch_jozsa('constant', leng)
    assert "0"*leng in result.keys()
    f.write("\n##############Test Begin#################\n")
    f.write("The problem space is "+str(leng)+" and in constant mode\n")
    f.write(f"Deutsch Jozsa - Constant Oracle: {result}\n")
    f.write("The output length is equal to the input length\n")
    f.write("###############Test End##################\n")

#This test will check the output in balanced mode 
@given(st.integers(min_value= int(c), max_value= int(d)))
@settings(deadline=None,max_examples=int(j))
def test_DJ_balanced_result_contains_no_0s(leng):
    note("leng %i"%leng)
    result=mymodule.deutsch_jozsa('balanced', leng)
    results=max(result.values())
    for k in result.keys():
        if result[k] == results:
            assert "0" not in k
            f.write("\n##############Test Begin#################\n")
            f.write("The problem space is "+str(leng)+" and in balanced mode\n")
            f.write(f"Deutsch Jozsa - balanced Oracle: {result}\n")
            f.write("There is no 0s in the result for 1000 shots\n")
            f.write("##############Test End#################\n")

#This test will check the output length in balanced mode 
@given(st.integers(min_value= int(a) , max_value= int(b)))
@settings(deadline=None,max_examples=int(j))
def test_DJ_balanced_input_length_equal_to_output(leng):
    note("leng %i"%leng)
    result=mymodule.deutsch_jozsa('balanced', leng)
    assert "1"*leng in result.keys()
    f.write("\n##############Test Begin#################\n")
    f.write("The problem space is "+str(leng)+" and in balanced mode\n")
    f.write(f"Deutsch Jozsa - balanced Oracle: {result}\n")
    f.write("The output length is equal to the input length\n")
    f.write("###############Test End##################\n")

#This test will check the probability of output in balanced mode 
@given(st.integers(min_value= int(o) , max_value= int(p)))
@settings(deadline=None,max_examples=int(j))
def test_DJ_balanced_probability(leng):
    note("leng %i"%leng)
    result=mymodule.deutsch_jozsa('balanced', leng)
    assert int(result["1"*leng])/1000 >= 0.99
    f.write("\n##############Test Begin#################\n")
    f.write("The problem space is "+str(leng)+" and in balanced mode\n")
    f.write(f"Deutsch Jozsa - balanced Oracle: {result}\n")
    f.write("The output probability satisfies the expected value\n")
    f.write("###############Test End##################\n")

#This test will check the probability of output in constant mode 
@given(st.integers(min_value= int(r) , max_value= int(s)))
@settings(deadline=None,max_examples=int(j))
def test_DJ_constant_probability(leng):
    note("leng %i"%leng)
    result=mymodule.deutsch_jozsa('constant', leng)
    assert int(result["0"*leng])/1000 >= 0.99
    f.write("\n##############Test Begin#################\n")
    f.write("The problem space is "+str(leng)+" and in constant mode\n")
    f.write(f"Deutsch Jozsa - constant Oracle: {result}\n")
    f.write("The output probability satisfies the expected value\n")
    f.write("###############Test End##################\n")


if __name__ == "__main__":
    
    #Open the result file ready to record
    f = open('result.txt','w')

    #Record the start time
    begintime = time()

    try:
        #Begin test
        test_DJ_constant_result_contains_no_1s()
        test_DJ_constant_input_length_equal_to_output()
        test_DJ_constant_probability()
        test_DJ_balanced_result_contains_no_0s()
        test_DJ_balanced_input_length_equal_to_output()
        test_DJ_balanced_probability()

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