rsync --log-file=$HOME/src/lago.log --remove-source-files -aPv $HOME/src/*.bz2 luthier@10.73.22.106:/disks/Exp/Lago/Argentina/bariloche/

#rsync --log-file=swgo.log --remove-source-files -aPv *.bz2 arnaldi@10.73.22.159:~/work/data/lago/rp/spnk/

#rsync -avP --remove-source-files --size-only --include="*.bz2" --exclude="*" . arnaldi@10.73.22.159:/home/arnaldi/work/data/lago/rp/spnk/
