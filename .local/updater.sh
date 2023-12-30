#!/bin/bash
#Script made to connect my local repositories and update the scripts within them
#One may need to further improve this implementation...

# The superset is the "main" repository containing all the scripts. One should improve any code there
# The subset is the repository used for pulling and simulating, so anything should work out of the box...

# It will just work in my local machine, edit it accordingly...
superset=../../magnumnp_scripts
subset=..

# xclean
subdir=file_handlers/xclean
## First, show the differences on the files... 
echo "<<<--- new file  |||||  old file --->>>"
diff "$superset/$subdir/xclean.sh" "$subset/xclean.sh"

read -p "Do you want to replace the old file with the new one? (y/n)" response
if [ "$response" = "y" ] || [ "$response" = "Y" ]; then
	echo "running "
	echo "$superset/$subdir/xclean.sh" "$subset/xclean.sh"
	cp -r "$superset/$subdir/xclean.sh" "$subset/xclean.sh"
	echo "xclean updated!"
fi
# xscreenshot 
#cd $superset/xclean $subset
