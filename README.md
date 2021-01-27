# OSCAR
#### The Ostensibly Smart Computer Aided Recycler

## DSI1019 Capstone Project by Billy Horn
---
## Welcome!

Hello and welcome to the OSCAR repo! OSCAR is an open-source project consisting of ML models, applications and websites to help combat recycling contamination. At its foundation, OSCAR is an image classifier pre-trained to categorize pictures of garbage. Please read further to find out more!

<img src="./images/trash.jpg" alt="image" width="600"/>

## Problem Statement

Recycling contamination occurs when items end up in a [single-streamed](https://en.wikipedia.org/wiki/Single-stream_recycling) recycling bin that cannot be processed by its destined facility. Aside from the typical garbage contaminants, other examples of recycling contamination include plastic bags, plastic film, electronics and plastic utensils, to name a few.

Recycling contaminants can vary depending on region due to different municipality accommodations and product availability. In the city of San Diego, CA, it is estimated that 15 - 17% of collected recyclables are contaminants, which equates to 10,000 tons of trash annually ([source](https://www.voiceofsandiego.org/topics/news/the-city-sends-about-15-percent-of-the-recycling-it-collects-to-the-dump/)). The recycling facilities separate the items they cannot process and send them to the landfill, even if they could be recycled by a different facility. The strain on the recycling industry is real, threatening its viability due to increased processing costs and lower return on the recycled product.([source](https://mediaroom.wm.com/the-battle-against-recycling-contamination-is-everyones-battle/)).

 The Ostensibly Smart Computer Aided Recycler (OSCAR) project is offered as an aid to mitigate recycling contamination, aiming to cutoff improper sorting at the consumer. With the aid of a convolutional neural network trained on images of garbage, OSCAR will attempt to classify images into six categories:\
*glass, metal, cardboard, paper, plastic, trash*\
With a crowd-soured data set planned via the [`website`](#website) portion of this repo, the OSCAR project hopes to amass enough categorized images to predict if an item can be recycled or not (stretch goal).

OSCAR can been deployed to portable iOS devices using the demo app found in the [`app`](#app) section of this repo.

## Table of Contents
- [Software Requirements](#software-requirements)
- [Methods of Analysis](#methods-of-analysis)
- [Data](#data)
- [Website](#website)
- [App](#app)
- [Findings and Conclusions](findings-conclusions)

## Software Requirements
    - jupyter notebooks:
        • tensorflow
        • numpy
        • matplotlib
        • PIL
        • pandas
    - application
        • XCode
        • CreateML


## Methods of Analysis

The OSCAR model is built with a Convolutional Neural Network. Two models constructed with TensorFlow can be found within the Jupyter Notebooks of the [`notebooks`](./notebooks) section of this repo. A model using CreateML can be found within the [`app`](./app) section of this repo. The models are assessed using the accuracy and precision metrics. Accuracy is used to determine how well the model is performing on all categories, and precision is used to determine how well each class is performing. Accuracy and precision were chosen as metrics because the true positives and true negatives are important for OSCAR's use as they can tell you what can and cannot be recycled.  

## Data
### Due to the size of the data set, it has not been included in this repo. Please follow the link below for downloading.

The data set from this project consists of over 2,500 total images separated into the five categories mentioned above. The images were collected and shared by [**Gary Thung**](https://github.com/garythung) and [**Mindy Yang**](https://github.com/yangmindy4) for their paper ( [**link**](http://cs229.stanford.edu/proj2016/poster/ThungYang-ClassificationOfTrashForRecyclabilityStatus-poster.pdf) ). More information on the data set and a download link can be found [**here**](https://github.com/garythung/trashnet#dataset).

## Website

The website is intended as a crowd-sourcing tool to build a robust data set of images. Users can post images of recyclables or trash, and then vote on images to help classify them manually. Most of the code for the website is included, however I've omitted secret keys for security reasons, and omitted the tensorflow models due to space constraints.

If you wish to test the website, you would need to create unique secret keys, and export the tensorflow model from the `notebooks` section of this repo. Please reach out for more information.

The website was built by augmenting the excellent django tutorial by Corey Schafer. Code may be identical or similar to code found in this tutorial ([source](https://www.youtube.com/channel/UCCezIgC97PvUuR4_gbFUs5g)).


## App

The app is for iOS devices only and can be accessed through demo mode in XCode. Open the XCode project in the `app` section of this repo, select the operating system you would like to test (through iOS14), and select `run`.
All code for the application was taken from the Apple CoreML image classifier tutorial ([source](https://developer.apple.com/documentation/vision/classifying_images_with_vision_and_core_ml)).

## Findings and Conclusions

The model chosen to be OSCAR's deployable model was the CreateML model because it had the highest testing accuracy with minimal overfitting. The testing accuracy of 90% far exceeded the baseline accuracy of any category. See tables of results below:

|**Model**|**Train Accuracy**|**Test Accuracy**|
|---|---|---|
|Tensorflow|82.6%|78.5%|
|CreateML|92.8%|89.9%|

|**Class**|**Baseline Scores**|
|---|---|
|Cardboard|16%|
|Glass|20%|
|Metal|16%|
|Paper|23.5%|
|Plastic|19%|
|Trash|5.4%|

However, the CreateML model was not without its faults. Even though the testing accuracy was at 90%, the precision of the Trash class was exceptionally underperforming (see table below). I believe this is due to the imbalanced quantity of data for this category, combined with not enough data reserved for testing (I could not figure out how to change this option in CreateML, but will be added to my improvement to-dos).

|**Class**|**Precision**|
|---|---|
|Cardboard|100%|
|Glass|91%|
|Metal|93%|
|Paper|90%|
|Plastic|84%|
|Trash|25%|

At 138 pictures, the Trash category consisted of a maximum of 25% of the other categories. For instance, the Glass category had 500+ images. With this imbalance, the model could not learn the images of trash as well as the other classes and underperformed in the category as a result.

Even though this model performed well overall, it is apparent more images need to be collected for proper training. Hopefully with the crowd-sourcing effort of manually gathering data, OSCAR can one day be trained on 20,000+ images.

Aside from gathering more data, the next steps for this project include implementing educational tags within the iOS application to help the end user become more aware of what can and cannot be recycled, researching ways to improve the TensorFlow model, and working with the local municipality to determine what can and cannot go into the single-streamed recycling bins so it can be incorporated into the app's functionality.
