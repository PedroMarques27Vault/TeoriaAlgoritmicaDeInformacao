# TAI_Project3
To run the application, run the compare.py inside the bin folder with some key arguments

    Required/Mandatory:
    
        -s "samples/samplename.wav" -> This sample needs to be available inside the "samples" folder, replace samplename.wav with the wav audio file name 
        -c "compression_method" -> Possible values include bzip2, gzip and zlib
        
    Optional:
    
        -reset -> Generates the signatures for all audio files inside "audio" folder


Project Folders inside bin/:

    audio -> Music database
    signatures -> Contains all signatures for each music in the database ("audio" folder)
    figures -> Plots used for result visualization
    sample_signatures -> folder with all signatures of given samples
    samples -> folder with audio samples to test
    results -> contains some txt results of the algorithm for each compression method


Link to the video presentation:
https://youtu.be/X57F_4C_xq0
