#!/usr/bin/env python

from matrix import Matrix
from csv_matrix_reader import CsvMatrixReader

matrix = Matrix([[1,2], [2,3], [3,4]])
print matrix
print 'transposed'
print matrix.transpose()
other_matrix = Matrix([[1,2,3], [2,3,4]])
print '*'
print other_matrix
print '='
print matrix * other_matrix

square_matrix = Matrix([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]])
identity_matrix = Matrix([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
print square_matrix
print '*'
print identity_matrix
print '='
print square_matrix * identity_matrix
square_matrix.append_row([1,2,3,4,5,6])
print 'not square anymore'
print square_matrix
square_matrix.append_column([1,2,3,4,5,6])
print 'square again!'
print square_matrix

matrix = CsvMatrixReader.read_matrix('test.csv')
print 'imported matrix'
print matrix
matrix.normalize_min_max()
print 'min-max normalized'
print matrix
matrix.normalize_mean()
print 'mean-normalized'
print matrix

print 'max'
print matrix.max()
print 'min'
print matrix.min()

print 'size'
print matrix.size()

print 'identity'
print Matrix.identity(5)
print -Matrix.identity(5)

print 'zeros'
print Matrix.zeros(2,3)
print 'ones'
print Matrix.ones(3,2)

print 'equal?'
print Matrix.ones(3,3) == Matrix.zeros(3,3)
print Matrix.ones(3,3) == Matrix.ones(3,3)

print 'not equal?'
print Matrix.ones(3,3) != Matrix.ones(3,3)

