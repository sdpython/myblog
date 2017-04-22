/*
see http://pig.apache.org/docs/r0.7.0/tutorial.html  (pig commands)
see Azure and Map/Reduce http://www.youtube.com/watch?v=TC0LK1nXzIw 
see http://blog.cloudera.com/blog/2012/10/whats-new-in-cdh4-1-pig/
*/
REGISTER ./tutorial.jar;

raw_velib = 
    LOAD 'velib_20r.txt'
    USING PigStorage('\t') 
    AS (address, 
        available_bike_stands:int, 
        available_bikes:int, 
        banking, 
        bike_stands, 
        bonus, 
        last_update, 
        lat:double, 
        lng:double, 
        name, 
        number:int, 
        status);
        
stations_group = 
    GROUP raw_velib 
    BY (name, status);
    
stations_count = 
    FOREACH stations_group 
    GENERATE flatten($0), COUNT($1) as count;
    
STORE stations_count 
INTO 'stations_count_2013-05-24.paris.short.pig.2.txt' 
USING PigStorage(); 
    
