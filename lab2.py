import operator
from lab1 import check_of_exemptions 
def calculator(string: str):
    if not(check_of_exemptions(string)):
        print("Проверьте корректность выражения")
        return 0
    stack_num=[]
    stack_operetors=[]
    operators=['+','-','*','/','(',')']
    nums=['0','1','2','3','4','5','6','7','8','9']
    chis=''
    operators_meaning={'+': operator.add, '-':operator.sub, '*':operator.mul, '/':operator.truediv}
    operators_priority={'+': 1, '-': 1, '*': 2, '/': 2}
    for i in range(len(string)-1):
        if string[i] in nums:
            chis+=string[i]
        elif string[i] in operators:
            if chis!='':
                stack_num.append(int(chis))
                chis=''
            else:
                pass
            if len(stack_operetors)!=0:
                if string[i] == '(':
                    stack_operetors.append(string[i])
                elif string[i] == ')':
                    while stack_operetors[-1] != '(':
                        second_num=stack_num.pop()
                        first_num=stack_num.pop()
                        operation=operators_meaning[stack_operetors.pop()]
                        if second_num==0 and operation == operator.truediv:
                            print("Деление на ноль невозможно")
                            return 0
                        result=operation(first_num,second_num)
                        stack_num.append(result)
                    stack_operetors.pop()
                elif (stack_operetors[-1]=='(') or (operators_priority.get(stack_operetors[-1])<operators_priority.get(string[i])):
                    stack_operetors.append(string[i])
                else:
                    while (operators_priority.get(string[i]) <= operators_priority.get(stack_operetors[-1])):
                        second_num=stack_num.pop()
                        first_num=stack_num.pop()
                        operation=operators_meaning[stack_operetors.pop()]
                        if second_num==0 and operation == operator.truediv:
                            print("Деление на ноль невозможно")
                            return 0
                        result=operation(first_num,second_num)
                        stack_num.append(result)
                        if len(stack_operetors)==0 or stack_operetors[-1]=='(':
                            break
                    stack_operetors.append(string[i])
                    
            else:
                stack_operetors.append(string[i])
        else:
            print('Введено некорректное выражение')
            return 0
    stack_num.append(int(chis))
    second_num=stack_num.pop()
    first_num=stack_num.pop()
    operation=operators_meaning[stack_operetors.pop()]
    if second_num==0 and operation == operator.truediv:
        print("Деление на ноль невозможно")
        return 0
    result=operation(first_num,second_num)
    stack_num.append(result)
    print(stack_num[0])
    return 1
b=input()
calculator(b)
