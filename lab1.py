def check_of_exemptions(arg1: str):
    cnt=0
    exemption_op=['(','[','{']
    exemption_cl=[')',']','}']
    for i in range(len(arg1)):
        if arg1[i] in exemption_op:
            if arg1[i]=='(':
                cnt+=1
            elif arg1[i]=='[':
                cnt+=2
            elif arg1[i]=='{':
                cnt+=3
            else:
                pass

        elif arg1[i] in exemption_cl:
            if arg1[i]==')':
                cnt-=1
            elif arg1[i]==']':
                cnt-=2
            elif arg1[i]=='}':
                cnt-=3
            else:
                pass
    if cnt == 0:
        print('Строка существует')
        return 1
    else:
        print('Строки не существует')
        return 0
""" 
s=input()
if __name__=='__main__':
    check_of_exemptions(s)"""

    