# Download all the stuff we need
Docker: https://www.docker.com/  
gitbash: https://git-scm.com/downloads  
VSCode: https://code.visualstudio.com/  
# Cloning the FILE to your own FILE
`git clone https://github.com/quang-ute/myprojects.git`  
  => Remember to clone this file where you can access for later on!
# Starting composing the file
- Go to .../yourpath/myprojects and do `docker run -it --privileged -v $HOME/Seclabs:/home/seed/seclabs img4lab`  
  ![image](https://github.com/user-attachments/assets/ea29da59-c312-4296-a915-eb0f5ca7fc12)
# Create your folder to maintain your workflow
- Firstly, check go to the your *Users* by doing `cd ~`  
  ![image](https://github.com/user-attachments/assets/a8a820a9-4ed3-4205-a25f-55732a17dccf)
- If you have created the seclabs file then nothing to do! If not, please type `mkdir -p $HOME/Seclabs`  
  ![image](https://github.com/user-attachments/assets/2c4703e3-a487-4bd9-8375-caab678ec573)
- Go to .../yourpath/myprojects and do `docker run -it --privileged -v $HOME/Seclabs:/home/seed/seclabs img4lab`  
  ![image](https://github.com/user-attachments/assets/fbbd6d8c-cb7e-4914-80d1-8b6ec737ced2)
  => You have finished the initialization step! Remember to use `cd seclabs` after to get in the files!
