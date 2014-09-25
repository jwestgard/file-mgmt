#! /usr/bin/awk -f

#########################################################################
#        tally.awk      |    Joshua Westgard    |      2014-09-25       #
#-----------------------------------------------------------------------#
#    usage: awk -f tally.awk [filename]                                 #
#########################################################################

$3~/[0..9]/   {   gsub(/"/, "", $3); c+=1; t+=$3; print $3
              };
              
END           {   printf "\nTOTAL: %.2f GB for %s files.\n\n", t/2**30, c
              }
