#! /usr/bin/awk -f

#########################################################################
#        avgsize.awk     |    Joshua Westgard    |     2014-05-27       #
# --------------------------------------------------------------------- #
# This script reads directory listings and counts files of specified    #
# type(s), totaling the size in bytes, and returning an average size in #
# megabytes. Assumes tab-separated input files, with filename in 1st	#
# column and size in bytes in 3rd. Run with:				            #
# 	            $ awk -f avgsize.awk [file(s) to analyze]			    #
#########################################################################

BEGIN	    { 	FS="\t";	# set field separator to tab char
                };

$1~/\.jpg$/ { 	jc+=1;		# jc = jpg count (increment when "jpg" in col 1)
                jb+=$3		# jb = byte sum of all jpgs
                }; 

$1~/\.tif$/ {	tc+=1;		# tc = tif count (increment when "tif" in col 1)
                tb+=$3 		# tb = byte sum of all tifs
                };

END 	    {	ta=tb/tc;	# ta = tif count / tif bytes
                ja=jb/jc;	# ja = jpg count / jpg bytes
                printf "\n";
                printf "TOTAL BYTES / NO. FILES = AVG. FILE SIZE\n"
                printf "----------------------------------------\n"
                printf "TIFs: %s / %s = %.2f MB\n", tb, tc, ta/2**20;	# print res. in MB
                printf "JPGs: %s / %s = %.2f MB\n", jb, jc, ja/2**20;	# for ea. file type
                printf "\n"
                }