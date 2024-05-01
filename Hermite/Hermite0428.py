xi=list(map(float,input().split()))

yi=list(map(float,input().split()))

zi=list(map(float,input().split()))

x=float(input())

if len(xi)==len(yi)==len(zi):

    pass

else:

    print("维数不相同,请重新输入")

H=0.0

len=len(xi)

for i in range(len):

    t1=1.0

    t2=0.0

    for j in range(len):

        if j!=i:

            t1=t1*((x-xi[j])/(xi[i]-xi[j]))

            t2=t2+1/(xi[i]-xi[j])

        alpha=(1-2*(x-xi[i])*t2)*t1*t1

        beta=(x-xi[i])*t1*t1

    H=H+yi[i]*alpha+zi[i]*beta

print("插值结果为:",H)
