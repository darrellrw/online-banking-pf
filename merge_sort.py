class BalanceMergeSort:  
  def merge(list_data: list, start: int, mid: int, end: int):
    left = list_data[start:mid]
    right = list_data[mid:end]
    left.append((float('inf'), float('inf')))
    right.append((float('inf'), float('inf')))
    i = j = 0
    for k in range(start, end):
      # List berurutan berdasarkan balance [(no_rekening, balance), ...]
      if left[i][1] <= right[j][1]:
        list_data[k] = left[i]
        i += 1
      else:
        list_data[k] = right[j]
        j += 1
  
  @staticmethod
  def sort(list_data: list, start: int = 0, end: int = None):
    if end is None:
      end = len(list_data)
    if end - start > 1:
      mid = (start + end) // 2
      # Rekursif
      BalanceMergeSort.sort(list_data, start, mid)
      BalanceMergeSort.sort(list_data, mid, end)
      BalanceMergeSort.merge(list_data, start, mid, end)