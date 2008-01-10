#!/usr/bin/env python
import sys
INF = sys.maxint


##  Rect
##
class Rect:
  
  def __init__(self, x0=-INF, y0=-INF, w=None, h=None):
    self.x0 = x0
    self.y0 = y0
    if w == None:
      self.x1 = INF
    else:      
      self.x1 = x0+w
    if h == None:
      self.y1 = INF
    else:
      self.y1 = y0+h
    return

  def overlap(self, rect):
    return not (rect.x1 <= self.x0 or self.x1 <= rect.x0 or
                rect.y1 <= self.y0 or self.y1 <= rect.y0)


##  ExtSet
##
class ExtSet:
  
  def __init__(self, gridsize):
    self.gridsize = gridsize
    self.grid = []
    return
  
  def cells(self, x0, x1):
    i = int(x0 / self.gridsize)
    x = i * self.gridsize
    while x < x1:
      yield i
      x += self.gridsize
      i += 1
    return
  
  def add(self, x0, x1, obj):
    for i in self.cells(x0, x1):
      self.grid[i].append(obj)
    return
  
  def get(self, x0, x1):
    objs = set()
    for i in self.cells(x0, x1):
      objs.update(self.grid[i])
    return objs

def test_extset():
  e=ExtSet(10)
  assert list(e.cells(-1, 1)) == [-1,0]
  assert list(e.cells(0, 1)) == [0]
  assert list(e.cells(0, 10)) == [0]
  assert list(e.cells(0, 11)) == [0,1]
  assert list(e.cells(1, 11)) == [0,1]
  assert list(e.cells(10, 11)) == [1]
  assert list(e.cells(0, 20)) == [0,1]
  assert list(e.cells(10, 20)) == [1]
  assert list(e.cells(1,21)) == [0,1,2]
  assert list(e.cells(11,21)) == [1,2]
  return


##  ExtGrid
##
class ExtGrid:
  
  def __init__(self, gridsize):
    self.hext = ExtSet(gridsize)
    self.vext = ExtSet(gridsize)
    return
  
  def add(self, rect):
    self.hext.add(rect.x0, rect.x1, rect)
    self.vext.add(rect.y0, rect.y1, rect)
    return
  
  def get(self, rect):
    rects = self.hext.get(rect.x0, rect.x1)
    rects.update_intersect(self.vext.get(rect.y0, rect.y1))
    return rects