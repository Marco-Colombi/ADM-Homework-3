# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 19:19:02 2019

@author: marco
"""

#We will use a recursive method to solve this question
def pr_func(strg):
    #The function func takes two strings and returns the length of the longest possible subsequence
    #that can be read in string1 and string 2
    def func(string1,string2):
        res=0
        if not string1 or not string2:
            res=0
        elif string1[-1] == string2[-1]:  
            #if the last letter in the two strings are equal we add 1 to the result plus our function applied on the substrings
            #(without considering the last letter). 
            res= (1 + func(string1[:-1],string2[:-1]))
        else:
            #if the last letter in the two strings are not equal we eliminate the last letter either of the first string
            #or the second string
            #We take the maximum because we're searching for the longest subsequence
            res=(max(func(string1[:-1],string2), func(string1,string2[:-1])))
        return(res)
    #we compute the reversed string of the input string
    reversed_strg=strg[::-1]
    #the result is our function applied to the input string and its reversed 
    return(func(strg,reversed_strg))
    
print(pr_func('dataminingsapienza'))