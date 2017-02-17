
import csv
import ast
import datetime

from collections import OrderedDict

###########  task 2 for assignment3
class Series(object):
    def __init__(self, items):
        self.data = items

    def __eq__(self, other):
        ret_list = []
        for item in self.data:
            ret_list.append(item == other)
        return ret_list

    def __gt__(self, other):
        ret_list = []
        for item in self.data:
            ret_list.append(item > other)
        return ret_list

    def __lt__(self, other):
        ret_list = []
        for item in self.data:
            ret_list.append(item < other)
        return ret_list

    def __ne__(self, other):
        ret_list = []
        for item in self.data:
            ret_list.append(item != other)
        return ret_list

    def __ge__(self, other):
        ret_list = []
        for item in self.data:
            ret_list.append(item >other| item == other)
        return ret_list

    def __le__(self, other):
        ret_list = []
        for item in self.data:
            ret_list.append(item < other| item == other)
        return ret_list




class DataFrame(object):

    @classmethod
    def from_csv(cls, file_path, delimiting_character=',', quote_character='"'):
        with open(file_path, 'rU') as infile:
            reader = csv.reader(infile, delimiter=delimiting_character, quotechar=quote_character)
            data = []

            for row in reader:
                data.append(row)

            return cls(list_of_lists=data)



    def __init__(self, list_of_lists, header=True):
        if header:
            self.header = list_of_lists[0]
            
            
    # Task 1 for checking duplications in column names .....assignment 2
            if len(self.header) != len(set(self.header)):
                raise TypeError('It appears there are duplicate names in the header')

            else :self.data = list_of_lists[1:]
        else:
            self.header = ['column' + str(index + 1) for index, column in enumerate(self.data[0])]
            self.data = list_of_lists
          
           
    #Task 2 stripping the leading and trailing space.....for assignment 2
        #for row in self.data:
        #    if isinstance([item for item in row.itervalues],str):
        #        item=item.strip()
        
        self.data = [OrderedDict(zip(self.header, row)) for row in self.data]


    def __getitem__(self, item):

        # this is for rows only
        if isinstance(item, (int, slice)):
            return self.data[item]

        # this is for columns only
        elif isinstance(item, (str, unicode)):
            return [row[item] for row in self.data]

        # this is for rows and columns
        elif isinstance(item, tuple):
            if isinstance(item[0], list) or isinstance(item[1], list):

                if isinstance(item[0], list):
                    rowz = [row for index, row in enumerate(self.data) if index in item[0]]
                else:
                    rowz = self.data[item[0]]

                if isinstance(item[1], list):
                    if all([isinstance(thing, int) for thing in item[1]]):
                        return [[column_value for index, column_value in enumerate([value for value in row.itervalues()]) if index in item[1]] for row in rowz]
                    elif all([isinstance(thing, (str, unicode)) for thing in item[1]]):
                        return [[row[column_name] for column_name in item[1]] for row in rowz]
                    else:
                        raise TypeError('What the hell is this?')

                else:
                    return [[value for value in row.itervalues()][item[1]] for row in rowz]
            else:
                if isinstance(item[1], (int, slice)):
                    return [[value for value in row.itervalues()][item[1]] for row in self.data[item[0]]]
                elif isinstance(item[1], (str, unicode)):
                    return [row[item[1]] for row in self.data[item[0]]]
                else:
                    raise TypeError('I don\'t know how to handle this...')

    ###### task2 for assignment 3
    
    ###### only for lists of column names
        
        elif isinstance(item, list):
             if isinstance(item[0],str):
                 return [[row[column_name] for column_name in item] for row in self.data]
        
    ####### task2 for assignment 3, only for list of bools
         
             if isinstance(item[0],bool):
                 return [self.data[index] for index, value in enumerate(item) if value]

        
       
        
        
        #elif isinstance(item,list):
        #     if 
        #     list1=[]
        #     for index, value in enumerate(item):
        #         if isinstance(value,bool) and value:
        #            list1.append(self.data[index])
        #     return list1



    def get_rows_where_column_has_value(self, column_name, value, index_only=False):
        if index_only:
            return [index for index, row_value in enumerate(self[column_name]) if row_value==value]
        else:
            return [row for row in self.data if row[column_name]==value]

    
    

####### task 3 for assignment 2
        
    

#####  Task 4 for assignment2
    def add_rows(self, list_of_lists) :
       for row in list_of_lists:
           if len(self.header)==len(row):
              data1 = OrderedDict(zip(self.header, row))
              self.data.append(data1)
           else:
              TypeError('the number of columns in you list you intend to add must be the same as in the dataframe')

####   Task 5  or assignment2
    def add_column(self, list_of_values, column_name):
       self.header.append(column_name)
       if len(list_of_values)==len(self.data):
          for index,row in enumerate(self.data):
               self.data[index][column_name]=list_of_values[index]
       else:
             TypeError('the number of items in the  list you intend to add must be the same as the number of rows in the  dataframe')


##### Task 1 for assignment 3

    def sort_by(self,item1,item2):
        if isinstance(item1,str) and isinstance(item2,bool):
           return(sorted(self.data, key=lambda x: x[item1] , reverse=item2))

        elif isinstance(item1,list) and isinstance(item2,list):
            for index,column_name  in enumerate(item1):
                self.data = sorted(self.data, key=lambda x: x[column_name] , reverse=item2[index])
            return self
        else:
            raise TypeError('something wrong with the parameter')

###### Task 3 for assignment 3

    def group_by(self,columnname1,columnname2,avg):
    
         unique_element=set(self[columnname1].data)
         result=[]
         agg_df=[]
         for element in unique_element:
             list1=[]
             for row in self.data:
                 if row[columnname1]==element:
                    list1.append(row[columnname2])
             result.append(avg(list1))
         agg_df.append([columnname1,columnname2])
         agg_df.append([unique_element,result])
         return agg_df
        


def avg(list_of_values):
    return sum(list_of_values)/float(len(list_of_values))




infile = open('/Users/liwentao/PycharmProjects/BIA-660-C-Spring2017/SalesJan2009.csv')

lines = infile.readlines()
lines = lines[0].split('\r')
data = [l.split(',') for l in lines]


df= DataFrame(list_of_lists=data)
#df['Price']
#df.sort_by('Payment_Type',True)
#df.sort_by(['Product','Price'],reverse=['Ture','False'])
#indices = df.get_rows_where_column_has_value('Payment_Type', 'Visa', index_only=True)
#df[df['Price']>1400]
#df.group_by('Prodcut','Payment_Type',avg)