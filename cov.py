#!/usr/bin/python3

from collections import deque

def norm(x):
    mn = min(x)
    shift = [v-mn for v in x]
    mx = max(shift)
    n = [v/mx for v in shift]
    return n

def read(filename):
    with open(filename,'rt') as file:
        [file.readline() for n in range(2)]
        raw = file.readline()
        labels = raw.strip('"()\n').replace('(','-').replace(')','').replace('"','').replace(':','-').split(' ')[1::]
        data_start = file.tell()
        ncols = len(file.readline().strip().split(' ')[1::])
        data = {n:[] for n in range(ncols)}
        file.seek(data_start)
        for line in file:
            line = line.strip().split(' ')[1::]
            [data[n].append(float(x)) for n,x in enumerate(line)];
    return data,labels

def cov(y,N=50):
    window=deque(y[0:N])
    data = [0]*len(y)
    for i in range(N,len(y)):
        window.popleft()
        window.append(y[i])
        mu = sum(window)/len(window)
        std = (sum([(x-mu)**2 for x in window])/len(window))**0.5
        data[i]=std/abs(mu)
    return data
    
def desc(data,labels,N=50):
    print('{1:32s}{0: >9d}'.format(len(data[0]),'ITERATION'))
    [print('{1:32s}{0:1.3e}'.format(cov(x,N)[-1],l)) for x,l in zip(data.values(),labels)]

def plot(data,labels,N=50,title='',limit=1e-5):
    import matplotlib.pyplot as plt
    fig,axs = plt.subplots(1,2,figsize=[16,9])
    ax = axs[0]
    [ax.semilogy(range(N,len(x)),cov(x,N)[N::],label=l) for x,l in zip(data.values(),labels)]
    ax.grid(True,axis='both',which='both')
    ax.semilogy([N,len(data[0])],2*[limit],c='black',ls='--')
    ax.set_xlim([N,len(data[0])])
    ax.set_ylabel('$COV_{'+str(N)+'}(y)$')
    ax.set_xlabel('$Iteration$')
    ax.legend()
    fig.suptitle(title)
    
    ax = axs[1]
    [ax.plot(norm(D)) for D in data.values()]
    ax.grid(True,axis='both',which='both')
    ax.set_ylabel('$\hat{y}$')
    ax.set_xlabel('$Iteration$')
    
    return fig,axs

if __name__ == '__main__':
    import os
    import sys
    try:
        import matplotlib.pyplot as plt
        mpl = True
    except ImportError:
        mpl = False
        
    if len(sys.argv)>=2:
        filenames = sys.argv[1:len(sys.argv)]
    else:
        filenames = os.listdir('.')
        
    for filename in filenames:
        if ('.out' in filename):
            outname = '.'.join(filename.split('.')[0:-1])
            data,labels = read(filename)
            
            if mpl:
                _,_ = plot(data,labels,title=outname)
                plt.savefig(outname+'.png')

            print(outname)
            desc(data,labels)
            print('')