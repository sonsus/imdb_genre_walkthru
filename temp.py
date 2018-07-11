

def count_qa(mv_key, qa_list):
    n_qa = 0
    for qa in qa_list:
        if qa['imdb_key'] == mv_key: 
            n_qa+=1
    return n_qa

def update_datacube(*):
    if mv_key in train_ids:
        elem_idx[1] = split2idx['train']
    elif mv_key in val_ids:
        elem_idx[1] = split2idx['val']
    elif mv_key in test_ids:
        elem_idx[1] = split2idx['test']
    else: 
        exit("wtf mv_key is this? its nowhere!")

    for genre in imdb_data[mv_key]['genre_list']:
        elem_idx[2] = genre2idx[genre]
        
        #only works when clip exists
        if mv_key in clip_exist_list:
            elem_idx[0] = entity2idx["n_cl_movie"]
            datacube[tuple(elem_idx)] += 1
            
            elem_idx[0] = entity2idx["n_clip"]
            datacube[tuple(elem_idx)] +=  imdb_data[mv_key]["num_clips"]
            
            elem_idx[0] = entity2idx["l_clip"]
            datacube[tuple(elem_idx)] += sum(imdb_data[my_key]["clip_duration"])

            elem_idx[0] = entity2idx["n_cl_qa"]
            datacube[tuple(elem_idx)] += count_qa(mv_key, qa_list)
        
        #include movies w/o clips
        elem_idx[0] = entity2idx["n_movie"]
        datacube[tuple(elem_idx)]+=1

        elem_idx[0] = entity2idx["n_qa"]
        datacube[tuple(elem_idx)]+= count_qa(mv_key, qa_list)            