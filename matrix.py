class Matrix:
  def __init__(self, n_rows_or_list = 0, n_columns = 0):
    if isinstance(n_rows_or_list, list):
      self.n_rows = len(n_rows_or_list)
      if len(n_rows_or_list) > 0 and isinstance(n_rows_or_list[0], list):
        self.n_columns = len(n_rows_or_list[0])
      else:
        self.n_columns = 0
    else:
      if isinstance(n_rows_or_list, (int, long)):
        self.n_rows = n_rows_or_list
        self.n_columns = n_columns
      else:
        print 'Don\'t know what to do with a ' + type(n_rows_or_list) + ' constructor. Defaulting to an empty 0-d matrix'
        self.n_rows = self.n_columns = 0

    self.values = [[0 for i in range(self.n_columns)] for j in range(self.n_rows)]
    if isinstance(n_rows_or_list, list):
      for row_index, row_value in enumerate(n_rows_or_list):
        if isinstance(row_value, list):
          for column_index, column_value in enumerate(row_value):
            self.values[row_index][column_index] = column_value
        else:
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

  def __str__(self):
    string = ''
    for row_index, row in enumerate(self.values):
      string += '['
      for column_index, value in enumerate(row):
        string += str(value)
        if column_index != self.n_columns - 1:
          string += ' '
      string += ']'
      if row_index != self.n_rows - 1:
        string += "\n"
    return string

  def append_row(self, new_row):
    if isinstance(new_row, (int, long, float, complex)):
      new_row = [new_row] # create a single-element list if input is number
    elif not isinstance(new_row, list):
      print 'Only know how to append lists or numbers to a matrix'
      return

    columns_to_pad = len(new_row) - self.n_columns
    if columns_to_pad > 0:
      # pad existing rows with zeros to match new dimensionality
      for row in self.values:
        for i in range(columns_to_pad):
          row.append(0)
    elif columns_to_pad < 0:
      # pad new row with zeros to match existing dimensionality
      for i in range(-columns_to_pad):
        new_row.append(0)

    self.values.append(new_row)
    self.n_rows += 1
    self.n_columns = len(new_row)

    return self

  def append_column(self, new_column):
    if isinstance(new_column, (int, long, float, complex)):
      new_column = [new_column] # create a single-element list if input is number
    elif not isinstance(new_column, list):
      print 'Only know how to append lists or numbers to a matrix'
      return

    rows_to_pad = len(new_column) - self.n_rows
    if rows_to_pad > 0:
      # pad with new 0-filled rows to match new dimensionality
      self.values.append([0] * self.n_columns)
    elif rows_to_pad < 0:
      # pad new row with zeros to match existing dimensionality
      for i in range(-rows_to_pad):
        new_column.append(0)

    for row_index, row in enumerate(self.values):
      row.append(new_column[row_index])

    self.n_columns += 1
    self.n_rows = len(self.values)

    return self

  def transpose(self):
    transposed_matrix = Matrix(self.n_columns, self.n_rows)
    for row_index, row_value in enumerate(self.values):
      for column_index, value in enumerate(row_value):
        transposed_matrix.values[column_index][row_index] = value

    return transposed_matrix

  def __plus_scalar(self, scalar):
    for row in self.values:
      for index, value in enumerate(row):
        row[index] += scalar

    return self

  def __plus_matrix(self, other):
    if other.n_rows == self.n_rows and other.n_columns == self.n_columns:
      for row_index, row in enumerate(self.values):
        for column_index, value in enumerate(row):
          self.values[row_index][column_index] += other.values[row_index][column_index]
    else:
      print 'Cannot add a matrix by another with different dimensionality.'

    return self

  def __times_scalar(self, scalar):
    for row in self.values:
      for index, value in enumerate(row):
        row[index] *= scalar

    return self

  def __times_matrix(self, other):
    if other.n_rows == self.n_columns:
      result_matrix = Matrix(self.n_rows, other.n_columns)
      for row_index, row in enumerate(self.values):
        for other_column_index in range(other.n_columns):
          result_matrix.values[row_index][other_column_index] = 0
          for column_index, value in enumerate(row):
            result_matrix.values[row_index][other_column_index] += value * other.values[column_index][other_column_index]
      return result_matrix
    else:
      print 'Can only multiply a matrix with shape NXM by another with shape MXO'

    return self
