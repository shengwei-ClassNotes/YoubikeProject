import os 

print('Preparing')

os.chdir('C:/Users/SyuShengWei/Desktop/project/')
#normal day List
Normal_Day_List = list()
inFile = open('NormalDay.txt','r')
Data_List = inFile.readlines()
for theLine in Data_List:
	Normal_Day_List.append(theLine.strip('\n'))
inFile.close()

NUM_normalday = len(Normal_Day_List)
NUM_peroid    = 24
NUM_station   = 164
NUM_lenofperoid = 3600
NUM_mergeday  = 10
NUM_merge	  = NUM_normalday - NUM_mergeday + 1

Perday_ODRRecord = list()
for day in range(0,NUM_normalday):
	ODRRecord = list()
	for O in range(0,NUM_station):
		O_List = list()
		for D in range(0,NUM_station):
			D_List = list()
			for peroid in range(0,NUM_peroid):
				peroid_record = 0
				D_List.append(peroid_record)
			O_List.append(D_List)
		ODRRecord.append(O_List)
	Perday_ODRRecord.append(ODRRecord)

Perday_TotalRecord = list()
for day in range(0,NUM_normalday):
	Total_ODRecord = list()	
	for O in range(0,NUM_station):
		O_List = list()
		for peroid in range(0,NUM_peroid):
			peroid_record = 0
			O_List.append(peroid_record)
		Total_ODRecord.append(O_List)	
	Perday_TotalRecord.append(Total_ODRecord)

print('Reading data')	


for filename in os.listdir('C:/Users/SyuShengWei/Desktop/project/RegularForm'):
	os.chdir('C:/Users/SyuShengWei/Desktop/project/RegularForm')
	the_day = filename.strip('.csv')
	if the_day not in Normal_Day_List : continue
	else :
		day_index = Normal_Day_List.index(the_day)
		inFile = open(filename,'r')
		titelLine = inFile.readline()
		Data_List = inFile.readlines()
		for dataLine in Data_List:
			theLine = dataLine.strip('\n')
			Line_Info = theLine.split(',')
			o_index = int(Line_Info[4])
			d_index = int(Line_Info[5])
			peroid_index =  int(Line_Info[1])//NUM_lenofperoid
			
			Perday_ODRRecord[day_index][o_index][d_index][peroid_index] 	+= 1
			Perday_TotalRecord[day_index][o_index][peroid_index] 			+= 1
		
		inFile.close()


		
Merge_ODRRecord = list()
for day in range(0,NUM_merge):
	ODRRecord = list()
	for O in range(0,NUM_station):
		O_List = list()
		for D in range(0,NUM_station):
			D_List = list()
			for peroid in range(0,NUM_peroid):
				peroid_record = 0
				for index in range(0,NUM_mergeday):
					peroid_record += Perday_ODRRecord[day+index][O][D][peroid]
				D_List.append(peroid_record)
			O_List.append(D_List)
		ODRRecord.append(O_List)
	Merge_ODRRecord.append(ODRRecord)		
		

Merge_TotalRecord = list()
for day in range(0,NUM_merge):
	Total_ODRecord = list()	
	for O in range(0,NUM_station):
		O_List = list()
		for peroid in range(0,NUM_peroid):
			peroid_record = 0
			for index in range(0,NUM_mergeday):
				peroid_record += Perday_TotalRecord[day+index][O][peroid]
			O_List.append(peroid_record)
		Total_ODRecord.append(O_List)	
	Merge_TotalRecord.append(Total_ODRecord)		
		
		
print('Top10 Recording')		
	
Top_10_Station_List = list()   #[day][O][peroid][i]
Top_10_Value_List = list()
for day in range(0,NUM_normalday):
	Day_List_1 = list()
	Day_List_2 = list()
	for O in range(0,NUM_station):
		O_List_1 = list()
		O_List_2 = list()
		for peroid in range(0,NUM_peroid):
			Peroid_List_1 = list()
			Peroid_List_2 = list()
			for i in range(0,10):
				Peroid_List_1.append(-1)
				Peroid_List_2.append(-1)
			O_List_1.append(Peroid_List_1)
			O_List_2.append(Peroid_List_2)
		Day_List_1.append(O_List_1)
		Day_List_2.append(O_List_2)
	Top_10_Station_List.append(Day_List_1)
	Top_10_Value_List.append(Day_List_2)

for day in range(0,NUM_merge):
	for O in range(0,NUM_station):
		for D in range(0,NUM_station):
			for peroid in range(0,NUM_peroid):
				if Merge_ODRRecord[day][O][D][peroid] == 0 : continue
				else:
					for index in range(0,10):
						if Merge_ODRRecord[day][O][D][peroid] >= Top_10_Value_List[day][O][peroid][index] :
							Top_10_Value_List[day][O][peroid].insert(index,Merge_ODRRecord[day][O][D][peroid])
							Top_10_Station_List[day][O][peroid].insert(index,D)
							lose_value = Top_10_Value_List[day][O][peroid].pop()
							lose_Station = Top_10_Station_List[day][O][peroid].pop()
							break
						else:
							continue

						
						
						
print('OutFile')
						
os.chdir('C:/Users/SyuShengWei/Desktop/project/Analysis/Top1_1HR_merge10')	
for O in range(NUM_station):
	outFile = open(str(O).rjust(3,'0')+'.csv','a')
	for peroid in range(0,NUM_peroid):
		for day in range(0,NUM_merge):
			if  (str(Top_10_Station_List[day][O][peroid][0]).rjust(3,'0') + ';' + str(Top_10_Value_List[day][O][peroid][0])) == '163;0' :
				outFile.write('Non')
			else:
				outFile.write(str(Top_10_Station_List[day][O][peroid][0]).rjust(3,'0') + ';' + str(Top_10_Value_List[day][O][peroid][0]))
			if day != NUM_merge -1 :
				outFile.write(',')
			else :
				outFile.write('\n')
print('TOP10_File')				


os.chdir('C:/Users/SyuShengWei/Desktop/project/Analysis/Top10_record_merge10')
for O in range(NUM_station):
	outFile = open('Top10-'+str(O).rjust(3,'0')+'.csv','a')
	for peroid in range(0,NUM_peroid):
		for day in range(0,NUM_merge):
			for index in range(0,10):
				outFile.write(str(Top_10_Station_List[day][O][peroid][index]))
				if index != 9 : 
					outFile.write('_')
			if day != NUM_merge -1 :
				outFile.write(',')
			else :
				outFile.write('\n')
	outFile.close()
	
	outFile = open('Value-'+str(O).rjust(3,'0')+'.csv','a')
	for peroid in range(0,NUM_peroid):
		for day in range(0,NUM_merge):
			for index in range(0,10):
				outFile.write(str(Top_10_Value_List[day][O][peroid][index]))
				if index != 9:
					outFile.write('_')
			if day != NUM_merge -1 :
				outFile.write(',')
			else :
				outFile.write('\n')
	outFile.close()
	
	outFile = open('ODR-'+str(O).rjust(3,'0')+'.csv','a')
	for peroid in range(0,NUM_peroid):
		for day in range(0,NUM_merge):
			for index in range(0,10):
				if Merge_TotalRecord[day][O][peroid] == 0 :
					ODR = 0.0
				else:
					ODR = round(Top_10_Value_List[day][O][peroid][index] / Merge_TotalRecord[day][O][peroid],5)
				
				outFile.write(str(ODR).ljust(6,'0'))
				if index != 9:
					outFile.write('-')
			if day != NUM_merge -1 :
				outFile.write(',')
			else :
				outFile.write('\n')
	outFile.close()
				