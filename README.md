# Color_Connected_Components

Sequential Connected Components is a well known classical computer vision algorithm (see cv2::connectedComponents) used to seperate out and label blobs in binary images. However, there are currently no existing implementations that work for greyscale or color images, although theoretical implementations have been propsed (see https://www.researchgate.net/publication/258712492_A_Simple_and_Efficient_Algorithm_for_Connected_Component_Labeling_in_Color_Images). This repository hopes to fix this, by providing an alternate implementation of Sequential Connected Components in python (c++ comming soon) that will work on color or greyscale images. Note that the implementation simply messures connectivity by same exact color, unlike other proposals. This means that it is designed for images where blobs are seperable singular color values, such as images preprocessed by K-means or other forms of clustering, such as objects in Atari Games.




In the future, this may also be integrated with Open CV or Scikit-image's Connected Components Algorithm. However, for now this is just a personal project designed to be used to be used as a preprocessing step for RL agents in classical games from the NES and Atari.



