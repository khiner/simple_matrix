import csv
from matrix import Matrix

class CsvMatrixReader:

  @staticmethod
  def read_matrix(file_path, delimiter = ','):
    matrix = Matrix()
    if not file_path.endswith('.csv'):
      print 'Don\'t know how to read ' + file_path + '.'
      return matrix

    with open(file_path, 'rb') as csvfile:
      spamreader = csv.reader(csvfile, delimiter = delimiter, quotechar='|')
      for row in spamreader:
        matrix.append_row(map(float, row))

    return matrix
