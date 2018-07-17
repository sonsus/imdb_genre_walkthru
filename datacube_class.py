import json 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.core.debugger import set_trace

class Datacube:
    def __init__(self, imdb_dict, qa_list, ds_split_dict, clip_exist_list ):
        super().__init__()
        # imdb_dict.keys() = ['data', 'genre_dictionary']

        # jsons into dicts
        self.imdb_dict = imdb_dict
        self.qa_list = qa_list
        self.ds_split_dict = ds_split_dict
        self.clip_exist_list = clip_exist_list

        #shortcuts (mostly lists)
        self.train_ids = self.ds_split_dict['train']
        self.val_ids = self.ds_split_dict['val']
        self.test_ids = self.ds_split_dict['test']

        self.imdb_data = self.imdb_dict['data'] # python dict
        self.genre_list = self.imdb_dict['genre_dictionary']
        self.entity_list = ["n_clip", "l_clip",
                       "n_cl_movie", "n_movie",
                       "n_qa", "n_cl_qa",]

        #str to idxs
        self.genre2idx = dict( zip( self.genre_list, range(len(self.genre_list))  )  )
        self.split2idx = {"train":0, "val":1, "test":2}
        self.entity2idx = dict( zip( self.entity_list, range(6) ) )

        # Datacube finally ! 
        # has 6,3,20 which corresponds to below
        self.datacube_shape = (len(self.entity2idx), len(self.split2idx), len(self.genre2idx))
        self.elem_idx = [None for i in range(3)] #initialization. to be updated
        self.datacube = np.zeros(self.datacube_shape)



    def count_qa(self, mv_key): #used for counting qa in qa_list 
        n_qa = 0
        for qa in self.qa_list:
            if qa['imdb_key'] == mv_key: 
                n_qa+=1
        return n_qa


    def update_datacube(self, mv_key): #used for feeding datacube while walking thru imdb_data
        if mv_key in self.train_ids:
            self.elem_idx[1] = self.split2idx['train']
        elif mv_key in self.val_ids:
            self.elem_idx[1] = self.split2idx['val']
        elif mv_key in self.test_ids:
            self.elem_idx[1] = self.split2idx['test']
        else: 
            exit("wtf mv_key is this? its nowhere!")

        for genre in self.imdb_data[mv_key]['genre_list']:
            self.elem_idx[2] = self.genre2idx[genre]
            
            #only works when clip exists
            if mv_key in self.clip_exist_list:
                self.elem_idx[0] = self.entity2idx["n_cl_movie"]
                self.datacube[tuple(self.elem_idx)] += 1
                
                self.elem_idx[0] = self.entity2idx["n_clip"]
                self.datacube[tuple(self.elem_idx)] += self.imdb_data[mv_key]["num_clips"]
                
                self.elem_idx[0] = self.entity2idx["l_clip"]
                self.datacube[tuple(self.elem_idx)] += sum(self.imdb_data[mv_key]["clip_duration"])

                self.elem_idx[0] = self.entity2idx["n_cl_qa"]
                self.datacube[tuple(self.elem_idx)] += self.count_qa(mv_key)
            
            #include movies w/o clips
            self.elem_idx[0] = self.entity2idx["n_movie"]
            self.datacube[tuple(self.elem_idx)]+=1

            self.elem_idx[0] = self.entity2idx["n_qa"]
            self.datacube[tuple(self.elem_idx)]+= self.count_qa(mv_key)
        return None 

    def np_2_dataframe(self, entity_of_interest): # entity of interest is "str"
        # entity to see in df. we see df for chosen entity of tr/v/test vs genre (3 x 20)
        datacube_slice = self.datacube[self.entity2idx[entity_of_interest], :, : ]
        df = pd.DataFrame(datacube_slice)

        rownaming =  dict (zip( range(len(self.split2idx)) , self.split2idx.keys()))
        colnaming =  dict (zip( range(len(self.genre2idx)) , self.genre2idx.keys()))
        #set_trace()
        df = df.rename(index=rownaming, columns=colnaming)
        return df

    def df_dict(self):
        return dict(zip(self.entity_list, [self.np_2_dataframe(entity) for entity in self.entity_list]))

    def run_analysis(self):
        for mv_key in self.imdb_data.keys():
            self.update_datacube(mv_key)
        return self.df_dict()

    #need redesign
    def show(self, df_dict, entity, genre_band, stacked=False): # genre_band is 0,1,2,3 : 1 shows 0~4 genre, 2shows 5~9 genre, so on to whole 19 genre
        #plt.figure()
        column_selector = self.genre_list[10*(genre_band) :10*(genre_band+1)]
        df_dict[entity][:][column_selector].plot.bar(stacked = stacked)
        plt.title("{e} _ genre: {s_}~{s}/20".format(e=entity, s_=str(10*(genre_band)+1), s=str(10*(genre_band+1))) )
        #print(df_dict[entity][:][column_selector])
    