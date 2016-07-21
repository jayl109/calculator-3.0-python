def calculator(equation):
   
    math={"+": lambda x,y: x+y, "-": lambda x,y: x-y, "/": lambda x,y:x/y, "*": lambda x,y:x*y}
    numbers=[]
    
    operations=[]
    todo=str(equation)
    print (todo+"is what you entered")
    toadd=0.0
    state="number"
    index=0
    decimalstate=False
     #removes parentheses
    while "(" in todo:
        todo=str(removeparentheses(todo))
    if todo=="error":
        return "error"
    decimalindex=1 
    
    for x in todo:
        if x in math:
            if state=="oper":
                return("error")
            operations.append(x)
            numbers.append(toadd)
            decimalindex=1
            toadd=0.0
            state="oper"
            decimalstate=False
        elif x.isdigit():
            if decimalstate==True:
                toadd=toadd+float(x)*10**-decimalindex
                decimalindex+=1
            else:    
                toadd=toadd*10+float(x)
                state="number"
        elif x==".":
            decimalstate=True
        else:
            return todo
        if index==len(todo)-1:
            numbers.append(toadd)
        index+=1    
    index=0
    
    
    
    while index < len(operations): #do multiplication/division
        if operations[index]== "*" or operations[index]=="/":
            numbers[index]=math[operations[index]](numbers[index], numbers[index+1])
            del numbers[index+1]
            del operations[index]
        else:
            index+=1
    while not (len(operations) == 0): #do addition/subtraction
        numbers[0]=math[operations[0]](numbers[0], numbers[1])
        del numbers[1]
        del operations[0]
    return numbers[0]


def removeparentheses(todo): #returns new string with the parentheses removed
    for x in range (0, len(todo)):#find first parentheses 
        if todo[x]=="(":
            index1=x
            if str(findparentheses(todo, x)).isdigit():
                index2=findparentheses(todo,x)
                temporary=todo[index1+1:index2]
                newvalue=calculator(temporary)
                return todo[0:index1]+str(newvalue)+todo[index2+1:len(todo)]
            elif findparentheses(todo, x)=="try again":
                continue
            else:
                return "error"
    else:
        return "error"
            
    
    
    
def findparentheses(todo, x): #finds next ) starting from y, if ( comes before ) then returns -9999
    for y in range(x+1, len(todo)):
        if todo[y]==")":
            return y
        elif todo[y]=="(":
            return "try again"
    return "error"
                    
            

            






#userinput=input('Enter something with spaces between numbers/operation signs and no parentheses')
'''status="good"
while status=="good":
    equation=raw_input("Enter your equation (no parentheses allowed)")
    print(calculator(equation))
    status="notgood"
    if calculator(equation)=="You messed up":
        status="good"'''
condition=True
while condition==True:
    equation=input("Enter your equation ")
    if not calculator(equation)=="error":
        print(calculator(equation))    
        condition=False
    else:
        print ("Error Try Again")
        
            
            
               
    
        
            
    
