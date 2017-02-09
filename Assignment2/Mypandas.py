
import csv
import ast
import datetime

from collections import OrderedDict

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
            # Task 1 for checking duplications in column names
            if len(self.header) > len(set(self.header)):
                raise TypeError('It appears there are duplicate names in the header')

            self.data = list_of_lists[1:]
        else:
            self.header = ['column' + str(index + 1) for index, column in enumerate(self.data[0])]
            self.data = list_of_lists
           #Task 2 stripping the leading and trailing space
        for row in self.data:
            if isinstance([item for item in row.itervalues],str):
                item=item.strip()
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

        # only for lists of column names
        elif isinstance(item, list):
            return [[row[column_name] for column_name in item] for row in self.data]

    def get_rows_where_column_has_value(self, column_name, value, index_only=False):
        if index_only:
            return [index for index, row_value in enumerate(self[column_name]) if row_value==value]
        else:
            return [row for row in self.data if row[column_name]==value]


####### task 3

    def median(self,column_name):
         if column_name in ('Transaction_date', 'Account_Created', 'Last_Login'):
             list3 = [datetime.datetime.strptime(row[column_name], format) for row in self.data]
             list3 = sorted(list3)

         else : list3 = [ast.literal_eval(row[column_name]) for row in self.data if ast.literal_eval(row[column_name]) != str]

         if len(list3) < 1:
            return None
         if len(list3) % 2 == 1:
            return list3[((len(list3) + 1) / 2) - 1]
         else:
            return float(sum(list3[(len(list3) / 2) - 1:(len(list3) / 2) + 1])) / 2.0

         TypeError('Only numeric numbers and datetime obejects can be calculated')


    def mean(self,column_name):
        sum1=0
        count1=0
        if column_name in ('Transaction_date', 'Account_Created', 'Last_Login'):
           list1 = [datetime.datetime.strptime(row[column_name], format) for row in self.data]
           list1 = sorted(list1)
           for item in list1 :
              sum1= sum1+item
              count1=count1+1
           return sum1/count1
        else: list1 = [ast.literal_eval(row[column_name]) for row in self.data if ast.literal_eval(row[column_name]) != str]
            for item in list1:
                   sum1= sum1+item
                   count1=count1+1
               return sum1 /count1
        TypeError('Only numeric numbers and datetime obejects can be calculated')




    def max(self,column_name) :
        mker=0
        if column_name in ('Transaction_date', 'Account_Created', 'Last_Login'):
           list2 = [datetime.datetime.strptime(row[column_name], format) for row in self.data]
           list2 = sorted(list2)
           for item in list2 :
              if item > mker:
                  mker=item
           return mker
        else: list2 = [ast.literal_eval(row[column_name]) for row in self.data if ast.literal_eval(row[column_name]) != str]
           for item in list2:
              if item > mker:
                  mker = item
           return mker
        TypeError ('Only numeric numbers and datetime obejects can be calculated')




    def min(self,column_name):
        mker=0
        if column_name in ('Transaction_date', 'Account_Created', 'Last_Login'):
           list2 = [datetime.datetime.strptime(row[column_name], format) for row in self.data]
           list2 = sorted(list2)
           for item in list2 :
              if item < mker:
                  mker=item
           return mker
        else:
            list2 = [ast.literal_eval(row[column_name]) for row in self.data if ast.literal_eval(row[column_name]) != str]
            for item in list2:
               if item < mker:
                  mker = item
           return mker
        else:
            raise TypeError('Only numeric numbers and datetime obejects can be calculated')



    def std(self,column_name):
       sum1 = 0
       var1=0
       count1 = 0
       if column_name in ('Transaction_date', 'Account_Created', 'Last_Login'):
            list1 = [datetime.datetime.strptime(row[column_name], format) for row in self.data]
            list1 = sorted(list1)
            for item in list1:
              sum1 = sum1 + item
              count1 = count1 + 1
            mean1= sum1 / count1
            for item in list1:
               var1=(item-mean1)^2+var1
            returnstd1=var1^0.5
        else:
            list1 = [ast.literal_eval(row[column_name]) for row in self.data if ast.literal_eval(row[column_name]) != str]
            for item in list1:
               sum1 = sum1 + item
               count1 = count1 + 1
            mean1 = sum1 / count1
            for item in list1:
                var1 = (item - mean1) ** 2 + var1
            return var1 ** 0.5
        TypeError('Only numeric numbers and datetime obejects can be calculated')


#####  Task 4
    def add_rows(self, list_of_lists) :
       for row in list_of_lists:
           if len(self.header)==len(row):
              data1 = OrderedDict(zip(self.header, row))
              self.data.append(data1)
           else:
              TypeError('the number of columns in you list you intend to add must be the same as in the dataframe')

####   Task 5
    def add_column(self, list_of_values, column_name):
       self.header.append(column_name)
       if len(list_of_values)==len(self.data):
          for index,row in enumerate(self.data):
               self.data[index][column_name]=list_of_values[index]
       else:
             TypeError('the number of items in the  list you intend to add must be the same as the number of rows in the  dataframe')


