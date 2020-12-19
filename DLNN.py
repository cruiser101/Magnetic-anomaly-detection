import keras
keras.__version__

#============
import numpy as np
import matplotlib.pyplot as plt

#============
import linecache

def file2matrix(filename):
    fr = open(filename)
    numberOfLines = len(fr.readlines()) #get the number of lines in the file
    count = linecache.getline(filename,1)
    numberOfColuns = len(count.split(' '))
    print ('numberOfLines=',numberOfLines,'numberOfColuns=',numberOfColuns)
    returnMat = np.zeros((numberOfLines,121))        #prepare matrix to return
    returnMatLabel = np.zeros((numberOfLines,242))   #prepare labels return
    returnMatPars = np.zeros((numberOfLines,5))
    fr = open(filename)
    index = 0
    for line in fr.readlines():
        line = line.strip()
        listFromLine = line.split(' ')
        returnMat[index,:] = listFromLine[0:121]
        returnMatLabel[index,:] = listFromLine[121:363]
        returnMatPars[index,:] = listFromLine[363:368]
        index += 1
    return returnMat/100000.0,returnMatLabel/100000.0, returnMatPars


def text_save(filename, data):#filename为写入CSV文件的路径，data为要写入数据列表.
    file = open(filename,'a')
    for i in range(len(data)):
        s = str(data[i]).replace('[','').replace(']','')#去除[],这两行按数据不同，可以选择
        s = s.replace("'",'').replace(',','') +'\n'   #去除单引号，逗号，每行末尾追加换行符
        file.write(s)
    file.close()


#===========
DataMat,DataLabels, Pars = file2matrix('D:/Papers/Geomagnetic/MAT/1126/localmdnoise01.dat')
print('(DataMat.shape=',DataMat.shape,'DataLabels.shape=',DataLabels.shape, 'Pars=',Pars.shape)

x_data=np.arange(-2,4.05,0.05)
x_data2=np.arange(-2,10.1,0.05)

plt.plot(x_data,DataLabels[55,0:121]+DataLabels[55,121:242], 'k,-', label='Za0')
plt.plot(x_data,DataLabels[55,0:121], 'b.--', label='Za1')
plt.plot(x_data,DataLabels[55,121:242], 'y.--', label='Za2')
plt.plot(x_data, DataMat[55,:], 'ro-', label='Zn')
plt.legend(ncol=1)
plt.figure()

for i in range(1,2):
    plt.clf()
    plt.plot(x_data,DataLabels[i,0:121]+DataLabels[i,121:242], 'k,-', label='Za0')
    plt.plot(x_data,DataLabels[i,0:121], 'b.--', label='Za1')
    plt.plot(x_data,DataLabels[i,121:242], 'y.--', label='Za2')
    plt.plot(x_data, DataMat[i,:], 'ro-', label='Zn')
    #plt.text(Pars[i,2],Pars[i,3],Pars[i,4], fontsize=15)
    plt.legend(ncol=1)
    plt.show()
    plt.pause(0.5)

# #===============
train_num=20000
validation_num=2000
test_num=2000

x_stack=np.arange(0,DataMat.shape[0],1)
#np.random.shuffle(x_stack)
print(x_stack)

#===============
train_data = DataMat[x_stack[0:train_num],:]
train_targets = DataLabels[x_stack[0:train_num],:]

validation_data = DataMat[x_stack[train_num : (train_num+validation_num)]]
validation_targets = DataLabels[x_stack[train_num : (train_num+validation_num)]]

test_data = DataMat[x_stack[(train_num+validation_num) : (train_num+validation_num+test_num)]]
test_targets = DataLabels[x_stack[(train_num+validation_num) : (train_num+validation_num+test_num)]]

print('train_data.shape=',train_data.shape,'train_targets.shape=',train_targets.shape)
# plt.plot(x_data, train_data[300,:], 'g*-', label='y')
# plt.figure()

#=============
from keras import models
from keras import layers

network = models.Sequential()
network.add(layers.Dense(121, activation='relu',
                            input_shape=(train_data.shape[1],)))
network.add(layers.Dense(121, activation='relu'))
network.add(layers.Dense(242, activation='relu'))
network.add(layers.Dense(484, activation='relu'))
network.add(layers.Dense(484, activation='relu'))
network.add(layers.Dense(484, activation='relu'))
network.add(layers.Dense(484, activation='sigmoid'))
network.add(layers.Dense(242, activation='sigmoid'))
network.add(layers.Dense(242))

#=============
from keras import optimizers
#optimizer='rmsprop'
network.compile(optimizer=optimizers.RMSprop(lr=0.001),
                loss='mse',
                metrics=['mae'])

#========
history = network.fit(train_data, train_targets,
                      epochs=110,
                      batch_size=100,
                      validation_data=(validation_data, validation_targets))

#=============
network.save('keras07.h5')

#=============
loss = history.history['loss']
print('type(loss)=',type(loss))
del loss[0]
val_loss = history.history['val_loss']
del val_loss[0]

epochs = range(1, len(loss)+1 )
plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'r', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

text_save('D:/Papers/Geomagnetic/Pythons/1126/loss06.txt', loss)
text_save('D:/Papers/Geomagnetic/Pythons/1126/val_loss06.txt', val_loss)


#=============
test_loss, test_acc = network.evaluate(test_data, test_targets)
print('test_loss=',test_loss,'test_acc=',test_acc)
preds = network.predict(test_data)

test_perc = np.zeros(test_num)
for i in range(test_num):
    z1_1=[0,0]
    za_2=[0,0]
    z1_1 = np.polyfit(test_targets[i,0:121], preds[i,0:121], 1)
    z1_2 = np.polyfit(test_targets[i,121:242], preds[i,121:242], 1)
    z1= abs(z1_1[0]-1)+abs(z1_2[0]-1)
    test_perc[i] = z1/2

# test_perc = np.zeros(test_num)
# for i in range(test_num):
#     test_perc_j=np.zeros(DataLabels.shape[1])
#     for j in range(DataLabels.shape[1]):
#         test_perc_j[j]= abs((preds[i,j]-test_targets[i,j])/test_targets[i,j])*100
#     test_perc[i]=sum(test_perc_j)/(DataLabels.shape[1])

plt.plot(range(1,test_num +1), test_perc, 'b*', label='test_perc')
plt.title('test_perc average')
plt.xlabel('num')
plt.ylabel('test_perc')
#plt.ylim(-1,100)
plt.show()

#============
plt.plot(x_data2, test_targets[100,:], 'r:', label='stand', linewidth=5)
plt.plot(x_data, test_data[100,:], 'bo-', label='signal', linewidth=1)
plt.plot(x_data2, preds[100,:], 'g-', label='preds', linewidth=2)
plt.legend()
plt.figure()

#=============
netfit = np.zeros(test_num)
for i in range(test_num):
    z1 = np.polyfit(preds[i,:], test_targets[i,:], 1)
    netfit[i]=z1[0]
#netfit=np.transpose(netfit)

net_x2=np.linspace(1,test_num,test_num)
plt.plot(net_x2,netfit,color="blue",label="net line",linewidth=0.5)
plt.legend() 
plt.show()










