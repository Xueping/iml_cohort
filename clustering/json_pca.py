'''
Created on 3 Nov 2017

@author: xuepeng
'''

import codecs, json 

def generateJson(data,outputPath):    

#     tolist = data.tolist() # nested lists with same data, indices
    json.dump(data, codecs.open(outputPath, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
    


if __name__ == "__main__":
    data  = [[12, 23, 34],
             [12, 43, 56]]
    outputPath = "../data/kmeans_pca.json"
    generateJson(data,outputPath)