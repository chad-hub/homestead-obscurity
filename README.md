# Homestead-Obscurity
Using deep learning to classify home architecture

## Tech Stack
<p align="center">
 <img src="/eda_plots/teach_stack.png" alt="drawing" width="800"/>
</p>

## Inspiration

<p align="center">
  <img src="/eda_plots/hagia_sophia.PNG" alt="drawing" width="300"/>
  <img src="eda_plots/duomo.png" alt="drawing" width="300"/>
</p>

Convolutional Neural Networks (CNNs) are especially good at processing images by featuring their shapes, edges, curves, and depth. As I have learned more about CNNs and applied them throughout my work, I found myself wanting to look deeper at these networks while applying them to something I find personally interesting. Architecture is the perfect means with which to explore this deeper. I've been fortunate to have traveled many places all over the world and experienced a wide variety of cultures. While traveling, I was always drawn to the unique architectures associated with different cultures - and how they became the pride of each location. I chose to process images of different home architectural styles. My reasoning:
  1) There are many home architectures that have very distinguishing features
  2) There are many resources for home images
  
 ## Data
 | Architecture | Train Images | Test Images |
 |--------------|--------------|-------------|
 | Tudor | 508 | 40 |
 | Modern | 600 | 49 |
 | Victorian | 476 | 41 |
 | Ranch | 426 | 42 |
 | Modern | 500 | 40 |
 
 Sources: Zillow.com, google images, Bing images, Pinterest
 
<p align="center">
  <img src="/eda_plots/tudor.png" alt="drawing" width="250" height="250"/>
  <img src="eda_plots/modern.PNG" alt="drawing" width="250" height="260"/>
  <img src="eda_plots/victorian.PNG" alt="drawing" width="250" height="250"/>
</p>
<p align="center">
  <img src="eda_plots/ranch.png" alt="drawing" width="250" height="280"/>
  <img src="eda_plots/cap_cod.PNG" alt="drawing" width="250" height="250"/>
</p>

I've highlighted what I believe to be the most prominent and distinguishing features exhibited by the five home styles I selected. I sought out images that were consistent with these features and opted for the photos that most centrally displayed the homes. 

## Data Augmentation

My corpus of images is small, especially in the realm of neural network training. To prevent over-fitting and introduce more variety for the model to train on, I applied an image augmentation protocol into my image processing pipeline. The augmentation randomly zooms in, shifts along vertical and horizontal axis, randomly horizontal flips, and slightly rotates images. See example below.

<p align="center">
  <img src="/eda_plots/image_augmentation.PNG" alt="drawing" width="600" />
</p>

## EDA
As I mentioned, architecture is defined by its lines, shapes and edges. As such, edge recognition / detection is an important feature that will have to be extracted. Prior to running the images through the 'black box' of a CNN, I wanted to see if the prominence of the edges I identified in each image would indeed shine through with some basic edge detection. 

| Modern Home Edge Detection |
|----------------------------|
| ![modern_edges](eda_plots/modern_home_edges.png) |

| Tudor Home Edge Detection |
|----------------------------|
| ![tudor_edges](eda_plots/tudor_home_edges.png) | 

| Victorian Home Edge Detection |
|----------------------------|
| ![victorian_edges](eda_plots/victorian_home_edges.png) | 

As expected, the prominent features of the home types above are evident in the edge detection filters. 

## CNNs

CNNS are widely regarded for their ability to efficiently process images. In fact, they were originally modeled after how neurons in the visual cortex interact. Research by David H. Hubel and Torstein Wiesel in the late 1950s proved that neurons in the visual cortex have a small receptive field, and react only to specific shapes. Different neurons react to different shapes, and together they form the visual field. Their research also showed that some neurons react to more complex patterns, and that these patterns were combinations of the simpler shapes perceived by other neurons. 

<p align="center">
  <img src="/eda_plots/home_cnn.png" alt="drawing" width="600" height="300"/>
</p>
 
In the above illustration, each individual filter will travel the entirety of the image, capturing the filters respective patterns and aggregating that information into what are called activation maps, or convolutions. A helpful analogy is to think about polarized sunglasses: only the light that is aligned with the orientation of the polarized lens reaches our eyes. These activation maps are then pooled, which is a downsizing operation. The pooling captures the strongest signals in the activation maps and then reduces the size of the convolution. At shallow depths, these activation maps capture simple shapes, lines, edges, etc. These are called 'spatial patterns'. In and of themselves, these spatial patterns do not provide a whole lot of insight. As we include more and more convolutional layers, however, these activation maps begin to capture more complex, or 'cross-channel' patterns. Keeping with the architecture analogy, shallow layers capture a sharp angle, line, or edge, and as we get deeper, we begin to see a door, window, and house begin to form. After the pooling layer, we flatten out the information and connect it to our classifications - 5 in our case. 

## Transfer Learning
The true power of CNNs are most evident when we employ transfer-learning. With transfer learning, we utilize a pre-trained network and adjust it for our needs. There are many readily available models to choose from, but I was most interested in, and had the best success with the Xception architecture (Francois Chollet - 2016). This model is trained on 350 million images and around 17,000 classes, and heavily features separable convolutional layers. While traditional convolutional layers use filters that try to simultaneously capture spatial and cross-channel patterns, separable layers strongly assumes that the spatial and cross-channel patterns can be modeled separately. 

<p align="center">
  <img src="/eda_plots/xception.PNG" alt="drawing" width="300"/>
</p>

 Once I loaded in the Xception network, I began adjusting the layers to meet the requirements of my project. This involved removing the final layer, replacing with a dense (fully connected) layer and SoftMax activation with five classifications (one for each home type), and freezing the remaining layers from being able to train. Every other layer was frozen because, as a pre-trained model, it already has all the learned shapes / lines / edges built in. SoftMax activation converts the final output layer of the neural network into probabilities in classification scenarios. These probabilities tell us which classification the model picks, as well as the confidence with which the pick was made. 
 
 ## Transfer Learning + Fine Tuning
 After the minimal tweaking of the Xception model, I wanted to train the model to get a base line transfer learning accuracy. Below is a plot of the training and validation loss / accuracy. 
 
 <p align="center">
  <img src="/eda_plots/final_xception_pre_ft.png" alt="drawing" width="450"/>
</p>

In 10 epochs, allowing no adjustment to the weights in all of the built in layers of Xception, the validation accuracy approached 80% accuracy, an extremely impressive result. The next step was to begin unfreezing some of the layers in Xception to allow the model to adjust it's parameters to better classify the categories required. I also adjusted the learning rate, which controls how aggressively the model can adjust the pre-trained components of the model. In general, smaller learning rates are recommended when fine tuning a transfer learning model to fight over-fitting. Below are the same plots, but I have added a line indicating when I allowed the model to unfreeze layers and begin adjusting the pre-trained Xception weights. 

| Learning Rate 0.00001 | Learning Rate 0.0001 |
| ----------------------|----------------------|
| ![lr_0.00001](eda_plots/fine_tuning_lr_0.00001.png) | ![lr_0.0001](eda_plots/fine_tuning_lr_0.0001.png) |

| Learning Rate 0.001 | Learning Rate 0.01 |
| ----------------------|----------------------|
| ![lr_0.001](eda_plots/fine_tuning_lr_0.001.png) | ![lr_0.01](eda_plots/fine_tuning_lr_0.01.png) |


There are some signs of over-fitting / confusion with the learning rate going down to 0.01. For this reason, I opted to keep the learning rate at 0.001 - yielding the best results. 

## Transfer Learning Results
 
<p align="center">
  <img src="/eda_plots/final_Xception_conf_M.png" alt="drawing" width="600"/>
</p>
 
 A perfect confusion matrix would have all solid dark blue along the diagonal, so the model is performing exceptionally well. The best accuracy I was able to achieve was 84%.
 
 <p align="center">
  <img src="/eda_plots/xception_pred_victorian.png" alt="drawing" width="300" height="300"/>
  <img src="/eda_plots/xception_pred_tudor.png" alt="drawing" width="300" height="300"/>
</p>
 
## My Own CNN
 
I knew full well that achieving anything close to the success of transfer-learning would be nearly impossible in the scope of this assignment. However, my goal in this project is to peek into the black box and understand what an excellent model reveals in the images and what a basic model from scratch would reveal. The basic structure of my base CNN is as follows:
 
<p align="center">
 <img src="/eda_plots/baseline_cnn.PNG" alt="drawing" width="800"/>
</p>
 
## Training
 
I introduced the same image corpus to train my model, and the resulting accuracy was to be expected:
 
<p align="center">
 <img src="/eda_plots/base_model_train.png" alt="drawing" width="2000" height="500"/>
</p>
 
The model struggled to converge, and the accuracy rarely achieved a value greater than random. 
 
 
## Results
 
<p align="center">
  <img src="/eda_plots/baseline_results.PNG" alt="drawing" width="600"/>
</p>
<p align="center">
  <img src="/eda_plots/baseline_predict_tudor.png" alt="drawing" width="300" height="300"/>
  <img src="/eda_plots/baseline_predict_modern.png" alt="drawing" width="300" height="300"/>
</p>
 
 Note that the model predicted modern homes for all the validation set classes. All of these predictions were made with very low probability, just above 1/5 as expected based on the confusion matrix and model accuracy. In observing the images, it's understandable why the baseline model mostly strongly captured the modern style home features. Most of the modern home images were clear of any trees or shrubbery around the home obscuring the image. Modern homes are the clearest photos, with prominent horizontal and vertical lines. Because every other home features these same lines somewhere on the house, the misclassification makes sense.
 
 ## Peek in the Black Box
 
<p float="center">
  <img src="/eda_plots/layer_2_activations.PNG" alt="drawing" width="1000"/>
  <img src="/eda_plots/layer_5_activations.PNG" alt="drawing" width="1000"/>
</p>

The above images are a sampling of the outputs from activation layers 2 and 5 for a tudor-style home, in Xception and my baseline model. It is now clear why my model struggled mightily to distinguish between any of the features of the houses. Why exactly are most of the images in the baseline model completely blacked out? It has to do with the activation function specified in the neural networks. Generally, activation functions are how we introduce non-linearity to the model. Activation functions take the input from the convolution step and adjust the outputs according to the specified function. Rectified Linear Unit (ReLu) activation is very common in CNNs, and is what I employed in my model. Below is a visual representation of ReLu. 

<p align="center">
  <img src="/eda_plots/relu.png" alt="drawing" width="400"/>
</p>

So any value that is negative, or does not contribute positively to feature determination, gets zeroed out. This zeroing out explains the blacked-out images in my model above.  
## Conclusion

It is entirely feasible to use CNNs to classify home architecture styles. The most successful method is to employ transfer-learning with minor fine tuning. I also suggest that thousands more images would benefit the accuracy of the model. Another procedure that would increase accuracy is to include bounding boxes in the images. Bounding boxes, as shown below, tell the model exactly where to look for when training, and what we want the model to focus on for classification. 

<p align="center">
  <img src="/eda_plots/bounding_box.PNG" alt="drawing" width="450"/>
</p>

Bounding boxes eliminate any confusion caused by trees, grass, or shrubbery surrounding the home.  
