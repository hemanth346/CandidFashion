# Fashion Search Project - CandidFashion

> This write up is intended as a report of final project for [Full Stack Deep Learning 2021](https://fullstackdeeplearning.com/spring2021/) course. The major focus of the course is to be able to take a model from development to production at scale and explore the current landscape of the ecosystem.



## Project Summary:

Being able to recognize apparel products from pictures could enhance the shopping experience for consumers. This project aim is to create a webapp that makes the apparel items, in given fashion image, available as separate image - ready to be able to search and buy online. Reverse Image search currently has to be done manually using platforms like [lykdat](https://lykdat.com/), but can be integrated as an api service. (Lykdat doesn't have an open APi, but has a twitter bot that can be used)

### https://candid-fashion.herokuapp.com/

## Details:

### Dataset:

- Kaggle compitetion [dataset](https://www.kaggle.com/c/imaterialist-fashion-2020-fgvc7), modified to the usecase. 3 categories of apparels are used for this project to keep it simple.

### Preprocessing pipeline: 

- Masks of the apparel are available in run-length encoded format. Custom dataset class is created to decode the masks and load the images. 

- All the images are resized to 480*720
- Used albumentations library and below augmentation techniques are applied:
    - horizontal_flip (object positional invariance)
    - blur (quality invariance)
    - brightness_range (brightness invariance)
    - channel_shift_range (shade invariance)
    <!-- - cutout(get_random_eraser) (occlusion invariance) - Not used due to implementation issues -->

### Training and experiment tracking:

- For the final model used `resnext101_32x8d` architecture backbone as Encoder using pretrained weights from [here](https://smp.readthedocs.io/en/latest/encoders.html)

- Trained on custom hardware and used _MLflow platform_ for experiment tracking. 

- Models are stored and accessed from S3 bucket.

### Deployment

 > **!!** Most difficult so far has been the frontend. Coming from entirely different background setting up some front end is really very time consuming and a night mare. 


Endpoints were first deployed using [serverless framework](https://www.serverless.com/) on AWS lambda but to host the flask rendered frontend on S3 as static website it has to be build, it didn't work due to multiple dependency and errors.

Later, moved to heroku platform, configured and deployed a flask app which can render frontend as well. Using some starter bootstrap code, created basic pages but connecting other parts is lot of effort and **the front end still remains unfinished**. 

#### Details about serverless deployment can be found [here](https://github.com/hemanth346/CandidFashion/tree/master/api_serverless). 

#### Unfinished local WebUI can be found [here](https://candid-fashion.herokuapp.com/)

#### Repo can be found [here](https://github.com/hemanth346/CandidFashion)

### Future work
- [ ] Get completed UI integrated with backend, better UX and feedback
- [ ] Integrate Reverse image search


### Learnt along the way apart from training a model
- MLflow
- Github actions, precommits
- Sphinx, mkdocs
- Different deployment platforms, nuance involved in connecting frontend to backend
- Infrastructure setup

### Issues faced:
- Data leak during training due to typo which was realized lately
- torch cpu wheel have dependency on the python runtime version in Heroku platfrom, took lot of time to debug and fix
- JS, different implementations(React, AntDesign) to get diverted and confused; the trouble of integrating with front end


Disclaimer:
I do not own any rights to the logo or the name CandidFashion. It is obtained from [here](https://namelix.com/) 