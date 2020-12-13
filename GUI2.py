from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import copy
import math
import os
import time
import collections
 
#functions
def Buildtree (FreqlistSort,DecompressStatus=False):
    TempList=copy.deepcopy(FreqlistSort)
    #for loop
    for z in range(len(FreqlistSort)-1):
        #sort the list        
        TempList=sorted(TempList,key=lambda x:x[1],reverse=True)
        
        TempRecord=[TempList[-1][0],TempList[-2][0]],TempList[-1][1]+TempList[-2][1],''
        TempRecord=list(TempRecord)
        if len(TempRecord[0])==2:

            Temp=[]
            Temp2=[]
            if len(TempRecord[0][0])>=2:
                for x in range(len(TempRecord[0][0])):
                    Temp=Temp+[TempRecord[0][0][x]]
                    for index in range(len(FreqlistSort)):
                        if TempRecord[0][0][x] == FreqlistSort[index][0][0]:
                            FreqlistSort[index][2]='0'+FreqlistSort[index][2]
            else:
                Temp=Temp+TempRecord[0][0]
                for index in range(len(FreqlistSort)):
                    if TempRecord[0][0][0] == FreqlistSort[index][0][0]:
                        FreqlistSort[index][2]='0'+FreqlistSort[index][2]
            if len(TempRecord[0][1])>=2:
                for x in range(len(TempRecord[0][1])):
                    Temp2=Temp2+[TempRecord[0][1][x]]
                    for index in range(len(FreqlistSort)):
                        if TempRecord[0][1][x] == FreqlistSort[index][0][0]:
                            FreqlistSort[index][2]='1'+FreqlistSort[index][2]
            else:
                Temp2=Temp2+TempRecord[0][1]
                for index in range(len(FreqlistSort)):
                    if TempRecord[0][1][0] == FreqlistSort[index][0][0]:
                        FreqlistSort[index][2]='1'+FreqlistSort[index][2]
            ComTemp=Temp+Temp2              
        if not DecompressStatus:
            FreqlistSort_DICT = {FreqlistSort[i][0][0]: FreqlistSort[i][2] for i in range(0, len(FreqlistSort))}
        else:
            FreqlistSort_DICT = {FreqlistSort[i][2]: FreqlistSort[i][0][0] for i in range(0, len(FreqlistSort))}
        TempList=TempList[:-2]+[[ComTemp,TempRecord[1],TempRecord[2]]]
    return FreqlistSort,FreqlistSort_DICT
 
class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Huffman Code Compressor/Decompressor")
        self.minsize(640, 200)
 
        self.labelFrame = ttk.LabelFrame(self, text = "Compressor")
        self.labelFrame.grid(column = 0, row = 1, padx = 20, pady = 20)
        
        self.labelFrame2 = ttk.LabelFrame(self, text = "Decompressor")
        self.labelFrame2.grid(column = 0, row = 5, padx = 20, pady = 20)
 
        self.button()
        self.button2()
 
    def button(self):
        self.button = ttk.Button(self.labelFrame, text = "Browse a file to Compress",command = self.fileDialog)
        self.button.grid(column = 1, row = 1)
   
    def button2(self):
        self.button2 = ttk.Button(self.labelFrame2, text = "Browse a file to Decompress",command = self.fileDialog2)
        self.button2.grid(column = 1, row = 5)
    
    def fileDialog2(self):
        self.filename = filedialog.askopenfilename(initialdir =  "/", title = "Select A File",filetypes=(("all files","*.bin"),("all files","*.bin")))
        self.label = ttk.Label(self.labelFrame2)
        self.label.grid(column = 1, row = 6)
        self.label.configure(text = 'File selected: '+self.filename)
        path = self.filename
        with open (path.split('.')[0]+'.bin',"rb") as image:
            f=image.read()
            b=bytearray(f)
        Decode_base64_bytes=b
        NumBytesChar=Decode_base64_bytes[0]
        NumChar=int.from_bytes(Decode_base64_bytes[1:1+NumBytesChar],byteorder='big')
        NumBytes=Decode_base64_bytes[1+NumBytesChar]
        Decode_list=[]
        CharNum=0
        #read the header file
        for x in range(NumChar):
            if x==0:
                Decode_list.append([[Decode_base64_bytes[2+NumBytesChar]],int.from_bytes(Decode_base64_bytes[3+NumBytesChar:3+NumBytesChar+NumBytes],byteorder='big'),''])
                CharNum+=int.from_bytes(Decode_base64_bytes[3+NumBytesChar:3+NumBytesChar+NumBytes],byteorder='big')
                'stop here need to fix index for the else statement'
            else:
                Decode_list.append([[Decode_base64_bytes[NumBytesChar+2+(1+NumBytes)*x]],int.from_bytes(Decode_base64_bytes[NumBytesChar+3+(1+NumBytes)*x:3+(1+NumBytes)*x+NumBytes+NumBytesChar],byteorder='big'),''])
                EndofInx=3+(1+NumBytes)*x+NumBytes+NumBytesChar
                CharNum+=int.from_bytes(Decode_base64_bytes[NumBytesChar+3+(1+NumBytes)*x:3+(1+NumBytes)*x+NumBytes+NumBytesChar],byteorder='big')
        EXTLen=Decode_base64_bytes[EndofInx]
        EXTType=Decode_base64_bytes[EndofInx+1:EndofInx+EXTLen+1].decode('ascii')
        EndofInx=EndofInx+EXTLen+1
        
        #rebuild tree for decoding    
        Decode_list,FreqlistSort_DICT=Buildtree(Decode_list,DecompressStatus=True)
        
        #Convert data into string of binary
        Decode_base64_bytes_str=''.join(bin(Decode_base64_bytes[EndofInx+x])[2:].zfill(8) for x in range(len(Decode_base64_bytes[EndofInx:])))

        #decode the data
        CharCNT=0
        Decode_str=[]
        startIndex=0
        
        for x in range (len(Decode_base64_bytes_str)+1):
            if CharCNT==CharNum:
                break
            if Decode_base64_bytes_str[startIndex:x] in FreqlistSort_DICT.keys():
                Decode_str+=[FreqlistSort_DICT[Decode_base64_bytes_str[startIndex:x]]]
                startIndex=x
                CharCNT+=1
        #write the data back in original form
        file = open(path.split('.')[0]+'_HuffmanDecode.'+EXTType, "wb")
        Hexarray=bytearray(Decode_str)
        file.write(Hexarray)
        file.close()    
        self.label = ttk.Label(self.labelFrame2, text = "")
        self.label.grid(column = 1, row = 7)
        self.label.configure(text = 'Decompressed file: '+path.split('.')[0]+'_HuffmanDecode.'+EXTType)
    
    def fileDialog(self):
        t1=time.time()
        self.filename = filedialog.askopenfilename(initialdir =  "/", title = "Select A File",filetypes=(("all files","*.*"),("all files","*.*")))
        self.label = ttk.Label(self.labelFrame, text = "")
        self.label.grid(column = 1, row = 2)
        self.label.configure(text = 'File selected: '+self.filename)

        path = self.filename
        
        with open (path,"rb") as image:
            f=image.read()
            b=bytearray(f)
        base64_bytes=b
        
        Freqlist2=collections.Counter(base64_bytes)
        Freqlist=[[[key],value,''] for key,value in Freqlist2.items()]
        #sort the list        
        FreqlistSort=sorted(Freqlist,key=lambda x:x[1],reverse=True)
        
        FreqlistSort,FreqlistSort_DICT=Buildtree(FreqlistSort)
            
        binaryString=''.join(FreqlistSort_DICT[x] for x in base64_bytes)
        #make sure the length is dividable by 8 bits
        if len(binaryString)%8!=0:
            binaryString+='0'*int(((1-(len(binaryString)/8-int(len(binaryString)/8)))*8))
            
        #Need to create a header file
        HeaderByte1=len(FreqlistSort)
        HeaderByte1Num=math.ceil(HeaderByte1/255)
        maxNum=0
        HeaderFrequency=[]
        completeHeader=0
        for x in range (len(FreqlistSort)):
            if FreqlistSort[x][1]>maxNum:
                maxNum=FreqlistSort[x][1]
            HeaderFrequency.append(FreqlistSort[x][1])  #list of ascii frequency
        HeaderByte2=len(hex(maxNum))-2 #1
        
        for x in range (len(FreqlistSort)):
            if x==0:
                completeHeader=bytes([HeaderByte1Num])+(HeaderByte1).to_bytes(HeaderByte1Num,byteorder="big")+bytes([HeaderByte2])+bytes(FreqlistSort[x][0])+(HeaderFrequency[x]).to_bytes(HeaderByte2, byteorder="big")
            else:
                completeHeader=completeHeader+bytes(FreqlistSort[x][0])+(HeaderFrequency[x]).to_bytes(HeaderByte2, byteorder="big")
        
        #include the file format in the header
        extention=path.split('.')[-1]
        HeaderEXTByteNUM=len(extention)
        HeaderEXTByte=[ord(c) for c in extention]
        for x in range (HeaderEXTByteNUM):
            if x==0:
                completeHeader=completeHeader+bytes([HeaderEXTByteNUM])+HeaderEXTByte[x].to_bytes(1, byteorder="big")
            else:
                completeHeader=completeHeader+HeaderEXTByte[x].to_bytes(1, byteorder="big")
        
        #convert to hex

        file = open(path.split('.')[0]+'_HuffmanCompress.bin', "wb")
        #Hexarray=bytearray(HexStringList)
        Hexarray=int(binaryString, 2).to_bytes(len(binaryString) // 8, byteorder='big')
        file.write(completeHeader+Hexarray)
        file.close()
        self.label2 = ttk.Label(self.labelFrame, text = "")
        self.label2.grid(column = 1, row = 3)
        self.label2.configure(text = 'Compressed file: '+path.split('.')[0]+'_HuffmanCompress.bin')
        t2=time.time()
        
        fileSize=os.stat(path.split('.')[0]+'_HuffmanCompress.bin').st_size
        file = open(path.split('.')[0]+'_HuffmanReport.txt', "w")
        file.write('Time took to Compress: '+str(t2-t1)+' Seconds\n')
        file.write('Original file size: '+str(len(base64_bytes))+' bytes\n')
        file.write('Header file size: '+str(len(completeHeader))+' bytes\n')
        file.write('Compressed file size: '+str(fileSize)+' bytes\n')
        file.write('Compression ratio (Compress file size/Original file size): '+str(fileSize/len(base64_bytes))+'\n\n')
        file.write('Ascii\t\t\tFrequency\t\tBinary Value\n')
        for x in range (len(FreqlistSort)):
            file.write(str(FreqlistSort[x][0][0])+'\t\t\t'+str(FreqlistSort[x][1])+'\t\t\t'+str(FreqlistSort[x][2])+'\n')
        file.close()
        self.label3 = ttk.Label(self.labelFrame, text = "")
        self.label3.grid(column = 1, row = 4)
        self.label3.configure(text = 'Huffman report generated: '+path.split('.')[0]+'_HuffmanReport.txt')
        
root = Root()
root.mainloop()