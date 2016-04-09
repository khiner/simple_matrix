#!/usr/bin/env python

class Matrix:
  def __init__(self, n_rows_or_list = 1, n_columns = 1):
    if isinstance(n_rows_or_list, list):
      self.n_rows = len(n_rows_or_list)
      self.n_columns = 1
    else:
      if isinstance(n_rows_or_list, (int, long)):
        self.n_rows = n_rows_or_list
        self.n_columns = n_columns
      else:
        print 'Don\'t know what to do with a ' + type(n_rows_or_list) + ' constructor. Defaulting to an empty 1-d matrix'
        self.n_rows = self.n_columns = 1

    self.values = [[0 for i in range(n_columns)] for j in range(self.n_rows)]
    if isinstance(n_rows_or_list, list):
      for row_index, row_value in enumerate(n_rows_or_list):
        self.values[row_index][0] = row_value

  def __add__(self, other):
    if isinstance(other, Matrix):
      return self.__plus_matrix(other)
    elif isinstance(other, (int, long, float, complex)):
      return self.__plus_scalar(other)
    else:
      print 'Do not know how to add a ' + type(other) + ' to a matrix.'
      return self

  def __mul__(self, other):
    if isinstance(other, Matrix):
      return self.__times_matrix(other)
    elif isinstance(other, list):
      return self.__times_matrix(Matrix(other))
    elif isinstance(other, (int, long, float, complex)):
      return self.__times_scalar(other)
    else:
      print 'Do not know how to add a ' + type(other) + ' to a matrix.'
      return self

  def to_string(self):
    string = ''
    for row in self.values:
      string += '['
      for columnIndex, value in enumerate(row):
        string += str(value)
        if columnIndex != self.n_columns - 1:
          string += ' '
      string += "]\n"

    return string

  def __plus_scalar(self, scalar):
    for row in self.values:
      for index, value in enumerate(row):
        row[index] += scalar

    return self

  def __plus_matrix(self, other):
    if other.n_rows == self.n_rows and other.n_columns == self.n_columns:
      for rowIndex, row in enumerate(self.values):
        for columnIndex, value in enumerate(row):
          self.values[rowIndex][columnIndex] += other.values[rowIndex][columnIndex]
    else:
      print 'Cannot add a matrix by another with different dimensionality.'

    return self

  def __times_scalar(self, scalar):
    for row in self.values:
      for index, value in enumerate(row):
        row[index] *= scalar

    return self

  def __times_matrix(self, other):
    if other.n_rows == self.n_rows and other.n_columns == self.n_columns:
      for rowIndex, row in enumerate(self.values):
        for columnIndex, value in enumerate(row):
          self.values[rowIndex][columnIndex] *= other.values[rowIndex][columnIndex]
    elif other.n_rows == self.n_columns and other.n_columns == 1:
      result_vector = Matrix(self.n_rows)
      for rowIndex, row in enumerate(self.values):
        result_vector.values[rowIndex][0] = 0
        for columnIndex, value in enumerate(row):
          result_vector.values[rowIndex][0] += value * other.values[columnIndex][0]
      return result_vector
    else:
      print 'Can only multiply a matrix by one with the same dimensionality or a vector with row length equal to this matrix\'s column length'

    return self

#matrix = (Matrix(2, 3) + 2 * 3 + (Matrix(2, 3) + 10) + 100) * [1, 1, 2]
#print matrix.to_string()
