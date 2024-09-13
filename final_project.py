#!/usr/bin/env python3
# # -*- coding: utf-8 -*-
"""cryptarithmetic puzzles"""
__author__="Toan Ngo"

import sys
import random
#//////////////////operation call function///////////////////////////////////////////////////////

def number_choice(valid, rectric):                 #pick number in the valid list with the exception of any number that are in the restrictions(resic) list are excluded 
    if((len(valid)!=0) and (len(rectric)!=len(valid))):
        number_pick=random.choice([val for val in valid if val not in rectric] )  #good can only select number that are valid with resiction place ontop 
        return number_pick
    else:
        return "no more number left"

def session_reset(input, input2,result, main_dict,current_index):
    #get the letter in the list current session and reset them 
    first_value=input                #A:45
    second_value=input2
    if(first_value!=second_value):
        main_dict.update({first_value:[]})
        main_dict.update({second_value:[]})
        main_dict.update({result:[]})
    else:
        main_dict.update({first_value:[]})
        main_dict.update({result:[]})

def resiction_add (input, input2,result, main_dict,current_index,value,resiction,carry):     #this should populate the main dict with value and if the value already exist do nothing 
    first_value=input
    second_value=input2
    number_generation=value
    packet=check_valid_input(first_value,second_value,main_dict,current_index,number_generation)        #call and check if the number valid 
    if(first_value==second_value):
        
        if((packet[2]==True) ):      #if boths number leter are the same applaying one number genration
            if(result_check(result,main_dict,value,carry)):
                    main_dict[first_value].append(number_generation)
                    return "added both"
            else:
                return"cant be added"
      
    else:   #they are not the same letter 
            if((packet[0]==True) and (packet[1]==False)):        #if value 1 is empty 
                if(result_check(result,main_dict,value,carry)):
                        main_dict.update({first_value:[number_generation]})           #repace the current value with new value
                        return "added 1"
                else:
                    return"cant be added"
            elif((packet[1]==True and packet[0]==False) ):
                if(result_check(result,main_dict,value,carry)):
                    main_dict.update({second_value:[number_generation]})
                    return "added 2"
                else:
                    return"cant be added"
            else:   #both case are true but difference value
                if((packet[0] == True) and (packet[1]== True) and (packet[2]==False)):
                    if(result_check(result,main_dict,value,carry)):
                        main_dict.update({first_value:[number_generation]})
                        main_dict.update({second_value:[number_generation]})
                        return "added 1 and 2"
                    else:
                        return"cant be added"
                elif((packet[0] == False) and (packet[1]== False) and (packet[2]==False)):
                    if(result_check(result,main_dict,value,carry)):
                        main_dict.update({first_value:[number_generation]})
                else:                                                       #case where all false meaning a number already exist in the letter 
                    return "cant be added"
            return "cant be added"

def overwrite(input, input2, main_dict,value, resiction):
    if(value not in resiction):
        main_dict[input]=[value]
        main_dict[input2]=[value]
        return True
    else:
        return False
    
def result_check(result,diction,value,carry):
    if (diction[result]==[]):
            return True
    elif((diction[result][0]==((value+value+1)%10)) and (len(carry)>0)):
            return True
    elif(diction[result][0]==((value+value)%10) and (len(carry)==0)):
            return True
    else:
        return False
    
def check_valid_input(input, input2, main_dict,current_index, Number_check):
    first_value=input
    second_value=input2
    packet=False
    packet1=False 
    packet2=False
    both=False  
    if(first_value==second_value):                              #both value are the same
        if(main_dict[first_value]==[] ):
            both=True
    elif(main_dict[second_value]==[] or main_dict[first_value]==[]):    #either one are true but not both are false 
        if(main_dict[second_value]==[]):
            packet2=True
        else:
            packet1=True
    else:
        packet=False
    return (packet1,packet2,both)

def check_sum_valid(sample_dict,letter,value,resiction,carry_over,compare):
    sample_list=[value for key in sample_dict.items() for value in key] #pupulate the list 
    #value ou want to check 
    #filter 
    indexs=sample_list.index(letter)
    track=sample_list[indexs+1]     #track should now have all the value contain in the letter o:[1231]

    if((((value % 10) in track) or ((value%10) in resiction)) and (compare ==False)):
        #this value already exist or there already value in the dict that map the leater 
        return False
    else:
        return True

def new_resic(sample_dict,resic):
    sample_list=[value for key in sample_dict.items() for value in key]
    counter=0
    resic.clear()
    for i in sample_list:
        if (counter % 2!=0):
            if(i!=[]):
                resic.append(i[0])
                counter+=1
            else:
                counter+=1
        else:
            counter+=1

def sum_test(x,y):
    X=lambda :x+y
    return X

def sum_added(sample_dict,letter,value,carry_over,run):
    if(len(carry_over)!=0 and run==True):

        sample_dict[letter]=[(value%10)+carry_over[0]]
        carry_over.pop()
    else:
        sample_dict[letter]=[value%10]

def get_value_result(input, input2,main_dict,current_index):                        #this code got replace by by sum-add method because this applying to multiple diffrence letter adding together 
    get_val=main_dict[input][0]                                                      #while sum add is applying work because the letter are the same, this should work for any letter that passing to it
    get_val2=main_dict[input2][0]
    result=sum_test(get_val,get_val2)
    return result()

def roll_back(input ,input2,result ,main_dict,current_index,current_re):
    letter_value=input[current_index+1]
    letter_value2=input2[current_index+1]
    result1=result[current_re+1]
    get_value=main_dict[letter_value]
    session_reset(letter_value,letter_value2,result1,main_dict,current_index)           #reset the stage 
    
    #roll back prev stage
    return get_value

#////////////////////////////////////////////worker function//////////////////////////////////////////////////////////////// 

def main_funct(input, input2,result_words,main_dict,bad_set,user_input):
    #set up counter
    current_index=len(input)-1
    current_result=len(result_words)-1
    valid=[1,2,3,4,5,6,7,8,9]
    resic=[]                 #this is a bad set of a selective character 
    carry_over=[]
    runback=False
    run=False
    compare=False
    leading=False
    while ((current_result !=-1) and (current_index !=-1)):
        
        letter_equation=input[current_index]
        letter_equation2=input2[current_index]
        letter_result=result_words[current_result]
      
        if(user_input != ""):                       #user_input hendle
            check=resiction_add(letter_equation,letter_equation2,letter_result,main_dict,current_index,user_input,resic,carry_over)
           
            resic.append(user_input)
          
            if(check=="added both"):
               
                sum=sum_test((main_dict[letter_equation])[0],(main_dict[letter_equation2])[0])
                #print(f"this is check: {sum()}")
                if(sum()>=10):
                    carry_over.append(int(str(sum())[:1]))
                    leading=True
    
                if(check_sum_valid(main_dict,letter_result,sum(),resic,carry_over,compare)):
          
                    sum_added(main_dict,letter_result,sum(),carry_over,run)
                    run=True
                    resic.append(sum()%10)
            user_input=""                                               #user now has its value extracted and its containner are now empty 
            #print(main_dict)
            current_result-=1
            current_index-=1

        else:                                                                       #normal run 
            
            number_get=number_choice(valid,resic)
            if (number_get!="no more number left"):
                check=resiction_add(letter_equation,letter_equation2,letter_result,main_dict,current_index,number_get,resic,carry_over)
            capture=resic
            while(check=="cant be added"):
                if(runback==False):
                    resic.append(number_get)
                
                    number_get=number_choice(valid,resic)
                    if(number_get=="no more number left"):
                        #back track part/roll back
                        #runback=True
                        number_result_change=roll_back(input,input2,result_words,main_dict,current_index,current_result)
                        new_resic(main_dict,resic)
                        resic.append(number_result_change[0])
                        current_index+=1
                        current_result+=1
                        letter_equation=input[current_index]            #moving back 
                        letter_equation2=input2[current_index]
                        letter_result=result_words[current_result]
                    
                        track=number_result_change[0]                   #generate a number that other than the last value in that letter
                        number_get=number_choice(valid,resic)
                        if(track<=5):                                   #separate number generation in two part 
                            while(int(number_get)<=int(track)):         #part1 if the prev letter number value are less than 5, generate a number that is in between 6-9 with the resiction place on each number that it cant be generate again after it has happen 
                                number_get=number_choice(valid,resic)
                                resic.append(number_get)
                                if(number_get=="no more number left"):
                                    resic=capture
                        elif(track>=5):                                 #part2 if the prev letter number value are greater than 5, generate a number that is between 1-4 with the resiction place on each number that it cant be generate again after it has happen
                            while(int(number_get)>=int(track)):
                                number_get=number_choice(valid,resic)
                                resic.append(number_get)
                                if(number_get=="no more number left"):
                                    resic=capture
                        sample=resic.pop()                              
                        resic=capture.append(sample)                                #this is a sceenshot of the prev verstion of the resicted list before the modification but now with the new value append to it 
                        if(number_get<=5 and len(carry_over)!=0 and leading==False):        #this is tracking if the leading number/ user input are a double or not when sum together
                            carry_over.clear()
                        elif(leading==True):
                            carry_over.clear()
                            carry_over.append(1)
                        check=resiction_add(letter_equation,letter_equation2,letter_result,main_dict,current_index,number_get,resic,carry_over)
                        #print(main_dict)
                    else:
                   
                        check=resiction_add(letter_equation,letter_equation2,letter_result,main_dict,current_index,number_get,resic,carry_over)
                        
               # else:
                #    number_get=number_choice(valid,resic)
                #    check=resiction_add(letter_equation,letter_equation2,letter_result,main_dict,current_index,number_get,resic,carry_over)
                #    runback=False

                    

            
           
            if(main_dict[letter_equation]!=[]):        
                sum=sum_test((main_dict[letter_equation])[0],(main_dict[letter_equation2])[0])
            #print(main_dict)
            resic=capture
            if(main_dict[letter_result]!=[]):                           #this is check if the current letter of sum are epmty or not if not then put in Comparison mode if not just add the value together in the next part
              
                compare=True
            if(len(carry_over)>=1):
                    run=True
            if(check_sum_valid(main_dict,letter_result,sum(),resic,carry_over,compare)):        #check if the sum that we get are valid or not
               
                sum_added(main_dict,letter_result,sum(),carry_over,run)
                if(sum()>=10):
                    carry_over.append(int(str(sum())[:1]))
                resic.append(sum()%10)
                resic.append(number_get)
                current_result-=1
                current_index-=1 
                compare=False 
                #runback=False
                run=False
                #print(main_dict)
            else:  
                
                while True:                                           #this entire loop is for when the summazion of the prev step fail the check if sum valid or not 
                    resic.append(number_get)                         #this loop is responsible for generation a new value for the letter and try and sum them up to pass the sum vail test                                                     
                    number_get=number_choice(valid,resic)  #number generation in this loop also have a resiction place on them and that is once a numbe has been generate and operation has been done and fail that number
                    #print(main_dict)
                    if(number_get=="no more number left"): #will not be in the poll of number that it can generate any more same with the rest of this number generation
                        resic=resic[:4]
                        number_get=number_choice(valid,resic)
                    if(number_get<=5 and leading==False):
                        carry_over.clear()
                    elif(number_get<=5 and leading==True):
                        carry_over.clear()
                        carry_over.append(1)
                    check=overwrite(letter_equation,letter_equation2,main_dict,number_get,resic)
                   
                    if(check):
                        sum=sum_test((main_dict[letter_equation])[0],(main_dict[letter_equation2])[0])
                        if(sum()>=10):
                            carry_over.append(int(str(sum())[:1]))
                            run=False
                        if(leading==True):
                            run=True
                        if(check_sum_valid(main_dict,letter_result,sum(),resic,carry_over,compare)):
                            sum_added(main_dict,letter_result,sum(),carry_over,run)
                            resic.append(sum()%10)
                            #print(main_dict)
                            break
                    else:
                        resic.append(number_get)
                current_result-=1
                current_index-=1                                                       #update the valid list
                #print(main_dict)



        
    if((current_result!=-1) and (current_index ==-1)):      #final letter get
        letter_result=result_words[current_result]
        current_result-=1
        total_carry=0
        while(len(carry_over)!=0 and (total_carry<=1)):         #edge case check
            total_carry+=int(carry_over.pop())
            #print(main_dict)
        if(total_carry!=0):
            main_dict[letter_result]=[1+total_carry]
            #print(main_dict)
        else:
            main_dict[letter_result]=[1]
            #print(main_dict)
        
#///////////////////////////////////////main area for output and helper///////////////////////////////////////////////////////////////////

def helper():
    print(f"This is a cryptarithmetic puzzles solver\nPlease enter the input from the range [1-9] in the command line along side with the program name,\nFor example: python crp.py 1")
    print(f"what you should be expecting when running this is, the program will compute and outputting the answers number for each letter in the following format")
    print("  [t]+[w]+[o]\n  [t]+[w]+[o]\n[f] [o] [u] [r]")
    #print("four")

def starting_and_out(user_input):
    first_equation=["t","w","o"]
    second_equation=["t","w","o"]
    result_words=["f","o","u","r"]
    main_dict={"t":[],"w":[],"o":[],"f":[],"u":[],"r":[]}
    bad_set={"t":[],"w":[],"o":[],"f":[],"u":[],"r":[]}
    user_input_int=user_input
    print(f"This is the number that you enter: {user_input_int}\n")
    print(f"this is the output")
    extract=main_funct(first_equation,second_equation,result_words,main_dict,bad_set,user_input_int)
    while(main_dict['t']==main_dict['w'] or main_dict['t']==[] or main_dict["w"]==main_dict["u"]  or main_dict["u"]==main_dict["o"]):
        main_dict={"t":[],"w":[],"o":[],"f":[],"u":[],"r":[]}
        extract=main_funct(first_equation,second_equation,result_words,main_dict,bad_set,user_input)
    #return main_dict
    print(f"    {main_dict['t']}+{main_dict['w']}+{main_dict['o']}\n    {main_dict['t']}+{main_dict['w']}+{main_dict['o']}\n{main_dict['f']} {main_dict['o']} {main_dict['u']} {main_dict['r']}")

#////////////////////////////////////user side input handle//////////////////////////////////////////////////////////////////////
if __name__=="__main__":
    user_input="".join(sys.argv[1])
    if((user_input.upper().strip()=="help".upper())):       #helper call
        helper()

    elif(user_input.isdigit()):                             #main function call
        if(user_input[:1]!="0"):
            user_packet=int(user_input[:1].strip())
            extracted_value=starting_and_out(user_packet)
        else:
            print("invalid number")
    else:
        print("please only input one number from the range [1-9] without any other characters")

#note: if you want to see how are the main dictionary are modify each iteration, please uncomments all the print(main_dict) in the program


    
     
