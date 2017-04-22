def distance_edition_chemin(mot1, mot2):
    dist = { (-1,-1): 0 }
    pred = { (-1,-1):  None }
    for i,c in enumerate(mot1) :
        dist[i,-1] = dist[i-1,-1] + 1
        pred[i,-1] = (i-1,-1)
        dist[-1,i] = dist[-1,i-1] + 1
        pred[-1,i] = (-1,i-1)
        for j,d in enumerate(mot2) :
            opt = [ ]
            if (i-1,j) in dist : 
                x = dist[i-1,j] + 1
                opt.append( (x, (i-1,j)) )
            if (i,j-1) in dist : 
                x = dist[i,j-1] + 1
                opt.append( (x, (i,j-1) ) )
            if (i-1,j-1) in dist :
                x = dist[i-1,j-1] + (1 if c != d else 0)
                opt.append((x, (i-1,j-1)) )
            mi = min(opt)
            dist[i,j] = mi[0]
            pred[i,j] = mi[1]
    p = (len(mot1)-1,len(mot2)-1)
    chemin = [ ]
    while p != None :
        chemin.append(p)
        p = pred[p]
    chemin.reverse()
    return chemin
    
def distance_edition_recursive(mot1, mot2):
    if len(mot1) == 0 : return len(mot2)
    elif len(mot2) == 0 : return len(mot1)
    else :
        return min ( distance_edition_recursive(mot1[:-1], mot2) + 1,
                     distance_edition_recursive(mot1, mot2[:-1]) + 1,
                     distance_edition_recursive(mot1[:-1], mot2[:-1]) + \
                          (1 if mot1[-1] != mot2[-1] else 0))
    
def dedit_rec(mot1, mot2, cache = None):
    print (len(mot1),len(mot2),cache)
    if len(mot1) == 0 : return len(mot2)
    elif len(mot2) == 0 : return len(mot1)
    else :
        if cache == None : cache = { }
        I = len(mot1)
        J = len(mot2)
        
        cache[I-1,J  ] = cache.get ( (I-1,J  ), dedit_rec(mot1[:-1], mot2, cache) + 1 )
        cache[I,  J-1] = cache.get ( (I  ,J-1), dedit_rec(mot1, mot2[:-1], cache) + 1 )
        cache[I-1,J-1] = cache.get ( (I-1,J-1), dedit_rec(mot1[:-1], mot2[:-1], cache) + \
                            (1 if mot1[-1] != mot2[-1] else 0))
        cache[I,J] =  min ( [ cache[I-1,J], cache[I,J-1], cache[I-1,J-1] ] )
        return cache[I,J]

m1 = "abc"  
m2 = "abc"
print (distance_edition_chemin(m1,m2))
  
m1 = "idstzance"  
m2 = "distances"
print (distance_edition_chemin(m1,m2))
                
m1 = "idstzance"  
m2 = ""
print (distance_edition_chemin(m1,m2))
                                