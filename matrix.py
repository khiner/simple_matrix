class Matrix:
  def __init__(self, n_rows_or_list = 0, n_columns = 0):
    if isinstance(n_rows_or_list, list):
      self.n_rows = len(n_rows_or_list)
      if self.n_rows > 0 and isinstance(n_rows_or_list[0], list):
        self.n_columns = len(n_rows_or_list[0])
      else:
        self.n_columns = 1
    else:
      if isinstance(n_rows_or_list, (int, long)):
        self.n_rows = n_rows_or_list
        self.n_columns = n_columns
      else:
        print 'Don\'t know what to do with a ' + type(n_rows_or_list) + ' constructor. Defaulting to an empty 0-d matrix'
        self.n_rows = self.n_columns = 0

    self.rows = [[0 for i in range(self.n_columns)] for j in range(self.n_rows)]
    if isinstance(n_rows_or_list, list):
      for row_index, row_value in enumerate(n_rows_or_list):
        if isinstance(row_value, list):
          for column_index, column_value in enumerate(row_value):
            self[row_index][column_index] = column_value
        else:
          self[row_index][0] = row_value

  def __add__(self, other):
    if isinstance(other, Matrix):
      return self.__plus_matrix(other)
    elif isinstance(other, (int, long, float, complex)):
      return self.__plus_scalar(other)
    else:
      print 'Do not know how to add a ' + type(other) + ' to a matrix.'
      return self

  def __sub__(self, other):
    if isinstance(other, Matrix):
      return self.__minus_matrix(other)
    elif isinstance(other, (int, long, float, complex)):
      return self.__plus_scalar(-other)
    else:
      print 'Do not know how to subtract a ' + type(other) + ' from a matrix.'
      return self

  def __mul__(self, other):
    if isinstance(other, Matrix):
      return self.__times_matrix(other)
    elif isinstance(other, list):
      return self.__times_matrix(Matrix(other))
    elif isinstance(other, (int, long, float, complex)):
      return self.__times_scalar(other)
    else:
      print 'Do not know how to multiply a ' + type(other) + ' to a matrix.'
      return self

  def __div__(self, other):
    if isinstance(other, Matrix):
      return self.__divided_by_matrix(other)
    elif isinstance(other, list):
      return self.__divided_by_matrix(Matrix(other))
    elif isinstance(other, (int, long, float, complex)):
      return self.__times_scalar(1.0 / other)
    else:
      print 'Do not know how to divide a ' + type(other) + ' to a matrix.'
      return self

  def __neg__(self):
    return self * -1

  def __getitem__(self, index):
    return self.rows.__getitem__(index)

  def __setitem__(self, index, value):
    self.rows.__setitem__(index)

  def __delitem__(self, index):
    self.rows.__delitem__(index)

  def __len__(self):
    return self.rows.__len__()

  def __str__(self):
    string = ''
    for row_index, row in enumerate(self):
      string += '['
      for column_index, value in enumerate(row):
        string += str(value)
        if column_index != self.n_columns - 1:
          string += ' '
      string += ']'
      if row_index != self.n_rows - 1:
        string += "\n"
    return string

  def dot(self, other):
    if other.n_rows == self.n_columns:
      result_matrix = Matrix(self.n_rows, other.n_columns)
      for row_index, row in enumerate(self):
        for other_column_index in range(other.n_columns):
          result_matrix[row_index][other_column_index] = 0
          for column_index, value in enumerate(row):
            result_matrix[row_index][other_column_index] += value * other[column_index][other_column_index]
      return result_matrix
    else:
      print 'Can only take the dot product of a matrix with shape NXM and another with shape MXO'

    return self

  def rows(self):
    return rows

  def columns(self):
    # alternatively, return self.transpose.rows - might even be faster?
    return [[row[column_index] for row in self] for column_index in range(self.n_columns)]

  # returns a 2X1 matrix (vector of length 2) populated with the row & column size of this matrix
  def size(self):
    return Matrix([self.n_rows, self.n_columns])

  def is_vector(self):
    return self.n_columns == 1

  def append(self, new_row):
    return self.append_row(new_row)

  def append_row(self, new_row):
    if isinstance(new_row, (int, long, float, complex)):
      new_row = [new_row] # create a single-element list if input is number
    elif not isinstance(new_row, list):
      print 'Only know how to append lists or numbers to a matrix'
      return

    columns_to_pad = len(new_row) - self.n_columns
    if columns_to_pad > 0:
      # pad existing rows with zeros to match new dimensionality
      for row in self:
        for i in range(columns_to_pad):
          row.append(0)
    elif columns_to_pad < 0:
      # pad new row with zeros to match existing dimensionality
      for i in range(-columns_to_pad):
        new_row.append(0)

    self.rows.append(new_row)
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
      self.append([0] * self.n_columns)
    elif rows_to_pad < 0:
      # pad new row with zeros to match existing dimensionality
      for i in range(-rows_to_pad):
        new_column.append(0)

    for row_index, row in enumerate(self):
      row.append(new_column[row_index])

    self.n_columns += 1
    self.n_rows = len(self)

    return self

  def transpose(self):
    transposed_matrix = Matrix(self.n_columns, self.n_rows)
    for row_index, row_value in enumerate(self):
      for column_index, value in enumerate(row_value):
        transposed_matrix[column_index][row_index] = value

    return transposed_matrix

  # !In-Place!
  # normalization technique, rescale features so each feature will have mean=0 and standard_dev=1
  def standardize(self):
    if self.n_rows <= 1:
      return self # nothing to do - only one row
    for column_index, column in enumerate(self.columns()):
      mean = sum(column) / self.n_rows
      std_dev = (sum([ (value - mean) ** 2 for value in column]) / float(self.n_rows)) ** 0.5
      for row_index, value in enumerate(column):
        if std_dev != 0:
          self[row_index][column_index] = (value - mean) / std_dev
        else:
          self[row_index][column_index] = 0

    return self

  # subtract the mean from each feature value, so each feature will have mean=0
  def normalize_mean(self):
    for column_index, column in enumerate(self.columns()):
      mean = sum(column) / self.n_rows
      for row_index, value in enumerate(column):
        self[row_index][column_index] = value - mean

    return self

  def normalize_min_max(self):
    for column_index, column in enumerate(self.columns()):
      min_value = min(column)
      max_value = max(column)
      value_range = max_value - min_value
      for row_index, value in enumerate(column):
        if value_range != 0:
          self[row_index][column_index] = (value - min_value) / value_range
        else:
          self[row_index][column_index] = 0

    return self

  @staticmethod
  def identity(size):
    identity_matrix = Matrix(size, size)
    for i in range(size):
      identity_matrix[i][i] = 1

    return identity_matrix

  @staticmethod
  def zeros(n_rows, n_columns):
    return Matrix(n_rows, n_columns)

  @staticmethod
  def ones(n_rows, n_columns):
    matrix = Matrix(n_rows, n_columns)
    for row_index in range(n_rows):
      for column_index in range(n_columns):
        matrix[row_index][column_index] = 1

    return matrix

  def __plus_scalar(self, scalar):
    for row in self:
      for index, value in enumerate(row):
        row[index] += scalar

    return self

  def __times_scalar(self, scalar):
    for row in self:
      for index, value in enumerate(row):
        row[index] *= scalar

    return self

  def __plus_matrix(self, other):
    if other.n_rows == self.n_rows and other.n_columns == self.n_columns:
      for row_index, row in enumerate(self):
        for column_index, value in enumerate(row):
          self[row_index][column_index] += other[row_index][column_index]
    else:
      print 'Cannot add a matrix by another with different dimensionality.'

    return self

  def __minus_matrix(self, other):
    if other.n_rows == self.n_rows and other.n_columns == self.n_columns:
      for row_index, row in enumerate(self):
        for column_index, value in enumerate(row):
          self[row_index][column_index] -= other[row_index][column_index]
    else:
      print 'Cannot subtract a matrix by another with different dimensionality.'

    return self

  def __times_matrix(self, other):
    if other.n_rows == self.n_rows and other.n_columns == self.n_columns:
      for row_index, row in enumerate(self):
        for column_index, value in enumerate(row):
          self[row_index][column_index] *= other[row_index][column_index]
    else:
      print 'Cannot multiply a matrix by another with different dimensionality.'

    return self

  def __divided_by_matrix(self, other):
    if other.n_rows == self.n_rows and other.n_columns == self.n_columns:
      for row_index, row in enumerate(self):
        for column_index, value in enumerate(row):
          self[row_index][column_index] /= other[row_index][column_index]
    else:
      print 'Cannot divide a matrix by another with different dimensionality.'

    return self
