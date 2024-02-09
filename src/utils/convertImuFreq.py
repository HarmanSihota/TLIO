# Converts data collected at some higher frequency to a lower frequency
# call convertAllFreqData and then convertAllDataDescriptions with your new and old frequency to create the new files

import numpy as np
import os
import sys
import json

def convertFreq(freq_ratio: int, path_original: str, path_new: str):
  arr = np.load(path_original, mmap_mode='c')
  newArr = []

  for i in range(len(arr)):
    if i % freq_ratio == 0:
      newArr.append(arr[i])
  
  newArr = np.array(newArr)
  np.save(path_new, newArr)


def convertAllFreqData(oldFreq: float, newFreq: float, path_base: str):
  freq_ratio = oldFreq/newFreq
  if not freq_ratio.is_integer():
    print("old freq must be a multiple of new freq")
    return
  
  freq_ratio = int(freq_ratio)
  dir_base = os.scandir(path_base)

  for entry in dir_base:
    if entry.is_dir():
      path_original = os.path.join(path_base, entry.name, 'imu0_resampled.npy')
      path_new = os.path.join(path_base, entry.name, f'imu0_resampled_adjusted_{newFreq}Hz.npy')
      convertFreq(freq_ratio, path_original, path_new)


def test_conversion(oldFreq: float, newFreq: float, path_base: str):
  freq_ratio = oldFreq/newFreq
  if not freq_ratio.is_integer():
    print("old freq must be a multiple of new freq")
    return
  
  freq_ratio = int(freq_ratio)
  dir_base = os.scandir(path_base)

  for entry in dir_base:
    if entry.is_dir():
      path_original = os.path.join(path_base, entry.name, 'imu0_resampled.npy')
      path_new = os.path.join(path_base, entry.name, f'imu0_resampled_adjusted_{newFreq}Hz.npy')
      checkFreq(freq_ratio, path_original, path_new)

  print("PASSED")

def checkFreq(freq_ratio: int, path_original: str, path_new: str):
  origArr = np.load(path_original, mmap_mode='c')
  newArr = np.load(path_new, mmap_mode='c')

  j = 0
  for i in range(len(newArr)):
    for k in range(len(newArr[i])):
      if origArr[j][k] != newArr[i][k]:
        print(f"ERROR in {path_new} at line {i}")
        sys.exit(1)
    j += freq_ratio 


def convertAllDataDescriptions(newFreq: float, path_base: str):
  dir_base = os.scandir(path_base)

  for entry in dir_base:
    if entry.is_dir():
      path_original = os.path.join(path_base, entry.name, 'imu0_resampled_description.json')
      path_new = os.path.join(path_base, entry.name, f'imu0_resampled_adjusted_{newFreq}Hz_description.json')
      arr_to_be_described = np.load(os.path.join(path_base, entry.name, f'imu0_resampled_adjusted_{newFreq}Hz.npy'), mmap_mode='c')
      num_rows = arr_to_be_described.shape[0]
      convertJson(newFreq, path_original, path_new, num_rows)


def convertJson(newFreq: float, path_original: str, path_new: str, num_rows: int):
  newJsonObj = None
  with open(path_original, 'r') as oldJsonFile:
    oldJsonObj = json.load(oldJsonFile)
    newJsonObj = oldJsonObj.copy()
    newJsonObj['approximate_frequency_hz'] = newFreq
    newJsonObj['num_rows'] = num_rows
  
  with open(path_new, 'w') as newJsonFile:
    json.dump(newJsonObj, newJsonFile, ensure_ascii=False, indent=4)

if __name__ == "__main__":
  pass
